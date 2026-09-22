from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any

from intake.adapters.writer import WriterAdapter
from intake.backfill import (
    backfill_dry_run,
    review_sheet,
    unlocated_claims,
)
from intake.budget import (
    Budget,
    BudgetExceededError,
    RunExistsError,
    new_run_id,
    run_directory,
)
from intake.extract import (
    WriterPayload,
    build_input,
    resolve_references,
    run_extract,
    strict_schema,
)
from intake.models import ExtractionRecord, Quote, finalize
from intake.numbers import (
    check_claim_dates,
    check_claim_numbers,
    extract_dates,
    extract_numbers,
)
from intake.segment import segment_content
from intake.verify_quotes import normalize_text, verify_claims, verify_quote

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "intake"


def load_fixture(record_id: str) -> ExtractionRecord:
    import yaml

    path = FIXTURES / f"{record_id}.extraction.yaml"
    return finalize(
        ExtractionRecord.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))
    )


def capture_paragraphs(record: ExtractionRecord, local_id: str):
    source = next(source for source in record.sources if source.local_id == local_id)
    content = (
        (ROOT / source.capture_manifest_path)
        .parent.joinpath("content.md")
        .read_text(encoding="utf-8")
    )
    return segment_content(content)


class QuoteVerificationTests(unittest.TestCase):
    def test_normalization_handles_unicode_marks_and_dashes(self) -> None:
        self.assertEqual(
            normalize_text("we’ve ‘shipped’ — 95%"),
            normalize_text("we've 'shipped' - 95%"),
        )
        self.assertNotEqual(normalize_text("River"), normalize_text("Roast"))

    def test_the_golden_quotes_verify_exact_in_their_captures(self) -> None:
        for record_id in ("plaid-ai-annotator", "zup-codegen", "duolingo-agentic-workflows"):
            with self.subTest(record=record_id):
                record = load_fixture(record_id)
                paragraphs = {
                    source.local_id: capture_paragraphs(record, source.local_id)
                    for source in record.sources
                }
                verified = verify_claims(record, paragraphs)
                for claim in verified.claims:
                    for quote in claim.quotes:
                        self.assertEqual(
                            quote.match,
                            "exact",
                            f"{claim.id}: {quote.text[:60]!r}",
                        )
                        self.assertIsNotNone(quote.lines)

    def test_a_curly_quote_variant_still_verifies_exact(self) -> None:
        record = load_fixture("duolingo-agentic-workflows")
        paragraphs = capture_paragraphs(record, "s1")
        claim = next(c for c in record.claims if c.id == "c-efabb5a6")
        straight = claim.quotes[0].model_copy(
            update={"text": claim.quotes[0].text.replace("’", "'")}
        )
        outcome = verify_quote(straight, paragraphs)
        self.assertEqual(outcome.match, "exact")

    def test_a_paraphrased_quote_is_fuzzy_not_exact(self) -> None:
        record = load_fixture("zup-codegen")
        paragraphs = capture_paragraphs(record, "s1")
        paraphrase = Quote(
            source="s1",
            text="string replacement edits instead of complete file rewrites",
            paragraph_id="p7",
        )
        outcome = verify_quote(paraphrase, paragraphs)
        self.assertEqual(outcome.match, "fuzzy")

    def test_an_absent_quote_is_missing(self) -> None:
        record = load_fixture("zup-codegen")
        paragraphs = capture_paragraphs(record, "s1")
        absent = Quote(source="s1", text="Zup reported a forty percent failure rate")
        outcome = verify_quote(absent, paragraphs)
        self.assertEqual(outcome.match, "missing")

    def test_an_unknown_source_marks_the_quote_missing(self) -> None:
        record = load_fixture("zup-codegen")
        verified = verify_claims(record, {})
        for claim in verified.claims:
            for quote in claim.quotes:
                self.assertEqual(quote.match, "missing")


