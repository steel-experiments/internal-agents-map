from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any

import yaml

from intake.adapters.jev import JevAnswer, JevResult
from intake.budget import Budget
from intake.cache import JsonCache
from intake.evals import (
    build_items,
    labeller_agreement,
    run_verdicts,
    score,
    split_groups,
    stability,
    stress_items,
    write_items,
)
from intake.judge import GATE, gates_pass
from intake.models import Judgments, Verdict

ROOT = Path(__file__).resolve().parents[1]


class GatesPassTests(unittest.TestCase):
    def judgments(
        self,
        *,
        relation_p: float,
        actor: float = 0.05,
        temporal_p: float | None = None,
    ) -> Judgments:
        return Judgments(
            relation=Verdict(label="stated", p=relation_p),
            actor_mismatch=actor,
            temporal=Verdict(label="current", p=temporal_p) if temporal_p is not None else None,
            approval_removed=0.05,
            basis=None,
            model="jev-1.13.0",
            question_version=1,
        )

    def test_a_stated_relation_above_the_bound_passes(self) -> None:
        self.assertTrue(gates_pass(self.judgments(relation_p=0.95), GATE))

    def test_a_weak_relation_fails(self) -> None:
        self.assertFalse(gates_pass(self.judgments(relation_p=0.5), GATE))

    def test_an_actor_flag_above_the_bound_fails(self) -> None:
        self.assertFalse(gates_pass(self.judgments(relation_p=0.95, actor=0.6), GATE))

    def test_a_current_temporal_claim_needs_its_own_bound(self) -> None:
        self.assertFalse(gates_pass(self.judgments(relation_p=0.95, temporal_p=0.3), GATE))
        self.assertTrue(gates_pass(self.judgments(relation_p=0.95, temporal_p=0.7), GATE))

    def test_no_judgments_passes_the_judgment_half(self) -> None:
        self.assertTrue(gates_pass(None, GATE))


