# ABOUTME: Validates the authored research records and normalizes them into the catalog.
# ABOUTME: Writes data/agents.json and the generated Markdown documents of the repository.
"""Validate the research records and build the catalog data and repository documents."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import struct
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn
from urllib.parse import urlsplit

try:
    import yaml
    from jsonschema import Draft7Validator, FormatChecker
except ImportError:
    sys.exit("PyYAML and jsonschema are required. Install project dependencies with 'uv sync'.")

ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOT / "data" / "agents"
README = ROOT / "README.md"
LANDSCAPE = ROOT / "docs" / "landscape.md"
PATTERNS = ROOT / "docs" / "patterns.md"
ADOPTION_LESSONS = ROOT / "docs" / "adoption-lessons.md"
DATA_JSON = ROOT / "data" / "agents.json"
OVERVIEW_BEGIN = "<!-- BEGIN OVERVIEW -->"
OVERVIEW_END = "<!-- END OVERVIEW -->"
README_FINDINGS_BEGIN = "<!-- BEGIN README FINDINGS -->"
README_FINDINGS_END = "<!-- END README FINDINGS -->"
PATTERNS_SNAPSHOT_BEGIN = "<!-- BEGIN PATTERNS SNAPSHOT -->"
PATTERNS_SNAPSHOT_END = "<!-- END PATTERNS SNAPSHOT -->"
ADOPTION_SNAPSHOT_BEGIN = "<!-- BEGIN ADOPTION SNAPSHOT -->"
ADOPTION_SNAPSHOT_END = "<!-- END ADOPTION SNAPSHOT -->"

AGENT_SCHEMA_FILE = ROOT / "data" / "agent.schema.json"
AGENT_SCHEMA = json.loads(AGENT_SCHEMA_FILE.read_text(encoding="utf-8"))
# Every agent file holds this line, so that a YAML editor loads the agent schema.
SCHEMA_MODELINE = "# yaml-language-server: $schema=../agent.schema.json"
SCHEMA_VALUES_TS = ROOT / "src" / "lib" / "schema-values.ts"
BOUNDARY_LEVELS = {
    "continuous-steering": 2,
    "work-product-review": 3,
    "outcome-review": 4,
    "exception-only": 5,
    "unknown": None,
}
ID_RE = re.compile(AGENT_SCHEMA["definitions"]["kebabId"]["pattern"])
DATE_RE = re.compile(AGENT_SCHEMA["definitions"]["partialDate"]["pattern"])
RFC3339_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
MAX_PDF_BYTES = 10 * 1024 * 1024
COMPANY_REQUIRED_FIELDS = {"id", "name", "homepage", "logo"}
COMPANY_OPTIONAL_FIELDS = {"logo_note"}
COMPANY_LOGO_FIELDS = {"file", "source_url", "accessed_at"}
LOGO_MEDIA_TYPES = {".svg": "image/svg+xml", ".png": "image/png"}
MAX_SVG_LOGO_BYTES = 64 * 1024
MAX_PNG_LOGO_BYTES = 128 * 1024
MIN_PNG_LOGO_WIDTH = 128
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
COMPANIES_FILE_NAME = "data/companies.yaml"
LOGOS_DIR_NAME = "public/logos"
CAPTURE_MANIFEST_FIELDS = {
    "schema_version",
    "source_id",
    "original_url",
    "final_url",
    "captured_at",
    "http_status",
    "tool",
    "artifacts",
}
CAPTURE_MANIFEST_OPTIONAL_FIELDS = {"external_archive_url"}
CAPTURE_ARTIFACT_FIELDS = {"path", "sha256", "bytes"}

TABLE_HEADER = (
    "| Company | Approach | Type | Domains | Operating model | Autonomy | Stage | Status | Year |\n"
    "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"
)
OVERVIEW_TABLE_HEADER = "| Organization | Approach | Type | Work |\n| --- | --- | --- | --- |"


class UniqueKeyLoader(yaml.SafeLoader):
    """Load YAML and reject duplicate mapping keys."""


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def die(message: str) -> NoReturn:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def schema_values(definition: str) -> frozenset[str]:
    """Give the allowed values of one enum definition in the agent schema."""
    return frozenset(AGENT_SCHEMA["definitions"][definition]["enum"])


FORMAT_CHECKER = FormatChecker(formats=())


@FORMAT_CHECKER.checks("partial-date", raises=ValueError)
def is_calendar_date(value: object) -> bool:
    """Reject a full date that does not exist, such as 2026-02-31."""
    if isinstance(value, str) and len(value) == 10:
        date.fromisoformat(value)
    return True


AGENT_VALIDATOR = Draft7Validator(AGENT_SCHEMA, format_checker=FORMAT_CHECKER)


def schema_errors(record: Any, filename: str) -> list[str]:
    """Give one line for each place where a record does not agree with the agent schema."""
    errors = sorted(
        AGENT_VALIDATOR.iter_errors(record),
        key=lambda error: [str(part) for part in error.absolute_path],
    )
    return [
        f"{filename}: {'.'.join(str(part) for part in error.absolute_path) or '(record)'}: "
        f"{error.message}"
        for error in errors
    ]


def validate_date(value: Any, field: str, filename: str) -> None:
    if not isinstance(value, str) or not DATE_RE.fullmatch(value):
        die(f"{filename}: '{field}' must use YYYY, YYYY-MM, or YYYY-MM-DD.")
    if len(value) == 10:
        try:
            date.fromisoformat(value)
        except ValueError:
            die(f"{filename}: '{field}' must be a valid calendar date.")


def validate_https_url(value: Any, field: str, filename: str) -> None:
    """Require a non-empty HTTPS URL with an authority component."""
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        die(f"{filename}: '{field}' must be a non-empty HTTPS URL.")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.netloc:
        die(f"{filename}: '{field}' must be a non-empty HTTPS URL.")


def validate_rfc3339_utc(value: Any, field: str, filename: str) -> None:
    """Require an RFC 3339 timestamp expressed with the UTC ``Z`` suffix."""
    if not isinstance(value, str) or not RFC3339_UTC_RE.fullmatch(value):
        die(f"{filename}: '{field}' must be an RFC 3339 UTC timestamp ending in Z.")
    try:
        datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
    except ValueError:
        die(f"{filename}: '{field}' must be a valid RFC 3339 UTC timestamp.")


def require_exact_fields(
    value: Any,
    required: set[str],
    optional: set[str],
    field: str,
    filename: str,
) -> dict:
    if not isinstance(value, dict):
        die(f"{filename}: '{field}' must be a mapping.")
    missing = sorted(required - set(value))
    unexpected = sorted(set(value) - required - optional, key=str)
    if missing:
        die(f"{filename}: '{field}' is missing field(s): {', '.join(missing)}")
    if unexpected:
        names = ", ".join(str(item) for item in unexpected)
        die(f"{filename}: '{field}' contains unexpected field(s): {names}")
    return value


def resolve_capture_path(
    value: Any,
    source_id: str,
    expected_name: str,
    field: str,
    filename: str,
    *,
    root: Path | None = None,
) -> Path:
    """Resolve one deterministic capture path without allowing repository escape."""
    if not isinstance(value, str) or not value.strip() or "\\" in value:
        die(f"{filename}: '{field}' must be a POSIX repository-relative path.")
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts:
        die(f"{filename}: '{field}' must not be absolute or contain '..'.")
    expected = PurePosixPath("archive", "sources", source_id, expected_name)
    if pure != expected or str(pure) != value:
        die(f"{filename}: '{field}' must be {str(expected)!r}.")

    repository_root = (root or ROOT).resolve()
    archive_root = repository_root / "archive" / "sources"
    bundle_root = archive_root / source_id
    if archive_root.resolve() != archive_root or bundle_root.resolve() != bundle_root:
        die(f"{filename}: '{field}' resolves outside archive/sources/{source_id}/.")
    resolved = (repository_root / Path(*pure.parts)).resolve()
    try:
        archive_root.relative_to(repository_root)
        bundle_root.relative_to(archive_root)
        resolved.relative_to(bundle_root)
    except ValueError:
        die(f"{filename}: '{field}' resolves outside archive/sources/{source_id}/.")
    return resolved


def _load_json_object(path: Path, field: str, filename: str) -> dict:
    def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate key {key!r}")
            result[key] = value
        return result

    try:
        text = path.read_text(encoding="utf-8")
        value = json.loads(text, object_pairs_hook=reject_duplicate_keys)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        die(f"{filename}: could not parse '{field}' as JSON: {error}")
    if not isinstance(value, dict):
        die(f"{filename}: '{field}' must contain a JSON object.")
    return value


def validate_capture_artifact(
    artifact: Any,
    artifact_name: str,
    source_id: str,
    filename: str,
    *,
    root: Path | None = None,
) -> None:
    field = f"sources.{source_id}.capture.artifacts.{artifact_name}"
    descriptor = require_exact_fields(artifact, CAPTURE_ARTIFACT_FIELDS, set(), field, filename)
    expected_name = "content.md" if artifact_name == "markdown" else "page.pdf"
    path = resolve_capture_path(
        descriptor["path"], source_id, expected_name, f"{field}.path", filename, root=root
    )
    if not isinstance(descriptor["sha256"], str) or not SHA256_RE.fullmatch(descriptor["sha256"]):
        die(f"{filename}: '{field}.sha256' must be 'sha256:' plus 64 lowercase hex digits.")
    byte_count = descriptor["bytes"]
    if type(byte_count) is not int or byte_count < 0:
        die(f"{filename}: '{field}.bytes' must be a non-negative integer.")
    if not path.is_file():
        die(f"{filename}: declared capture artifact does not exist: {descriptor['path']}")
    try:
        actual_size = path.stat().st_size
    except OSError as error:
        die(f"{filename}: could not inspect capture artifact {descriptor['path']!r}: {error}")
    if artifact_name == "pdf" and actual_size > MAX_PDF_BYTES:
        die(f"{filename}: PDF capture exceeds the 10 MiB limit: {descriptor['path']}")
    try:
        content = path.read_bytes()
    except OSError as error:
        die(f"{filename}: could not read capture artifact {descriptor['path']!r}: {error}")
    if actual_size != byte_count:
        die(f"{filename}: byte count does not match capture artifact {descriptor['path']!r}.")
    digest = f"sha256:{hashlib.sha256(content).hexdigest()}"
    if digest != descriptor["sha256"]:
        die(f"{filename}: SHA-256 does not match capture artifact {descriptor['path']!r}.")
    if artifact_name == "markdown":
        try:
            markdown_content = content.decode("utf-8")
        except UnicodeDecodeError:
            die(f"{filename}: Markdown capture must be valid UTF-8: {descriptor['path']}")
        if not markdown_content.strip():
            die(f"{filename}: Markdown capture must not be empty: {descriptor['path']}")
    elif not content.startswith(b"%PDF-"):
        die(f"{filename}: PDF capture must begin with '%PDF-': {descriptor['path']}")


def load_capture_manifest(source: dict, filename: str, *, root: Path | None = None) -> dict | None:
    """Load and fully validate a source's optional Steel capture manifest."""
    if "capture" not in source:
        return None
    source_id = source.get("id")
    if not isinstance(source_id, str):
        die(f"{filename}: a captured source must have a string id.")
    field = f"sources.{source_id}.capture"
    capture = require_exact_fields(source["capture"], {"manifest_path"}, set(), field, filename)
    manifest_path = resolve_capture_path(
        capture["manifest_path"],
        source_id,
        "metadata.json",
        f"{field}.manifest_path",
        filename,
        root=root,
    )
    if not manifest_path.is_file():
        die(f"{filename}: declared capture manifest does not exist: {capture['manifest_path']}")
    manifest = _load_json_object(manifest_path, f"{field}.manifest_path", filename)
    manifest = require_exact_fields(
        manifest,
        CAPTURE_MANIFEST_FIELDS,
        CAPTURE_MANIFEST_OPTIONAL_FIELDS,
        f"{field} manifest",
        filename,
    )
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
        die(f"{filename}: capture manifest schema_version must be 1.")
    if manifest["source_id"] != source_id:
        die(f"{filename}: capture manifest source_id must match {source_id!r}.")
    if manifest["original_url"] != source.get("url"):
        die(f"{filename}: capture manifest original_url must match the source URL.")
    validate_https_url(manifest["final_url"], f"{field}.final_url", filename)
    validate_rfc3339_utc(manifest["captured_at"], f"{field}.captured_at", filename)
    status = manifest["http_status"]
    if type(status) is not int or not 200 <= status <= 299:
        die(f"{filename}: capture manifest http_status must be an integer from 200 to 299.")
    tool = require_exact_fields(
        manifest["tool"], {"name", "version"}, set(), f"{field}.tool", filename
    )
    if tool["name"] != "steel":
        die(f"{filename}: capture manifest tool name must be 'steel'.")
    if not isinstance(tool["version"], str) or not tool["version"].strip():
        die(f"{filename}: capture manifest tool version must be a non-empty string.")
    artifacts = require_exact_fields(
        manifest["artifacts"], {"markdown"}, {"pdf"}, f"{field}.artifacts", filename
    )
    validate_capture_artifact(artifacts["markdown"], "markdown", source_id, filename, root=root)
    if "pdf" in artifacts:
        validate_capture_artifact(artifacts["pdf"], "pdf", source_id, filename, root=root)
    if "external_archive_url" in manifest and manifest["external_archive_url"] != source.get(
        "archived_url"
    ):
        die(
            f"{filename}: capture manifest external_archive_url must match the source archived_url."
        )
    return manifest


