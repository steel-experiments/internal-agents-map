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
except ImportError:
    sys.exit("PyYAML is required. Install project dependencies with 'uv sync'.")

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

REQUIRED = {
    "id",
    "company",
    "agent_name",
    "approach_type",
    "deployment_stage",
    "year",
    "first_public_evidence",
    "last_reviewed_at",
    "status",
    "domains",
    "autonomy",
    "operating_models",
    "summary",
    "rubric",
    "sources",
    "evidence",
}
ALLOWED_TOP_LEVEL = REQUIRED | {
    "headline_metric",
    "architecture",
    "primitives",
    "key_metrics",
    "lessons_learned",
    "claim_metadata",
    "aliases",
    "family_id",
    "relationships",
    "page_content",
}
ARCHITECTURE_FIELDS = {
    "sandbox",
    "harness",
    "model",
    "tool_access",
    "interfaces",
    "knowledge",
    "credentials",
    "context_mgmt",
}
PAGE_QUESTIONS = {
    "purpose",
    "workflow",
    "human_involvement",
    "implementation",
    "validation",
    "observations",
    "lessons",
}
REVIEW_STATES = {"reported", "unreported", "not-applicable", "not-reviewed"}
PRIMITIVE_ROLES = {"workflow", "mechanism", "validation"}
OBSERVATION_CATEGORIES = {
    "effectiveness",
    "adoption-output",
    "cost-latency",
    "implementation-scale",
    "runtime-capacity",
}
OBSERVATION_BASES = {"reported-measurement", "qualitative", "estimate", "target"}
SOURCE_FIELDS = {
    "id",
    "title",
    "url",
    "canonical_url",
    "kind",
    "provenance_class",
    "role",
    "publisher",
    "authors",
    "published_at",
    "accessed_at",
    "last_verified_at",
    "archived_url",
    "capture",
    "duplicate_of",
}
CLAIM_METADATA_FIELDS = {
    "kind",
    "provenance",
    "confidence",
    "confidence_reason",
    "valid_at",
    "value",
    "unit",
    "reported_by",
    "metric_scope",
    "denominator",
    "measurement_method",
}
AUTONOMY = {"assistive", "human-in-loop", "drafts-reviewed", "autonomous", "unknown"}
STATUS = {"internal", "open-sourced", "commercialized", "mixed"}
APPROACH_TYPES = {
    "agent",
    "agent-system",
    "platform",
    "orchestration-system",
    "supporting-pattern",
}
DEPLOYMENT_STAGES = {"research", "prototype", "pilot", "deployed", "scaled", "unknown"}
INVOCATION = {"interactive", "background", "scheduled", "event-driven", "unknown"}
STATE = {"run-only", "durable-session", "cross-session-memory", "mixed", "unknown"}
IDENTITY = {"user", "dedicated-agent", "service", "mixed", "unknown"}
EVIDENCE_STRENGTH = {"detailed-primary", "limited-primary", "secondary-only", "mixed", "unknown"}
SOURCE_KINDS = {
    "engineering-blog",
    "corporate-article",
    "documentation",
    "source-code",
    "repository",
    "release",
    "social-post",
    "talk",
    "transcript",
    "podcast",
    "paper",
    "case-study",
    "news",
    "hn-thread",
    "hn-comment",
    "forum",
    "other",
}
PROVENANCE_CLASSES = {
    "first-party",
    "direct-participant",
    "independent-secondary",
    "community",
    "aggregator",
}
SOURCE_ROLES = {"evidence", "commentary", "discovery"}
CLAIM_KINDS = {"fact", "metric", "inference", "opinion"}
CLAIM_PROVENANCE = {"reported", "observed", "inferred", "catalog-judgment"}
CONFIDENCE = {"high", "medium", "low", "unverified"}
ATTENTION_BOUNDARIES = {
    "continuous-steering",
    "work-product-review",
    "outcome-review",
    "exception-only",
    "unknown",
}
BOUNDARY_LEVELS = {
    "continuous-steering": 2,
    "work-product-review": 3,
    "outcome-review": 4,
    "exception-only": 5,
    "unknown": None,
}
EVIDENCE_RELATIONS = {"supports", "contradicts", "contextualizes"}
RELATION_TYPES = {"component-of", "built-on", "successor-of", "related-to"}
DOMAIN_VALUES = {
    "coding",
    "code-review",
    "support",
    "on-call",
    "research",
    "customer-success",
    "security",
    "finance-ops",
    "data",
    "ci-triage",
    "maintenance",
    "ops",
    "recruitment",
    "migrations",
    "design",
}
INTERFACE_VALUES = {
    "slack",
    "github",
    "web",
    "cli",
    "linear",
    "chrome-extension",
    "webhook",
    "desktop",
    "scheduled",
    "skill",
    "cursor",
    "api",
    "automation",
    "ci",
    "intercom",
    "jira",
    "internal-ui",
    "mobile",
    "monday",
}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}(?:-(?:0[1-9]|1[0-2])(?:-(?:0[1-9]|[12]\d|3[01]))?)?$")
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


