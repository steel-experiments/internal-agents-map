# ABOUTME: Stage 7 of the intake pipeline: numeric and date agreement (Plan 017).
# ABOUTME: Code owns numbers and dates; every claim number must appear in its quote.
"""Check that the numbers and dates in a claim agree with its quote.

Extraction covers percentages, counts with separators, ratios and multipliers,
durations, spelled quantities such as ``high hundreds`` or ``one in eight``,
and calendar dates. Every number in the claim must appear in the quote. A date
in the claim must appear in the quote or equal the source's published date,
and the fallback is flagged in a note.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from intake.models import NumberCheck

_NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "dozen": 12,
    "dozens": 12,
    "hundreds": 100,
    "thousands": 1000,
    "millions": 1_000_000,
}
# Quantities the catalog spells out instead of digitising; matched as phrases.
_SPELLED_QUANTITY_RE = re.compile(
    r"\b(?:high|low|several|a few|some|hundreds of|thousands of|millions of)\s+"
    r"(?:dozen|dozens|hundred|hundreds|thousand|thousands|million|millions)\b",
    re.IGNORECASE,
)
_FRACTION_RE = re.compile(
    r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+in\s+(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\b",
    re.IGNORECASE,
)
_PERCENT_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*(?:%|percent|per cent)(?!\w)", re.IGNORECASE)
_MULTIPLIER_RE = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*[x×](?!\w)|(?<=\s)(\d+(?:\.\d+)?)\s*(?:fold|times)\b", re.IGNORECASE
)
_COUNT_RE = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(?![\w%])")
# Canonical duration units and the abbreviations sources use for them.
_DURATION_UNITS = {
    "sec": "second",
    "secs": "second",
    "second": "second",
    "seconds": "second",
    "min": "minute",
    "mins": "minute",
    "minute": "minute",
    "minutes": "minute",
    "hr": "hour",
    "hrs": "hour",
    "hour": "hour",
    "hours": "hour",
    "day": "day",
    "days": "day",
    "wk": "week",
    "wks": "week",
    "week": "week",
    "weeks": "week",
    "mo": "month",
    "mos": "month",
    "month": "month",
    "months": "month",
    "qtr": "quarter",
    "qtrs": "quarter",
    "quarter": "quarter",
    "quarters": "quarter",
    "yr": "year",
    "yrs": "year",
    "year": "year",
    "years": "year",
}
_DURATION_RE = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*(" + "|".join(_DURATION_UNITS) + r")\b",
    re.IGNORECASE,
)
_MONTHS = "january february march april may june july august september october november december"
_ISO_DATE_RE = re.compile(r"\b(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?\b")
_MONTH_YEAR_RE = re.compile(rf"\b({'|'.join(_MONTHS.split())})\s+(\d{{4}})\b", re.IGNORECASE)


def _normalize_digits(value: str) -> str:
    formed = unicodedata.normalize("NFKC", value)
    return formed.replace(",", "").replace("٪", "%")


def _as_number(token: str) -> float | None:
    try:
        return float(token)
    except ValueError:
        lowered = token.lower()
        if lowered in _NUMBER_WORDS:
            return float(_NUMBER_WORDS[lowered])
        return None


@dataclass(frozen=True)
class ExtractedNumber:
    """One number found in a text, with its surface form."""

    value: float
    surface: str
    unit: str | None = None


def extract_numbers(text: str) -> list[ExtractedNumber]:
    """Extract every number, percentage, ratio, duration, and spelled quantity."""
    text = _normalize_digits(text)
    found: list[ExtractedNumber] = []

    def push(value: float, surface: str, unit: str | None = None) -> None:
        found.append(ExtractedNumber(value=value, surface=surface, unit=unit))

    for match in _PERCENT_RE.finditer(text):
        value = _as_number(match.group(1))
        if value is not None:
            push(value, match.group(0), "percent")
    for match in _MULTIPLIER_RE.finditer(text):
        token = match.group(1) or match.group(2)
        value = _as_number(token) if token else None
        if value is not None:
            push(value, match.group(0), "multiplier")
    for match in _DURATION_RE.finditer(text):
        value = _as_number(match.group(1))
        if value is not None:
            unit = _DURATION_UNITS[match.group(2).lower()]
            push(value, match.group(0), unit)
    for match in _FRACTION_RE.finditer(text):
        for group in (match.group(1), match.group(2)):
            value = _as_number(group)
            if value is not None:
                push(value, group, "fraction-part")
    for match in _COUNT_RE.finditer(text):
        value = _as_number(match.group(1))
        if value is not None:
            push(value, match.group(1), "count")
    for match in _SPELLED_QUANTITY_RE.finditer(text):
        push(float("inf"), match.group(0), "spelled-quantity")
    return found


@dataclass(frozen=True)
class ExtractedDate:
    """One date found in a text."""

    surface: str
    year: int
    month: int | None
    day: int | None

    def key(self) -> tuple[int, int | None, int | None]:
        return (self.year, self.month, self.day)


def extract_dates(text: str) -> list[ExtractedDate]:
    """Extract ISO dates and month-name dates."""
    text = _normalize_digits(text)
    found: list[ExtractedDate] = []
    masked = text
    for match in _MONTH_YEAR_RE.finditer(text):
        month = _MONTHS.split().index(match.group(1).lower()) + 1
        found.append(
            ExtractedDate(surface=match.group(0), year=int(match.group(2)), month=month, day=None)
        )
        # Mask the span so the ISO pass does not re-extract the bare year.
        masked = (
            masked[: match.start()] + " " * (match.end() - match.start()) + masked[match.end() :]
        )
    for match in _ISO_DATE_RE.finditer(masked):
        year = int(match.group(1))
        if not 1990 <= year <= 2100:
            continue
        month = int(match.group(2)) if match.group(2) else None
        day = int(match.group(3)) if match.group(3) else None
        found.append(ExtractedDate(surface=match.group(0), year=year, month=month, day=day))
    return found


def _value_key(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return repr(value)


def check_claim_numbers(claim_text: str, quote_text: str) -> list[NumberCheck]:
    """Check every number in the claim against the quote's numbers."""
    claim_numbers = extract_numbers(claim_text)
    quote_numbers = extract_numbers(quote_text)
    quote_keys = {_value_key(number.value) for number in quote_numbers}
    quote_units = {number.unit for number in quote_numbers}
    checks: list[NumberCheck] = []
    for number in claim_numbers:
        key = _value_key(number.value)
        in_quote = key in quote_keys
        note = None
        if in_quote and number.unit is not None and number.unit not in quote_units:
            note = f"Value {key} appears in the quote with a different unit."
        if number.unit == "spelled-quantity":
            in_quote = number.surface.casefold() in quote_text.casefold()
        checks.append(NumberCheck(claim=number.surface, in_quote=in_quote, note=note))
    return checks


