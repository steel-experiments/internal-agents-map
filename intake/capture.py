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
    pdf: bool = False,
    download: Any = None,
) -> StagedCapture:
    """Scrape one URL into a staging bundle keyed by the canonical URL hash.

    With ``pdf`` — the plan's opt-in for when layout or visual evidence
    matters — the page's PDF is fetched through the archiver's own
    downloader and saved beside the Markdown as ``page.pdf``.
    """
    archiver = load_archiver()
    archiver._require_https_url(url, "Source URL")
    page = (adapter or SteelSdkAdapter()).scrape(url, pdf=pdf)
    canonical = page.canonical_url or page.final_url
    key = staging_key(canonical)
    directory = staging_root / key
    timestamp = archiver._format_utc_timestamp(captured_at or datetime.now(timezone.utc))
    content = _staging_header(f"staging-{key}", url, page, timestamp) + page.markdown + "\n"
    pdf_bytes: bytes | None = None
    if pdf and page.pdf_url:
        fetch = download or archiver.download_pdf
        try:
            pdf_bytes = fetch(page.pdf_url)
        except Exception as error:
            raise CaptureStageError(f"could not download the page PDF: {error}") from error
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
    if pdf_bytes is not None:
        staging_facts["pdf_sha256"] = f"sha256:{hashlib.sha256(pdf_bytes).hexdigest()}"
    try:
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "content.md").write_text(content, encoding="utf-8")
        (directory / "page.json").write_text(
            json.dumps(page_metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (directory / "staging.json").write_text(
            json.dumps(staging_facts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        if pdf_bytes is not None:
            (directory / "page.pdf").write_bytes(pdf_bytes)
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
    pdf_path = staging_dir / "page.pdf"
    pdf_data = pdf_path.read_bytes() if pdf_path.is_file() else None
    try:
        result = archiver.write_capture_bundle(
            source_id,
            facts["url"],
            steel_result,
            tool_version=str(tool_version),
            captured_at=datetime.fromisoformat(facts["captured_at"].replace("Z", "+00:00")),
            repo_root=repo_root,
            tool_name=str(tool.get("name") or "steel"),
            pdf_data=pdf_data,
        )
    except archiver.ArchiveError as error:
        raise CaptureStageError(str(error)) from error
    return result.manifest_path


def promote_staging(
    staging_dir: Path,
    source_id: str,
    *,
    repo_root: Path = ROOT,
) -> str:
    """Promote, or accept an identical bundle an earlier run promoted.

    A rerun over the same queue meets its own bundle. The append-only rule
    forbids rewriting it, and identical content means the artifact is already
    correct, so the run reuses it. Different content is a real conflict and
    stops the run; a person decides.
    """

    def body_of(content: str) -> str:
        return "\n".join(content.splitlines()[HEADER_LINES:])

    manifest = repo_root / "archive" / "sources" / source_id / "metadata.json"
    if not manifest.is_file():
        return promote(staging_dir, source_id, repo_root=repo_root)
    staged_body = body_of(read_staging(staging_dir)["content"])
    promoted_body = body_of((manifest.parent / "content.md").read_text(encoding="utf-8"))
    if (
        hashlib.sha256(staged_body.encode("utf-8")).hexdigest()
        != hashlib.sha256(promoted_body.encode("utf-8")).hexdigest()
    ):
        raise CaptureStageError(
            f"archive/sources/{source_id} already holds different content; "
            "the append-only rule forbids overwriting it"
        )
    return f"archive/sources/{source_id}/metadata.json"
