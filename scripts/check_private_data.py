# ABOUTME: Scan tracked catalog text for e-mail addresses that must not be public.
# ABOUTME: Contact data belongs in the private companion repo and the CRM, not here.
"""Fail when a tracked file in the public catalog contains an e-mail address."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# External reference snapshots are copies of third-party pages and may quote
# their own contact details. They are not catalog prose, so the scan skips them.
SKIPPED_PREFIXES = ("archive/",)
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")


def tracked_files(root: Path) -> list[Path]:
    """Return the git-tracked files that the scan must read."""
    output = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, check=True, capture_output=True, text=True
    ).stdout
    return [
        root / name for name in output.split("\0") if name and not name.startswith(SKIPPED_PREFIXES)
    ]


def find_emails(path: Path) -> list[tuple[int, str]]:
    """Return each (line number, match) e-mail address in a text file."""
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    return [
        (number, match.group(0))
        for number, line in enumerate(text.splitlines(), start=1)
        for match in EMAIL_RE.finditer(line)
    ]


def scan(root: Path) -> list[str]:
    """Return one report line for each e-mail address found under root."""
    findings: list[str] = []
    for path in tracked_files(root):
        for number, address in find_emails(path):
            findings.append(f"{path.relative_to(root)}:{number}: {address}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root to scan.")
    args = parser.parse_args()
    findings = scan(args.root.resolve())
    if findings:
        print("E-mail addresses are not allowed in the public catalog:", file=sys.stderr)
        for line in findings:
            print(f"  {line}", file=sys.stderr)
        print(
            "Move contact data to the private companion repo or the CRM.",
            file=sys.stderr,
        )
        return 1
    print("No e-mail addresses found in tracked files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
