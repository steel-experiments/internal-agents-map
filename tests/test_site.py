# ABOUTME: Artifact contracts of the built site in dist/, read with the publication checker.
# ABOUTME: Covers evidence coverage, escaping, qualifications, source links, and guide links.
"""Behavioral contracts of the built site artifact. Run 'npm run build' first."""

import importlib.util
import json
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = load_script("check_site")


def read_page(name):
    page = checker.SiteParser()
    page.feed((DIST / name).read_text(encoding="utf-8"))
    return page


class ArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (DIST / "index.html").is_file():
            raise AssertionError(f"{DIST} holds no build. Run 'npm run build' first.")
        cls.catalog = json.loads((ROOT / "data/agents.json").read_text(encoding="utf-8"))
        cls.claims = {claim["id"]: claim for claim in cls.catalog["claims"]}
        cls.sources = {source["id"]: source for source in cls.catalog["sources"]}
        cls.entries = {
            approach["id"]: read_page(f"agents/{approach['id']}.html")
            for approach in cls.catalog["approaches"]
        }

    def test_the_built_artifact_passes_every_publication_rule(self):
        self.assertEqual(checker.validate(DIST), [])

    def test_company_pages_contain_only_their_records(self):
        for company_id in {a["company_id"] for a in self.catalog["approaches"]}:
            page = read_page(f"organizations/{company_id}.html")
            expected = Counter(
                a["id"] for a in self.catalog["approaches"] if a["company_id"] == company_id
            )
            self.assertEqual(Counter(page.coverage["approach"]), expected)

    def test_every_claim_and_source_reaches_its_own_entry_page(self):
        for kind, field in (("claim", "claim_ids"), ("source", "source_ids")):
            published = Counter(
                identifier for page in self.entries.values() for identifier in page.coverage[kind]
            )
            expected = Counter(
                identifier
                for approach in self.catalog["approaches"]
                for identifier in approach[field]
            )
            self.assertEqual(published, expected)
        for approach in self.catalog["approaches"]:
            text = checker.visible_text(self.entries[approach["id"]])
            for claim_id in approach["claim_ids"]:
                claim = self.claims[claim_id]
                self.assertIn(" ".join(str(claim["text"]).split()), text, claim_id)

    def test_the_directory_holds_one_card_and_a_crawlable_link_per_entry(self):
        directory = read_page("index.html")
        self.assertEqual(
            Counter(directory.coverage["approach"]),
            Counter(approach["id"] for approach in self.catalog["approaches"]),
        )
        linked = {url.split("#")[0] for url in directory.urls if url.startswith("/agents/")}
        for approach in self.catalog["approaches"]:
            self.assertIn(f"/agents/{approach['id']}", linked)

    def test_contradicting_and_contextualizing_evidence_keeps_its_role(self):
        pages = {
            identifier: (DIST / f"agents/{identifier}.html").read_text(encoding="utf-8")
            for identifier in self.entries
        }
        for relation in ("contradicts", "contextualizes"):
            wanted = {
                claim["approach_id"]
                for claim in self.catalog["claims"]
                if any(link["relation"] == relation for link in claim["evidence"])
            }
            self.assertTrue(wanted, relation)
            for identifier in wanted:
                self.assertIn(f"relation-{relation}", pages[identifier])

    def test_the_uber_volume_conflict_stays_beside_its_metric(self):
        conflicting = [
            claim
            for claim in self.catalog["claims"]
            if claim["approach_id"] == "uber-ureview"
            and any(link["relation"] == "contradicts" for link in claim["evidence"])
        ]
        self.assertTrue(conflicting)
        text = checker.visible_text(self.entries["uber-ureview"])
        for claim in conflicting:
            self.assertEqual(claim["confidence"], "low")
            self.assertIn(" ".join(str(claim["text"]).split()), text)
            for field in checker.QUALIFIER_FIELDS:
                if claim.get(field):
                    self.assertIn(" ".join(str(claim[field]).split()), text)

    def test_catalog_prose_reaches_the_page_as_text(self):
        # These claims hold characters that would open a tag or an attribute if
        # they were written to the page unescaped.
        for claim_id in (
            "doordash-flux--architecture-sandbox",
            "cloudflare-ai-stack--key-metrics-0",
        ):
            claim = self.claims[claim_id]
            self.assertRegex(str(claim["text"]), r"[<>&\"]")
            text = checker.visible_text(self.entries[claim["approach_id"]])
            self.assertIn(" ".join(str(claim["text"]).split()), text)

    def test_source_links_keep_the_original_and_the_preserved_copy_apart(self):
        blob = "https://github.com/steel-experiments/internal-agents-map/blob/main/"
        for approach in self.catalog["approaches"]:
            page = (DIST / f"agents/{approach['id']}.html").read_text(encoding="utf-8")
            for source_id in approach["source_ids"]:
                source = self.sources[source_id]
                self.assertIn(f'href="{source["url"]}"', page, source_id)
                capture = source.get("capture")
                if capture:
                    preserved = blob + capture["artifacts"]["markdown"]["path"]
                    self.assertIn(preserved, page, source_id)
                    self.assertNotEqual(preserved, source["url"])
                else:
                    self.assertNotIn("Preserved copy", page, source_id)

    def test_the_guides_send_the_reader_to_the_entry_pages(self):
        definitions = (DIST / "definitions.html").read_text(encoding="utf-8")
        self.assertEqual(definitions.count("data-chart-reference="), 3)
        chart = definitions.split('class="quadrant-plot"', 1)[1].split("</figure>", 1)[0]
        notes = definitions.split('class="placement-notes"', 1)[1].split("</details>", 1)[0]
        # Each marker links to its note, and the note links to the entry page.
        placed = {
            fragment.split('"', 1)[0] for fragment in chart.split('data-chart-approach-id="')[1:]
        }
        self.assertTrue(placed)
        known = {a["id"] for a in self.catalog["approaches"]}
        self.assertEqual(placed - known, set())
        for approach_id in placed:
            self.assertIn(f'href="#placement-{approach_id}"', chart)
            self.assertIn(f'id="placement-{approach_id}"', notes)
            self.assertIn(f'href="/agents/{approach_id}"', notes)


if __name__ == "__main__":
    unittest.main()
