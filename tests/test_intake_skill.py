# ABOUTME: The skill's configuration and golden cases cannot drift from the code.
"""Hold the intake skill's config and eval set to the code's versions.

The plan's ongoing-evaluation rule: the skill's ``evals/`` folder keeps the
golden cases, and a change to a prompt or question version reruns them before
it ships. Nothing can force the live rerun offline, but the versions, the
thresholds, and the golden files can be pinned to the code, so a bump on
either side fails this suite until the skill is updated and the goldens rerun.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from intake.adapters.jev import MODEL as JEV_MODEL
from intake.adapters.writer import DEFAULT_MODEL, DEFAULT_REASONING_EFFORT
from intake.extract import PROMPT_VERSION as EXTRACT_PROMPT
from intake.judge import GATE, QUESTION_VERSION
from intake.run import DEFAULT_BUDGET_USD
from intake.verify_quotes import DEFAULT_SIMILARITY_BOUND
from intake.write import PROMPT_VERSION as WRITE_PROMPT

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".claude" / "skills" / "intake"
GOLDEN_NAMES = (
    "zup-codegen",
    "plaid-ai-annotator",
    "duolingo-agentic-workflows",
)


class SkillConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = json.loads((SKILL / "config.json").read_text(encoding="utf-8"))

    def test_the_writer_configuration_names_the_code_defaults(self) -> None:
        writer = self.config["writer"]
        self.assertEqual(writer["model"], DEFAULT_MODEL)
        self.assertEqual(writer["reasoning_effort"], DEFAULT_REASONING_EFFORT)
        self.assertEqual(writer["prompts"]["extract"], EXTRACT_PROMPT)
        self.assertEqual(writer["prompts"]["write"], WRITE_PROMPT)

    def test_the_jev_and_gate_configuration_names_the_code_defaults(self) -> None:
        jev = self.config["jev"]
        self.assertEqual(jev["model"], JEV_MODEL)
        self.assertEqual(jev["question_version"], QUESTION_VERSION)
        gate = self.config["gate"]
        for key in (
            "model",
            "question_version",
            "relation_stated_min",
            "actor_mismatch_max",
            "approval_removed_max",
            "temporal_current_min",
        ):
            self.assertEqual(gate[key], GATE[key], key)
        # The Phase 3 calibration never ran; the flag stays honest about it.
        self.assertFalse(gate["calibrated"])

    def test_the_identity_gate_names_the_code_defaults(self) -> None:
        from intake.resolve import IDENTITY_GATE

        identity_gate = self.config["identity_gate"]
        self.assertEqual(identity_gate, IDENTITY_GATE)
        self.assertFalse(identity_gate["calibrated"])

    def test_the_budget_and_quote_bound_name_the_code_defaults(self) -> None:
        from intake.__main__ import build_parser

        parser = build_parser()
        cli_budgets = {
            "run_usd": parser.parse_args(["run", "queue.yaml"]).budget_usd,
            "backtest_usd": parser.parse_args(["backtest"]).budget_usd,
            "backfill_usd": parser.parse_args(["backfill", "record.yaml"]).budget_usd,
            "drift_usd": parser.parse_args(["drift"]).budget_usd,
            "evals_usd": parser.parse_args(["evals", "--items", "items.json"]).budget_usd,
        }
        self.assertEqual(self.config["budgets"], cli_budgets)
        self.assertEqual(self.config["budgets"]["run_usd"], DEFAULT_BUDGET_USD)
        self.assertEqual(self.config["quotes"]["fuzzy_similarity_bound"], DEFAULT_SIMILARITY_BOUND)


class GoldenCaseTests(unittest.TestCase):
    def test_the_skill_eval_set_is_the_test_fixture_set(self) -> None:
        """A fixture edit must carry into the eval set, never drift apart."""
        for name in GOLDEN_NAMES:
            skill_file = SKILL / "evals" / f"{name}.extraction.yaml"
            fixture = ROOT / "tests" / "fixtures" / "intake" / f"{name}.extraction.yaml"
            self.assertTrue(skill_file.is_file(), f"{name}: missing from the eval set")
            self.assertEqual(
                skill_file.read_bytes(),
                fixture.read_bytes(),
                f"{name}: the skill's eval copy must match the test fixture",
            )

    def test_the_eval_readme_names_the_rerun_command(self) -> None:
        """The skill must tell its reader how the goldens rerun."""
        readme = (SKILL / "evals" / "README.md").read_text(encoding="utf-8")
        self.assertIn("unittest discover", readme)

    def test_the_skill_names_the_non_drafting_outcomes(self) -> None:
        """The operator's entry point must keep pace with the run's behavior."""
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        # Collection blockers continue the run; the other two outcomes do not.
        self.assertIn("collection blocker", skill)
        self.assertIn("`blocked`", skill)
        self.assertIn("`needs-evidence`", skill)
        # Draft collisions report; they never overwrite.
        self.assertIn("collision", skill)
        # Phase 5's worst-first batching and the hint authority rule.
        self.assertIn("backfill --rank", skill)
        self.assertIn("authoritative over the writer model's echo", skill)


class SchemaCommandTests(unittest.TestCase):
    def test_a_bare_schema_call_writes_the_committed_file(self) -> None:
        """The documented default: no --output refreshes the committed file."""
        import tempfile

        import intake.__main__ as cli

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "extraction-record.v1.json"
            saved = cli.SCHEMA_PATH
            cli.SCHEMA_PATH = target
            try:
                self.assertEqual(cli.main(["schema"]), 0)
            finally:
                cli.SCHEMA_PATH = saved
            payload = json.loads(target.read_text(encoding="utf-8"))
            self.assertIn("extraction_record", payload)


if __name__ == "__main__":
    unittest.main()
