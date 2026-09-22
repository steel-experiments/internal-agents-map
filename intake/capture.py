# ABOUTME: Staging capture and promotion for the intake pipeline (Plan 017, stage 1).
# ABOUTME: Stages under .intake/captures/; promotes through the archiver's own writer.
"""Capture a source into staging and promote it into the append-only archive.

A staging bundle lives under ``.intake/captures/<url-hash>/`` and holds the
validated Markdown snapshot (with a placeholder header of the same shape the
archive uses), the page metadata the SDK returns, and the staging facts. The
identity of a source is unknown at capture time, so promotion rebuilds the
snapshot bytes with the final source ID through the archiver's
``write_capture_bundle``; the header keeps the same line count, so paragraph
and line locators stay stable from staging to promotion.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from intake.adapters.steel import ScrapedPage, SteelSdkAdapter
from intake.catalog import load_archiver

ROOT = Path(__file__).resolve().parent.parent
STAGING_ROOT = ROOT / ".intake" / "captures"
# The snapshot header occupies exactly this many lines: six blockquote lines,
# a blank line, the rule, and the blank line after it.
HEADER_LINES = 9
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class CaptureStageError(RuntimeError):
    """A safe capture or promotion failure."""


@dataclass(frozen=True)
class StagedCapture:
    """One staged capture and its paths."""

    staging_dir: Path
    url: str
    canonical_url: str
    content_sha256: str
    captured_at: str

    @property
    def staging_path(self) -> str:
        return self.staging_dir.as_posix()


def staging_key(url: str) -> str:
    """Hash the URL into the staging directory key."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]


def _sdk_version() -> str:
    """The installed Steel SDK version, recorded in the staging facts."""
    try:
        import steel
    except ImportError as error:  # pragma: no cover - dependency is pinned
        raise CaptureStageError(
            f"the steel-sdk package is required for capture: {error}"
        ) from error
    version = getattr(steel, "__version__", None)
    if not version:
        raise CaptureStageError("the steel-sdk package does not report its version")
    return str(version)


def _staging_header(source_label: str, original_url: str, page: ScrapedPage, captured_at: str):
    archiver = load_archiver()
    single = archiver._single_line
    return (
        "> Archived source snapshot  \n"
        f"> Source ID: `{source_label}`  \n"
        f"> Original URL: <{original_url}>  \n"
        f"> Final URL: <{page.final_url}>  \n"
        f"> Title: {single(page.title)}  \n"
        f"> Captured at: `{captured_at}`\n\n"
        "---\n\n"
    )


def capture_staging(
    url: str,
    *,
    staging_root: Path = STAGING_ROOT,
    adapter: SteelSdkAdapter | None = None,
    captured_at: datetime | None = None,
    tool_version: str | None = None,
) -> StagedCapture:
    """Scrape one URL into a staging bundle keyed by the canonical URL hash."""
    archiver = load_archiver()
    archiver._require_https_url(url, "Source URL")
    page = (adapter or SteelSdkAdapter()).scrape(url)
    canonical = page.canonical_url or page.final_url
    key = staging_key(canonical)
    directory = staging_root / key
    timestamp = archiver._format_utc_timestamp(captured_at or datetime.now(timezone.utc))
    content = _staging_header(f"staging-{key}", url, page, timestamp) + page.markdown + "\n"
    page_metadata = {
        "title": page.title,
        "final_url": page.final_url,
        "http_status": page.http_status,
        "published_at": page.published_at,
        "language": page.language,
        "canonical_url": page.canonical_url,
        "description": page.description,
    }
    staging_facts = {
        "schema_version": 1,
        "url": url,
        "canonical_url": canonical,
        "captured_at": timestamp,
        "content_sha256": f"sha256:{hashlib.sha256(page.markdown.encode('utf-8')).hexdigest()}",
        "tool": {"name": "steel-python-sdk", "version": tool_version or _sdk_version()},
    }
    try:
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "content.md").write_text(content, encoding="utf-8")
        (directory / "page.json").write_text(
            json.dumps(page_metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (directory / "staging.json").write_text(
            json.dumps(staging_facts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    except OSError as error:
        raise CaptureStageError(f"could not write the staging bundle: {error}") from error
    return StagedCapture(
        staging_dir=directory,
        url=url,
        canonical_url=canonical,
        content_sha256=staging_facts["content_sha256"],
        captured_at=timestamp,
    )


def read_staging(staging_dir: Path) -> dict[str, Any]:
    """Load one staging bundle's facts, page metadata, and snapshot text."""
    try:
        facts = json.loads((staging_dir / "staging.json").read_text(encoding="utf-8"))
        page = json.loads((staging_dir / "page.json").read_text(encoding="utf-8"))
        content = (staging_dir / "content.md").read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as error:
        raise CaptureStageError(
            f"could not read the staging bundle {staging_dir}: {error}"
        ) from error
    return {"staging": facts, "page": page, "content": content}


def promote(
    staging_dir: Path,
    source_id: str,
    *,
    repo_root: Path = ROOT,
) -> str:
    """Promote one staging bundle into ``archive/sources/<source_id>/``.

    Returns the manifest path. Refuses to promote onto an existing bundle; the
    archiver's writer enforces the append-only rule and the manifest format.
    """
    archiver = load_archiver()
    if not ID_RE.fullmatch(source_id):
        raise CaptureStageError(f"source id {source_id!r} must use kebab-case")
    bundle = read_staging(staging_dir)
    facts = bundle["staging"]
    page = bundle["page"]
    lines = bundle["content"].splitlines()
    if len(lines) <= HEADER_LINES or lines[HEADER_LINES - 1] != "":
        raise CaptureStageError(
            f"{staging_dir}: the staging snapshot does not carry the expected header"
        )
    body = "\n".join(lines[HEADER_LINES:])
    steel_result = archiver.SteelResult(
        markdown=body,
        final_url=page["final_url"],
        title=page["title"],
        http_status=page["http_status"],
    )
    tool = facts.get("tool") or {}
    tool_version = tool.get("version")
    if not tool_version:
        raise CaptureStageError(f"{staging_dir}: the staging facts do not record the tool version")
    try:
        result = archiver.write_capture_bundle(
            source_id,
            facts["url"],
            steel_result,
            tool_version=str(tool_version),
            captured_at=datetime.fromisoformat(facts["captured_at"].replace("Z", "+00:00")),
            repo_root=repo_root,
            tool_name=str(tool.get("name") or "steel"),
        )
    except archiver.ArchiveError as error:
        raise CaptureStageError(str(error)) from error
    return result.manifest_path
