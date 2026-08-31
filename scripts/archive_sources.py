"""Capture and verify append-only source snapshots with the Steel CLI."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO, NoReturn, TextIO

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required. Install project dependencies with 'uv sync'.")


ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOT / "data" / "agents"
ARCHIVE_ROOT = ROOT / "archive" / "sources"
MAX_PDF_BYTES = 10 * 1024 * 1024
MAX_WAYBACK_RESPONSE_BYTES = 1024 * 1024
MIN_MARKDOWN_CHARS = 80
DEFAULT_DELAY_MS = 1000
USER_AGENT = "steel-internal-agents-map-source-archiver/1.0"
WAYBACK_AVAILABILITY_URL = "https://archive.org/wayback/available"
WAYBACK_SAVE_URL = "https://web.archive.org/save/"
WAYBACK_STATUS_URL = "https://web.archive.org/save/status/"

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
UTC_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
WAYBACK_PATH_RE = re.compile(r"^/web/\d{6,14}(?:[a-z_]+)?/")
INTERSTITIAL_TITLES = (
    "access denied",
    "attention required",
    "captcha",
    "checking your browser",
    "cloudflare ray id",
    "forbidden",
    "internal server error",
    "just a moment",
    "log in or sign up",
    "login or sign up",
    "page not found",
    "request blocked",
    "security check",
    "service unavailable",
    "site unavailable",
    "temporarily unavailable",
    "verify you are human",
)
INTERSTITIAL_BODY_MARKERS = (
    "sorry, the page you're looking for cannot be found",
    "sorry, the page you are looking for cannot be found",
    "the page you're looking for doesn't exist",
    "the page you are looking for doesn't exist",
    "we couldn't find that page",
    "please sign in to continue",
    "sign in to view this content",
)

REQUIRED_MANIFEST_KEYS = {
    "schema_version",
    "source_id",
    "original_url",
    "final_url",
    "captured_at",
    "http_status",
    "tool",
    "artifacts",
}
OPTIONAL_MANIFEST_KEYS = {"external_archive_url"}
ARTIFACT_KEYS = {"path", "sha256", "bytes"}


class ArchiveError(RuntimeError):
    """A safe, user-facing archival error that contains no credentials."""


@dataclass(frozen=True)
class SteelResult:
    markdown: str
    final_url: str
    title: str
    http_status: int
    pdf_url: str | None = None


@dataclass(frozen=True)
class CaptureResult:
    source_id: str
    manifest_path: str
    archived_url: str | None

    def yaml_snippet(self) -> str:
        """Return the exact source fields a contributor should paste into YAML."""
        lines: list[str] = []
        if self.archived_url:
            lines.append(f"archived_url: {json.dumps(self.archived_url)}")
        lines.extend(
            [
                "capture:",
                f"  manifest_path: {json.dumps(self.manifest_path)}",
            ]
        )
        return "\n".join(lines) + "\n"


def fail(message: str) -> NoReturn:
    raise ArchiveError(message)


def _mapping(value: Any, description: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        fail(f"{description} must be an object.")
    return value


def _exact_keys(
    value: Mapping[str, Any],
    required: set[str],
    description: str,
    optional: set[str] | None = None,
) -> None:
    allowed = required | (optional or set())
    missing = required - set(value)
    unexpected = set(value) - allowed
    if missing:
        fail(f"{description} is missing field(s): {', '.join(sorted(missing))}.")
    if unexpected:
        fail(f"{description} has unexpected field(s): {', '.join(sorted(unexpected))}.")


def _require_https_url(value: Any, description: str) -> str:
    if not isinstance(value, str) or not value:
        fail(f"{description} must be a non-empty HTTPS URL.")
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme != "https" or not parsed.netloc:
        fail(f"{description} must be a non-empty HTTPS URL.")
    return value


def _format_utc_timestamp(value: datetime) -> str:
    if value.tzinfo is None:
        fail("Capture time must be timezone-aware.")
    value = value.astimezone(timezone.utc).replace(microsecond=0)
    return value.isoformat().replace("+00:00", "Z")


def _validate_utc_timestamp(value: Any) -> str:
    if not isinstance(value, str) or not UTC_TIMESTAMP_RE.fullmatch(value):
        fail("Manifest captured_at must be an RFC 3339 UTC timestamp ending in Z.")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        fail("Manifest captured_at must be a valid RFC 3339 UTC timestamp.")
    if parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        fail("Manifest captured_at must use UTC.")
    return value


def _sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _safe_relative_path(value: Any, expected: str, description: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        fail(f"{description} must be a POSIX repository-relative path.")
    candidate = PurePosixPath(value)
    if candidate.is_absolute() or ".." in candidate.parts or "." in candidate.parts:
        fail(f"{description} must be a POSIX repository-relative path without traversal.")
    if value != candidate.as_posix() or value != expected:
        fail(f"{description} must be {expected!r}.")
    return value


def _read_json_file(path: Path, description: str) -> Mapping[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        fail(f"Unable to read {description}.")
    try:
        return _mapping(json.loads(raw), description)
    except json.JSONDecodeError:
        fail(f"{description} is not valid JSON.")


def _artifact_file(
    artifact: Mapping[str, Any],
    *,
    kind: str,
    source_id: str,
    repo_root: Path,
    bundle_dir: Path | None,
) -> tuple[Path, bytes]:
    _exact_keys(artifact, ARTIFACT_KEYS, f"Manifest {kind} artifact")
    filename = "content.md" if kind == "markdown" else "page.pdf"
    relative = f"archive/sources/{source_id}/{filename}"
    _safe_relative_path(artifact["path"], relative, f"Manifest {kind} artifact path")

    path = bundle_dir / filename if bundle_dir is not None else repo_root / relative
    archive_root = (repo_root / "archive" / "sources").resolve()
    try:
        resolved = path.resolve(strict=True)
    except OSError:
        fail(f"Manifest {kind} artifact does not exist at {relative!r}.")
    if not resolved.is_relative_to(archive_root) or not resolved.is_file():
        fail(f"Manifest {kind} artifact escapes archive/sources/ or is not a file.")
    try:
        data = resolved.read_bytes()
    except OSError:
        fail(f"Unable to read manifest {kind} artifact.")

    byte_count = artifact["bytes"]
    if isinstance(byte_count, bool) or not isinstance(byte_count, int) or byte_count < 0:
        fail(f"Manifest {kind} artifact bytes must be a non-negative integer.")
    if byte_count != len(data):
        fail(f"Manifest {kind} artifact byte count does not match the file.")
    digest = artifact["sha256"]
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        fail(f"Manifest {kind} artifact sha256 must use lowercase sha256:<hex> form.")
    if digest != _sha256(data):
        fail(f"Manifest {kind} artifact SHA-256 does not match the file.")
    return resolved, data


def validate_bundle(
    manifest_path: Path,
    source_id: str,
    original_url: str,
    *,
    repo_root: Path = ROOT,
    bundle_dir: Path | None = None,
    archived_url: str | None = None,
) -> Mapping[str, Any]:
    """Validate a complete capture bundle without making any network calls."""
    if not ID_RE.fullmatch(source_id):
        fail(f"Invalid source ID {source_id!r}.")
    _require_https_url(original_url, "Source original URL")
    expected_manifest = f"archive/sources/{source_id}/metadata.json"
    if bundle_dir is None:
        try:
            relative_manifest = manifest_path.relative_to(repo_root).as_posix()
        except ValueError:
            fail("Capture manifest must be inside the repository.")
        _safe_relative_path(relative_manifest, expected_manifest, "Capture manifest path")
        archive_root = (repo_root / "archive" / "sources").resolve()
        try:
            resolved_manifest = manifest_path.resolve(strict=True)
        except OSError:
            fail(f"Capture manifest does not exist at {expected_manifest!r}.")
        if not resolved_manifest.is_relative_to(archive_root) or not resolved_manifest.is_file():
            fail("Capture manifest escapes archive/sources/ or is not a file.")
        manifest_file = resolved_manifest
    else:
        manifest_file = bundle_dir / "metadata.json"

    manifest = _read_json_file(manifest_file, "capture manifest")
    _exact_keys(
        manifest,
        REQUIRED_MANIFEST_KEYS,
        "Capture manifest",
        OPTIONAL_MANIFEST_KEYS,
    )
    if manifest["schema_version"] != 1 or isinstance(manifest["schema_version"], bool):
        fail("Capture manifest schema_version must be 1.")
    if manifest["source_id"] != source_id:
        fail("Capture manifest source_id does not match the source.")
    if manifest["original_url"] != original_url:
        fail("Capture manifest original_url does not match the source URL.")
    _require_https_url(manifest["final_url"], "Capture manifest final_url")
    _validate_utc_timestamp(manifest["captured_at"])
    status = manifest["http_status"]
    if isinstance(status, bool) or not isinstance(status, int) or not 200 <= status < 300:
        fail("Capture manifest http_status must be a 2xx integer.")

    tool = _mapping(manifest["tool"], "Capture manifest tool")
    _exact_keys(tool, {"name", "version"}, "Capture manifest tool")
    if tool["name"] != "steel":
        fail("Capture manifest tool name must be 'steel'.")
    if not isinstance(tool["version"], str) or not tool["version"].strip():
        fail("Capture manifest tool version must be non-empty.")

    artifacts = _mapping(manifest["artifacts"], "Capture manifest artifacts")
    _exact_keys(artifacts, {"markdown"}, "Capture manifest artifacts", {"pdf"})
    _, markdown = _artifact_file(
        _mapping(artifacts["markdown"], "Manifest markdown artifact"),
        kind="markdown",
        source_id=source_id,
        repo_root=repo_root,
        bundle_dir=bundle_dir,
    )
    if not markdown:
        fail("Manifest Markdown artifact must not be empty.")

    if "pdf" in artifacts:
        _, pdf = _artifact_file(
            _mapping(artifacts["pdf"], "Manifest PDF artifact"),
            kind="pdf",
            source_id=source_id,
            repo_root=repo_root,
            bundle_dir=bundle_dir,
        )
        if len(pdf) > MAX_PDF_BYTES:
            fail("Manifest PDF artifact exceeds the 10 MiB limit.")
        if not pdf.startswith(b"%PDF-"):
            fail("Manifest PDF artifact does not begin with %PDF-.")

    if "external_archive_url" in manifest:
        external_url = _require_https_url(
            manifest["external_archive_url"], "Capture manifest external_archive_url"
        )
        if external_url != archived_url:
            fail("Capture manifest external_archive_url does not match source archived_url.")
    return manifest


def load_sources(agents_dir: Path = AGENTS_DIR) -> dict[str, Mapping[str, Any]]:
    """Load all source records and reject missing or duplicate IDs."""
    sources: dict[str, Mapping[str, Any]] = {}
    for path in sorted(agents_dir.glob("*.yaml")):
        try:
            record = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as error:
            raise ArchiveError(f"Unable to load {path.name}: {error.__class__.__name__}.") from None
        if not isinstance(record, Mapping):
            fail(f"{path.name}: top level must be a map.")
        source_items = record.get("sources")
        if not isinstance(source_items, list):
            fail(f"{path.name}: sources must be a list.")
        for index, source_value in enumerate(source_items):
            source = _mapping(source_value, f"{path.name}: source {index + 1}")
            source_id = source.get("id")
            if not isinstance(source_id, str) or not ID_RE.fullmatch(source_id):
                fail(f"{path.name}: source {index + 1} has a missing or invalid ID.")
            if source_id in sources:
                fail(f"Duplicate source ID {source_id!r}.")
            _require_https_url(source.get("url"), f"{path.name}: source {source_id!r} URL")
            sources[source_id] = source
    return sources


def get_source(source_id: str, sources: Mapping[str, Mapping[str, Any]]) -> Mapping[str, Any]:
    try:
        return sources[source_id]
    except KeyError:
        fail(f"Unknown source ID {source_id!r}.")


def _normalize_newlines(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n")


def _single_line(value: str) -> str:
    return " ".join(_normalize_newlines(value).splitlines()).strip()


def _has_noarchive(value: Any, key_hint: str = "") -> bool:
    if isinstance(value, Mapping):
        return any(_has_noarchive(item, str(key)) for key, item in value.items())
    if isinstance(value, list):
        return any(_has_noarchive(item, key_hint) for item in value)
    if key_hint.casefold() == "noarchive" and value is True:
        return True
    if not isinstance(value, str):
        return False
    lowered = value.lower()
    if "robot" in key_hint.lower() and re.search(r"(?:^|[\s,;])noarchive(?:$|[\s,;])", lowered):
        return True
    return bool(
        re.search(r"<meta\b[^>]*(?:robots|googlebot)[^>]*noarchive[^>]*>", lowered)
        or re.search(r"x-robots-tag\s*:\s*[^\n]*\bnoarchive\b", lowered)
    )


def _validate_scraped_page(data: Mapping[str, Any], include_pdf: bool) -> SteelResult:
    content = _mapping(data.get("content"), "Steel data.content")
    metadata = _mapping(data.get("metadata"), "Steel data.metadata")
    status = metadata.get("statusCode")
    if isinstance(status, bool) or not isinstance(status, int):
        fail("Steel metadata.statusCode must be an integer.")
    if not 200 <= status < 300:
        fail(f"Steel returned non-success HTTP status {status}.")

    markdown = content.get("markdown")
    if not isinstance(markdown, str):
        fail("Steel response is missing content.markdown.")
    normalized_markdown = _normalize_newlines(markdown).strip()
    if len(normalized_markdown) < MIN_MARKDOWN_CHARS:
        fail("Steel returned missing or suspiciously short Markdown.")

    title = metadata.get("title")
    if not isinstance(title, str) or not _single_line(title):
        fail("Steel response is missing metadata.title.")
    clean_title = _single_line(title)
    lowered_title = clean_title.casefold()
    if any(marker in lowered_title for marker in INTERSTITIAL_TITLES) or re.fullmatch(
        r"(?:error\s*)?(?:4\d\d|5\d\d)(?:\s*error)?", lowered_title
    ):
        fail("Steel returned an obvious error or interstitial page title.")
    lowered_markdown = normalized_markdown.casefold()
    if any(marker in lowered_markdown for marker in INTERSTITIAL_BODY_MARKERS):
        fail("Steel returned an obvious error or interstitial page body.")
    if _has_noarchive({"content": content, "metadata": metadata}):
        fail("Source explicitly declares noarchive; capture was not saved.")

    final_url = _require_https_url(metadata.get("urlSource"), "Steel metadata.urlSource")
    pdf_url: str | None = None
    if include_pdf:
        pdf = _mapping(data.get("pdf"), "Steel data.pdf")
        pdf_url = _require_https_url(pdf.get("url"), "Steel data.pdf.url")
    return SteelResult(normalized_markdown, final_url, clean_title, status, pdf_url)


def parse_steel_response(stdout: str, *, include_pdf: bool = False) -> SteelResult:
    """Parse the documented Steel JSON envelope and validate the captured page."""
    if not isinstance(stdout, str) or not stdout.strip():
        fail("Steel returned an empty response.")
    try:
        envelope = _mapping(json.loads(stdout), "Steel response")
    except json.JSONDecodeError:
        fail("Steel returned malformed JSON.")
    if envelope.get("success") is not True:
        fail("Steel reported that the scrape failed.")
    data = _mapping(envelope.get("data"), "Steel response.data")
    return _validate_scraped_page(data, include_pdf)


def steel_version(
    *,
    runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    executable: str = "steel",
) -> str:
    run = runner or subprocess.run
    try:
        result = run(
            [executable, "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        fail("Unable to execute the Steel CLI.")
    if result.returncode != 0:
        fail(f"Steel version command exited with status {result.returncode}.")
    match = re.fullmatch(r"steel\s+(\S+)\s*", result.stdout)
    if not match:
        fail("Unable to parse the Steel CLI version.")
    return match.group(1)


def scrape_with_steel(
    url: str,
    *,
    pdf: bool = False,
    delay_ms: int = DEFAULT_DELAY_MS,
    runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    executable: str = "steel",
) -> SteelResult:
    """Run Steel with an argument array and parse its structured response."""
    _require_https_url(url, "Source URL")
    if isinstance(delay_ms, bool) or not isinstance(delay_ms, int) or delay_ms < 0:
        fail("Delay must be a non-negative integer number of milliseconds.")
    command = [executable, "--json", "scrape", url, "--format", "markdown"]
    if delay_ms:
        command.extend(["--delay", str(delay_ms)])
    if pdf:
        command.append("--pdf")
    run = runner or subprocess.run
    try:
        result = run(command, capture_output=True, text=True, check=False)
    except OSError:
        fail("Unable to execute the Steel CLI.")
    if result.returncode != 0:
        fail(f"Steel scrape exited with status {result.returncode}.")
    return parse_steel_response(result.stdout, include_pdf=pdf)


def _response_status(response: Any, description: str) -> None:
    status = getattr(response, "status", None)
    if isinstance(status, int) and not 200 <= status < 300:
        fail(f"{description} returned HTTP status {status}.")


def _content_length(response: Any, description: str) -> int | None:
    headers = getattr(response, "headers", None)
    raw = headers.get("Content-Length") if headers is not None else None
    if raw is None:
        return None
    try:
        length = int(raw)
    except (TypeError, ValueError):
        fail(f"{description} returned an invalid Content-Length header.")
    if length < 0:
        fail(f"{description} returned an invalid Content-Length header.")
    return length


def _read_response_bytes(response: BinaryIO, limit: int, description: str) -> bytes:
    declared = _content_length(response, description)
    if declared is not None and declared > limit:
        fail(f"{description} exceeds the allowed size.")
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(min(64 * 1024, limit + 1 - total))
        if not chunk:
            break
        if not isinstance(chunk, bytes):
            fail(f"{description} returned non-binary content.")
        chunks.append(chunk)
        total += len(chunk)
        if total > limit:
            fail(f"{description} exceeds the allowed size.")
    if declared is not None and total != declared:
        fail(f"{description} download was truncated.")
    return b"".join(chunks)


def _open(request: urllib.request.Request, opener: Callable[..., Any] | None, timeout: int) -> Any:
    open_url = opener or urllib.request.urlopen
    try:
        return open_url(request, timeout=timeout)
    except (urllib.error.URLError, TimeoutError, OSError):
        fail("Network request failed.")


def download_pdf(url: str, *, opener: Callable[..., Any] | None = None) -> bytes:
    """Download a Steel-hosted PDF immediately and enforce the permanent-copy limits."""
    _require_https_url(url, "Steel PDF URL")
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/pdf", "User-Agent": USER_AGENT},
        method="GET",
    )
    response = _open(request, opener, 30)
    with response:
        _response_status(response, "Steel PDF download")
        data = _read_response_bytes(response, MAX_PDF_BYTES, "Steel PDF")
    if not data.startswith(b"%PDF-"):
        fail("Steel PDF does not begin with %PDF-.")
    return data


def _read_json_response(response: Any, description: str) -> Mapping[str, Any]:
    _response_status(response, description)
    raw = _read_response_bytes(response, MAX_WAYBACK_RESPONSE_BYTES, description)
    try:
        return _mapping(json.loads(raw), description)
    except (UnicodeDecodeError, json.JSONDecodeError):
        fail(f"{description} returned malformed JSON.")


def _normalize_wayback_url(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    if value.startswith("http://web.archive.org/"):
        value = "https://" + value.removeprefix("http://")
    try:
        parsed = urllib.parse.urlsplit(value)
    except ValueError:
        return None
    if (
        parsed.scheme != "https"
        or parsed.netloc != "web.archive.org"
        or not WAYBACK_PATH_RE.match(parsed.path)
    ):
        return None
    return value


def query_wayback(url: str, *, opener: Callable[..., Any] | None = None) -> str | None:
    """Return an immutable existing Wayback capture, if one is available."""
    query = urllib.parse.urlencode({"url": url})
    request = urllib.request.Request(
        f"{WAYBACK_AVAILABILITY_URL}?{query}",
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
        method="GET",
    )
    response = _open(request, opener, 20)
    with response:
        payload = _read_json_response(response, "Wayback availability query")
    snapshots = payload.get("archived_snapshots")
    if not isinstance(snapshots, Mapping):
        return None
    closest = snapshots.get("closest")
    if not isinstance(closest, Mapping) or closest.get("available") is not True:
        return None
    if str(closest.get("status")) != "200":
        return None
    return _normalize_wayback_url(closest.get("url"))


def _wayback_url_from_payload(payload: Mapping[str, Any], original_url: str) -> str | None:
    for key in ("archive_url", "wayback_url", "url"):
        result = _normalize_wayback_url(payload.get(key))
        if result:
            return result
    timestamp = payload.get("timestamp")
    if isinstance(timestamp, str):
        digits = "".join(character for character in timestamp if character.isdigit())
        if len(digits) >= 14:
            return f"https://web.archive.org/web/{digits[:14]}/{original_url}"
    return None


def save_to_wayback(
    url: str,
    access_key: str,
    secret_key: str,
    *,
    opener: Callable[..., Any] | None = None,
    sleep: Callable[[float], None] = time.sleep,
    max_polls: int = 10,
) -> str:
    """Submit a public URL to Save Page Now and poll for its immutable replay URL."""
    if not access_key or not secret_key:
        fail("Wayback credentials are incomplete.")
    encoded_url = urllib.parse.quote(url, safe=":/")
    request = urllib.request.Request(
        WAYBACK_SAVE_URL + encoded_url,
        data=b"",
        headers={
            "Accept": "application/json",
            "Authorization": f"LOW {access_key}:{secret_key}",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    response = _open(request, opener, 30)
    with response:
        payload = _read_json_response(response, "Wayback save request")
    direct = _wayback_url_from_payload(payload, url)
    if direct and str(payload.get("status", "success")).casefold() in {
        "success",
        "done",
        "completed",
    }:
        return direct
    job_id = payload.get("job_id")
    if not isinstance(job_id, str) or not job_id:
        fail("Wayback save request did not return a job ID.")

    for poll_number in range(max_polls):
        if poll_number:
            sleep(2)
        status_request = urllib.request.Request(
            WAYBACK_STATUS_URL + urllib.parse.quote(job_id, safe=""),
            headers={
                "Accept": "application/json",
                "Authorization": f"LOW {access_key}:{secret_key}",
                "User-Agent": USER_AGENT,
            },
            method="GET",
        )
        status_response = _open(status_request, opener, 30)
        with status_response:
            status_payload = _read_json_response(status_response, "Wayback save status")
        status = str(status_payload.get("status", "")).casefold()
        if status in {"success", "done", "completed"}:
            archived_url = _wayback_url_from_payload(status_payload, url)
            if archived_url:
                return archived_url
            fail("Wayback completed without an immutable replay URL.")
        if status in {"error", "failed", "failure"}:
            fail("Wayback reported that the save failed.")
    fail("Wayback save did not complete before the polling limit.")


def _wayback_credentials(environ: Mapping[str, str]) -> tuple[str, str] | None:
    for access_name, secret_name in (
        ("IA_ACCESS_KEY_ID", "IA_SECRET_ACCESS_KEY"),
        ("WAYBACK_ACCESS_KEY", "WAYBACK_SECRET_KEY"),
    ):
        access = environ.get(access_name, "")
        secret = environ.get(secret_name, "")
        if access or secret:
            return (access, secret) if access and secret else None
    return None


def preserve_with_wayback(
    url: str,
    *,
    opener: Callable[..., Any] | None = None,
    sleep: Callable[[float], None] = time.sleep,
    environ: Mapping[str, str] | None = None,
    warning_stream: TextIO = sys.stderr,
) -> str | None:
    """Best-effort Wayback save, falling back to a public availability query."""
    environment = os.environ if environ is None else environ
    credentials = _wayback_credentials(environment)
    if credentials:
        try:
            return save_to_wayback(
                url,
                credentials[0],
                credentials[1],
                opener=opener,
                sleep=sleep,
            )
        except ArchiveError:
            print(
                "warning: Wayback save failed; checking for an existing capture.",
                file=warning_stream,
            )
    else:
        print(
            "warning: Wayback credentials unavailable or incomplete; "
            "checking for an existing capture.",
            file=warning_stream,
        )
    try:
        return query_wayback(url, opener=opener)
    except ArchiveError:
        print(
            "warning: Wayback availability query failed; continuing locally.", file=warning_stream
        )
        return None


def build_markdown_snapshot(
    result: SteelResult,
    *,
    source_id: str,
    original_url: str,
    captured_at: str,
) -> bytes:
    """Add provenance and normalize the exact bytes committed as content.md."""
    title = _single_line(result.title)
    header = (
        "> Archived source snapshot  \n"
        f"> Source ID: `{source_id}`  \n"
        f"> Original URL: <{original_url}>  \n"
        f"> Final URL: <{result.final_url}>  \n"
        f"> Title: {title}  \n"
        f"> Captured at: `{captured_at}`\n\n"
        "---\n\n"
    )
    body = _normalize_newlines(result.markdown).strip()
    return (header + body + "\n").encode("utf-8")


def _artifact_metadata(path: str, data: bytes) -> dict[str, Any]:
    return {"path": path, "sha256": _sha256(data), "bytes": len(data)}


def _target_exists(path: Path) -> bool:
    return os.path.lexists(path)


def capture_source(
    source: Mapping[str, Any],
    *,
    pdf: bool = False,
    delay_ms: int = DEFAULT_DELAY_MS,
    save_wayback: bool = False,
    repo_root: Path = ROOT,
    runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    opener: Callable[..., Any] | None = None,
    sleep: Callable[[float], None] = time.sleep,
    environ: Mapping[str, str] | None = None,
    captured_at: datetime | None = None,
    steel_version_value: str | None = None,
    warning_stream: TextIO = sys.stderr,
) -> CaptureResult:
    """Capture one source into an atomic, append-only repository bundle."""
    source_id = source.get("id")
    if not isinstance(source_id, str) or not ID_RE.fullmatch(source_id):
        fail("Source has a missing or invalid ID.")
    original_url = _require_https_url(source.get("url"), f"Source {source_id!r} URL")
    archive_root = repo_root / "archive" / "sources"
    target = archive_root / source_id
    if _target_exists(target):
        fail(f"Capture bundle already exists for {source_id!r}; archives are append-only.")

    version = steel_version_value or steel_version(runner=runner)
    if not isinstance(version, str) or not version.strip():
        fail("Steel version must be non-empty.")
    steel_result = scrape_with_steel(
        original_url,
        pdf=pdf,
        delay_ms=delay_ms,
        runner=runner,
    )
    pdf_data = download_pdf(steel_result.pdf_url, opener=opener) if steel_result.pdf_url else None
    archived_url = (
        preserve_with_wayback(
            original_url,
            opener=opener,
            sleep=sleep,
            environ=environ,
            warning_stream=warning_stream,
        )
        if save_wayback
        else None
    )

    timestamp = _format_utc_timestamp(captured_at or datetime.now(timezone.utc))
    markdown_data = build_markdown_snapshot(
        steel_result,
        source_id=source_id,
        original_url=original_url,
        captured_at=timestamp,
    )
    manifest_path = f"archive/sources/{source_id}/metadata.json"
    artifacts: dict[str, Any] = {
        "markdown": _artifact_metadata(f"archive/sources/{source_id}/content.md", markdown_data)
    }
    if pdf_data is not None:
        artifacts["pdf"] = _artifact_metadata(f"archive/sources/{source_id}/page.pdf", pdf_data)
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "source_id": source_id,
        "original_url": original_url,
        "final_url": steel_result.final_url,
        "captured_at": timestamp,
        "http_status": steel_result.http_status,
        "tool": {"name": "steel", "version": version.strip()},
        "artifacts": artifacts,
    }
    if archived_url:
        manifest["external_archive_url"] = archived_url

    try:
        archive_root.mkdir(parents=True, exist_ok=True)
        temporary = Path(tempfile.mkdtemp(prefix=f".{source_id}.", dir=archive_root))
    except OSError:
        fail(f"Unable to create a temporary capture bundle for {source_id!r}.")
    try:
        (temporary / "content.md").write_bytes(markdown_data)
        if pdf_data is not None:
            (temporary / "page.pdf").write_bytes(pdf_data)
        (temporary / "metadata.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        validate_bundle(
            temporary / "metadata.json",
            source_id,
            original_url,
            repo_root=repo_root,
            bundle_dir=temporary,
            archived_url=archived_url,
        )
        if _target_exists(target):
            fail(f"Capture bundle already exists for {source_id!r}; archives are append-only.")
        temporary.rename(target)
    except ArchiveError:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    except OSError:
        shutil.rmtree(temporary, ignore_errors=True)
        fail(f"Unable to write capture bundle for {source_id!r}.")
    return CaptureResult(source_id, manifest_path, archived_url)


def check_declared_captures(
    sources: Mapping[str, Mapping[str, Any]], *, repo_root: Path = ROOT
) -> list[str]:
    """Validate every YAML-declared capture and return all safe error messages."""
    errors: list[str] = []
    for source_id in sorted(sources):
        source = sources[source_id]
        if "capture" not in source:
            continue
        try:
            capture = _mapping(source["capture"], f"Source {source_id!r} capture")
            _exact_keys(capture, {"manifest_path"}, f"Source {source_id!r} capture")
            expected = f"archive/sources/{source_id}/metadata.json"
            relative = _safe_relative_path(
                capture["manifest_path"], expected, f"Source {source_id!r} manifest_path"
            )
            validate_bundle(
                repo_root / relative,
                source_id,
                str(source["url"]),
                repo_root=repo_root,
                archived_url=source.get("archived_url"),
            )
        except (ArchiveError, OSError) as error:
            errors.append(f"{source_id}: {error}")
    return errors


def _delay_value(value: str) -> int:
    try:
        delay = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("delay must be a non-negative integer") from error
    if delay < 0:
        raise argparse.ArgumentTypeError("delay must be a non-negative integer")
    return delay


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--source-id", metavar="ID", help="capture one source ID")
    mode.add_argument("--all", action="store_true", help="capture every uncaptured source")
    mode.add_argument("--check", action="store_true", help="validate declared captures offline")
    parser.add_argument("--continue-on-error", action="store_true")
    parser.add_argument("--delay", type=_delay_value, default=DEFAULT_DELAY_MS, metavar="MS")
    parser.add_argument("--pdf", action="store_true", help="also preserve a PDF")
    parser.add_argument("--save-wayback", action="store_true", help="attempt a Wayback capture")
    return parser


def _capture_summary(result: CaptureResult) -> dict[str, Any]:
    return {
        "source_id": result.source_id,
        "manifest_path": result.manifest_path,
        "archived_url": result.archived_url,
        "yaml": result.yaml_snippet(),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.continue_on_error and not args.all:
        parser.error("--continue-on-error requires --all")
    if args.check and (args.pdf or args.save_wayback or args.delay != DEFAULT_DELAY_MS):
        parser.error("--check cannot be combined with capture options")

    try:
        sources = load_sources()
    except ArchiveError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if args.check:
        errors = check_declared_captures(sources)
        if errors:
            for error in errors:
                print(f"error: {error}", file=sys.stderr)
            return 1
        checked = sum("capture" in source for source in sources.values())
        print(f"Validated {checked} declared source capture(s).")
        return 0

    if args.source_id:
        try:
            source = get_source(args.source_id, sources)
            result = capture_source(
                source,
                pdf=args.pdf,
                delay_ms=args.delay,
                save_wayback=args.save_wayback,
            )
        except ArchiveError as error:
            print(f"error: {error}", file=sys.stderr)
            return 1
        print(result.yaml_snippet(), end="")
        return 0

    summary: dict[str, Any] = {"captured": [], "skipped": [], "failed": []}
    pending = [
        source_id
        for source_id, source in sorted(sources.items())
        if "capture" not in source and not _target_exists(ROOT / "archive" / "sources" / source_id)
    ]
    skipped = sorted(set(sources) - set(pending))
    summary["skipped"] = skipped
    try:
        version = steel_version() if pending else None
    except ArchiveError as error:
        summary["failed"].append({"source_id": None, "error": str(error)})
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 1

    for index, source_id in enumerate(pending):
        try:
            result = capture_source(
                sources[source_id],
                pdf=args.pdf,
                delay_ms=args.delay,
                save_wayback=args.save_wayback,
                steel_version_value=version,
            )
            summary["captured"].append(_capture_summary(result))
        except (ArchiveError, OSError) as error:
            summary["failed"].append({"source_id": source_id, "error": str(error)})
            if not args.continue_on_error:
                break
        if index + 1 < len(pending) and args.delay:
            time.sleep(args.delay / 1000)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 1 if summary["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
