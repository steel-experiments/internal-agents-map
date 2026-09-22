from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

from intake.adapters.steel import MissingApiKeyError, SteelSdkAdapter
from intake.capture import (
    HEADER_LINES,
    CaptureStageError,
    capture_staging,
    promote,
    staging_key,
)
from intake.catalog import load_archiver, load_build
from intake.resolve import name_score, normalize_name, resolve_identity
from intake.segment import coverage, load_paragraphs_file, paragraphs_json, segment_content

ROOT = Path(__file__).resolve().parents[1]
CAPTURES = sorted((ROOT / "archive" / "sources").glob("*/content.md"))


class FakeResponse:
    """The SDK response seam: any object with ``model_dump(by_alias=...)``."""

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    def model_dump(self, *, by_alias: bool = False, exclude_none: bool = False) -> dict[str, Any]:
        return self._data


class FakeClient:
    def __init__(self, response: FakeResponse) -> None:
        self._response = response

    def scrape(self, *, url: str, format: list[str], pdf: bool, delay: int) -> FakeResponse:
        return self._response


def sdk_payload(
    *,
    markdown: str = (
        "Example published a long post about its internal agent platform. "
        "The post describes the architecture, the rollout, and the measured impact "
        "of the system across several internal teams over two quarters of use."
    ),
    title: str = "Example: agents inside",
    status: int = 200,
    url: str = "https://example.com/posts/agents",
    published: str | None = "2026-05-01T00:00:00Z",
    language: str | None = "en",
    canonical: str | None = "https://example.com/posts/agents",
) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "statusCode": status,
        "title": title,
        "urlSource": url,
    }
    if published is not None:
        metadata["publishedTime"] = published
    if language is not None:
        metadata["language"] = language
    if canonical is not None:
        metadata["canonical"] = canonical
    return {"content": {"markdown": markdown}, "metadata": metadata}


def fake_adapter(payload: dict[str, Any]) -> SteelSdkAdapter:
    return SteelSdkAdapter(
        api_key="test-key",
        client_factory=lambda _key: FakeClient(FakeResponse(payload)),
    )


class SteelAdapterTests(unittest.TestCase):
    def test_a_valid_scrape_returns_the_page_and_its_metadata(self) -> None:
        page = fake_adapter(sdk_payload()).scrape("https://example.com/posts/agents")
        self.assertEqual(page.http_status, 200)
        self.assertEqual(page.title, "Example: agents inside")
        self.assertEqual(page.published_at, "2026-05-01T00:00:00Z")
        self.assertEqual(page.language, "en")

    def test_an_interstitial_title_is_rejected_by_the_archiver_checks(self) -> None:
        archiver = load_archiver()
        with self.assertRaises(archiver.ArchiveError):
            fake_adapter(sdk_payload(title="Just a moment...")).scrape(
                "https://example.com/posts/agents"
            )

    def test_an_error_status_is_rejected(self) -> None:
        archiver = load_archiver()
        with self.assertRaises(archiver.ArchiveError):
            fake_adapter(sdk_payload(status=503)).scrape("https://example.com/posts/agents")

    def test_a_missing_api_key_fails_before_any_client_is_built(self) -> None:
        with mock.patch.dict("os.environ", {}, clear=False):
            import os

            os.environ.pop("STEEL_API_KEY", None)
            with self.assertRaises(MissingApiKeyError):
                SteelSdkAdapter().scrape("https://example.com/posts/agents")