def claim_fields(record: dict) -> dict[str, tuple[str, str, str]]:
    """Return claim path -> (text, kind, provenance) for authored claim fields."""
    claims: dict[str, tuple[str, str, str]] = {"summary": (record["summary"], "fact", "reported")}
    headline = record.get("headline_metric")
    if headline:
        claims["headline_metric"] = (headline, "metric", "reported")
    for key, value in (record.get("architecture") or {}).items():
        if value:
            text = ", ".join(value) if key == "interfaces" else value
            claims[f"architecture.{key}"] = (text, "fact", "reported")
    for index, item in enumerate(record.get("primitives") or []):
        text = item.get("desc") or item.get("name")
        claims[f"primitives.{index}"] = (text, "fact", "reported")
    for index, text in enumerate(record.get("key_metrics") or []):
        claims[f"key_metrics.{index}"] = (text, "metric", "reported")
    for index, text in enumerate(record.get("lessons_learned") or []):
        claims[f"lessons_learned.{index}"] = (text, "inference", "catalog-judgment")
    for index, item in enumerate(record["operating_models"]):
        boundary = item["attention_boundary"]
        level = BOUNDARY_LEVELS[boundary]
        label = f"Level {level}" if level is not None else "Unclassified"
        text = f"{label} for {item['scope']}; human attention boundary: {boundary}."
        claims[f"operating_models.{index}"] = (text, "inference", "catalog-judgment")
    return claims


