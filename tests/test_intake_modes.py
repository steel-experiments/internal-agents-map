from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any

import yaml

from intake.adapters.jev import JevAnswer, JevResult
from intake.adapters.steel import ScrapedPage, SteelSdkAdapter
from intake.adapters.writer import WriterAdapter
from intake.apply import ApplyError, apply_proposals, load_proposals
from intake.backfill import (
    BackfillError,
    backfill_dry_run,
    proposals_payload,
    rank_unlocated,
    ranking_text,
    review_sheet,
)
from intake.backtest import batch_report_text, run_batch
from intake.budget import Budget
from intake.cache import JsonCache
from intake.drift import (
    _changed_line_spans,
    affected_claim_paths,
    drift_report,
    report_markdown,
)

ROOT = Path(__file__).resolve().parents[1]


class EnvFileTests(unittest.TestCase):
    def test_the_env_file_seeds_the_environment_without_overriding(self) -> None:
        import os

        from intake.__main__ import _load_env_file

        with tempfile.TemporaryDirectory() as directory:
            env = Path(directory) / ".env"
            env.write_text(
                "# a comment\n"
                "STEEL_API_KEY=file-key\n"
                'TYPESAFE_API_KEY="quoted-key"\n'
                "BROKEN LINE WITHOUT EQUALS\n",
                encoding="utf-8",
            )
            saved = {
                "STEEL_API_KEY": os.environ.get("STEEL_API_KEY"),
                "TYPESAFE_API_KEY": os.environ.get("TYPESAFE_API_KEY"),
            }
            try:
                os.environ["STEEL_API_KEY"] = "env-key"
                os.environ.pop("TYPESAFE_API_KEY", None)
                _load_env_file(env)
                # The environment wins over the file.
                self.assertEqual(os.environ["STEEL_API_KEY"], "env-key")
                self.assertEqual(os.environ["TYPESAFE_API_KEY"], "quoted-key")
            finally:
                for key, value in saved.items():
                    if value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = value

    def test_a_missing_env_file_changes_nothing(self) -> None:
        from intake.__main__ import _load_env_file

        # The repository has no .env; the loader must stay a no-op.
        _load_env_file(ROOT / ".env")
        _load_env_file(ROOT / "definitely-no-such-file.env")


class CliKeyGuardTests(unittest.TestCase):
    """The backfill precedent, extended: spend no key the machine lacks."""

    def setUp(self) -> None:
        import os

        self._os = os
        self._saved = os.environ.get("TYPESAFE_API_KEY")
        os.environ.pop("TYPESAFE_API_KEY", None)

    def tearDown(self) -> None:
        if self._saved is None:
            self._os.environ.pop("TYPESAFE_API_KEY", None)
        else:
            self._os.environ["TYPESAFE_API_KEY"] = self._saved

    def test_drift_without_the_jev_key_still_reports_unjudged(self) -> None:
        import contextlib
        import io
        from unittest.mock import patch

        import intake.drift as drift_module
        from intake.__main__ import main

        captured: dict[str, Any] = {}

        def fake_drift_report(**kwargs: Any) -> dict[str, Any]:
            captured.update(kwargs)
            return {
                "sources_checked": 0,
                "sources_changed": 0,
                "drift": [],
                "blocked": [],
                "errors": 0,
            }

        output = io.StringIO()
        with (
            patch.object(drift_module, "drift_report", fake_drift_report),
            contextlib.redirect_stdout(output),
        ):
            self.assertEqual(main(["drift"]), 0)
        self.assertIsNone(captured["jev"])
        self.assertIn("listed without verdicts", output.getvalue())

    def test_evals_score_without_the_jev_key_refuses_upfront(self) -> None:
        import contextlib
        import io
        import json as json_module
        import tempfile

        from intake.__main__ import main

        with tempfile.TemporaryDirectory() as directory:
            items = Path(directory) / "items.json"
            items.write_text(json_module.dumps([{"item_id": "a"}]), encoding="utf-8")
            errors = io.StringIO()
            with contextlib.redirect_stderr(errors):
                self.assertEqual(main(["evals", "--items", str(items), "--score"]), 2)
            self.assertIn("TYPESAFE_API_KEY", errors.getvalue())

    def test_bare_backfill_names_its_two_modes(self) -> None:
        import contextlib
        import io

        from intake.__main__ import main

        errors = io.StringIO()
        with contextlib.redirect_stderr(errors):
            self.assertEqual(main(["backfill"]), 2)
        self.assertIn("--rank", errors.getvalue())


