# ABOUTME: Stage 2 of the intake pipeline: split a capture into paragraphs (Plan 017).
# ABOUTME: Paragraph IDs and line ranges back the quote locators of every claim.
"""Segment a preserved capture into paragraphs with stable IDs.

A paragraph is a maximal run of non-blank lines. Fenced code blocks stay one
paragraph even when they contain blank lines, so a quote inside a code block
keeps one locator. A Markdown heading is its own paragraph and extends the
heading path for the paragraphs that follow. Transcript timestamps stay in the
paragraph text, so a locator can name them.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


@dataclass(frozen=True)
class Paragraph:
    """One addressable block of the capture."""

    id: str
    heading_path: tuple[str, ...]
    start: int
    end: int
    text: str


def segment_content(markdown: str) -> list[Paragraph]:
    """Split one capture into paragraphs with IDs, heading paths, and line ranges."""
    lines = markdown.splitlines()
    paragraphs: list[Paragraph] = []
    heading_path: list[str] = []
    start: int | None = None
    in_fence = False
    fence_marker = ""

    def flush(end: int) -> None:
        nonlocal start
        if start is None:
            return
        text = "\n".join(lines[start - 1 : end])
        paragraphs.append(
            Paragraph(
                id=f"p{len(paragraphs) + 1}",
                heading_path=tuple(heading_path),
                start=start,
                end=end,
                text=text,
            )
        )
        start = None

    for index, line in enumerate(lines, start=1):
        fence = FENCE_RE.match(line)
        if fence and not in_fence:
            flush(index - 1)
            in_fence = True
            fence_marker = fence.group(1)
            start = index
            continue
        if in_fence:
            if fence and fence.group(1) == fence_marker and line.strip().startswith(fence_marker):
                flush(index)
                in_fence = False
                fence_marker = ""
            continue
        if not line.strip():
            flush(index - 1)
            continue
        heading = HEADING_RE.match(line)
        if heading:
            flush(index - 1)
            level = len(heading.group(1))
            del heading_path[level - 1 :]
            heading_path.append(heading.group(2).strip())
            start = index
            continue
        if start is None:
            start = index
    flush(len(lines))
    return paragraphs


def paragraphs_json(paragraphs: list[Paragraph]) -> str:
    """Serialize paragraphs with heading paths as lists for JSON round-tripping."""
    payload = [
        {
            "id": paragraph.id,
            "heading_path": list(paragraph.heading_path),
            "start": paragraph.start,
            "end": paragraph.end,
            "text": paragraph.text,
        }
        for paragraph in paragraphs
    ]
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def load_paragraphs_file(path: Path) -> list[Paragraph]:
    """Load paragraphs written by :func:`paragraphs_json`."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [
        Paragraph(
            id=item["id"],
            heading_path=tuple(item["heading_path"]),
            start=item["start"],
            end=item["end"],
            text=item["text"],
        )
        for item in payload
    ]


def coverage(paragraphs: list[Paragraph]) -> set[int]:
    """The line numbers covered by the paragraphs."""
    covered: set[int] = set()
    for paragraph in paragraphs:
        covered.update(range(paragraph.start, paragraph.end + 1))
    return covered