def require_string(record: dict, field: str, filename: str) -> None:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        die(f"{filename}: '{field}' must be a non-empty string.")


def require_string_list(value: Any, field: str, filename: str, *, nonempty: bool = True) -> None:
    if not isinstance(value, list) or (nonempty and not value):
        die(f"{filename}: '{field}' must be a{' non-empty' if nonempty else ''} list.")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        die(f"{filename}: every '{field}' value must be a non-empty string.")


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
    if tool["name"] not in ("steel", "steel-python-sdk"):
        die(f"{filename}: capture manifest tool name must be 'steel' or 'steel-python-sdk'.")
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


def validate_source(source: Any, filename: str, seen: set[str]) -> None:
    if not isinstance(source, dict):
        die(f"{filename}: every source must be a mapping.")
    unexpected = sorted(set(source) - SOURCE_FIELDS)
    if unexpected:
        die(f"{filename}: source contains unexpected field(s): {', '.join(unexpected)}")
    for field in (
        "id",
        "title",
        "url",
        "canonical_url",
        "kind",
        "provenance_class",
        "accessed_at",
        "last_verified_at",
    ):
        require_string(source, field, filename)
    source_id = source["id"]
    if not ID_RE.fullmatch(source_id):
        die(f"{filename}: source id {source_id!r} must use kebab-case.")
    if source_id in seen:
        die(f"{filename}: duplicate source id {source_id!r}.")
    seen.add(source_id)
    if not source["url"].startswith("https://"):
        die(f"{filename}: source {source_id!r} must use an HTTPS URL.")
    if not source["canonical_url"].startswith("https://"):
        die(f"{filename}: source {source_id!r} canonical URL must use HTTPS.")
    if "archived_url" in source:
        validate_https_url(source["archived_url"], f"sources.{source_id}.archived_url", filename)
    if source["kind"] not in SOURCE_KINDS:
        die(f"{filename}: source {source_id!r} has invalid kind {source['kind']!r}.")
    if source["provenance_class"] not in PROVENANCE_CLASSES:
        die(f"{filename}: source {source_id!r} has invalid provenance class.")
    if source.get("role", "evidence") not in SOURCE_ROLES:
        die(f"{filename}: source {source_id!r} has invalid role {source.get('role')!r}.")
    for field in ("published_at", "accessed_at", "last_verified_at"):
        if source.get(field):
            validate_date(source[field], f"sources.{source_id}.{field}", filename)
    if source.get("authors") is not None:
        require_string_list(source["authors"], f"sources.{source_id}.authors", filename)
    load_capture_manifest(source, filename)


