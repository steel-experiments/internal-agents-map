from __future__ import annotations

import unittest
from pathlib import Path
from typing import Any

import yaml

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
        quotes=[Quote(source="s1", text=text, paragraph_id="p1", match="exact", lines=(18, 18))],
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
        self.assertTrue(flags[0]["quotes"])

    def test_a_conflict_renders_as_a_contradicts_link_on_the_existing_claim(self) -> None:
        from intake.catalog import load_build
        from intake.models import ExtractionRecord, finalize
        from intake.render import render_extraction

        payload = yaml.safe_load(
            (ROOT / "tests" / "fixtures" / "intake" / "zup-codegen.extraction.yaml").read_text(
                encoding="utf-8"
            )
        )
        quote = dict(payload["claims"][0]["quotes"][0])
        payload["claims"].append(
            {
                "field": "lessons_learned[]",
                "text": "The agent serves 4000 users.",
                "kind": "fact",
                "provenance": "reported",
                "quotes": [quote],
                "disposition": "accept",
            }
        )
        rebuilt = finalize(ExtractionRecord.model_validate(payload))
        rebuilt = rebuilt.model_copy(
            update={
                "sources": [
                    source.model_copy(update={"capture_manifest_path": None})
                    for source in rebuilt.sources
                ]
            }
        )
        # A synthetic existing record with a numbered lesson proves the flag.
        synthetic = {
            "id": "zup-codegen",
            "summary": "A record.",
            "operating_models": [{"scope": "a task", "attention_boundary": "unknown"}],
            "lessons_learned": ["The agent serves 3500 users."],
            "sources": [{"id": "zup-codegen-source-1"}],
        }
        flags = number_conflicts(synthetic, rebuilt)
        self.assertEqual([flag["claim_path"] for flag in flags], ["lessons_learned.0"])
        self.assertTrue(flags[0]["quotes"])
        # The real record proves the rendered link and the validation.
        existing = yaml.safe_load(
            (ROOT / "data" / "agents" / "zup-codegen.yaml").read_text(encoding="utf-8")
        )
        merged = render_extraction(
            rebuilt,
            reviewed_at="2026-09-22",
            existing=existing,
            contradictions=[
                {"claim_path": "lessons_learned.0", "quotes": [{"source": "s1", "lines": [18, 18]}]}
            ],
        )
        links = merged.record["evidence"]["lessons_learned.0"]
        self.assertEqual(links[-1]["relation"], "contradicts")
        self.assertEqual(links[-1]["source_id"], "zup-codegen-source-2")
        self.assertIn("Preserved content.md", links[-1]["locator"])
        # The merged record with its contradiction link still validates.
        load_build().validate_record(merged.record, Path("zup-codegen.yaml"), set())

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
