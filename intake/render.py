# ABOUTME: Renders a finalized extraction record into today's authored YAML (Plan 017).
# ABOUTME: Code owns numbering, IDs, locators, and dates; the writer model owns prose only.
"""Render an extraction record into the catalog's authored record format.

The renderer is deterministic: the same finalized extraction record renders to the
same YAML. It assigns rendered source IDs, list indexes, evidence locators, and the
claim-ID-to-path compatibility map. Only accepted claims render; ``review`` and
``drop`` claims stay on the review sheet.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

import yaml

from intake import catalog
from intake.models import Claim, ExtractionRecord, StagedSource

ARCHITECTURE_KEYS = (
    "sandbox",
    "harness",
    "model",
    "tool_access",
    "interfaces",
    "knowledge",
    "credentials",
    "context_mgmt",
)
LIST_FAMILIES = ("primitives[]", "key_metrics[]", "lessons_learned[]")
# Observation bases ranked for headline selection; the strongest evidence leads.
BASIS_RANK = {
    "reported-measurement": 0,
    "qualitative": 1,
    "estimate": 2,
    "target": 3,
}
READER_QUESTIONS = (
    "purpose",
    "workflow",
    "human_involvement",
    "implementation",
    "validation",
    "observations",
    "lessons",
)


class RenderError(ValueError):
    """The extraction record cannot render into a valid authored record."""


@dataclass
class RenderResult:
    """Everything stage 10 produces for one candidate."""

    record: dict[str, Any]
    record_yaml: str
    company_entry: dict[str, Any] | None = None
    compatibility: dict[str, list[str]] = field(default_factory=dict)
    not_carried: dict[str, str] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)


def _text_key(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def _date_key(value: str) -> tuple[int, int, int]:
    parts = [int(part) for part in value.split("-")]
    parts += [1] * (3 - len(parts))
    return (parts[0], parts[1], parts[2])


def _source_date(source: StagedSource) -> str | None:
    """The best known date for one source: publication, else capture month."""
    if source.published_at:
        return source.published_at
    if source.captured_at:
        return source.captured_at[:7]
    return None


def _locator(start: int, end: int) -> str:
    if start == end:
        return f"Preserved content.md, line {start}"
    return f"Preserved content.md, lines {start}–{end}"


def _enum(build: Any, value: str, allowed: set[str], label: str) -> str:
    if value not in allowed:
        raise RenderError(f"{label} is {value!r}; expected one of: {', '.join(sorted(allowed))}")
    return value


class _Renderer:
    """One extraction record's walk from claims to the authored shape."""

    def __init__(
        self,
        record: ExtractionRecord,
        reviewed_at: str,
        source_offset: int,
        list_offsets: dict[str, int] | None = None,
        existing_items: dict[str, dict[str, int]] | None = None,
    ) -> None:
        self.extraction = record
        self.build = catalog.load_build()
        self.reviewed_at = reviewed_at
        self.source_offset = source_offset
        # When merging onto an existing record, new list items append after
        # the recorded ones, so their rendered paths start at these offsets.
        self.list_offsets = dict(list_offsets or {})
        # Items the existing record already carries, keyed the way the merge
        # keys them: a claim for a known item registers against that item's
        # index instead of appending a duplicate.
        self.existing_items = existing_items or {}
        self.notes: list[str] = []
        self.evidence: dict[str, list[dict[str, str]]] = {}
        self.claim_metadata: dict[str, dict[str, Any]] = {}
        self.compatibility: dict[str, list[str]] = {}
        self.not_carried: dict[str, str] = {}
        self.source_ids = self._rendered_source_ids()

    def _rendered_source_ids(self) -> dict[str, str]:
        mapping: dict[str, str] = {}
        for index, source in enumerate(self.extraction.sources, start=1 + self.source_offset):
            rendered = f"{self.extraction.candidate.record_id}-source-{index}"
            if not self.build.ID_RE.fullmatch(rendered):
                raise RenderError(f"rendered source id {rendered!r} must use kebab-case")
            mapping[source.local_id] = rendered
        return mapping

    def _existing_list_index(self, root: str, key: str | None) -> int | None:
        """The index of an item the existing record already carries."""
        if not key:
            return None
        return self.existing_items.get(root, {}).get(key)

    def register(self, claim: Claim, path: str) -> None:
        """Attach one claim's exact quotes to a rendered path."""
        if claim.id is None:
            raise RenderError("claims must be finalized before rendering")
        self.compatibility.setdefault(claim.id, []).append(path)
        links = []
        for quote in claim.quotes:
            if quote.match != "exact":
                continue
            start, end = quote.lines or (0, 0)
            links.append(
                {
                    "source_id": self.source_ids[quote.source],
                    "relation": "supports",
                    "locator": _locator(start, end),
                }
            )
        if not links:
            raise RenderError(
                f"accepted claim {claim.id!r} for {path} has no exact quote; this is a "
                "correctness bug in the disposition policy, not a rendering choice"
            )
        existing = self.evidence.setdefault(path, [])
        existing.extend(link for link in links if link not in existing)

    def metadata_entry(self, claim: Claim) -> dict[str, Any]:
        """Compose the claim_metadata block for one claim."""
        entry: dict[str, Any] = {"kind": claim.kind, "provenance": claim.provenance}
        extra = claim.metadata
        if extra is not None:
            for key in (
                "confidence",
                "confidence_reason",
                "valid_at",
                "reported_by",
                "metric_scope",
                "denominator",
                "measurement_method",
                "unit",
                "value",
            ):
                if getattr(extra, key) is not None:
                    entry[key] = getattr(extra, key)
        if "valid_at" not in entry:
            exact = next((q for q in claim.quotes if q.match == "exact"), None)
            if exact is not None:
                source = self.source_by_local_id(exact.source)
                published = _source_date(source)
                if published:
                    entry["valid_at"] = published
        return entry

    def source_by_local_id(self, local_id: str) -> StagedSource:
        return next(source for source in self.extraction.sources if source.local_id == local_id)

    def render(self) -> RenderResult:
        record = self.extraction
        classification = record.classification
        self._validate_classification()
        accepted = [claim for claim in record.claims if claim.disposition == "accept"]
        if not accepted:
            raise RenderError("no accepted claims; a draft needs at least one")

        summaries = [claim for claim in accepted if claim.field == "summary"]
        if len(summaries) != 1:
            raise RenderError(
                f"exactly one accepted summary claim is required, found {len(summaries)}"
            )

        headline = self._pick_headline(accepted)

        architecture: dict[str, Any] = {}
        interfaces: list[str] = []
        primitives: list[dict[str, str]] = []
        key_metrics: list[str] = []
        lessons: list[str] = []
        operating_models: list[dict[str, str]] = []
        counters = {family: self.list_offsets.get(family, 0) for family in LIST_FAMILIES}

        for claim in accepted:
            family = claim.field
            if family.startswith("architecture."):
                key = family.removeprefix("architecture.")
                if key == "interfaces":
                    value = claim.text.strip()
                    _enum(
                        self.build,
                        value,
                        self.build.INTERFACE_VALUES,
                        "architecture.interfaces claim",
                    )
                    interfaces.append(value)
                    self.register(claim, "architecture.interfaces")
                else:
                    architecture[key] = claim.text
                    self.register(claim, family)
            elif family == "primitives[]":
                name = claim.primitive_name or ""
                known = self._existing_list_index("primitives", name)
                if known is not None:
                    self.register(claim, f"primitives.{known}")
                    continue
                index = counters[family]
                counters[family] += 1
                primitives.append({"name": name, "desc": claim.text})
                self.register(claim, f"primitives.{index}")
            elif family == "key_metrics[]":
                if headline is not None and _text_key(claim.text) == _text_key(headline.text):
                    self.notes.append(
                        f"metric claim {claim.id} repeats the headline text; dropped from "
                        "key_metrics so no metric appears twice"
                    )
                    continue
                known = self._existing_list_index("key_metrics", claim.text)
                if known is not None:
                    self.register(claim, f"key_metrics.{known}")
                    continue
                index = counters[family]
                counters[family] += 1
                key_metrics.append(claim.text)
                self.register(claim, f"key_metrics.{index}")
                entry = self.metadata_entry(claim)
                if entry:
                    self.claim_metadata[f"key_metrics.{index}"] = entry
            elif family == "lessons_learned[]":
                known = self._existing_list_index("lessons_learned", claim.text)
                if known is not None:
                    self.register(claim, f"lessons_learned.{known}")
                    continue
                index = counters[family]
                counters[family] += 1
                lessons.append(claim.text)
                self.register(claim, f"lessons_learned.{index}")
                entry = self.metadata_entry(claim)
                if entry:
                    self.claim_metadata[f"lessons_learned.{index}"] = entry

        for proposal in classification.operating_models:
            known = self._existing_list_index("operating_models", proposal.scope)
            if known is not None:
                for claim_id in proposal.claim_ids:
                    claim = record.claim_by_id(claim_id)
                    if claim.field == "operating_models[]":
                        self.register(claim, f"operating_models.{known}")
                continue
            boundary = proposal.attention_boundary
            _enum(
                self.build,
                boundary,
                self.build.ATTENTION_BOUNDARIES,
                "operating_models.attention_boundary",
            )
            index = self.list_offsets.get("operating_models", 0) + len(operating_models)
            operating_models.append({"scope": proposal.scope, "attention_boundary": boundary})
            entry = {
                "kind": "inference",
                "provenance": "catalog-judgment",
                "confidence": "unverified",
                "confidence_reason": (
                    "The catalog derives this assessment from the linked sources; the "
                    "pipeline found no passage that states the supervision form directly."
                ),
            }
            for claim_id in proposal.claim_ids:
                claim = record.claim_by_id(claim_id)
                if claim.field == "operating_models[]":
                    self.register(claim, f"operating_models.{index}")
                if claim.metadata is not None:
                    if claim.metadata.confidence:
                        entry["confidence"] = claim.metadata.confidence
                    if claim.metadata.confidence_reason:
                        entry["confidence_reason"] = claim.metadata.confidence_reason
                    if claim.metadata.valid_at:
                        entry["valid_at"] = claim.metadata.valid_at
            if "valid_at" not in entry:
                dates = [value for value in map(_source_date, record.sources) if value]
                if dates:
                    entry["valid_at"] = min(dates, key=_date_key)[:4]
            self.claim_metadata[f"operating_models.{index}"] = entry

        if headline is not None:
            self.register(headline, "headline_metric")
            entry = self.metadata_entry(headline)
            if entry:
                self.claim_metadata["headline_metric"] = entry

        self.register(summaries[0], "summary")

        first_date, first_source = self._first_public_evidence()
        authored: dict[str, Any] = {
            "id": record.candidate.record_id,
            "company": record.candidate.company,
            "agent_name": classification.agent_name,
            "approach_type": classification.approach_type,
            "deployment_stage": classification.deployment_stage,
            "year": classification.year,
            "first_public_evidence": {"date": first_date, "source_id": first_source},
            "last_reviewed_at": self.reviewed_at,
            "status": classification.status,
            "domains": classification.domains,
            "autonomy": classification.autonomy,
            "operating_models": operating_models,
            "rubric": {
                "invocation": classification.rubric.invocation,
                "state": classification.rubric.state,
                "identity": classification.rubric.identity,
                "evidence_strength": classification.rubric.evidence_strength,
            },
            "summary": summaries[0].text,
        }
        if headline is not None:
            authored["headline_metric"] = headline.text
        if architecture or interfaces:
            ordered = {key: architecture[key] for key in ARCHITECTURE_KEYS if key in architecture}
            if interfaces:
                ordered["interfaces"] = interfaces
            authored["architecture"] = ordered
        if primitives:
            authored["primitives"] = primitives
        if key_metrics:
            authored["key_metrics"] = key_metrics
        if lessons:
            authored["lessons_learned"] = lessons
        authored["sources"] = [self._rendered_source(source) for source in record.sources]
        authored["evidence"] = self.evidence
        if self.claim_metadata:
            authored["claim_metadata"] = self.claim_metadata
        page = self._page_content(authored, headline, key_metrics, primitives)
        if page is not None:
            authored["page_content"] = page

        return RenderResult(
            record=authored,
            record_yaml=to_authored_yaml(authored),
            company_entry=self._company_entry(),
            compatibility=self.compatibility,
            not_carried=self.not_carried,
            notes=self.notes,
        )

    def _pick_headline(self, accepted: list[Claim]) -> Claim | None:
        """Take the writer-marked headline, else choose by basis and number specificity."""
        marked = [claim for claim in accepted if claim.field == "headline_metric"]
        if marked:
            if len(marked) > 1:
                raise RenderError("at most one accepted headline_metric claim is allowed")
            return marked[0]
        metrics = [claim for claim in accepted if claim.field == "key_metrics[]"]
        if not metrics:
            return None

        def rank(claim: Claim, order: int) -> tuple[int, int, int]:
            basis = None
            if claim.judgments is not None and claim.judgments.basis is not None:
                basis = claim.judgments.basis.label
            basis_rank = BASIS_RANK.get(basis or "", len(BASIS_RANK))
            numbers = sum(1 for check in claim.numbers if check.in_quote)
            return (basis_rank, -numbers, order)

        winner = min(
            ((claim, order) for order, claim in enumerate(metrics)),
            key=lambda pair: rank(pair[0], pair[1]),
        )[0]
        self.notes.append(
            f"headline_metric chosen from {len(metrics)} metric claims by observation basis "
            "and number specificity; the reviewer confirms the choice"
        )
        return winner

    def _validate_classification(self) -> None:
        build = self.build
        classification = self.extraction.classification
        _enum(build, classification.approach_type, build.APPROACH_TYPES, "approach_type")
        _enum(
            build,
            classification.deployment_stage,
            build.DEPLOYMENT_STAGES,
            "deployment_stage",
        )
        _enum(build, classification.status, build.STATUS, "status")
        _enum(build, classification.autonomy, build.AUTONOMY, "autonomy")
        for domain in classification.domains:
            _enum(build, domain, build.DOMAIN_VALUES, f"domain {domain!r}")
        for value in classification.rubric.invocation:
            _enum(build, value, build.INVOCATION, "rubric.invocation value")
        _enum(build, classification.rubric.state, build.STATE, "rubric.state")
        _enum(build, classification.rubric.identity, build.IDENTITY, "rubric.identity")
        _enum(
            build,
            classification.rubric.evidence_strength,
            build.EVIDENCE_STRENGTH,
            "rubric.evidence_strength",
        )
        for source in self.extraction.sources:
            _enum(build, source.kind, build.SOURCE_KINDS, f"source {source.local_id} kind")
            _enum(
                build,
                source.provenance_class,
                build.PROVENANCE_CLASSES,
                f"source {source.local_id} provenance_class",
            )
            _enum(build, source.role, build.SOURCE_ROLES, f"source {source.local_id} role")
        for claim in self.extraction.claims:
            if claim.observation is not None and claim.observation.duplicate_of is None:
                _enum(
                    build,
                    claim.observation.category or "",
                    build.OBSERVATION_CATEGORIES,
                    "observation.category",
                )
                _enum(
                    build,
                    claim.observation.basis or "",
                    build.OBSERVATION_BASES,
                    "observation.basis",
                )
            if claim.metadata is not None and claim.metadata.attention_boundary is not None:
                _enum(
                    build,
                    claim.metadata.attention_boundary,
                    build.ATTENTION_BOUNDARIES,
                    "claim attention_boundary",
                )

    def _first_public_evidence(self) -> tuple[str, str]:
        dated = [
            (value, self.source_ids[source.local_id])
            for source in self.extraction.sources
            if source.role == "evidence" and (value := _source_date(source))
        ]
        if not dated:
            raise RenderError(
                "first_public_evidence needs one source with published_at or captured_at"
            )
        value, source_id = min(dated, key=lambda item: _date_key(item[0]))
        return value, source_id

    def _rendered_source(self, source: StagedSource) -> dict[str, Any]:
        rendered_id = self.source_ids[source.local_id]
        entry: dict[str, Any] = {
            "id": rendered_id,
            "title": source.title,
            "url": source.url,
            "canonical_url": source.canonical_url,
            "kind": source.kind,
            "provenance_class": source.provenance_class,
        }
        if source.role != "evidence":
            entry["role"] = source.role
        if source.publisher:
            entry["publisher"] = source.publisher
        if source.authors:
            entry["authors"] = source.authors
        if source.published_at:
            entry["published_at"] = source.published_at
        verified = source.captured_at or source.published_at
        if not verified:
            raise RenderError(f"source {source.local_id} needs captured_at or published_at")
        entry["accessed_at"] = verified
        entry["last_verified_at"] = verified
        if source.capture_manifest_path is not None:
            expected = f"archive/sources/{rendered_id}/metadata.json"
            if source.capture_manifest_path != expected:
                raise RenderError(
                    f"source {source.local_id} capture path {source.capture_manifest_path!r} "
                    f"must be {expected!r} after promotion"
                )
            entry["capture"] = {"manifest_path": expected}
        # Open decision 3: page metadata that today's source schema cannot
        # carry stays in the extraction record, and the compatibility map —
        # the explicit mapping the schema migration will need — says where
        # it went instead of dropping it silently.
        carried = []
        for name, value in (("language", source.language), ("description", source.description)):
            if not value:
                continue
            carried.append(f"{name} {value}")
            self.not_carried[f"{source.local_id}.{name}"] = (
                f"today's source schema has no {name} field; preserved in the extraction record"
            )
        if carried:
            self.notes.append(
                f"source {source.local_id} page metadata not carried by today's schema "
                f"({'; '.join(carried)}); preserved in the extraction record and named "
                "in the compatibility map"
            )
        return entry

    def _page_content(
        self,
        authored: dict[str, Any],
        headline: Claim | None,
        key_metrics: list[str],
        primitives: list[dict[str, str]],
    ) -> dict[str, Any] | None:
        """Derive the page-content block, or return ``None`` with a note when incomplete."""
        questions = self.extraction.questions
        if questions is None:
            self.notes.append(
                "page_content omitted: the extraction record carries no questions block; "
                "the reviewer completes the editorial coverage contract"
            )
            return None
        silent_note = (
            f"The pipeline found no passage in "
            f"{', '.join(source.local_id for source in self.extraction.sources)}. "
            "Confirm silence or record the next action."
        )
        accepted_ids = {
            claim.id for claim in self.extraction.claims if claim.disposition == "accept"
        }
        path_of = self.compatibility

        def disposition(answer: Any, allowed: set[str] | None, label: str) -> dict[str, Any]:
            answered = [claim_id for claim_id in answer.claim_ids if claim_id in accepted_ids]
            paths = [path for claim_id in answered for path in path_of.get(claim_id, [])]
            paths = [path for index, path in enumerate(paths) if path not in paths[:index]]
            if not answered or not paths:
                if answer.claim_ids:
                    self.notes.append(
                        f"{label}: its claims did not render; left not-reviewed for the "
                        "reviewer to complete"
                    )
                return {
                    "state": "not-reviewed",
                    "claim_paths": [],
                    "note": answer.note or silent_note,
                }
            if allowed is not None and set(paths) - allowed:
                raise RenderError(
                    f"{label} names claims outside its allowed field: "
                    f"{sorted(set(paths) - allowed)}"
                )
            if len(answered) != len(answer.claim_ids):
                self.notes.append(
                    f"{label} is partly answered: claims "
                    f"{[c for c in answer.claim_ids if c not in accepted_ids]} are still "
                    "in review and did not render; the reviewer completes the answer"
                )
            entry: dict[str, Any] = {"state": "reported", "claim_paths": paths}
            if answer.note:
                entry["note"] = answer.note
            return entry

        page_questions = {
            key: disposition(getattr(questions, key), None, f"questions.{key}")
            for key in READER_QUESTIONS
        }
        implementation_fields: dict[str, Any] = {}
        for key in ARCHITECTURE_KEYS:
            answer = questions.implementation_fields.get(key)
            implementation_fields[key] = (
                {"state": "not-reviewed", "claim_paths": [], "note": silent_note}
                if answer is None
                else disposition(answer, {f"architecture.{key}"}, f"implementation_fields.{key}")
            )

        workflow_paths = page_questions["workflow"]["claim_paths"]
        primitive_roles: dict[str, str] = {}
        for index, claim in enumerate(
            claim for claim in self.extraction.claims if claim.field == "primitives[]"
        ):
            path = f"primitives.{index}"
            if path not in self.evidence:
                continue
            if claim.primitive_role is not None and claim.primitive_role != "workflow":
                if path in workflow_paths:
                    raise RenderError(
                        f"primitive claim {claim.id} carries role {claim.primitive_role!r} "
                        "but the workflow answer names it; resolve the conflict"
                    )
                primitive_roles[path] = claim.primitive_role
            elif path in workflow_paths:
                primitive_roles[path] = "workflow"
            else:
                primitive_roles[path] = claim.primitive_role or "mechanism"
        orphaned = set(workflow_paths) - set(primitive_roles)
        if orphaned:
            raise RenderError(
                f"workflow answer names claims that are not rendered primitives: {sorted(orphaned)}"
            )

        observations = self._observations(authored, headline, key_metrics)
        if observations is None:
            return None

        page: dict[str, Any] = {
            "version": 1,
            "reviewed_at": self.reviewed_at,
            "source_ids": [self.source_ids[source.local_id] for source in self.extraction.sources],
            "questions": page_questions,
            "implementation_fields": implementation_fields,
            "primitive_roles": primitive_roles,
            "observations": observations,
        }
        if page_questions["workflow"]["state"] == "reported":
            if not questions.workflow_scope:
                raise RenderError(
                    "questions.workflow_scope is required when the workflow answer is reported"
                )
            page["workflow_scope"] = questions.workflow_scope
        return page

    def _observations(
        self, authored: dict[str, Any], headline: Claim | None, key_metrics: list[str]
    ) -> dict[str, Any] | None:
        """Classify every rendered metric claim, or give up with a note."""
        metric_paths = (["headline_metric"] if headline is not None else []) + [
            f"key_metrics.{index}" for index in range(len(key_metrics))
        ]
        claim_by_path: dict[str, Claim] = {}
        for claim_id, paths in self.compatibility.items():
            claim = self.extraction.claim_by_id(claim_id)
            for path in paths:
                if path in metric_paths:
                    claim_by_path[path] = claim
        observations: dict[str, Any] = {}
        for path in metric_paths:
            claim = claim_by_path.get(path)
            if claim is None or claim.observation is None:
                self.notes.append(
                    f"page_content omitted: the metric claim for {path} has no observation "
                    "block; the reviewer classifies it"
                )
                return None
            observation = claim.observation
            if observation.duplicate_of is not None:
                targets = self.compatibility.get(observation.duplicate_of, [])
                target = next((value for value in targets if value in metric_paths), None)
                if target is None or target == path:
                    raise RenderError(
                        f"observation for {path} duplicates {observation.duplicate_of!r}, "
                        "which is not another rendered metric claim"
                    )
                observations[path] = {"duplicate_of": target, "reason": observation.reason}
            else:
                observations[path] = {
                    "category": observation.category,
                    "basis": observation.basis,
                    "subject": observation.subject,
                }
        for path, value in observations.items():
            target = value.get("duplicate_of")
            if target is not None and "duplicate_of" in observations.get(target, {}):
                raise RenderError(f"observation {path!r} forms a duplicate chain")
        return observations

    def _company_entry(self) -> dict[str, Any] | None:
        candidate = self.extraction.candidate
        if candidate.homepage is None:
            self.notes.append(
                "no company entry: the queue entry carried no homepage hint; the reviewer "
                "adds the organization to data/companies.yaml"
            )
            return None
        company_id = candidate.company_id
        if company_id is None:
            company_id = re.sub(r"[^a-z0-9]+", "-", candidate.company.lower()).strip("-")
        if not self.build.ID_RE.fullmatch(company_id):
            raise RenderError(
                f"company id {company_id!r} must use kebab-case; pass candidate.company_id"
            )
        return {
            "id": company_id,
            "name": candidate.company,
            "homepage": candidate.homepage,
            "logo": "none",
            "logo_note": (
                "Editorial follow-up: collect a logo asset for this organization "
                "(public/logos/<id>.svg or .png with a source URL)."
            ),
        }