class NumbersTests(unittest.TestCase):
    def test_percentages_counts_multipliers_and_durations_extract(self) -> None:
        text = "59,918 sessions across 5,170 channels; 95% alignment; 3.5x more; median 19 min; 1-2 days"
        values = {(number.value, number.unit) for number in extract_numbers(text)}
        self.assertIn((59918.0, "count"), values)
        self.assertIn((5170.0, "count"), values)
        self.assertIn((95.0, "percent"), values)
        self.assertIn((3.5, "multiplier"), values)
        self.assertIn((19.0, "minute"), values)

    def test_spelled_quantities_and_fractions_extract(self) -> None:
        text = "high hundreds of daily users and one in eight merged PRs"
        surfaces = [number.surface.casefold() for number in extract_numbers(text)]
        values = {number.value for number in extract_numbers(text)}
        self.assertIn("high hundreds", surfaces)
        self.assertIn(1.0, values)
        self.assertIn(8.0, values)

    def test_every_claim_number_must_appear_in_the_quote(self) -> None:
        checks = check_claim_numbers(
            "Greater than 95% human alignment across 3,000 labels",
            "greater than 95% human alignment at a fraction of cost",
        )
        by_surface = {check.claim: check.in_quote for check in checks}
        self.assertTrue(by_surface["95%"])
        self.assertFalse(by_surface["3000"])

    def test_dates_agree_with_the_quote_or_the_published_date(self) -> None:
        checks = check_claim_dates(
            "The post of June 2026 reports 95% alignment",
            "we report 95% alignment",
            "2026-06",
        )
        self.assertTrue(all(check.in_quote for check in checks))
        self.assertTrue(any(check.note for check in checks))
        missing = check_claim_dates("Since May 2025 adoption grew", "adoption grew", None)
        self.assertFalse(all(check.in_quote for check in missing))

    def test_iso_and_month_name_dates_extract(self) -> None:
        dates = extract_dates("Published 2026-05-09; updated September 2026; since 2025")
        keys = {date.key() for date in dates}
        self.assertIn((2026, 5, 9), keys)
        self.assertIn((2026, 9, None), keys)
        self.assertIn((2025, None, None), keys)


class BudgetTests(unittest.TestCase):
    def test_reservation_refuses_runs_above_the_budget(self) -> None:
        budget = Budget(budget_usd=0.50)
        budget.reserve_calls(1)
        with self.assertRaises(BudgetExceededError):
            budget.reserve_calls(2)

    def test_usage_recording_accumulates_cost(self) -> None:
        budget = Budget(budget_usd=10.0)
        budget.record_usage(1000, 1000)
        budget.record_usage(1000, 1000)
        self.assertEqual(budget.input_tokens, 2000)
        self.assertAlmostEqual(budget.cost_usd, 2000 * 2 / 1e6 + 2000 * 10 / 1e6)

    def test_run_directories_are_never_overwritten(self) -> None:
        import tempfile

        run_id = new_run_id()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = run_directory(run_id, runs_root=root)
            self.assertTrue(first.is_dir())
            with self.assertRaises(RunExistsError):
                run_directory(run_id, runs_root=root)


class FakeResponses:
    """The writer seam: canned payloads in sequence."""

    def __init__(self, payloads: list[dict[str, Any]]) -> None:
        self._payloads = list(payloads)

    def create(self, **kwargs: Any) -> Any:
        return FakeResponse(self._payloads.pop(0))


class FakeResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self._payload = payload
        self.output_text = json.dumps(payload)
        self.usage = type("Usage", (), {"input_tokens": 1000, "output_tokens": 500})()
        self.model = "gpt-6-sol-2026-09-22"


def writer_payload_for_zup() -> dict[str, Any]:
    """A minimal writer reply shaped like the zup fixture's claims."""
    return {
        "candidate": {
            "company": "Zup",
            "system_name": "CodeGen",
            "record_id": "zup-codegen",
            "decision": "update",
        },
        "classification": {
            "approach_type": "agent",
            "deployment_stage": "research",
            "year": 2026,
            "domains": ["coding"],
            "rubric": {
                "invocation": ["unknown"],
                "state": "unknown",
                "identity": "unknown",
                "evidence_strength": "detailed-primary",
            },
            "operating_models": [
                {
                    "scope": "constrained coding task → human-supervised edit",
                    "attention_boundary": "unknown",
                    "claim_ids": ["#1"],
                }
            ],
            "agent_name": "CodeGen",
        },
        "claims": [
            {
                "field": "summary",
                "text": "CodeGen is Zup's internal coding agent.",
                "kind": "fact",
                "provenance": "reported",
                "quotes": [
                    {
                        "source": "s1",
                        "text": "We present CodeGen, an internal coding agent at Zup",
                        "paragraph_id": "p3",
                        "match": "missing",
                    }
                ],
                "disposition": "accept",
            },
            {
                "field": "operating_models[]",
                "text": "Progressive human oversight modes are reported without defined boundaries",
                "kind": "fact",
                "provenance": "reported",
                "quotes": [
                    {
                        "source": "s1",
                        "text": "while progressive human oversight modes drove organic adoption without mandating trust",
                        "paragraph_id": "p3",
                        "match": "missing",
                    }
                ],
                "disposition": "accept",
            },
        ],
        "questions": {"purpose": {"claim_ids": ["#0"]}},
    }