class StagingCaptureTests(unittest.TestCase):
    def stage(
        self,
        tmp: Path,
        payload: dict[str, Any] | None = None,
        url: str = "https://example.com/posts/agents",
    ):
        return capture_staging(
            url,
            staging_root=tmp / ".intake" / "captures",
            adapter=fake_adapter(payload or sdk_payload()),
        )

    def test_staging_writes_the_snapshot_the_metadata_and_the_facts(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            staged = self.stage(tmp)
            content = (staged.staging_dir / "content.md").read_text(encoding="utf-8")
            lines = content.splitlines()
            self.assertEqual(lines[0], "> Archived source snapshot  ")
            self.assertTrue(
                lines[1].startswith(
                    f"> Source ID: `staging-{staging_key('https://example.com/posts/agents')}`"
                )
            )
            self.assertEqual(len(lines[:HEADER_LINES]), HEADER_LINES)
            page = json.loads((staged.staging_dir / "page.json").read_text(encoding="utf-8"))
            self.assertEqual(page["published_at"], "2026-05-01T00:00:00Z")
            facts = json.loads((staged.staging_dir / "staging.json").read_text(encoding="utf-8"))
            self.assertEqual(facts["tool"]["name"], "steel-python-sdk")
            self.assertTrue(facts["content_sha256"].startswith("sha256:"))

    def test_promotion_writes_a_valid_append_only_bundle(self) -> None:
        import tempfile

        archiver = load_archiver()
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            staged = self.stage(tmp)
            repo = tmp / "repo"
            manifest = promote(staged.staging_dir, "example-agents-source-1", repo_root=repo)
            self.assertEqual(manifest, "archive/sources/example-agents-source-1/metadata.json")
            bundle = repo / "archive" / "sources" / "example-agents-source-1"
            archiver.validate_bundle(
                bundle / "metadata.json",
                "example-agents-source-1",
                "https://example.com/posts/agents",
                repo_root=repo,
            )
            manifest_data = json.loads((bundle / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest_data["tool"]["name"], "steel-python-sdk")
            self.assertEqual(manifest_data["captured_at"], staged.captured_at)

    def test_promotion_keeps_every_line_number_stable(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            staged = self.stage(tmp)
            repo = tmp / "repo"
            promote(staged.staging_dir, "example-agents-source-1", repo_root=repo)
            staged_lines = (
                (staged.staging_dir / "content.md").read_text(encoding="utf-8").splitlines()
            )
            promoted_lines = (
                (repo / "archive" / "sources" / "example-agents-source-1" / "content.md")
                .read_text(encoding="utf-8")
                .splitlines()
            )
            self.assertEqual(len(staged_lines), len(promoted_lines))
            self.assertEqual(staged_lines[HEADER_LINES:], promoted_lines[HEADER_LINES:])
            self.assertIn("example-agents-source-1", promoted_lines[1])

    def test_promotion_refuses_an_existing_bundle(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            staged = self.stage(tmp)
            repo = tmp / "repo"
            promote(staged.staging_dir, "example-agents-source-1", repo_root=repo)
            with self.assertRaises(CaptureStageError):
                promote(staged.staging_dir, "example-agents-source-1", repo_root=repo)

    def test_promotion_refuses_an_invalid_source_id(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            staged = self.stage(tmp)
            with self.assertRaises(CaptureStageError):
                promote(staged.staging_dir, "Not A Kebab Id", repo_root=tmp / "repo")


class SegmentationTests(unittest.TestCase):
    def test_headings_code_blocks_and_lists_segment_as_expected(self) -> None:
        markdown = "\n".join(
            [
                "# Title",
                "",
                "Intro paragraph.",
                "",
                "## Section",
                "",
                "First text.",
                "more text",
                "",
                "```python",
                "code()",
                "",
                "still code",
                "```",
                "",
                "- item one",
                "- item two",
                "",
                "| a | b |",
                "| --- | --- |",
                "| 1 | 2 |",
            ]
        )
        paragraphs = segment_content(markdown)
        by_id = {paragraph.id: paragraph for paragraph in paragraphs}
        self.assertEqual(by_id["p1"].text, "# Title")
        self.assertEqual(by_id["p1"].heading_path, ("Title",))
        self.assertEqual(by_id["p2"].text, "Intro paragraph.")
        self.assertEqual(by_id["p3"].text, "## Section")
        self.assertEqual(by_id["p4"].heading_path, ("Title", "Section"))
        self.assertEqual(by_id["p4"].text, "First text.\nmore text")
        code = by_id["p5"]
        self.assertEqual(code.text, "```python\ncode()\n\nstill code\n```")
        self.assertEqual((code.start, code.end), (10, 14))
        self.assertEqual(by_id["p6"].text, "- item one\n- item two")
        self.assertEqual(by_id["p7"].text, "| a | b |\n| --- | --- |\n| 1 | 2 |")

    def test_every_existing_capture_segments_stably_and_covers_its_lines(self) -> None:
        self.assertGreaterEqual(len(CAPTURES), 120)
        for path in CAPTURES:
            with self.subTest(capture=path.parent.name):
                text = path.read_text(encoding="utf-8")
                first = segment_content(text)
                second = segment_content(text)
                self.assertEqual(first, second)
                self.assertEqual(
                    [paragraph.id for paragraph in first],
                    [f"p{index}" for index in range(1, len(first) + 1)],
                )
                covered = coverage(first)
                for index, line in enumerate(text.splitlines(), start=1):
                    if line.strip():
                        self.assertIn(index, covered)
                for paragraph in first:
                    self.assertLessEqual(paragraph.start, paragraph.end)
                overlaps = coverage(first)
                total = sum(paragraph.end - paragraph.start + 1 for paragraph in first)
                self.assertEqual(total, len(overlaps))

    def test_paragraphs_json_round_trips(self) -> None:
        import tempfile

        markdown = "# T\n\nBody text here.\n"
        paragraphs = segment_content(markdown)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "paragraphs.json"
            path.write_text(paragraphs_json(paragraphs), encoding="utf-8")
            self.assertEqual(load_paragraphs_file(path), paragraphs)


class ResolveIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        build = load_build()
        cls.records = build.load_agents()
        cls.companies = build.load_companies(cls.records)

    def test_name_scoring_is_deterministic_and_ordered(self) -> None:
        self.assertEqual(normalize_name("  AI Code-Review Agent! "), "ai code review agent")
        self.assertEqual(name_score("River", "river"), 1.0)
        self.assertGreaterEqual(name_score("River", "The River agent"), 0.85)
        self.assertEqual(name_score("River", "Roast"), 0.0)

    def test_every_existing_record_is_found_from_its_own_summary(self) -> None:
        for record in self.records:
            with self.subTest(record=record["id"]):
                identity = resolve_identity(
                    company=record["company"],
                    system_name=record["agent_name"],
                    text=record["summary"],
                    records=self.records,
                    companies=self.companies,
                )
                self.assertIsNotNone(identity["company"], record["id"])
                shortlist = identity["matched_records"]
                self.assertTrue(shortlist, record["id"])
                self.assertEqual(shortlist[0]["id"], record["id"])
                self.assertEqual(identity["proposed_decision"], "update")

    def test_no_company_evidence_proposes_needs_evidence(self) -> None:
        identity = resolve_identity(
            company="Unknown Corp",
            system_name="Mystery Agent",
            records=self.records,
            companies=self.companies,
        )
        self.assertIsNone(identity["company"])
        self.assertEqual(identity["proposed_decision"], "needs-evidence")

    def test_a_known_company_with_a_new_system_proposes_add(self) -> None:
        identity = resolve_identity(
            company="Shopify",
            system_name="Brand New System",
            records=self.records,
            companies=self.companies,
        )
        self.assertEqual(identity["company"]["name"], "Shopify")
        self.assertEqual(identity["proposed_decision"], "add")


if __name__ == "__main__":
    unittest.main()
