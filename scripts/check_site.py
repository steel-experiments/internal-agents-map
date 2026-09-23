# ABOUTME: Checks the built site artifact against the routes, exports, and assets it may publish.
# ABOUTME: Rejects extra files, unsafe links, missing evidence, and private contact data.
"""Validate the built site artifact without fetching external citations."""

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

# Files that public/ publishes exactly as they are authored.
PUBLIC_FILES = {"favicon.ico", "og.png", "fonts/Areal.woff2", "fonts/NanumMyeongjo-ExtraBold.woff2"}
# Exports and discovery files that no page route serves.
EXPORT_FILES = {
    "agents.json",
    "agents/index.json",
    "data-guide.md",
    "llms.txt",
    "robots.txt",
    "sitemap.xml",
}
# The document the host returns for an unknown path. No route points to it.
ERROR_PAGE = "404.html"
DIRECTORIES = {
    "_astro",
    "fonts",
    "notes",
    "agents",
    "logos",
    "organizations",
    "og",
    "og/agents",
    "og/organizations",
    "og/notes",
}
# A link preview card: PNG, this size, and no heavier than this.
OG_IMAGE_SIZE = (1200, 630)
OG_IMAGE_MAX_BYTES = 300_000
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
# A bundled stylesheet or script: a stem, which can hold dots, a content hash, and its type.
BUNDLED_ASSET = re.compile(r"_astro/[A-Za-z0-9_.-]+\.[A-Za-z0-9_-]{8,}\.(?:css|js)")
CHUNK_IMPORT = re.compile(r"\./([A-Za-z0-9_.-]+\.[A-Za-z0-9_-]{8,}\.js)")
CSS_URL = re.compile(r"url\(\s*['\"]?([^'\"\s)]+)['\"]?\s*\)")
# The research fields that qualify a statement and must stay beside it.
QUALIFIER_FIELDS = ("reported_by", "metric_scope", "denominator", "measurement_method", "valid_at")


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.urls: list[str] = []
        self.tags: set[str] = set()
        self.coverage: dict[str, list[str]] = {key: [] for key in ("approach", "claim", "source")}
        self.text: list[str] = []
        self.og_image: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.add(tag)
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(attributes["id"])
        for key in ("href", "src"):
            if attributes.get(key):
                self.urls.append(attributes[key])
        if attributes.get("srcset"):
            # Each candidate is a URL and an optional width or density descriptor.
            for candidate in attributes["srcset"].split(","):
                parts = candidate.split()
                if parts:
                    self.urls.append(parts[0])
        for key in self.coverage:
            if attributes.get(f"data-{key}-id"):
                self.coverage[key].append(attributes[f"data-{key}-id"])
        if tag == "meta" and attributes.get("property") == "og:image":
            self.og_image = attributes.get("content")

    def handle_data(self, data: str) -> None:
        self.text.append(data)


def visible_text(page: SiteParser) -> str:
    return " ".join(" ".join(page.text).split())


def og_image_file(route: str) -> str:
    """The preview card of a route. The home page keeps the authored card in public/."""
    return "og.png" if route == "/" else "og" + route + ".png"


def png_size(data: bytes) -> tuple[int, int] | None:
    """Read the pixel size of a PNG from its header, or None when it is not a PNG."""
    if not data.startswith(PNG_SIGNATURE) or data[12:16] != b"IHDR":
        return None
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def check_og_image(page: SiteParser, name: str, root: Path, errors: list[str]) -> None:
    """Every page names a card that exists in the artifact at the card size."""
    if not page.og_image:
        errors.append(f"Missing og:image: {name}")
        return
    parts = urlsplit(page.og_image)
    target = root / unquote(parts.path).lstrip("/")
    if not target.is_file():
        errors.append(f"Missing og:image target: {page.og_image} in {name}")
        return
    data = target.read_bytes()
    if png_size(data) != OG_IMAGE_SIZE:
        errors.append(f"og:image is not a {OG_IMAGE_SIZE[0]}x{OG_IMAGE_SIZE[1]} PNG: {parts.path}")
    if len(data) > OG_IMAGE_MAX_BYTES:
        errors.append(f"og:image is over {OG_IMAGE_MAX_BYTES} bytes: {parts.path}")


def route_files(routes: dict, errors: list[str]) -> set[str]:
    """Name the HTML and Markdown file that each published route is served from."""
    names: set[str] = set()
    for path, artifacts in sorted(routes.items()):
        if not path.startswith("/"):
            errors.append(f"Route path must start at the root: {path}")
            continue
        if not isinstance(artifacts, dict) or set(artifacts) != {"html", "markdown"}:
            errors.append(f"Route {path} must name one HTML and one Markdown artifact.")
            continue
        for name in artifacts.values():
            if not isinstance(name, str) or not name.startswith("/"):
                errors.append(f"Route {path} names an artifact outside the root: {name}")
                continue
            names.add(name.lstrip("/"))
    return names