class FakeJev:
    """The Jev seam: one canned answer set for every request."""

    def __init__(self, relation_p: float) -> None:
        self._relation_p = relation_p
        self.calls = 0

    def ask(self, *, state: dict[str, Any], questions: dict[str, Any], budget: Any) -> JevResult:
        self.calls += 1
        answers = {
            "a0_relation": JevAnswer(
                type="choice",
                choice="stated",
                probabilities={"stated": self._relation_p, "unknown": 1 - self._relation_p},
            ),
            "a0_actor": JevAnswer(type="noul", noul=0.05),
            "a0_temporal": JevAnswer(type="choice", choice="past", probabilities={"past": 0.9}),
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


class BuildItemsTests(unittest.TestCase):
    def test_items_sample_located_claims_with_passages(self) -> None:
        record = yaml.safe_load(
            (ROOT / "data" / "agents" / "zup-codegen.yaml").read_text(encoding="utf-8")
        )
        items = build_items([record], count=3)
        self.assertTrue(items)
        for item in items:
            self.assertTrue(item["item_id"].startswith("item-"))
            self.assertIn("Preserved content.md", item["locator"])
            self.assertTrue(item["passage"].strip())

    def test_write_items_never_overwrites(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "items.json"
            write_items([], path)
            with self.assertRaises(FileExistsError):
                write_items([], path)


class RunVerdictsTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        record = yaml.safe_load(
            (ROOT / "data" / "agents" / "zup-codegen.yaml").read_text(encoding="utf-8")
        )
        self.items = build_items([record], count=2)
        self.cache = JsonCache(Path(self._tmp.name) / "cache.json")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_a_stated_relation_yields_accept(self) -> None:
        fake = FakeJev(relation_p=0.95)
        verdicts = run_verdicts(
            self.items,
            adapter=fake,
            budget=Budget(budget_usd=20.0),
            cache=self.cache,
        )
        self.assertEqual(set(verdicts), {item["item_id"] for item in self.items})
        self.assertEqual(set(verdicts.values()), {"accept"})
        self.assertEqual(fake.calls, len(self.items))

    def test_a_weak_relation_yields_review(self) -> None:
        verdicts = run_verdicts(
            self.items,
            adapter=FakeJev(relation_p=0.4),
            budget=Budget(budget_usd=20.0),
            cache=self.cache,
        )
        self.assertEqual(set(verdicts.values()), {"review"})

    def test_a_warm_cache_makes_no_new_calls(self) -> None:
        run_verdicts(
            self.items,
            adapter=FakeJev(relation_p=0.95),
            budget=Budget(budget_usd=20.0),
            cache=self.cache,
        )
        cold = FakeJev(relation_p=0.4)
        verdicts = run_verdicts(
            self.items, adapter=cold, budget=Budget(budget_usd=20.0), cache=self.cache
        )
        self.assertEqual(cold.calls, 0)
        self.assertEqual(set(verdicts.values()), {"accept"})


class ScoreTests(unittest.TestCase):
    @staticmethod
    def items_with_labels() -> list[dict[str, Any]]:
        labels = ["insufficient"] + ["ambiguity"] * 4 + ["support"] * 5
        return [
            {
                "item_id": f"item-{index:04d}",
                "labels": {"labeller_a": label, "labeller_b": label, "adjudicated": label},
            }
            for index, label in enumerate(labels)
        ]

    def test_the_gate_measures_recall_and_precision(self) -> None:
        items = self.items_with_labels()
        verdicts = {item["item_id"]: "accept" for item in items}
        verdicts["item-0000"] = "review"  # the caught defect
        for index in range(1, 5):
            verdicts[f"item-{index:04d}"] = "review"  # ambiguities: true alerts
        verdicts["item-0005"] = "review"  # clean support: the one false alert
        report = score(items, verdicts)
        self.assertEqual(report["scored"], 10)
        self.assertEqual(report["defects"], 1)
        self.assertEqual(report["defect_recall"], 1.0)
        self.assertEqual(report["alerts"], 6)
        self.assertEqual(report["alert_precision"], round(5 / 6, 4))
        self.assertTrue(report["gate"]["passes"])

    def test_a_missed_defect_fails_the_gate(self) -> None:
        items = self.items_with_labels()
        verdicts = {item["item_id"]: "accept" for item in items}
        for index in range(1, 5):
            verdicts[f"item-{index:04d}"] = "review"
        report = score(items, verdicts)
        self.assertEqual(report["defect_recall"], 0.0)
        self.assertFalse(report["gate"]["passes"])

    def test_labeller_agreement_counts_pairs(self) -> None:
        items = self.items_with_labels()
        items[0]["labels"]["labeller_b"] = "ambiguity"
        report = labeller_agreement(items)
        self.assertEqual(report["labelled"], 10)
        self.assertEqual(report["agreeing"], 9)
        self.assertEqual(report["agreement"], 0.9)


class TrackSplitStressTests(unittest.TestCase):
    """The evaluation mechanics Plan 016 specified and Phase 3 adopts."""

    def test_the_retrieval_track_finds_a_passage_by_search(self) -> None:
        oracle = build_items(count=20, track="oracle")
        retrieval = build_items(count=20, track="retrieval")
        self.assertTrue(oracle)
        self.assertTrue(retrieval)
        self.assertTrue(all(item["track"] == "retrieval" for item in retrieval))
        # The searched passage shares words with the claim it must support.
        for item in retrieval:
            self.assertTrue(item["passage"].strip())
        # The zup record's claims retrieve passages that overlap them.
        everything = build_items(count=10_000, track="retrieval")
        zup = [item for item in everything if item["record_id"] == "zup-codegen"]
        self.assertTrue(zup)
        from intake.evals import _tokens

        for item in zup:
            self.assertTrue(_tokens(item["claim_text"]) & _tokens(item["passage"]))

    def test_grouped_splits_keep_whole_records_on_one_side(self) -> None:
        items = build_items(count=40)
        groups = split_groups(items)
        calibration_records = {item["record_id"] for item in groups["calibration"]}
        test_records = {item["record_id"] for item in groups["test"]}
        self.assertFalse(calibration_records & test_records)
        self.assertEqual(len(groups["calibration"]) + len(groups["test"]), len(items))
        # Deterministic for a fixed seed.
        again = split_groups(items)
        self.assertEqual(groups, again)

    def test_stress_repeats_permute_and_report_stability(self) -> None:
        items = build_items(count=6)
        stressed = stress_items(items, repeats=3)
        self.assertEqual(len(stressed), 18)
        ids = [item["item_id"] for item in stressed]
        self.assertEqual(len(set(ids)), 18)
        groups = {item["repeat_group"] for item in stressed}
        self.assertEqual(groups, {item["item_id"] for item in items})
        verdicts = {item["item_id"]: "accept" for item in stressed}
        self.assertEqual(stability(stressed, verdicts)["stability"], 1.0)
        verdicts[ids[0]] = "review"
        report = stability(stressed, verdicts)
        self.assertLess(report["stability"], 1.0)
        self.assertEqual(report["repeated_groups"], 6)
        # Without repeats there is nothing to report.
        self.assertEqual(
            stability(items, {item["item_id"]: "accept" for item in items}),
            {
                "repeated_groups": 0,
            },
        )


if __name__ == "__main__":
    unittest.main()
