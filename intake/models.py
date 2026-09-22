# ABOUTME: Extraction-record and run-manifest models for the source intake pipeline (Plan 017).
# ABOUTME: The writer model authors claims; code fills every other block and owns identities.
"""Typed models for the source intake pipeline.

The extraction record is the pipeline's intermediate format. Stage 4 (the writer model)
produces the ``claims`` list; every other block is filled by code. Claim IDs are content
addressed, so two runs over the same capture give the same IDs and no ID depends on list
position. Enum-valued fields (source kinds, domains, rubric values) are validated against
the catalog builder's own rule sets at render time; these models check only structure,
patterns, and cross-references.
"""

from __future__ import annotations

import hashlib
import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

SCHEMA_VERSION = 1

CLAIM_ID_RE = re.compile(r"^c-[0-9a-f]{8}$")
# The writer model cannot know content-addressed IDs, so it refers to its own
# claims positionally as "#0", "#1", ...; intake.extract.resolve_references
# rewrites those into computed IDs after finalize.
CLAIM_REF_RE = re.compile(r"^c-[0-9a-f]{8}$|^#\d+$")
LOCAL_SOURCE_RE = re.compile(r"^s\d+$")
RUN_ID_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z-[0-9a-f]{4}$")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
# Date forms the authored records use: year, year-month, or a full calendar date.
PARTIAL_DATE_RE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")

FIELD_FAMILIES = (
    "summary",
    "headline_metric",
    "architecture.credentials",
    "architecture.context_mgmt",
    "architecture.harness",
    "architecture.interfaces",
    "architecture.knowledge",
    "architecture.model",
    "architecture.sandbox",
    "architecture.tool_access",
    "primitives[]",
    "key_metrics[]",
    "lessons_learned[]",
    "operating_models[]",
)
READER_QUESTIONS = (
    "purpose",
    "workflow",
    "human_involvement",
    "implementation",
    "validation",
    "observations",
    "lessons",
)

QuoteMatch = Literal["exact", "fuzzy", "missing"]
ClaimKind = Literal["fact", "metric", "inference", "opinion"]
ClaimProvenance = Literal["reported", "observed", "inferred", "catalog-judgment"]
Disposition = Literal["accept", "review", "drop"]
Decision = Literal["add", "update", "needs-evidence", "out-of-scope"]
PrimitiveRole = Literal["workflow", "mechanism", "validation"]
StageName = Literal[
    "capture",
    "segment",
    "resolve",
    "extract",
    "verify",
    "judge",
    "numbers",
    "write",
    "preflight",
    "render",
    "validate",
    "review",
]


class StrictModel(BaseModel):
    """Base model that rejects unknown keys; extraction records carry no extras."""

    model_config = ConfigDict(extra="forbid")


class Quote(StrictModel):
    """One verbatim passage from a captured source that a claim rests on."""

    source: str
    text: str = Field(min_length=1)
    paragraph_id: str | None = None
    lines: tuple[int, int] | None = None
    match: QuoteMatch = "missing"

    @model_validator(mode="after")
    def _check_lines(self) -> Quote:
        if self.lines is not None:
            start, end = self.lines
            if start < 1 or end < start:
                raise ValueError("quote lines must be a 1-based ascending range")
        if self.match != "missing" and self.paragraph_id is None and self.lines is None:
            raise ValueError("an exact or fuzzy quote needs a paragraph id or a line range")
        return self


class NumberCheck(StrictModel):
    """One number or date from a claim, checked against its quote by stage 7."""

    claim: str = Field(min_length=1)
    in_quote: bool
    note: str | None = None


class Verdict(StrictModel):
    """A labelled Jev judgment with its probability."""

    label: str
    p: float = Field(ge=0.0, le=1.0)


class Judgments(StrictModel):
    """Advisory stage-6 verdicts for one claim. Labels are checked at render time."""

    relation: Verdict | None = None
    actor_mismatch: float | None = Field(default=None, ge=0.0, le=1.0)
    temporal: Verdict | None = None
    approval_removed: float | None = Field(default=None, ge=0.0, le=1.0)
    basis: Verdict | None = None
    model: str | None = None
    question_version: int | None = Field(default=None, ge=1)


