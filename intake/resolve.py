# ABOUTME: Stage 3 of the intake pipeline: resolve identity (Plan 017).
# ABOUTME: Deterministic company and system-name matching; Jev joins in Phase 3.
"""Shortlist the existing records a candidate most likely belongs to.

Identity is deterministic here: company and system names are normalised and
matched against the company registry, the records, and their aliases. A
shortlist with scores becomes the identity file; the proposed decision names
Add, Update, or review, and a person confirms every identity decision.
"""

from __future__ import annotations

import re
from typing import Any

from intake.catalog import load_build

EXACT_SCORE = 1.0
CONTAINS_SCORE = 0.85
MIN_SHORTLIST_SCORE = 0.5


def normalize_name(value: str) -> str:
    """Case-fold, drop punctuation, and collapse whitespace."""
    lowered = value.casefold()
    without_punct = re.sub(r"[^\w\s]", " ", lowered)
    return re.sub(r"\s+", " ", without_punct).strip()


def _tokens(value: str) -> set[str]:
    return set(normalize_name(value).split())


def name_score(hint: str, target: str) -> float:
    """Score one name pair: exact, containment, or token overlap."""
    left = normalize_name(hint)
    right = normalize_name(target)
    if not left or not right:
        return 0.0
    if left == right:
        return EXACT_SCORE
    if left in right or right in left:
        return CONTAINS_SCORE
    left_tokens = _tokens(hint)
    right_tokens = _tokens(target)
    if not left_tokens or not right_tokens:
        return 0.0
    overlap = len(left_tokens & right_tokens)
    if not overlap:
        return 0.0
    return round(overlap / max(len(left_tokens), len(right_tokens)), 4)


def match_company(
    company_hint: str | None,
    *,
    companies: list[dict[str, Any]],
    text: str = "",
) -> dict[str, Any] | None:
    """Find the registry entry for the company hint or a company named in the text."""
    candidates: list[tuple[float, dict[str, Any]]] = []
    for company in companies:
        best = name_score(company_hint or "", company["name"])
        if text and company["name"].casefold() in text.casefold():
            best = max(best, CONTAINS_SCORE)
        if best >= MIN_SHORTLIST_SCORE:
            candidates.append((best, company))
    if not candidates:
        return None
    best_score = max(score for score, _ in candidates)
    winners = [company for score, company in candidates if score == best_score]
    if len(winners) > 1:
        return None
    return winners[0]


def resolve_identity(
    *,
    company: str | None = None,
    system_name: str | None = None,
    text: str = "",
    records: list[dict[str, Any]] | None = None,
    companies: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Produce the identity file contents for one queue candidate."""
    build = load_build()
    if records is None:
        records = build.load_agents()
    if companies is None:
        companies = build.load_companies(records)
    matched_company = match_company(company, companies=companies, text=text)
    shortlist: list[dict[str, Any]] = []
    for record in records:
        if matched_company is not None and record["company"] != matched_company["name"]:
            continue
        names = [record["agent_name"], *(record.get("aliases") or [])]
        best = max((name_score(system_name or "", name) for name in names), default=0.0)
        if text and not system_name:
            best = max(best, max((name_score(name, text) for name in names), default=0.0))
        if best < MIN_SHORTLIST_SCORE:
            continue
        shortlist.append(
            {
                "id": record["id"],
                "agent_name": record["agent_name"],
                "aliases": record.get("aliases") or [],
                "score": best,
                "reason": (
                    "company and system name match"
                    if matched_company is not None
                    else "system name matches without a company match"
                ),
            }
        )
    shortlist.sort(key=lambda item: (-item["score"], item["id"]))
    shortlist = shortlist[:5]
    if matched_company is None:
        decision = "needs-evidence"
    elif shortlist:
        top = shortlist[0]["score"]
        unique_top = len(shortlist) == 1 or shortlist[1]["score"] < top
        decision = "update" if top >= CONTAINS_SCORE and unique_top else "review"
    else:
        decision = "add"
    return {
        "format_version": 1,
        "company_hint": company,
        "system_name_hint": system_name,
        "company": (
            {"id": matched_company["id"], "name": matched_company["name"]}
            if matched_company
            else None
        ),
        "matched_records": shortlist,
        "proposed_decision": decision,
        "note": (
            "Deterministic name matching only; the Jev same-system question and the "
            "reviewer confirm every identity decision."
        ),
    }