class WriterAdapterTests(unittest.TestCase):
    def test_every_result_carries_the_input_hash_and_replays_keep_it(self) -> None:
        import tempfile

        from intake.adapters.writer import WriterAdapter
        from intake.cache import JsonCache

        schema = {
            "type": "object",
            "properties": {"found": {"type": "boolean"}},
            "required": ["found"],
            "additionalProperties": False,
        }

        class SameReply:
            def create(self, **kwargs: Any) -> Any:
                return FakeResponse({"found": True})

        with tempfile.TemporaryDirectory() as directory:
            cache = JsonCache(Path(directory) / "writer.json")
            adapter = WriterAdapter(api_key="test-key", responses=SameReply())
            budget = Budget(budget_usd=10.0)
            call = dict(
                instructions="Find the quote.",
                schema=schema,
                schema_name="quote",
            )
            first = adapter.complete_json(
                input_text="paragraph one", budget=budget, cache=cache, **call
            )
            second = adapter.complete_json(
                input_text="paragraph one", budget=budget, cache=cache, **call
            )
            self.assertFalse(first.cache_hit)
            self.assertTrue(second.cache_hit)
            # The replayed call names the same inputs it originally read.
            self.assertRegex(first.input_sha256, r"^[0-9a-f]{64}$")
            self.assertEqual(first.input_sha256, second.input_sha256)
            changed = adapter.complete_json(
                input_text="paragraph two", budget=budget, cache=cache, **call
            )
            self.assertFalse(changed.cache_hit)
            self.assertNotEqual(first.input_sha256, changed.input_sha256)


class ExtractStageTests(unittest.TestCase):
    def setUp(self) -> None:
        import yaml

        from intake.models import StagedSource

        self.fixture = load_fixture("zup-codegen")
        payload = yaml.safe_load(
            (FIXTURES / "zup-codegen.extraction.yaml").read_text(encoding="utf-8")
        )
        self.sources = [
            StagedSource.model_validate(
                source
                | {
                    "content_sha256": source["content_sha256"],
                    "captured_at": source.get("captured_at"),
                }
            )
            for source in payload["sources"]
        ]

    def test_strict_schema_requires_every_key(self) -> None:
        schema = strict_schema(WriterPayload)
        self.assertEqual(
            schema["required"],
            ["candidate", "classification", "claims", "questions"],
        )

    def test_run_extract_resolves_positional_references(self) -> None:
        adapter = WriterAdapter(
            api_key="test-key", responses=FakeResponses([writer_payload_for_zup()])
        )
        budget = Budget(budget_usd=1.0)
        paragraphs = capture_paragraphs(self.fixture, "s1")
        record, stage = run_extract(
            run_id="2026-09-22T19:40:11Z-3f9a",
            paragraphs_by_source={"s1": paragraphs},
            sources=self.sources,
            hints={"company": "Zup"},
            adapter=adapter,
            budget=budget,
        )
        self.assertEqual(stage["model"], "gpt-6-sol-2026-09-22")
        self.assertEqual(stage["calls"], 1)
        operating = record.classification.operating_models[0]
        self.assertTrue(operating.claim_ids[0].startswith("c-"))
        self.assertTrue(
            record.questions is not None and record.questions.purpose.claim_ids[0].startswith("c-")
        )

    def test_a_schema_violation_retries_once(self) -> None:
        bad = writer_payload_for_zup() | {"claims": "not a list"}
        good = writer_payload_for_zup()
        adapter = WriterAdapter(api_key="test-key", responses=FakeResponses([bad, good]))
        budget = Budget(budget_usd=1.0)
        paragraphs = capture_paragraphs(self.fixture, "s1")
        _record, stage = run_extract(
            run_id="2026-09-22T19:40:11Z-3f9a",
            paragraphs_by_source={"s1": paragraphs},
            sources=self.sources,
            adapter=adapter,
            budget=budget,
        )
        self.assertEqual(stage["calls"], 2)

    def test_a_second_violation_fails_the_stage(self) -> None:
        bad = writer_payload_for_zup() | {"claims": "not a list"}
        adapter = WriterAdapter(api_key="test-key", responses=FakeResponses([bad, dict(bad)]))
        budget = Budget(budget_usd=1.0)
        from intake.extract import ExtractionStageError

        with self.assertRaises(ExtractionStageError):
            run_extract(
                run_id="2026-09-22T19:40:11Z-3f9a",
                paragraphs_by_source={"s1": capture_paragraphs(self.fixture, "s1")},
                sources=self.sources,
                adapter=adapter,
                budget=budget,
            )

    def test_the_input_payload_carries_paragraphs_not_instructions(self) -> None:
        paragraphs = capture_paragraphs(self.fixture, "s1")
        payload = json.loads(
            build_input(
                paragraphs_by_source={"s1": paragraphs},
                sources=self.sources,
                hints={"company": "Zup"},
            )
        )
        self.assertIn("paragraphs", payload)
        self.assertEqual(payload["candidate"], {"company": "Zup"})
        self.assertEqual(payload["sources"][0]["local_id"], "s1")