def validate_evidence(record: dict, filename: str, source_ids: set[str]) -> None:
    evidence = record["evidence"]
    if not isinstance(evidence, dict):
        die(f"{filename}: 'evidence' must be a mapping from claim paths to source links.")
    claims = claim_fields(record)
    missing = sorted(set(claims) - set(evidence))
    extra = sorted(set(evidence) - set(claims))
    if missing:
        die(f"{filename}: missing evidence for claim(s): {', '.join(missing)}")
    if extra:
        die(f"{filename}: evidence refers to unknown claim(s): {', '.join(extra)}")
    for path, links in evidence.items():
        if not isinstance(links, list) or not links:
            die(f"{filename}: evidence for {path!r} must be a non-empty list.")
        for link in links:
            if not isinstance(link, dict) or not isinstance(link.get("source_id"), str):
                die(f"{filename}: evidence for {path!r} must contain source mappings.")
            if link["source_id"] not in source_ids:
                die(f"{filename}: evidence for {path!r} uses unknown source {link['source_id']!r}.")
            relation = link.get("relation", "supports")
            if relation not in EVIDENCE_RELATIONS:
                die(f"{filename}: evidence for {path!r} has invalid relation {relation!r}.")
    metadata = record.get("claim_metadata") or {}
    if not isinstance(metadata, dict):
        die(f"{filename}: 'claim_metadata' must be a mapping.")
    for path, values in metadata.items():
        if path not in claims or not isinstance(values, dict):
            die(f"{filename}: invalid claim metadata path {path!r}.")
        unexpected = sorted(set(values) - CLAIM_METADATA_FIELDS)
        if unexpected:
            die(
                f"{filename}: claim metadata for {path!r} contains unexpected field(s): {', '.join(unexpected)}"
            )
        if values.get("kind") and values["kind"] not in CLAIM_KINDS:
            die(f"{filename}: invalid claim kind for {path!r}.")
        if values.get("provenance") and values["provenance"] not in CLAIM_PROVENANCE:
            die(f"{filename}: invalid claim provenance for {path!r}.")
        if values.get("confidence") and values["confidence"] not in CONFIDENCE:
            die(f"{filename}: invalid claim confidence for {path!r}.")
        if values.get("valid_at"):
            validate_date(values["valid_at"], f"claim_metadata.{path}.valid_at", filename)
        for field in ("reported_by", "metric_scope", "denominator", "measurement_method", "unit"):
            if values.get(field) is not None and not isinstance(values[field], str):
                die(f"{filename}: claim metadata '{field}' for {path!r} must be a string.")
        if values.get("value") is not None and not isinstance(values["value"], (int, float, str)):
            die(f"{filename}: claim metadata 'value' for {path!r} must be a number or string.")


