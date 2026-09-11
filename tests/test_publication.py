"""Contracts for agent discovery, evidence exports, and deploy-safe asset caching."""

import hashlib
import html
import importlib.util
import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("publication_build", ROOT / "scripts/build.py")
build = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build)


class PublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs = build.rendered_outputs(build.load_agents())
        cls.site = ROOT / "site"
        cls.catalog = json.loads(cls.outputs[cls.site / "agents.json"])

    def test_sitemap_and_canonicals_cover_pages_except_404(self):
        urls = [
            e.text
            for e in ET.fromstring(self.outputs[self.site / "sitemap.xml"]).iter()
            if e.tag.endswith("}loc")
        ]
        pages = [p for p in self.outputs if p.is_relative_to(self.site) and p.suffix == ".html"]
        expected = []
        for path in pages:
            soup = BeautifulSoup(self.outputs[path], "html.parser")
            if path.name == "404.html":
                self.assertEqual(soup.find("meta", attrs={"name": "robots"})["content"], "noindex")
                self.assertIn('href="/index.html#catalog"', self.outputs[path])
                continue
            canonical = build.canonical_url(path.relative_to(self.site).as_posix())
            expected.append(canonical)
            self.assertEqual(soup.find("link", rel="canonical")["href"], canonical)
            self.assertIn(path.with_suffix(".md"), self.outputs)
        self.assertCountEqual(urls, expected)
        robots = self.outputs[self.site / "robots.txt"]
        self.assertIn("User-agent: *\nAllow: /", robots)
        self.assertIn("Sitemap: https://internal-agents.com/sitemap.xml", robots)
        self.assertEqual(robots.count("Content-Signal: search=yes, ai-input=yes, ai-train=yes"), 2)

    def test_pages_declare_publisher_previews_and_change_dates(self):
        sitemap = {
            u.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text: u.find(
                "{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod"
            )
            for u in ET.fromstring(self.outputs[self.site / "sitemap.xml"])
        }
        latest_review = max(a["last_reviewed_at"] for a in self.catalog["approaches"])
        for path, content in self.outputs.items():
            if not (path.is_relative_to(self.site) and path.suffix == ".html"):
                continue
            name = path.relative_to(self.site).as_posix()
            soup = BeautifulSoup(content, "html.parser")
            if name == "404.html":
                self.assertIsNone(soup.find("script", type="application/ld+json"))
                continue
            url = build.canonical_url(name)
            graph = json.loads(soup.find("script", type="application/ld+json").string)["@graph"]
            types = {node["@type"]: node for node in graph}
            self.assertEqual(types["Organization"]["url"], "https://steel.dev/")
            self.assertEqual(types["WebSite"]["publisher"]["@id"], types["Organization"]["@id"])
            self.assertEqual(soup.find("meta", property="og:url")["content"], url)
            self.assertEqual(soup.find("meta", property="og:title")["content"], soup.title.string)
            self.assertEqual(
                soup.find("meta", attrs={"name": "twitter:card"})["content"], "summary"
            )
            lastmod = sitemap[url]
            if name.startswith("notes/"):
                published = soup.select_one(".note-meta time")["datetime"]
                self.assertEqual(types["Article"]["datePublished"], published)
                self.assertEqual(types["Article"]["publisher"]["@id"], types["Organization"]["@id"])
                self.assertEqual(soup.find("meta", property="og:type")["content"], "article")
                self.assertEqual(lastmod.text, published)
            elif name == "index.html":
                self.assertEqual(types["Dataset"]["dateModified"], latest_review)
                self.assertIn(
                    build.ORIGIN + "/agents.json",
                    [d["contentUrl"] for d in types["Dataset"]["distribution"]],
                )
                self.assertEqual(lastmod.text, latest_review)
            elif name == "methodology.html":
                self.assertIsNone(lastmod)
                self.assertIsNotNone(soup.select_one('main a[href="https://steel.dev/"]'))
            self.assertIn("Compiled by", soup.footer.get_text())
            self.assertIsNotNone(soup.footer.select_one('a[href^="https://steel.dev/"]'))

    def test_individual_records_preserve_claims_sources_and_qualifications(self):
        index = json.loads(self.outputs[self.site / "agents/index.json"])["approaches"]
        self.assertCountEqual(
            [a["id"] for a in index], [a["id"] for a in self.catalog["approaches"]]
        )
        for approach in self.catalog["approaches"]:
            record = json.loads(self.outputs[self.site / f"agents/{approach['id']}.json"])
            self.assertEqual(record["approaches"], [approach])
            self.assertEqual(
                record["claims"],
                [c for c in self.catalog["claims"] if c["id"] in approach["claim_ids"]],
            )
            self.assertEqual(
                record["sources"],
                [s for s in self.catalog["sources"] if s["id"] in approach["source_ids"]],
            )
            md = self.outputs[self.site / f"agents/{approach['id']}.md"]
            for claim in record["claims"]:
                rendered_text = markdownify(html.escape(str(claim["text"])))
                self.assertIn(" ".join(rendered_text.split()), " ".join(md.split()))
            for source in record["sources"]:
                self.assertIn(source["url"], md)

    def test_markdown_keeps_reading_content_links_and_diagram_descriptions(self):
        doc = '<main><h1>Title</h1><p>A <strong>qualified</strong> claim.</p><details><summary>Evidence</summary><p>Contradicts <a href="../index.html#claim">source</a></p></details><svg aria-label="Local and cloud execution"></svg><form>Search controls</form><p hidden>Hidden UI</p></main>'
        md = build.page_markdown(doc, build.ORIGIN + "/notes/test.html")
        for value in (
            "# Title",
            "**qualified**",
            "Contradicts",
            "https://internal-agents.com/index.html#claim",
            "Local and cloud execution",
        ):
            self.assertIn(value, md)
        self.assertNotIn("Search controls", md)
        self.assertNotIn("Hidden UI", md)

    def test_served_assets_have_matching_hashes_and_immutable_headers(self):
        manifest = json.loads(self.outputs[self.site / "assets/manifest.json"])
        config = json.loads(self.outputs[ROOT / "vercel.json"])
        for original, hashed in manifest.items():
            data = self.outputs[self.site / "assets" / hashed]
            digest = hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()[
                :16
            ]
            self.assertIn(digest, hashed)
            rule = next(r for r in config["headers"] if r["source"] == "/assets/" + hashed)
            self.assertIn("immutable", rule["headers"][0]["value"])
            self.assertNotIn('"/assets/' + original + '"', json.dumps(config))
        self.assertIn(
            manifest["fonts/Geist.woff2"], self.outputs[self.site / "assets" / manifest["site.css"]]
        )
        for path, content in self.outputs.items():
            if path.is_relative_to(self.site) and path.suffix == ".html":
                self.assertIn("assets/" + manifest["site.css"], content)
                self.assertNotIn('href="assets/site.css"', content)
