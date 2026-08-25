#!/usr/bin/env python3
"""Rewrite the approach-type table in docs/patterns.md from the live records.

The build test test_documented_sample_counts_are_current enforces this table.
Run this after adding or removing a record, then update the prose counts by
hand using the values this script prints.
"""

import re
import sys
from collections import Counter
from pathlib import Path

import yaml

LABELS = {
    "task-agent": "Task agent",
    "platform": "Platform",
    "background-agent": "Background agent",
    "agent-system": "Agent system",
    "orchestration-system": "Orchestration system",
    "supporting-pattern": "Supporting pattern",
}

TABLE_RE = re.compile(
    r"(\| Type \| Count \|\n\| --- \| ---: \|\n)((?:\| [^\n]+ \| \d+ \|\n)+)"
)


def main() -> int:
    root = Path.cwd()
    if not (root / "data" / "agents").is_dir():
        print("run this from the repo root", file=sys.stderr)
        return 1

    recs = [
        yaml.safe_load(p.read_text(encoding="utf-8"))
        for p in sorted((root / "data" / "agents").glob("*.yaml"))
    ]
    counts = Counter(r["approach_type"] for r in recs)
    rows = "".join(f"| {label} | {counts.get(value, 0)} |\n" for value, label in LABELS.items())

    patterns = root / "docs" / "patterns.md"
    text = patterns.read_text(encoding="utf-8")
    new_text, n = TABLE_RE.subn(lambda m: m.group(1) + rows, text, count=1)
    if n != 1:
        print("approach-type table not found in docs/patterns.md", file=sys.stderr)
        return 1
    patterns.write_text(new_text, encoding="utf-8")

    print(f"table rewritten for {len(recs)} approaches")
    print(f"total approaches: {len(recs)}")
    print("prose counts to update by hand:")
    print(f"  autonomy: {dict(Counter(r['autonomy'] for r in recs))}")
    print(f"  rubric state: {dict(Counter(r['rubric']['state'] for r in recs))}")
    slack = sum(1 for r in recs if "slack" in ((r.get("architecture") or {}).get("interfaces") or []))
    print(f"  slack interfaces: {slack}")
    sandbox = sum(
        1 for r in recs
        if (r.get("architecture") or {}).get("sandbox") not in (None, "", "unknown")
    )
    print(f"  architecture.sandbox documented: {sandbox}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
