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
    from intake.backtest import main as backtest_main

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
    backtest.add_argument("--record", type=Path, required=True)
    backtest.add_argument("--extraction", type=Path, required=True)
    backtest.add_argument("--compatibility", type=Path)
    backtest.add_argument("--output", type=Path)
    backtest.set_defaults(func=_command_backtest)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