def validate_page_content(record: dict, filename: str, source_ids: set[str]) -> None:
    """Validate the optional editorial coverage contract against this record's claims."""
    page = record.get("page_content")
    if page is None:
        return
    page = require_exact_fields(
        page,
        {
            "version",
            "reviewed_at",
            "source_ids",
            "questions",
            "implementation_fields",
            "primitive_roles",
            "observations",
        },
        {"workflow_scope"},
        "page_content",
        filename,
    )
    if page["version"] != 1:
        die(f"{filename}: page_content.version must be 1.")
    if not isinstance(page["reviewed_at"], str) or len(page["reviewed_at"]) != 10:
        die(f"{filename}: page_content.reviewed_at must use YYYY-MM-DD.")
    validate_date(page["reviewed_at"], "page_content.reviewed_at", filename)
    require_string_list(page["source_ids"], "page_content.source_ids", filename)
    reviewed = set(page["source_ids"])
    if len(reviewed) != len(page["source_ids"]) or reviewed - source_ids:
        die(f"{filename}: page_content.source_ids must be unique sources belonging to this entry.")
    claims = claim_fields(record)

    def disposition(
        value: Any,
        field: str,
        allowed_paths: set[str] | None = None,
        bare_unreported: bool = False,
    ) -> dict:
        value = require_exact_fields(value, {"state", "claim_paths"}, {"note"}, field, filename)
        if value["state"] not in REVIEW_STATES:
            die(f"{filename}: {field}.state is invalid.")
        require_string_list(value["claim_paths"], f"{field}.claim_paths", filename, nonempty=False)
        paths = value["claim_paths"]
        if len(paths) != len(set(paths)) or any(path not in claims for path in paths):
            die(f"{filename}: {field}.claim_paths contains a duplicate or unknown claim path.")
        if allowed_paths is not None and set(paths) - allowed_paths:
            die(f"{filename}: {field}.claim_paths contains a claim outside its allowed field.")
        note = value.get("note")
        if note is not None and (not isinstance(note, str) or not note.strip()):
            die(f"{filename}: {field}.note must be a non-empty string when present.")
        if value["state"] == "reported":
            if not paths:
                die(f"{filename}: {field} reported state requires claim_paths.")
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
        elif paths:
            die(f"{filename}: {field} {value['state']} state requires empty claim_paths.")
        elif not note and not (bare_unreported and value["state"] == "unreported"):
            die(f"{filename}: {field} {value['state']} state requires a note.")
        return value

    questions = page["questions"]
    if not isinstance(questions, dict) or set(questions) != PAGE_QUESTIONS:
        die(f"{filename}: page_content.questions must contain exactly the seven reader questions.")
    for key, value in questions.items():
        disposition(value, f"page_content.questions.{key}", bare_unreported=True)
    if questions["workflow"]["state"] == "reported" and (
        not isinstance(page.get("workflow_scope"), str) or not page["workflow_scope"].strip()
    ):
        die(f"{filename}: page_content.workflow_scope is required for a reported workflow.")

    fields = page["implementation_fields"]
    if not isinstance(fields, dict) or set(fields) != ARCHITECTURE_FIELDS:
        die(
            f"{filename}: page_content.implementation_fields must contain all eight architecture fields."
        )
    for key, value in fields.items():
        disposition(
            value,
            f"page_content.implementation_fields.{key}",
            {f"architecture.{key}"},
            bare_unreported=True,
        )

    roles = page["primitive_roles"]
    expected_primitives = {f"primitives.{i}" for i, _ in enumerate(record.get("primitives") or [])}
    if not isinstance(roles, dict) or set(roles) != expected_primitives:
        die(f"{filename}: page_content.primitive_roles must classify every primitive exactly once.")
    if any(role not in PRIMITIVE_ROLES for role in roles.values()):
        die(f"{filename}: page_content.primitive_roles contains an invalid role.")
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
    if not isinstance(observations, dict) or set(observations) != expected_observations:
        die(f"{filename}: page_content.observations must describe every observation claim.")
    duplicates: dict[str, str] = {}
    for path, value in observations.items():
        value = require_exact_fields(
            value,
            set(),
            {"category", "basis", "subject", "duplicate_of", "reason"},
            f"page_content.observations.{path}",
            filename,
        )
        if "duplicate_of" in value:
            target = value["duplicate_of"]
            if target not in expected_observations or target == path:
                die(f"{filename}: observation {path!r} has an invalid duplicate target.")
            if not isinstance(value.get("reason"), str) or not value["reason"].strip():
                die(f"{filename}: duplicate observation {path!r} requires a reason.")
            duplicates[path] = target
        else:
            if (
                value.get("category") not in OBSERVATION_CATEGORIES
                or value.get("basis") not in OBSERVATION_BASES
            ):
                die(f"{filename}: observation {path!r} has an invalid category or basis.")
            if not isinstance(value.get("subject"), str) or not value["subject"].strip():
                die(f"{filename}: observation {path!r} requires a subject.")
    for source, target in duplicates.items():
        if target in duplicates:
            die(f"{filename}: duplicate observation {source!r} may not form a chain or cycle.")