class FakeWriterResponse:
    """The writer seam: one canned payload."""

    def __init__(self, payload: dict[str, Any]) -> None:
        self.output_text = json.dumps(payload)
        self.usage = type("Usage", (), {"input_tokens": 1000, "output_tokens": 500})()
        self.model = "gpt-6-sol-2026-09-22"


class BatchFound:
    """The writer seam: one batched reply citing every supplied claim."""

    def __init__(
        self,
        quote: str = "an internal coding agent at Zup",
        skip: tuple[str, ...] = (),
        first_reply: dict[str, Any] | None = None,
    ) -> None:
        self.calls = 0
        self._quote = quote
        self._skip = skip
        self._first_reply = first_reply

    def create(self, **kwargs: Any) -> Any:
        self.calls += 1
        if self.calls == 1 and self._first_reply is not None:
            return FakeWriterResponse(self._first_reply)
        # The retry appends the rejection after the JSON; read the object only.
        input_payload, _end = json.JSONDecoder().raw_decode(kwargs["input"])
        claims = input_payload["claims"]
        return FakeWriterResponse(
            {
                "proposals": [
                    {
                        "path": claim["path"],
                        "found": claim["path"] not in self._skip,
                        "source": "zup-codegen-source-1",
                        "quote": self._quote,
                        "paragraph_id": "p3",
                    }
                    for claim in claims
                ]
            }
        )


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


class BackfillToApplyTests(unittest.TestCase):
    """The Phase 2 dry run and the Phase 5 applier must compose."""

    def test_the_dry_run_output_applies_after_approval(self) -> None:
        record = yaml.safe_load(
            (ROOT / "data" / "agents" / "zup-codegen.yaml").read_text(encoding="utf-8")
        )
        record["evidence"]["summary"][0].pop("locator", None)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record_path = root / "zup-codegen.yaml"
            record_path.write_text(
                yaml.safe_dump(record, sort_keys=False, allow_unicode=True, width=100),
                encoding="utf-8",
            )
            report = backfill_dry_run(
                record_path,
                adapter=WriterAdapter(api_key="test-key", responses=BatchFound()),
                budget=Budget(budget_usd=10.0),
            )
            # The reviewer reads the quote on the sheet, not only the locator.
            self.assertIn("an internal coding agent at Zup", review_sheet(report))

            payload = proposals_payload(report)
            entry = next(item for item in payload if item["path"] == "summary")
            self.assertIn("Preserved content.md", entry["locator"])
            self.assertIs(entry["approved"], False)

            proposals_path = root / "proposals.json"
            proposals_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            with self.assertRaises(ApplyError):
                load_proposals(proposals_path)

            for item in payload:
                item["approved"] = True
            proposals_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            changed = apply_proposals(load_proposals(proposals_path), record_root=root)
            self.assertEqual([path.name for path in changed], ["zup-codegen.yaml"])
            after = yaml.safe_load(record_path.read_text(encoding="utf-8"))
            self.assertEqual(after["evidence"]["summary"][0]["locator"], entry["locator"])

    def test_entries_without_a_locator_stay_out_of_the_payload(self) -> None:
        report = {
            "record": "r1",
            "proposals": [
                {
                    "path": "summary",
                    "source_id": "s1",
                    "quote": "q",
                    "match": "exact",
                    "lines": [18, 18],
                    "numbers_ok": True,
                    "locator": "Preserved content.md, line 18",
                },
                {
                    "path": "key_metrics.0",
                    "source_id": "s1",
                    "quote": "q",
                    "match": "fuzzy",
                    "lines": None,
                    "numbers_ok": None,
                    "locator": None,
                },
            ],
        }
        payload = proposals_payload(report)
        self.assertEqual([item["path"] for item in payload], ["summary"])


