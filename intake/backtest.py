# ABOUTME: Backtest scaffold comparing an extraction record with a human record (Plan 017).
# ABOUTME: Reports claim recall and precision, locator agreement, and unverified quotes.
"""Compare a supplied extraction record against a human-authored record.

The backtest is the Phase 2 gate's measuring stick. It loads an existing record from
``data/agents/`` and an extraction record produced over the same captures, then
reports claim recall by kind, claim precision, locator agreement with the human
locators, and the number of quotes the verifier could not find. The single-pair
mode takes a supplied extraction record; the batch mode (``--records all``) runs
the writer over every captured record itself, under one budget reservation.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import yaml

from intake import catalog
from intake.capture import HEADER_LINES
from intake.models import ExtractionRecord, StagedSource

LOCATOR_RE = re.compile(r"^Preserved content\.md, lines? (?P<lines>[0-9][0-9, –-]*)$", re.DOTALL)
ROOT = Path(__file__).resolve().parent.parent


def _text_key(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def _family(path: str) -> str:
    """Collapse one rendered claim path to its field family."""
    if re.fullmatch(r"(primitives|key_metrics|lessons_learned|operating_models)\.\d+", path):
        return path.rsplit(".", 1)[0] + "[]"
    return path


def _locator_lines(locator: str | None) -> set[int] | None:
    """Parse the line numbers a human locator names, when it names any."""
    if not locator:
        return None
    match = LOCATOR_RE.fullmatch(" ".join(locator.split()))
    if match is None:
        return None
    numbers = {
        int(value) for value in re.split(r"[,–-]", match.group("lines")) if value.strip().isdigit()
    }
    return numbers or None


def load_human_record(path: Path) -> dict[str, Any]:
    """Load one authored record and its claim fields from ``data/agents/``."""
    record = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        raise ValueError(f"{path}: not a YAML mapping")
    return record


def human_locators(record: dict[str, Any], path: str) -> list[set[int]]:
    """The parsed line sets of every preserved-content locator on one claim path."""
    line_sets = []
    for link in record.get("evidence", {}).get(path, []):
        lines = _locator_lines(link.get("locator"))
        if lines:
            line_sets.append(lines)
    return line_sets


def extraction_lines(record: ExtractionRecord, claim_id: str) -> list[set[int]]:
    """The parsed line sets of one claim's located quotes."""
    line_sets = []
    for claim in record.claims:
        if claim.id != claim_id:
            continue
        for quote in claim.quotes:
            if quote.lines is not None:
                line_sets.append(set(range(quote.lines[0], quote.lines[1] + 1)))
    return line_sets


