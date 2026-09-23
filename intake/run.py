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
from intake.budget import Budget, BudgetExceededError, new_run_id, run_directory
from intake.capture import CaptureStageError, StagedCapture, capture_staging
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
        role = item.get("source_role")
        if role is not None:
            # The build's own class set is the rule; a typo stops the queue
            # before any capture or spend.
            from intake.catalog import load_build

            allowed = load_build().PROVENANCE_CLASSES
            if role not in allowed:
                raise QueueError(
                    f"{path}: entry {index} source_role {role!r} is not one of: "
                    + ", ".join(sorted(allowed))
                )
        homepage = item.get("homepage")
        if homepage is not None and not str(homepage).startswith("https://"):
            # The hint reaches the company entry through model_copy, which
            # skips field validation, so the queue is where it must be caught.
            raise QueueError(f"{path}: entry {index} homepage must use HTTPS: {homepage!r}")
        entries.append(
            QueueEntry(
                urls=urls,
                company=item.get("company"),
                system_name=item.get("system_name"),
                record_id=item.get("record_id"),
                source_role=role,
                homepage=str(homepage) if homepage is not None else None,
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
    writer_cache: Any = None,
    runs_root: Path = RUNS_ROOT,
    drafts_root: Path = DRAFTS_ROOT,
    staging_root: Path | None = None,
    reviewed_at: str | None = None,
    repo_root: Path = ROOT,
) -> RunSummary:
    """Run all twelve stages for one queue candidate."""
    import datetime as dt

    from intake.cache import jev_cache
    from intake.cache import writer_cache as default_writer_cache
    from intake.catalog import load_build

    cache = cache or jev_cache()
    writer_cache = writer_cache if writer_cache is not None else default_writer_cache()
    reviewed_at = reviewed_at or dt.date.today().isoformat()
    # The product contract: a run refuses to start when its worst-case
    # reservation cannot fit the budget. The judge's request count is
    # unknowable before extraction, but the writer floor — one extract and
    # one write call — is, so the admission check runs before anything is
    # captured or spent instead of letting the run pay for its extract call
    # and die at the write reservation.
    floor = budget.total_reservation(2)
    if floor > budget.budget_usd + 1e-9:
        raise BudgetExceededError(
            f"this run needs at least {floor:.4f} USD worst case (one extract "
            f"and one write call), above the {budget.budget_usd:.4f} USD budget"
        )
    run_id = new_run_id()
    directory = run_directory(run_id, runs_root=runs_root)
    stages: list[dict[str, Any]] = []
    notes: list[str] = []

    # Stage 1: capture every URL into staging. A failed capture is a
    # collection blocker for that URL — reported, never worked around — and
    # the run continues with the other URLs.
    capture_kwargs = {"adapter": steel}
    if staging_root is not None:
        capture_kwargs["staging_root"] = staging_root
    staged: list[StagedCapture] = []
    blockers: list[dict[str, str]] = []
    for url in entry.urls:
        try:
            staged.append(capture_staging(url, **capture_kwargs))
        except CaptureStageError as error:
            blockers.append({"url": url, "error": str(error)})
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
            # The queue's role hint names the class when the author stated
            # one; the conservative default stays otherwise.
            provenance_class=entry.source_role or "independent-secondary",
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
            "calls": len(entry.urls),
        }
    )
    if blockers:
        (directory / "blockers.json").write_text(
            json.dumps(blockers, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        notes.extend(f"collection blocker: {item['url']}: {item['error']}" for item in blockers)
    if not staged:
        # No URL survived its page checks; there is nothing to draft. The
        # run directory holds the blocker list, and the queue continues.
        return RunSummary(
            run_id=run_id,
            record_id=None,
            decision="blocked",
            draft_path=None,
            sheet_path=None,
            stages=stages,
            notes=notes,
        )

    # Stage 2: segment every capture.
    from intake.capture import HEADER_LINES, read_staging

    paragraphs = {}
    for source in sources:
        bundle = read_staging(Path(source.staging_path or ""))
        # The staging header is archiver bookkeeping and carries the capture
        # timestamp; the writer never sees it, so a warm rerun's input is
        # byte-identical. Paragraph IDs and line ranges keep numbering the
        # full file, so locators stay stable.
        paragraphs[source.local_id] = [
            paragraph
            for paragraph in segment_content(bundle["content"])
            if paragraph.end > HEADER_LINES
        ]
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
            "input_hashes": [usage["input_sha256"]] if usage.get("input_sha256") else [],
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
        cache=writer_cache,
    )
    stages.append(stage)
    # The STOP-line guard: contact data the writer produced stops the run here.
    privacy.assert_clean(json.loads(record.model_dump_json()), label=f"{run_id} stage 4")
    # The queue's record-id hint is authoritative: the writer may echo a
    # matched-record ID of its own choosing instead of the run's intent.
    candidate_updates: dict[str, Any] = {}
    if entry.record_id:
        candidate_updates["record_id"] = entry.record_id
    # The queue's company and homepage hints are input data the writer
    # cannot know; they drive the company entry the renderer produces.
    if entry.company:
        candidate_updates["company"] = entry.company
    if entry.homepage:
        candidate_updates["homepage"] = entry.homepage
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
    # The decision policy's eligibility proposal: categorical, over the
    # accepted claims, with reasons. No numerical score.
    from intake.eligibility import propose_eligibility

    eligibility = propose_eligibility(record)
    notes.append(f"eligibility proposal: {eligibility['decision']}")

    # Stage 8: confidence reasons.
    from intake.write import run_write

    record, stage = run_write(
        record, adapter=writer or WriterAdapter(), budget=budget, cache=writer_cache
    )
    stages.append(stage)
    # The reasons are the last writer text; guard them like the claims.
    privacy.assert_clean(json.loads(record.model_dump_json()), label=f"{run_id} stage 8")

    # Stage 10: render. An update numbers its new sources after the existing
    # record's, and its claims are cross-checked against them.
    from intake import crosscheck

    existing = crosscheck.load_existing(record_id)
    cross_flags = crosscheck.number_conflicts(existing, record) if existing is not None else []
    result = render_extraction(
        record,
        reviewed_at=reviewed_at,
        existing=existing,
        contradictions=cross_flags,
    )
    stages.append({"stage": "render", "model": None, "calls": 0, "cost_usd": 0.0})
    notes.extend(result.notes)

    # Stage 11: validate the draft with the build's own rules.
    draft_id = result.record.get("id")
    build.validate_record(result.record, Path(f"{draft_id or 'draft'}.yaml"), set())
    stages.append({"stage": "validate", "model": None, "calls": 0, "cost_usd": 0.0})

    # Stage 10's promotion half: only a validating draft earns it. The
    # product contract names the promoted bundles under archive/sources/ as
    # a run output; the archiver's append-only writer stays the single
    # writer, and a rerun that meets its own identical bundle reuses it.
    if draft_id:
        from intake.capture import promote_staging

        rendered_new = result.record["sources"][-len(sources) :]
        promoted = [
            source.model_copy(
                update={
                    "capture_manifest_path": promote_staging(
                        Path(source.staging_path or ""), rendered["id"], repo_root=repo_root
                    )
                }
            )
            for source, rendered in zip(sources, rendered_new)
        ]
        record = record.model_copy(update={"sources": promoted})
        result = render_extraction(
            record, reviewed_at=reviewed_at, existing=existing, contradictions=cross_flags
        )
        # The record itself is unchanged from the validated draft; the only
        # addition is the capture blocks, so the build's own manifest
        # validator — with its root parameter — checks exactly those,
        # against the bundles this run just wrote.
        for source_entry in result.record["sources"][-len(promoted) :]:
            build.load_capture_manifest(source_entry, Path(f"{draft_id}.yaml"), root=repo_root)
        notes.append(
            f"promoted {len(promoted)} capture bundle(s) under archive/sources/; "
            "the pull request carries them"
        )

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
        # The run's own archival copy: a stage rerun reads its review date
        # and promoted capture paths from here, never from today's clock.
        (directory / "draft.yaml").write_text(result.record_yaml, encoding="utf-8")
    sheet = review_sheet(
        record,
        result,
        stages=stages,
        preflight_flags=flags,
        cross_flags=cross_flags,
        source_role=entry.source_role,
        eligibility=eligibility,
        blockers=blockers,
    )
    _sheet_path, _manifest_path = write_review(
        directory,
        sheet=sheet,
        record=record,
        result=result,
        stages=stages,
        queue_entry=entry.payload(),
        notes=notes,
    )
    # Open decision 1's recommendation: commit one run.json per drafted
    # record under archive/intake/, so a reader sees the record was
    # machine-drafted and by which model, with the compatibility map. The
    # per-run history stays under .intake/runs/<run-id>/ (never overwritten);
    # the archived copy records the latest run that drafted the record, so a
    # warm rerun supersedes it instead of failing.
    archived_manifest: Path | None = None
    if draft_id:
        import shutil

        intake_dir = repo_root / "archive" / "intake" / draft_id
        intake_dir.mkdir(parents=True, exist_ok=True)
        archived_manifest = intake_dir / "run.json"
        shutil.copyfile(_manifest_path, archived_manifest)
        notes.append(
            f"run manifest archived at {archived_manifest.relative_to(repo_root).as_posix()}"
        )
    # The product contract: a company registry entry when the organization
    # is new. The run knows the registry from stage 3, so it decides.
    if result.company_entry is not None:
        entry_id = str(result.company_entry.get("id"))
        known = any(
            str(company.get("id")) == entry_id
            or str(company.get("name", "")).lower() == str(entry.company or "").lower()
            for company in companies
        )
        if known:
            notes.append(
                f"organization already in data/companies.yaml ({entry_id}); "
                "no company entry written"
            )
        else:
            entry_text = yaml.safe_dump(
                [result.company_entry], sort_keys=False, allow_unicode=True, width=100
            )
            entry_path = directory / "company-entry.yaml"
            entry_path.write_text(entry_text, encoding="utf-8")
            if draft_id:
                shutil.copyfile(
                    entry_path, repo_root / "archive" / "intake" / draft_id / "company-entry.yaml"
                )
            notes.append(
                "company entry written; append it to data/companies.yaml "
                "(keep the list sorted by id)"
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
    writer_cache: Any = None,
    repo_root: Path = ROOT,
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
            writer_cache=writer_cache,
            runs_root=runs_root,
            drafts_root=drafts_root,
            staging_root=staging_root,
            repo_root=repo_root,
        )
        for entry in entries
    ]
