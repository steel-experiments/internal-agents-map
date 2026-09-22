from __future__ import annotations

import unittest
from pathlib import Path
from typing import Any

from intake.crosscheck import load_existing, number_conflicts, source_count
from intake.models import Claim, Quote

ROOT = Path(__file__).resolve().parents[1]


def record_with_summary(summary: str) -> dict[str, Any]:
    """A minimal authored record the cross checks can read."""
    return {
        "id": "crosscheck-example",
        "summary": summary,
        "operating_models": [{"scope": "a task", "attention_boundary": "unknown"}],
        "sources": [{"id": "crosscheck-example-source-1"}],
    }


def claim(text: str) -> Claim:
    return Claim(
        field="summary",
        text=text,
        kind="fact",
        provenance="reported",
        quotes=[Quote(source="s1", text=text, paragraph_id="p1")],
        disposition="review",
    )


def extraction(claims: list[Claim]) -> Any:
    """The zup fixture with the test's claims appended.

    The fixture's own claims stay: its operating models reference their IDs,
    and none of them match the synthetic existing record below.
    """
    import yaml

    from intake.models import ExtractionRecord

    payload = yaml.safe_load(
        (ROOT / "tests" / "fixtures" / "intake" / "zup-codegen.extraction.yaml").read_text(
            encoding="utf-8"
        )
    )
    payload["claims"] = list(payload["claims"]) + [claim.model_dump() for claim in claims]
    return ExtractionRecord.model_validate(payload)


class LoadExistingTests(unittest.TestCase):
    def test_a_known_record_id_loads(self) -> None:
        existing = load_existing("zup-codegen")
        self.assertIsNotNone(existing)
        self.assertEqual(existing["id"], "zup-codegen")  # type: ignore[index]

    def test_an_unknown_record_id_loads_nothing(self) -> None:
        self.assertIsNone(load_existing("no-such-record"))
        self.assertIsNone(load_existing(None))

    def test_the_source_count_feeds_the_renderer(self) -> None:
        self.assertEqual(source_count(load_existing("zup-codegen") or {}), 1)


class NumberConflictTests(unittest.TestCase):
    def test_agreeing_numbers_produce_no_flag(self) -> None:
        existing = record_with_summary("The agent serves 3500 users.")
        flags = number_conflicts(existing, extraction([claim("The agent serves 3500 users.")]))
        self.assertEqual(flags, [])

    def test_differing_numbers_are_flagged_with_both_values(self) -> None:
        existing = record_with_summary("The agent serves 3500 users.")
        flags = number_conflicts(existing, extraction([claim("The agent serves 4000 users.")]))
        self.assertEqual(len(flags), 1)
        self.assertEqual(flags[0]["claim_path"], "summary")
        self.assertEqual(flags[0]["issue"], "numbers differ")
        self.assertEqual(flags[0]["existing"], [3500])
        self.assertEqual(flags[0]["new"], [4000])

    def test_a_dropped_number_is_flagged_softly(self) -> None:
        existing = record_with_summary("The agent serves 3500 users.")
        flags = number_conflicts(existing, extraction([claim("The agent serves")]))
        self.assertEqual(len(flags), 1)
        self.assertEqual(flags[0]["issue"], "the new claim drops the recorded numbers")
        self.assertEqual(flags[0]["new"], [])

    def test_an_unmatched_claim_is_not_flagged(self) -> None:
        existing = record_with_summary("The agent serves 3500 users.")
        flags = number_conflicts(
            existing, extraction([claim("The harness runs edits in a sandbox.")])
        )
        self.assertEqual(flags, [])


if __name__ == "__main__":
    unittest.main()