def compare(
    human: dict[str, Any],
    extraction: ExtractionRecord,
    *,
    compatibility: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    """Produce the backtest report for one record pair.

    ``compatibility`` is the renderer's claim-ID-to-path map; without it the
    comparison falls back to text matching inside each field family.
    """

    build = catalog.load_build()
    human_claims = build.claim_fields(human)
    path_of: dict[str, list[str]] = compatibility or {}

    matches: list[dict[str, Any]] = []
    matched_human: set[str] = set()
    unmatched_extraction: list[str] = []
    for claim in extraction.claims:
        if claim.id is None:
            raise ValueError("run intake.models.finalize before comparing")
        candidates = [
            path for path in path_of.get(claim.id, []) if path in human_claims
        ] or _match_by_text(human_claims, claim)
        if candidates:
            best = candidates[0]
            matched_human.add(best)
            matches.append(
                {
                    "claim_id": claim.id,
                    "human_path": best,
                    "kind": claim.kind,
                    "locator_agrees": _locator_agrees(
                        human_locators(human, best), extraction_lines(extraction, claim.id)
                    ),
                }
            )
        else:
            unmatched_extraction.append(claim.id)

    recall_by_kind: dict[str, dict[str, int]] = {}
    for path, (_text, kind, _provenance) in human_claims.items():
        bucket = recall_by_kind.setdefault(kind, {"human": 0, "found": 0})
        bucket["human"] += 1
        if path in matched_human:
            bucket["found"] += 1
    located_matches = [match for match in matches if match["locator_agrees"] is not None]
    agreeing = [match for match in located_matches if match["locator_agrees"]]
    unverified_quotes = sum(
        1 for claim in extraction.claims for quote in claim.quotes if quote.match != "exact"
    )
    return {
        "format_version": 1,
        "human_claims": len(human_claims),
        "extraction_claims": len(extraction.claims),
        "matched_claims": len(matches),
        "claim_recall_by_kind": {
            kind: {
                "found": bucket["found"],
                "human": bucket["human"],
                "recall": round(bucket["found"] / bucket["human"], 4) if bucket["human"] else None,
            }
            for kind, bucket in sorted(recall_by_kind.items())
        },
        "claim_precision": round(len(matches) / len(extraction.claims), 4)
        if extraction.claims
        else None,
        "unmatched_extraction_claims": unmatched_extraction,
        "missed_human_paths": sorted(set(human_claims) - matched_human),
        "locator_agreement": {
            "compared": len(located_matches),
            "agreeing": len(agreeing),
            "agreement": round(len(agreeing) / len(located_matches), 4)
            if located_matches
            else None,
        },
        "unverified_quotes": unverified_quotes,
    }


def _match_by_text(human_claims: dict[str, tuple[str, str, str]], claim: Any) -> list[str]:
    """Match one extraction claim to a human claim path by normalized text."""
    key = _text_key(claim.text)
    exact = [path for path, (text, _k, _p) in human_claims.items() if _text_key(text) == key]
    if exact:
        return exact
    family = _family(claim.field)
    contained = [
        path
        for path, (text, _k, _p) in human_claims.items()
        if _family(path) == family and key and (key in _text_key(text) or _text_key(text) in key)
    ]
    return contained


def _locator_agrees(human_sets: list[set[int]], extraction_sets: list[set[int]]) -> bool | None:
    """Whether any extraction quote range overlaps any human locator line set."""
    if not human_sets or not extraction_sets:
        return None
    return any(human & extraction for human in human_sets for extraction in extraction_sets)


def report_text(report: dict[str, Any]) -> str:
    """Render one backtest report as the Markdown block the review sheet embeds."""
    recall = report["claim_recall_by_kind"]
    recall_lines = "\n".join(
        f"| {kind} | {bucket['found']} of {bucket['human']} "
        f"| {bucket['recall'] if bucket['recall'] is not None else '—'} |"
        for kind, bucket in recall.items()
    )
    locator = report["locator_agreement"]
    return "\n".join(
        [
            f"Human claims: {report['human_claims']}; extraction claims: "
            f"{report['extraction_claims']}; matched: {report['matched_claims']}.",
            f"Claim precision: {report['claim_precision']}.",
            "",
            "| Kind | Found | Recall |",
            "| --- | --- | --- |",
            recall_lines,
            "",
            f"Locator agreement: {locator['agreeing']} of {locator['compared']} compared "
            f"({locator['agreement'] if locator['agreement'] is not None else '—'}).",
            f"Unverified quotes: {report['unverified_quotes']}.",
        ]
    )


def main(argv: list[str] | None = None) -> int:
    """Run the backtest scaffold from the command line."""
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, required=True, help="human record YAML")
    parser.add_argument("--extraction", type=Path, required=True, help="extraction record YAML")
    parser.add_argument("--compatibility", type=Path, help="renderer compatibility JSON")
    parser.add_argument("--output", type=Path, help="write the JSON report to a file")
    args = parser.parse_args(argv)

    human = load_human_record(args.record)
    extraction = ExtractionRecord.model_validate(
        yaml.safe_load(args.extraction.read_text(encoding="utf-8"))
    )
    compatibility = None
    if args.compatibility is not None:
        compatibility = json.loads(args.compatibility.read_text(encoding="utf-8"))
    report = compare(human, extraction, compatibility=compatibility)
    text = json.dumps(report, indent=2) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(text, end="")
    print(report_text(report))
    return 0


def _body_sha256(bundle: Path) -> str:
    """Hash the capture body the way staging does, header excluded."""
    lines = (bundle / "content.md").read_text(encoding="utf-8").splitlines()
    body = "\n".join(lines[HEADER_LINES:]) if len(lines) > HEADER_LINES else ""
    return f"sha256:{hashlib.sha256(body.encode('utf-8')).hexdigest()}"


def staged_sources_of(
    record: dict[str, Any], bundles: dict[str, Path]
) -> tuple[list[StagedSource], dict[str, str]]:
    """One staged source per captured source, keyed ``s1, s2, ...`` locally.

    Returns the staged sources and the archive-source-ID to local-ID map, so
    the writer and the quote verifier speak the same local keys a run uses.
    """
    staged: list[StagedSource] = []
    local_of: dict[str, str] = {}
    for index, source in enumerate(record.get("sources", []), start=1):
        bundle = bundles.get(source.get("id"))
        if bundle is None:
            continue
        local = f"s{index}"
        local_of[source["id"]] = local
        staged.append(
            StagedSource(
                local_id=local,
                title=source.get("title") or source["id"],
                url=source["url"],
                canonical_url=source.get("canonical_url") or source["url"],
                kind=source.get("kind", "other"),
                provenance_class=source.get("provenance_class", "independent-secondary"),
                published_at=source.get("published_at"),
                content_sha256=_body_sha256(bundle),
            )
        )
    return staged, local_of


