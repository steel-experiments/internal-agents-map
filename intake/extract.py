# ABOUTME: Stage 4 of the intake pipeline: extract claims with the writer model (Plan 017).
# ABOUTME: One retry on schema violation; the budget is reserved before the call.
"""Run the extraction stage over one candidate's captured paragraphs.

The writer model receives the versioned prompt, the paragraphs with their IDs,
the field definitions, and the queue hints. It returns the claims list; code
fills every other block: the sources from the staging facts, the claim IDs from
the content address, and the dispositions policy check. One retry on a schema
violation; any API error stops the run.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError

from intake.adapters.writer import WriterAdapter
from intake.budget import Budget
from intake.models import (
    Candidate,
    Claim,
    Classification,
    ExtractionRecord,
    Questions,
    StagedSource,
    finalize,
)
from intake.segment import Paragraph

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
PROMPT_VERSION = "extract.v1"


class ExtractionStageError(RuntimeError):
    """The extraction stage failed after its one retry."""


class WriterPayload(BaseModel):
    """The writer model's own output: claims and classification, nothing else."""

    model_config = ConfigDict(extra="forbid")

    candidate: Candidate
    classification: Classification
    claims: list[Claim]
    questions: Questions | None = None


def strict_schema(model: type[BaseModel]) -> dict[str, Any]:
    """The model's JSON schema made strict: every key required, no extras."""
    schema = model.model_json_schema()
    if "$defs" in schema:
        schema = dict(schema)
        schema["$defs"] = dict(schema["$defs"])

    def strictify(node: Any) -> None:
        if isinstance(node, dict):
            properties = node.get("properties")
            if isinstance(properties, dict) and properties:
                node["required"] = list(properties)
                node["additionalProperties"] = False
            for value in node.values():
                strictify(value)
        elif isinstance(node, list):
            for value in node:
                strictify(value)

    strictify(schema)
    return schema


def load_prompt(version: str = PROMPT_VERSION) -> str:
    """Read one versioned prompt file."""
    path = PROMPTS_DIR / f"{version}.md"
    if not path.is_file():
        raise ExtractionStageError(f"prompt file {path} does not exist")
    return path.read_text(encoding="utf-8")


def build_input(
    *,
    paragraphs: list[Paragraph],
    sources: list[StagedSource],
    hints: dict[str, Any] | None = None,
) -> str:
    """Compose the untrusted input payload for the writer model."""
    return json.dumps(
        {
            "candidate": hints or {},
            "sources": [
                {
                    "local_id": source.local_id,
                    "url": source.url,
                    "title": source.title,
                    "published_at": source.published_at,
                }
                for source in sources
            ],
            "paragraphs": [
                {
                    "id": paragraph.id,
                    "heading_path": list(paragraph.heading_path),
                    "start": paragraph.start,
                    "end": paragraph.end,
                    "text": paragraph.text,
                }
                for paragraph in paragraphs
            ],
        },
        ensure_ascii=False,
        indent=2,
    )


def run_extract(
    *,
    run_id: str,
    paragraphs: list[Paragraph],
    sources: list[StagedSource],
    hints: dict[str, Any] | None = None,
    adapter: WriterAdapter,
    budget: Budget,
) -> tuple[ExtractionRecord, dict[str, Any]]:
    """Extract one candidate's claims; returns the record and the stage facts.

    The stage facts feed the run manifest: the model string the API returned,
    token usage, cost, and whether the retry fired.
    """

    budget.reserve_calls(1)
    instructions = load_prompt()
    input_text = build_input(paragraphs=paragraphs, sources=sources, hints=hints)
    schema = strict_schema(WriterPayload)
    result = adapter.complete_json(
        instructions=instructions,
        input_text=input_text,
        schema=schema,
        schema_name="extraction_payload",
        budget=budget,
    )
    calls = 1
    try:
        payload = WriterPayload.model_validate(result.payload)
    except ValidationError as error:
        budget.reserve_calls(1)
        retry_input = (
            input_text
            + "\n\nYour previous reply violated the schema:\n"
            + json.dumps(json.loads(error.json()), indent=2)[:4000]
            + "\n\nReturn a reply that validates against the same schema."
        )
        result = adapter.complete_json(
            instructions=instructions,
            input_text=retry_input,
            schema=schema,
            schema_name="extraction_payload",
            budget=budget,
        )
        calls += 1
        try:
            payload = WriterPayload.model_validate(result.payload)
        except ValidationError as retry_error:
            raise ExtractionStageError(
                f"extraction schema violation after one retry: {retry_error}"
            ) from retry_error
    record = ExtractionRecord(
        run_id=run_id,
        candidate=payload.candidate,
        classification=payload.classification,
        sources=sources,
        claims=payload.claims,
        questions=payload.questions,
    )
    record = finalize(record)
    record = resolve_references(record)
    stage = {
        "stage": "extract",
        "model": result.model,
        "prompt_version": PROMPT_VERSION,
        "input_tokens": result.input_tokens,
        "output_tokens": result.output_tokens,
        "cost_usd": round(result.cost_usd, 6),
        "calls": calls,
    }
    return record, stage


def resolve_references(record: ExtractionRecord) -> ExtractionRecord:
    """Rewrite the writer's positional claim references into computed IDs.

    The writer model refers to its own claims as ``#0``, ``#1``, ... because the
    content-addressed IDs do not exist until code computes them. This runs after
    :func:`~intake.models.finalize`, so every reference either resolves to a real
    claim ID or the record is rejected.
    """

    ids = [claim.id or "" for claim in record.claims]

    def resolve_one(item: str) -> str:
        if item.startswith("#"):
            index = int(item[1:])
            if index >= len(ids):
                raise ExtractionStageError(
                    f"claim reference {item!r} is out of range for {len(ids)} claims"
                )
            return ids[index]
        return item

    def resolve(items: list[str]) -> list[str]:
        return [resolve_one(item) for item in items]

    claims = [
        claim.model_copy(
            update={
                "observation": (
                    claim.observation.model_copy(
                        update={"duplicate_of": resolve_one(claim.observation.duplicate_of)}
                    )
                    if claim.observation is not None and claim.observation.duplicate_of is not None
                    else claim.observation
                )
            }
        )
        for claim in record.claims
    ]
    record = record.model_copy(update={"claims": claims})

    questions = record.questions
    if questions is not None:
        updated = {}
        for key in (
            "purpose",
            "workflow",
            "human_involvement",
            "implementation",
            "validation",
            "observations",
            "lessons",
        ):
            answer = getattr(questions, key)
            updated[key] = answer.model_copy(update={"claim_ids": resolve(answer.claim_ids)})
        for key, answer in questions.implementation_fields.items():
            updated.setdefault(
                key, answer.model_copy(update={"claim_ids": resolve(answer.claim_ids)})
            )
        questions = questions.model_copy(update=updated)
    classification = record.classification
    operating_models = [
        proposal.model_copy(update={"claim_ids": resolve(proposal.claim_ids)})
        for proposal in classification.operating_models
    ]
    classification = classification.model_copy(update={"operating_models": operating_models})
    return record.model_copy(update={"questions": questions, "classification": classification})
