#!/usr/bin/env python3
"""Check local Markdown links and catalog source URLs."""

from __future__ import annotations

import argparse
import http.client
import re
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
BLOCKED_STATUS = {401, 403, 405, 406, 429}


def tracked_markdown() -> list[Path]:
    tracked = subprocess.run(
        ["git", "ls-files", "*.md"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    return [ROOT / relative for relative in sorted(tracked)]


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


def source_urls() -> list[str]:
    urls = set()
    for path in sorted((ROOT / "data" / "agents").glob("*.yaml")):
        record = yaml.safe_load(path.read_text(encoding="utf-8"))
        urls.update(source["url"] for source in record.get("sources", []))
    return sorted(urls | markdown_urls())


def check_url(url: str) -> str | None:
    headers = {"User-Agent": "internal-agents-map-link-check/1.0"}
    request = urllib.request.Request(url, headers=headers, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if response.status < 400:
                return None
            return f"{url}: HTTP {response.status}"
    except urllib.error.HTTPError as error:
        if error.code in BLOCKED_STATUS:
            return None
        if error.code != 404:
            return None
        # Some sites do not implement HEAD correctly. Confirm a missing page with GET.
        try:
            get_request = urllib.request.Request(
                url,
                headers={**headers, "Range": "bytes=0-1023"},
                method="GET",
            )
            with urllib.request.urlopen(get_request, timeout=20):
                return None
        except urllib.error.HTTPError as get_error:
            return f"{url}: HTTP 404" if get_error.code == 404 else None
        except (urllib.error.URLError, TimeoutError, http.client.HTTPException, OSError):
            return None
    except (urllib.error.URLError, TimeoutError, http.client.HTTPException, OSError):
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local", action="store_true", help="Check local links only.")
    args = parser.parse_args()
    errors = local_links()
    if not args.local:
        with ThreadPoolExecutor(max_workers=8) as executor:
            checks = {executor.submit(check_url, url): url for url in source_urls()}
            for future in as_completed(checks):
                result = future.result()
                if result:
                    errors.append(result)
    if errors:
        print("\n".join(sorted(errors)), file=sys.stderr)
        return 1
    scope = "local links" if args.local else "local and external links"
    print(f"Checked {scope}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
