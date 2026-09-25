# ABOUTME: Publication contracts of the built artifact, the hosting policy, and the CI workflow.
# ABOUTME: Covers the sitemap, page metadata, exports, route manifest, and indexing rules.
"""Contracts for agent discovery, evidence exports, and deploy-safe hosting rules."""

import importlib.util
import json
import sys
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ORIGIN = "https://internal-agents.com"
SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


build = load_script("build")


class DocumentParser(HTMLParser):
    """Collect the head elements and the structured data that a page declares."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.metas = []
        self.title = ""
        self.structured_data = []
        self._collect = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "link":
            self.links.append(attributes)
        elif tag == "meta":
            self.metas.append(attributes)
        elif tag == "title":
            self._collect = "title"
        elif tag == "script" and attributes.get("type") == "application/ld+json":
            self._collect = "ld+json"

    def handle_endtag(self, tag):
        self._collect = None

    def handle_data(self, data):
        if self._collect == "title":
            self.title += data
        elif self._collect == "ld+json":
            self.structured_data.append(data)

    def link(self, rel):
        return next((item.get("href") for item in self.links if item.get("rel") == rel), None)

    def meta(self, **match):
        key, value = next(iter(match.items()))
        return next(
            (item.get("content") for item in self.metas if item.get(key) == value),
            None,
        )


def canonical_path(name):
    """The clean public path that one built HTML file is served from."""
    if name == "index.html":
        return "/"
    return "/" + name.removesuffix(".html")


def read_document(name):
    page = DocumentParser()
    page.feed((DIST / name).read_text(encoding="utf-8"))
    return page


class PublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (DIST / "sitemap.xml").is_file():
            raise AssertionError(f"{DIST} holds no build. Run 'npm run build' first.")
        cls.catalog = json.loads((DIST / "agents.json").read_text(encoding="utf-8"))
        cls.pages = sorted(path.relative_to(DIST).as_posix() for path in DIST.rglob("*.html"))
        cls.sitemap = ET.fromstring((DIST / "sitemap.xml").read_text(encoding="utf-8"))

    def test_the_sitemap_lists_every_canonical_page_and_nothing_else(self):
        listed = [element.text for element in self.sitemap.iter(SITEMAP_NS + "loc")]
        expected = [ORIGIN + canonical_path(name) for name in self.pages if name != "404.html"]
        self.assertCountEqual(listed, expected)
        self.assertEqual(len(listed), len(set(listed)))

    def test_every_page_is_self_canonical_and_has_a_markdown_representation(self):
        for name in self.pages:
            if name == "404.html":
                continue
            with self.subTest(page=name):
                page = read_document(name)
                self.assertEqual(page.link("canonical"), ORIGIN + canonical_path(name))
                self.assertTrue((DIST / name.replace(".html", ".md")).is_file())

    def test_the_error_page_stays_out_of_search_and_returns_to_the_directory(self):
        page = read_document("404.html")
        self.assertEqual(page.meta(name="robots"), "noindex")
        self.assertEqual(page.structured_data, [])
        self.assertIn('href="/"', (DIST / "404.html").read_text(encoding="utf-8"))

    def test_every_page_declares_its_preview_and_its_publisher(self):
        for name in self.pages:
            if name == "404.html":
                continue
            with self.subTest(page=name):
                page = read_document(name)
                url = ORIGIN + canonical_path(name)
                self.assertEqual(page.meta(property="og:url"), url)
                self.assertEqual(page.meta(property="og:title"), page.title)
                # The home page keeps the site card; every other page draws its own.
                path = canonical_path(name)
                image = page.meta(property="og:image")
                if path == "/":
                    self.assertEqual(image, ORIGIN + "/og.png")
                else:
                    self.assertRegex(image, rf"^{ORIGIN}/og{path}\.png\?v=[0-9a-f]{{8}}$")
                    self.assertTrue((DIST / f"og{path}.png").is_file(), image)
                self.assertTrue(page.meta(property="og:image:alt"))
                self.assertEqual(page.meta(name="twitter:card"), "summary_large_image")
                graph = json.loads(page.structured_data[0])["@graph"]
                types = {node["@type"]: node for node in graph}
                self.assertEqual(types["Organization"]["url"], "https://steel.dev/")
                self.assertEqual(types["WebSite"]["publisher"]["@id"], types["Organization"]["@id"])

    def test_the_robots_file_allows_crawling_and_keeps_the_content_signals(self):
        robots = (DIST / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("User-agent: *\nAllow: /", robots)
        self.assertIn(f"Sitemap: {ORIGIN}/sitemap.xml", robots)
        self.assertEqual(robots.count("Content-Signal: search=yes, ai-input=yes, ai-train=yes"), 2)

    def test_record_exports_preserve_claims_sources_and_qualifications(self):
        claims = {claim["id"]: claim for claim in self.catalog["claims"]}
        sources = {source["id"]: source for source in self.catalog["sources"]}
        for approach in self.catalog["approaches"]:
            with self.subTest(approach=approach["id"]):
                record = json.loads(
                    (DIST / f"agents/{approach['id']}.json").read_text(encoding="utf-8")
                )
                self.assertEqual(record["approaches"], [approach])
                self.assertEqual(record["claims"], [claims[key] for key in approach["claim_ids"]])
                self.assertEqual(
                    record["sources"], [sources[key] for key in approach["source_ids"]]
                )
                markdown = " ".join(
                    (DIST / f"agents/{approach['id']}.md").read_text(encoding="utf-8").split()
                )
                for claim in record["claims"]:
                    self.assertIn(" ".join(str(claim["text"]).split()), markdown)
                    for field in ("metric_scope", "denominator", "measurement_method"):
                        if claim.get(field):
                            self.assertIn(" ".join(str(claim[field]).split()), markdown)
                for source in record["sources"]:
                    self.assertIn(source["url"], markdown)

    def test_the_compact_index_points_at_the_entry_pages(self):
        index = json.loads((DIST / "agents/index.json").read_text(encoding="utf-8"))["approaches"]
        self.assertCountEqual(
            [entry["id"] for entry in index],
            [approach["id"] for approach in self.catalog["approaches"]],
        )
        for entry in index:
            self.assertEqual(entry["url"], f"{ORIGIN}/agents/{entry['id']}")

    def test_the_published_catalog_matches_the_committed_data(self):
        self.assertEqual(
            (DIST / "agents.json").read_bytes(), (ROOT / "data/agents.json").read_bytes()
        )

    def test_alias_hosts_redirect_and_record_files_stay_out_of_search(self):
        # The hosting policy is authored at the repository root. Vercel reads it
        # before the build command, so no build step may write it.
        config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
        alias_hosts = {
            rule["has"][0]["value"]
            for rule in config["redirects"]
            if rule["destination"] == f"{ORIGIN}/:path*" and rule["permanent"]
        }
        self.assertEqual(alias_hosts, {"www.internal-agents.com", "internal-agents-map.vercel.app"})
        noindex = {
            rule["source"]
            for rule in config["headers"]
            if {"key": "X-Robots-Tag", "value": "noindex"} in rule["headers"]
        }
        # Raw records stay out of search; the HTML entry pages must not inherit it.
        self.assertEqual(noindex, {"/agents/:path*.json", "/agents/index.json", "/404.html"})
        immutable = next(rule for rule in config["headers"] if rule["source"] == "/_astro/:path*")
        self.assertIn("immutable", immutable["headers"][0]["value"])

    def test_the_data_build_writes_no_hosting_or_routing_configuration(self):
        records = build.load_agents()
        companies = build.load_companies(records)
        outputs = build.data_outputs(records, build.normalize(records, companies))
        for path in (ROOT / "vercel.json", ROOT / "routing-manifest.json"):
            self.assertNotIn(path, outputs)
        manifest = json.loads((ROOT / "routing-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 1)
        for path, artifacts in manifest["routes"].items():
            self.assertEqual(set(artifacts), {"html", "markdown"})
            self.assertTrue(path.startswith("/"))
            for name in artifacts.values():
                self.assertTrue((DIST / name.lstrip("/")).is_file(), name)


class WorkflowTests(unittest.TestCase):
    def test_workflow_validates_without_deploying(self):
        workflow = yaml.load(
            (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8"),
            Loader=yaml.BaseLoader,
        )
        self.assertIn("on", workflow)
        self.assertIn("github.ref", workflow["concurrency"]["group"])
        self.assertEqual(workflow["concurrency"]["cancel-in-progress"], "true")
        steps = workflow["jobs"]["validate"]["steps"]
        commands = "\n".join(step.get("run", "") for step in steps)
        self.assertIn("npm run verify", commands)
        # One public host only: GitHub Pages would duplicate every page.
        self.assertNotIn("pages", str(workflow).lower())
        for step in steps:
            if "uses" in step:
                self.assertRegex(step["uses"], r"@[0-9a-f]{40}$")

    def test_the_verify_gate_builds_the_site_before_it_reads_the_artifact(self):
        verify = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["scripts"][
            "verify"
        ]
        self.assertIn("scripts/build.py --check", verify)
        self.assertNotIn("--data-only", verify)
        artifact_checks = [
            verify.index("scripts/check_site.py --root dist"),
            verify.index("unittest discover -s tests"),
        ]
        for position in artifact_checks:
            self.assertLess(verify.index("npm run build"), position)


if __name__ == "__main__":
    unittest.main()


class ContributionTests(unittest.TestCase):
    TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "catalog-suggestion.yml"

    def test_the_contribution_link_opens_the_catalog_issue_form(self):
        metadata = (ROOT / "src" / "lib" / "metadata.ts").read_text(encoding="utf-8")
        self.assertIn(f"issues/new?template={self.TEMPLATE.name}", metadata)
        self.assertTrue(self.TEMPLATE.is_file())

    def test_the_issue_form_asks_for_what_a_catalog_entry_needs(self):
        form = yaml.safe_load(self.TEMPLATE.read_text(encoding="utf-8"))
        fields = {item["id"]: item for item in form["body"] if "id" in item}
        # A short form: the request, the company and agent, and one public link.
        self.assertEqual(list(fields), ["request", "agent", "source", "details"])
        for field in ("request", "agent", "source"):
            with self.subTest(field=field):
                self.assertTrue(fields[field]["validations"]["required"])
        self.assertEqual(
            fields["request"]["attributes"]["options"],
            ["Add a new agent", "Fix an existing entry"],
        )
        self.assertIn("public", fields["source"]["attributes"]["description"])
        self.assertFalse(fields["details"].get("validations", {}).get("required", False))
