"""Behavioral contracts for the generated static site and its publication boundary."""

import copy
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build = load_script("build")
checker = load_script("check_site")


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "data/agents.json").read_text())
        cls.html = build.render_site(cls.catalog)

    def test_complete_catalog_and_all_evidence_relations(self):
        parsed = checker.SiteParser()
        parsed.feed(self.html)
        for key, collection in [
            ("approach", "approaches"),
            ("claim", "claims"),
            ("source", "sources"),
        ]:
            self.assertCountEqual(
                parsed.coverage[key], [item["id"] for item in self.catalog[collection]]
            )
        self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
        self.assertIn("relation-contradicts", self.html)
        self.assertIn("relation-contextualizes", self.html)
        for claim in self.catalog["claims"]:
            self.assertIn(build.site_text(claim["text"]), self.html)
            for evidence in claim["evidence"]:
                if evidence.get("locator"):
                    self.assertIn(build.site_text(evidence["locator"]), self.html)
        expected_order = sorted(
            self.catalog["approaches"],
            key=lambda a: (a["company"].casefold(), a["agent_name"].casefold(), a["id"]),
        )
        self.assertEqual(parsed.coverage["approach"], [a["id"] for a in expected_order])

    def test_definitions_placements_require_matching_workflow_metadata(self):
        html = build.render_definitions(self.catalog)
        self.assertEqual(html.count("data-chart-approach-id="), 6)
        self.assertIn('href="index.html#sentry-junior"', html)
        self.assertNotIn("@@", html)
        changed = copy.deepcopy(self.catalog)
        for approach in changed["approaches"]:
            if approach["id"] == "sentry-junior":
                approach["operating_models"] = []
            if approach["id"] == "stripe-minions":
                approach["rubric"]["invocation"] = ["unknown"]
        html = build.render_definitions(changed)
        self.assertEqual(html.count("data-chart-approach-id="), 4)
        self.assertNotIn('data-chart-approach-id="sentry-junior"', html)
        self.assertNotIn('data-chart-approach-id="stripe-minions"', html)

    def fixture(self):
        source = copy.deepcopy(self.catalog["sources"][0])
        approach = copy.deepcopy(self.catalog["approaches"][0])
        claim = copy.deepcopy(self.catalog["claims"][0])
        approach["claim_ids"] = [claim["id"]]
        approach["source_ids"] = [source["id"]]
        claim["evidence"] = [{"source_id": source["id"], "relation": "supports"}]
        return {
            "schema_version": 4,
            "approaches": [approach],
            "claims": [claim],
            "sources": [source],
        }

    def test_kind_overrides_unknowns_scopes_and_metric_qualifications(self):
        fixture = self.fixture()
        claim = fixture["claims"][0]
        claim.update(
            field="key_metrics.0",
            kind="opinion",
            provenance="inferred",
            text="A target, not a measured result.",
        )
        page = build.render_site(fixture)
        self.assertNotIn("<h4>Reported metrics</h4>", page)
        self.assertIn("<h4>Other reported details and interpretation</h4>", page)
        claim.update(
            kind="metric",
            confidence="low",
            valid_at=None,
            reported_by="Fixture company",
            metric_scope="Pilot only",
            denominator="Unknown",
        )
        fixture["approaches"][0]["operating_models"] = [
            {"scope": "Draft code", "attention_boundary": "work-product-review", "level": 3},
            {"scope": "Investigate alerts", "attention_boundary": "exception-only", "level": 5},
        ]
        fixture["approaches"][0]["domains"] = []
        page = build.render_site(fixture)
        self.assertIn("<h4>Reported metrics</h4>", page)
        self.assertIn("Low confidence", page)
        self.assertIn("<dt>Observation date</dt><dd>Unknown</dd>", page)
        self.assertIn("<dt>Method</dt><dd>Unknown</dd>", page)
        self.assertIn("Pilot only", page)
        self.assertIn("Draft code", page)
        self.assertIn("Investigate alerts", page)
        self.assertIn('data-supervision="exception-only work-product-review"', page)
        self.assertIn('<option value="unknown">Unknown</option>', page)

    def test_uber_conflict_is_preserved(self):
        uber = [
            c
            for c in self.catalog["claims"]
            if c["approach_id"] == "uber-ureview"
            and any(e.get("relation") == "contradicts" for e in c["evidence"])
        ]
        self.assertTrue(uber)
        for claim in uber:
            self.assertIn(build.site_text(claim["text"]), self.html)
            self.assertEqual(claim["confidence"], "low")
            for field in ["metric_scope", "denominator", "measurement_method"]:
                if claim.get(field):
                    self.assertIn(build.site_text(claim[field]), self.html)

    def test_prose_is_text_and_attributes_are_escaped(self):
        fixture = self.fixture()
        dangerous = '<img src=x onerror="alert(1)"> Héllo & "quotes"'
        fixture["claims"][0]["text"] = dangerous
        fixture["approaches"][0]["company"] = dangerous
        fixture["sources"][0]["title"] = dangerous
        fixture["sources"][0]["url"] = "javascript:alert(1)"
        page = build.render_site(fixture)
        self.assertIn(build.site_text(dangerous), page)
        self.assertNotIn("<img", page)
        parser = checker.SiteParser()
        parser.feed(page)
        self.assertFalse(any(url.startswith("javascript:") for url in parser.urls))
        self.assertIn(dangerous, "".join(parser.text))

    def test_original_and_preserved_links_are_distinct_without_fabrication(self):
        fixture = self.fixture()
        source = fixture["sources"][0]
        source.pop("archived_url", None)
        page = build.render_site(fixture)
        self.assertIn('href="' + source["url"] + '"', page)
        self.assertIn("blob/main/" + source["capture"]["artifacts"]["markdown"]["path"], page)
        self.assertNotIn("Wayback snapshot", page)
        self.assertNotIn("page.pdf", page)
        source.pop("capture")
        self.assertNotIn("Preserved Markdown", build.render_site(fixture))

    def test_empty_catalog_and_determinism(self):
        empty = {"approaches": [], "claims": [], "sources": []}
        page = build.render_site(empty)
        self.assertIn("0 approaches", page)
        self.assertIn("<time>Unknown</time>", page)
        self.assertEqual(build.render_site(self.catalog), self.html)

    def test_output_map_and_binary_staging_and_stale_checks(self):
        records = build.load_agents()
        outputs = build.rendered_outputs(records)
        self.assertEqual(outputs[ROOT / "site/agents.json"], outputs[build.DATA_JSON])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relocated = {
                root / path.relative_to(ROOT): content for path, content in outputs.items()
            }
            with mock.patch.object(build, "ROOT", root):
                build.write_outputs(relocated)
                for path, content in relocated.items():
                    self.assertEqual(
                        path.read_bytes(), content.encode() if isinstance(content, str) else content
                    )
                with (
                    mock.patch.object(build, "load_agents", return_value=records),
                    mock.patch.object(build, "rendered_outputs", return_value=relocated),
                    mock.patch.object(sys, "argv", ["build.py", "--check"]),
                ):
                    build.main()
                    for name in [
                        "index.html",
                        "definitions.html",
                        "agents.json",
                        "assets/site.css",
                        "assets/site.js",
                        "assets/fonts/Geist.woff2",
                    ]:
                        path = root / "site" / name
                        original = path.read_bytes()
                        for replacement in [b"stale", None]:
                            if replacement is None:
                                path.unlink()
                            else:
                                path.write_bytes(replacement)
                            with self.assertRaises(SystemExit):
                                build.main()
                            path.write_bytes(original)


class ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "internal-agents-map"
        shutil.copytree(ROOT / "site", self.root)

    def change_html(self, old, new):
        path = self.root / "index.html"
        path.write_text(path.read_text().replace(old, new, 1))

    def test_root_and_project_subdirectory(self):
        self.assertEqual(checker.validate(ROOT / "site"), [])
        self.assertEqual(checker.validate(self.root), [])

    def test_missing_asset(self):
        (self.root / "assets/site.css").unlink()
        self.assertTrue(checker.validate(self.root))

    def test_cross_page_fragments_and_document_local_ids(self):
        path = self.root / "definitions.html"
        original = path.read_text()
        self.assertEqual(checker.validate(self.root), [])
        path.write_text(original.replace('href="#terms"', 'href="index.html#terms"'))
        self.assertTrue(any("Invalid fragment" in e for e in checker.validate(self.root)))
        path.write_text(
            original.replace('href="index.html#sentry-junior"', 'href="#sentry-junior"')
        )
        self.assertTrue(any("Invalid fragment" in e for e in checker.validate(self.root)))
        path.unlink()
        self.assertTrue(any("definitions.html" in e for e in checker.validate(self.root)))

    def test_bad_fragment(self):
        self.change_html('href="#main"', 'href="#missing"')
        self.assertTrue(any("fragment" in e for e in checker.validate(self.root)))

    def test_duplicate_id(self):
        self.change_html("<body>", '<body id="main">')
        self.assertTrue(any("Duplicate IDs" in e for e in checker.validate(self.root)))

    def test_escaping_path(self):
        self.change_html('href="assets/site.css"', 'href="../outside.css"')
        self.assertTrue(any("escapes" in e for e in checker.validate(self.root)))

    def test_absolute_asset(self):
        self.change_html('href="assets/site.css"', 'href="/assets/site.css"')
        self.assertTrue(any("relative" in e for e in checker.validate(self.root)))

    def test_executable_scheme(self):
        self.change_html('href="#main"', 'href="javascript:alert(1)"')
        self.assertTrue(any("Unsafe URL" in e for e in checker.validate(self.root)))

    def test_symlink_and_extra_files(self):
        target = self.root / "assets/site.css"
        target.unlink()
        target.symlink_to(ROOT / "site/assets/site.css")
        self.assertTrue(any("Symlink" in e for e in checker.validate(self.root)))
        target.unlink()
        shutil.copy(ROOT / "site/assets/site.css", target)
        (self.root / "unexpected.txt").write_text("unexpected")
        self.assertTrue(any("extra" in e for e in checker.validate(self.root)))

    def test_css_font_path_is_checked(self):
        path = self.root / "assets/site.css"
        path.write_text(path.read_text().replace("fonts/Geist.woff2", "../missing.woff2"))
        self.assertTrue(any("Missing local target" in e for e in checker.validate(self.root)))

    def test_missing_claim_and_json_drift(self):
        self.change_html("data-claim-id=", "data-removed-claim-id=")
        self.assertTrue(any("claim coverage" in e for e in checker.validate(self.root)))
        (self.root / "agents.json").write_text("{}")
        self.assertTrue(any("JSON differs" in e for e in checker.validate(self.root)))

    def test_untracked_artifact_privacy(self):
        self.change_html("</footer>", "<p>" + "fixture" + "@" + "example.invalid" + "</p></footer>")
        self.assertTrue(any("Private contact data" in e for e in checker.validate(self.root)))


