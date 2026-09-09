"""Validate the generated Pages artifact without fetching external citations."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_FILES = {
    "index.html",
    "definitions.html",
    "agents.json",
    "assets/site.css",
    "assets/site.js",
    "assets/fonts/Geist.woff2",
    "assets/fonts/OFL.txt",
}


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.urls: list[str] = []
        self.tags: set[str] = set()
        self.coverage: dict[str, list[str]] = {key: [] for key in ("approach", "claim", "source")}
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.add(tag)
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(attributes["id"])
        for key in ("href", "src"):
            if attributes.get(key):
                self.urls.append(attributes[key])
        for key in self.coverage:
            if attributes.get(f"data-{key}-id"):
                self.coverage[key].append(attributes[f"data-{key}-id"])

    def handle_data(self, data: str) -> None:
        self.text.append(data)


def validate(root: Path, catalog_path: Path = ROOT / "data/agents.json") -> list[str]:
    errors = []
    if root.is_symlink() or not root.is_dir():
        return ["Site root must be a real directory, not a symlink."]
    root = root.resolve()
    actual = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append(f"Symlink is forbidden: {path.relative_to(root)}")
        elif path.is_file():
            actual.add(path.relative_to(root).as_posix())
            if path.stat().st_size == 0:
                errors.append(f"Empty output: {path.relative_to(root)}")
        elif path.is_dir() and path.relative_to(root).as_posix() not in {"assets", "assets/fonts"}:
            errors.append(f"Unexpected directory: {path.relative_to(root)}")
    if actual != ALLOWED_FILES:
        errors.append(
            f"Output boundary mismatch: missing {sorted(ALLOWED_FILES - actual)}, extra {sorted(actual - ALLOWED_FILES)}"
        )
    if errors:
        return errors
    try:
        pages = {}
        for name in sorted(ALLOWED_FILES):
            if not name.endswith(".html"):
                continue
            page = SiteParser()
            page.feed((root / name).read_text(encoding="utf-8"))
            pages[root / name] = page
            for required in ("html", "head", "title", "body", "nav", "main", "header", "footer"):
                if required not in page.tags:
                    errors.append(f"Missing landmark: {required} in {name}")
            duplicates = sorted(key for key, count in Counter(page.ids).items() if count > 1)
            if duplicates:
                errors.append(f"Duplicate IDs: {duplicates} in {name}")
        parser = pages[root / "index.html"]
        catalog_bytes = catalog_path.read_bytes()
        catalog = json.loads(catalog_bytes)
        if (root / "agents.json").read_bytes() != catalog_bytes:
            errors.append("Site JSON differs from the source catalog.")
        for kind, collection in (
            ("approach", "approaches"),
            ("claim", "claims"),
            ("source", "sources"),
        ):
            expected = Counter(item["id"] for item in catalog[collection])
            if Counter(parser.coverage[kind]) != expected:
                errors.append(f"Incomplete or duplicate {kind} coverage.")
        visible_text = " ".join(" ".join(parser.text).split())
        for claim in catalog["claims"]:
            if " ".join(str(claim["text"]).split()) not in visible_text:
                errors.append(f"Missing claim text: {claim['id']}")

        def check_url(url: str, document: Path) -> None:
            url = url.strip()
            parts = urlsplit(url)
            if parts.scheme:
                if parts.scheme.lower() not in {"http", "https"}:
                    errors.append(f"Unsafe URL scheme: {url}")
                return
            if parts.netloc or url.startswith(("/", "\\")):
                errors.append(f"Asset/link must be relative: {url}")
                return
            decoded = unquote(parts.path)
            if "\\" in decoded:
                errors.append(f"Invalid path separator: {url}")
                return
            target = (document.parent / decoded).resolve() if decoded else document
            if not target.is_relative_to(root):
                errors.append(f"Path escapes site: {url}")
            elif not target.is_file():
                errors.append(f"Missing local target: {url}")
            elif parts.fragment and (
                target not in pages or unquote(parts.fragment) not in pages[target].ids
            ):
                errors.append(f"Invalid fragment: {url}")

        for document, page in pages.items():
            for url in page.urls:
                check_url(url, document)
        css = (root / "assets/site.css").read_text(encoding="utf-8")
        for match in re.finditer(r'url\(\s*[\'"]?([^\'"\s)]+)[\'"]?\s*\)', css):
            check_url(match[1], root / "assets/site.css")
        if "@import" in css.lower():
            errors.append("CSS imports are outside the self-contained artifact contract.")
        # Reuse the existing policy on every artifact, including new untracked text.
        spec = importlib.util.spec_from_file_location(
            "site_privacy", ROOT / "scripts/check_private_data.py"
        )
        privacy = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(privacy)
        for name in ALLOWED_FILES:
            if privacy.find_emails(root / name):
                errors.append(f"Private contact data in artifact: {name}")
    except (OSError, ValueError, KeyError) as error:
        errors.append(f"Invalid artifact: {error}")
    return errors


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root", type=Path, default=ROOT / "site")
    args = cli.parse_args()
    errors = validate(args.root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Validated site artifact: coverage, links, assets, JSON parity, and privacy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
