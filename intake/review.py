# ABOUTME: Stage 12 of the intake pipeline: the review sheet and run manifest (Plan 017).
# ABOUTME: A person reads the sheet, edits the draft, and opens the pull request.
"""Write the review sheet and the run manifest for one pipeline run.

The sheet lists every claim with its quote, its line locator, its numeric
check, its Jev verdicts with probabilities, its disposition, and the open
questions. It names the decision the pipeline proposes and the decision a
person must make. The run manifest records the model strings the APIs
returned, the prompt and question versions, token usage, cost, cache hits, and
the claim-ID-to-path compatibility map.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from intake.models import ExtractionRecord
from intake.render import RenderResult


def claim_row(claim: Any) -> dict[str, Any]:
    """One sheet row for one claim."""
    quotes = []
    for quote in claim.quotes:
        lines = quote.lines
        quotes.append(
            {
                "source": quote.source,
                "match": quote.match,
                "lines": f"{lines[0]}–{lines[1]}" if lines else "—",
                "text": quote.text,
            }
        )
    judgments = claim.judgments
    verdicts: dict[str, Any] = {}
    if judgments is not None:
        for name in ("relation", "temporal", "basis"):
            verdict = getattr(judgments, name)
            if verdict is not None:
                verdicts[name] = f"{verdict.label} ({verdict.p:.2f})"
        if judgments.actor_mismatch is not None:
            verdicts["actor_mismatch"] = f"{judgments.actor_mismatch:.2f}"
        if judgments.approval_removed is not None:
            verdicts["approval_removed"] = f"{judgments.approval_removed:.2f}"
    numbers_ok = None
    if claim.numbers:
        numbers_ok = all(check.in_quote for check in claim.numbers)
    return {
        "claim_id": claim.id,
        "field": claim.field,
        "disposition": claim.disposition,
        "kind": claim.kind,
        "provenance": claim.provenance,
        "text": claim.text,
        "quotes": quotes,
        "numbers_ok": numbers_ok,
        "verdicts": verdicts,
        "review_note": claim.review_note,
    }


def _open_questions(questions: Any) -> list[tuple[str, str | None]]:
    """Every reader question the extraction left unanswered.

    Principle 5: unanswered questions render as ``not-reviewed`` and a person
    flips them after reading; this lists them so the person sees which ones.
    """
    open_questions: list[tuple[str, str | None]] = []
    for name in (
        "purpose",
        "workflow",
        "human_involvement",
        "implementation",
        "validation",
        "observations",
        "lessons",
    ):
        answer = getattr(questions, name)
        if not answer.claim_ids:
            open_questions.append((name, answer.note))
    for field_name, answer in sorted(questions.implementation_fields.items()):
        if not answer.claim_ids:
            open_questions.append((f"implementation_fields.{field_name}", answer.note))
    return open_questions


def review_sheet(
    record: ExtractionRecord,
    result: RenderResult,
    *,
    stages: list[dict[str, Any]] | None = None,
    preflight_flags: list[Any] | None = None,
    cross_flags: list[dict[str, Any]] | None = None,
    source_role: str | None = None,
    eligibility: dict[str, Any] | None = None,
    blockers: list[dict[str, str]] | None = None,
) -> str:
    """Render the Markdown sheet a reviewer reads."""
    candidate = record.candidate
    lines: list[str] = [
        f"# Intake review: {candidate.company}"
        + (f" — {candidate.system_name}" if candidate.system_name else ""),
        "",
        f"Run `{record.run_id}`; proposed decision: **{candidate.decision}**; "
        + (
            f"draft record `{candidate.record_id}`."
            if candidate.record_id
            else "no record ID proposed; a person decides."
        ),
        "",
        "## Sources",
        "",
    ]
    for source in record.sources:
        promoted = source.capture_manifest_path or "staged only, not promoted"
        published = f", published {source.published_at}" if source.published_at else ""
        lines.append(
            f"- `{source.local_id}` {source.title} — {source.url} ({source.kind}, "
            f"{source.provenance_class}{published}); {promoted}"
        )
    lines.append("")
    if source_role:
        lines.append(
            f"The queue hint set every source's provenance class to "
            f"`{source_role}`; confirm it against each page. The `kind` stayed "
            "the conservative `other`; set the real one."
        )
    else:
        lines.append(
            "No queue hint named a source role, so every source staged "
            "conservatively (`other`, `independent-secondary`); set the real "
            "kind and class."
        )
    if blockers:
        lines.extend(["", "## Collection blockers", ""])
        lines.append(
            "These URLs failed the page checks and were not captured. Capture "
            "them by hand or drop them; nothing was reconstructed from "
            "snippets, a search result, or memory."
        )
        for item in blockers:
            lines.append(f"- {item['url']}: {item['error']}")
    matched = candidate.matched_records
    if matched:
        lines.extend(["", "## Identity", ""])
        for entry in matched:
            same = getattr(entry, "same_system", None)
            same_column = (
                f", deterministic score {same:.2f}" if isinstance(same, (int, float)) else ""
            )
            jev = getattr(entry, "same_system_jev", None)
            jev_column = f", Jev same-system {jev:.2f}" if isinstance(jev, (int, float)) else ""
            reason = getattr(entry, "reason", None)
            reason_column = f" — {reason}" if reason else ""
            lines.append(f"- `{entry.id}`{same_column}{jev_column}{reason_column}")
    if eligibility:
        lines.extend(["", "## Eligibility", ""])
        lines.append(
            f"Proposal: **{eligibility['decision']}** "
            f"(the writer proposed `{eligibility['writer_decision']}`). "
            "No numerical score; a person decides."
        )
        lines.extend(f"- {reason}" for reason in eligibility["reasons"])
    lines.extend(["", "## Claims", ""])
    header = "| Claim | Field | Disposition | Quote match | Numbers | Verdicts | Flags | Note |"
    lines.extend([header, "| --- | --- | --- | --- | --- | --- | --- | --- |"])
    for claim in record.claims:
        row = claim_row(claim)
        quote_matches = ",".join(quote["match"] for quote in row["quotes"]) or "—"
        lines_of_quotes = ",".join(quote["lines"] for quote in row["quotes"])
        numbers = "—" if row["numbers_ok"] is None else ("ok" if row["numbers_ok"] else "check")
        verdicts = "; ".join(
            row["verdicts"][name]
            for name in ("relation", "temporal", "basis")
            if name in row["verdicts"]
        )
        flags = [name for name in ("actor_mismatch", "approval_removed") if name in row["verdicts"]]
        note = row["review_note"] or ""
        lines.append(
            f"| `{row['claim_id']}` | {row['field']} | {row['disposition']} | "
            f"{quote_matches} ({lines_of_quotes}) | {numbers} | {verdicts or '—'} | "
            f"{', '.join(flags) or '—'} | {note} |"
        )
    if record.questions is not None:
        open_questions = _open_questions(record.questions)
        if open_questions:
            lines.extend(["", "## Open questions", ""])
            lines.extend(
                f"- `{name}`: no claim answers it, so the draft records "
                f"`not-reviewed`{f' — {note}' if note else ''}."
                for name, note in open_questions
            )
    if result.notes:
        lines.extend(["", "## Renderer notes", ""])
        lines.extend(f"- {note}" for note in result.notes)
    if preflight_flags:
        lines.extend(["", "## Preflight flags", ""])
        lines.extend(
            f"- `{flag.claim_id}` ({flag.field}): {flag.issue}" for flag in preflight_flags
        )
    if cross_flags:
        lines.extend(["", "## Cross-source checks", ""])
        lines.extend(
            f"- `{flag['claim_path']}`: {flag['issue']}"
            + (f" (recorded {flag['existing']}, new {flag['new']})" if flag["new"] else "")
            + ". The draft carries the new quote as a `contradicts` link on the "
            "existing claim; a person decides whether the numbers describe the "
            "same observation."
            for flag in cross_flags
        )
    if stages:
        lines.extend(["", "## Model usage", ""])
        lines.append("| Stage | Model | Calls | Input tokens | Output tokens | Cost USD |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for stage in stages:
            lines.append(
                f"| {stage.get('stage')} | {stage.get('model') or '—'} | "
                f"{stage.get('calls', 1)} | {stage.get('input_tokens', 0)} | "
                f"{stage.get('output_tokens', 0)} | {stage.get('cost_usd', 0.0)} |"
            )
    lines.extend(
        [
            "",
            "## The decision a person makes",
            "",
            "1. Confirm the identity decision and the eligibility proposal.",
            "2. Set each source's real `kind` and confirm its provenance class",
            "   (see Sources above).",
            "3. Read every claim row with disposition `review`; edit the draft.",
            "4. Confirm `published_at` where no quote states it.",
            "5. Confirm no person's name or contact detail appears outside a",
            "   source's `authors` field; code catches e-mail addresses only.",
            "6. Review the capture bundles (promoted under `archive/sources/`",
            "   when the run drafted a record; still staged otherwise), add the",
            "   company entry, and open the pull request. The pipeline does",
            "   none of this.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def write_review(
    directory: Path,
    *,
    sheet: str,
    record: ExtractionRecord,
    result: RenderResult,
    stages: list[dict[str, Any]],
    queue_entry: dict[str, Any],
    notes: list[str] | None = None,
) -> tuple[Path, Path]:
    """Write review.md and run.json into one run directory."""

    from intake.budget import write_manifest

    sheet_path = directory / "review.md"
    sheet_path.write_text(sheet, encoding="utf-8")
    model_strings = {stage["stage"]: stage["model"] for stage in stages if stage.get("model")}
    prompt_versions = {
        stage["stage"]: stage["prompt_version"] for stage in stages if stage.get("prompt_version")
    }
    capture_hashes = {source.local_id: source.content_sha256 for source in record.sources}
    manifest_path = write_manifest(
        directory,
        run_id=record.run_id,
        queue_entry=queue_entry,
        stage_runs=stages,
        model_strings=model_strings,
        prompt_versions=prompt_versions,
        capture_hashes=capture_hashes,
        compatibility=result.compatibility,
        decision=record.candidate.decision,
        record_id=record.candidate.record_id,
        notes=notes,
    )
    return sheet_path, manifest_path


def load_review(run_id: str, runs_root: Path | None = None) -> str:
    """Print-ready sheet for one recorded run."""
    root = runs_root or (Path(__file__).resolve().parent.parent / ".intake" / "runs")
    path = root / run_id / "review.md"
    if not path.is_file():
        raise FileNotFoundError(f"no review sheet for run {run_id} under {root}")
    return path.read_text(encoding="utf-8")
