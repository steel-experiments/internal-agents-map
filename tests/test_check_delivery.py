# ABOUTME: Tests the pure route, header, and body rules of the deployed delivery checker.
# ABOUTME: Every case uses a constructed response object, so no test reaches the network.
"""Route derivation, manifest parsing, and header assertions of check_delivery.py."""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


delivery = load_script("check_delivery")

MANIFEST = {
    "schema_version": 1,
    "routes": {
        "/": {"html": "/index.html", "markdown": "/index.md"},
        "/lessons": {"html": "/lessons.html", "markdown": "/lessons.md"},
        "/agents/first-agent": {
            "html": "/agents/first-agent.html",
            "markdown": "/agents/first-agent.md",
        },
        "/agents/second-agent": {
            "html": "/agents/second-agent.html",
            "markdown": "/agents/second-agent.md",
        },
    },
}
PREVIEW_ORIGIN = "https://map-preview.vercel.app"
PAGE_HEADERS = {
    "content-type": "text/html; charset=utf-8",
    "vary": "Accept",
    "link": '<https://internal-agents.com/index.md>; rel="alternate"; type="text/markdown"',
    "cache-control": "public, max-age=0, must-revalidate",
}


def response(status=200, headers=None, body=b""):
    return delivery.Response(status, dict(headers or {}), body)


class ManifestTests(unittest.TestCase):
    def write(self, manifest):
        path = Path(self.folder.name) / "routing-manifest.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return path

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)

    def test_reads_the_route_map(self):
        routes = delivery.load_routes(self.write(MANIFEST))
        self.assertEqual(routes["/"]["markdown"], "/index.md")

    def test_refuses_another_schema_version(self):
        with self.assertRaises(ValueError):
            delivery.load_routes(self.write({**MANIFEST, "schema_version": 2}))

    def test_refuses_a_route_without_both_artifacts(self):
        with self.assertRaises(ValueError):
            delivery.load_routes(
                self.write({"schema_version": 1, "routes": {"/": {"html": "/index.html"}}})
            )

    def test_refuses_an_artifact_outside_the_root(self):
        broken = {"schema_version": 1, "routes": {"/": {"html": "x.html", "markdown": "/x.md"}}}
        with self.assertRaises(ValueError):
            delivery.load_routes(self.write(broken))

    def test_refuses_an_empty_manifest(self):
        with self.assertRaises(ValueError):
            delivery.load_routes(self.write({"schema_version": 1, "routes": {}}))