def validate_source(source: dict, filename: str, seen: set[str]) -> None:
    source_id = source["id"]
    if source_id in seen:
        die(f"{filename}: duplicate source id {source_id!r}.")
    seen.add(source_id)
    load_capture_manifest(source, filename)


def validate_evidence(record: dict, filename: str, source_ids: set[str]) -> None:
    evidence = record["evidence"]
    claims = claim_fields(record)
    missing = sorted(set(claims) - set(evidence))
    extra = sorted(set(evidence) - set(claims))
    if missing:
        die(f"{filename}: missing evidence for claim(s): {', '.join(missing)}")
    if extra:
        die(f"{filename}: evidence refers to unknown claim(s): {', '.join(extra)}")
    for path, links in evidence.items():
        for link in links:
            if link["source_id"] not in source_ids:
                die(f"{filename}: evidence for {path!r} uses unknown source {link['source_id']!r}.")
    for path in record.get("claim_metadata") or {}:
        if path not in claims:
            die(f"{filename}: invalid claim metadata path {path!r}.")


def validate_page_content(record: dict, filename: str, source_ids: set[str]) -> None:
    """Validate the optional editorial coverage contract against this record's claims."""
    page = record.get("page_content")
    if page is None:
        return
    reviewed = set(page["source_ids"])
    if reviewed - source_ids:
        die(f"{filename}: page_content.source_ids must be sources belonging to this entry.")
    claims = claim_fields(record)

    def disposition(value: dict, field: str, allowed_paths: set[str] | None = None) -> None:
        paths = value["claim_paths"]
        if any(path not in claims for path in paths):
            die(f"{filename}: {field}.claim_paths contains an unknown claim path.")
        if allowed_paths is not None and set(paths) - allowed_paths:
            die(f"{filename}: {field}.claim_paths contains a claim outside its allowed field.")
        if value["state"] != "reported":
            return
        for path in paths:
            supports = {
                link["source_id"]
                for link in record["evidence"][path]
                if link.get("relation", "supports") == "supports"
            }
            if not supports & reviewed:
                die(
                    f"{filename}: {field} reported claim {path!r} lacks support from a reviewed source."
                )

    for key, value in page["questions"].items():
        disposition(value, f"page_content.questions.{key}")
    for key, value in page["implementation_fields"].items():
        disposition(value, f"page_content.implementation_fields.{key}", {f"architecture.{key}"})

    roles = page["primitive_roles"]
    expected_primitives = {f"primitives.{i}" for i, _ in enumerate(record.get("primitives") or [])}
    if set(roles) != expected_primitives:
        die(f"{filename}: page_content.primitive_roles must classify every primitive exactly once.")
    workflow_paths = page["questions"]["workflow"]["claim_paths"]
    if any(roles.get(path) != "workflow" for path in workflow_paths) or set(workflow_paths) != {
        path for path, role in roles.items() if role == "workflow"
    }:
        die(
            f"{filename}: workflow claim_paths must name exactly the workflow primitives in reading order."
        )

    observations = page["observations"]
    expected_observations = ({"headline_metric"} if record.get("headline_metric") else set()) | {
        f"key_metrics.{i}" for i, _ in enumerate(record.get("key_metrics") or [])
    }
    if set(observations) != expected_observations:
        die(f"{filename}: page_content.observations must describe every observation claim.")
    duplicates: dict[str, str] = {}
    for path, value in observations.items():
        if "duplicate_of" in value:
            target = value["duplicate_of"]
            if target not in expected_observations or target == path:
                die(f"{filename}: observation {path!r} has an invalid duplicate target.")
            duplicates[path] = target
    for source, target in duplicates.items():
        if target in duplicates:
            die(f"{filename}: duplicate observation {source!r} may not form a chain or cycle.")


def validate_record(record: dict, path: Path, global_sources: set[str]) -> None:
    """Check one record against the agent schema, then against its sources and claims."""
    filename = path.name
    errors = schema_errors(record, filename)
    if errors:
        die("\n".join(errors))
    if record["id"] != path.stem:
        die(f"{filename}: 'id' must match the filename stem.")
    local_sources: set[str] = set()
    for source in record["sources"]:
        validate_source(source, filename, local_sources)
        if source["id"] in global_sources:
            die(f"{filename}: source id {source['id']!r} is already used by another record.")
        global_sources.add(source["id"])
    first = record["first_public_evidence"]
    if first["source_id"] not in local_sources:
        die(f"{filename}: first public evidence must refer to a source in this record.")
    first_source = next(
        source for source in record["sources"] if source["id"] == first["source_id"]
    )
    if first_source.get("role", "evidence") != "evidence":
        die(f"{filename}: first public evidence must use a source with the evidence role.")
    validate_evidence(record, filename, local_sources)
    validate_page_content(record, filename, local_sources)
    metadata = record.get("claim_metadata") or {}
    for index, _ in enumerate(record["operating_models"]):
        claim_path = f"operating_models.{index}"
        values = metadata.get(claim_path) or {}
        for field in ("confidence", "confidence_reason", "valid_at"):
            if not values.get(field):
                die(f"{filename}: claim metadata for {claim_path!r} requires '{field}'.")
        if values.get("kind", "inference") != "inference":
            die(f"{filename}: {claim_path!r} must be an inference.")
        if values.get("provenance", "catalog-judgment") != "catalog-judgment":
            die(f"{filename}: {claim_path!r} must be a catalog judgment.")
    referenced_sources = {
        link["source_id"] for links in record["evidence"].values() for link in links
    }
    unused_evidence = sorted(
        source["id"]
        for source in record["sources"]
        if source.get("role", "evidence") == "evidence" and source["id"] not in referenced_sources
    )
    if unused_evidence:
        die(
            f"{filename}: evidence source(s) are not linked to a claim: {', '.join(unused_evidence)}"
        )


