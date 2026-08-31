"""Check local Markdown links and catalog source URLs."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Literal
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOT / "data" / "agents"
ARCHIVE_DIR = ROOT / "archive"
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SHA256_RE = re.compile(r"^sha256:([0-9a-f]{64})$")
BLOCKED_STATUS = {401, 403, 405, 406, 429}
MISSING_STATUS = {404, 410}
HTTPStatus = Literal["healthy", "missing", "blocked", "unreachable"]
SourceStatus = Literal["healthy", "archived", "missing", "blocked", "unreachable"]
SnapshotStatus = Literal["healthy", "absent", "invalid"]


@dataclass(frozen=True)
class LinkResult:
    url: str
    status: HTTPStatus
    detail: str


@dataclass(frozen=True)
class SourceTarget:
    source_id: str
    url: str
    archived_url: str | None = None
    manifest_path: str | None = None
    configuration_error: str | None = None


@dataclass(frozen=True)
class SnapshotResult:
    status: SnapshotStatus
    detail: str
    path: Path | None = None


@dataclass(frozen=True)
class SourceResult:
    source_id: str
    url: str
    status: SourceStatus
    detail: str
    warnings: tuple[str, ...] = ()


def tracked_markdown() -> list[Path]:
    tracked = subprocess.run(
        ["git", "ls-files", "*.md"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    paths = [ROOT / relative for relative in sorted(tracked)]
    return [path for path in paths if not path.is_relative_to(ARCHIVE_DIR)]


def heading_anchors(text: str) -> set[str]:
    anchors = set(re.findall(r'<a\s+id=["\']([^"\']+)["\']', text))
    for heading in re.findall(r"^#{1,6}\s+(.+)$", text, flags=re.MULTILINE):
        slug = re.sub(r"[^a-z0-9 -]", "", heading.casefold()).strip().replace(" ", "-")
        slug = re.sub(r"-+", "-", slug)
        anchors.add(slug)
    return anchors


def local_links() -> list[str]:
    errors = []
    for path in tracked_markdown():
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            raw = target.strip("<>")
            clean, _, fragment = raw.partition("#")
            if urlsplit(clean).scheme in {"http", "https", "mailto"}:
                continue
            if not clean:
                if fragment and unquote(fragment).casefold() not in heading_anchors(text):
                    errors.append(f"{path.relative_to(ROOT)}: missing anchor {target}")
                continue
            resolved = (path.parent / clean).resolve()
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing local target {target}")
            elif fragment and resolved.suffix.casefold() == ".md":
                anchors = heading_anchors(resolved.read_text(encoding="utf-8"))
                if unquote(fragment).casefold() not in anchors:
                    errors.append(f"{path.relative_to(ROOT)}: missing anchor {target}")
    return errors


def markdown_urls() -> set[str]:
    urls = set()
    for path in tracked_markdown():
        for target in MARKDOWN_LINK.findall(path.read_text(encoding="utf-8")):
            clean = target.strip("<>")
            if urlsplit(clean).scheme in {"http", "https"}:
                urls.add(clean)
    return urls


def catalog_sources() -> list[SourceTarget]:
    targets = []
    for path in sorted(AGENTS_DIR.glob("*.yaml")):
        record = yaml.safe_load(path.read_text(encoding="utf-8"))
        for source in record.get("sources", []):
            errors = []
            source_id = source.get("id")
            url = source.get("url")
            archived_url = source.get("archived_url")
            capture = source.get("capture")
            manifest_path = None

            if not isinstance(source_id, str) or not source_id:
                errors.append("source id is missing or invalid")
                source_id = f"{path.name}:unknown-source"
            if not isinstance(url, str) or not url:
                errors.append("original URL is missing or invalid")
                url = ""
            if archived_url is not None and (not isinstance(archived_url, str) or not archived_url):
                errors.append("archived_url must be a non-empty string")
                archived_url = None
            if capture is not None:
                if not isinstance(capture, dict) or set(capture) != {"manifest_path"}:
                    errors.append("capture must contain only manifest_path")
                elif not isinstance(capture["manifest_path"], str) or not capture["manifest_path"]:
                    errors.append("capture.manifest_path must be a non-empty string")
                else:
                    manifest_path = capture["manifest_path"]

            targets.append(
                SourceTarget(
                    source_id=source_id,
                    url=url,
                    archived_url=archived_url,
                    manifest_path=manifest_path,
                    configuration_error="; ".join(errors) or None,
                )
            )
    return sorted(targets, key=lambda target: target.source_id)


def external_targets(
    sources: list[SourceTarget], documentation_urls: set[str]
) -> tuple[list[SourceTarget], list[str]]:
    catalog_urls = {target.url for target in sources if target.url}
    catalog_urls.update(target.archived_url for target in sources if target.archived_url)
    return sources, sorted(documentation_urls - catalog_urls)


def _safe_archive_path(relative: object, source_id: str, filename: str) -> tuple[Path | None, str]:
    if not isinstance(relative, str) or not relative:
        return None, f"{filename} path must be a non-empty string"
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or Path(relative).as_posix() != relative:
        return None, f"{filename} path must be a safe repository-relative POSIX path"
    expected_parent = PurePosixPath("archive", "sources", source_id)
    if pure.parent != expected_parent or pure.name != filename:
        return None, f"{filename} path must be {expected_parent / filename}"
    resolved = (ROOT / relative).resolve()
    source_root = (ROOT / expected_parent).resolve()
    if not resolved.is_relative_to(source_root):
        return None, f"{filename} path escapes {expected_parent}"
    return resolved, ""


def local_snapshot_result(target: SourceTarget) -> SnapshotResult:
    if target.configuration_error:
        return SnapshotResult("invalid", target.configuration_error)
    if target.manifest_path is None:
        return SnapshotResult("absent", "no local snapshot declared")

    manifest_path, error = _safe_archive_path(
        target.manifest_path, target.source_id, "metadata.json"
    )
    if error:
        return SnapshotResult("invalid", error)
    assert manifest_path is not None
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return SnapshotResult("invalid", f"manifest does not exist: {target.manifest_path}")
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return SnapshotResult("invalid", f"cannot read manifest: {type(exc).__name__}: {exc}")

    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        return SnapshotResult("invalid", "manifest must be a version 1 JSON object")
    if manifest.get("source_id") != target.source_id:
        return SnapshotResult("invalid", "manifest source_id does not match the catalog source")
    if manifest.get("original_url") != target.url:
        return SnapshotResult("invalid", "manifest original_url does not match the catalog source")
    if (
        "external_archive_url" in manifest
        and manifest["external_archive_url"] != target.archived_url
    ):
        return SnapshotResult(
            "invalid", "manifest external_archive_url does not match archived_url"
        )

    artifacts = manifest.get("artifacts")
    markdown = artifacts.get("markdown") if isinstance(artifacts, dict) else None
    if not isinstance(markdown, dict):
        return SnapshotResult("invalid", "manifest has no Markdown artifact")
    content_path, error = _safe_archive_path(markdown.get("path"), target.source_id, "content.md")
    if error:
        return SnapshotResult("invalid", error)
    assert content_path is not None
    try:
        content = content_path.read_bytes()
    except OSError as exc:
        return SnapshotResult(
            "invalid", f"cannot read Markdown artifact: {type(exc).__name__}: {exc}"
        )
    if not content:
        return SnapshotResult("invalid", "Markdown artifact is empty")

    expected_bytes = markdown.get("bytes")
    if (
        not isinstance(expected_bytes, int)
        or isinstance(expected_bytes, bool)
        or expected_bytes != len(content)
    ):
        return SnapshotResult("invalid", "Markdown artifact byte count does not match manifest")
    fingerprint = markdown.get("sha256")
    match = SHA256_RE.fullmatch(fingerprint) if isinstance(fingerprint, str) else None
    if match is None:
        return SnapshotResult("invalid", "Markdown artifact has an invalid SHA-256")
    actual_hash = hashlib.sha256(content).hexdigest()
    if actual_hash != match.group(1):
        return SnapshotResult("invalid", "Markdown artifact SHA-256 does not match manifest")
    return SnapshotResult("healthy", "verified local Markdown snapshot", content_path)


def check_url(url: str) -> LinkResult:
    headers = {"User-Agent": "internal-agents-map-link-check/1.0"}
    request = urllib.request.Request(url, headers=headers, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if response.status < 400:
                return LinkResult(url, "healthy", f"HTTP {response.status}")
            return LinkResult(url, "unreachable", f"HTTP {response.status}")
    except urllib.error.HTTPError as error:
        if error.code in BLOCKED_STATUS:
            return LinkResult(url, "blocked", f"HTTP {error.code}")
        if error.code not in MISSING_STATUS:
            return LinkResult(url, "unreachable", f"HTTP {error.code}")
        # Some sites do not implement HEAD correctly. Confirm a removed page with GET.
        try:
            get_request = urllib.request.Request(
                url,
                headers={**headers, "Range": "bytes=0-1023"},
                method="GET",
            )
            with urllib.request.urlopen(get_request, timeout=20) as response:
                return LinkResult(url, "healthy", f"GET HTTP {response.status}")
        except urllib.error.HTTPError as get_error:
            if get_error.code in MISSING_STATUS:
                return LinkResult(
                    url,
                    "missing",
                    f"HTTP {get_error.code} confirmed by GET",
                )
            if get_error.code in BLOCKED_STATUS:
                return LinkResult(url, "blocked", f"GET HTTP {get_error.code}")
            return LinkResult(url, "unreachable", f"GET HTTP {get_error.code}")
        except (urllib.error.URLError, TimeoutError, http.client.HTTPException, OSError) as error:
            return LinkResult(url, "unreachable", f"GET {type(error).__name__}: {error}")
    except (urllib.error.URLError, TimeoutError, http.client.HTTPException, OSError) as error:
        return LinkResult(url, "unreachable", f"{type(error).__name__}: {error}")


def classify_source(
    target: SourceTarget,
    original: LinkResult,
    snapshot: SnapshotResult,
    external_archive: LinkResult | None,
) -> SourceResult:
    archive_warnings = ()
    if external_archive is not None and external_archive.status != "healthy":
        archive_warnings = (
            f"external archive {external_archive.status}: {external_archive.url}: "
            f"{external_archive.detail}",
        )

    if snapshot.status == "invalid":
        return SourceResult(
            target.source_id,
            target.url,
            "missing",
            f"invalid declared local snapshot: {snapshot.detail}",
            archive_warnings,
        )
    if original.status != "missing":
        return SourceResult(
            target.source_id,
            target.url,
            original.status,
            original.detail,
            archive_warnings,
        )

    fallbacks = []
    if snapshot.status == "healthy":
        fallbacks.append("verified local snapshot")
    if external_archive is not None and external_archive.status == "healthy":
        fallbacks.append("healthy external archive")
    if fallbacks:
        return SourceResult(
            target.source_id,
            target.url,
            "archived",
            f"{original.detail}; fallback: {' and '.join(fallbacks)}",
            archive_warnings,
        )
    return SourceResult(
        target.source_id,
        target.url,
        "missing",
        f"{original.detail}; no verified archive fallback",
        archive_warnings,
    )


def check_external_targets(
    sources: list[SourceTarget],
    documentation_urls: list[str],
    checker: Callable[[str], LinkResult],
) -> tuple[list[SourceResult], list[LinkResult]]:
    urls = {target.url for target in sources if target.url}
    urls.update(target.archived_url for target in sources if target.archived_url)
    urls.update(documentation_urls)
    checked: dict[str, LinkResult] = {}
    if urls:
        with ThreadPoolExecutor(max_workers=min(8, len(urls))) as executor:
            futures = {executor.submit(checker, url): url for url in urls}
            for future in as_completed(futures):
                checked[futures[future]] = future.result()

    source_results = []
    for target in sources:
        original = checked.get(target.url)
        if original is None:
            original = LinkResult(target.url, "unreachable", "original URL is unavailable")
        archive = checked.get(target.archived_url) if target.archived_url else None
        source_results.append(
            classify_source(target, original, local_snapshot_result(target), archive)
        )
    documentation_results = [checked[url] for url in documentation_urls]
    return source_results, documentation_results


def main(
    argv: list[str] | None = None,
    *,
    checker: Callable[[str], LinkResult] | None = None,
) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local", action="store_true", help="Check local links only.")
    args = parser.parse_args(argv)
    errors = local_links()
    if not args.local:
        sources, documentation_urls = external_targets(catalog_sources(), markdown_urls())
        source_results, documentation_results = check_external_targets(
            sources, documentation_urls, checker or check_url
        )
        for result in sorted(source_results, key=lambda item: item.source_id):
            for warning in result.warnings:
                print(f"warning: {result.source_id}: {warning}", file=sys.stderr)
            if result.status == "missing":
                errors.append(f"{result.source_id}: {result.url}: {result.detail}")
            elif result.status != "healthy":
                print(
                    f"warning: {result.status}: {result.source_id}: {result.url}: {result.detail}",
                    file=sys.stderr,
                )
        for result in sorted(documentation_results, key=lambda item: item.url):
            if result.status == "missing":
                errors.append(f"{result.url}: {result.detail}")
            elif result.status != "healthy":
                print(
                    f"warning: {result.status}: {result.url}: {result.detail}",
                    file=sys.stderr,
                )

        statuses = ("healthy", "archived", "missing", "blocked", "unreachable")
        counts = {status: 0 for status in statuses}
        for result in [*source_results, *documentation_results]:
            counts[result.status] += 1
        print(
            "External links: "
            + ", ".join(f"{counts[status]} {status}" for status in statuses)
            + "."
        )
    if errors:
        print("\n".join(sorted(errors)), file=sys.stderr)
        return 1
    scope = "local links" if args.local else "local and external links"
    print(f"Checked {scope}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
