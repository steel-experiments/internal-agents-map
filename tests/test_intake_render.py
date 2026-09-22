from __future__ import annotations

import unittest
from pathlib import Path

import yaml

from intake.catalog import load_build
from intake.models import ExtractionRecord, finalize
from intake.render import RenderError, render_extraction

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "intake"
DATA = ROOT / "data" / "agents"

GOLDEN = [
    ("plaid-ai-annotator", "agent with metrics"),
    ("zup-codegen", "agent with lessons"),
    ("duolingo-agentic-workflows", "platform"),
]
REVIEWED_AT = "2026-09-22"


def load_fixture(record_id: str) -> ExtractionRecord:
    path = FIXTURES / f"{record_id}.extraction.yaml"
    return finalize(
        ExtractionRecord.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))
    )


def capture_window(record: ExtractionRecord, local_id: str, start: int, end: int) -> str:
    source = next(source for source in record.sources if source.local_id == local_id)
    content = (
        (ROOT / source.capture_manifest_path)
        .parent.joinpath("content.md")
        .read_text(encoding="utf-8")
    )
    return "\n".join(content.splitlines()[start - 1 : end])


class GoldenRenderTests(unittest.TestCase):
    """Three hand-written extraction records render to valid authored YAML."""

    def setUp(self) -> None:
        self.build = load_build()

    def render(self, record_id: str):
        record = load_fixture(record_id)
        return record, render_extraction(record, reviewed_at=REVIEWED_AT)

    def test_the_build_validators_accept_every_golden_draft(self) -> None:
        for record_id, shape in GOLDEN:
            with self.subTest(record=record_id, shape=shape):
                _record, result = self.render(record_id)
                parsed = yaml.safe_load(result.record_yaml)
                self.build.validate_record(parsed, Path(f"{record_id}.yaml"), set())

    def test_every_evidence_link_carries_a_locator(self) -> None:
        for record_id, _shape in GOLDEN:
            with self.subTest(record=record_id):
                _record, result = self.render(record_id)
                parsed = yaml.safe_load(result.record_yaml)
                self.assertTrue(parsed["evidence"])
                for path, links in parsed["evidence"].items():
                    for link in links:
                        self.assertIn(
                            "locator",
                            link,
                            f"evidence link for {path} has no locator",
                        )

    def test_every_exact_quote_is_found_in_its_capture_at_its_lines(self) -> None:
        for record_id, _shape in GOLDEN:
            with self.subTest(record=record_id):
                record, _result = self.render(record_id)
                for claim in record.claims:
                    for quote in claim.quotes:
                        if quote.match != "exact":
                            continue
                        start, end = quote.lines or (0, 0)
                        window = capture_window(record, quote.source, start, end)
                        self.assertIn(
                            quote.text,
                            window,
                            f"quote for {claim.id} not found at lines {start}-{end}",
                        )

    def test_rendering_is_deterministic(self) -> None:
        for record_id, _shape in GOLDEN:
            with self.subTest(record=record_id):
                record = load_fixture(record_id)
                first = render_extraction(record, reviewed_at=REVIEWED_AT)
                second = render_extraction(record, reviewed_at=REVIEWED_AT)
                self.assertEqual(first.record_yaml, second.record_yaml)
                self.assertEqual(first.compatibility, second.compatibility)

    def test_the_compatibility_map_covers_every_accepted_claim(self) -> None:
        record, result = self.render("zup-codegen")
        accepted = {claim.id for claim in record.claims if claim.disposition == "accept"}
        self.assertEqual(set(result.compatibility), accepted)
        paths = [path for paths in result.compatibility.values() for path in paths]
        parsed = yaml.safe_load(result.record_yaml)
        self.assertEqual(set(paths), set(parsed["evidence"]))

    def test_the_golden_shapes_render_their_distinct_blocks(self) -> None:
        _record, plaid = self.render("plaid-ai-annotator")
        self.assertIn("headline_metric", plaid.record)
        self.assertIn("page_content", plaid.record)
        observations = plaid.record["page_content"]["observations"]
        self.assertIn("headline_metric", observations)
        self.assertEqual(observations["key_metrics.0"]["duplicate_of"], "headline_metric")
        _record, zup = self.render("zup-codegen")
        self.assertNotIn("headline_metric", zup.record)
        self.assertEqual(zup.record["page_content"]["observations"], {})
        _record, duolingo = self.render("duolingo-agentic-workflows")
        self.assertEqual(duolingo.record["approach_type"], "platform")
        self.assertEqual(
            duolingo.record["page_content"]["primitive_roles"],
            {"primitives.0": "workflow", "primitives.1": "workflow"},
        )
        self.assertEqual(
            duolingo.record["page_content"]["workflow_scope"],
            "prompt drafted and tested with a coding agent → workflow form merged into "
            "the internal tool list",
        )

    def test_operating_model_claims_get_their_required_metadata(self) -> None:
        _record, result = self.render("plaid-ai-annotator")
        entry = result.record["claim_metadata"]["operating_models.0"]
        self.assertEqual(entry["kind"], "inference")
        self.assertEqual(entry["provenance"], "catalog-judgment")
        for field in ("confidence", "confidence_reason", "valid_at"):
            self.assertIn(field, entry)

    def test_pipeline_silence_becomes_not_reviewed_never_unreported(self) -> None:
        _record, result = self.render("zup-codegen")
        questions = result.record["page_content"]["questions"]
        self.assertEqual(questions["workflow"]["state"], "not-reviewed")
        self.assertIn("The pipeline found no passage in s1", questions["workflow"]["note"])
        for block in (
            *questions.values(),
            *result.record["page_content"]["implementation_fields"].values(),
        ):
            self.assertNotEqual(block["state"], "unreported")


