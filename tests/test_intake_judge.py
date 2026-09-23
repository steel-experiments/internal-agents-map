from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from intake.adapters.jev import JevAdapter, JevAnswer, JevApiError, JevResult, MissingApiKeyError
from intake.budget import Budget, BudgetExceededError
from intake.cache import JsonCache
from intake.evals import build_items, labeller_agreement, score, write_items
from intake.judge import (
    GATE,
    apply_dispositions,
    build_request,
    judge_claims,
)
from intake.models import ExtractionRecord, finalize
from intake.resolve import jev_identity_questions, refine_with_jev, resolve_identity
from intake.segment import segment_content

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


class FakeJevConnection:
    """A Jev HTTP seam that answers every question in the sent payload."""

    def __init__(self) -> None:
        self.requests: list[dict[str, Any]] = []
        self._pending: dict[str, Any] = {}

    def request(self, method: str, path: str, body: bytes, headers: dict[str, str]) -> None:
        self._pending = json.loads(body)

    def getresponse(self) -> "FakeJevResponse":
        import copy

        payload = copy.deepcopy(self._pending)
        self.requests.append(payload)
        return FakeJevResponse(payload["questions"])


class FakeJevResponse:
    def __init__(self, questions: dict[str, Any]) -> None:
        self.status = 200
        self._questions = questions

    def read(self) -> bytes:
        answers: dict[str, Any] = {}
        for question_id, question in self._questions.items():
            if question["type"] == "noul":
                answers[question_id] = {"type": "noul", "noul": 0.05}
            else:
                answers[question_id] = {
                    "type": "choice",
                    "choice": "stated" if "relation" in question_id else "current",
                    "probabilities": (
                        {"stated": 0.9, "conflicts": 0.05, "unknown": 0.05}
                        if "relation" in question_id
                        else {
                            "current": 0.9,
                            "future": 0.05,
                            "historical": 0.03,
                            "unknown": 0.02,
                        }
                    ),
                }
        return json.dumps(
            {
                "model": "jev-1.13.0",
                "answers": answers,
                "usage": {"input_tokens": 4000, "output_tokens": 40},
            }
        ).encode()


class BandedIdentityJev:
    """The Jev seam for the identity bands: one noul answer for every record."""

    def __init__(self, noul: float) -> None:
        self.noul = noul

    def ask(self, *, state: Any, questions: Any, budget: Any) -> JevResult:
        answers = {question_id: JevAnswer(type="noul", noul=self.noul) for question_id in questions}
        return JevResult(
            answers=answers,
            model="jev-1.13.0",
            input_tokens=500,
            output_tokens=0,
            cost_usd=0.0,
            cache_hit=False,
        )


class JevAdapterTests(unittest.TestCase):
    def make_adapter(self) -> tuple[JevAdapter, FakeJevConnection]:
        connection = FakeJevConnection()
        return JevAdapter(api_key="test-key", connection=connection), connection

    def test_one_request_returns_validated_answers_and_usage(self) -> None:
        adapter, connection = self.make_adapter()
        budget = Budget(budget_usd=1.0)
        result = adapter.ask(
            state={"passage": "Example runs the agent.", "assertions": [{"id": "a", "text": "t"}]},
            questions={
                "a0_relation": {
                    "type": "choice",
                    "instructions": "judge",
                    "criteria": {"stated": "s", "conflicts": "c", "unknown": "u"},
                }
            },
            budget=budget,
        )
        self.assertEqual(result.model, "jev-1.13.0")
        self.assertEqual(result.answers["a0_relation"].choice, "stated")
        self.assertEqual(result.answers["a0_relation"].probability_of("stated"), 0.9)
        self.assertEqual(result.input_tokens, 4000)
        self.assertGreater(budget.cost_usd, 0.0)
        self.assertRegex(result.input_sha256, r"^[0-9a-f]{64}$")

    def test_the_input_hash_follows_the_request_not_the_reply(self) -> None:
        adapter, _connection = self.make_adapter()
        budget = Budget(budget_usd=1.0)
        state = {"passage": "Example runs the agent."}
        questions = {"q": {"type": "noul", "instructions": "same system?"}}
        first = adapter.ask(state=state, questions=questions, budget=budget)
        second = adapter.ask(state=state, questions=questions, budget=budget)
        self.assertEqual(first.input_sha256, second.input_sha256)
        changed = adapter.ask(
            state={"passage": "Another company runs the agent."},
            questions=questions,
            budget=budget,
        )
        self.assertNotEqual(first.input_sha256, changed.input_sha256)

    def test_the_budget_refuses_unreserved_jev_requests(self) -> None:
        adapter, _connection = self.make_adapter()
        budget = Budget(budget_usd=0.0)
        with self.assertRaises(BudgetExceededError):
            adapter.ask(
                state={"passage": "p"},
                questions={"q": {"type": "noul", "instructions": "same system?"}},
                budget=budget,
            )

    def test_an_http_error_stops_the_run_without_retry(self) -> None:
        class BrokenConnection:
            def request(self, *args: Any, **kwargs: Any) -> None:
                raise OSError("connection reset")

        adapter = JevAdapter(api_key="test-key", connection=BrokenConnection())
        with self.assertRaises(JevApiError):
            adapter.ask(
                state={"passage": "p"},
                questions={"q": {"type": "noul", "instructions": "same?"}},
                budget=Budget(budget_usd=1.0),
            )

    def test_a_malformed_answer_shape_is_rejected(self) -> None:
        class BadShapeConnection(FakeJevConnection):
            def getresponse(self) -> Any:
                response = type("R", (), {"status": 200})()
                response.read = lambda: json.dumps(
                    {"model": "jev-1.13.0", "answers": {"q": {"type": "noul"}}, "usage": {}}
                ).encode()
                return response

        adapter = JevAdapter(api_key="test-key", connection=BadShapeConnection())
        with self.assertRaises(JevApiError):
            adapter.ask(
                state={"passage": "p"},
                questions={"q": {"type": "noul", "instructions": "same?"}},
                budget=Budget(budget_usd=1.0),
            )

    def test_a_missing_api_key_fails_before_any_request(self) -> None:
        import os
        from unittest import mock

        with mock.patch.dict("os.environ", {}, clear=False):
            os.environ.pop("TYPESAFE_API_KEY", None)
            with self.assertRaises(MissingApiKeyError):
                JevAdapter().ask(
                    state={"passage": "p"},
                    questions={"q": {"type": "noul", "instructions": "same?"}},
                    budget=Budget(budget_usd=1.0),
                )


