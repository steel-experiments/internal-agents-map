# ABOUTME: Eligibility proposal over accepted claims (Plan 017 decision policy).
# ABOUTME: Categorical questions only; no score; a person decides.
"""Propose Add, Update, Needs evidence, or Out of scope for one candidate.

The contribution guide's inclusion questions are categorical: which
organization uses the system and for what internal work; what that
organization built or materially adapted; what implementation or use the
source describes. This module checks what code can check — the organization
name, the accepted claims, and the writer's own scope proposal — and leaves
the semantic judgement to the reviewer with the reasons spelled out. It never
produces a numerical score.
"""

from __future__ import annotations

from typing import Any

# Claim families that describe an implementation or a use of the system.
USE_FIELD_PREFIXES = ("architecture.",)
USE_FIELD_NAMES = ("primitives[]", "operating_models[]")


def _describes_use(record: Any) -> bool:
    """Whether an accepted claim or a reader answer describes use."""
    for claim in record.claims:
        if claim.disposition != "accept":
            continue
        if claim.field in USE_FIELD_NAMES or claim.field.startswith(USE_FIELD_PREFIXES):
            return True
    questions = record.questions
    return bool(questions and (questions.implementation.claim_ids or questions.workflow.claim_ids))


def propose_eligibility(record: Any) -> dict[str, Any]:
    """The eligibility proposal with reasons; the reviewer decides."""
    writer_decision = record.candidate.decision
    if not record.candidate.company:
        return {
            "decision": "needs-evidence",
            "writer_decision": writer_decision,
            "reasons": [
                "inclusion question 1: no organization is named in the candidate or the text"
            ],
        }
    accepted = [claim for claim in record.claims if claim.disposition == "accept"]
    if not accepted:
        return {
            "decision": "needs-evidence",
            "writer_decision": writer_decision,
            "reasons": [
                "no claim passed quote verification and the coarse gate, so "
                "nothing establishes a build or an adaptation"
            ],
        }
    if writer_decision == "out-of-scope":
        return {
            "decision": "out-of-scope",
            "writer_decision": writer_decision,
            "reasons": [
                "the writer proposed out-of-scope; a person names which "
                "inclusion rule fails before the proposal stands"
            ],
        }
    reasons = [
        f"inclusion question 2: {len(accepted)} accepted claims establish "
        "what the organization built or adapted"
    ]
    if _describes_use(record):
        reasons.append(
            "inclusion question 3: an accepted claim or a reader answer "
            "describes the implementation or the use"
        )
    else:
        reasons.append(
            "inclusion question 3: no accepted claim describes the "
            "implementation or the use; a person confirms it against the sources"
        )
    decision = writer_decision if writer_decision in ("add", "update") else "needs-evidence"
    return {
        "decision": decision,
        "writer_decision": writer_decision,
        "reasons": reasons,
    }
