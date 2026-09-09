"""Build and validate the Internal Agents Map."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
import tempfile
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
    "task-agent",
    "background-agent",
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


def render_overview(records: list[dict]) -> str:
    export = normalize(records)
    company_count = len({record["company"] for record in records})
    summary = (
        f"**Current map: {len(records)} approaches across {company_count} organizations, "
        f"backed by {len(export['sources'])} sources and "
        f"{len(export['claims'])} evidence-linked claims.**"
    )
    return "\n".join(
        [
            OVERVIEW_BEGIN,
            "",
            summary,
            "",
            "## Overview",
            "",
            render_overview_table(records),
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


def render_patterns_snapshot(records: list[dict]) -> str:
    approach_labels = {
        "task-agent": "Task agent",
        "platform": "Platform",
        "background-agent": "Background agent",
        "agent-system": "Agent system",
        "orchestration-system": "Orchestration system",
        "supporting-pattern": "Supporting pattern",
    }
    approach_counts = Counter(record["approach_type"] for record in records)
    autonomy_counts = Counter(record["autonomy"] for record in records)
    state_counts = Counter(record["rubric"]["state"] for record in records)
    slack_count = sum(
        "slack" in ((record.get("architecture") or {}).get("interfaces") or [])
        for record in records
    )
    sandbox_count = sum(
        documented_environment((record.get("architecture") or {}).get("sandbox"))
        for record in records
    )
    return "\n".join(
        [
            PATTERNS_SNAPSHOT_BEGIN,
            "",
            "## Catalog snapshot",
            "",
            f"The catalog currently contains {len(records)} approaches:",
            "",
            count_table(approach_counts, approach_labels),
            "",
            f"- {sandbox_count} approaches document a concrete execution environment.",
            f"- {slack_count} approaches list Slack as an interface.",
            "- State duration is "
            f"unknown for {state_counts['unknown']}, durable-session for "
            f"{state_counts['durable-session']}, cross-session-memory for "
            f"{state_counts['cross-session-memory']}, mixed for {state_counts['mixed']}, "
            f"and run-only for {state_counts['run-only']} approaches.",
            "- Autonomy is classified as "
            f"drafts-reviewed for {autonomy_counts['drafts-reviewed']}, human-in-loop for "
            f"{autonomy_counts['human-in-loop']}, autonomous for "
            f"{autonomy_counts['autonomous']}, assistive for {autonomy_counts['assistive']}, "
            f"and unknown for {autonomy_counts['unknown']} approaches.",
            "",
            PATTERNS_SNAPSHOT_END,
        ]
    )


def render_adoption_snapshot(records: list[dict]) -> str:
    autonomy_counts = Counter(record["autonomy"] for record in records)
    slack_count = sum(
        "slack" in ((record.get("architecture") or {}).get("interfaces") or [])
        for record in records
    )
    return "\n".join(
        [
            ADOPTION_SNAPSHOT_BEGIN,
            "",
            "## Catalog snapshot",
            "",
            f"These observations draw on {len(records)} cataloged approaches. "
            "The evidence is uneven, and most sources are company reports.",
            "",
            f"{slack_count} approaches list Slack as an interface. The autonomy distribution is "
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
        "## Comparison",
        "",
        render_comparison_table(records),
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


def normalize(records: list[dict]) -> dict:
    approaches = []
    claims = []
    sources = []
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
        approach["operating_models"] = [
            {**item, "level": BOUNDARY_LEVELS[item["attention_boundary"]]}
            for item in record["operating_models"]
        ]
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
    return {"schema_version": 4, "approaches": approaches, "claims": claims, "sources": sources}


def replace_between_markers(
    text: str, begin: str, end_marker: str, block: str, filename: str
) -> str:
    start = text.find(begin)
    end = text.find(end_marker)
    if text.count(begin) != 1 or text.count(end_marker) != 1 or end < start:
        die(f"{filename} must contain exactly one ordered {begin} and {end_marker} marker pair.")
    return text[:start] + block + text[end + len(end_marker) :]


def site_text(value: Any) -> str:
    """Escape all catalog prose; source text never becomes executable markup."""
    return html.escape(str(value), quote=True)


def site_label(value: str) -> str:
    labels = {"ci-triage": "CI triage", "on-call": "On-call"}
    if value in labels:
        return labels[value]
    if value.startswith("primitives."):
        return "Supporting component"
    if value == "architecture.context_mgmt":
        return "Context management"
    if value.startswith("architecture."):
        return value.split(".", 1)[1].replace("_", " ").capitalize()
    if value.startswith("key_metrics."):
        return "Key observation"
    if value == "headline_metric":
        return "Headline claim"
    if value.startswith("lessons_learned."):
        return "Lesson"
    if value.startswith("operating_models."):
        return "Operating model assessment"
    return value.replace("-", " ").replace("_", " ").capitalize()


def render_site(catalog: dict) -> str:
    """Render a complete, independently readable page from the normalized catalog."""
    repository = "https://github.com/steel-experiments/internal-agents-map"
    blob = repository + "/blob/main/"
    claims = {item["id"]: item for item in catalog["claims"]}
    sources = {item["id"]: item for item in catalog["sources"]}
    approaches = sorted(
        catalog["approaches"],
        key=lambda item: (item["company"].casefold(), item["agent_name"].casefold(), item["id"]),
    )

    def link(url: str, label: str, **attrs: str) -> str:
        # Validation normally restricts sources to HTTPS. Keep this pure renderer
        # safe even when called directly with a fixture or future imported data.
        if urlsplit(url).scheme not in {"http", "https", ""}:
            return site_text(label)
        attributes = "".join(f' {key}="{site_text(value)}"' for key, value in attrs.items())
        return f'<a href="{site_text(url)}"{attributes}>{site_text(label)}</a>'

    def source_links(source: dict) -> str:
        parts = [link(source["url"], source["title"])]
        capture = source.get("capture") or {}
        path = capture.get("artifacts", {}).get("markdown", {}).get("path")
        if path:
            parts.append(link(blob + path, "Preserved Markdown"))
        if source.get("archived_url"):
            parts.append(link(source["archived_url"], "Wayback snapshot"))
        return " · ".join(parts)

    def render_claim(claim: dict) -> str:
        details = []
        metadata = (
            ("confidence_reason", "Confidence reason"),
            ("reported_by", "Reported by"),
            ("metric_scope", "Scope"),
            ("denominator", "Denominator"),
            ("measurement_method", "Method"),
            ("valid_at", "Observation date"),
        )
        for key, label in metadata:
            value = claim.get(key)
            if value is not None or claim["kind"] == "metric":
                details.append(f"<dt>{label}</dt><dd>{site_text(value or 'Unknown')}</dd>")
        evidence = []
        for item in claim.get("evidence", []):
            source = sources[item["source_id"]]
            relation = item.get("relation", "supports")
            locator = (
                f'<span class="locator">{site_text(item["locator"])}</span>'
                if item.get("locator")
                else ""
            )
            evidence.append(
                f'<li><span class="relation relation-{site_text(relation)}">'
                f"{site_text(site_label(relation))}</span>{source_links(source)}"
                f" <span>({site_text(source['provenance_class'])})</span>{locator}</li>"
            )
        return (
            f'<article class="claim" id="claim-{site_text(claim["id"])}" '
            f'data-claim-id="{site_text(claim["id"])}">'
            f'<span class="claim-label">{site_text(site_label(claim["field"]))}</span>'
            f'<p>{site_text(claim["text"])}</p><div class="claim-meta">'
            f"<span>{site_text(site_label(claim['kind']))}</span> · "
            f"<span>{site_text(site_label(claim['provenance']))}</span> · "
            f"<span>{site_text(site_label(claim['confidence']))} confidence</span></div>"
            f'<details class="claim-details"><summary>Evidence and qualifications</summary>'
            f'<dl>{"".join(details)}</dl><ul class="evidence">{"".join(evidence)}</ul>'
            "</details></article>"
        )

    entries = []
    filter_values: dict[str, set[str]] = {"work": set(), "type": set(), "supervision": set()}
    for approach in approaches:
        attached = [claims[key] for key in approach["claim_ids"]]
        summary = next((item["text"] for item in attached if item["field"] == "summary"), "Unknown")
        domains = approach.get("domains") or ["unknown"]
        models = approach.get("operating_models") or []
        boundaries = sorted({item.get("attention_boundary") or "unknown" for item in models}) or [
            "unknown"
        ]
        approach_type = approach.get("approach_type") or "unknown"
        filter_values["work"].update(domains)
        filter_values["type"].add(approach_type)
        filter_values["supervision"].update(boundaries)
        search = " ".join(
            " ".join(
                [
                    approach["company"],
                    approach["agent_name"],
                    summary,
                    " ".join(domains),
                    approach_type,
                    site_label(approach_type),
                    " ".join(site_label(d) for d in domains),
                ]
            ).split()
        ).lower()
        attrs = {
            "id": approach["id"],
            "data-approach-id": approach["id"],
            "data-search": search,
            "data-work": " ".join(domains),
            "data-type": approach_type,
            "data-supervision": " ".join(boundaries),
        }
        attrs_html = " ".join(f'{key}="{site_text(value)}"' for key, value in attrs.items())
        model_html = (
            "".join(
                f'<p class="operating-model"><strong>{site_text(item["scope"])}</strong>'
                f"{site_text(site_label(item['attention_boundary']))} · "
                f"{'Level ' + str(item['level']) if item.get('level') is not None else 'Level unknown'}</p>"
                for item in models
            )
            or "<p>Operating model unknown.</p>"
        )
        supervision = (
            "".join(
                f"<span>{site_text(item['scope'])}: {site_text(site_label(item['attention_boundary']))}</span>"
                for item in models
            )
            or "<span>Unknown</span>"
        )
        groups: dict[str, list[dict]] = {}
        for claim in attached:
            field = claim["field"]
            group = (
                "Reported metrics"
                if claim["kind"] == "metric"
                else "Summary and context"
                if field == "summary"
                else "Architecture and primitives"
                if field.startswith(("architecture.", "primitives."))
                else "Operating model evidence"
                if field.startswith("operating_models.")
                else "Lessons and interpretation"
                if field.startswith("lessons_learned.")
                else "Other reported details and interpretation"
            )
            groups.setdefault(group, []).append(claim)
        group_html = "".join(
            f"<h4>{title}</h4>{''.join(render_claim(item) for item in items)}"
            for title, items in groups.items()
        )
        source_html = []
        for source_id in approach["source_ids"]:
            source = sources[source_id]
            source_html.append(
                f'<li id="source-{site_text(source_id)}" data-source-id="{site_text(source_id)}">'
                f'<span class="source-title">{source_links(source)}</span>'
                f"{link(source['url'], source['url'], **{'class': 'source-url'})}"
                f'<span class="source-meta">{site_text(source["kind"])} · '
                f"{site_text(source['provenance_class'])} · "
                f"Last source verification: {site_text(source.get('last_verified_at', 'Unknown'))}"
                "</span></li>"
            )
        tags = "".join(
            f'<span class="tag">{site_text(site_label(item))}</span>' for item in domains
        )
        entries.append(
            f'<article class="entry" {attrs_html}><div class="entry-top">'
            f'<span class="company">{site_text(approach["company"])}</span>'
            f'<span class="entry-type">{site_text(site_label(approach_type))}</span></div>'
            f'<h3>{site_text(approach["agent_name"])}</h3><p class="entry-summary">{site_text(summary)}</p>'
            f'<div class="tags">{tags}</div><div class="supervision">{supervision}</div>'
            f'<details><summary>Operating model, claims &amp; sources</summary><div class="entry-body">'
            f"<h4>Scoped operating models</h4>{model_html}{group_html}"
            f'<h4>Sources</h4><ol class="sources">{"".join(source_html)}</ol></div></details>'
            f'<div class="entry-end"><span>Entry reviewed {site_text(approach["last_reviewed_at"])}</span>'
            f"{link('#' + approach['id'], 'Permalink ↗', **{'class': 'permalink', 'aria-label': 'Permalink to ' + approach['company'] + ' — ' + approach['agent_name']})}"
            "</div></article>"
        )
    filters = []
    for name, label in (
        ("work", "Work"),
        ("type", "Approach type"),
        ("supervision", "Human supervision"),
    ):
        options = "".join(
            f'<option value="{site_text(value)}">{site_text(site_label(value))}</option>'
            for value in sorted(filter_values[name])
        )
        filters.append(
            f'<label for="{name}">{label}<select id="{name}" name="{name}">'
            f'<option value="">All</option>{options}</select></label>'
        )
    stats = "".join(
        f'<div class="stat"><strong>{count}</strong><span>{label}</span></div>'
        for count, label in (
            (len(approaches), "approaches"),
            (len({item["company"] for item in approaches}), "organizations"),
            (len(sources), "sources"),
        )
    )
    docs = "".join(
        link(blob + path, label)
        for path, label in (
            ("data/schema.md", "Data schema"),
            ("docs/patterns.md", "Architecture patterns"),
            ("docs/adoption-lessons.md", "Adoption observations"),
            ("docs/evidence-review.md", "Evidence review"),
            ("CONTRIBUTING.md", "Contribution guide"),
        )
    )
    values = {
        "STATS": stats,
        "REVIEW": site_text(max((a["last_reviewed_at"] for a in approaches), default="Unknown")),
        "FILTERS": "".join(filters),
        "COUNT": str(len(approaches)),
        "ENTRIES": "\n".join(entries),
        "DOCS": docs,
    }
    template = (ROOT / "templates/site.html").read_text(encoding="utf-8")
    return re.sub(r"@@([A-Z]+)@@", lambda match: values[match[1]], template)


def render_definitions(catalog: dict) -> str:
    """Illustrate selected, scoped catalog assessments without ranking agents."""
    # Editorial regions, supported by the linked scope/context claims; not scores.
    selected = {
        "doordash-code-review": (
            "specialized",
            "One code-review workflow, grounded in repository evidence and domain rules.",
        ),
        "stripe-minions": (
            "specialized",
            "Several engineering tasks within a coding workflow, connected to Stripe’s development tools and repository rules. Placed toward the middle of workflow breadth.",
        ),
        "posthog-stamphog": (
            "specialized",
            "One pull-request approval workflow, grounded in repository-specific safety gates, review state, ownership, and prior human approvals.",
        ),
        "ramp-inspect": (
            "specialized",
            "A background coding agent that verifies work with tests, telemetry, feature flags, and the rendered frontend; it later expanded into production monitoring and a host for other internal agents.",
        ),
        "brex-agent-platform": (
            "shared",
            "A Retool-based platform for multiple operations workflows, with company procedures, account data, and product tools. Described in a First Round case study.",
        ),
        "sentry-junior": (
            "shared",
            "A general internal agent that takes varied tasks across company systems, with persistent context and tools discovered through MCP.",
        ),
        "shopify-internal-agents": (
            "shared",
            "A shared platform that powers coding, research, migration, and application-security agents using Shopify’s monorepo context and internal tools.",
        ),
    }
    claims = {claim["id"]: claim for claim in catalog["claims"]}
    cells = {"specialized": [], "shared": []}
    notes = []
    for approach in catalog["approaches"]:
        if approach["id"] not in selected:
            continue
        cell, reason = selected[approach["id"]]
        evidence = {
            claims[key]["field"]: claims[key] for key in approach["claim_ids"] if key in claims
        }
        required = ("summary", "architecture.knowledge", "architecture.tool_access")
        if any(
            field not in evidence
            or str(evidence[field]["text"]).strip().lower() in {"unknown", "not specified", ""}
            or not any(e["relation"] == "supports" for e in evidence[field]["evidence"])
            for field in required
        ):
            continue
        cells[cell].append(
            f'<li data-chart-approach-id="{site_text(approach["id"])}">'
            f'<a href="index.html#{site_text(approach["id"])}" '
            f'title="{site_text(reason)}">'
            f"<strong>{site_text(approach['company'])}</strong>"
            f"<span>{site_text(approach['agent_name'])}</span></a></li>"
        )
        links = " · ".join(
            f'<a href="index.html#claim-{site_text(evidence[field]["id"])}">{label}</a>'
            for field, label in zip(required, ("Scope", "Context", "Tools"))
        )
        notes.append(
            f"<li><strong>{site_text(approach['company'])} · {site_text(approach['agent_name'])}</strong>"
            f"<p>{site_text(reason)}</p><div>{links}</div></li>"
        )
    shell = (ROOT / "templates/site.html").read_text(encoding="utf-8")
    sidebar = re.search(r"<aside.*?</aside>", shell, re.S)[0]
    for anchor in ("main", "catalog", "methodology"):
        sidebar = sidebar.replace(f'href="#{anchor}"', f'href="index.html#{anchor}"')
    sidebar = sidebar.replace(
        'href="definitions.html"', 'href="definitions.html" aria-current="page"'
    )
    values = {
        "SIDEBAR": sidebar,
        "PLACEMENTS": "".join(notes),
        "FOOTER": re.search(r"<footer>.*?</footer>", shell, re.S)[0],
        **{
            key.upper(): "".join(items) or "<li>No selected example currently fits.</li>"
            for key, items in cells.items()
        },
    }
    template = (ROOT / "templates/definitions.html").read_text(encoding="utf-8")
    return re.sub(r"@@([A-Z]+)@@", lambda match: values[match[1]], template)


def rendered_outputs(records: list[dict]) -> dict[Path, str | bytes]:
    readme = README.read_text(encoding="utf-8")
    patterns = PATTERNS.read_text(encoding="utf-8")
    adoption_lessons = ADOPTION_LESSONS.read_text(encoding="utf-8")
    catalog = normalize(records)
    catalog_json = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    return {
        README: replace_between_markers(
            readme, OVERVIEW_BEGIN, OVERVIEW_END, render_overview(records), "README.md"
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
        DATA_JSON: catalog_json,
        ROOT / "site/index.html": render_site(catalog),
        ROOT / "site/definitions.html": render_definitions(catalog),
        ROOT / "site/agents.json": catalog_json,
        **{
            ROOT / "site/assets" / name: (ROOT / "templates" / name).read_text(encoding="utf-8")
            for name in ("site.css", "site.js")
        },
        **{
            ROOT / "site/assets/fonts" / name: (ROOT / "templates/fonts" / name).read_bytes()
            for name in ("Geist.woff2", "OFL.txt")
        },
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale.")
    args = parser.parse_args()
    records = load_agents()
    outputs = rendered_outputs(records)
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
        print(f"Validated {len(records)} approaches. Generated files are current.")
        return
    write_outputs(outputs)
    print(f"\n{len(records)} approaches. Build complete.")


if __name__ == "__main__":
    main()
