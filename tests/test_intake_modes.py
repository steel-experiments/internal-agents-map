from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any

import yaml

from intake.adapters.steel import ScrapedPage, SteelSdkAdapter
from intake.apply import ApplyError, apply_proposals, load_proposals
from intake.drift import (
    _changed_line_spans,
    affected_claim_paths,
    drift_report,
    report_markdown,
)

ROOT = Path(__file__).resolve().parents[1]


def scraped(markdown: str, url: str) -> ScrapedPage:
    return ScrapedPage(
        markdown=markdown,
        final_url=url,
        title="A page",
        http_status=200,
        pdf_url=None,
        published_at=None,
        language=None,
        canonical_url=None,
        description=None,
    )


class StaticDriftAdapter(SteelSdkAdapter):
    """Serves fixed pages keyed by URL."""

    def __init__(self, pages: dict[str, str]) -> None:
        super().__init__(api_key="test-key")
        self._pages = pages

    def scrape(self, url: str, *, pdf: bool = False, delay_ms: int = 1000) -> ScrapedPage:
        return scraped(self._pages[url], url)


class ChangedLineSpansTests(unittest.TestCase):
    def test_unchanged_text_has_no_spans(self) -> None:
        text = "one\ntwo\nthree"
        self.assertEqual(_changed_line_spans(text, text), [])

    def test_a_single_changed_line_is_one_span(self) -> None:
        old = "one\ntwo\nthree"
        new = "one\nTWO changed\nthree"
        spans = _changed_line_spans(old, new)
        self.assertEqual([span.start for span in spans], [2])
        self.assertEqual([span.stop - 1 for span in spans], [2])

    def test_whitespace_and_marks_do_not_count_as_change(self) -> None:
        old = "we’ve “shipped” — done"
        new = 'we\'ve "shipped" -   done'
        self.assertEqual(_changed_line_spans(old, new), [])


class ApplyTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.records = self.root / "agents"
        self.records.mkdir()
        for name in ("zup-codegen", "plaid-ai-annotator"):
            shutil.copy(ROOT / "data" / "agents" / f"{name}.yaml", self.records / f"{name}.yaml")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def proposals(self, entries: list[dict[str, Any]]) -> Path:
        path = self.root / "proposals.json"
        path.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
        return path

    def test_approved_proposals_add_locators_and_nothing_else(self) -> None:
        path = self.proposals(
            [
                {
                    "record": "zup-codegen",
                    "path": "architecture.harness",
                    "source_id": "zup-codegen-source-1",
                    "locator": "Preserved content.md, line 18",
                    "approved": True,
                }
            ]
        )
        changed = apply_proposals(load_proposals(path), record_root=self.records)
        self.assertEqual([p.name for p in changed], ["zup-codegen.yaml"])
        before = yaml.safe_load(
            (ROOT / "data" / "agents" / "zup-codegen.yaml").read_text(encoding="utf-8")
        )
        after = yaml.safe_load((self.records / "zup-codegen.yaml").read_text(encoding="utf-8"))
        link = after["evidence"]["architecture.harness"][0]
        self.assertEqual(link["locator"], "Preserved content.md, line 18")
        # Nothing else moved: same claim paths, same order, same texts.
        self.assertEqual(list(after["evidence"]), list(before["evidence"]))
        self.assertEqual(after["summary"], before["summary"])
        self.assertEqual(after["sources"], before["sources"])

    def test_unapproved_proposals_are_refused(self) -> None:
        path = self.proposals(
            [
                {
                    "record": "zup-codegen",
                    "path": "summary",
                    "source_id": "zup-codegen-source-1",
                    "locator": "Preserved content.md, line 18",
                    "approved": False,
                }
            ]
        )
        with self.assertRaises(ApplyError):
            load_proposals(path)

    def test_a_conflicting_existing_locator_is_refused(self) -> None:
        path = self.proposals(
            [
                {
                    "record": "zup-codegen",
                    "path": "summary",
                    "source_id": "zup-codegen-source-1",
                    "locator": "Preserved content.md, line 99",
                    "approved": True,
                }
            ]
        )
        with self.assertRaises(ApplyError):
            apply_proposals(load_proposals(path), record_root=self.records)

    def test_an_unknown_evidence_path_is_refused(self) -> None:
        path = self.proposals(
            [
                {
                    "record": "zup-codegen",
                    "path": "key_metrics.9",
                    "source_id": "zup-codegen-source-1",
                    "locator": "Preserved content.md, line 18",
                    "approved": True,
                }
            ]
        )
        with self.assertRaises(ApplyError):
            apply_proposals(load_proposals(path), record_root=self.records)


