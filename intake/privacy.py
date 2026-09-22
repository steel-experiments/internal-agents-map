# ABOUTME: The in-run private-data guard over writer output (Plan 017 STOP line).
# ABOUTME: Mirrors scripts/check_private_data.py; a find stops the run.
"""Stop the run when the writer produces contact data.

The public catalog carries no e-mail addresses; contact data belongs to the
private companion repository. The repository-level scan in ``npm run verify``
is the last guard; this module is the early one, so a writer reply that
carries an e-mail address anywhere in the extraction record stops the run at
the stage that produced it instead of at review time.

A person's name is not mechanically detectable; that half of the STOP line
stays on the review sheet as a human check.
"""

from __future__ import annotations

import re
from typing import Any

# Kept in lockstep with scripts/check_private_data.py.
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")


class PrivateDataError(RuntimeError):
    """The extraction record carries contact data outside a source's authors."""


def find_contact_data(payload: Any, *, path: str = "") -> list[str]:
    """Every payload path whose string holds an e-mail address.

    ``sources[*].authors`` is exempt: it is the one place the schema allows
    names, and a page's byline may name an e-mail address as its author.
    """
    if isinstance(payload, str):
        matches = EMAIL_RE.findall(payload)
        return [f"{path or '<root>'}: {match}" for match in matches]
    if isinstance(payload, dict):
        findings: list[str] = []
        for key, value in payload.items():
            if key == "authors":
                continue
            findings.extend(find_contact_data(value, path=f"{path}.{key}" if path else key))
        return findings
    if isinstance(payload, (list, tuple)):
        findings = []
        for index, item in enumerate(payload):
            findings.extend(find_contact_data(item, path=f"{path}.{index}"))
        return findings
    return []


def assert_clean(payload: Any, *, label: str) -> None:
    """Stop with a report when the payload carries contact data."""
    findings = find_contact_data(payload)
    if findings:
        listed = "\n".join(f"  {finding}" for finding in findings)
        raise PrivateDataError(
            f"{label}: the writer produced contact data outside a source's "
            f"authors field:\n{listed}\n"
            "Strip it, or keep it in the private companion repository."
        )