def load_agents() -> list[dict]:
    paths = sorted(AGENTS_DIR.glob("*.yaml"))
    if not paths:
        die(f"No YAML files found in {AGENTS_DIR.relative_to(ROOT)}.")
    records: list[dict] = []
    source_ids: set[str] = set()
    for path in paths:
        try:
            record = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
        except yaml.YAMLError as error:
            die(f"YAML parse error in {path.name}:\n    {error}")
        if not isinstance(record, dict):
            die(f"{path.name}: top-level YAML must be a mapping.")
        validate_record(record, path, source_ids)
        records.append(record)
    records.sort(key=lambda item: (item["company"].casefold(), item["agent_name"].casefold()))
    approach_ids = {record["id"] for record in records}
    for record in records:
        for relation in record.get("relationships") or []:
            if relation["approach_id"] not in approach_ids:
                die(
                    f"{record['id']}.yaml: relationship uses unknown approach {relation['approach_id']!r}."
                )
            if relation["approach_id"] == record["id"]:
                die(f"{record['id']}.yaml: an approach cannot relate to itself.")
    return records


def svg_logo_size(content: bytes, where: str) -> tuple[int, int]:
    """Check an SVG logo for unsafe markup and read the size of its viewBox."""
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        die(f"{where}: an SVG logo must be valid UTF-8.")
    lowered = text.lower()
    if "<!doctype" in lowered or "<!entity" in lowered:
        die(f"{where}: an SVG logo must not hold a DOCTYPE or ENTITY declaration.")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as error:
        die(f"{where}: the SVG logo does not parse: {error}")
    for element in root.iter():
        tag = element.tag.rsplit("}", 1)[-1] if isinstance(element.tag, str) else ""
        if tag.lower() in {"script", "foreignobject"}:
            die(f"{where}: an SVG logo must not hold a {tag} element.")
        for attribute, value in element.attrib.items():
            name = attribute.rsplit("}", 1)[-1]
            if name.startswith("on"):
                die(f"{where}: an SVG logo must not hold the '{name}' attribute.")
            if isinstance(value, str) and "javascript:" in value.lower():
                die(f"{where}: an SVG logo must not hold a 'javascript:' value.")
            if name == "href" and not value.startswith("#"):
                die(f"{where}: an SVG logo href must stay a local fragment, found {value!r}.")
    view_box = root.attrib.get("viewBox") or root.attrib.get("viewbox")
    if not isinstance(view_box, str) or not view_box.strip():
        die(f"{where}: an SVG logo needs a viewBox so the page can reserve its size.")
    parts = view_box.replace(",", " ").split()
    if len(parts) != 4:
        die(f"{where}: the SVG viewBox must hold four numbers.")
    try:
        width, height = float(parts[2]), float(parts[3])
    except ValueError:
        die(f"{where}: the SVG viewBox must hold four numbers.")
    if not (math.isfinite(width) and math.isfinite(height)) or width <= 0 or height <= 0:
        die(f"{where}: the SVG viewBox must describe a positive size.")
    return math.ceil(width), math.ceil(height)


def png_logo_size(content: bytes, where: str) -> tuple[int, int]:
    """Read the intrinsic pixel size of a PNG from its IHDR header."""
    if len(content) < 24 or not content.startswith(PNG_SIGNATURE) or content[12:16] != b"IHDR":
        die(f"{where}: the PNG logo header is not readable.")
    width, height = struct.unpack(">II", content[16:24])
    if width < MIN_PNG_LOGO_WIDTH:
        die(f"{where}: a PNG logo must be at least {MIN_PNG_LOGO_WIDTH} pixels wide.")
    return width, height


def read_logo_descriptor(company: dict, repository: Path) -> dict:
    """Read one registry logo asset, check it, and derive its published descriptor."""
    file_name = company["logo"]["file"]
    where = f"{LOGOS_DIR_NAME}/{file_name}"
    try:
        content = (repository / LOGOS_DIR_NAME / file_name).read_bytes()
    except OSError as error:
        die(f"{where}: could not read the logo asset: {error}")
    suffix = PurePosixPath(file_name).suffix
    if suffix == ".svg":
        width, height = svg_logo_size(content, where)
        limit = MAX_SVG_LOGO_BYTES
    else:
        width, height = png_logo_size(content, where)
        limit = MAX_PNG_LOGO_BYTES
    if len(content) > limit:
        die(f"{where}: the logo asset exceeds its limit of {limit // 1024} KiB.")
    return {
        "path": f"logos/{file_name}",
        "media_type": LOGO_MEDIA_TYPES[suffix],
        "width": width,
        "height": height,
        "bytes": len(content),
        "sha256": f"sha256:{hashlib.sha256(content).hexdigest()}",
        "source_url": company["logo"]["source_url"],
        "accessed_at": company["logo"]["accessed_at"],
    }