def validate_record(record: dict, path: Path, global_sources: set[str]) -> None:
    filename = path.name
    missing = sorted(REQUIRED - set(record))
    if missing:
        die(f"{filename}: missing required field(s): {', '.join(missing)}")
    unexpected = sorted(set(record) - ALLOWED_TOP_LEVEL)
    if unexpected:
        die(f"{filename}: unexpected top-level field(s): {', '.join(unexpected)}")
    for field in ("id", "company", "agent_name", "summary"):
        require_string(record, field, filename)
    if not ID_RE.fullmatch(record["id"]):
        die(f"{filename}: 'id' must use kebab-case.")
    if record["id"] != path.stem:
        die(f"{filename}: 'id' must match the filename stem.")
    if not isinstance(record["year"], int) or isinstance(record["year"], bool):
        die(f"{filename}: 'year' must be an integer.")
    if record["status"] not in STATUS:
        die(f"{filename}: invalid status {record['status']!r}.")
    if record["autonomy"] not in AUTONOMY:
        die(f"{filename}: invalid autonomy {record['autonomy']!r}.")
    if record["approach_type"] not in APPROACH_TYPES:
        die(f"{filename}: invalid approach type {record['approach_type']!r}.")
    if record["deployment_stage"] not in DEPLOYMENT_STAGES:
        die(f"{filename}: invalid deployment stage {record['deployment_stage']!r}.")
    require_string_list(record["domains"], "domains", filename)
    if set(record["domains"]) - DOMAIN_VALUES:
        die(f"{filename}: 'domains' contains an unknown value.")
    rubric = record["rubric"]
    if not isinstance(rubric, dict):
        die(f"{filename}: 'rubric' must be a mapping.")
    require_string_list(rubric.get("invocation"), "rubric.invocation", filename)
    if set(rubric["invocation"]) - INVOCATION:
        die(f"{filename}: 'rubric.invocation' contains an invalid value.")
    for field, allowed in (
        ("state", STATE),
        ("identity", IDENTITY),
        ("evidence_strength", EVIDENCE_STRENGTH),
    ):
        if rubric.get(field) not in allowed:
            die(f"{filename}: 'rubric.{field}' is invalid.")
    operating_models = record["operating_models"]
    if not isinstance(operating_models, list) or not operating_models:
        die(f"{filename}: 'operating_models' must be a non-empty list.")
    for index, item in enumerate(operating_models):
        if not isinstance(item, dict) or set(item) != {"scope", "attention_boundary"}:
            die(
                f"{filename}: operating_models.{index} needs only 'scope' and 'attention_boundary'."
            )
        require_string(item, "scope", filename)
        if item["attention_boundary"] not in ATTENTION_BOUNDARIES:
            die(f"{filename}: operating_models.{index}.attention_boundary is invalid.")
    first = record.get("first_public_evidence")
    if not isinstance(first, dict):
        die(f"{filename}: 'first_public_evidence' must be a mapping.")
    validate_date(first.get("date"), "first_public_evidence.date", filename)
    require_string(first, "source_id", filename)
    validate_date(record.get("last_reviewed_at"), "last_reviewed_at", filename)
    if record.get("headline_metric") is not None:
        require_string(record, "headline_metric", filename)
    if record.get("aliases") is not None:
        require_string_list(record["aliases"], "aliases", filename, nonempty=False)
    if record.get("family_id") is not None:
        require_string(record, "family_id", filename)
        if not ID_RE.fullmatch(record["family_id"]):
            die(f"{filename}: 'family_id' must use kebab-case.")
    relationships = record.get("relationships") or []
    if not isinstance(relationships, list):
        die(f"{filename}: 'relationships' must be a list.")
    for relation in relationships:
        if not isinstance(relation, dict) or set(relation) != {"type", "approach_id"}:
            die(f"{filename}: every relationship needs only 'type' and 'approach_id'.")
        if relation["type"] not in RELATION_TYPES or not isinstance(relation["approach_id"], str):
            die(f"{filename}: relationship contains an invalid value.")
    architecture = record.get("architecture") or {}
    if not isinstance(architecture, dict):
        die(f"{filename}: 'architecture' must be a mapping.")
    unexpected_architecture = sorted(set(architecture) - ARCHITECTURE_FIELDS)
    if unexpected_architecture:
        die(f"{filename}: unexpected architecture field(s): {', '.join(unexpected_architecture)}")
    for key, value in architecture.items():
        if key == "interfaces":
            require_string_list(value, "architecture.interfaces", filename, nonempty=False)
            if set(value) - INTERFACE_VALUES:
                die(f"{filename}: 'architecture.interfaces' contains an unknown value.")
        elif not isinstance(value, str):
            die(f"{filename}: 'architecture.{key}' must be a string.")
    for field in ("key_metrics", "lessons_learned"):
        if field in record:
            require_string_list(record[field], field, filename, nonempty=False)
    if "primitives" in record:
        if not isinstance(record["primitives"], list):
            die(f"{filename}: 'primitives' must be a list.")
        for item in record["primitives"]:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("name"), str)
                or not item["name"]
            ):
                die(f"{filename}: every primitive needs a non-empty name.")
            if item.get("desc") is not None and not isinstance(item["desc"], str):
                die(f"{filename}: primitive descriptions must be strings.")
    if not isinstance(record["sources"], list) or not record["sources"]:
        die(f"{filename}: 'sources' must be a non-empty list.")
    local_sources: set[str] = set()
    for source in record["sources"]:
        validate_source(source, filename, local_sources)
        if source["id"] in global_sources:
            die(f"{filename}: source id {source['id']!r} is already used by another record.")
        global_sources.add(source["id"])
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
    for index, _ in enumerate(operating_models):
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