def run_batch(
    *,
    adapter: Any,
    budget: Any,
    records_root: Path | None = None,
) -> dict[str, Any]:
    """Backtest every captured record: extract with the writer, then compare.

    Records without captures are skipped and listed. One budget reservation
    covers the whole batch; when it refuses, the batch stops and reports what
    completed. A writer failure stops the batch the way it stops a run.
    """

    from intake.adapters.writer import WriterApiError
    from intake.backfill import capture_paragraphs, capture_sources, load_record
    from intake.budget import BudgetExceededError, new_run_id
    from intake.extract import run_extract
    from intake.models import finalize
    from intake.verify_quotes import verify_claims

    root = records_root or (ROOT / "data" / "agents")
    run_id = new_run_id()
    rows: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    stopped: dict[str, str] | None = None
    for path in sorted(root.glob("*.yaml")):
        record = load_record(path)
        bundles = capture_sources(record)
        if not bundles:
            skipped.append({"record": record.get("id"), "reason": "no captured source"})
            continue
        try:
            sources, local_of = staged_sources_of(record, bundles)
            paragraphs = {
                local_of[source_id]: source_paragraphs
                for source_id, source_paragraphs in capture_paragraphs(bundles).items()
            }
            extraction, _stage = run_extract(
                run_id=run_id,
                paragraphs_by_source=paragraphs,
                sources=sources,
                hints={
                    "company": record.get("company"),
                    "system_name": record.get("agent_name"),
                    "record_id": record.get("id"),
                },
                adapter=adapter,
                budget=budget,
            )
            extraction = finalize(extraction)
            extraction = verify_claims(extraction, paragraphs)
            report = compare(record, extraction)
        except BudgetExceededError as error:
            stopped = {"reason": "budget", "detail": str(error)}
            break
        except WriterApiError as error:
            stopped = {"reason": "writer", "detail": str(error)}
            break
        rows.append({"record": record.get("id"), **report})

    totals = {
        "records": len(rows),
        "human_claims": sum(row["human_claims"] for row in rows),
        "extraction_claims": sum(row["extraction_claims"] for row in rows),
        "matched_claims": sum(row["matched_claims"] for row in rows),
        "unverified_quotes": sum(row["unverified_quotes"] for row in rows),
        "locator_compared": sum(row["locator_agreement"]["compared"] for row in rows),
        "locator_agreeing": sum(row["locator_agreement"]["agreeing"] for row in rows),
    }
    by_kind: dict[str, dict[str, int]] = {}
    for row in rows:
        for kind, bucket in row["claim_recall_by_kind"].items():
            entry = by_kind.setdefault(kind, {"human": 0, "found": 0})
            entry["human"] += bucket["human"]
            entry["found"] += bucket["found"]
    return {
        "format_version": 1,
        "run_id": run_id,
        "records": len(rows),
        "skipped": skipped,
        "stopped": stopped,
        "totals": totals,
        "claim_recall_by_kind": {
            kind: {
                "found": bucket["found"],
                "human": bucket["human"],
                "recall": round(bucket["found"] / bucket["human"], 4) if bucket["human"] else None,
            }
            for kind, bucket in sorted(by_kind.items())
        },
        "rows": rows,
    }


def batch_report_text(report: dict[str, Any]) -> str:
    """Render the batch backtest report as the Markdown sheet a reviewer reads."""
    totals = report["totals"]
    recall = totals["matched_claims"] / totals["human_claims"] if totals["human_claims"] else None
    precision = (
        totals["matched_claims"] / totals["extraction_claims"]
        if totals["extraction_claims"]
        else None
    )
    agreement = (
        totals["locator_agreeing"] / totals["locator_compared"]
        if totals["locator_compared"]
        else None
    )
    lines = [
        f"# Backtest batch {report['run_id']}",
        "",
        f"{report['records']} records backtested; {len(report['skipped'])} skipped.",
        "",
        f"Matched claims: {totals['matched_claims']} of {totals['human_claims']} human "
        f"(recall {round(recall, 4) if recall is not None else '—'}); "
        f"precision {round(precision, 4) if precision is not None else '—'}.",
        f"Locator agreement: {totals['locator_agreeing']} of {totals['locator_compared']} "
        f"compared ({round(agreement, 4) if agreement is not None else '—'}). "
        f"Unverified quotes: {totals['unverified_quotes']}.",
        "",
        "| Record | Human | Extraction | Matched | Unverified |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in report["rows"]:
        lines.append(
            f"| {row['record']} | {row['human_claims']} | {row['extraction_claims']} "
            f"| {row['matched_claims']} | {row['unverified_quotes']} |"
        )
    for entry in report["skipped"]:
        lines.append(f"- skipped `{entry['record']}`: {entry['reason']}")
    if report["stopped"] is not None:
        lines.append(
            f"- stopped early: {report['stopped']['reason']} — {report['stopped']['detail']}"
        )
    lines.append("")
    lines.append("A measurement only; nothing was applied.")
    return "\n".join(lines) + "\n"
