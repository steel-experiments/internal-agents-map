# ABOUTME: The Update merge: an existing record plus the update's additions.
# ABOUTME: Principle 4 of Plan 017: additive only, at the end of every list.
"""Merge an update's rendered draft into the record it proposes to update.

The merge is additive by construction. Sources, list items, evidence links,
and metadata entries are appended at the end of their lists when absent.
Nothing is reordered, rewritten, or removed. Single-valued fields keep the
recorded text; an update that claims a different value produces a note for
the reviewer instead of a silent change. The page-content block keeps the
recorded answers and upgrades only the questions the new run reviewed.
"""

from __future__ import annotations

import copy
from typing import Any

# Each list field and the key that identifies a duplicate item.
_LIST_FIELDS: dict[str, Any] = {
    "primitives": lambda item: item.get("name"),
    "lessons_learned": lambda item: item,
    "key_metrics": lambda item: item,
    "operating_models": lambda item: item.get("scope"),
}

_SINGLE_FIELDS = ("summary", "agent_name", "company", "headline_metric")


def merge_update(
    existing: dict[str, Any],
    rendered: dict[str, Any],
    *,
    reviewed_at: str,
    notes: list[str] | None = None,
    contradictions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """The existing record with the update's additions appended.

    ``contradictions`` carries the cross checks' number conflicts as rendered
    links; each appends to the existing claim's evidence with
    ``relation: contradicts`` — the plan's proposed contradiction link. The
    reviewer decides whether the numbers describe the same observation.
    """
    notes = notes if notes is not None else []
    merged = copy.deepcopy(existing)
    merged["last_reviewed_at"] = reviewed_at

    existing_source_ids = {source.get("id") for source in merged.get("sources") or []}
    for source in rendered.get("sources") or []:
        if source.get("id") in existing_source_ids:
            notes.append(f"source {source['id']} already exists on the record; not duplicated")
            continue
        merged.setdefault("sources", []).append(source)
        existing_source_ids.add(source.get("id"))

    for field, key_of in _LIST_FIELDS.items():
        present = {key_of(item) for item in merged.get(field) or []}
        for item in rendered.get(field) or []:
            if key_of(item) in present:
                continue
            merged.setdefault(field, []).append(item)
            present.add(key_of(item))

    for field in _SINGLE_FIELDS:
        if rendered.get(field) is not None and rendered[field] != merged.get(field):
            notes.append(
                f"the update claims a new {field}; the field is single-valued and the "
                "recorded text stays — a person decides"
            )
    for key, value in (rendered.get("architecture") or {}).items():
        if (merged.get("architecture") or {}).get(key) != value:
            notes.append(
                f"the update claims architecture.{key}; the recorded text stays — a person decides"
            )

    evidence = merged.setdefault("evidence", {})

    def _fingerprint(link: dict[str, Any]) -> tuple[Any, ...]:
        return (link.get("source_id"), link.get("locator"), link.get("relation"))

    for path, links in (rendered.get("evidence") or {}).items():
        known = {_fingerprint(link) for link in evidence.get(path) or []}
        for link in links:
            if _fingerprint(link) in known:
                continue
            evidence.setdefault(path, []).append(link)
            known.add(_fingerprint(link))

    # The plan's contradiction policy: a restated number that disagrees with
    # a recorded metric becomes a proposed link on the existing claim.
    for contradiction in contradictions or []:
        link = {
            "source_id": contradiction["source_id"],
            "relation": "contradicts",
            "locator": contradiction["locator"],
        }
        known = {_fingerprint(item) for item in evidence.get(contradiction["claim_path"]) or []}
        if _fingerprint(link) not in known:
            evidence.setdefault(contradiction["claim_path"], []).append(link)

    metadata = merged.setdefault("claim_metadata", {})
    for path, meta in (rendered.get("claim_metadata") or {}).items():
        if path not in metadata:
            metadata[path] = meta

    rendered_page = rendered.get("page_content")
    if rendered_page:
        page = merged.get("page_content")
        if not page:
            merged["page_content"] = rendered_page
        else:
            page = copy.deepcopy(page)
            page["reviewed_at"] = rendered_page.get("reviewed_at", reviewed_at)
            page["source_ids"] = list(
                dict.fromkeys(
                    (page.get("source_ids") or []) + (rendered_page.get("source_ids") or [])
                )
            )
            for block in ("questions", "implementation_fields"):
                for key, value in (rendered_page.get(block) or {}).items():
                    if value.get("state") == "not-reviewed":
                        continue
                    old = (page.get(block) or {}).get(key)
                    if old is None:
                        page.setdefault(block, {})[key] = value
                        continue
                    upgraded: dict[str, Any] = {
                        "state": value["state"],
                        "claim_paths": sorted(
                            set(old.get("claim_paths") or []) | set(value.get("claim_paths") or [])
                        ),
                    }
                    if value.get("note"):
                        upgraded["note"] = value["note"]
                    page.setdefault(block, {})[key] = upgraded
            observations = page.setdefault("observations", {})
            for key, value in (rendered_page.get("observations") or {}).items():
                if key not in observations:
                    observations[key] = value
            merged["page_content"] = page
    return merged
