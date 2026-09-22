# ABOUTME: Rerun one pipeline stage from a saved run directory (Plan 017).
# ABOUTME: Offline stages rerun from artifacts; model stages come from their caches.
"""Rerun one stage of a recorded run.

A run directory holds every stage's artifact. The offline stages (segment,
resolve, verify, render, review) rerun from those artifacts without any model
call; the model-driven stages are driven by their caches, so a warm-cache
rerun of the whole run is byte-identical. Reruns never overwrite the original
artifacts; the new output goes to ``<artifact>.rerun`` beside it.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from intake.models import ExtractionRecord, finalize

ROOT = Path(__file__).resolve().parent.parent
RUNS_ROOT = ROOT / ".intake" / "runs"

RERUNNABLE = ("segment", "resolve", "verify", "render", "review")


class StageRerunError(RuntimeError):
    """The stage cannot rerun from this run directory."""


def _run_dir(run_id: str, runs_root: Path | None = None) -> Path:
    directory = (runs_root or RUNS_ROOT) / run_id
    if not directory.is_dir():
        raise StageRerunError(f"no run directory for {run_id}")
    return directory


def _load_extraction(directory: Path) -> ExtractionRecord:
    gated = directory / "extraction-gated.yaml"
    source = gated if gated.is_file() else directory / "extraction.yaml"
    if not source.is_file():
        raise StageRerunError(f"no extraction artifact under {directory}")
    payload = yaml.safe_load(source.read_text(encoding="utf-8"))
    payload.pop("schema_version", None)
    return finalize(ExtractionRecord.model_validate(payload))


def run_stage(
    name: str,
    run_id: str,
    *,
    runs_root: Path | None = None,
) -> int:
    """Rerun one stage; prints where the new artifact landed."""
    directory = _run_dir(run_id, runs_root)
    if name not in RERUNNABLE:
        raise StageRerunError(f"stage {name!r} is not rerunnable offline; choices: {RERUNNABLE}")
    if name == "segment":
        return _rerun_segment(directory)
    if name == "resolve":
        return _rerun_resolve(directory)
    if name == "verify":
        return _rerun_verify(directory)
    if name == "render":
        return _rerun_render(directory)
    return _rerun_review(directory)


def _write_rerun(path: Path, text: str) -> int:
    target = path.with_name(path.name + ".rerun")
    target.write_text(text, encoding="utf-8")
    print(f"wrote {target}")
    return 0


def _rerun_segment(directory: Path) -> int:
    from intake.capture import read_staging
    from intake.segment import paragraphs_json, segment_content

    for staging_file in sorted(directory.glob("staging-*.txt")):
        staging_dir = Path(staging_file.read_text(encoding="utf-8").strip())
        bundle = read_staging(staging_dir)
        paragraphs = segment_content(bundle["content"])
        _write_rerun(
            directory / f"paragraphs-{_local_id_of(staging_file)}.json",
            paragraphs_json(paragraphs),
        )
    return 0


def _local_id_of(staging_file: Path) -> str:
    return staging_file.stem.removeprefix("staging-")


def _rerun_resolve(directory: Path) -> int:
    from intake.resolve import resolve_identity

    identity = json.loads((directory / "identity.json").read_text(encoding="utf-8"))
    rerun = resolve_identity(
        company=identity.get("company_hint"),
        system_name=identity.get("system_name_hint"),
    )
    return _write_rerun(
        directory / "identity.json", json.dumps(rerun, indent=2, ensure_ascii=False) + "\n"
    )


def _rerun_verify(directory: Path) -> int:
    from intake.segment import load_paragraphs_file
    from intake.verify_quotes import verify_claims

    record = _load_extraction(directory)
    paragraphs: dict[str, list[Any]] = {}
    for paragraphs_file in sorted(directory.glob("paragraphs-s*.json")):
        local_id = paragraphs_file.stem.removeprefix("paragraphs-")
        paragraphs[local_id] = load_paragraphs_file(
            paragraphs_file
            if not paragraphs_file.with_name(paragraphs_file.name + ".rerun").is_file()
            else paragraphs_file.with_name(paragraphs_file.name + ".rerun")
        )
    verified = verify_claims(record, paragraphs)
    payload = yaml.safe_dump(
        json.loads(verified.model_dump_json()), sort_keys=False, allow_unicode=True
    )
    return _write_rerun(directory / "extraction-verified.yaml", payload)


def _rerun_render(directory: Path) -> int:
    import datetime as dt

    from intake.crosscheck import load_existing, number_conflicts
    from intake.render import render_extraction

    record = _load_extraction(directory)
    # The rerun must reproduce the run's draft: the review date comes from the
    # draft itself, and an update merges onto the record it named.
    reviewed_at = dt.date.today().isoformat()
    draft = directory / "draft.yaml"
    if draft.is_file():
        parsed = yaml.safe_load(draft.read_text(encoding="utf-8")) or {}
        if parsed.get("last_reviewed_at"):
            reviewed_at = str(parsed["last_reviewed_at"])
        # The run promoted its captures after this extraction was saved; the
        # draft carries the manifest paths, so stamp them back on before
        # re-rendering or the rerun would drop the capture blocks.
        promoted = [
            source.get("capture", {}).get("manifest_path")
            for source in parsed.get("sources", [])[-len(record.sources) :]
        ]
        if len(promoted) == len(record.sources) and all(promoted):
            record = record.model_copy(
                update={
                    "sources": [
                        source.model_copy(update={"capture_manifest_path": path})
                        for source, path in zip(record.sources, promoted)
                    ]
                }
            )
    existing = None
    manifest_path = directory / "run.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        record_id = manifest.get("record_id") or (manifest.get("queue_entry") or {}).get(
            "record_id"
        )
        existing = load_existing(str(record_id)) if record_id else None
    contradictions = number_conflicts(existing, record) if existing is not None else None
    result = render_extraction(
        record, reviewed_at=reviewed_at, existing=existing, contradictions=contradictions
    )
    return _write_rerun(directory / "draft.yaml", result.record_yaml)


def _rerun_review(directory: Path) -> int:
    manifest_path = directory / "run.json"
    if not manifest_path.is_file():
        raise StageRerunError(f"no run manifest under {directory}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    sheet = directory / "review.md"
    if not sheet.is_file():
        raise StageRerunError(f"no review sheet under {directory}")
    print(sheet.read_text(encoding="utf-8"), end="")
    print(f"model strings: {json.dumps(manifest.get('model_strings', {}), indent=2)}")
    return 0
