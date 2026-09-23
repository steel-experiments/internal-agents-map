# ABOUTME: Command line for the source intake pipeline (Plan 017).
# ABOUTME: Each stage is a separate command with its own budget, cache, and manifest.
"""Run the intake pipeline stages: ``uv run python -m intake <command>``."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from intake import models

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "intake" / "schemas" / "extraction-record.v1.json"


def _command_schema(args: argparse.Namespace) -> int:
    payload = {
        "extraction_record": models.ExtractionRecord.model_json_schema(),
        "run_manifest": models.RunManifest.model_json_schema(),
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(text, end="")
    return 0


def _command_render(args: argparse.Namespace) -> int:
    from intake.models import finalize
    from intake.render import render_extraction

    extraction = models.ExtractionRecord.model_validate(
        yaml.safe_load(args.extraction.read_text(encoding="utf-8"))
    )
    extraction = finalize(extraction)
    result = render_extraction(extraction, reviewed_at=args.reviewed_at)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result.record_yaml, encoding="utf-8")
    print(f"wrote {args.output}")
    if args.compatibility is not None:
        args.compatibility.parent.mkdir(parents=True, exist_ok=True)
        args.compatibility.write_text(
            json.dumps(result.compatibility, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {args.compatibility}")
    if result.company_entry is not None:
        company_yaml = yaml.safe_dump(
            [result.company_entry], sort_keys=False, allow_unicode=True, width=100
        )
        print("company entry (append to data/companies.yaml, keep the list sorted by id):")
        print(company_yaml, end="")
    for note in result.notes:
        print(f"note: {note}")
    return 0


def _command_backtest(args: argparse.Namespace) -> int:
    from intake.adapters.writer import WriterAdapter
    from intake.backtest import batch_report_text, run_batch
    from intake.backtest import main as backtest_main
    from intake.budget import Budget

    if args.records == "all":
        report = run_batch(adapter=WriterAdapter(), budget=Budget(budget_usd=args.budget_usd))
        text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if args.output is not None:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
            print(f"wrote {args.output}")
        print(batch_report_text(report), end="")
        return 0
    if args.record is None or args.extraction is None:
        print("backtest needs --record and --extraction, or --records all", file=sys.stderr)
        return 2
    return backtest_main(
        [
            "--record",
            str(args.record),
            "--extraction",
            str(args.extraction),
            *(["--compatibility", str(args.compatibility)] if args.compatibility else []),
            *(["--output", str(args.output)] if args.output else []),
        ]
    )


def _command_capture(args: argparse.Namespace) -> int:
    from intake.capture import capture_staging

    staged = capture_staging(args.url, pdf=args.pdf)
    print(
        json.dumps(
            {
                "staging_dir": str(staged.staging_dir),
                "canonical_url": staged.canonical_url,
                "captured_at": staged.captured_at,
                "content_sha256": staged.content_sha256,
            },
            indent=2,
        )
    )
    return 0


def _command_promote(args: argparse.Namespace) -> int:
    from intake.capture import promote

    manifest = promote(args.staging_dir, args.source_id)
    print(f"promoted {args.staging_dir} -> {manifest}")
    return 0


def _command_segment(args: argparse.Namespace) -> int:
    from intake.segment import paragraphs_json, segment_content

    paragraphs = segment_content(args.input.read_text(encoding="utf-8"))
    payload = paragraphs_json(paragraphs)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
        print(f"wrote {args.output} ({len(paragraphs)} paragraphs)")
    else:
        print(payload, end="")
    return 0


def _command_resolve(args: argparse.Namespace) -> int:
    from intake.resolve import refine_with_jev, resolve_identity

    text = args.text_file.read_text(encoding="utf-8") if args.text_file else (args.text or "")
    identity = resolve_identity(company=args.company, system_name=args.system, text=text)
    if args.jev and identity["matched_records"]:
        from intake.adapters.jev import JevAdapter
        from intake.budget import Budget
        from intake.cache import jev_cache

        identity = refine_with_jev(
            identity,
            passage=text[:8000],
            candidate_name=args.system or args.company or "the candidate",
            adapter=JevAdapter(),
            budget=Budget(budget_usd=args.budget_usd),
            cache=jev_cache(),
        )
    payload = json.dumps(identity, indent=2, ensure_ascii=False) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(payload, end="")
    return 0


def _command_run(args: argparse.Namespace) -> int:
    from intake.run import run_queue

    summaries = run_queue(args.queue, budget_usd=args.budget_usd)
    for summary in summaries:
        print(
            f"{summary.run_id}: {summary.decision}"
            + (f" -> {summary.draft_path}" if summary.draft_path else " (no draft; see sheet)")
        )
        print(f"  sheet: {summary.sheet_path}")
        for note in summary.notes:
            print(f"  note: {note}")
    return 0


def _command_stage(args: argparse.Namespace) -> int:
    from intake.stage import run_stage

    return run_stage(args.name, args.run)


def _command_review(args: argparse.Namespace) -> int:
    from intake.review import load_review

    print(load_review(args.run_id), end="")
    return 0


def _command_backfill(args: argparse.Namespace) -> int:
    import os

    from intake.adapters.jev import JevAdapter
    from intake.adapters.writer import WriterAdapter
    from intake.backfill import backfill_dry_run, proposals_payload, review_sheet
    from intake.budget import Budget
    from intake.cache import jev_cache, writer_cache

    budget = Budget(budget_usd=args.budget_usd)
    # Stage 6 grades each proposal; without the key the sheet says so.
    jev = JevAdapter() if os.environ.get("TYPESAFE_API_KEY") else None
    if jev is None:
        print("note: TYPESAFE_API_KEY is not set; proposals skip the judge (stage 6).")
    report = backfill_dry_run(
        args.record,
        adapter=WriterAdapter(),
        budget=budget,
        jev=jev,
        cache=jev_cache(),
        writer_cache=writer_cache(),
    )
    sheet = review_sheet(report)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(sheet, encoding="utf-8")
        print(f"wrote {args.output}")
    if args.proposals is not None:
        import json

        args.proposals.parent.mkdir(parents=True, exist_ok=True)
        args.proposals.write_text(
            json.dumps(proposals_payload(report), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {args.proposals} (every entry starts unapproved)")
    print(sheet, end="")
    return 0


def _command_backfill_apply(args: argparse.Namespace) -> int:
    from intake.apply import apply_proposals, load_proposals

    changed = apply_proposals(load_proposals(args.proposals))
    for path in changed:
        print(f"updated locators in {path}")
    print("Regenerate the data outputs and open the pull request yourself.")
    return 0


def _command_drift(args: argparse.Namespace) -> int:
    from intake.adapters.jev import JevAdapter
    from intake.adapters.steel import SteelSdkAdapter
    from intake.budget import Budget
    from intake.drift import drift_report, report_markdown

    payload = drift_report(
        adapter=SteelSdkAdapter(),
        jev=JevAdapter(),
        budget=Budget(budget_usd=args.budget_usd),
        output=args.output,
    )
    print(report_markdown(payload), end="")
    return 0


def _command_evals(args: argparse.Namespace) -> int:
    from intake.adapters.jev import JevAdapter
    from intake.budget import Budget
    from intake.evals import build_items, labeller_agreement, run_verdicts, score, write_items

    if not args.score:
        items = build_items(count=args.count)
        write_items(items, args.items)
        print(f"wrote {args.items} ({len(items)} items)")
        print(
            "Two labellers fill labels.labeller_a and labels.labeller_b on every item, "
            "then a person fills labels.adjudicated. Then rerun with --score."
        )
        return 0
    items = json.loads(args.items.read_text(encoding="utf-8"))
    verdicts = run_verdicts(items, adapter=JevAdapter(), budget=Budget(budget_usd=args.budget_usd))
    report = score(items, verdicts)
    report["labeller_agreement"] = labeller_agreement(items)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(f"wrote {args.output}")
    agreement = report["labeller_agreement"]
    gate = report["gate"]
    print(f"scored {report['scored']} items ({agreement.get('labelled', 0)} double-labelled)")
    print(
        f"material-defect recall {report['defect_recall']}; "
        f"alert precision {report['alert_precision']}; gate passes: {gate['passes']}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="intake", description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    schema = subparsers.add_parser("schema", help="export the extraction-record JSON schema")
    schema.add_argument("--output", type=Path, default=None, help=f"default: {SCHEMA_PATH}")
    schema.set_defaults(func=_command_schema)

    render = subparsers.add_parser("render", help="render an extraction record to draft YAML")
    render.add_argument("--extraction", type=Path, required=True)
    render.add_argument("--output", type=Path, required=True, help="draft record YAML path")
    render.add_argument("--compatibility", type=Path, help="claim-ID-to-path map JSON")
    render.add_argument("--reviewed-at", required=True, help="review date, YYYY-MM-DD")
    render.set_defaults(func=_command_render)

    backtest = subparsers.add_parser(
        "backtest", help="compare an extraction record with a human record"
    )
    backtest.add_argument("--record", type=Path)
    backtest.add_argument("--extraction", type=Path)
    backtest.add_argument("--compatibility", type=Path)
    backtest.add_argument("--records", choices=["all"], help="backtest every captured record")
    backtest.add_argument("--budget-usd", type=float, default=20.0, help="batch mode budget")
    backtest.add_argument("--output", type=Path)
    backtest.set_defaults(func=_command_backtest)

    capture = subparsers.add_parser("capture", help="scrape one URL into staging")
    capture.add_argument("url")
    capture.add_argument(
        "--pdf", action="store_true", help="also fetch the page PDF when layout evidence matters"
    )
    capture.set_defaults(func=_command_capture)

    promote_command = subparsers.add_parser(
        "promote", help="promote a staging bundle into archive/sources/"
    )
    promote_command.add_argument("staging_dir", type=Path)
    promote_command.add_argument("--source-id", required=True)
    promote_command.set_defaults(func=_command_promote)

    segment = subparsers.add_parser("segment", help="split a capture into paragraphs")
    segment.add_argument("--input", type=Path, required=True, help="capture content.md")
    segment.add_argument("--output", type=Path, help="paragraphs.json path")
    segment.set_defaults(func=_command_segment)

    resolve = subparsers.add_parser("resolve", help="shortlist records for a candidate")
    resolve.add_argument("--company")
    resolve.add_argument("--system")
    resolve.add_argument("--text", help="candidate text, such as the summary")
    resolve.add_argument("--text-file", type=Path)
    resolve.add_argument("--jev", action="store_true", help="add the same-system advisory column")
    resolve.add_argument("--budget-usd", type=float, default=1.0)
    resolve.add_argument("--output", type=Path)
    resolve.set_defaults(func=_command_resolve)

    run = subparsers.add_parser("run", help="run the whole pipeline over a queue file")
    run.add_argument("queue", type=Path)
    run.add_argument("--budget-usd", type=float, default=2.0)
    run.set_defaults(func=_command_run)

    stage = subparsers.add_parser("stage", help="rerun one stage from a run directory")
    stage.add_argument("name", choices=["segment", "resolve", "verify", "render", "review"])
    stage.add_argument("--run", required=True, help="run ID under .intake/runs/")
    stage.set_defaults(func=_command_stage)

    review = subparsers.add_parser("review", help="print one run's review sheet")
    review.add_argument("run_id")
    review.set_defaults(func=_command_review)

    backfill = subparsers.add_parser(
        "backfill", help="propose locators for a record's unlocated claims (dry run)"
    )
    backfill.add_argument("record", type=Path)
    backfill.add_argument("--budget-usd", type=float, default=10.0)
    backfill.add_argument("--output", type=Path)
    backfill.add_argument(
        "--proposals", type=Path, help="write the proposal list backfill-apply consumes"
    )
    backfill.set_defaults(func=_command_backfill)

    backfill_apply = subparsers.add_parser(
        "backfill-apply", help="apply approved locator proposals (locator fields only)"
    )
    backfill_apply.add_argument("proposals", type=Path)
    backfill_apply.set_defaults(func=_command_backfill_apply)

    drift = subparsers.add_parser(
        "drift", help="rescrape captures and report changed sources and affected claims"
    )
    drift.add_argument(
        "--budget-usd", type=float, default=5.0, help="budget for the advisory claim re-judging"
    )
    drift.add_argument("--output", type=Path)
    drift.set_defaults(func=_command_drift)

    evals = subparsers.add_parser("evals", help="build and score the adjudicated Jev evaluation")
    evals.add_argument("--items", type=Path, required=True, help="the item set JSON path")
    evals.add_argument("--count", type=int, default=120, help="items to sample")
    evals.add_argument(
        "--score", action="store_true", help="judge the labelled items and score the gate"
    )
    evals.add_argument("--budget-usd", type=float, default=20.0)
    evals.add_argument("--output", type=Path)
    evals.set_defaults(func=_command_evals)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
