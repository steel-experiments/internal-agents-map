from __future__ import annotations

import unittest
from pathlib import Path

import yaml

from intake.backtest import (
    _locator_lines,
    compare,
    load_human_record,
    report_text,
)
from intake.models import ExtractionRecord, finalize
from intake.render import render_extraction

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "intake"
DATA = ROOT / "data" / "agents"
REVIEWED_AT = "2026-09-22"


def load_fixture(record_id: str) -> ExtractionRecord:
    path = FIXTURES / f"{record_id}.extraction.yaml"
    return finalize(
        ExtractionRecord.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))
    )


class LocatorParsingTests(unittest.TestCase):
    def test_human_locator_forms_parse_to_line_sets(self) -> None:
        self.assertEqual(_locator_lines("Preserved content.md, line 18"), {18})
        self.assertEqual(_locator_lines("Preserved content.md, lines 16–20"), {16, 20})
        self.assertEqual(_locator_lines("Preserved content.md, lines 12, 83"), {12, 83})
        self.assertEqual(_locator_lines("Preserved content.md, lines 26–28"), {26, 28})

    def test_prose_and_missing_locators_parse_to_none(self) -> None:
        self.assertIsNone(_locator_lines("Mux workspace and concurrent-agent sections"))
        self.assertIsNone(_locator_lines("Episode audio, YouTube edition, 11:17–11:53"))
        self.assertIsNone(_locator_lines(None))


class BacktestComparisonTests(unittest.TestCase):
    def test_a_record_matching_its_own_extraction_scores_full_recall(self) -> None:
        human = load_human_record(DATA / "zup-codegen.yaml")
        extraction = load_fixture("zup-codegen")
        result = render_extraction(extraction, reviewed_at=REVIEWED_AT)
        report = compare(human, extraction, compatibility=result.compatibility)
        self.assertEqual(report["human_claims"], 10)
        self.assertEqual(report["matched_claims"], 10)
        self.assertEqual(report["claim_precision"], 1.0)
        for bucket in report["claim_recall_by_kind"].values():
            self.assertEqual(bucket["recall"], 1.0)
        self.assertEqual(report["locator_agreement"]["agreement"], 1.0)
        self.assertEqual(report["unverified_quotes"], 0)

    def test_a_partial_extraction_reports_recall_and_the_missed_paths(self) -> None:
        human = load_human_record(DATA / "plaid-ai-annotator.yaml")
        extraction = load_fixture("plaid-ai-annotator")
        result = render_extraction(extraction, reviewed_at=REVIEWED_AT)
        report = compare(human, extraction, compatibility=result.compatibility)
        self.assertEqual(report["human_claims"], 7)
        self.assertEqual(report["matched_claims"], 6)
        self.assertEqual(report["missed_human_paths"], ["key_metrics.1"])
        self.assertEqual(report["claim_precision"], 1.0)
        metric = report["claim_recall_by_kind"]["metric"]
        self.assertEqual(metric["found"], 2)
        self.assertEqual(metric["human"], 3)
        self.assertEqual(report["unverified_quotes"], 0)

    def test_without_a_compatibility_map_only_text_identical_claims_match(self) -> None:
        human = load_human_record(DATA / "zup-codegen.yaml")
        extraction = load_fixture("zup-codegen")
        with_map = compare(human, extraction, compatibility=None)
        # The naive fallback matches only text-identical or contained claims;
        # paraphrased claims need the renderer's compatibility map.
        self.assertLess(with_map["matched_claims"], with_map["human_claims"])
        self.assertEqual(
            round(with_map["claim_precision"], 4),
            round(with_map["matched_claims"] / with_map["extraction_claims"], 4),
        )

    def test_the_report_text_names_every_measure(self) -> None:
        human = load_human_record(DATA / "zup-codegen.yaml")
        extraction = load_fixture("zup-codegen")
        result = render_extraction(extraction, reviewed_at=REVIEWED_AT)
        report = compare(human, extraction, compatibility=result.compatibility)
        text = report_text(report)
        self.assertIn("Claim precision: 1.0", text)
        self.assertIn("| Kind | Found | Recall |", text)
        self.assertIn("Unverified quotes: 0", text)


if __name__ == "__main__":
    unittest.main()