class ClaimMetadata(StrictModel):
    """Qualifications the renderer copies into ``claim_metadata`` for one claim."""

    confidence: str | None = None
    confidence_reason: str | None = None
    valid_at: str | None = None
    reported_by: str | None = None
    metric_scope: str | None = None
    denominator: str | None = None
    measurement_method: str | None = None
    unit: str | None = None
    value: str | int | float | None = None
    attention_boundary: str | None = None

    @field_validator("valid_at")
    @classmethod
    def _check_valid_at(cls, value: str | None) -> str | None:
        if value is not None and not PARTIAL_DATE_RE.fullmatch(value):
            raise ValueError("valid_at must use YYYY, YYYY-MM, or YYYY-MM-DD")
        return value


class Observation(StrictModel):
    """The page-content classification for one metric claim.

    Either a canonical observation (category, basis, subject) or a duplicate alias
    that points at another metric claim and says why.
    """

    category: str | None = None
    basis: str | None = None
    subject: str | None = None
    duplicate_of: str | None = None
    reason: str | None = None

    @model_validator(mode="after")
    def _check_shape(self) -> Observation:
        if self.duplicate_of is not None:
            if self.category or self.basis or self.subject:
                raise ValueError("a duplicate observation carries no category, basis, or subject")
            if not self.reason or not self.reason.strip():
                raise ValueError("a duplicate observation requires a reason")
        elif not (self.category and self.basis and self.subject):
            raise ValueError("a canonical observation requires category, basis, and subject")
        return self


class Claim(StrictModel):
    """One reported statement with the quotes that support it."""

    id: str | None = None
    field: str
    text: str = Field(min_length=1)
    kind: ClaimKind
    provenance: ClaimProvenance
    quotes: list[Quote] = Field(min_length=1)
    numbers: list[NumberCheck] = []
    judgments: Judgments | None = None
    disposition: Disposition = "review"
    review_note: str | None = None
    metadata: ClaimMetadata | None = None
    observation: Observation | None = None
    primitive_role: PrimitiveRole | None = None
    # A primitive claim names its heading; other list claims render their text directly.
    primitive_name: str | None = None

    @field_validator("field")
    @classmethod
    def _check_field(cls, value: str) -> str:
        if value not in FIELD_FAMILIES:
            known = ", ".join(FIELD_FAMILIES)
            raise ValueError(f"unknown field family {value!r}; expected one of: {known}")
        return value

    @model_validator(mode="after")
    def _check_shape(self) -> Claim:
        if self.field == "primitives[]":
            if not self.primitive_name or not self.primitive_name.strip():
                raise ValueError("a primitives[] claim requires primitive_name")
        elif self.primitive_name is not None:
            raise ValueError("primitive_name is only valid on primitives[] claims")
        if self.field in ("key_metrics[]", "headline_metric") and self.kind != "metric":
            raise ValueError("metric fields carry metric-kind claims")
        return self


class StagedSource(StrictModel):
    """One captured source, staged under ``.intake/captures/`` until promotion."""

    local_id: str
    title: str = Field(min_length=1)
    url: str
    canonical_url: str
    kind: str
    provenance_class: str
    role: str = "evidence"
    publisher: str | None = None
    authors: list[str] | None = None
    published_at: str | None = None
    staging_path: str | None = None
    captured_at: str | None = None
    content_sha256: str
    capture_manifest_path: str | None = None

    @field_validator("local_id")
    @classmethod
    def _check_local_id(cls, value: str) -> str:
        if not LOCAL_SOURCE_RE.fullmatch(value):
            raise ValueError("local_id must look like s1, s2, ...")
        return value

    @field_validator("url", "canonical_url")
    @classmethod
    def _check_https(cls, value: str) -> str:
        if not value.startswith("https://"):
            raise ValueError("source URLs must use HTTPS")
        return value

    @field_validator("content_sha256")
    @classmethod
    def _check_sha(cls, value: str) -> str:
        if not SHA256_RE.fullmatch(value):
            raise ValueError("content_sha256 must look like sha256:<64 hex digits>")
        return value

    @field_validator("published_at", "captured_at")
    @classmethod
    def _check_dates(cls, value: str | None) -> str | None:
        if value is not None and not PARTIAL_DATE_RE.fullmatch(value):
            raise ValueError("dates must use YYYY, YYYY-MM, or YYYY-MM-DD")
        return value