def check_entry_routes(routes: dict, approaches: list[dict], errors: list[str]) -> None:
    """The entry routes and the catalog hold the same implementations."""
    listed = {path for path in routes if path.startswith("/agents/")}
    wanted = {f"/agents/{approach['id']}" for approach in approaches}
    for path in sorted(wanted - listed):
        errors.append(f"The route manifest omits {path}.")
    for path in sorted(listed - wanted):
        errors.append(f"The route manifest holds an entry the catalog does not hold: {path}.")


def check_directory_coverage(page: SiteParser, approaches: list[dict], errors: list[str]) -> None:
    """Every implementation has one card in the directory, and that card links to its page."""
    expected = Counter(approach["id"] for approach in approaches)
    if Counter(page.coverage["approach"]) != expected:
        errors.append("Incomplete or duplicate approach coverage in the directory.")
    linked = {url.split("#")[0] for url in page.urls if url.startswith("/agents/")}
    wanted = {f"/agents/{approach['id']}" for approach in approaches}
    for path in sorted(wanted - linked):
        errors.append(f"The directory does not link to {path}.")
    for path in sorted(linked - wanted):
        errors.append(f"The directory links to an entry that the catalog does not hold: {path}.")


def check_entry_coverage(
    page: SiteParser, approach: dict, claims: dict[str, dict], errors: list[str]
) -> None:
    """One entry page carries its own record, its own claims, and its own sources."""
    name = f"agents/{approach['id']}.html"
    if Counter(page.coverage["approach"]) != Counter([approach["id"]]):
        errors.append(f"Incomplete or duplicate approach coverage in {name}.")
    for kind, ids in (("claim", approach["claim_ids"]), ("source", approach["source_ids"])):
        if Counter(page.coverage[kind]) != Counter(ids):
            errors.append(f"Incomplete or duplicate {kind} coverage in {name}.")
    text = visible_text(page)
    for claim_id in approach["claim_ids"]:
        claim = claims.get(claim_id)
        if claim is None:
            errors.append(f"Unknown claim {claim_id} in {name}.")
            continue
        if " ".join(str(claim["text"]).split()) not in text:
            errors.append(f"Missing claim text: {claim_id} in {name}")
        for field in QUALIFIER_FIELDS:
            value = claim.get(field)
            if value and " ".join(str(value).split()) not in text:
                errors.append(f"Missing caveat {field}: {claim_id} in {name}")