class BackfillRankingTests(unittest.TestCase):
    """Phase 5's "worst records first", as a count a person can check."""

    def test_records_rank_worst_first_and_the_text_names_the_order(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "few.yaml").write_text(
                "id: few\nevidence:\n  summary:\n  - source_id: s1\n", encoding="utf-8"
            )
            (root / "many.yaml").write_text(
                "id: many\nevidence:\n"
                "  summary:\n  - source_id: s1\n"
                "  lessons_learned.0:\n  - source_id: s1\n"
                "  key_metrics.0:\n  - source_id: s1\n",
                encoding="utf-8",
            )
            (root / "clean.yaml").write_text(
                "id: clean\nevidence:\n"
                "  summary:\n  - source_id: s1\n"
                "    locator: Preserved content.md, line 3\n",
                encoding="utf-8",
            )
            ranked = rank_unlocated(root)
            self.assertEqual([entry["record"] for entry in ranked], ["many", "few"])
            self.assertEqual(ranked[0]["unlocated"], 3)
            self.assertIn("summary", ranked[1]["paths"])
            text = ranking_text(ranked)
            self.assertIn("worst first", text)
            self.assertIn("many: 3 unlocated path(s)", text)
            self.assertIn("2 record(s) hold 4 unlocated path(s) in total.", text)
            # The catalog itself ranks without error (read-only).
            self.assertTrue(ranking_text(rank_unlocated()))

    def test_a_catalog_with_no_unlocated_paths_says_so(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "clean.yaml").write_text(
                "id: clean\nevidence:\n"
                "  summary:\n  - source_id: s1\n"
                "    locator: Preserved content.md, line 3\n",
                encoding="utf-8",
            )
            self.assertIn("nothing to backfill", ranking_text(rank_unlocated(root)))


class FakeGradingJev:
    """The Jev seam for backfill grading: five answers, one counted call."""

    def __init__(self, relation_p: float = 0.95) -> None:
        self.calls = 0
        self.relation_p = relation_p

    def ask(self, *, state: Any, questions: Any, budget: Any) -> Any:
        self.calls += 1
        answers = {
            "a0_relation": JevAnswer(
                type="choice",
                choice="stated",
                probabilities={"stated": self.relation_p, "conflicts": 0.03, "unknown": 0.02},
            ),
            "a0_actor": JevAnswer(type="noul", noul=0.04),
            "a0_temporal": JevAnswer(
                type="choice",
                choice="current",
                probabilities={"current": 0.9, "future": 0.05, "historical": 0.03, "unknown": 0.02},
            ),
            "a0_approval": JevAnswer(type="noul", noul=0.02),
            "a0_basis": JevAnswer(
                type="choice",
                choice="measured",
                probabilities={
                    "measured": 0.9,
                    "qualitative": 0.05,
                    "target": 0.03,
                    "unknown": 0.02,
                },
            ),
        }
        return JevResult(
            answers=answers,
            model="jev-1.13.0",
            input_tokens=3000,
            output_tokens=30,
            cost_usd=0.0,
            cache_hit=False,
        )


