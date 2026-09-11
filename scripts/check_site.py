"""Validate the generated Pages artifact without fetching external citations."""

from __future__ import annotations

import argparse
import hashlib
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
    "favicon.ico",
    "og.png",
    "404.html",
    "index.html",
    "definitions.html",
    "methodology.html",
    "notes.html",
    "notes/stop-a-run.html",
    "notes/review-noise.html",
    "notes/split-the-work.html",
    "notes/work-can-continue.html",
    "notes/load-tools.html",
    "notes/steps-without-a-model.html",
    "notes/test-on-your-work.html",
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
    catalog = json.loads(catalog_path.read_bytes())
    allowed = ALLOWED_FILES | {
        "robots.txt",
        "sitemap.xml",
        "llms.txt",
        "data-guide.md",
        "agents/index.json",
        "assets/manifest.json",
    }
    allowed |= {
        name.replace(".html", ".md")
        for name in ALLOWED_FILES
        if name.endswith(".html") and name != "404.html"
    }
    allowed |= {f"agents/{a['id']}.{ext}" for a in catalog["approaches"] for ext in ("json", "md")}
    try:
        manifest = json.loads((root / "assets/manifest.json").read_text())
        if set(manifest) != {"site.css", "site.js", "fonts/Geist.woff2"}:
            errors.append("Invalid hashed asset manifest.")
        for original, hashed in manifest.items():
            original_path = Path(original)
            pattern = (
                re.escape(str(original_path.with_suffix("")))
                + r"\.[a-f0-9]{16}"
                + re.escape(original_path.suffix)
            )
            if not re.fullmatch(pattern, hashed):
                errors.append(f"Invalid hashed asset path: {hashed}")
                continue
            allowed.add("assets/" + hashed)
            content = (root / "assets" / hashed).read_bytes()
            if hashlib.sha256(content).hexdigest()[:16] != Path(hashed).name.split(".")[-2]:
                errors.append(f"Asset content hash mismatch: {hashed}")
    except (OSError, ValueError, TypeError):
        errors.append("Missing or invalid hashed assets.")
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
        elif path.is_dir() and path.relative_to(root).as_posix() not in {
            "assets",
            "assets/fonts",
            "notes",
            "agents",
        }:
            errors.append(f"Unexpected directory: {path.relative_to(root)}")
    if actual != allowed:
        errors.append(
            f"Output boundary mismatch: missing {sorted(allowed - actual)}, extra {sorted(actual - allowed)}"
        )
    if errors:
        return errors
    try:
        pages = {}
        for name in sorted(allowed):
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
            if document.name == "404.html" and url.startswith("/") and not url.startswith("//"):
                check_url(url[1:], root / "index.html")
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
        for css_path in (root / "assets").glob("*.css"):
            css = css_path.read_text(encoding="utf-8")
            for match in re.finditer(r"url\(\s*['\"]?([^'\"\s)]+)['\"]?\s*\)", css):
                check_url(match[1], css_path)
            if "@import" in css.lower():
                errors.append("CSS imports are outside the self-contained artifact contract.")
        # Reuse the existing policy on every artifact, including new untracked text.
        spec = importlib.util.spec_from_file_location(
            "site_privacy", ROOT / "scripts/check_private_data.py"
        )
        privacy = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(privacy)
        for name in allowed:
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