def render_extraction(
    record: ExtractionRecord,
    *,
    reviewed_at: str,
    existing_source_count: int = 0,
    existing: dict[str, Any] | None = None,
    contradictions: list[dict[str, Any]] | None = None,
) -> RenderResult:
    """Render one finalized extraction record into today's YAML shape.

    With ``existing`` (an authored record the update names), the result is
    the existing record with the update's additions appended — sources, list
    items, evidence links, metadata — and single-valued fields kept, per the
    plan's append-only principle. The source offset comes from the existing
    record itself. ``contradictions`` (the cross checks' number conflicts)
    become proposed evidence links with ``relation: contradicts`` on the
    existing claims they name.
    """
    if record.candidate.record_id is None:
        raise RenderError("candidate.record_id is required before rendering")
    if existing is not None:
        existing_source_count = len(existing.get("sources") or [])
    if existing_source_count < 0:
        raise RenderError("existing_source_count must not be negative")
    if any(claim.id is None for claim in record.claims):
        raise RenderError("run intake.models.finalize before rendering")
    list_offsets: dict[str, int] | None = None
    existing_items: dict[str, dict[str, int]] | None = None
    if existing is not None:
        list_offsets = {
            "primitives[]": len(existing.get("primitives") or []),
            "key_metrics[]": len(existing.get("key_metrics") or []),
            "lessons_learned[]": len(existing.get("lessons_learned") or []),
            "operating_models": len(existing.get("operating_models") or []),
        }
        existing_items = {
            "primitives": {
                item.get("name"): index
                for index, item in enumerate(existing.get("primitives") or [])
            },
            "key_metrics": {
                item: index for index, item in enumerate(existing.get("key_metrics") or [])
            },
            "lessons_learned": {
                item: index for index, item in enumerate(existing.get("lessons_learned") or [])
            },
            "operating_models": {
                item.get("scope"): index
                for index, item in enumerate(existing.get("operating_models") or [])
            },
        }
    renderer = _Renderer(record, reviewed_at, existing_source_count, list_offsets, existing_items)
    result = renderer.render()
    if existing is None:
        return result
    from intake.merge import merge_update

    links = []
    for flag in contradictions or []:
        for quote in flag.get("quotes") or []:
            start, end = quote["lines"][0], quote["lines"][-1]
            links.append(
                {
                    "claim_path": flag["claim_path"],
                    "source_id": renderer.source_ids[quote["source"]],
                    "locator": _locator(start, end),
                }
            )
    merged = merge_update(
        existing,
        result.record,
        reviewed_at=reviewed_at,
        notes=result.notes,
        contradictions=links,
    )
    return RenderResult(
        record=merged,
        record_yaml=to_authored_yaml(merged),
        company_entry=result.company_entry,
        compatibility=result.compatibility,
        notes=result.notes,
    )


def to_authored_yaml(record: dict[str, Any]) -> str:
    """Dump one authored record in the repository's block style."""
    return yaml.safe_dump(
        record,
        sort_keys=False,
        allow_unicode=True,
        width=100,
        default_flow_style=False,
    )
