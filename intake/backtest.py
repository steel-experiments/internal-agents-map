# ABOUTME: Backtest scaffold comparing an extraction record with a human record (Plan 017).
# ABOUTME: Reports claim recall and precision, locator agreement, and unverified quotes.
"""Compare a supplied extraction record against a human-authored record.

The backtest is the Phase 2 gate's measuring stick. It loads an existing record from
``data/agents/`` and an extraction record produced over the same captures, then
reports claim recall by kind, claim precision, locator agreement with the human
locators, and the number of quotes the verifier could not find. No model call
happens here; the caller supplies the extraction record.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

from intake import catalog
from intake.models import ExtractionRecord

LOCATOR_RE = re.compile(r"^Preserved content\.md, lines? (?P<lines>[0-9][0-9, –-]*)$", re.DOTALL)


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