class ResolveReferenceTests(unittest.TestCase):
    def test_resolve_references_rewrites_every_positional_form(self) -> None:
        record = load_fixture("zup-codegen")
        claims = [claim.model_copy(update={"id": None}) for claim in record.claims]
        record = record.model_copy(update={"claims": claims})
        record = finalize(record)
        resolved = resolve_references(record)
        ids = {claim.id for claim in resolved.claims}
        for answer in (
            resolved.questions.purpose,
            resolved.questions.lessons,
        ):
            for reference in answer.claim_ids:
                self.assertIn(reference, ids)


class BackfillTests(unittest.TestCase):
    def test_unlocated_claims_finds_the_paths_without_locators(self) -> None:
        import yaml

        record = yaml.safe_load(
            (ROOT / "data" / "agents" / "zup-codegen.yaml").read_text(encoding="utf-8")
        )
        paths = unlocated_claims(record)
        self.assertIn("summary" if "summary" in paths else paths[0], paths)
        self.assertNotIn("primitives.0", paths)

    def test_a_dry_run_proposes_only_verified_quotes(self) -> None:
        record_path = ROOT / "data" / "agents" / "zup-codegen.yaml"

        class FoundResponses:
            def __init__(self) -> None:
                self.calls = 0

            def create(self, **kwargs: Any) -> Any:
                self.calls += 1
                payload = {
                    "found": True,
                    "source": "zup-codegen-source-1",
                    "quote": "an internal coding agent at Zup",
                    "paragraph_id": "p3",
                }
                return FakeResponse(payload)

        adapter = WriterAdapter(api_key="test-key", responses=FoundResponses())
        budget = Budget(budget_usd=10.0)
        report = backfill_dry_run(record_path, adapter=adapter, budget=budget)
        self.assertGreater(report["unlocated_claims"], 0)
        self.assertGreater(report["verified"], 0)
        sheet = review_sheet(report)
        self.assertIn("Backfill dry run", sheet)
        self.assertIn("Preserved content.md", sheet)

    def test_a_not_found_reply_leaves_no_proposal(self) -> None:
        record_path = ROOT / "data" / "agents" / "zup-codegen.yaml"

        class NotFoundResponses:
            def create(self, **kwargs: Any) -> Any:
                return FakeResponse(
                    {
                        "found": False,
                        "source": "zup-codegen-source-1",
                        "quote": "",
                        "paragraph_id": "",
                    }
                )

        adapter = WriterAdapter(api_key="test-key", responses=NotFoundResponses())
        report = backfill_dry_run(record_path, adapter=adapter, budget=Budget(budget_usd=10.0))
        self.assertEqual(report["verified"], 0)
        self.assertEqual(report["proposals"], [])


if __name__ == "__main__":
    unittest.main()