class DriftTests(unittest.TestCase):
    def test_affected_claims_map_through_line_locators(self) -> None:
        record = {
            "evidence": {
                "summary": [
                    {
                        "source_id": "s1",
                        "relation": "supports",
                        "locator": "Preserved content.md, line 18",
                    }
                ],
                "key_metrics.0": [{"source_id": "s1", "relation": "supports"}],
                "lessons_learned.0": [
                    {
                        "source_id": "s1",
                        "relation": "supports",
                        "locator": "Preserved content.md, line 40",
                    }
                ],
            }
        }
        self.assertEqual(affected_claim_paths(record, [range(18, 19)]), ["summary"])
        self.assertEqual(affected_claim_paths(record, [range(15, 20)]), ["summary"])

    def test_a_changed_page_reports_drift_and_affected_claims(self) -> None:
        record_path = ROOT / "data" / "agents" / "zup-codegen.yaml"
        record = yaml.safe_load(record_path.read_text(encoding="utf-8"))
        preserved = (
            ROOT / "archive" / "sources" / "zup-codegen-source-1" / "content.md"
        ).read_text(encoding="utf-8")
        # A fresh scrape returns the body alone; the preserved file adds the
        # nine-line header on top. Change full-file line 18 (the abstract).
        body = preserved.splitlines()[9:]
        body[8] = body[8] + " A new sentence changes the abstract."
        adapter = StaticDriftAdapter({"https://arxiv.org/abs/2604.09805": "\n".join(body)})
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            payload = drift_report(adapter=adapter, records=[record], output=output)
            self.assertEqual(payload["sources_checked"], 1)
            self.assertEqual(payload["sources_changed"], 1)
            entry = payload["drift"][0]
            self.assertEqual(entry["source_id"], "zup-codegen-source-1")
            self.assertTrue(
                all(span["start"] <= 18 <= span["end"] for span in entry["changed_lines"])
            )
            self.assertIn("summary", entry["affected_claims"])
            sheet = report_markdown(payload)
            self.assertIn("zup-codegen-source-1", sheet)
            self.assertIn("affected claims", sheet)

    def test_an_unchanged_page_reports_no_drift(self) -> None:
        record = yaml.safe_load(
            (ROOT / "data" / "agents" / "zup-codegen.yaml").read_text(encoding="utf-8")
        )
        preserved = (
            ROOT / "archive" / "sources" / "zup-codegen-source-1" / "content.md"
        ).read_text(encoding="utf-8")
        # The preserved snapshot minus its nine-line header is what a rescrape
        # of the same page would return.
        adapter = StaticDriftAdapter(
            {"https://arxiv.org/abs/2604.09805": "\n".join(preserved.splitlines()[9:])}
        )
        with tempfile.TemporaryDirectory() as directory:
            payload = drift_report(
                adapter=adapter, records=[record], output=Path(directory) / "report.json"
            )
            self.assertEqual(payload["sources_changed"], 0)
            self.assertIn("No source changed", report_markdown(payload))

    def test_a_blocked_rescrape_is_reported_not_hidden(self) -> None:
        record = yaml.safe_load(
            (ROOT / "data" / "agents" / "zup-codegen.yaml").read_text(encoding="utf-8")
        )

        class BlockedAdapter(SteelSdkAdapter):
            def scrape(self, url: str, *, pdf: bool = False, delay_ms: int = 1000):
                raise RuntimeError("collection blocker")

        with tempfile.TemporaryDirectory() as directory:
            payload = drift_report(
                adapter=BlockedAdapter(api_key="test-key"),
                records=[record],
                output=Path(directory) / "report.json",
            )
            self.assertEqual(payload["sources_changed"], 0)
            self.assertEqual(payload["errors"], 1)
            self.assertIn("rescrape failed", payload["blocked"][0]["error"])


if __name__ == "__main__":
    unittest.main()