class JudgeStageTests(unittest.TestCase):
    def make_adapter(self) -> tuple[JevAdapter, FakeJevConnection]:
        connection = FakeJevConnection()
        return JevAdapter(api_key="test-key", connection=connection), connection

    def test_the_request_batches_claims_of_one_cluster(self) -> None:
        record = load_fixture("zup-codegen")
        paragraphs = capture_paragraphs(record, "s1")
        claims = [claim for claim in record.claims if claim.field.startswith("architecture.")]
        state, questions = build_request(claims, paragraphs)
        self.assertEqual(len(state["assertions"]), 4)
        self.assertIn("passage", state)
        self.assertIn("a0_relation", questions)
        self.assertIn("a1_actor", questions)
        self.assertIn("a2_temporal", questions)
        self.assertIn("a3_approval", questions)

    def test_judging_fills_every_judgment_and_the_stage_facts(self) -> None:
        adapter, connection = self.make_adapter()
        record = load_fixture("zup-codegen")
        paragraphs = {"s1": capture_paragraphs(record, "s1")}
        budget = Budget(budget_usd=1.0)
        with tempfile.TemporaryDirectory() as directory:
            cache = JsonCache(Path(directory) / "jev.json")
            outcome = judge_claims(record, paragraphs, adapter=adapter, budget=budget, cache=cache)
            judged = [claim for claim in outcome.record.claims if claim.judgments is not None]
            self.assertTrue(judged)
            self.assertGreaterEqual(outcome.stage["calls"], 1)
            self.assertEqual(outcome.stage["model"], "jev-1.13.0")
            # Every sent request carried the five questions per claim.
            for payload in connection.requests:
                keys = set(payload["questions"])
                for suffix in ("_relation", "_actor", "_temporal", "_approval", "_basis"):
                    self.assertTrue(
                        any(key.endswith(suffix) for key in keys),
                        f"request lacks a {suffix} question",
                    )
            # A rerun with the warm cache makes no new requests.
            judged_claims = sum(
                1
                for claim in record.claims
                if claim.id is not None and any(quote.match == "exact" for quote in claim.quotes)
            )
            outcome_two = judge_claims(
                record, paragraphs, adapter=adapter, budget=budget, cache=cache
            )
            self.assertEqual(outcome_two.stage["calls"], 0)
            self.assertEqual(outcome_two.stage["cache_hits"], judged_claims)

    def test_the_coarse_gate_accepts_only_clearly_stated_verified_claims(self) -> None:
        record = load_fixture("zup-codegen")
        adapter, _connection = self.make_adapter()
        paragraphs = {"s1": capture_paragraphs(record, "s1")}
        budget = Budget(budget_usd=1.0)
        with tempfile.TemporaryDirectory() as directory:
            cache = JsonCache(Path(directory) / "jev.json")
            judged = judge_claims(record, paragraphs, adapter=adapter, budget=budget, cache=cache)
        gated = apply_dispositions(judged.record)
        accepted = [claim for claim in gated.claims if claim.disposition == "accept"]
        self.assertTrue(accepted)
        for claim in accepted:
            judgments = claim.judgments
            assert judgments is not None
            self.assertGreaterEqual(judgments.relation.p, GATE["relation_stated_min"])  # type: ignore[union-attr]
            self.assertTrue(any(quote.match == "exact" for quote in claim.quotes))

    def test_a_fuzzy_quote_never_accepts(self) -> None:
        record = load_fixture("zup-codegen")
        adapter, _connection = self.make_adapter()
        claims = []
        for claim in record.claims:
            quotes = [
                quote.model_copy(update={"match": "fuzzy", "lines": None}) for quote in claim.quotes
            ]
            claims.append(claim.model_copy(update={"quotes": quotes}))
        fuzzy = record.model_copy(update={"claims": claims})
        gated = apply_dispositions(fuzzy)
        for claim in gated.claims:
            if claim.provenance == "reported":
                self.assertIn(claim.disposition, ("review", "drop"))

    def test_a_missing_quote_on_a_reported_claim_drops(self) -> None:
        record = load_fixture("zup-codegen")
        claims = [
            claim.model_copy(
                update={
                    "quotes": [
                        quote.model_copy(update={"match": "missing", "lines": None})
                        for quote in claim.quotes
                    ]
                }
            )
            for claim in record.claims
        ]
        gated = apply_dispositions(record.model_copy(update={"claims": claims}))
        dropped = [
            claim
            for claim in gated.claims
            if claim.disposition == "drop" and claim.provenance == "reported"
        ]
        self.assertTrue(dropped)

    def test_a_number_disagreement_blocks_acceptance(self) -> None:
        record = load_fixture("plaid-ai-annotator")
        claims = []
        for claim in record.claims:
            if claim.field == "headline_metric":
                numbers = [
                    check.model_copy(update={"in_quote": False}) for check in claim.numbers
                ] or None
                if numbers is None:
                    from intake.models import NumberCheck

                    numbers = [NumberCheck(claim="99%", in_quote=False)]
                claims.append(claim.model_copy(update={"numbers": numbers}))
            else:
                claims.append(claim)
        gated = apply_dispositions(record.model_copy(update={"claims": claims}))
        headline = next(claim for claim in gated.claims if claim.field == "headline_metric")
        self.assertEqual(headline.disposition, "review")


