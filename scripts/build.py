#!/usr/bin/env python3
"""Build and validate the Internal Agents Map."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, NoReturn

try:
    import yaml
except ImportError:
    sys.exit(
        "PyYAML is required. Install dependencies with "
        "'python3 -m pip install -r requirements.txt'."
    )

ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOT / "data" / "agents"
README = ROOT / "README.md"
LANDSCAPE = ROOT / "docs" / "landscape.md"
DATA_JSON = ROOT / "data" / "agents.json"
BEGIN = "<!-- BEGIN LANDSCAPE -->"
END = "<!-- END LANDSCAPE -->"

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
    "sandbox", "harness", "model", "tool_access", "interfaces", "knowledge",
    "credentials", "context_mgmt",
}
SOURCE_FIELDS = {
    "id", "title", "url", "canonical_url", "kind", "provenance_class", "role",
    "publisher", "authors", "published_at", "accessed_at", "last_verified_at",
    "archived_url", "content_fingerprint", "duplicate_of",
}
CLAIM_METADATA_FIELDS = {
    "kind", "provenance", "confidence", "confidence_reason", "valid_at", "value",
    "unit", "reported_by", "metric_scope", "denominator", "measurement_method",
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
EVIDENCE_RELATIONS = {"supports", "contradicts", "contextualizes"}
RELATION_TYPES = {"component-of", "built-on", "successor-of", "related-to"}
DOMAIN_VALUES = {
    "coding", "code-review", "support", "on-call", "research", "customer-success",
    "security", "finance-ops", "data", "ci-triage", "maintenance", "ops",
    "recruitment", "migrations",
}
INTERFACE_VALUES = {
    "slack", "github", "web", "cli", "linear", "chrome-extension", "webhook",
    "desktop", "scheduled", "skill", "cursor", "api", "automation", "ci",
    "intercom", "jira", "internal-ui", "mobile", "monday",
}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}(?:-(?:0[1-9]|1[0-2])(?:-(?:0[1-9]|[12]\d|3[01]))?)?$")

TABLE_HEADER = (
    "| Company | Approach | Type | Domains | Autonomy | Stage | Status | Year |\n"
    "| --- | --- | --- | --- | --- | --- | --- | --- |"
)


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


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


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


def claim_fields(record: dict) -> dict[str, tuple[str, str, str]]:
    """Return claim path -> (text, kind, provenance) for authored claim fields."""
    claims: dict[str, tuple[str, str, str]] = {
        "summary": (record["summary"], "fact", "reported")
    }
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
    return claims


def validate_source(source: Any, filename: str, seen: set[str]) -> None:
    if not isinstance(source, dict):
        die(f"{filename}: every source must be a mapping.")
    unexpected = sorted(set(source) - SOURCE_FIELDS)
    if unexpected:
        die(f"{filename}: source contains unexpected field(s): {', '.join(unexpected)}")
    for field in ("id", "title", "url", "canonical_url", "kind", "provenance_class", "accessed_at", "last_verified_at"):
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
            die(f"{filename}: claim metadata for {path!r} contains unexpected field(s): {', '.join(unexpected)}")
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
    for field, allowed in (("state", STATE), ("identity", IDENTITY), ("evidence_strength", EVIDENCE_STRENGTH)):
        if rubric.get(field) not in allowed:
            die(f"{filename}: 'rubric.{field}' is invalid.")
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
            if not isinstance(item, dict) or not isinstance(item.get("name"), str) or not item["name"]:
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
    first_source = next(source for source in record["sources"] if source["id"] == first["source_id"])
    if first_source.get("role", "evidence") != "evidence":
        die(f"{filename}: first public evidence must use a source with the evidence role.")
    validate_evidence(record, filename, local_sources)
    referenced_sources = {
        link["source_id"]
        for links in record["evidence"].values()
        for link in links
    }
    unused_evidence = sorted(
        source["id"]
        for source in record["sources"]
        if source.get("role", "evidence") == "evidence" and source["id"] not in referenced_sources
    )
    if unused_evidence:
        die(f"{filename}: evidence source(s) are not linked to a claim: {', '.join(unused_evidence)}")


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
                die(f"{record['id']}.yaml: relationship uses unknown approach {relation['approach_id']!r}.")
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


def render_table(records: list[dict]) -> str:
    lines = [BEGIN, "", TABLE_HEADER]
    for record in records:
        link = f"[{markdown(record['agent_name'])}](docs/landscape.md#{anchor(record)})"
        lines.append(
            "| {company} | {approach} | {kind} | {domains} | {autonomy} | {stage} | {status} | {year} |".format(
                company=markdown(record["company"]),
                approach=link,
                kind=markdown(record["approach_type"]),
                domains=markdown(record["domains"]),
                autonomy=markdown(record["autonomy"]),
                stage=markdown(record["deployment_stage"]),
                status=markdown(record["status"]),
                year=record["year"],
            )
        )
    return "\n".join([*lines, "", END])


def render_landscape(records: list[dict]) -> str:
    out = [
        "# Internal agents: full catalog",
        "",
        "<!-- Generated by scripts/build.py. Edit data/agents/*.yaml instead. -->",
        "",
        f"The catalog contains {len(records)} approaches. Company names determine the sort order.",
        "",
        "## Contents",
        "",
    ]
    for record in records:
        out.append(f"- [{record['company']}: {record['agent_name']}](#{anchor(record)})")
    out.extend([
        "",
        "## Terms and rubric",
        "",
        "Common terms include artificial intelligence (AI), application programming interface (API), continuous integration (CI), and command-line interface (CLI).",
        "Other terms include large language model (LLM), Model Context Protocol (MCP), pull request (PR), and software development kit (SDK).",
        "Access terms include attribute-based access control (ABAC), role-based access control (RBAC), and single sign-on (SSO).",
        "Domain terms include know your customer (KYC), quality assurance (QA), security operations center (SOC), and structured query language (SQL).",
        "",
        "The [schema reference](../data/schema.md) defines each comparison field. Unknown means that the collected sources do not document the value.",
        "",
    ])
    for record in records:
        rubric = record["rubric"]
        out.extend([
            f"<a id=\"{anchor(record)}\"></a>",
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
            f"| Autonomy | {markdown(record['autonomy'])} |",
            f"| Invocation | {markdown(rubric['invocation'])} |",
            f"| State | {markdown(rubric['state'])} |",
            f"| Identity | {markdown(rubric['identity'])} |",
            f"| Evidence | {markdown(rubric['evidence_strength'])} |",
        ])
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
        for field, heading in (("primitives", "Primitives"), ("key_metrics", "Reported metrics"), ("lessons_learned", "Catalog observations")):
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
            detail = f"{source['kind']}; {source['provenance_class']}; {source.get('role', 'evidence')}"
            out.append(f"- <a id=\"{source['id']}\"></a>[{source['title']}]({source['url']}) ({detail})")
        out.extend(["", f"Last reviewed: {record['last_reviewed_at']}.", "", "---", ""])
    return "\n".join(out)


def normalize(records: list[dict]) -> dict:
    approaches = []
    claims = []
    sources = []
    for record in records:
        claim_value_fields = {
            "summary", "headline_metric", "architecture", "primitives", "key_metrics",
            "lessons_learned",
        }
        approach = {
            key: value
            for key, value in record.items()
            if key not in {"sources", "evidence", "claim_metadata"} | claim_value_fields
        }
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
            default_confidence = "high" if "first-party" in classes else (
                "medium" if classes & {"direct-participant", "independent-secondary"} else "low"
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
            sources.append({**source, "role": source.get("role", "evidence"), "approach_id": record["id"]})
    return {"schema_version": 2, "approaches": approaches, "claims": claims, "sources": sources}


def replace_between_markers(text: str, block: str) -> str:
    start = text.find(BEGIN)
    end = text.find(END)
    if start == -1 or end == -1 or end < start:
        die(f"README.md must contain one ordered {BEGIN} and {END} marker pair.")
    return text[:start] + block + text[end + len(END):]


def rendered_outputs(records: list[dict]) -> dict[Path, str]:
    readme = README.read_text(encoding="utf-8")
    return {
        README: replace_between_markers(readme, render_table(records)),
        LANDSCAPE: render_landscape(records),
        DATA_JSON: json.dumps(normalize(records), indent=2, ensure_ascii=False) + "\n",
    }


def write_outputs(outputs: dict[Path, str]) -> None:
    staged: list[tuple[Path, Path]] = []
    try:
        for path, content in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
            temporary_path = Path(temporary)
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                stream.write(content)
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
    stale = [path for path, content in outputs.items() if not path.exists() or path.read_text(encoding="utf-8") != content]
    if args.check:
        if stale:
            die("Generated files are stale: " + ", ".join(str(path.relative_to(ROOT)) for path in stale))
        print(f"Validated {len(records)} approaches. Generated files are current.")
        return
    write_outputs(outputs)
    print(f"\n{len(records)} approaches. Build complete.")


if __name__ == "__main__":
    main()