class RenderBehaviourTests(unittest.TestCase):
    def test_an_accepted_claim_without_an_exact_quote_is_a_render_error(self) -> None:
        record = load_fixture("zup-codegen")
        claims = [
            claim.model_copy(
                update={
                    "quotes": [
                        quote.model_copy(update={"match": "fuzzy", "lines": None})
                        for quote in claim.quotes
                    ]
                }
            )
            if claim.field == "summary"
            else claim
            for claim in record.claims
        ]
        with self.assertRaises(RenderError):
            render_extraction(record.model_copy(update={"claims": claims}), reviewed_at=REVIEWED_AT)

    def test_a_metric_without_an_observation_omits_page_content_with_a_note(self) -> None:
        record = load_fixture("plaid-ai-annotator")
        claims = [
            claim.model_copy(update={"observation": None})
            if claim.field == "key_metrics[]"
            else claim
            for claim in record.claims
        ]
        result = render_extraction(
            record.model_copy(update={"claims": claims}), reviewed_at=REVIEWED_AT
        )
        self.assertNotIn("page_content", result.record)
        self.assertTrue(any("observation block" in note for note in result.notes))

    def test_a_duplicate_metric_text_drops_from_key_metrics(self) -> None:
        record = load_fixture("plaid-ai-annotator")
        headline = next(claim for claim in record.claims if claim.field == "headline_metric")
        duplicate = next(
            claim for claim in record.claims if claim.field == "key_metrics[]"
        ).model_copy(update={"text": headline.text.upper()})
        claims = [claim for claim in record.claims if claim.field != "key_metrics[]"]
        claims.append(duplicate)
        result = render_extraction(
            record.model_copy(update={"claims": claims}), reviewed_at=REVIEWED_AT
        )
        self.assertNotIn("key_metrics", result.record)
        self.assertTrue(any("no metric appears twice" in note for note in result.notes))

    def test_the_company_entry_uses_a_placeholder_logo_with_a_note(self) -> None:
        record = load_fixture("plaid-ai-annotator")
        candidate = record.candidate.model_copy(
            update={"homepage": "https://example.com/", "company_id": "example"}
        )
        result = render_extraction(
            record.model_copy(update={"candidate": candidate}), reviewed_at=REVIEWED_AT
        )
        entry = result.company_entry
        assert entry is not None
        self.assertEqual(entry["logo"], "none")
        self.assertIn("logo_note", entry)
        self.assertEqual(entry["id"], "example")

    def test_a_missing_homepage_leaves_no_company_entry(self) -> None:
        record = load_fixture("plaid-ai-annotator")
        result = render_extraction(record, reviewed_at=REVIEWED_AT)
        self.assertIsNone(result.company_entry)
        self.assertTrue(any("company entry" in note for note in result.notes))

    def test_update_rendering_appends_source_ids_after_the_existing_ones(self) -> None:
        record = load_fixture("plaid-ai-annotator")
        sources = [
            source.model_copy(update={"capture_manifest_path": None}) for source in record.sources
        ]
        result = render_extraction(
            record.model_copy(update={"sources": sources}),
            reviewed_at=REVIEWED_AT,
            existing_source_count=3,
        )
        self.assertEqual(result.record["sources"][0]["id"], "plaid-ai-annotator-source-4")
        self.assertNotIn("capture", result.record["sources"][0])
        self.assertEqual(
            result.record["first_public_evidence"]["source_id"],
            "plaid-ai-annotator-source-4",
        )

    def test_unfinalized_claims_are_refused(self) -> None:
        record = load_fixture("zup-codegen")
        unfinalized = record.model_copy(
            update={"claims": [record.claims[0].model_copy(update={"id": None})]}
        )
        with self.assertRaises(RenderError):
            render_extraction(unfinalized, reviewed_at=REVIEWED_AT)

    def test_to_authored_yaml_round_trips_through_safe_load(self) -> None:
        _record, result = self.render_fixture("duolingo-agentic-workflows")
        parsed = yaml.safe_load(result.record_yaml)
        self.assertEqual(parsed, result.record)

    def staged_fixture(self, record_id: str):
        """The fixture with its sources reset to staging semantics."""
        record = load_fixture(record_id)
        sources = [
            source.model_copy(update={"capture_manifest_path": None}) for source in record.sources
        ]
        return record.model_copy(update={"sources": sources})

    def test_an_update_merges_additively_onto_the_existing_record(self) -> None:
        import copy

        record = self.staged_fixture("zup-codegen")
        existing = yaml.safe_load(
            (
                Path(__file__).resolve().parents[1] / "data" / "agents" / "zup-codegen.yaml"
            ).read_text(encoding="utf-8")
        )
        before = copy.deepcopy(existing)
        merged = render_extraction(record, reviewed_at=REVIEWED_AT, existing=existing)
        draft = merged.record
        self.assertEqual([s["id"] for s in draft["sources"]][0], "zup-codegen-source-1")
        self.assertIn("zup-codegen-source-2", [s["id"] for s in draft["sources"]])
        # Recorded fields, lists, and their order are untouched; additions append.
        self.assertEqual(draft["summary"], before["summary"])
        self.assertEqual(
            draft["lessons_learned"][: len(before["lessons_learned"])], before["lessons_learned"]
        )
        self.assertEqual(draft["evidence"]["summary"][0], before["evidence"]["summary"][0])
        self.assertEqual(draft["page_content"]["questions"]["workflow"]["state"], "unreported")
        # A single-valued difference is a note, never a change.
        self.assertTrue(any("single-valued" in note for note in merged.notes))
        # The compatibility map names the merged paths, never dangling ones:
        # a claim for an item the record already carries registers against
        # that item's index, and a new item appends after the recorded ones.
        evidence_paths = set(draft["evidence"])
        list_roots = {"primitives", "key_metrics", "lessons_learned", "operating_models"}
        for paths in merged.compatibility.values():
            for path in paths:
                if path.split(".")[0] in list_roots:
                    self.assertIn(path, evidence_paths, f"{path} is not a merged path")
        # The fixture restates the recorded operating model; it must not
        # duplicate it, and its claim maps to the recorded index.
        self.assertEqual(len(draft["operating_models"]), len(before["operating_models"]))
        self.assertIn("operating_models.0", evidence_paths)
        # The yaml round-trips like a standalone draft.
        self.assertEqual(yaml.safe_load(merged.record_yaml), draft)

    def test_a_reviewed_answer_upgrades_a_recorded_unreviewed_one(self) -> None:
        from intake.merge import merge_update

        existing = {
            "sources": [{"id": "zup-codegen-source-1"}],
            "page_content": {
                "version": 1,
                "reviewed_at": "2026-08-01",
                "source_ids": ["zup-codegen-source-1"],
                "questions": {
                    "workflow": {"state": "unreported", "claim_paths": [], "note": "old note"}
                },
                "implementation_fields": {},
                "observations": {},
            },
        }
        rendered = {
            "sources": [{"id": "zup-codegen-source-2"}],
            "page_content": {
                "version": 1,
                "reviewed_at": "2026-09-22",
                "source_ids": ["zup-codegen-source-2"],
                "questions": {
                    "workflow": {
                        "state": "reported",
                        "claim_paths": ["summary"],
                        "note": "new note",
                    }
                },
                "implementation_fields": {},
                "observations": {},
            },
        }
        merged = merge_update(existing, rendered, reviewed_at="2026-09-22")
        question = merged["page_content"]["questions"]["workflow"]
        self.assertEqual(question["state"], "reported")
        self.assertEqual(question["note"], "new note")
        self.assertEqual(
            merged["page_content"]["source_ids"],
            ["zup-codegen-source-1", "zup-codegen-source-2"],
        )
        # A not-reviewed new answer never downgrades a recorded one.
        again = merge_update(
            merged,
            {
                "sources": [],
                "page_content": {
                    **rendered["page_content"],
                    "questions": {
                        "workflow": {"state": "not-reviewed", "claim_paths": [], "note": ""}
                    },
                },
            },
            reviewed_at="2026-09-23",
        )
        self.assertEqual(again["page_content"]["questions"]["workflow"]["state"], "reported")

    def test_a_new_list_item_appends_after_the_recorded_ones(self) -> None:
        from intake.models import ExtractionRecord, finalize

        record = self.staged_fixture("zup-codegen")
        payload = record.model_dump()
        payload["claims"].append(
            {
                "field": "lessons_learned[]",
                "text": "A brand-new lesson the update reports.",
                "kind": "opinion",
                "provenance": "reported",
                "quotes": [dict(payload["claims"][0]["quotes"][0])],
                "disposition": "accept",
            }
        )
        rebuilt = finalize(ExtractionRecord.model_validate(payload))
        existing = yaml.safe_load(
            (
                Path(__file__).resolve().parents[1] / "data" / "agents" / "zup-codegen.yaml"
            ).read_text(encoding="utf-8")
        )
        merged = render_extraction(rebuilt, reviewed_at=REVIEWED_AT, existing=existing)
        draft = merged.record
        new_index = len(existing["lessons_learned"])
        self.assertEqual(len(draft["lessons_learned"]), new_index + 1)
        self.assertEqual(
            draft["lessons_learned"][new_index], "A brand-new lesson the update reports."
        )
        self.assertIn(f"lessons_learned.{new_index}", draft["evidence"])
        self.assertIn(f"lessons_learned.{new_index}", draft["claim_metadata"])
        for paths in merged.compatibility.values():
            for path in paths:
                if path.startswith("lessons_learned."):
                    self.assertLess(int(path.rsplit(".", 1)[1]), len(draft["lessons_learned"]))

    def render_fixture(self, record_id: str):
        record = load_fixture(record_id)
        return record, render_extraction(record, reviewed_at=REVIEWED_AT)


if __name__ == "__main__":
    unittest.main()