class MatchedRecord(StrictModel):
    """One shortlisted existing record from the identity stage."""

    id: str
    same_system: float | None = Field(default=None, ge=0.0, le=1.0)
    same_system_jev: float | None = Field(default=None, ge=0.0, le=1.0)
    reason: str | None = None


class Candidate(StrictModel):
    """The identity decision the pipeline proposes for one queue entry."""

    company: str = Field(min_length=1)
    system_name: str | None = None
    record_id: str | None = None
    decision: Decision = "needs-evidence"
    matched_records: list[MatchedRecord] = []
    homepage: str | None = None
    company_id: str | None = None

    @field_validator("homepage")
    @classmethod
    def _check_homepage(cls, value: str | None) -> str | None:
        if value is not None and not value.startswith("https://"):
            raise ValueError("homepage must use HTTPS")
        return value


class RubricProposal(StrictModel):
    """The structural rubric the writer model proposes; code validates the values."""

    invocation: list[str] = Field(min_length=1)
    state: str
    identity: str
    evidence_strength: str = "unknown"


class OperatingModelProposal(StrictModel):
    """One scoped supervision assessment, backed by the named claims."""

    scope: str = Field(min_length=1)
    attention_boundary: str
    claim_ids: list[str] = Field(min_length=1)


class Classification(StrictModel):
    """Entry-level classification fields proposed by the writer model."""

    approach_type: str
    deployment_stage: str
    year: int = Field(ge=2000, le=2100)
    status: str = "internal"
    autonomy: str = "unknown"
    domains: list[str] = Field(min_length=1)
    rubric: RubricProposal
    operating_models: list[OperatingModelProposal] = Field(min_length=1)
    agent_name: str = Field(min_length=1)


class QuestionAnswer(StrictModel):
    """Claim IDs that answer one reader question, plus the silence note."""

    claim_ids: list[str] = []
    note: str | None = None


class Questions(StrictModel):
    """The seven reader questions plus per-field implementation answers."""

    purpose: QuestionAnswer = QuestionAnswer()
    workflow: QuestionAnswer = QuestionAnswer()
    human_involvement: QuestionAnswer = QuestionAnswer()
    implementation: QuestionAnswer = QuestionAnswer()
    validation: QuestionAnswer = QuestionAnswer()
    observations: QuestionAnswer = QuestionAnswer()
    lessons: QuestionAnswer = QuestionAnswer()
    implementation_fields: dict[str, QuestionAnswer] = {}
    workflow_scope: str | None = None


