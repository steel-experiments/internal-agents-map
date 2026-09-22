# ABOUTME: Stage 8 of the intake pipeline: confidence reasons for accepted claims (Plan 017).
# ABOUTME: The claim prose comes from stage 4; this pass writes the reasons, not the facts.
"""Write one confidence reason per accepted claim that lacks one.

Stage 4 already authors the claim prose, so stage 8's writer call covers the
one piece of prose that stage 4 may leave blank: the per-claim confidence
reason the schema review asks to keep honest. Every reason must reference its
claim; an unknown claim ID, a number the claim does not carry, or an empty
reason fails the stage after one retry. The prose fields themselves are
validated structurally: every rendered field maps to claims through the
compatibility map, and the renderer refuses a field without one.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError

from intake.adapters.writer import WriterAdapter
from intake.budget import Budget
from intake.models import ClaimMetadata, ExtractionRecord
from intake.numbers import check_claim_numbers

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
PROMPT_VERSION = "write.v1"


class WriteStageError(RuntimeError):
    """The write stage failed after its one retry."""


class ReasonsPayload(BaseModel):
    """The writer model's output: one reason per claim ID."""

    model_config = ConfigDict(extra="forbid")

    reasons: dict[str, str]


def _strict_schema() -> dict[str, Any]:
    from intake.extract import strict_schema

    return strict_schema(ReasonsPayload)


def load_prompt(version: str = PROMPT_VERSION) -> str:
    """Read one versioned prompt file."""
    path = PROMPTS_DIR / f"{version}.md"
    if not path.is_file():
        raise WriteStageError(f"prompt file {path} does not exist")
    return path.read_text(encoding="utf-8")


def claims_needing_reasons(record: ExtractionRecord) -> list[Any]:
    """The accepted claims whose metadata lacks a confidence reason."""
    return [
        claim
        for claim in record.claims
        if claim.disposition == "accept"
        and (claim.metadata is None or not claim.metadata.confidence_reason)
    ]


def build_input(record: ExtractionRecord) -> str:
    """Compose the writer input: the claims that need reasons, with quotes."""
    claims = [
        {
            "claim_id": claim.id,
            "field": claim.field,
            "text": claim.text,
            "kind": claim.kind,
            "provenance": claim.provenance,
            "quotes": [
                {"source": quote.source, "text": quote.text, "match": quote.match}
                for quote in claim.quotes
            ],
            "confidence": claim.metadata.confidence if claim.metadata else None,
        }
        for claim in claims_needing_reasons(record)
    ]
    return json.dumps({"claims": claims}, ensure_ascii=False, indent=2)


def validate_reasons(record: ExtractionRecord, payload: ReasonsPayload) -> dict[str, str]:
    """Every needed claim has one non-empty reason that introduces no numbers."""
    needed = {claim.id or "" for claim in claims_needing_reasons(record)}
    if set(payload.reasons) != needed:
        missing = sorted(needed - set(payload.reasons))
        extra = sorted(set(payload.reasons) - needed)
        raise WriteStageError(
            f"reasons do not match the claims (missing {missing}, unexpected {extra})"
        )
    for claim in claims_needing_reasons(record):
        reason = payload.reasons[claim.id or ""]
        if not reason.strip():
            raise WriteStageError(f"claim {claim.id} received an empty reason")
        quote_text = " ".join(quote.text for quote in claim.quotes)
        for check in check_claim_numbers(reason, f"{claim.text} {quote_text}"):
            if not check.in_quote:
                raise WriteStageError(
                    f"reason for claim {claim.id} introduces the number "
                    f"{check.claim!r}, which neither the claim nor its quotes carry"
                )
    return dict(payload.reasons)


def run_write(
    record: ExtractionRecord,
    *,
    adapter: WriterAdapter,
    budget: Budget,
    cache: Any = None,
) -> tuple[ExtractionRecord, dict[str, Any]]:
    """Write the missing confidence reasons; returns the record and stage facts.

    With a cache, a warm call replays the recorded reasons and reports zero
    calls.
    """

    needed = claims_needing_reasons(record)
    if not needed:
        return record, {
            "stage": "write",
            "model": None,
            "prompt_version": PROMPT_VERSION,
            "input_tokens": 0,
            "output_tokens": 0,
            "cost_usd": 0.0,
            "calls": 0,
        }
    budget.reserve_calls(1)
    instructions = load_prompt()
    input_text = build_input(record)
    schema = _strict_schema()
    result = adapter.complete_json(
        instructions=instructions,
        input_text=input_text,
        schema=schema,
        schema_name="confidence_reasons",
        budget=budget,
        cache=cache,
    )
    calls = 0 if result.cache_hit else 1
    cache_hits = 1 if result.cache_hit else 0
    try:
        payload = ReasonsPayload.model_validate(result.payload)
        reasons = validate_reasons(record, payload)
    except (ValidationError, WriteStageError) as error:
        budget.reserve_calls(1)
        retry_input = (
            input_text
            + "\n\nYour previous reply was rejected:\n"
            + str(error)[:2000]
            + "\n\nReturn one valid reason for exactly the claim IDs supplied."
        )
        result = adapter.complete_json(
            instructions=instructions,
            input_text=retry_input,
            schema=schema,
            schema_name="confidence_reasons",
            budget=budget,
            cache=cache,
        )
        calls += 1
        try:
            payload = ReasonsPayload.model_validate(result.payload)
            reasons = validate_reasons(record, payload)
        except (ValidationError, WriteStageError) as retry_error:
            raise WriteStageError(
                f"confidence reasons failed after one retry: {retry_error}"
            ) from retry_error
    claims = []
    for claim in record.claims:
        reason = reasons.get(claim.id or "")
        if reason is None:
            claims.append(claim)
            continue
        metadata = claim.metadata or ClaimMetadata()
        claims.append(
            claim.model_copy(
                update={"metadata": metadata.model_copy(update={"confidence_reason": reason})}
            )
        )
    stage = {
        "stage": "write",
        "model": result.model,
        "prompt_version": PROMPT_VERSION,
        "input_tokens": result.input_tokens,
        "output_tokens": result.output_tokens,
        "cost_usd": round(result.cost_usd, 6),
        "cache_hits": cache_hits,
        "calls": calls,
    }
    return record.model_copy(update={"claims": claims}), stage
