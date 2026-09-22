from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

import yaml

from intake.adapters.jev import JevAdapter
from intake.adapters.steel import SteelSdkAdapter
from intake.adapters.writer import WriterAdapter
from intake.budget import Budget
from intake.run import load_queue, run_candidate, run_queue
from intake.stage import run_stage

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "intake"


class FakeSteelClient:
    def __init__(self, markdown: str) -> None:
        self._markdown = markdown

    def scrape(self, *, url: str, format: list[str], pdf: bool, delay: int) -> Any:
        return FakeSteelResponse(self._markdown, url)


class FakeSteelResponse:
    def __init__(self, markdown: str, url: str) -> None:
        self._markdown = markdown
        self._url = url

    def model_dump(self, *, by_alias: bool = False, exclude_none: bool = False) -> dict[str, Any]:
        return {
            "content": {"markdown": self._markdown},
            "metadata": {
                "statusCode": 200,
                "title": "Building an Internal Coding Agent at Zup",
                "urlSource": self._url,
                "publishedTime": "2026-04-01T00:00:00Z",
                "language": "en",
                "canonical": self._url,
            },
        }


def zup_capture_markdown() -> str:
    """The real preserved zup abstract, as the SDK would return its body."""
    content = (ROOT / "archive" / "sources" / "zup-codegen-source-1" / "content.md").read_text(
        encoding="utf-8"
    )
    lines = content.splitlines()
    return "\n".join(lines[9:])


def zup_writer_payload() -> dict[str, Any]:
    """The zup fixture's claims, as the writer model would return them."""
    fixture = yaml.safe_load((FIXTURES / "zup-codegen.extraction.yaml").read_text(encoding="utf-8"))
    claims = []
    for claim in fixture["claims"]:
        entry = dict(claim)
        entry["id"] = None
        claims.append(entry)
    order = [claim["id"] for claim in fixture["claims"]]

    def positional(answer: dict[str, Any]) -> dict[str, Any]:
        answer = dict(answer)
        answer["claim_ids"] = [
            f"#{order.index(claim_id)}" for claim_id in answer.get("claim_ids", [])
        ]
        return answer

    questions: dict[str, Any] = {}
    for key in (
        "purpose",
        "workflow",
        "human_involvement",
        "implementation",
        "validation",
        "observations",
        "lessons",
    ):
        questions[key] = positional(fixture["questions"][key])
    questions["implementation_fields"] = {
        key: positional(answer)
        for key, answer in fixture["questions"]["implementation_fields"].items()
    }
    if fixture["questions"].get("workflow_scope"):
        questions["workflow_scope"] = fixture["questions"]["workflow_scope"]
    classification = dict(fixture["classification"])
    classification["operating_models"] = [
        dict(model, claim_ids=[f"#{order.index(claim_id)}" for claim_id in model["claim_ids"]])
        for model in fixture["classification"]["operating_models"]
    ]
    return {
        "candidate": fixture["candidate"],
        "classification": classification,
        "claims": claims,
        "questions": questions,
    }


class ZupWriterResponses:
    """Answers the extract call; the write call echoes the claim IDs it gets."""

    def __init__(self) -> None:
        self._calls = 0

    def create(self, **kwargs: Any) -> Any:
        self._calls += 1
        if self._calls == 1:
            payload: dict[str, Any] = zup_writer_payload()
        else:
            supplied = json.loads(kwargs["input"])["claims"]
            reasons = {
                claim[
                    "claim_id"
                ]: "The preserved abstract states this directly with its qualifications."
                for claim in supplied
                if not claim.get("confidence_reason")
            }
            payload = {"reasons": reasons}
        return FakeWriterResponse(payload)


class FakeWriterResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.output_text = json.dumps(payload)
        self.usage = type("Usage", (), {"input_tokens": 8000, "output_tokens": 2000})()
        self.model = "gpt-6-sol-2026-09-22"


class FakeJevConnection:
    def __init__(self) -> None:
        self.requests: list[dict[str, Any]] = []

    def request(self, method: str, path: str, body: bytes, headers: dict[str, str]) -> None:
        self._pending = json.loads(body)

    def getresponse(self) -> Any:
        import copy

        payload = copy.deepcopy(self._pending)
        self.requests.append(payload)
        questions = payload["questions"]

        class Response:
            status = 200

            def read(self) -> bytes:
                answers = {}
                for question_id, question in questions.items():
                    if question["type"] == "noul":
                        answers[question_id] = {"type": "noul", "noul": 0.05}
                    else:
                        answers[question_id] = {
                            "type": "choice",
                            "choice": "stated" if "relation" in question_id else "current",
                            "probabilities": (
                                {"stated": 0.92, "conflicts": 0.03, "unknown": 0.05}
                                if "relation" in question_id
                                else {
                                    "current": 0.9,
                                    "future": 0.04,
                                    "historical": 0.03,
                                    "unknown": 0.03,
                                }
                            ),
                        }
                return json.dumps(
                    {
                        "model": "jev-1.13.0",
                        "answers": answers,
                        "usage": {"input_tokens": 3000, "output_tokens": 30},
                    }
                ).encode()

        return Response()


class EndToEndRunTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.markdown = zup_capture_markdown()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_zup(self) -> Any:
        from intake.cache import JsonCache
        from intake.run import QueueEntry

        steel = SteelSdkAdapter(
            api_key="test-key",
            client_factory=lambda _key: FakeSteelClient(self.markdown),
        )
        writer = WriterAdapter(api_key="test-key", responses=ZupWriterResponses())
        jev = JevAdapter(api_key="test-key", connection=FakeJevConnection())
        return run_candidate(
            QueueEntry(
                urls=["https://arxiv.org/abs/2604.09805"],
                company="Zup",
                system_name="CodeGen",
                record_id="zup-codegen-draft",
            ),
            budget=Budget(budget_usd=5.0),
            steel=steel,
            writer=writer,  # type: ignore[arg-type]
            jev=jev,  # type: ignore[arg-type]
            cache=JsonCache(self.root / "jev-cache.json"),
            writer_cache=JsonCache(self.root / "writer-cache.json"),
            runs_root=self.root / "runs",
            drafts_root=self.root / "drafts",
            staging_root=self.root / "staging",
            reviewed_at="2026-09-22",
        )

    def test_the_twelve_stages_produce_a_valid_draft_and_sheet(self) -> None:
        summary = self.run_zup()
        self.assertEqual(summary.decision, "update")
        self.assertIsNotNone(summary.draft_path)
        draft = yaml.safe_load(summary.draft_path.read_text(encoding="utf-8"))  # type: ignore[union-attr]
        self.assertEqual(draft["id"], "zup-codegen-draft")
        self.assertEqual(draft["company"], "Zup")
        self.assertIn("summary", draft["evidence"])
        sheet = summary.sheet_path.read_text(encoding="utf-8") if summary.sheet_path else ""
        self.assertIn("Intake review: Zup", sheet)
        self.assertIn("## Claims", sheet)
        self.assertIn("## Model usage", sheet)

    def test_a_warm_rerun_is_byte_identical_and_makes_no_calls(self) -> None:
        """The product contract: a warm-cache rerun reproduces the draft."""
        from intake.cache import JsonCache
        from intake.run import QueueEntry

        steel = SteelSdkAdapter(
            api_key="test-key",
            client_factory=lambda _key: FakeSteelClient(self.markdown),
        )
        entry = QueueEntry(
            urls=["https://arxiv.org/abs/2604.09805"],
            company="Zup",
            system_name="CodeGen",
            record_id="zup-codegen-draft",
        )
        common: Any = dict(
            budget=Budget(budget_usd=5.0),
            steel=steel,
            writer=WriterAdapter(api_key="test-key", responses=ZupWriterResponses()),
            jev=JevAdapter(api_key="test-key", connection=FakeJevConnection()),
            cache=JsonCache(self.root / "warm-jev.json"),
            writer_cache=JsonCache(self.root / "warm-writer.json"),
            runs_root=self.root / "runs",
            drafts_root=self.root / "drafts",
            staging_root=self.root / "staging",
            reviewed_at="2026-09-22",
        )
        first = run_candidate(entry, **common)
        # Drafts are never overwritten; the rerun gets its own directory.
        second = run_candidate(entry, **(common | {"drafts_root": self.root / "drafts-2"}))
        self.assertIsNotNone(first.draft_path)
        self.assertIsNotNone(second.draft_path)
        self.assertEqual(
            first.draft_path.read_text(encoding="utf-8"),  # type: ignore[union-attr]
            second.draft_path.read_text(encoding="utf-8"),  # type: ignore[union-attr]
        )
        manifest = json.loads(
            (self.root / "runs" / second.run_id / "run.json").read_text(encoding="utf-8")
        )
        by_stage = {stage["stage"]: stage for stage in manifest["stage_runs"]}
        for name in ("extract", "judge", "write"):
            self.assertEqual(by_stage[name]["calls"], 0, name)
            self.assertGreaterEqual(by_stage[name]["cache_hits"], 1, name)

    def test_an_update_merges_additively_into_the_existing_record(self) -> None:
        from intake.cache import JsonCache
        from intake.run import QueueEntry

        steel = SteelSdkAdapter(
            api_key="test-key",
            client_factory=lambda _key: FakeSteelClient(self.markdown),
        )
        summary = run_candidate(
            QueueEntry(
                urls=["https://arxiv.org/abs/2604.09805"],
                company="Zup",
                system_name="CodeGen",
                record_id="zup-codegen",  # the existing record: an Update
            ),
            budget=Budget(budget_usd=5.0),
            steel=steel,
            writer=WriterAdapter(api_key="test-key", responses=ZupWriterResponses()),
            jev=JevAdapter(api_key="test-key", connection=FakeJevConnection()),
            cache=JsonCache(self.root / "jev-update.json"),
            writer_cache=JsonCache(self.root / "writer-update.json"),
            runs_root=self.root / "runs",
            drafts_root=self.root / "drafts",
            staging_root=self.root / "staging",
            reviewed_at="2026-09-22",
        )
        draft = yaml.safe_load(summary.draft_path.read_text(encoding="utf-8"))  # type: ignore[union-attr]
        source_ids = [source["id"] for source in draft["sources"]]
        self.assertIn("zup-codegen-source-1", source_ids)  # the existing source stays
        self.assertIn("zup-codegen-source-2", source_ids)  # the update appends
        # The recorded summary is untouched: single-valued fields never change.
        self.assertIn("preserved paper abstract", draft["summary"])
        # Recorded evidence links stay; the update's links append.
        self.assertTrue(draft["evidence"]["summary"])
        self.assertIn("lessons_learned.1", draft["evidence"])
        # The page-content block keeps the recorded answers and the new review date.
        self.assertEqual(draft["page_content"]["reviewed_at"], "2026-09-22")
        self.assertIn(
            "primitives.1", draft["page_content"]["questions"]["human_involvement"]["claim_paths"]
        )
        sheet = summary.sheet_path.read_text(encoding="utf-8") if summary.sheet_path else ""
        self.assertIn("single-valued", sheet)
        # A render rerun reproduces the merged draft, not a standalone one.
        self.assertEqual(run_stage("render", summary.run_id, runs_root=self.root / "runs"), 0)
        rerun = (self.root / "runs" / summary.run_id / "draft.yaml.rerun").read_text(
            encoding="utf-8"
        )
        self.assertEqual(rerun, summary.draft_path.read_text(encoding="utf-8"))  # type: ignore[union-attr]

    def test_the_identity_file_carries_the_jev_advisory_column(self) -> None:
        summary = self.run_zup()
        run_dir = self.root / "runs" / summary.run_id
        identity = json.loads((run_dir / "identity.json").read_text(encoding="utf-8"))
        self.assertTrue(identity["matched_records"])
        for entry in identity["matched_records"]:
            self.assertIn("same_system_jev", entry)
        manifest = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        resolve_stage = next(s for s in manifest["stage_runs"] if s["stage"] == "resolve")
        self.assertEqual(resolve_stage["model"], "jev-1.13.0")
        self.assertEqual(resolve_stage["calls"], 1)
        sheet = summary.sheet_path.read_text(encoding="utf-8") if summary.sheet_path else ""
        self.assertIn("## Identity", sheet)
        self.assertIn("Jev same-system 0.05", sheet)
        self.assertIn("deterministic score", sheet)
        manifest = json.loads(
            ((self.root / "runs" / summary.run_id) / "run.json").read_text(encoding="utf-8")
        )
        self.assertIn("extract", manifest["model_strings"])
        self.assertTrue(manifest["compatibility"])

    def test_every_evidence_link_of_the_draft_carries_a_locator(self) -> None:
        summary = self.run_zup()
        draft = yaml.safe_load(summary.draft_path.read_text(encoding="utf-8"))  # type: ignore[union-attr]
        for path, links in draft["evidence"].items():
            for link in links:
                self.assertIn("locator", link, f"link for {path} lacks a locator")

    def test_a_queue_file_drives_the_run(self) -> None:
        queue = self.root / "queue.yaml"
        queue.write_text(
            "- urls: [https://arxiv.org/abs/2604.09805]\n"
            "  company: Zup\n"
            "  system_name: CodeGen\n"
            "  record_id: zup-codegen-draft\n",
            encoding="utf-8",
        )
        entries = load_queue(queue)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].company, "Zup")
        steel = SteelSdkAdapter(
            api_key="test-key",
            client_factory=lambda _key: FakeSteelClient(self.markdown),
        )
        writer = WriterAdapter(api_key="test-key", responses=ZupWriterResponses())
        jev = JevAdapter(api_key="test-key", connection=FakeJevConnection())
        from intake.cache import JsonCache

        summaries = run_queue(
            queue,
            budget_usd=5.0,
            runs_root=self.root / "runs",
            drafts_root=self.root / "drafts",
            staging_root=self.root / "staging",
            steel=steel,
            writer=writer,  # type: ignore[arg-type]
            jev=jev,  # type: ignore[arg-type]
            cache=JsonCache(self.root / "jev-cache-queue.json"),
            writer_cache=JsonCache(self.root / "writer-cache-queue.json"),
        )
        self.assertEqual(len(summaries), 1)
        self.assertEqual(summaries[0].decision, "update")

    def test_a_queue_without_https_urls_is_rejected(self) -> None:
        queue = self.root / "queue.yaml"
        queue.write_text("- urls: [http://example.com/insecure]\n", encoding="utf-8")
        from intake.run import QueueError

        with self.assertRaises(QueueError):
            load_queue(queue)

    def test_offline_stages_rerun_from_the_run_directory(self) -> None:
        summary = self.run_zup()
        self.assertEqual(run_stage("render", summary.run_id, runs_root=self.root / "runs"), 0)
        rerun = (self.root / "runs" / summary.run_id / "draft.yaml.rerun").read_text(
            encoding="utf-8"
        )
        self.assertIn("zup-codegen-draft", rerun)
        self.assertEqual(run_stage("review", summary.run_id, runs_root=self.root / "runs"), 0)


if __name__ == "__main__":
    unittest.main()