def load_companies(records: list[dict], *, root: Path | None = None) -> list[dict]:
    """Load data/companies.yaml and validate its records, its join, and its assets."""
    repository = root or ROOT
    registry_path = repository / COMPANIES_FILE_NAME
    if not registry_path.is_file():
        die(f"{COMPANIES_FILE_NAME}: the company registry is required.")
    try:
        registry = yaml.load(registry_path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except yaml.YAMLError as error:
        die(f"YAML parse error in {COMPANIES_FILE_NAME}:\n    {error}")
    if not isinstance(registry, list) or not registry:
        die(f"{COMPANIES_FILE_NAME}: must hold a non-empty list of company records.")
    seen_ids: set[str] = set()
    seen_names: set[str] = set()
    named_files: set[str] = set()
    for company in registry:
        require_exact_fields(
            company,
            COMPANY_REQUIRED_FIELDS,
            COMPANY_OPTIONAL_FIELDS,
            "company",
            COMPANIES_FILE_NAME,
        )
        company_id = company["id"]
        if not isinstance(company_id, str) or not ID_RE.fullmatch(company_id):
            die(f"{COMPANIES_FILE_NAME}: company id {company_id!r} must use kebab-case.")
        if company_id in seen_ids:
            die(f"{COMPANIES_FILE_NAME}: duplicate company id {company_id!r}.")
        seen_ids.add(company_id)
        name = company["name"]
        if not isinstance(name, str) or not name.strip():
            die(f"{COMPANIES_FILE_NAME}: company {company_id!r} needs a non-empty name.")
        if name in seen_names:
            die(f"{COMPANIES_FILE_NAME}: duplicate company name {name!r}.")
        seen_names.add(name)
        validate_https_url(
            company["homepage"], f"companies.{company_id}.homepage", COMPANIES_FILE_NAME
        )
        logo = company["logo"]
        if logo == "none":
            note = company.get("logo_note")
            if not isinstance(note, str) or not note.strip():
                die(
                    f"{COMPANIES_FILE_NAME}: companies.{company_id} uses 'logo: none' "
                    "and needs a logo_note."
                )
        elif isinstance(logo, dict):
            if "logo_note" in company:
                die(
                    f"{COMPANIES_FILE_NAME}: companies.{company_id} names a logo file "
                    "and also holds a logo_note."
                )
            descriptor = require_exact_fields(
                logo,
                COMPANY_LOGO_FIELDS,
                set(),
                f"companies.{company_id}.logo",
                COMPANIES_FILE_NAME,
            )
            validate_https_url(
                descriptor["source_url"],
                f"companies.{company_id}.logo.source_url",
                COMPANIES_FILE_NAME,
            )
            validate_date(
                descriptor["accessed_at"],
                f"companies.{company_id}.logo.accessed_at",
                COMPANIES_FILE_NAME,
            )
            file_name = descriptor["file"]
            pure = PurePosixPath(file_name) if isinstance(file_name, str) else None
            if (
                pure is None
                or len(pure.parts) != 1
                or pure.stem != company_id
                or pure.suffix not in LOGO_MEDIA_TYPES
            ):
                die(
                    f"{COMPANIES_FILE_NAME}: companies.{company_id}.logo.file must be "
                    f"'{company_id}.svg' or '{company_id}.png'."
                )
            named_files.add(file_name)
        else:
            die(
                f"{COMPANIES_FILE_NAME}: companies.{company_id}.logo must be a mapping "
                "or the value 'none'."
            )
    ids = [company["id"] for company in registry]
    if ids != sorted(ids):
        die(f"{COMPANIES_FILE_NAME}: company records must stay sorted by id.")
    approach_files: dict[str, str] = {}
    for record in records:
        approach_files.setdefault(record["company"], f"{record['id']}.yaml")
    for name in sorted(set(approach_files) - seen_names):
        die(f"{approach_files[name]}: company {name!r} has no record in {COMPANIES_FILE_NAME}.")
    for company in registry:
        if company["name"] not in approach_files:
            die(
                f"{COMPANIES_FILE_NAME}: company {company['id']!r} is not used "
                "by any approach record."
            )
    logos_dir = repository / LOGOS_DIR_NAME
    for company in registry:
        if company["logo"] == "none":
            continue
        if not (logos_dir / company["logo"]["file"]).is_file():
            die(
                f"{COMPANIES_FILE_NAME}: companies.{company['id']}.logo.file "
                f"{company['logo']['file']!r} is missing from {LOGOS_DIR_NAME}/."
            )
    if logos_dir.is_dir():
        strays = sorted(
            str(path.name) for path in logos_dir.iterdir() if path.name not in named_files
        )
        if strays:
            die(f"{LOGOS_DIR_NAME}/ holds files the registry does not name: {', '.join(strays)}")
    # Reading every asset here validates its size, its safety, and its usable size.
    normalize_companies(registry, root=repository)
    return registry


def normalize_companies(registry: list[dict], *, root: Path | None = None) -> list[dict]:
    """Derive the published company collection, checking every logo asset."""
    repository = root or ROOT
    companies = []
    for company in registry:
        descriptor = (
            None if company["logo"] == "none" else read_logo_descriptor(company, repository)
        )
        companies.append(
            {
                "id": company["id"],
                "name": company["name"],
                "homepage": company["homepage"],
                "logo": descriptor,
            }
        )
    return companies


def markdown(value: Any) -> str:
    if value is None or value == "" or value == []:
        return "Unknown"
    if isinstance(value, list):
        value = ", ".join(str(item) for item in value)
    return str(value).replace("|", "\\|").replace("\n", " ")


def anchor(record: dict) -> str:
    return record["id"]


def operating_model_summary(record: dict) -> str:
    """Render each derived level together with its required workflow scope."""
    summaries = []
    for item in record["operating_models"]:
        level = BOUNDARY_LEVELS[item["attention_boundary"]]
        label = f"L{level}" if level is not None else "Unknown"
        summaries.append(f"{label} · {item['scope']}")
    return "<br>".join(summaries)


def evidence_refs(record: dict, path: str) -> str:
    """Render compact claim-to-source links for the catalog."""
    links = record["evidence"].get(path, [])
    if not links:
        return ""
    grouped: dict[str, list[str]] = {}
    for link in links:
        relation = link.get("relation", "supports")
        grouped.setdefault(relation, []).append(link["source_id"])
    parts = []
    labels = {"supports": "Sources", "contradicts": "Conflicting", "contextualizes": "Context"}
    for relation in ("supports", "contradicts", "contextualizes"):
        ids = grouped.get(relation, [])
        if ids:
            refs = ", ".join(f"[{source_id}](#{source_id})" for source_id in ids)
            parts.append(f"{labels[relation]}: {refs}")
    return " <small>" + "; ".join(parts) + ".</small>"


def render_source_reference(source: dict) -> str:
    """Render the original citation and any verified preserved copies together."""
    original = f"[{source['title']}]({source['url']})"
    fallbacks = []
    manifest = load_capture_manifest(source, "catalog source rendering")
    if manifest is not None:
        snapshot_path = manifest["artifacts"]["markdown"]["path"]
        fallbacks.append(f"[snapshot](../{snapshot_path})")
        pdf = manifest["artifacts"].get("pdf")
        if pdf is not None:
            fallbacks.append(f"[PDF](../{pdf['path']})")
    if source.get("archived_url"):
        fallbacks.append(f"[Wayback]({source['archived_url']})")
    if manifest is not None:
        fallbacks.append(f"captured {manifest['captured_at'][:10]}")
    if not fallbacks:
        return original
    return f"{original} ({', '.join(fallbacks)})"


def render_comparison_table(records: list[dict]) -> str:
    lines = [TABLE_HEADER]
    for record in records:
        link = f"[{markdown(record['agent_name'])}](#{anchor(record)})"
        lines.append(
            "| {company} | {approach} | {kind} | {domains} | {level} | {autonomy} | {stage} | {status} | {year} |".format(
                company=markdown(record["company"]),
                approach=link,
                kind=markdown(record["approach_type"]),
                domains=markdown(record["domains"]),
                level=markdown(operating_model_summary(record)),
                autonomy=markdown(record["autonomy"]),
                stage=markdown(record["deployment_stage"]),
                status=markdown(record["status"]),
                year=record["year"],
            )
        )
    return "\n".join(lines)


def render_overview_table(records: list[dict]) -> str:
    lines = [OVERVIEW_TABLE_HEADER]
    for record in records:
        link = f"[{markdown(record['agent_name'])}](docs/landscape.md#{anchor(record)})"
        lines.append(
            "| {organization} | {approach} | {kind} | {work} |".format(
                organization=markdown(record["company"]),
                approach=link,
                kind=markdown(record["approach_type"]),
                work=markdown(record["domains"]),
            )
        )
    return "\n".join(lines)


def catalog_section(approach_type: str) -> str:
    """Derive collection identity from the audited structural type."""
    if approach_type in {"agent", "agent-system"}:
        return "agents"
    if approach_type in {"platform", "supporting-pattern", "orchestration-system"}:
        return "infrastructure"
    die(f"Unknown approach type: {approach_type!r}")


def render_overview(records: list[dict], export: dict) -> str:
    agents = [record for record in records if catalog_section(record["approach_type"]) == "agents"]
    infrastructure = [
        record for record in records if catalog_section(record["approach_type"]) == "infrastructure"
    ]
    company_count = len({record["company"] for record in agents})
    summary = (
        f"**Current map: {len(agents)} agents across {company_count} organizations, "
        f"plus {len(infrastructure)} infrastructure records. The complete catalog is "
        f"backed by {len({source.get('canonical_url', source['url']) for source in export['sources']})} distinct sources and "
        f"{len(export['claims'])} evidence-linked claims.**"
    )
    return "\n".join(
        [
            OVERVIEW_BEGIN,
            "",
            summary,
            "",
            "## Agents",
            "",
            render_overview_table(agents),
            "",
            "## Infrastructure",
            "",
            render_overview_table(infrastructure),
            "",
            OVERVIEW_END,
        ]
    )


def count_table(counts: Counter[str], labels: dict[str, str]) -> str:
    lines = ["| Type | Count |", "| --- | ---: |"]
    lines.extend(f"| {label} | {counts[value]} |" for value, label in labels.items())
    return "\n".join(lines)


def documented_environment(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    return not re.match(
        r"^(?:unknown|n/a|not (?:specified|detailed|documented|applicable))(?:\b|$)",
        value.strip(),
        flags=re.IGNORECASE,
    )


def catalog_statistics(records: list[dict]) -> dict[str, Any]:
    """Return the shared entry and scoped-workflow counts used by generated summaries."""
    agents = [record for record in records if catalog_section(record["approach_type"]) == "agents"]
    operating_models = [model for record in agents for model in record["operating_models"]]
    return {
        "entries": len(records),
        "agents": len(agents),
        "approach_types": Counter(record["approach_type"] for record in records),
        "autonomy": Counter(record["autonomy"] for record in agents),
        "state": Counter(record["rubric"]["state"] for record in records),
        "attention_boundaries": Counter(model["attention_boundary"] for model in operating_models),
        "operating_models": len(operating_models),
        "multi_workflow_entries": sum(len(record["operating_models"]) > 1 for record in agents),
        "supporting_entries": sum(
            catalog_section(record["approach_type"]) == "infrastructure" for record in records
        ),
        "slack": sum(
            "slack" in ((record.get("architecture") or {}).get("interfaces") or [])
            for record in records
        ),
        "sandbox": sum(
            documented_environment((record.get("architecture") or {}).get("sandbox"))
            for record in records
        ),
    }


def render_readme_findings(records: list[dict]) -> str:
    stats = catalog_statistics(records)
    autonomy = stats["autonomy"]
    boundaries = stats["attention_boundaries"]
    return "\n".join(
        [
            README_FINDINGS_BEGIN,
            "",
            "## What the current map shows",
            "",
            f"These counts classify {stats['entries']} catalog entries. A platform and one of its "
            "components can both appear, so the entries are not independent deployments, shares "
            "of industry practice, or counts of successful runs.",
            "",
            f"Agent autonomy ({stats['agents']} records; infrastructure excluded) is classified as "
            f"{autonomy['drafts-reviewed']} drafts-reviewed, "
            f"{autonomy['human-in-loop']} human-in-loop, "
            f"{autonomy['autonomous']} autonomous, {autonomy['assistive']} assistive, and "
            f"{autonomy['unknown']} unknown. Human-in-loop includes approval checkpoints; it does "
            "not mean a person continuously steers the whole run.",
            "",
            f"The catalog contains {stats['operating_models']} scoped supervision assessments "
            f"across those entries, including {boundaries['continuous-steering']} continuous-steering, "
            f"{boundaries['work-product-review']} work-product-review, "
            f"{boundaries['outcome-review']} outcome-review, {boundaries['exception-only']} "
            f"exception-only, and {boundaries['unknown']} unknown assessments. "
            f"{stats['multi_workflow_entries']} entries have more than one assessed workflow; the "
            "counts therefore do not assign one level to each company.",
            "",
            f"{stats['supporting_entries']} entries are platforms or supporting patterns. State "
            f"duration is undocumented for {stats['state']['unknown']} entries. Review cost, failure "
            "rates, and retired systems remain rarely reported.",
            "",
            README_FINDINGS_END,
        ]
    )


def render_patterns_snapshot(records: list[dict]) -> str:
    approach_labels = {
        "agent": "Agent",
        "platform": "Platform",
        "agent-system": "Agent family",
        "orchestration-system": "Orchestration system",
        "supporting-pattern": "Supporting pattern",
    }
    stats = catalog_statistics(records)
    approach_counts = stats["approach_types"]
    autonomy_counts = stats["autonomy"]
    state_counts = stats["state"]
    return "\n".join(
        [
            PATTERNS_SNAPSHOT_BEGIN,
            "",
            "## Catalog snapshot",
            "",
            f"The catalog currently contains {stats['entries']} entries. These are catalog "
            "classifications, not independent deployments or industry shares:",
            "",
            count_table(approach_counts, approach_labels),
            "",
            f"- {stats['sandbox']} entries document a concrete execution environment.",
            f"- {stats['slack']} entries list Slack as an interface.",
            "- State duration is "
            f"unknown for {state_counts['unknown']}, durable-session for "
            f"{state_counts['durable-session']}, cross-session-memory for "
            f"{state_counts['cross-session-memory']}, mixed for {state_counts['mixed']}, "
            f"and run-only for {state_counts['run-only']} approaches.",
            f"- Agent autonomy ({stats['agents']} records; infrastructure excluded) is classified as "
            f"drafts-reviewed for {autonomy_counts['drafts-reviewed']}, human-in-loop for "
            f"{autonomy_counts['human-in-loop']}, autonomous for "
            f"{autonomy_counts['autonomous']}, assistive for {autonomy_counts['assistive']}, "
            f"and unknown for {autonomy_counts['unknown']} approaches.",
            "",
            PATTERNS_SNAPSHOT_END,
        ]
    )


def render_adoption_snapshot(records: list[dict]) -> str:
    stats = catalog_statistics(records)
    autonomy_counts = stats["autonomy"]
    return "\n".join(
        [
            ADOPTION_SNAPSHOT_BEGIN,
            "",
            "## Catalog snapshot",
            "",
            f"These observations draw on {stats['entries']} catalog entries. The entry is the "
            "counting unit; platforms and components can both appear. The evidence is uneven, "
            "and most sources are company reports.",
            "",
            f"{stats['slack']} entries list Slack as an interface. Agent autonomy, excluding infrastructure, is "
            f"{autonomy_counts['drafts-reviewed']} `drafts-reviewed`, "
            f"{autonomy_counts['human-in-loop']} `human-in-loop`, "
            f"{autonomy_counts['autonomous']} `autonomous`, "
            f"{autonomy_counts['assistive']} `assistive`, and "
            f"{autonomy_counts['unknown']} `unknown`.",
            "",
            ADOPTION_SNAPSHOT_END,
        ]
    )


def render_landscape(records: list[dict]) -> str:
    out = [
        "# Internal agents: full catalog",
        "",
        "<!-- Generated by scripts/build.py. Edit data/agents/*.yaml instead. -->",
        "",
        f"The catalog contains {len(records)} approaches. Company names determine the sort order.",
        "",
        "The L2-L5 labels adapt [Dan Shapiro's five levels of AI-assisted software development](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/) into scoped human-attention boundaries: **L2** continuous steering, **L3** work-product review, **L4** outcome review, and **L5** exception-only supervision. Each label applies only to the workflow shown; it is a catalog judgment, not a company maturity score.",
        "",
        "## Agent comparison",
        "",
        render_comparison_table(
            [record for record in records if catalog_section(record["approach_type"]) == "agents"]
        ),
        "",
        "## Infrastructure",
        "",
        "These records describe reusable systems, not equivalent agent deployments.",
        "",
        "\n".join(
            [
                "| Organization | Infrastructure | Type | Work supported |",
                "| --- | --- | --- | --- |",
                *[
                    f"| {markdown(record['company'])} | [{markdown(record['agent_name'])}](#{anchor(record)}) | {record['approach_type']} | {markdown(record['domains'])} |"
                    for record in records
                    if catalog_section(record["approach_type"]) == "infrastructure"
                ],
            ]
        ),
        "",
    ]
    out.extend(
        [
            "## Terms and rubric",
            "",
            "Common terms include artificial intelligence (AI), application programming interface (API), continuous integration (CI), and command-line interface (CLI).",
            "Other terms include large language model (LLM), Model Context Protocol (MCP), pull request (PR), and software development kit (SDK).",
            "Access terms include attribute-based access control (ABAC), role-based access control (RBAC), and single sign-on (SSO).",
            "Domain terms include know your customer (KYC), quality assurance (QA), security operations center (SOC), and structured query language (SQL).",
            "",
            "The [schema reference](../data/schema.md) defines each comparison field. Unknown means that the collected sources do not document the value.",
            "Operating levels are generated from scoped, evidence-backed human-attention boundaries; they are catalog judgments, not company-wide maturity scores.",
            "",
        ]
    )
    for record in records:
        rubric = record["rubric"]
        out.extend(
            [
                f'<a id="{anchor(record)}"></a>',
                "",
                f"## {record['company']}: {record['agent_name']}",
                "",
                f"> {record['summary']}{evidence_refs(record, 'summary')}",
                "",
                "| Field | Value |",
                "| --- | --- |",
                f"| Collection | {catalog_section(record['approach_type'])} |",
                f"| Approach type | {markdown(record['approach_type'])} |",
                f"| First public evidence | {markdown(record['first_public_evidence']['date'])} |",
                f"| Deployment stage | {markdown(record['deployment_stage'])} |",
                f"| Availability | {markdown(record['status'])} |",
                f"| Domains | {markdown(record['domains'])} |",
                f"| Operating model | {markdown(operating_model_summary(record))} |",
                f"| Autonomy | {markdown(record['autonomy'])} |",
                f"| Invocation | {markdown(rubric['invocation'])} |",
                f"| State | {markdown(rubric['state'])} |",
                f"| Identity | {markdown(rubric['identity'])} |",
                f"| Evidence | {markdown(rubric['evidence_strength'])} |",
            ]
        )
        if record.get("headline_metric"):
            out.append(
                f"| Headline metric | {markdown(record['headline_metric'])}"
                f"{evidence_refs(record, 'headline_metric')} |"
            )
        if record.get("relationships"):
            related = ", ".join(
                f"{relation['type']}: [{relation['approach_id']}](#{relation['approach_id']})"
                for relation in record["relationships"]
            )
            out.append(f"| Relationships | {related} |")
        out.append("")
        out.extend(["### Operating model", ""])
        for index, item in enumerate(record["operating_models"]):
            path = f"operating_models.{index}"
            level = BOUNDARY_LEVELS[item["attention_boundary"]]
            label = f"Level {level}" if level is not None else "Unclassified"
            meta = (record.get("claim_metadata") or {}).get(path, {})
            out.append(
                f"- **{label} · {item['attention_boundary']}** — {item['scope']} "
                f"({meta['confidence']} confidence; {meta['valid_at']})"
                f"{evidence_refs(record, path)}"
            )
        out.append("")
        architecture = record.get("architecture") or {}
        if architecture:
            out.extend(["### Architecture", ""])
            for key, value in architecture.items():
                if value not in (None, "", []):
                    out.append(
                        f"- {key.replace('_', ' ').capitalize()}: {markdown(value)}"
                        f"{evidence_refs(record, f'architecture.{key}')}"
                    )
            out.append("")
        for field, heading in (
            ("primitives", "Primitives"),
            ("key_metrics", "Reported metrics"),
            ("lessons_learned", "Catalog observations"),
        ):
            values = record.get(field) or []
            if not values:
                continue
            out.extend([f"### {heading}", ""])
            for index, value in enumerate(values):
                if isinstance(value, dict):
                    text = f"{value['name']}: {value.get('desc', '')}".rstrip()
                else:
                    text = value
                out.append(f"- {text}{evidence_refs(record, f'{field}.{index}')}")
            out.append("")
        out.extend(["### Sources", ""])
        for source in record["sources"]:
            detail = (
                f"{source['kind']}; {source['provenance_class']}; {source.get('role', 'evidence')}"
            )
            out.append(f'- <a id="{source["id"]}"></a>{render_source_reference(source)} ({detail})')
        out.extend(["", f"Last reviewed: {record['last_reviewed_at']}.", "", "---", ""])
    return "\n".join(out)


def normalize(records: list[dict], companies: list[dict]) -> dict:
    approaches = []
    claims = []
    sources = []
    company_ids = {company["name"]: company["id"] for company in companies}
    for record in records:
        claim_value_fields = {
            "summary",
            "headline_metric",
            "architecture",
            "primitives",
            "key_metrics",
            "lessons_learned",
        }
        approach = {
            key: value
            for key, value in record.items()
            if key not in {"sources", "evidence", "claim_metadata"} | claim_value_fields
        }
        approach["company_id"] = company_ids[record["company"]]
        approach["operating_models"] = [
            {**item, "level": BOUNDARY_LEVELS[item["attention_boundary"]]}
            for item in record["operating_models"]
        ]
        approach["catalog_section"] = catalog_section(record["approach_type"])
        approach["claim_ids"] = []
        approach["source_ids"] = [source["id"] for source in record["sources"]]
        approach["interfaces"] = (record.get("architecture") or {}).get("interfaces", [])
        source_index = {source["id"]: source for source in record["sources"]}
        for path, (claim_text, default_kind, default_provenance) in claim_fields(record).items():
            claim_id = f"{record['id']}--{path.replace('.', '-').replace('_', '-')}"
            meta = (record.get("claim_metadata") or {}).get(path, {})
            links = record["evidence"][path]
            supporting_sources = [
                source_index[link["source_id"]]
                for link in links
                if link.get("relation", "supports") == "supports"
            ]
            classes = {source["provenance_class"] for source in supporting_sources}
            default_confidence = (
                "high"
                if "first-party" in classes
                else (
                    "medium" if classes & {"direct-participant", "independent-secondary"} else "low"
                )
            )
            default_reason = {
                "high": "A linked first-party source states the claim.",
                "medium": "A linked participant or independent source reports the claim.",
                "low": "Only community or aggregate evidence supports the claim.",
            }[default_confidence]
            claim = {
                "id": claim_id,
                "approach_id": record["id"],
                "field": path,
                "text": claim_text,
                "kind": meta.get("kind", default_kind),
                "provenance": meta.get("provenance", default_provenance),
                "confidence": meta.get("confidence", default_confidence),
                "confidence_reason": meta.get("confidence_reason", default_reason),
                "valid_at": meta.get("valid_at"),
                "evidence": links,
            }
            if path.startswith("primitives."):
                item = record["primitives"][int(path.split(".")[1])]
                claim["display_name"] = item["name"]
            if claim["kind"] == "metric" and claim["provenance"] == "reported":
                claim["reported_by"] = meta.get("reported_by", record["company"])
            for field in ("value", "unit", "metric_scope", "denominator", "measurement_method"):
                if meta.get(field) is not None:
                    claim[field] = meta[field]
            claims.append(claim)
            approach["claim_ids"].append(claim_id)
        approaches.append(approach)
        for source in record["sources"]:
            normalized_source = {
                **source,
                "role": source.get("role", "evidence"),
                "approach_id": record["id"],
            }
            manifest = load_capture_manifest(source, f"{record['id']}.yaml")
            if manifest is not None:
                normalized_source["capture"] = manifest
            sources.append(normalized_source)
    return {
        "schema_version": 7,
        "approaches": approaches,
        "claims": claims,
        "sources": sources,
        "companies": normalize_companies(companies),
    }


def replace_between_markers(
    text: str, begin: str, end_marker: str, block: str, filename: str
) -> str:
    start = text.find(begin)
    end = text.find(end_marker)
    if text.count(begin) != 1 or text.count(end_marker) != 1 or end < start:
        die(f"{filename} must contain exactly one ordered {begin} and {end_marker} marker pair.")
    return text[:start] + block + text[end + len(end_marker) :]


def render_schema_values() -> str:
    """Give the TypeScript value list and type of every enum definition in the agent schema."""
    lines = [
        "// ABOUTME: Lists the allowed values of each enum definition in data/agent.schema.json.",
        "// ABOUTME: scripts/build.py generates this file. Do not edit it by hand.",
        "",
    ]
    for name, definition in AGENT_SCHEMA["definitions"].items():
        if "enum" not in definition:
            continue
        constant = re.sub(r"(?<!^)(?=[A-Z])", "_", name).upper() + "_VALUES"
        values = ", ".join(f"'{value}'" for value in definition["enum"])
        lines += [
            f"export const {constant} = [{values}] as const;",
            f"export type {name[0].upper() + name[1:]} = (typeof {constant})[number];",
            "",
        ]
    return "\n".join(lines).rstrip("\n") + "\n"


def data_outputs(records: list[dict], catalog: dict) -> dict[Path, str | bytes]:
    """Give the normalized catalog and the generated repository documents."""
    readme = README.read_text(encoding="utf-8")
    patterns = PATTERNS.read_text(encoding="utf-8")
    adoption_lessons = ADOPTION_LESSONS.read_text(encoding="utf-8")
    return {
        README: replace_between_markers(
            replace_between_markers(
                readme,
                OVERVIEW_BEGIN,
                OVERVIEW_END,
                render_overview(records, catalog),
                "README.md",
            ),
            README_FINDINGS_BEGIN,
            README_FINDINGS_END,
            render_readme_findings(records),
            "README.md",
        ),
        PATTERNS: replace_between_markers(
            patterns,
            PATTERNS_SNAPSHOT_BEGIN,
            PATTERNS_SNAPSHOT_END,
            render_patterns_snapshot(records),
            "docs/patterns.md",
        ),
        ADOPTION_LESSONS: replace_between_markers(
            adoption_lessons,
            ADOPTION_SNAPSHOT_BEGIN,
            ADOPTION_SNAPSHOT_END,
            render_adoption_snapshot(records),
            "docs/adoption-lessons.md",
        ),
        LANDSCAPE: render_landscape(records),
        DATA_JSON: json.dumps(catalog, indent=2, ensure_ascii=False) + "\n",
        SCHEMA_VALUES_TS: render_schema_values(),
    }


def write_outputs(outputs: dict[Path, str | bytes]) -> None:
    staged: list[tuple[Path, Path]] = []
    try:
        for path, content in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
            temporary_path = Path(temporary)
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(content.encode("utf-8") if isinstance(content, str) else content)
                stream.flush()
                os.fsync(stream.fileno())
            staged.append((temporary_path, path))
        for temporary_path, path in staged:
            os.replace(temporary_path, path)
            print(f"wrote {path.relative_to(ROOT)}")
    finally:
        for temporary_path, _ in staged:
            temporary_path.unlink(missing_ok=True)


def company_summary(registry: list[dict]) -> str:
    """State the logo coverage, so the remaining asset work stays visible."""
    logos = sum(1 for company in registry if company["logo"] != "none")
    return f"{len(registry)} organizations, {logos} logos, {len(registry) - logos} monograms"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale.")
    args = parser.parse_args()
    records = load_agents()
    companies = load_companies(records)
    outputs = data_outputs(records, normalize(records, companies))
    stale = [
        path
        for path, content in outputs.items()
        if not path.exists()
        or path.read_bytes() != (content.encode("utf-8") if isinstance(content, str) else content)
    ]
    if args.check:
        if stale:
            die(
                "Generated files are stale: "
                + ", ".join(str(path.relative_to(ROOT)) for path in stale)
            )
        print(
            f"Validated {len(records)} approaches, {company_summary(companies)}. "
            "Generated files are current."
        )
        return
    write_outputs(outputs)
    print(f"\n{len(records)} approaches, {company_summary(companies)}. Build complete.")


if __name__ == "__main__":
    main()
