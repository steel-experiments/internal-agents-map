# ABOUTME: Drift mode: rescrape captures and report what changed (Plan 017, Gap 3).
# ABOUTME: A report and proposed new captures; applying them stays with a person.
"""Detect content drift between a live page and its preserved capture.

Every source with a capture is rescraped without saving, normalised, and
hashed against the capture's preserved Markdown. On change the drift report
diffs the paragraphs, maps the changed paragraph ranges to the claims that
cite those lines, and proposes a new capture under a new source ID. The
rescrape uses the Steel adapter; the report itself is written to
`.intake/drift/` and never edits a record.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from intake.adapters.steel import SteelSdkAdapter
from intake.capture import HEADER_LINES
from intake.catalog import load_build
from intake.verify_quotes import normalize_text

ROOT = Path(__file__).resolve().parent.parent
DRIFT_ROOT = ROOT / ".intake" / "drift"
LOCATOR_RE = re.compile(r"^Preserved content\.md, lines? (?P<lines>[0-9][0-9, –-]*)$", re.DOTALL)


class DriftError(RuntimeError):
    """The drift run could not read a record or its capture."""


@dataclass
class SourceDrift:
    """The drift of one source."""

    source_id: str
    record_id: str
    url: str
    changed: bool
    changed_lines: list[range] = field(default_factory=list)
    affected_claims: list[str] = field(default_factory=list)
    claim_verdicts: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None
    new_markdown: str | None = None

    def to_payload(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "record_id": self.record_id,
            "url": self.url,
            "changed": self.changed,
            "changed_lines": [
                {"start": span.start, "end": span.stop - 1} for span in self.changed_lines
            ],
            "affected_claims": self.affected_claims,
            "claim_verdicts": self.claim_verdicts,
            "error": self.error,
        }


def _locator_spans(locator: str | None) -> list[range]:
    if not locator:
        return []
    match = LOCATOR_RE.fullmatch(" ".join(locator.split()))
    if match is None:
        return []
    numbers = [
        int(value) for value in re.split(r"[,–-]", match.group("lines")) if value.strip().isdigit()
    ]
    if not numbers:
        return []
    return [range(min(numbers), max(numbers) + 1)]


def _changed_line_spans(old: str, new: str) -> list[range]:
    """The contiguous line spans that differ between two texts."""
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    spans: list[range] = []
    index = 0
    while index < max(len(old_lines), len(new_lines)):
        old_slice = old_lines[index] if index < len(old_lines) else None
        new_slice = new_lines[index] if index < len(new_lines) else None
        same = (
            old_slice is not None
            and new_slice is not None
            and (normalize_text(old_slice) == normalize_text(new_slice))
        )
        if same:
            index += 1
            continue
        start = index
        while index < max(len(old_lines), len(new_lines)):
            old_slice = old_lines[index] if index < len(old_lines) else None
            new_slice = new_lines[index] if index < len(new_lines) else None
            if (
                old_slice is not None
                and new_slice is not None
                and (normalize_text(old_slice) == normalize_text(new_slice))
            ):
                break
            index += 1
        spans.append(range(start + 1, index + 1))
    return spans


def drift_one(
    *,
    record_id: str,
    source: dict[str, Any],
    adapter: SteelSdkAdapter,
) -> SourceDrift:
    """Rescrape one source and compare against its preserved capture."""
    capture = (source.get("capture") or {}).get("manifest_path")
    url = source.get("url")
    if not capture or not url:
        return SourceDrift(
            source_id=source.get("id", "?"),
            record_id=record_id,
            url=str(url or ""),
            changed=False,
            error="no capture or no URL; skipped",
        )
    try:
        raw = (ROOT / capture).parent.joinpath("content.md").read_text(encoding="utf-8")
    except OSError as error:
        raise DriftError(f"{record_id}: could not read the capture: {error}") from error
    lines = raw.splitlines()
    if len(lines) <= HEADER_LINES or lines[HEADER_LINES - 1] != "":
        raise DriftError(f"{record_id}: {capture} does not carry the capture header")
    # The preserved file starts with the placeholder header; a fresh scrape
    # returns the page alone. Compare body against body, then shift the
    # spans back so they number lines the way locators do.
    preserved = "\n".join(lines[HEADER_LINES:])
    try:
        page = adapter.scrape(str(url))
    except Exception as error:  # a collection blocker, reported per source
        return SourceDrift(
            source_id=source["id"],
            record_id=record_id,
            url=str(url),
            changed=False,
            error=f"rescrape failed: {error}",
        )
    if normalize_text(preserved) == normalize_text(page.markdown):
        return SourceDrift(source_id=source["id"], record_id=record_id, url=str(url), changed=False)
    spans = [
        range(span.start + HEADER_LINES, span.stop + HEADER_LINES)
        for span in _changed_line_spans(preserved, page.markdown)
    ]
    return SourceDrift(
        source_id=source["id"],
        record_id=record_id,
        url=str(url),
        changed=True,
        changed_lines=spans,
        new_markdown=page.markdown,
    )


def affected_claim_paths(record: dict[str, Any], spans: list[range]) -> list[str]:
    """The claim paths whose locators fall inside a changed span."""
    paths = []
    for path, links in record.get("evidence", {}).items():
        for link in links:
            locator = link.get("locator")
            for cited in _locator_spans(locator):
                if any(line in span for span in spans for line in cited):
                    paths.append(path)
                    break
            else:
                continue
            break
    return sorted(set(paths))


def _widened_passage(lines: list[str], start: int, end: int) -> str:
    """The changed span widened to the surrounding blank-line paragraph."""
    start = max(start, 1)
    end = min(end, len(lines))
    while start > 1 and lines[start - 2].strip():
        start -= 1
    while end < len(lines) and lines[end].strip():
        end += 1
    return "\n".join(lines[start - 1 : end])


def judge_drifted(
    *,
    record: dict[str, Any],
    source_id: str,
    affected: list[str],
    new_markdown: str,
    spans: list[range],
    adapter: Any,
    budget: Any,
    cache: Any = None,
    build: Any = None,
) -> list[dict[str, Any]]:
    """Run the judge's questions on the affected claims against the new text.

    Advisory only: the verdicts tell the reviewer whether each claim still
    holds in the rescraped page. A person still captures and reviews.
    """

    import hashlib

    from intake.cache import cache_key, jev_cache
    from intake.judge import build_request, judgments_from_answers, load_questions
    from intake.models import Claim, Quote
    from intake.segment import Paragraph

    if not affected:
        return []
    if build is None:
        from intake.catalog import load_build

        build = load_build()
    cache = cache or jev_cache()
    questions = load_questions()
    model = questions["model"]
    claims_map = build.claim_fields(record)
    body_lines = new_markdown.splitlines()
    verdicts: list[dict[str, Any]] = []
    for path in affected:
        entry = claims_map.get(path)
        if entry is None:
            continue
        text, kind, provenance = entry
        # The spans number the preserved file with its header; the new page
        # has none, so shift back before widening to the paragraph.
        body_spans = [
            range(max(span.start - HEADER_LINES, 1), max(span.stop - HEADER_LINES, 1))
            for span in spans
        ]
        passage = _widened_passage(
            body_lines,
            min(span.start for span in body_spans),
            max(span.stop for span in body_spans),
        )
        if not passage.strip():
            continue
        passage_hash = f"sha256:{hashlib.sha256(passage.encode('utf-8')).hexdigest()}"
        key = cache_key(text, "drift", passage_hash, path, str(questions.get("version", 1)), model)
        cached = cache.get(key)
        if cached is not None:
            verdicts.append(cached)
            continue
        claim = Claim(
            id=f"drift:{path}",
            field="summary",
            text=text,
            kind=kind,
            provenance=provenance,
            quotes=[Quote(source=source_id, text=text, paragraph_id="p1")],
            disposition="review",
        )
        paragraph = Paragraph(id="p1", heading_path=(), start=1, end=1, text=passage)
        state, request_questions = build_request([claim], [paragraph], questions)
        result = adapter.ask(state=state, questions=request_questions, budget=budget)
        judgments = judgments_from_answers(claim, result.answers, 0, result.model)
        verdict = {
            "path": path,
            "relation": (
                f"{judgments.relation.label} ({judgments.relation.p:.2f})"
                if judgments.relation
                else None
            ),
            "actor_mismatch": judgments.actor_mismatch,
            "temporal": (
                f"{judgments.temporal.label} ({judgments.temporal.p:.2f})"
                if judgments.temporal
                else None
            ),
        }
        cache.put(key, verdict)
        verdicts.append(verdict)
    return verdicts


def drift_report(
    *,
    adapter: SteelSdkAdapter,
    records: list[dict[str, Any]] | None = None,
    jev: Any = None,
    budget: Any = None,
    cache: Any = None,
    output: Path | None = None,
) -> dict[str, Any]:
    """Rescrape every captured source and write the drift report.

    With a Jev adapter and a budget, each changed source's affected claims are
    re-judged against the rescraped text as advisory verdicts. Without them the
    report lists the affected claims and stops there.
    """
    build = load_build()
    if records is None:
        records = build.load_agents()
    results: list[SourceDrift] = []
    for record in records:
        for source in record.get("sources", []):
            drift = drift_one(record_id=record["id"], source=source, adapter=adapter)
            if drift.changed:
                drift.affected_claims = affected_claim_paths(record, drift.changed_lines)
                if jev is not None and budget is not None and drift.affected_claims:
                    drift.claim_verdicts = judge_drifted(
                        record=record,
                        source_id=source["id"],
                        affected=drift.affected_claims,
                        new_markdown=drift.new_markdown or "",
                        spans=drift.changed_lines,
                        adapter=jev,
                        budget=budget,
                        cache=cache,
                        build=build,
                    )
            results.append(drift)
    payload = {
        "format_version": 1,
        "sources_checked": len(results),
        "sources_changed": sum(1 for result in results if result.changed),
        "errors": sum(1 for result in results if result.error),
        "drift": [result.to_payload() for result in results if result.changed],
        "blocked": [result.to_payload() for result in results if result.error],
    }
    target = output or (DRIFT_ROOT / "report.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


def report_markdown(payload: dict[str, Any]) -> str:
    """Render the drift report as the Markdown sheet a reviewer reads."""
    lines = [
        "# Drift report",
        "",
        f"{payload['sources_checked']} sources checked; "
        f"{payload['sources_changed']} changed; {payload['errors']} blocked.",
        "",
    ]
    if not payload["drift"]:
        lines.append("No source changed against its preserved capture.")
    for entry in payload["drift"]:
        spans = ", ".join(f"{span['start']}–{span['end']}" for span in entry["changed_lines"])
        claims = ", ".join(entry["affected_claims"]) or "none"
        lines.append(
            f"- `{entry['source_id']}` ({entry['record_id']}): changed lines {spans}; "
            f"affected claims: {claims}. Capture the page again under a new source "
            "ID and review the claims before citing it."
        )
        for verdict in entry.get("claim_verdicts") or []:
            flags = []
            if verdict.get("actor_mismatch") is not None:
                flags.append(f"actor {verdict['actor_mismatch']:.2f}")
            if verdict.get("temporal"):
                flags.append(f"temporal {verdict['temporal']}")
            flag_text = f"; {', '.join(flags)}" if flags else ""
            lines.append(
                f"  - `{verdict['path']}`: relation {verdict.get('relation') or 'unknown'}"
                f"{flag_text} — advisory, against the rescraped text"
            )
    for entry in payload["blocked"]:
        lines.append(f"- `{entry['source_id']}` ({entry['record_id']}): {entry['error']}")
    lines.append("")
    lines.append("The pipeline proposes; a person captures and reviews.")
    return "\n".join(lines) + "\n"
