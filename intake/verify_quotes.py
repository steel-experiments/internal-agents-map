# ABOUTME: Stage 5 of the intake pipeline: find each quote in its capture (Plan 017).
# ABOUTME: A quote that is not found is a failed extraction, never a locator.
"""Verify that every claim quote exists verbatim in the immutable capture.

Both sides are normalised: Unicode compatibility forms, curly quotation marks,
dashes, and whitespace. A normalised containment inside the capture marks the
quote ``exact`` with its line range. A near match at or above the similarity
bound inside the named paragraph marks it ``fuzzy``, which sends the claim to
review. Anything else is ``missing``.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher

from intake.models import Quote
from intake.segment import Paragraph

# A near match at or above this bound inside the named paragraph is "fuzzy",
# which sends the claim to review; below it the quote is "missing". The bound
# is deliberately loose: fuzzy only downgrades a claim to review, never accepts.
DEFAULT_SIMILARITY_BOUND = 0.7

_QUOTE_MAP = {
    "‘": "'",
    "’": "'",
    "“": '"',
    "”": '"',
    "′": "'",
    "″": '"',
    "«": '"',
    "»": '"',
}
_DASH_MAP = {
    "‐": "-",
    "‑": "-",
    "‒": "-",
    "–": "-",
    "—": "-",
    "―": "-",
    "−": "-",
    "∓": "-",
    "∕": "/",
}
_WHITESPACE_RE = re.compile(r"\s+")


def normalize_text(value: str) -> str:
    """Normalise one side of the comparison: form, marks, dashes, whitespace."""
    formed = unicodedata.normalize("NFKC", value)
    for mark, replacement in _QUOTE_MAP.items():
        formed = formed.replace(mark, replacement)
    for mark, replacement in _DASH_MAP.items():
        formed = formed.replace(mark, replacement)
    collapsed = _WHITESPACE_RE.sub(" ", formed).strip()
    return collapsed.casefold()


@dataclass(frozen=True)
class QuoteMatch:
    """The verification outcome for one quote."""

    match: str
    lines: tuple[int, int] | None
    paragraph_id: str | None
    similarity: float | None


def _find_exact(
    quote: str, paragraphs: list[Paragraph]
) -> tuple[tuple[int, int] | None, str | None]:
    """Find the smallest line window whose normalised text contains the quote."""
    needle = normalize_text(quote)
    if not needle:
        return None, None
    best: tuple[int, int] | None = None
    best_paragraph: str | None = None
    for paragraph in paragraphs:
        normalized_lines = [normalize_text(line) for line in paragraph.text.splitlines()]
        for start in range(len(normalized_lines)):
            window: list[str] = []
            for end in range(start, len(normalized_lines)):
                window.append(normalized_lines[end])
                joined = " ".join(part for part in window if part)
                if len(joined) >= len(needle):
                    if needle in joined:
                        span = (paragraph.start + start, paragraph.start + end)
                        if best is None or (span[1] - span[0]) < (best[1] - best[0]):
                            best = span
                            best_paragraph = paragraph.id
                    break
        if best is not None:
            continue
    return best, best_paragraph


def _loose_key(value: str) -> str:
    """The similarity-side normalization: hyphenation varies between writers."""
    return normalize_text(value).replace("-", " ")


def _similarity(quote: str, text: str) -> float:
    """The best ratio of the quote against any same-length word window of the text."""
    left = _loose_key(quote)
    right = _loose_key(text)
    if not left or not right:
        return 0.0
    quote_words = left.split()
    text_words = right.split()
    if not quote_words or not text_words:
        return 0.0
    best = 0.0
    widths = range(
        max(2, len(quote_words) - 1),
        min(len(text_words), len(quote_words) + 2) + 1,
    )
    for width in widths:
        for start in range(0, max(1, len(text_words) - width + 1)):
            window = " ".join(text_words[start : start + width])
            best = max(best, SequenceMatcher(None, left, window).ratio())
    if not widths:
        best = SequenceMatcher(None, left, right).ratio()
    return best


def verify_quote(
    quote: Quote,
    paragraphs: list[Paragraph],
    *,
    similarity_bound: float = DEFAULT_SIMILARITY_BOUND,
) -> QuoteMatch:
    """Verify one quote against the segmented capture."""
    lines, paragraph_id = _find_exact(quote.text, paragraphs)
    if lines is not None:
        return QuoteMatch("exact", lines, paragraph_id, 1.0)
    named = [
        paragraph
        for paragraph in paragraphs
        if quote.paragraph_id is not None and paragraph.id == quote.paragraph_id
    ]
    candidates = named or paragraphs
    scored = [(_similarity(quote.text, paragraph.text), paragraph) for paragraph in candidates]
    ratio, best_paragraph = max(scored, key=lambda pair: pair[0])
    if ratio >= similarity_bound:
        return QuoteMatch(
            "fuzzy", (best_paragraph.start, best_paragraph.end), best_paragraph.id, ratio
        )
    return QuoteMatch("missing", None, None, ratio)


def verify_claims(
    record,
    captures: dict[str, list[Paragraph]],
    *,
    similarity_bound: float = DEFAULT_SIMILARITY_BOUND,
):
    """Verify every quote of every claim; returns the record with updated quotes.

    Accepts and returns an :class:`~intake.models.ExtractionRecord`; quotes gain
    their match, lines, and paragraph id. Claim IDs stay untouched.
    """

    claims = []
    for claim in record.claims:
        quotes = []
        for quote in claim.quotes:
            if quote.source not in captures:
                quotes.append(quote.model_copy(update={"match": "missing", "lines": None}))
                continue
            outcome = verify_quote(quote, captures[quote.source], similarity_bound=similarity_bound)
            quotes.append(
                quote.model_copy(
                    update={
                        "match": outcome.match,
                        "lines": outcome.lines,
                        "paragraph_id": outcome.paragraph_id,
                    }
                )
            )
        claims.append(claim.model_copy(update={"quotes": quotes}))
    return record.model_copy(update={"claims": claims})
