# ABOUTME: Backfill apply: locator-only edits to existing records (Plan 017, Phase 5).
# ABOUTME: Touches only locator fields, on a person's approved proposals.
"""Apply approved locator proposals to existing records.

The input is an approved proposals file: the dry run's report with each
proposal carrying an ``approved: true`` flag a person added after reading the
quote in its capture. The applier touches only ``locator`` fields — it adds a
locator to an existing evidence link or refuses. It never reorders, rewrites,
or removes anything. The reviewer regenerates the data outputs and opens the
pull request; the pipeline does not.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent


class ApplyError(RuntimeError):
    """The proposals file is invalid or conflicts with the record."""


def load_proposals(path: Path) -> list[dict[str, Any]]:
    """Load the approved proposals; unapproved entries are refused."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ApplyError(f"{path}: proposals are a JSON list")
    approved = []
    for index, proposal in enumerate(payload):
        if not isinstance(proposal, dict):
            raise ApplyError(f"{path}: proposal {index} is not an object")
        for field in ("record", "path", "source_id", "locator"):
            if not proposal.get(field):
                raise ApplyError(f"{path}: proposal {index} lacks {field!r}")
        if proposal.get("approved") is not True:
            raise ApplyError(
                f"{path}: proposal {index} for {proposal.get('record')}/"
                f"{proposal.get('path')} is not approved; a person must approve it"
            )
        approved.append(proposal)
    return approved


def apply_proposals(
    proposals: list[dict[str, Any]],
    *,
    record_root: Path | None = None,
) -> list[Path]:
    """Apply locator-only changes; returns the changed record paths."""

    root = record_root or (ROOT / "data" / "agents")
    by_record: dict[str, list[dict[str, Any]]] = {}
    for proposal in proposals:
        by_record.setdefault(proposal["record"], []).append(proposal)
    changed: list[Path] = []
    for record_id, entries in sorted(by_record.items()):
        path = root / f"{record_id}.yaml"
        if not path.is_file():
            raise ApplyError(f"no record {record_id}.yaml under {root}")
        record = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(record, dict):
            raise ApplyError(f"{path}: not a YAML mapping")
        for proposal in entries:
            links = record.get("evidence", {}).get(proposal["path"])
            if links is None:
                raise ApplyError(f"{record_id}: evidence path {proposal['path']!r} does not exist")
            matching = [link for link in links if link.get("source_id") == proposal["source_id"]]
            if not matching:
                raise ApplyError(
                    f"{record_id}: no evidence link on {proposal['path']!r} names "
                    f"source {proposal['source_id']!r}"
                )
            for link in matching:
                if link.get("locator") and link["locator"] != proposal["locator"]:
                    raise ApplyError(
                        f"{record_id}/{proposal['path']}: link already carries a "
                        f"different locator {link['locator']!r}; locators are "
                        "append-only"
                    )
                link["locator"] = proposal["locator"]
        path.write_text(
            yaml.safe_dump(record, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )
        changed.append(path)
    return changed
