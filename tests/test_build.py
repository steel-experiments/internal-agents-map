from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("catalog_build", ROOT / "scripts" / "build.py")
build = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(build)


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = build.load_agents()

    def test_catalog_has_unique_ids(self) -> None:
        approach_ids = [record["id"] for record in self.records]
        source_ids = [source["id"] for record in self.records for source in record["sources"]]
        self.assertEqual(len(approach_ids), len(set(approach_ids)))
        self.assertEqual(len(source_ids), len(set(source_ids)))

    def test_normalized_export_has_linked_collections(self) -> None:
        export = build.normalize(self.records)
        self.assertEqual(export["schema_version"], 3)
        claim_ids = {claim["id"] for claim in export["claims"]}
        source_ids = {source["id"] for source in export["sources"]}
        self.assertTrue(all(source["role"] in build.SOURCE_ROLES for source in export["sources"]))
        for approach in export["approaches"]:
            self.assertTrue(set(approach["claim_ids"]).issubset(claim_ids))
            self.assertTrue(set(approach["source_ids"]).issubset(source_ids))
            self.assertTrue(approach["operating_models"])
            for item in approach["operating_models"]:
                expected = build.BOUNDARY_LEVELS[item["attention_boundary"]]
                self.assertEqual(item["level"], expected)
        for claim in export["claims"]:
            self.assertTrue(claim["evidence"])
            self.assertIn(claim["confidence"], build.CONFIDENCE)
            self.assertTrue({item["source_id"] for item in claim["evidence"]}.issubset(source_ids))
            if claim["field"].startswith("operating_models."):
                self.assertEqual(claim["kind"], "inference")
                self.assertEqual(claim["provenance"], "catalog-judgment")
                self.assertTrue(claim["valid_at"])

    def test_generated_files_are_current(self) -> None:
        outputs = build.rendered_outputs(self.records)
        for path, expected in outputs.items():
            self.assertEqual(path.read_text(encoding="utf-8"), expected)

    def test_catalog_contains_source_anchors(self) -> None:
        catalog = build.render_landscape(self.records)
        for record in self.records:
            for source in record["sources"]:
                self.assertIn(f'<a id="{source["id"]}"></a>', catalog)

    def test_catalog_contains_comparison_links(self) -> None:
        catalog = build.render_landscape(self.records)
        for record in self.records:
            self.assertIn(f"[{record['agent_name']}](#{record['id']})", catalog)

    def test_overview_counts_match_export(self) -> None:
        export = build.normalize(self.records)
        company_count = len({record["company"] for record in self.records})
        overview = build.render_overview(self.records)
        self.assertIn(f"{len(self.records)} approaches", overview)
        self.assertIn(f"{company_count} organizations", overview)
        self.assertIn(f"{len(export['sources'])} sources", overview)
        self.assertIn(f"{len(export['claims'])} evidence-linked claims", overview)

    def test_readme_overview_contains_every_approach(self) -> None:
        overview = build.render_overview_table(self.records)
        for record in self.records:
            self.assertIn(
                f"[{record['agent_name']}](docs/landscape.md#{record['id']})",
                overview,
            )

    def test_readme_findings_counts_are_current(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        autonomy_counts = Counter(record["autonomy"] for record in self.records)
        unknown_state_count = sum(record["rubric"]["state"] == "unknown" for record in self.records)
        self.assertIn(
            f"{autonomy_counts['drafts-reviewed']} of the {len(self.records)} approaches",
            readme,
        )
        self.assertIn(
            f"{autonomy_counts['human-in-loop']} keep a person involved",
            readme,
        )
        self.assertIn(
            f"{autonomy_counts['autonomous']} report autonomous action",
            readme,
        )
        self.assertIn(
            f"State duration is undocumented for {unknown_state_count} approaches",
            readme,
        )

    def test_analysis_snapshots_match_catalog(self) -> None:
        patterns = build.render_patterns_snapshot(self.records)
        adoption = build.render_adoption_snapshot(self.records)
        autonomy_counts = Counter(record["autonomy"] for record in self.records)
        self.assertIn(f"contains {len(self.records)} approaches", patterns)
        self.assertIn(f"draw on {len(self.records)} cataloged approaches", adoption)
        self.assertIn(
            f"{autonomy_counts['drafts-reviewed']} `drafts-reviewed`",
            adoption,
        )

    def test_markdown_escapes_table_values(self) -> None:
        self.assertEqual(build.markdown("Acme | Corp\nTeam"), "Acme \\| Corp Team")
        self.assertEqual(build.markdown(["slack", "web"]), "slack, web")

    def test_duplicate_yaml_keys_fail(self) -> None:
        with self.assertRaises(yaml.constructor.ConstructorError):
            yaml.load("id: first\nid: second\n", Loader=build.UniqueKeyLoader)

    def test_invalid_nested_value_fails_before_render(self) -> None:
        record = copy.deepcopy(self.records[0])
        record["architecture"]["sandbox"] = ["not", "a", "string"]
        with (
            tempfile.TemporaryDirectory() as directory,
            contextlib.redirect_stderr(io.StringIO()),
            self.assertRaises(SystemExit),
        ):
            path = Path(directory) / f"{record['id']}.yaml"
            build.validate_record(record, path, set())

    def test_invalid_attention_boundary_fails_before_render(self) -> None:
        record = copy.deepcopy(self.records[0])
        record["operating_models"][0]["attention_boundary"] = "sometimes"
        with (
            tempfile.TemporaryDirectory() as directory,
            contextlib.redirect_stderr(io.StringIO()),
            self.assertRaises(SystemExit),
        ):
            path = Path(directory) / f"{record['id']}.yaml"
            build.validate_record(record, path, set())

    def test_impossible_calendar_date_fails(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            build.validate_date("2026-02-31", "last_reviewed_at", "example.yaml")

    def test_json_is_serializable(self) -> None:
        json.dumps(build.normalize(self.records))

    def test_template_matches_schema(self) -> None:
        template = yaml.safe_load((ROOT / "templates" / "agent.yaml").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "company-agent.yaml"
            build.validate_record(template, path, set())

    def test_documented_sample_counts_are_current(self) -> None:
        patterns = (ROOT / "docs" / "patterns.md").read_text(encoding="utf-8")
        labels = {
            "task-agent": "Task agent",
            "platform": "Platform",
            "background-agent": "Background agent",
            "agent-system": "Agent system",
            "orchestration-system": "Orchestration system",
            "supporting-pattern": "Supporting pattern",
        }
        counts = Counter(record["approach_type"] for record in self.records)
        for value, label in labels.items():
            self.assertIn(f"| {label} | {counts[value]} |", patterns)


if __name__ == "__main__":
    unittest.main()