class WorkflowTests(unittest.TestCase):
    def test_publication_requires_validated_main_artifact(self):
        workflow = yaml.load(
            (ROOT / ".github/workflows/validate.yml").read_text(), Loader=yaml.BaseLoader
        )
        self.assertIn("on", workflow)
        self.assertIn("github.ref", workflow["concurrency"]["group"])
        self.assertEqual(workflow["concurrency"]["cancel-in-progress"], "true")
        jobs = workflow["jobs"]
        validation = jobs["validate"]
        steps = validation["steps"]
        commands = [step.get("run", "") for step in steps]
        self.assertIn("uv run --locked python scripts/build.py --check", commands)
        self.assertIn("uv run --locked python scripts/check_site.py --root site", commands)
        self.assertNotIn("uv run --locked python scripts/build.py", commands)
        upload = steps[-1]
        self.assertTrue(upload["uses"].startswith("actions/upload-pages-artifact@"))
        self.assertEqual(upload["with"]["path"], "site/")
        deploy = jobs["deploy"]
        self.assertEqual(deploy["needs"], "validate")
        for condition in [upload["if"], deploy["if"]]:
            self.assertIn("github.ref == 'refs/heads/main'", condition)
            self.assertIn("github.event_name == 'push'", condition)
            self.assertIn("github.event_name == 'workflow_dispatch'", condition)
            self.assertNotIn("github.event_name == 'pull_request'", condition)
        self.assertEqual(deploy["environment"]["name"], "github-pages")
        self.assertEqual(deploy["permissions"], {"pages": "write", "id-token": "write"})
        self.assertNotIn("pages", validation.get("permissions", {}))
        self.assertIn("concurrency", deploy)
        for step in steps + deploy["steps"]:
            if "uses" in step:
                self.assertRegex(step["uses"], r"@[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()