def validate(
    root: Path,
    catalog_path: Path = ROOT / "data/agents.json",
    routes_path: Path = ROOT / "routing-manifest.json",
) -> list[str]:
    errors: list[str] = []
    if root.is_symlink() or not root.is_dir():
        return ["Site root must be a real directory, not a symlink."]
    catalog_bytes = catalog_path.read_bytes()
    catalog = json.loads(catalog_bytes)
    approaches = list(catalog["approaches"])
    claims = {claim["id"]: claim for claim in catalog["claims"]}
    manifest = json.loads(routes_path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1:
        errors.append("Unsupported route manifest schema version.")
    routes = manifest.get("routes") or {}
    check_entry_routes(routes, approaches, errors)
    company_ids = {approach["company_id"] for approach in approaches}
    wanted_companies = {f"/organizations/{company_id}" for company_id in company_ids}
    listed_companies = {path for path in routes if path.startswith("/organizations/")}
    if wanted_companies != listed_companies:
        errors.append("Organization route membership differs from the catalog.")
    expected = route_files(routes, errors) | PUBLIC_FILES | EXPORT_FILES | {ERROR_PAGE}
    # Every route except the home page publishes its own preview card.
    expected |= {og_image_file(route) for route in routes}
    expected |= {f"agents/{approach['id']}.json" for approach in approaches}
    # The published logo set comes from the companies the catalog declares.
    for company in catalog.get("companies") or []:
        logo = company.get("logo")
        if isinstance(logo, dict) and isinstance(logo.get("path"), str):
            expected.add(logo["path"])
    if errors:
        return errors

    root = root.resolve()
    actual = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append(f"Symlink is forbidden: {path.relative_to(root)}")
        elif path.is_file():
            actual.add(path.relative_to(root).as_posix())
            if path.stat().st_size == 0:
                errors.append(f"Empty output: {path.relative_to(root)}")
        elif path.is_dir() and path.relative_to(root).as_posix() not in DIRECTORIES:
            errors.append(f"Unexpected directory: {path.relative_to(root)}")
    missing = sorted(expected - actual)
    if missing:
        errors.append(f"Output boundary mismatch: missing {missing}")
    if errors:
        return errors

    try:
        pages = {}
        for name in sorted(name for name in expected if name.endswith(".html")):
            page = SiteParser()
            page.feed((root / name).read_text(encoding="utf-8"))
            pages[root / name] = page
            for required in ("html", "head", "title", "body", "nav", "main", "header", "footer"):
                if required not in page.tags:
                    errors.append(f"Missing landmark: {required} in {name}")
            duplicates = sorted(key for key, count in Counter(page.ids).items() if count > 1)
            if duplicates:
                errors.append(f"Duplicate IDs: {duplicates} in {name}")
            check_og_image(page, name, root, errors)

        # A bundled asset is publishable only where a published document asks for it.
        referenced = {url.lstrip("/").split("#")[0] for page in pages.values() for url in page.urls}
        for css_path in (root / "_astro").glob("*.css"):
            css = css_path.read_text(encoding="utf-8")
            referenced |= {match[1].lstrip("/") for match in CSS_URL.finditer(css)}
        # A bundled script may import another chunk, which no document names.
        pending = [name for name in referenced if name.endswith(".js")]
        walked = set()
        while pending:
            script_name = pending.pop()
            if script_name in walked:
                continue
            walked.add(script_name)
            script_path = root / script_name
            if not script_path.is_file():
                continue
            folder = script_name.rsplit("/", 1)[0] if "/" in script_name else ""
            script = script_path.read_text(encoding="utf-8")
            for match in CHUNK_IMPORT.finditer(script):
                imported = f"{folder}/{match[1]}" if folder else match[1]
                referenced.add(imported)
                pending.append(imported)
        allowed = expected | {name for name in referenced if BUNDLED_ASSET.fullmatch(name)}
        extra = sorted(actual - allowed)
        if extra:
            errors.append(f"Output boundary mismatch: extra {extra}")

        if (root / "agents.json").read_bytes() != catalog_bytes:
            errors.append("Site JSON differs from the source catalog.")
        check_directory_coverage(pages[root / "index.html"], approaches, errors)
        for company_id in company_ids:
            page = pages.get(root / f"organizations/{company_id}.html")
            wanted = Counter(a["id"] for a in approaches if a["company_id"] == company_id)
            if page is None or Counter(page.coverage["approach"]) != wanted:
                errors.append(f"Incorrect organization membership: {company_id}.")
        for approach in approaches:
            page = pages.get(root / f"agents/{approach['id']}.html")
            if page is not None:
                check_entry_coverage(page, approach, claims, errors)

        def check_url(url: str, document: Path) -> None:
            url = url.strip()
            parts = urlsplit(url)
            if parts.scheme:
                if parts.scheme.lower() not in {"http", "https"}:
                    errors.append(f"Unsafe URL scheme: {url}")
                return
            if parts.netloc:
                errors.append(f"Asset/link must be relative: {url}")
                return
            rooted = url.startswith("/")
            decoded = unquote(parts.path)
            if "\\" in decoded:
                errors.append(f"Invalid path separator: {url}")
                return
            base = root if rooted else document.parent
            target = (base / decoded.lstrip("/")).resolve() if decoded else document
            if not target.is_relative_to(root):
                errors.append(f"Path escapes site: {url}")
                return
            # A clean URL such as /agents/<id> or /notes is served from <id>.html.
            clean = None if target == root else target.with_name(target.name + ".html")
            if clean is not None and clean.is_file():
                target = clean
            elif target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                errors.append(f"Missing local target: {url}")
            elif parts.fragment and (
                target not in pages or unquote(parts.fragment) not in pages[target].ids
            ):
                errors.append(f"Invalid fragment: {url}")

        for document, page in pages.items():
            for url in page.urls:
                check_url(url, document)
        for css_path in (root / "_astro").glob("*.css"):
            css = css_path.read_text(encoding="utf-8")
            for match in CSS_URL.finditer(css):
                check_url(match[1], css_path)
            if "@import" in css.lower():
                errors.append("CSS imports are outside the self-contained artifact contract.")
        # Reuse the existing policy on every artifact, including new untracked text.
        spec = importlib.util.spec_from_file_location(
            "site_privacy", ROOT / "scripts/check_private_data.py"
        )
        privacy = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(privacy)
        for name in sorted(actual):
            if privacy.find_emails(root / name):
                errors.append(f"Private contact data in artifact: {name}")
    except (OSError, ValueError, KeyError) as error:
        errors.append(f"Invalid artifact: {error}")
    return errors


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root", type=Path, default=ROOT / "dist")
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
