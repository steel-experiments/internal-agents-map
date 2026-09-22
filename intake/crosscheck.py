# ABOUTME: Update-path cross checks: the new source against the existing record.
# ABOUTME: The evidential-independence gap: numbers must agree across sources.
"""Compare an update's new claims against the record it proposes to update.

The gap analysis names evidential independence as a research gap: records
cite one source and almost never contradict each other. When a run proposes
an Update, its claims are matched against the existing record's claims by
text; a matched pair whose numbers differ is a contradiction a reviewer must
see before the merge. The checks are advisory flags on the review sheet —
they never edit, drop, or reorder anything.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from intake.models import ExtractionRecord

ROOT = Path(__file__).resolve().parent.parent


def load_existing(record_id: str | None, *, root: Path | None = None) -> dict[str, Any] | None:
    """The existing record an update names, when it exists on disk."""
    if not record_id:
        return None
    path = (root or ROOT / "data" / "agents") / f"{record_id}.yaml"
    if not path.is_file():
        return None
    record = yaml.safe_load(path.read_text(encoding="utf-8"))
    return record if isinstance(record, dict) else None


def source_count(record: dict[str, Any]) -> int:
    """How many sources the existing record already carries."""
    return len(record.get("sources") or [])


def _values(text: str) -> set[float]:
    from intake.numbers import extract_numbers

    return {number.value for number in extract_numbers(text)}


def _masked_key(text: str) -> str:
    """A text key with digits masked, so claims differing only in their
    numbers still align."""
    import re

    collapsed = re.sub(r"\s+", " ", text).strip().casefold()
    return re.sub(r"\d+(?:[.,]\d+)?", "#", collapsed)


def _match_paths(old_claims: dict[str, tuple[str, str, str]], field: str, text: str) -> list[str]:
    """Match one new claim to existing claim paths, digits masked."""
    from intake.backtest import _family

    key = _masked_key(text)
    family = _family(field)
    exact = [path for path, (old, _k, _p) in old_claims.items() if _masked_key(old) == key]
    if exact:
        return exact
    return [
        path
        for path, (old, _k, _p) in old_claims.items()
        if _family(path) == family and key and (key in _masked_key(old) or _masked_key(old) in key)
    ]


def number_conflicts(
    existing: dict[str, Any],
    record: ExtractionRecord,
    *,
    build: Any = None,
) -> list[dict[str, Any]]:
    """Flag matched claim pairs whose numbers disagree.

    A pair matches when the new claim's text matches an existing claim path
    with digits masked, so a restated metric with a new value still aligns.
    Both sides carrying numbers with nothing in common is a contradiction;
    the old side carrying numbers the new claim drops is a softer note.
    """
    if build is None:
        from intake.catalog import load_build

        build = load_build()
    old_claims = build.claim_fields(existing)
    flags: list[dict[str, Any]] = []
    for claim in record.claims:
        if not claim.quotes:
            continue
        candidates = _match_paths(old_claims, claim.field, claim.text)
        if not candidates:
            continue
        path = candidates[0]
        old_values = _values(old_claims[path][0])
        new_values = _values(claim.text)
        quotes = [
            {"source": quote.source, "lines": list(quote.lines)}
            for quote in claim.quotes
            if quote.match == "exact" and quote.lines
        ]
        if old_values and new_values and not (old_values & new_values):
            flags.append(
                {
                    "claim_path": path,
                    "issue": "numbers differ",
                    "existing": sorted(old_values),
                    "new": sorted(new_values),
                    "quotes": quotes,
                }
            )
        elif old_values and not new_values:
            flags.append(
                {
                    "claim_path": path,
                    "issue": "the new claim drops the recorded numbers",
                    "existing": sorted(old_values),
                    "new": [],
                }
            )
    return flags