class IdentityQuestionTests(unittest.TestCase):
    def test_the_identity_question_names_each_shortlisted_record(self) -> None:
        questions = jev_identity_questions(
            "River",
            [
                {"id": "shopify-internal-agents", "agent_name": "Aquifer / River", "score": 1.0},
                {"id": "shopify-roast", "agent_name": "Roast", "score": 0.6},
            ],
        )
        self.assertIn("same_0", questions)
        self.assertIn(
            "Aquifer / River (shopify-internal-agents)", questions["same_0"]["instructions"]
        )
        self.assertEqual(questions["same_1"]["type"], "noul")

    def test_refine_with_jev_adds_the_advisory_probability(self) -> None:
        connection = FakeJevConnection()
        adapter = JevAdapter(api_key="test-key", connection=connection)
        identity = resolve_identity(company="Shopify", system_name="River")
        refined = refine_with_jev(
            identity,
            passage="River is Shopify's Slack-native coding agent.",
            candidate_name="River",
            adapter=adapter,
            budget=Budget(budget_usd=1.0),
        )
        self.assertIn("same_system_jev", refined["matched_records"][0])
        self.assertEqual(refined["jev_model"], "jev-1.13.0")
        self.assertEqual(refined["decision_basis"]["rule"], "jev-identity-bands")

    def refined_with(self, noul: float) -> dict[str, Any]:
        identity = resolve_identity(company="Shopify", system_name="River")
        return refine_with_jev(
            identity,
            passage="River is Shopify's Slack-native coding agent.",
            candidate_name="River",
            adapter=BandedIdentityJev(noul),
            budget=Budget(budget_usd=1.0),
        )

    def test_a_high_probability_proposes_update(self) -> None:
        refined = self.refined_with(0.9)
        self.assertEqual(refined["proposed_decision"], "update")
        basis = refined["decision_basis"]
        self.assertEqual(basis["rule"], "jev-identity-bands")
        self.assertEqual(basis["top_same_system_jev"], 0.9)
        self.assertEqual(basis["update_min"], 0.8)
        self.assertFalse(basis["calibrated"])

    def test_a_middle_probability_proposes_review(self) -> None:
        refined = self.refined_with(0.5)
        self.assertEqual(refined["proposed_decision"], "review")
        self.assertEqual(refined["decision_basis"]["top_same_system_jev"], 0.5)

    def test_a_low_probability_proposes_add(self) -> None:
        refined = self.refined_with(0.1)
        self.assertEqual(refined["proposed_decision"], "add")

    def test_without_an_answer_the_deterministic_decision_stands(self) -> None:
        class SilentJev:
            def ask(self, *, state: Any, questions: Any, budget: Any) -> JevResult:
                return JevResult(
                    answers={},
                    model="jev-1.13.0",
                    input_tokens=10,
                    output_tokens=0,
                    cost_usd=0.0,
                    cache_hit=False,
                )

        identity = resolve_identity(company="Shopify", system_name="River")
        refined = refine_with_jev(
            identity,
            passage="River is Shopify's Slack-native coding agent.",
            candidate_name="River",
            adapter=SilentJev(),  # type: ignore[arg-type]
            budget=Budget(budget_usd=1.0),
        )
        self.assertEqual(refined["proposed_decision"], identity["proposed_decision"])
        self.assertEqual(refined["decision_basis"], {"rule": "deterministic"})

    def test_a_warm_identity_cache_makes_no_new_calls(self) -> None:
        import tempfile
        from pathlib import Path

        from intake.cache import JsonCache

        with tempfile.TemporaryDirectory() as directory:
            cache = JsonCache(Path(directory) / "identity.json")
            connection = FakeJevConnection()
            adapter = JevAdapter(api_key="test-key", connection=connection)
            identity = resolve_identity(company="Shopify", system_name="River")
            first = refine_with_jev(
                identity,
                passage="River is Shopify's Slack-native coding agent.",
                candidate_name="River",
                adapter=adapter,
                budget=Budget(budget_usd=1.0),
                cache=cache,
            )
            self.assertEqual(len(connection.requests), 1)
            second = refine_with_jev(
                identity,
                passage="River is Shopify's Slack-native coding agent.",
                candidate_name="River",
                adapter=adapter,
                budget=Budget(budget_usd=1.0),
                cache=cache,
            )
            self.assertEqual(len(connection.requests), 1)
            self.assertTrue(second["jev_usage"]["cache_hit"])
            self.assertEqual(
                first["matched_records"][0]["same_system_jev"],
                second["matched_records"][0]["same_system_jev"],
            )
            # The bands apply on the warm path too, not only on a fresh ask.
            self.assertEqual(second["proposed_decision"], first["proposed_decision"])
            self.assertEqual(second["decision_basis"], first["decision_basis"])