class BackfillGradingTests(unittest.TestCase):
    """Stage 6 of the backfill mode: grade each verified proposal."""

    def setUp(self) -> None:
        record = yaml.safe_load(
            (ROOT / "data" / "agents" / "zup-codegen.yaml").read_text(encoding="utf-8")
        )
        record["evidence"]["summary"][0].pop("locator", None)
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.record_path = self.root / "zup-codegen.yaml"
        self.record_path.write_text(
            yaml.safe_dump(record, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_dry_run(self, jev: Any, cache: Any, batch: BatchFound | None = None) -> dict[str, Any]:
        return backfill_dry_run(
            self.record_path,
            adapter=WriterAdapter(api_key="test-key", responses=batch or BatchFound()),
            budget=Budget(budget_usd=10.0),
            jev=jev,
            cache=cache,
        )

    def summary_proposal(self, report: dict[str, Any]) -> dict[str, Any]:
        return next(item for item in report["proposals"] if item["path"] == "summary")

    def test_every_exactly_verified_proposal_is_graded(self) -> None:
        jev = FakeGradingJev()
        report = self.run_dry_run(jev, cache=None)
        # One judgment request per verified proposal; fuzzy ones never grade.
        self.assertEqual(jev.calls, len(report["proposals"]))
        verdicts = self.summary_proposal(report)["verdicts"]
        self.assertEqual(verdicts["relation"], "stated (0.95)")
        self.assertEqual(verdicts["actor_mismatch"], 0.04)
        self.assertEqual(verdicts["model"], "jev-1.13.0")
        self.assertIn("stated (0.95)", review_sheet(report))

    def test_without_jev_the_sheet_says_not_judged(self) -> None:
        report = self.run_dry_run(None, cache=None)
        self.assertIsNone(self.summary_proposal(report)["verdicts"])
        sheet = review_sheet(report)
        self.assertIn("not judged", sheet)
        self.assertNotIn("stated (", sheet)

    def test_a_warm_cache_grades_nothing_anew(self) -> None:
        cache = JsonCache(self.root / "grades.json")
        first = self.run_dry_run(FakeGradingJev(), cache=cache)
        self.assertEqual(cache.hits, 0)  # every key was written, none read yet
        second_jev = FakeGradingJev()
        second = self.run_dry_run(second_jev, cache=cache)
        self.assertEqual(second_jev.calls, 0)  # the cache answered every grade
        self.assertGreaterEqual(cache.hits, len(second["proposals"]))
        self.assertEqual(
            self.summary_proposal(second)["verdicts"],
            self.summary_proposal(first)["verdicts"],
        )
        self.assertIn("stated (0.95)", review_sheet(second))

    def test_one_writer_call_carries_the_whole_claim_list(self) -> None:
        """The cost table: one extract call per record, whatever the count."""
        batch = BatchFound()
        report = self.run_dry_run(None, cache=None, batch=batch)
        self.assertGreaterEqual(report["unlocated_claims"], 6)
        self.assertEqual(batch.calls, 1)

    def test_a_claim_the_writer_cannot_support_gets_no_proposal(self) -> None:
        report = self.run_dry_run(None, cache=None, batch=BatchFound(skip=("summary",)))
        paths = [proposal["path"] for proposal in report["proposals"]]
        self.assertNotIn("summary", paths)
        self.assertIn("architecture.harness", paths)

    def test_a_malformed_first_reply_retries_once(self) -> None:
        batch = BatchFound(first_reply={"proposals": "not a list"})
        report = self.run_dry_run(None, cache=None, batch=batch)
        self.assertEqual(batch.calls, 2)
        self.assertTrue(report["proposals"])

    def test_a_second_bad_reply_fails_the_mode(self) -> None:
        batch = AlwaysBad()
        with self.assertRaises(BackfillError):
            self.run_dry_run(None, cache=None, batch=batch)  # type: ignore[arg-type]

    def test_a_poisoned_reply_stops_the_mode_before_the_sheet(self) -> None:
        from intake.privacy import PrivateDataError

        address = "jane" + "@" + "example.com"
        batch = BatchFound(quote=f"Contact {address} for details")
        with self.assertRaises(PrivateDataError):
            self.run_dry_run(None, cache=None, batch=batch)


class AlwaysBad:
    """The writer seam: replies that never validate."""

    def create(self, **kwargs: Any) -> Any:
        return FakeWriterResponse({"proposals": "still not a list"})


def zup_batch_payload() -> dict[str, Any]:
    """A minimal writer reply citing the archived zup source by its real ID."""
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


class BatchBacktestTests(unittest.TestCase):
    """The Phase 2 gate command: backtest every captured record."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        shutil.copy(ROOT / "data" / "agents" / "zup-codegen.yaml", self.root / "zup-codegen.yaml")
        (self.root / "no-capture.yaml").write_text(
            "id: no-capture\nsources:\n- id: s1\n  url: https://example.com/a\nevidence: {}\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_the_batch_backtests_captured_records_and_skips_the_rest(self) -> None:
        class OnePayload:
            def create(self, **kwargs: Any) -> Any:
                return FakeWriterResponse(zup_batch_payload())

        report = run_batch(
            adapter=WriterAdapter(api_key="test-key", responses=OnePayload()),
            budget=Budget(budget_usd=20.0),
            records_root=self.root,
        )
        self.assertEqual(report["records"], 1)
        self.assertEqual([entry["record"] for entry in report["skipped"]], ["no-capture"])
        row = report["rows"][0]
        self.assertEqual(row["record"], "zup-codegen")
        self.assertGreaterEqual(row["matched_claims"], 1)
        self.assertEqual(row["unverified_quotes"], 0)
        self.assertEqual(row["locator_agreement"]["compared"], 1)
        self.assertEqual(row["locator_agreement"]["agreeing"], 1)
        # Phase 2 step 4: the model string, token usage, and cost per record.
        self.assertEqual(row["model"], "gpt-6-sol-2026-09-22")
        self.assertGreater(row["input_tokens"], 0)
        self.assertGreater(row["cost_usd"], 0.0)
        self.assertEqual(report["totals"]["input_tokens"], row["input_tokens"])
        self.assertAlmostEqual(report["totals"]["cost_usd"], row["cost_usd"], places=6)
        sheet = batch_report_text(report)
        self.assertIn("zup-codegen", sheet)
        self.assertIn("no-capture", sheet)
        self.assertIn("Writer usage:", sheet)
        self.assertIn("gpt-6-sol-2026-09-22", sheet)
        self.assertIn("A measurement only", sheet)

    def test_a_refused_budget_stops_the_batch_before_any_call(self) -> None:
        class NoCalls:
            def create(self, **kwargs: Any) -> Any:
                raise AssertionError("the budget must refuse before any call")

        report = run_batch(
            adapter=WriterAdapter(api_key="test-key", responses=NoCalls()),
            budget=Budget(budget_usd=0.001),
            records_root=self.root,
        )
        self.assertEqual(report["records"], 0)
        self.assertEqual(report["stopped"]["reason"], "budget")
        self.assertIn("no captured source", batch_report_text(report))

    def test_a_poisoned_writer_reply_stops_the_batch(self) -> None:
        from intake.privacy import PrivateDataError

        address = "jane" + "@" + "example.com"
        payload = zup_batch_payload()
        payload["claims"][0]["text"] = f"Reach {address} for details."

        class Poisoned:
            def create(self, **kwargs: Any) -> Any:
                return FakeWriterResponse(payload)

        with self.assertRaises(PrivateDataError):
            run_batch(
                adapter=WriterAdapter(api_key="test-key", responses=Poisoned()),
                budget=Budget(budget_usd=20.0),
                records_root=self.root,
            )

    def test_a_writer_failure_stops_the_batch(self) -> None:
        from intake.adapters.writer import WriterApiError

        class Boom:
            def create(self, **kwargs: Any) -> Any:
                raise WriterApiError("writer down")

        report = run_batch(
            adapter=WriterAdapter(api_key="test-key", responses=Boom()),
            budget=Budget(budget_usd=20.0),
            records_root=self.root,
        )
        self.assertEqual(report["records"], 0)
        self.assertEqual(report["stopped"]["reason"], "writer")
        self.assertIn("stopped early: writer", batch_report_text(report))


class AcceptanceQueueTests(unittest.TestCase):
    """The committed acceptance queue must stay loadable and complete."""

    def test_the_queue_holds_the_three_policy_review_leads(self) -> None:
        from intake.run import load_queue

        entries = load_queue(ROOT / "queue" / "acceptance-2026-09-11.yaml")
        self.assertEqual(len(entries), 3)
        self.assertEqual(
            [entry.system_name for entry in entries],
            ["Cortex Code", "Omnigent", "Amazon Q Developer"],
        )
        for entry in entries:
            self.assertTrue(entry.urls)
            self.assertTrue(all(url.startswith("https://") for url in entry.urls))
        # Every lead carries at least one first-party source.
        first_party = {
            "Cortex Code": "snowflake.com",
            "Omnigent": "databricks.com",
            "Amazon Q Developer": "amazon.science",
        }
        for entry in entries:
            domain = first_party[entry.system_name]
            self.assertTrue(any(domain in url for url in entry.urls))


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
            # The proposal names the new capture's source ID.
            self.assertEqual(entry["proposed_source_id"], "zup-codegen-source-2")
            sheet = report_markdown(payload)
            self.assertIn("zup-codegen-source-1", sheet)
            self.assertIn("under `zup-codegen-source-2`", sheet)
            self.assertIn("affected claims", sheet)

    def test_changed_sources_of_one_record_get_consecutive_ids(self) -> None:
        from intake.drift import _next_source_number

        record = {
            "id": "r",
            "sources": [{"id": "r-source-1"}, {"id": "r-source-3"}, {"id": "unrelated"}],
        }
        self.assertEqual(_next_source_number(record), 4)
        self.assertEqual(_next_source_number({"id": "r", "sources": []}), 1)

    def test_changed_claims_are_rejudged_against_the_new_text(self) -> None:
        from intake.adapters.jev import JevAnswer, JevResult
        from intake.cache import JsonCache

        record = yaml.safe_load(
            (ROOT / "data" / "agents" / "zup-codegen.yaml").read_text(encoding="utf-8")
        )
        preserved = (
            ROOT / "archive" / "sources" / "zup-codegen-source-1" / "content.md"
        ).read_text(encoding="utf-8")
        body = preserved.splitlines()[9:]
        body[8] = body[8] + " A new sentence changes the abstract."
        adapter = StaticDriftAdapter({"https://arxiv.org/abs/2604.09805": "\n".join(body)})

        class StatedJev:
            calls = 0

            def ask(self, *, state: dict[str, Any], questions: dict[str, Any], budget: Any):
                StatedJev.calls += 1
                answers = {
                    "a0_relation": JevAnswer(
                        type="choice",
                        choice="stated",
                        probabilities={"stated": 0.95, "unknown": 0.05},
                    ),
                    "a0_actor": JevAnswer(type="noul", noul=0.05),
                    "a0_temporal": JevAnswer(
                        type="choice", choice="past", probabilities={"past": 0.9}
                    ),
                    "a0_approval": JevAnswer(type="noul", noul=0.05),
                    "a0_basis": JevAnswer(
                        type="choice", choice="qualitative", probabilities={"qualitative": 0.9}
                    ),
                }
                return JevResult(
                    answers=answers,
                    model="jev-1.13.0",
                    input_tokens=1000,
                    output_tokens=0,
                    cost_usd=0.0001,
                    cache_hit=False,
                )

        with tempfile.TemporaryDirectory() as directory:
            cache = JsonCache(Path(directory) / "cache.json")
            payload = drift_report(
                adapter=adapter,
                records=[record],
                jev=StatedJev(),
                budget=Budget(budget_usd=5.0),
                cache=cache,
                output=Path(directory) / "report.json",
            )
            entry = payload["drift"][0]
            self.assertTrue(entry["claim_verdicts"])
            paths = [verdict["path"] for verdict in entry["claim_verdicts"]]
            self.assertIn("summary", paths)
            summary = next(v for v in entry["claim_verdicts"] if v["path"] == "summary")
            self.assertEqual(summary["relation"], "stated (0.95)")
            sheet = report_markdown(payload)
            self.assertIn("relation stated (0.95)", sheet)
            self.assertIn("advisory, against the rescraped text", sheet)
            # A warm rerun judges nothing anew.
            before = StatedJev.calls
            drift_report(
                adapter=adapter,
                records=[record],
                jev=StatedJev(),
                budget=Budget(budget_usd=5.0),
                cache=cache,
                output=Path(directory) / "report.json",
            )
            self.assertEqual(StatedJev.calls, before)

    def test_drift_without_a_jev_adapter_lists_claims_without_verdicts(self) -> None:
        record = yaml.safe_load(
            (ROOT / "data" / "agents" / "zup-codegen.yaml").read_text(encoding="utf-8")
        )
        preserved = (
            ROOT / "archive" / "sources" / "zup-codegen-source-1" / "content.md"
        ).read_text(encoding="utf-8")
        body = preserved.splitlines()[9:]
        body[8] = body[8] + " A new sentence changes the abstract."
        adapter = StaticDriftAdapter({"https://arxiv.org/abs/2604.09805": "\n".join(body)})
        with tempfile.TemporaryDirectory() as directory:
            payload = drift_report(
                adapter=adapter, records=[record], output=Path(directory) / "report.json"
            )
            self.assertEqual(payload["drift"][0]["claim_verdicts"], [])

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
