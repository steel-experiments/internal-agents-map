# ABOUTME: The full pipeline run: queue file in, reviewed draft out (Plan 017).
# ABOUTME: Twelve stages, separate budgets and artifacts; a person merges nothing here.
"""Run the whole intake pipeline over a queue file.

Each queue entry holds one or more URLs and optional hints (company, system
name, existing record ID, source role). The run executes the twelve stages per
candidate, writes its artifacts under ``.intake/runs/<run-id>/`` (never
overwritten), the draft under ``drafts/``, and the review sheet beside the run
manifest. The run refuses to start when its worst-case reservation exceeds the
budget, stops on the first API error, and never commits, opens a pull
request, or publishes.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from intake import privacy
from intake.adapters.jev import JevAdapter
from intake.adapters.steel import SteelSdkAdapter
from intake.adapters.writer import WriterAdapter
from intake.budget import Budget, new_run_id, run_directory
from intake.capture import capture_staging
from intake.extract import run_extract
from intake.judge import apply_dispositions, judge_claims
from intake.models import MatchedRecord, StagedSource
from intake.numbers import check_claim
from intake.preflight import preflight_flags
from intake.render import render_extraction
from intake.resolve import IDENTITY_QUESTION_VERSION, resolve_identity
from intake.review import review_sheet, write_review
from intake.segment import segment_content
from intake.verify_quotes import verify_claims

ROOT = Path(__file__).resolve().parent.parent
RUNS_ROOT = ROOT / ".intake" / "runs"
DRAFTS_ROOT = ROOT / "drafts"
DEFAULT_BUDGET_USD = 2.0


class QueueError(RuntimeError):
    """The queue file is not a valid queue."""


@dataclass
class QueueEntry:
    """One candidate: its URLs and hints."""

    urls: list[str]
    company: str | None = None
    system_name: str | None = None
    record_id: str | None = None
    source_role: str | None = None
    homepage: str | None = None

    def payload(self) -> dict[str, Any]:
        return {
            "urls": self.urls,
            "company": self.company,
            "system_name": self.system_name,
            "record_id": self.record_id,
            "source_role": self.source_role,
            "homepage": self.homepage,
        }


@dataclass
class RunSummary:
    """What one candidate's run produced."""

    run_id: str
    record_id: str | None
    decision: str
    draft_path: Path | None = None
    sheet_path: Path | None = None
    stages: list[dict[str, Any]] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def load_queue(path: Path) -> list[QueueEntry]:
    """Load one queue file; every entry needs at least one HTTPS URL."""
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not payload:
        raise QueueError(f"{path}: a queue is a non-empty list of entries")
    entries: list[QueueEntry] = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise QueueError(f"{path}: entry {index} is not a mapping")
        urls = item.get("urls") or ([item["url"]] if "url" in item else [])
        urls = [str(url) for url in urls]
        if not urls or not all(url.startswith("https://") for url in urls):
            raise QueueError(f"{path}: entry {index} needs at least one HTTPS URL")
        entries.append(
            QueueEntry(
                urls=urls,
                company=item.get("company"),
                system_name=item.get("system_name"),
                record_id=item.get("record_id"),
                source_role=item.get("source_role"),
                homepage=item.get("homepage"),
            )
        )
    return entries


def _numbers_stage(record) -> tuple[Any, dict[str, Any]]:
    """Stage 7: attach the numeric and date checks to every claim."""
    published = {source.local_id: source.published_at for source in record.sources}
    claims = []
    for claim in record.claims:
        pairs = [
            (quote.text, published.get(quote.source))
            for quote in claim.quotes
            if quote.match == "exact"
        ]
        checks = check_claim(claim.text, pairs)
        claims.append(claim.model_copy(update={"numbers": checks}))
    return record.model_copy(update={"claims": claims}), {
        "stage": "numbers",
        "model": None,
        "input_tokens": 0,
        "output_tokens": 0,
        "cost_usd": 0.0,
        "calls": 0,
    }