class RouteTests(unittest.TestCase):
    def test_lists_the_entry_routes_in_order(self):
        self.assertEqual(
            delivery.entry_routes(MANIFEST["routes"]),
            ["/agents/first-agent", "/agents/second-agent"],
        )

    def test_the_home_page_has_one_legacy_path(self):
        self.assertEqual(delivery.legacy_paths("/"), ["/index.html"])

    def test_a_page_answers_its_extension_and_its_trailing_slash(self):
        self.assertEqual(
            delivery.legacy_paths("/agents/first-agent"),
            ["/agents/first-agent.html", "/agents/first-agent/"],
        )

    def test_names_the_media_type_of_every_published_extension(self):
        self.assertEqual(delivery.mime_for("agents.json"), "application/json")
        self.assertEqual(delivery.mime_for("index.md"), "text/markdown")
        self.assertEqual(delivery.mime_for("sitemap.xml"), "application/xml")
        self.assertEqual(delivery.mime_for("robots.txt"), "text/plain")
        self.assertEqual(delivery.mime_for("logos/fixture.svg"), "image/svg+xml")
        self.assertEqual(delivery.mime_for("logos/fixture.png"), "image/png")

    def test_every_route_is_asked_for_html_markdown_and_its_export(self):
        cases = delivery.route_cases(MANIFEST["routes"])
        self.assertEqual(len(cases), 3 * len(MANIFEST["routes"]))
        html = next(case for case in cases if case.path == "/" and case.accept == "text/html")
        self.assertEqual((html.artifact, html.mime), ("index.html", "text/html"))
        self.assertTrue(html.negotiated and html.alternate_link)
        self.assertIs(html.noindex, False)
        markdown = next(
            case for case in cases if case.path == "/" and case.accept == "text/markdown"
        )
        self.assertEqual((markdown.artifact, markdown.mime), ("index.md", "text/markdown"))
        self.assertTrue(markdown.canonical_link)
        direct = next(case for case in cases if case.path == "/index.md")
        self.assertEqual(direct.artifact, "index.md")

    def test_record_json_stays_out_of_search_and_the_catalog_stays_in(self):
        cases = {case.path: case for case in delivery.export_cases(MANIFEST["routes"])}
        self.assertIs(cases["/agents/first-agent.json"].noindex, True)
        self.assertEqual(cases["/agents/first-agent.json"].artifact, "agents/first-agent.json")
        self.assertIs(cases["/agents/index.json"].noindex, True)
        self.assertIsNone(cases["/agents.json"].noindex)
        self.assertEqual(cases["/sitemap.xml"].mime, "application/xml")

    def test_every_legacy_path_redirects_once_to_its_route(self):
        cases = delivery.redirect_cases(MANIFEST["routes"])
        by_path = {case.path: case for case in cases}
        self.assertEqual(by_path["/index.html"].location, "/")
        self.assertEqual(by_path["/lessons/"].location, "/lessons")
        self.assertEqual(by_path["/agents/first-agent.html"].location, "/agents/first-agent")
        for case in cases:
            self.assertEqual(case.status, 308)

    def test_alias_hosts_send_the_visitor_to_the_canonical_origin(self):
        cases = delivery.alias_cases(MANIFEST["routes"])
        self.assertEqual({case.host for case in cases}, set(delivery.ALIAS_HOSTS))
        for case in cases:
            self.assertEqual(case.location, delivery.CANONICAL_ORIGIN + case.path)
            self.assertEqual(case.status, 308)

    def test_a_missing_document_is_a_real_404(self):
        cases = delivery.error_cases()
        entry = next(case for case in cases if case.path == "/agents/does-not-exist")
        self.assertEqual((entry.status, entry.artifact), (404, "404.html"))
        legacy = next(case for case in cases if case.path == "/missing/nested/page.html")
        self.assertEqual((legacy.status, legacy.location), (308, "/missing/nested/page"))

    def test_the_warming_list_alternates_both_representations(self):
        cases = delivery.warm_cases(MANIFEST["routes"])
        self.assertEqual([case.accept for case in cases[:4]], ["text/html", "text/markdown"] * 2)
        self.assertEqual(cases[0].artifact, "index.html")
        self.assertEqual(cases[1].artifact, "index.md")

    def test_alias_cases_are_left_out_of_a_preview_run(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "_astro").mkdir()
            preview = delivery.build_cases(MANIFEST["routes"], root, True)
            production = delivery.build_cases(MANIFEST["routes"], root, False)
        self.assertFalse([case for case in preview if case.host])
        self.assertTrue([case for case in production if case.host])

    def test_a_bundled_asset_keeps_its_own_cache_policy(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "_astro").mkdir()
            (root / "_astro/site.abcd1234.css").write_text("body{}", encoding="utf-8")
            cases = delivery.asset_cases(root)
        self.assertEqual([case.path for case in cases], ["/_astro/site.abcd1234.css"])
        self.assertTrue(cases[0].immutable)

    def test_a_published_logo_answers_with_its_image_type(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            cases = delivery.logo_cases(root)
            self.assertEqual(cases, [])
            (root / "logos").mkdir()
            (root / "logos/fixture.svg").write_text("<svg/>", encoding="utf-8")
            (root / "logos/fixture.png").write_bytes(b"\x89PNG\r\n\x1a\n")
            cases = delivery.logo_cases(root)
        self.assertEqual(
            [case.path for case in cases], ["/logos/fixture.png", "/logos/fixture.svg"]
        )
        self.assertEqual([case.mime for case in cases], ["image/png", "image/svg+xml"])
        for case in cases:
            self.assertEqual(case.artifact, "logos/" + case.path.rsplit("/", 1)[-1])
            self.assertFalse(case.immutable)


class HeaderTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        (self.root / "index.html").write_bytes(b"<html></html>")

    def test_reads_the_last_header_block_of_a_chain(self):
        dump = "HTTP/2 308\r\nlocation: /\r\n\r\nHTTP/2 200\r\nContent-Type: text/html\r\n\r\n"
        status, headers = delivery.parse_headers(dump)
        self.assertEqual(status, 200)
        self.assertEqual(headers["content-type"], "text/html")

    def test_refuses_an_empty_header_dump(self):
        with self.assertRaises(ValueError):
            delivery.parse_headers("   ")

    def case(self, **fields):
        return delivery.Case(path="/", accept="text/html", **fields)

    def test_a_correct_page_response_raises_nothing(self):
        case = self.case(
            artifact="index.html",
            mime="text/html",
            negotiated=True,
            alternate_link=True,
            noindex=False,
        )
        answer = response(200, PAGE_HEADERS, b"<html></html>")
        self.assertEqual(delivery.check_response(case, answer, self.root), [])

    def test_a_wrong_status_stops_the_other_checks(self):
        case = self.case(artifact="index.html", mime="text/html")
        problems = delivery.check_response(case, response(500, {}, b""), self.root)
        self.assertEqual(problems, ["HTTP 500, wanted 200"])

    def test_a_body_that_differs_from_the_build_is_named(self):
        case = self.case(artifact="index.html", mime="text/html")
        answer = response(200, PAGE_HEADERS, b"<html>other</html>")
        self.assertIn(
            "Body differs from index.html", delivery.check_response(case, answer, self.root)
        )

    def test_a_missing_vary_and_link_header_are_named(self):
        case = self.case(negotiated=True, alternate_link=True, canonical_link=True)
        answer = response(200, {"cache-control": "must-revalidate"})
        problems = delivery.check_response(case, answer, self.root)
        self.assertIn("Missing Vary: Accept", problems)
        self.assertIn("Missing alternate Link header", problems)
        self.assertIn("Missing canonical Link header", problems)

    def test_an_html_page_must_not_carry_the_record_noindex_rule(self):
        case = self.case(noindex=False)
        answer = response(200, {**PAGE_HEADERS, "x-robots-tag": "noindex"})
        self.assertIn(
            "Unwanted X-Robots-Tag: noindex", delivery.check_response(case, answer, self.root)
        )

    def test_a_record_export_must_carry_it(self):
        case = delivery.Case(path="/agents/first-agent.json", noindex=True)
        answer = response(200, {"cache-control": "must-revalidate"})
        self.assertIn(
            "Missing X-Robots-Tag: noindex", delivery.check_response(case, answer, self.root)
        )

    def test_a_redirect_must_reach_the_canonical_path(self):
        case = delivery.Case(path="/index.html", status=308, location="/")
        wrong = response(308, {"location": "/somewhere-else"})
        self.assertIn("Location", delivery.check_response(case, wrong, self.root)[0])
        for value in ("/", delivery.CANONICAL_ORIGIN + "/"):
            self.assertEqual(
                delivery.check_response(case, response(308, {"location": value}), self.root), []
            )

    def test_a_redirect_may_stay_on_the_origin_that_was_asked(self):
        case = delivery.Case(path="/index.html", status=308, location="/")
        for value in ("/", PREVIEW_ORIGIN + "/"):
            self.assertEqual(
                delivery.check_response(
                    case, response(308, {"location": value}), self.root, PREVIEW_ORIGIN
                ),
                [],
            )

    def test_a_redirect_to_another_origin_is_named(self):
        case = delivery.Case(path="/index.html", status=308, location="/")
        answer = response(308, {"location": "https://somewhere-else.example/"})
        problems = delivery.check_response(case, answer, self.root, PREVIEW_ORIGIN)
        self.assertIn("Location", problems[0])

    def test_an_alias_host_must_reach_the_production_origin(self):
        case = delivery.Case(
            path="/",
            status=308,
            location=delivery.CANONICAL_ORIGIN + "/",
            host="www.internal-agents.com",
        )
        good = response(308, {"location": delivery.CANONICAL_ORIGIN + "/"})
        self.assertEqual(delivery.check_response(case, good, self.root, PREVIEW_ORIGIN), [])
        preview = response(308, {"location": PREVIEW_ORIGIN + "/"})
        problems = delivery.check_response(case, preview, self.root, PREVIEW_ORIGIN)
        self.assertIn("Location", problems[0])

    def test_a_page_must_revalidate_and_an_asset_must_not(self):
        page = self.case()
        self.assertIn(
            "does not revalidate",
            " ".join(delivery.check_response(page, response(200, {}), self.root)),
        )
        asset = delivery.Case(path="/_astro/site.abcd1234.css", immutable=True)
        answer = response(200, {"cache-control": "public, max-age=0, must-revalidate"})
        self.assertIn(
            "is not an immutable asset policy",
            " ".join(delivery.check_response(asset, answer, self.root)),
        )

    def test_an_asset_must_never_be_served_as_markdown(self):
        asset = delivery.Case(path="/_astro/site.abcd1234.css", immutable=True)
        answer = response(
            200,
            {
                "cache-control": "public, max-age=31536000, immutable",
                "content-type": "text/markdown; charset=utf-8",
            },
        )
        self.assertIn(
            "A bundled asset must not be served as Markdown",
            delivery.check_response(asset, answer, self.root),
        )

    def test_a_head_response_carries_no_body(self):
        case = delivery.Case(path="/", method="HEAD", mime="text/html")
        answer = response(200, PAGE_HEADERS, b"<html></html>")
        self.assertIn("HEAD returned a body", delivery.check_response(case, answer, self.root))


class PayloadTests(unittest.TestCase):
    """curl repeats the header block in the payload file of a --head request."""

    DUMP = b"HTTP/2 200\r\ncontent-type: text/html\r\ncontent-length: 18\r\n\r\n"

    def test_a_head_payload_that_repeats_the_headers_is_no_body(self):
        self.assertEqual(delivery.head_body(self.DUMP, self.DUMP), b"")

    def test_a_head_payload_after_the_headers_is_a_body(self):
        self.assertEqual(delivery.head_body(self.DUMP, self.DUMP + b"oops"), b"oops")

    def test_a_payload_without_the_header_block_stays_whole(self):
        self.assertEqual(delivery.head_body(self.DUMP, b"oops"), b"oops")

    def test_reads_the_origin_of_a_deployment_address(self):
        self.assertEqual(
            delivery.origin_of("https://internal-agents.com/"), delivery.CANONICAL_ORIGIN
        )
        self.assertEqual(delivery.origin_of("map-preview.vercel.app"), PREVIEW_ORIGIN)


if __name__ == "__main__":
    unittest.main()
