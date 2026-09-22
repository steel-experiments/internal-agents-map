from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any

import yaml

from intake.models import ExtractionRecord, finalize
from intake.privacy import PrivateDataError, assert_clean, find_contact_data

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "intake"


def load_fixture(record_id: str) -> ExtractionRecord:
    payload = yaml.safe_load(
        (FIXTURES / f"{record_id}.extraction.yaml").read_text(encoding="utf-8")
    )
    return finalize(ExtractionRecord.model_validate(payload))


class FindContactDataTests(unittest.TestCase):
    def test_an_e_mail_in_any_string_is_found_with_its_path(self) -> None:
        payload = {"claims": [{"text": "contact jane@example.org for details"}]}
        self.assertEqual(find_contact_data(payload), ["claims.0.text: jane@example.org"])

    def test_nested_lists_and_none_are_walked_safely(self) -> None:
        payload = {"a": [None, 3, {"b": ("x@y.co.uk",)}], "c": None}
        self.assertEqual(find_contact_data(payload), ["a.2.b.0: x@y.co.uk"])

    def test_authors_lists_are_exempt(self) -> None:
        payload = {"sources": [{"authors": ["ops@example.com"], "title": "A page"}]}
        self.assertEqual(find_contact_data(payload), [])

    def test_plain_text_without_addresses_is_clean(self) -> None:
        self.assertEqual(find_contact_data({"text": "The agent ships edits for review."}), [])


class AssertCleanTests(unittest.TestCase):
    def test_a_finding_stops_with_the_label_and_the_path(self) -> None:
        with self.assertRaises(PrivateDataError) as caught:
            assert_clean({"summary": "mail helpdesk@corp.example"}, label="run-1 stage 4")
        self.assertIn("run-1 stage 4", str(caught.exception))
        self.assertIn("summary: helpdesk@corp.example", str(caught.exception))

    def test_clean_payloads_pass(self) -> None:
        assert_clean({"summary": "No contact data here."}, label="run-1")


class GoldenFixtureTests(unittest.TestCase):
    def test_the_golden_extraction_records_carry_no_contact_data(self) -> None:
        for path in sorted(FIXTURES.glob("*.extraction.yaml")):
            record = finalize(
                ExtractionRecord.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))
            )
            assert_clean(json.loads(record.model_dump_json()), label=path.name)


class RunGuardTests(unittest.TestCase):
    """The STOP line: a writer reply with contact data stops the run."""

    def test_a_claim_text_with_an_e_mail_stops_stage_four(self) -> None:
        import tempfile

        from intake.adapters.steel import SteelSdkAdapter
        from intake.adapters.writer import WriterAdapter
        from intake.budget import Budget
        from intake.cache import JsonCache
        from intake.run import QueueEntry, run_candidate
        from tests.test_intake_run import FakeSteelClient, ZupWriterResponses, zup_capture_markdown

        class PoisonedResponses(ZupWriterResponses):
            def create(self, **kwargs: Any) -> Any:
                response = super().create(**kwargs)
                payload = json.loads(response.output_text)
                payload["claims"][0]["text"] += " Ask jane@example.org."
                response.output_text = json.dumps(payload)
                return response

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            markdown = zup_capture_markdown()
            steel = SteelSdkAdapter(
                api_key="test-key", client_factory=lambda _key: FakeSteelClient(markdown)
            )
            with self.assertRaises(PrivateDataError) as caught:
                run_candidate(
                    QueueEntry(
                        urls=["https://arxiv.org/abs/2604.09805"],
                        company="Zup",
                        system_name="CodeGen",
                        record_id="zup-codegen-draft",
                    ),
                    budget=Budget(budget_usd=5.0),
                    steel=steel,
                    writer=WriterAdapter(api_key="test-key", responses=PoisonedResponses()),
                    cache=JsonCache(root / "cache.json"),
                    runs_root=root / "runs",
                    drafts_root=root / "drafts",
                    staging_root=root / "staging",
                )
            self.assertIn("stage 4", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