def run_candidate(
    entry: QueueEntry,
    *,
    budget: Budget,
    steel: SteelSdkAdapter | None = None,
    writer: WriterAdapter | None = None,
    jev: JevAdapter | None = None,
    cache: Any = None,
    runs_root: Path = RUNS_ROOT,
    drafts_root: Path = DRAFTS_ROOT,
    staging_root: Path | None = None,
    reviewed_at: str | None = None,
) -> RunSummary:
    """Run all twelve stages for one queue candidate."""
    import datetime as dt

    from intake.cache import jev_cache
    from intake.catalog import load_build

    cache = cache or jev_cache()
    reviewed_at = reviewed_at or dt.date.today().isoformat()
    run_id = new_run_id()
    directory = run_directory(run_id, runs_root=runs_root)
    stages: list[dict[str, Any]] = []
    notes: list[str] = []

    # Stage 1: capture every URL into staging.
    capture_kwargs = {"adapter": steel}
    if staging_root is not None:
        capture_kwargs["staging_root"] = staging_root
    staged = [capture_staging(url, **capture_kwargs) for url in entry.urls]
    for index, capture in enumerate(staged, start=1):
        (directory / f"staging-s{index}.txt").write_text(
            str(capture.staging_dir) + "\n", encoding="utf-8"
        )
    sources = [
        StagedSource(
            local_id=f"s{index}",
            title=_page_title(capture),
            url=capture.url,
            canonical_url=capture.canonical_url,
            kind="other",
            provenance_class="independent-secondary",
            published_at=_page_published(capture),
            staging_path=capture.staging_path,
            captured_at=capture.captured_at[:10],
            content_sha256=capture.content_sha256,
        )
        for index, capture in enumerate(staged, start=1)
    ]
    stages.append(
        {
            "stage": "capture",
            "model": None,
            "input_tokens": 0,
            "output_tokens": 0,
            "cost_usd": 0.0,
            "calls": len(staged),
        }
    )

    # Stage 2: segment every capture.
    from intake.capture import read_staging

    paragraphs = {}
    for source in sources:
        bundle = read_staging(Path(source.staging_path or ""))
        paragraphs[source.local_id] = segment_content(bundle["content"])
        (directory / f"paragraphs-{source.local_id}.json").write_text(
            json.dumps(
                [
                    {
                        "id": paragraph.id,
                        "heading_path": list(paragraph.heading_path),
                        "start": paragraph.start,
                        "end": paragraph.end,
                        "text": paragraph.text,
                    }
                    for paragraph in paragraphs[source.local_id]
                ],
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
    stages.append({"stage": "segment", "model": None, "calls": 0, "cost_usd": 0.0})

    # Stage 3: resolve identity.
    build = load_build()
    records = build.load_agents()
    companies = build.load_companies(records)
    summary_text = "\n\n".join(
        paragraph.text
        for source_paragraphs in paragraphs.values()
        for paragraph in source_paragraphs[:20]
    )
    identity = resolve_identity(
        company=entry.company,
        system_name=entry.system_name,
        text=summary_text,
        records=records,
        companies=companies,
    )
    resolve_stage: dict[str, Any] = {"stage": "resolve", "model": None, "calls": 0, "cost_usd": 0.0}
    if identity["matched_records"]:
        from intake.resolve import refine_with_jev

        identity = refine_with_jev(
            identity,
            passage=summary_text[:8000],
            candidate_name=entry.system_name or entry.company or "the candidate",
            adapter=jev or JevAdapter(),
            budget=budget,
            cache=cache,
        )
        usage = identity.get("jev_usage") or {}
        resolve_stage = {
            "stage": "resolve",
            "model": usage.get("model"),
            "question_version": IDENTITY_QUESTION_VERSION,
            "input_tokens": usage.get("input_tokens", 0),
            "cost_usd": usage.get("cost_usd", 0.0),
            "cache_hits": 1 if usage.get("cache_hit") else 0,
            "calls": 0 if usage.get("cache_hit") else 1,
        }
    (directory / "identity.json").write_text(
        json.dumps(identity, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    record_id = entry.record_id or (
        identity["matched_records"][0]["id"]
        if identity["matched_records"] and identity["proposed_decision"] == "update"
        else None
    )
    stages.append(resolve_stage)

    # Stage 4: extract.
    hints: dict[str, Any] = {
        "company": entry.company,
        "system_name": entry.system_name,
        "record_id": record_id,
    }
    record, stage = run_extract(
        run_id=run_id,
        paragraphs_by_source=paragraphs,
        sources=sources,
        hints=hints,
        adapter=writer or WriterAdapter(),
        budget=budget,
    )
    stages.append(stage)
    # The STOP-line guard: contact data the writer produced stops the run here.
    privacy.assert_clean(json.loads(record.model_dump_json()), label=f"{run_id} stage 4")
    # The queue's record-id hint is authoritative: the writer may echo a
    # matched-record ID of its own choosing instead of the run's intent.
    candidate_updates: dict[str, Any] = {}
    if entry.record_id:
        candidate_updates["record_id"] = entry.record_id
    # The identity stage's shortlist — not the writer's echo — is what the
    # reviewer reads on the sheet, with the Jev advisory column when it ran.
    candidate_updates["matched_records"] = [
        MatchedRecord(
            id=entry_["id"],
            same_system=entry_.get("score"),
            same_system_jev=entry_.get("same_system_jev"),
            reason=entry_.get("reason"),
        )
        for entry_ in identity["matched_records"]
    ]
    record = record.model_copy(
        update={"candidate": record.candidate.model_copy(update=candidate_updates)}
    )
    (directory / "extraction.yaml").write_text(
        yaml.safe_dump(json.loads(record.model_dump_json()), sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    # Stage 5: verify quotes.
    record = verify_claims(record, paragraphs)
    stages.append({"stage": "verify", "model": None, "calls": 0, "cost_usd": 0.0})

    # Stage 6: judge.
    outcome = judge_claims(
        record, paragraphs, adapter=jev or JevAdapter(), budget=budget, cache=cache
    )
    record, stage = outcome.record, outcome.stage
    stages.append(stage)

    # Stage 7: numbers and dates, then the coarse gate over both.
    record, stage = _numbers_stage(record)
    stages.append(stage)
    record = apply_dispositions(record)
    (directory / "extraction-gated.yaml").write_text(
        yaml.safe_dump(json.loads(record.model_dump_json()), sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    # Stage 8: confidence reasons.
    from intake.write import run_write

    record, stage = run_write(record, adapter=writer or WriterAdapter(), budget=budget)
    stages.append(stage)
    # The reasons are the last writer text; guard them like the claims.
    privacy.assert_clean(json.loads(record.model_dump_json()), label=f"{run_id} stage 8")

    # Stage 10: render.
    result = render_extraction(record, reviewed_at=reviewed_at)
    stages.append({"stage": "render", "model": None, "calls": 0, "cost_usd": 0.0})
    notes.extend(result.notes)

    # Stage 11: validate the draft with the build's own rules.
    draft_id = result.record.get("id")
    build.validate_record(result.record, Path(f"{draft_id or 'draft'}.yaml"), set())
    stages.append({"stage": "validate", "model": None, "calls": 0, "cost_usd": 0.0})

    # Stage 9: preflight flags for the sheet.
    flags = preflight_flags(record, result)

    # Stage 12: the review sheet and the run manifest.
    draft_path = None
    if draft_id:
        drafts_root.mkdir(parents=True, exist_ok=True)
        draft_path = drafts_root / f"{draft_id}.yaml"
        if draft_path.exists():
            raise FileExistsError(f"{draft_path} already exists; drafts are never overwritten")
        draft_path.write_text(result.record_yaml, encoding="utf-8")
    sheet = review_sheet(record, result, stages=stages, preflight_flags=flags)
    _sheet_path, _manifest_path = write_review(
        directory,
        sheet=sheet,
        record=record,
        result=result,
        stages=stages,
        queue_entry=entry.payload(),
        notes=notes,
    )
    return RunSummary(
        run_id=run_id,
        record_id=draft_id,
        decision=record.candidate.decision,
        draft_path=draft_path,
        sheet_path=_sheet_path,
        stages=stages,
        notes=notes,
    )


def _page_title(capture: Any) -> str:
    from intake.capture import read_staging

    return str(read_staging(capture.staging_dir)["page"].get("title") or capture.canonical_url)


def _page_published(capture: Any) -> str | None:
    from intake.capture import read_staging

    published = read_staging(capture.staging_dir)["page"].get("published_at")
    if not published:
        return None
    return published[:10]


def run_queue(
    path: Path,
    *,
    budget_usd: float = DEFAULT_BUDGET_USD,
    runs_root: Path = RUNS_ROOT,
    drafts_root: Path = DRAFTS_ROOT,
    staging_root: Path | None = None,
    steel: SteelSdkAdapter | None = None,
    writer: WriterAdapter | None = None,
    jev: JevAdapter | None = None,
    cache: Any = None,
) -> list[RunSummary]:
    """Run every queue entry inside one budget."""
    entries = load_queue(path)
    budget = Budget(budget_usd=budget_usd)
    return [
        run_candidate(
            entry,
            budget=budget,
            steel=steel,
            writer=writer,
            jev=jev,
            cache=cache,
            runs_root=runs_root,
            drafts_root=drafts_root,
            staging_root=staging_root,
        )
        for entry in entries
    ]
