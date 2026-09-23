# ABOUTME: Stage 3 of the intake pipeline: resolve identity (Plan 017).
# ABOUTME: Deterministic company and system-name matching; Jev joins in Phase 3.
"""Shortlist the existing records a candidate most likely belongs to.

Identity is deterministic here: company and system names are normalised and
matched against the company registry, the records, and their aliases. A
shortlist with scores becomes the identity file; the proposed decision names
Add, Update, or review, and a person confirms every identity decision.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from intake.catalog import load_build

EXACT_SCORE = 1.0
CONTAINS_SCORE = 0.85
MIN_SHORTLIST_SCORE = 0.5
IDENTITY_QUESTION_VERSION = 1
# The decision policy's identity bands: a same-system probability at or
# above the update bound proposes Update, one below the add bound proposes
# Add, and a value between proposes review. Provisional until the Phase 3
# calibration runs — the same honesty the judge's GATE carries — and the
# deterministic scores stay as columns beside them.
IDENTITY_GATE = {
    "model": "jev-1.13.0",
    "question_version": IDENTITY_QUESTION_VERSION,
    "calibrated": False,
    "update_min": 0.8,
    "add_max": 0.3,
}


def _with_identity_decision(identity: dict[str, Any]) -> dict[str, Any]:
    """Apply the decision policy's Jev bands to the proposed decision.

    The bands read the shortlist's top entry, whose Jev answer exists only
    after refinement. Without an answer the deterministic decision stands
    and the basis says so. The reviewer confirms every identity decision
    either way; the sheet lists both columns.
    """
    top = identity["matched_records"][0]
    probability = top.get("same_system_jev")
    if probability is None:
        return identity | {"decision_basis": {"rule": "deterministic"}}
    if probability >= IDENTITY_GATE["update_min"]:
        decision = "update"
    elif probability < IDENTITY_GATE["add_max"]:
        decision = "add"
    else:
        decision = "review"
    return identity | {
        "proposed_decision": decision,
        "decision_basis": {
            "rule": "jev-identity-bands",
            "update_min": IDENTITY_GATE["update_min"],
            "add_max": IDENTITY_GATE["add_max"],
            "top_same_system_jev": probability,
            "record": top["id"],
            "calibrated": IDENTITY_GATE["calibrated"],
        },
    }


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
    named_new_organization = matched_company is None and bool((company or "").strip())
    if matched_company is None and not named_new_organization:
        # The stage 3 contract: no company name in the text or the hints.
        decision = "needs-evidence"
        note = (
            "No company name in the hints or the text; needs evidence. A person "
            "names the organization and reruns the queue entry."
        )
    elif named_new_organization:
        # The Add path: a company the registry does not know, named by the
        # queue hint. The company-entry output covers the registry gap.
        decision = "add"
        note = (
            "The company hint names an organization the registry does not know; "
            "proposing add for a new organization."
        )
    elif shortlist:
        top = shortlist[0]["score"]
        unique_top = len(shortlist) == 1 or shortlist[1]["score"] < top
        decision = "update" if top >= CONTAINS_SCORE and unique_top else "review"
        note = (
            "Deterministic name matching only; the Jev same-system question and the "
            "reviewer confirm every identity decision."
        )
    else:
        decision = "add"
        note = (
            "Deterministic name matching only; the Jev same-system question and the "
            "reviewer confirm every identity decision."
        )
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
        "note": note,
    }


def jev_identity_questions(
    candidate_name: str, shortlist: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    """The Design 2 identity question for every shortlisted record."""
    questions: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(shortlist):
        record = f"{entry['agent_name']} ({entry['id']})"
        questions[f"same_{index}"] = {
            "type": "noul",
            "instructions": (
                f"Does the passage describe {record} as the same system and version "
                f"as {candidate_name}, rather than merely the same company?"
            ),
        }
    return questions


def refine_with_jev(
    identity: dict[str, Any],
    *,
    passage: str,
    candidate_name: str,
    adapter: Any,
    budget: Any,
    cache: Any = None,
) -> dict[str, Any]:
    """Add the Jev same-system probability to every shortlist entry.

    The deterministic scores stay; Jev's answer is one advisory column that the
    reviewer reads beside them. With a cache, a warm rerun makes no new calls.
    """

    shortlist = identity["matched_records"]
    if not shortlist:
        return identity
    if cache is not None:
        from intake.cache import cache_key

        fingerprint = json.dumps(
            [{"id": entry["id"], "agent_name": entry.get("agent_name")} for entry in shortlist],
            sort_keys=True,
        )
        passage_hash = f"sha256:{hashlib.sha256(passage.encode('utf-8')).hexdigest()}"
        key = cache_key(
            candidate_name,
            passage_hash,
            fingerprint,
            f"identity-v{IDENTITY_QUESTION_VERSION}",
        )
        cached = cache.get(key)
        if cached is not None:
            return _with_identity_decision(
                identity
                | {
                    "matched_records": cached["matched_records"],
                    "jev_model": cached["usage"]["model"],
                    "jev_usage": cached["usage"] | {"cache_hit": True},
                }
            )
    result = adapter.ask(
        state={"candidate": candidate_name, "passage": passage},
        questions=jev_identity_questions(candidate_name, shortlist),
        budget=budget,
    )
    refined = []
    for index, entry in enumerate(shortlist):
        answer = result.answers.get(f"same_{index}")
        refined.append(entry | {"same_system_jev": answer.noul if answer else None})
    usage = {
        "model": result.model,
        "input_tokens": result.input_tokens,
        "cost_usd": round(result.cost_usd, 6),
        "cache_hit": False,
        "input_sha256": result.input_sha256,
    }
    if cache is not None:
        cache.put(key, {"matched_records": refined, "usage": usage})
    return _with_identity_decision(
        identity
        | {
            "matched_records": refined,
            "jev_model": result.model,
            "jev_usage": usage,
        }
    )
