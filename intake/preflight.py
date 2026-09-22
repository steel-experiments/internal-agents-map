# ABOUTME: Stage 9 of the intake pipeline: preflight the written draft (Plan 017).
# ABOUTME: Consumes the stage-6 relation verdicts; flags, never rewrites.
"""Preflight the draft against the claims' evidence.

The plan's stage 9 checks each written sentence against the quotes of its
claims with the relation question. In this pipeline the claim prose comes from
stage 4 and is judged by the same relation question in stage 6, so preflight
consumes those verdicts instead of asking the question twice on the same
passage: a ``conflicts`` verdict or a ``stated`` probability below the gate
sends the claim to the review sheet. Stage 8's own output is confidence
reasons, which carry no factual prose; their numbers were checked at write
time. Nothing here rewrites the draft.
"""

from __future__ import annotations

from dataclasses import dataclass

from intake.judge import GATE
from intake.models import ExtractionRecord
from intake.render import RenderResult


@dataclass(frozen=True)
class PreflightFlag:
    """One preflight finding for the review sheet."""

    claim_id: str
    field: str
    issue: str


def preflight_flags(
    record: ExtractionRecord, result: RenderResult, *, gate: dict | None = None
) -> list[PreflightFlag]:
    """Flag every rendered claim whose relation verdict is weak or conflicting."""
    policy = gate or GATE
    flags: list[PreflightFlag] = []
    for claim_id, paths in result.compatibility.items():
        claim = record.claim_by_id(claim_id)
        judgments = claim.judgments
        if judgments is None or judgments.relation is None:
            flags.append(
                PreflightFlag(
                    claim_id=claim_id,
                    field=claim.field,
                    issue="no relation verdict; the claim was never judged",
                )
            )
            continue
        relation = judgments.relation
        if relation.label == "conflicts":
            flags.append(
                PreflightFlag(
                    claim_id=claim_id,
                    field=claim.field,
                    issue=f"the passage explicitly conflicts (p={relation.p:.2f})",
                )
            )
        elif relation.label != "stated" or relation.p < policy["relation_stated_min"]:
            flags.append(
                PreflightFlag(
                    claim_id=claim_id,
                    field=claim.field,
                    issue=(
                        f"relation is {relation.label} at p={relation.p:.2f}, below the "
                        f"{policy['relation_stated_min']} gate"
                    ),
                )
            )
        if (judgments.actor_mismatch or 0.0) > policy["actor_mismatch_max"]:
            flags.append(
                PreflightFlag(
                    claim_id=claim_id,
                    field=claim.field,
                    issue=(
                        f"possible actor mismatch (p={judgments.actor_mismatch:.2f} above "
                        f"{policy['actor_mismatch_max']})"
                    ),
                )
            )
    return flags