def check_claim_dates(
    claim_text: str, quote_text: str, published_at: str | None
) -> list[NumberCheck]:
    """Check every date in the claim against the quote and the published date."""
    quote_keys = {date.key() for date in extract_dates(quote_text)}
    published_key = None
    if published_at:
        parts = [int(part) for part in published_at.split("-")]
        parts += [None] * (3 - len(parts))
        published_key = (parts[0], parts[1], parts[2])
    checks: list[NumberCheck] = []
    for date in extract_dates(claim_text):
        note = None
        in_quote = date.key() in quote_keys
        if not in_quote and published_key is not None and date.key() == published_key:
            in_quote = True
            note = "The date matches the source's published date, not a quoted passage."
        checks.append(NumberCheck(claim=date.surface, in_quote=in_quote, note=note))
    return checks


def check_claim(claim_text: str, quotes: list[tuple[str, str | None]]) -> list[NumberCheck]:
    """Check numbers and dates of one claim against its exact quotes.

    ``quotes`` holds ``(quote_text, published_at)`` pairs; a number agrees when
    it appears in any quote, a date when it appears in a quote or equals that
    source's published date.
    """
    number_checks = []
    for quote_text, _published in quotes:
        number_checks = check_claim_numbers(claim_text, quote_text)
        if all(check.in_quote for check in number_checks):
            return number_checks
    date_checks: list[NumberCheck] = []
    for quote_text, published in quotes:
        date_checks = check_claim_dates(claim_text, quote_text, published)
        if all(check.in_quote for check in date_checks):
            return date_checks
    return number_checks + date_checks