class EvaluationHarnessTests(unittest.TestCase):
    def test_items_are_sampled_with_passages_and_empty_labels(self) -> None:
        items = build_items(count=12)
        self.assertGreater(len(items), 0)
        for item in items:
            self.assertTrue(item["passage"].strip())
            self.assertIn(item["labels"]["adjudicated"], (None,))
        # The build is reproducible for a fixed seed.
        again = build_items(count=12)
        self.assertEqual([item["item_id"] for item in items], [i["item_id"] for i in again])

    def test_scoring_measures_defect_recall_and_alert_precision(self) -> None:
        items = build_items(count=10)
        labels = ["support", "explicit-conflict", "insufficient", "support", "ambiguity"] * 2
        for item, label in zip(items, labels):
            item["labels"]["adjudicated"] = label
        verdicts = {
            item["item_id"]: ("review" if item["labels"]["adjudicated"] != "support" else "accept")
            for item in items
        }
        report = score(items, verdicts)
        self.assertEqual(report["defect_recall"], 1.0)
        self.assertEqual(report["alert_precision"], 1.0)
        self.assertTrue(report["gate"]["passes"])
        missed = dict(verdicts)
        first_defect = next(
            item["item_id"]
            for item in items
            if item["labels"]["adjudicated"] == "explicit-conflict"
        )
        missed[first_defect] = "accept"
        failed = score(items, missed)
        self.assertLess(failed["defect_recall"], 0.9)
        self.assertFalse(failed["gate"]["passes"])

    def test_labeller_agreement_counts_only_fully_labelled_items(self) -> None:
        items = build_items(count=4)
        self.assertEqual(labeller_agreement(items), {"labelled": 0})
        items[0]["labels"]["labeller_a"] = "support"
        self.assertEqual(labeller_agreement(items), {"labelled": 0})
        items[0]["labels"]["labeller_b"] = "support"
        items[1]["labels"]["labeller_a"] = "insufficient"
        items[1]["labels"]["labeller_b"] = "ambiguity"
        report = labeller_agreement(items)
        self.assertEqual(report["labelled"], 2)
        self.assertEqual(report["agreement"], 0.5)

    def test_written_item_files_are_never_overwritten(self) -> None:
        items = build_items(count=2)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "items.json"
            write_items(items, path)
            with self.assertRaises(FileExistsError):
                write_items(items, path)


if __name__ == "__main__":
    unittest.main()