class ExtractionRecord(StrictModel):
    """The full stage-4 output for one queue candidate."""

    schema_version: int = SCHEMA_VERSION
    run_id: str
    candidate: Candidate
    classification: Classification
    sources: list[StagedSource] = Field(min_length=1)
    claims: list[Claim] = Field(min_length=1)
    questions: Questions | None = None

    @field_validator("run_id")
    @classmethod
    def _check_run_id(cls, value: str) -> str:
        if not RUN_ID_RE.fullmatch(value):
            raise ValueError("run_id must look like 2026-09-22T19:40:11Z-3f9a")
        return value

    @model_validator(mode="after")
    def _check_references(self) -> ExtractionRecord:
        local_ids = [source.local_id for source in self.sources]
        if len(local_ids) != len(set(local_ids)):
            raise ValueError("source local_ids must be unique")
        known_sources = set(local_ids)
        for claim in self.claims:
            for quote in claim.quotes:
                if quote.source not in known_sources:
                    raise ValueError(f"claim quotes unknown source {quote.source!r}")
        claim_ids = [claim.id for claim in self.claims if claim.id is not None]
        if len(claim_ids) != len(set(claim_ids)):
            raise ValueError("claim ids must be unique")
        known_claims = set(claim_ids)
        positional = {f"#{index}" for index in range(len(self.claims))}

        def known_ref(reference: str) -> bool:
            return reference in known_claims or reference in positional

        for claim in self.claims:
            if (
                claim.observation is not None
                and claim.observation.duplicate_of is not None
                and not known_ref(claim.observation.duplicate_of)
            ):
                raise ValueError(
                    f"observation on claim {claim.id!r} duplicates unknown claim "
                    f"{claim.observation.duplicate_of!r}"
                )
        if self.questions is not None:
            answers = [
                self.questions.purpose,
                self.questions.workflow,
                self.questions.human_involvement,
                self.questions.implementation,
                self.questions.validation,
                self.questions.observations,
                self.questions.lessons,
                *self.questions.implementation_fields.values(),
            ]
            for answer in answers:
                unknown = {ref for ref in answer.claim_ids if not known_ref(ref)}
                if unknown:
                    raise ValueError(f"question answer references unknown claims {sorted(unknown)}")
        for model in self.classification.operating_models:
            unknown = {ref for ref in model.claim_ids if not known_ref(ref)}
            if unknown:
                raise ValueError(f"operating model references unknown claims {sorted(unknown)}")
        return self

    def claim_by_id(self, claim_id: str) -> Claim:
        for claim in self.claims:
            if claim.id == claim_id:
                return claim
        raise KeyError(claim_id)


def compute_claim_id(content_sha256: str, quote_text: str, field: str) -> str:
    """Hash the capture, the quote span, and the field path into a claim ID."""
    digest = hashlib.sha256()
    digest.update(content_sha256.encode("utf-8"))
    digest.update(b"\x00")
    digest.update(quote_text.encode("utf-8"))
    digest.update(b"\x00")
    digest.update(field.encode("utf-8"))
    return f"c-{digest.hexdigest()[:8]}"


def finalize(record: ExtractionRecord) -> ExtractionRecord:
    """Fill missing claim IDs from content and verify the existing ones.

    Returns a copy when any ID changes; the input stays untouched. Raises
    ``ValueError`` when an existing ID does not match its content address.
    """

    shas = {source.local_id: source.content_sha256 for source in record.sources}
    claims = []
    for claim in record.claims:
        if claim.id is None or not CLAIM_ID_RE.fullmatch(claim.id):
            first = claim.quotes[0]
            computed = compute_claim_id(shas[first.source], first.text, claim.field)
            claims.append(claim.model_copy(update={"id": computed}))
            continue
        first = claim.quotes[0]
        computed = compute_claim_id(shas[first.source], first.text, claim.field)
        if claim.id != computed:
            raise ValueError(
                f"claim id {claim.id!r} does not match its content address {computed!r}"
            )
        claims.append(claim)
    return record.model_copy(update={"claims": claims})


class StageRun(StrictModel):
    """One recorded model call block for a pipeline stage."""

    stage: StageName
    model: str | None = None
    prompt_version: str | None = None
    question_version: int | None = None
    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)
    cost_usd: float = Field(default=0.0, ge=0.0)
    cache_hits: int = Field(default=0, ge=0)
    calls: int = Field(default=0, ge=0)
    # Principle 8: the sha256 digests of the exact request inputs each call
    # read, so an auditor can confirm which calls a rerun replayed.
    input_hashes: list[str] = []
    ok: bool = True


class RunManifest(StrictModel):
    """The provenance record for one pipeline run."""

    schema_version: int = SCHEMA_VERSION
    run_id: str
    created_at: str
    queue_entry: dict[str, str | list[str] | None]
    decision: Decision = "needs-evidence"
    record_id: str | None = None
    model_strings: dict[str, str] = {}
    prompt_versions: dict[str, str] = {}
    capture_hashes: dict[str, str] = {}
    stage_runs: list[StageRun] = []
    compatibility: dict[str, list[str]] = {}
    notes: list[str] = []
