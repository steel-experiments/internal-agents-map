from __future__ import annotations

import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import shutil
import struct
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

import yaml

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "src" / "content" / "lessons"
SPEC = importlib.util.spec_from_file_location("catalog_build", ROOT / "scripts" / "build.py")
build = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(build)
PAGE_SCHEMA = build.AGENT_SCHEMA["definitions"]["pageContent"]["properties"]
# The agent schema checks the shape of a source; validate_source checks its capture.
SOURCE_VALIDATOR = build.Draft7Validator(
    {
        **build.AGENT_SCHEMA["definitions"]["source"],
        "definitions": build.AGENT_SCHEMA["definitions"],
    },
    format_checker=build.FORMAT_CHECKER,
)


class BuildTests(unittest.TestCase):
    def test_environment_count_excludes_undocumented_legacy_values(self) -> None:
        values = [
            None,
            "",
            "  ",
            "unknown",
            "UNKNOWN",
            "Not specified in source",
            "NOT DETAILED",
            "n/a - platform",
            "not applicable",
            "AWS EC2 devbox",
            "Docker container",
        ]
        records = [
            {
                "approach_type": "agent",
                "autonomy": "unknown",
                "operating_models": [{"attention_boundary": "unknown"}],
                "rubric": {"state": "unknown"},
                "architecture": {"sandbox": value},
            }
            for value in values
        ]
        self.assertIn(
            "- 2 entries document a concrete execution environment.",
            build.render_patterns_snapshot(records),
        )

    def test_capture_paths_reject_symlink_boundaries(self) -> None:
        for mode in (
            "content-sibling",
            "manifest-sibling",
            "content-external",
            "manifest-external",
            "source-sibling",
            "source-external",
            "archive-external",
        ):
            with (
                self.subTest(mode=mode),
                tempfile.TemporaryDirectory() as directory,
                tempfile.TemporaryDirectory() as outside,
            ):
                root = Path(directory)
                bundle = root / "archive" / "sources" / "fixture"
                bundle.mkdir(parents=True)
                sibling = bundle.parent / "sibling"
                sibling.mkdir()
                destination = Path(outside) if "external" in mode else sibling
                name = "metadata.json" if mode.startswith("manifest") else "content.md"
                if mode.startswith("source"):
                    bundle.rmdir()
                    bundle.symlink_to(destination, target_is_directory=True)
                elif mode.startswith("archive"):
                    shutil.rmtree(root / "archive")
                    (root / "archive").symlink_to(destination, target_is_directory=True)
                else:
                    (bundle / name).symlink_to(destination / name)
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    build.resolve_capture_path(
                        f"archive/sources/fixture/{name}",
                        "fixture",
                        name,
                        "capture",
                        "fixture.yaml",
                        root=root,
                    )

    @classmethod
    def setUpClass(cls) -> None:
        cls.records = build.load_agents()
        cls.companies = build.load_companies(cls.records)

    def company_fixture(self, **overrides) -> dict:
        company = {
            "id": "fixture-company",
            "name": "Fixture",
            "homepage": "https://www.fixture.example/",
            "logo": "none",
            "logo_note": "No logo asset has been collected yet.",
        }
        company.update(overrides)
        if isinstance(company.get("logo"), dict):
            company.pop("logo_note", None)
        return company

    def fixture_records(self) -> list[dict]:
        return [{"id": "fixture-agent", "company": "Fixture"}]

    def write_registry(self, root: Path, companies: list[dict]) -> None:
        (root / "data").mkdir(parents=True, exist_ok=True)
        (root / "data" / "companies.yaml").write_text(
            yaml.safe_dump(companies, sort_keys=False), encoding="utf-8"
        )

    def write_logo(self, root: Path, name: str, content: bytes) -> None:
        logos = root / "public" / "logos"
        logos.mkdir(parents=True, exist_ok=True)
        (logos / name).write_bytes(content)

    def assert_registry_invalid(self, records: list[dict], root: Path) -> None:
        with (
            contextlib.redirect_stderr(io.StringIO()),
            self.assertRaises(SystemExit),
        ):
            build.load_companies(records, root=root)

    def logo_svg(self, **overrides) -> bytes:
        attributes = {
            "xmlns": "http://www.w3.org/2000/svg",
            "viewBox": "0 0 128 40",
            **overrides,
        }
        markup = " ".join(f'{key}="{value}"' for key, value in attributes.items())
        return f'<svg {markup}><path d="M0 0h128v40H0z"/></svg>'.encode("utf-8")

    def logo_png(self, width: int = 128, height: int = 40) -> bytes:
        return b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\x0dIHDR" + struct.pack(">II", width, height)

    def source_fixture(self) -> dict:
        return {
            "id": "fixture-source",
            "title": "Fixture source",
            "url": "https://example.com/article",
            "canonical_url": "https://example.com/article",
            "kind": "engineering-blog",
            "provenance_class": "first-party",
            "role": "evidence",
            "accessed_at": "2026-08-31",
            "last_verified_at": "2026-08-31",
        }

    def write_capture(
        self,
        root: Path,
        *,
        source: dict | None = None,
        markdown: bytes = b"# Preserved source\n\nEvidence.\n",
        pdf: bytes | None = None,
        archived_url: str | None = None,
    ) -> tuple[dict, dict, Path]:
        source = copy.deepcopy(source or self.source_fixture())
        source_id = source["id"]
        bundle = root / "archive" / "sources" / source_id
        bundle.mkdir(parents=True)
        markdown_path = bundle / "content.md"
        markdown_path.write_bytes(markdown)
        relative_bundle = f"archive/sources/{source_id}"
        artifacts = {
            "markdown": {
                "path": f"{relative_bundle}/content.md",
                "sha256": f"sha256:{hashlib.sha256(markdown).hexdigest()}",
                "bytes": len(markdown),
            }
        }
        if pdf is not None:
            (bundle / "page.pdf").write_bytes(pdf)
            artifacts["pdf"] = {
                "path": f"{relative_bundle}/page.pdf",
                "sha256": f"sha256:{hashlib.sha256(pdf).hexdigest()}",
                "bytes": len(pdf),
            }
        manifest = {
            "schema_version": 1,
            "source_id": source_id,
            "original_url": source["url"],
            "final_url": source["canonical_url"],
            "captured_at": "2026-08-31T12:34:56Z",
            "http_status": 200,
            "tool": {"name": "steel", "version": "0.4.4"},
            "artifacts": artifacts,
        }
        if archived_url is not None:
            source["archived_url"] = archived_url
            manifest["external_archive_url"] = archived_url
        manifest_path = bundle / "metadata.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        source["capture"] = {"manifest_path": f"{relative_bundle}/metadata.json"}
        return source, manifest, manifest_path

    def assert_source_invalid(self, source: dict, root: Path) -> None:
        if not SOURCE_VALIDATOR.is_valid(source):
            return
        with (
            mock.patch.object(build, "ROOT", root),
            contextlib.redirect_stderr(io.StringIO()),
            self.assertRaises(SystemExit),
        ):
            build.validate_source(source, "fixture.yaml", set())

    def rewrite_manifest(self, path: Path, manifest: dict) -> None:
        path.write_text(json.dumps(manifest), encoding="utf-8")

    def test_catalog_has_unique_ids(self) -> None:
        approach_ids = [record["id"] for record in self.records]
        source_ids = [source["id"] for record in self.records for source in record["sources"]]
        self.assertEqual(len(approach_ids), len(set(approach_ids)))
        self.assertEqual(len(source_ids), len(set(source_ids)))

    def test_normalized_export_has_linked_collections(self) -> None:
        export = build.normalize(self.records, self.companies)
        self.assertEqual(export["schema_version"], 7)
        claim_ids = {claim["id"] for claim in export["claims"]}
        source_ids = {source["id"] for source in export["sources"]}
        company_ids = {company["id"] for company in export["companies"]}
        self.assertTrue(
            all(source["role"] in build.schema_values("sourceRole") for source in export["sources"])
        )
        for approach in export["approaches"]:
            self.assertIn(approach["company_id"], company_ids)
            self.assertTrue(set(approach["claim_ids"]).issubset(claim_ids))
            self.assertTrue(set(approach["source_ids"]).issubset(source_ids))
            self.assertTrue(approach["operating_models"])
            for item in approach["operating_models"]:
                expected = build.BOUNDARY_LEVELS[item["attention_boundary"]]
                self.assertEqual(item["level"], expected)
        for claim in export["claims"]:
            self.assertTrue(claim["evidence"])
            self.assertIn(claim["confidence"], build.schema_values("confidence"))
            self.assertTrue({item["source_id"] for item in claim["evidence"]}.issubset(source_ids))
            if claim["field"].startswith("operating_models."):
                self.assertEqual(claim["kind"], "inference")
                self.assertEqual(claim["provenance"], "catalog-judgment")
                self.assertTrue(claim["valid_at"])

    def test_page_content_pilot_is_complete_and_preserves_primitive_names(self) -> None:
        pilot = [record for record in self.records if record.get("page_content")]
        self.assertEqual(len(pilot), len(self.records))
        catalog = build.normalize(self.records, self.companies)
        claims = {
            claim["field"]: claim
            for claim in catalog["claims"]
            if claim["approach_id"] == "github-qubot"
        }
        self.assertEqual(claims["primitives.0"]["id"], "github-qubot--primitives-0")
        self.assertEqual(claims["primitives.0"]["display_name"], "Start a Qubot run")
        for record in pilot:
            page = record["page_content"]
            self.assertEqual(set(page["questions"]), set(PAGE_SCHEMA["questions"]["required"]))
            self.assertEqual(
                set(page["implementation_fields"]),
                set(PAGE_SCHEMA["implementation_fields"]["required"]),
            )
            self.assertNotIn(
                "not-reviewed",
                [value["state"] for value in page["questions"].values()]
                + [value["state"] for value in page["implementation_fields"].values()],
            )

    def test_page_content_rejects_unsupported_reported_and_duplicate_chains(self) -> None:
        record = copy.deepcopy(
            next(item for item in self.records if item["id"] == "notion-custom-agents")
        )
        sources = {source["id"] for source in record["sources"]}
        for link in record["evidence"]["summary"]:
            link["relation"] = "contextualizes"
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            build.validate_page_content(record, "fixture.yaml", sources)

        record = copy.deepcopy(
            next(item for item in self.records if item["id"] == "notion-custom-agents")
        )
        record["page_content"]["observations"]["headline_metric"] = {
            "duplicate_of": "key_metrics.0",
            "reason": "Fixture cycle.",
        }
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            build.validate_page_content(record, "fixture.yaml", sources)

    def test_page_content_accepts_all_four_review_states(self) -> None:
        record = copy.deepcopy(next(item for item in self.records if item["id"] == "github-qubot"))
        questions = record["page_content"]["questions"]
        questions["human_involvement"] = {
            "state": "not-applicable",
            "claim_paths": [],
            "note": "Fixture scope has no human step.",
        }
        questions["lessons"] = {
            "state": "not-reviewed",
            "claim_paths": [],
            "note": "Review the next capture.",
        }
        build.validate_page_content(
            record, "fixture.yaml", {source["id"] for source in record["sources"]}
        )

    def test_a_note_is_optional_for_unreported_and_required_for_every_other_state(self) -> None:
        path = build.AGENTS_DIR / "github-qubot.yaml"

        def record_with(slot: str, key: str, state: str) -> dict:
            record = copy.deepcopy(
                next(item for item in self.records if item["id"] == "github-qubot")
            )
            record["page_content"][slot][key] = {"state": state, "claim_paths": []}
            return record

        for slot, key in (("implementation_fields", "sandbox"), ("questions", "lessons")):
            with self.subTest(slot=slot, state="unreported"):
                build.validate_record(record_with(slot, key, "unreported"), path, set())
            for state in ("not-reviewed", "not-applicable"):
                with (
                    self.subTest(slot=slot, state=state),
                    contextlib.redirect_stderr(io.StringIO()),
                    self.assertRaises(SystemExit),
                ):
                    build.validate_record(record_with(slot, key, state), path, set())

    def test_valid_markdown_only_capture(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, manifest, _ = self.write_capture(root)
            # A capture test proves nothing when the schema already rejects its source.
            self.assertTrue(SOURCE_VALIDATOR.is_valid(source))
            with mock.patch.object(build, "ROOT", root):
                build.validate_source(source, "fixture.yaml", set())
                self.assertEqual(build.load_capture_manifest(source, "fixture.yaml"), manifest)

    def test_valid_markdown_and_pdf_capture(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, manifest, _ = self.write_capture(root, pdf=b"%PDF-1.7\nfixture\n%%EOF\n")
            with mock.patch.object(build, "ROOT", root):
                build.validate_source(source, "fixture.yaml", set())
                loaded = build.load_capture_manifest(source, "fixture.yaml")
            self.assertEqual(loaded, manifest)
            self.assertIn("pdf", loaded["artifacts"])

    def test_archived_url_requires_https(self) -> None:
        for value in ("", "http://web.archive.org/example", "https://"):
            with self.subTest(value=value):
                source = self.source_fixture()
                source["archived_url"] = value
                with tempfile.TemporaryDirectory() as directory:
                    self.assert_source_invalid(source, Path(directory))

    def test_capture_requires_exact_authored_shape(self) -> None:
        for capture in ({}, {"manifest_path": "unused", "extra": True}, "unused"):
            with self.subTest(capture=capture):
                source = self.source_fixture()
                source["capture"] = capture
                with tempfile.TemporaryDirectory() as directory:
                    self.assert_source_invalid(source, Path(directory))

    def test_capture_manifest_requires_exact_schema(self) -> None:
        mutations = (
            lambda manifest: manifest.pop("http_status"),
            lambda manifest: manifest.update({"unexpected": True}),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source, manifest, path = self.write_capture(root)
                mutate(manifest)
                self.rewrite_manifest(path, manifest)
                self.assert_source_invalid(source, root)

    def test_capture_timestamp_must_be_rfc3339_utc(self) -> None:
        for value in (
            "2026-08-31",
            "2026-08-31T12:34:56+00:00",
            "2026-02-31T12:34:56Z",
        ):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source, manifest, path = self.write_capture(root)
                manifest["captured_at"] = value
                self.rewrite_manifest(path, manifest)
                self.assert_source_invalid(source, root)

    def test_capture_source_identity_must_match(self) -> None:
        mutations = (
            lambda manifest: manifest.update({"source_id": "different-source"}),
            lambda manifest: manifest.update({"original_url": "https://example.com/different"}),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source, manifest, path = self.write_capture(root)
                mutate(manifest)
                self.rewrite_manifest(path, manifest)
                self.assert_source_invalid(source, root)

    def test_capture_metadata_values_are_validated(self) -> None:
        mutations = (
            lambda manifest: manifest.update({"schema_version": 2}),
            lambda manifest: manifest.update({"final_url": "http://example.com"}),
            lambda manifest: manifest.update({"http_status": 404}),
            lambda manifest: manifest.update({"tool": {"name": "browser", "version": "1"}}),
            lambda manifest: manifest.update({"tool": {"name": "steel", "version": ""}}),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source, manifest, path = self.write_capture(root)
                mutate(manifest)
                self.rewrite_manifest(path, manifest)
                self.assert_source_invalid(source, root)

    def test_capture_paths_reject_absolute_traversal_and_cross_source_values(self) -> None:
        values = (
            "/archive/sources/fixture-source/metadata.json",
            "archive/sources/fixture-source/../fixture-source/metadata.json",
            "archive/sources/different-source/metadata.json",
            "archive\\sources\\fixture-source\\metadata.json",
        )
        for value in values:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source, _, _ = self.write_capture(root)
                source["capture"]["manifest_path"] = value
                self.assert_source_invalid(source, root)

    def test_capture_artifact_paths_cannot_escape_or_cross_bundles(self) -> None:
        values = (
            "/archive/sources/fixture-source/content.md",
            "archive/sources/fixture-source/../fixture-source/content.md",
            "archive/sources/different-source/content.md",
        )
        for value in values:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source, manifest, path = self.write_capture(root)
                manifest["artifacts"]["markdown"]["path"] = value
                self.rewrite_manifest(path, manifest)
                self.assert_source_invalid(source, root)

    def test_capture_rejects_missing_and_empty_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, _, _ = self.write_capture(root)
            (root / "archive/sources/fixture-source/content.md").unlink()
            self.assert_source_invalid(source, root)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, _, _ = self.write_capture(root, markdown=b" \n\t")
            self.assert_source_invalid(source, root)

    def test_capture_rejects_byte_count_and_sha_mismatches(self) -> None:
        mutations = (
            lambda artifact: artifact.update({"bytes": artifact["bytes"] + 1}),
            lambda artifact: artifact.update({"sha256": f"sha256:{'0' * 64}"}),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source, manifest, path = self.write_capture(root)
                mutate(manifest["artifacts"]["markdown"])
                self.rewrite_manifest(path, manifest)
                self.assert_source_invalid(source, root)

    def test_capture_rejects_invalid_and_oversized_pdf(self) -> None:
        pdf_values = (
            b"not a PDF",
            b"%PDF-" + b"0" * build.MAX_PDF_BYTES,
        )
        for pdf in pdf_values:
            with self.subTest(size=len(pdf)), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source, _, _ = self.write_capture(root, pdf=pdf)
                self.assert_source_invalid(source, root)

    def test_capture_external_archive_must_match_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, manifest, path = self.write_capture(
                root,
                archived_url="https://web.archive.org/web/20260831/https://example.com/article",
            )
            manifest["external_archive_url"] = "https://web.archive.org/web/different"
            self.rewrite_manifest(path, manifest)
            self.assert_source_invalid(source, root)

    def test_normalized_export_resolves_capture_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = copy.deepcopy(self.records[0])
            for existing_source in record["sources"]:
                existing_source.pop("capture", None)
            source, manifest, _ = self.write_capture(root, source=record["sources"][0])
            record["sources"][0] = source
            with mock.patch.object(build, "ROOT", root):
                export = build.normalize([record], [self.company_fixture(name=record["company"])])
            normalized_source = next(
                item for item in export["sources"] if item["id"] == source["id"]
            )
            self.assertEqual(export["schema_version"], 7)
            self.assertEqual(normalized_source["capture"], manifest)
            self.assertNotIn("manifest_path", normalized_source["capture"])

    def test_source_reference_renders_all_archive_combinations(self) -> None:
        original = "[Fixture source](https://example.com/article)"
        wayback = "https://web.archive.org/web/20260831/https://example.com/article"
        self.assertEqual(build.render_source_reference(self.source_fixture()), original)

        external_source = self.source_fixture()
        external_source["archived_url"] = wayback
        self.assertEqual(
            build.render_source_reference(external_source),
            f"{original} ([Wayback]({wayback}))",
        )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            local_source, _, _ = self.write_capture(root)
            with mock.patch.object(build, "ROOT", root):
                self.assertEqual(
                    build.render_source_reference(local_source),
                    f"{original} ([snapshot](../archive/sources/fixture-source/content.md), "
                    "captured 2026-08-31)",
                )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            both_source, _, _ = self.write_capture(root, archived_url=wayback)
            with mock.patch.object(build, "ROOT", root):
                self.assertEqual(
                    build.render_source_reference(both_source),
                    f"{original} ([snapshot](../archive/sources/fixture-source/content.md), "
                    f"[Wayback]({wayback}), captured 2026-08-31)",
                )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pdf_source, _, _ = self.write_capture(root, pdf=b"%PDF-1.7\nfixture\n%%EOF\n")
            with mock.patch.object(build, "ROOT", root):
                self.assertEqual(
                    build.render_source_reference(pdf_source),
                    f"{original} ([snapshot](../archive/sources/fixture-source/content.md), "
                    "[PDF](../archive/sources/fixture-source/page.pdf), captured 2026-08-31)",
                )

    def test_the_default_build_writes_the_data_and_the_repository_documents(self) -> None:
        outputs = build.data_outputs(self.records, build.normalize(self.records, self.companies))
        self.assertEqual(
            set(outputs),
            {
                build.README,
                build.PATTERNS,
                build.ADOPTION_LESSONS,
                build.LANDSCAPE,
                build.DATA_JSON,
                build.SCHEMA_VALUES_TS,
            },
        )
        for path, expected in outputs.items():
            with self.subTest(path=path.name):
                self.assertEqual(
                    path.read_bytes(),
                    expected.encode("utf-8") if isinstance(expected, str) else expected,
                )

    def test_two_builds_of_the_same_records_agree(self) -> None:
        first = build.data_outputs(self.records, build.normalize(self.records, self.companies))
        second = build.data_outputs(self.records, build.normalize(self.records, self.companies))
        self.assertEqual(first, second)

    def test_outputs_are_staged_and_a_stale_file_fails_the_check(self) -> None:
        catalog = build.normalize(self.records, self.companies)
        outputs = build.data_outputs(self.records, catalog)
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            root = Path(directory)
            relocated = {
                root / path.relative_to(ROOT): content for path, content in outputs.items()
            }
            with mock.patch.object(build, "ROOT", root):
                build.write_outputs(relocated)
                for path, content in relocated.items():
                    self.assertEqual(
                        path.read_bytes(),
                        content.encode("utf-8") if isinstance(content, str) else content,
                    )
                with (
                    mock.patch.object(build, "load_agents", return_value=self.records),
                    mock.patch.object(build, "load_companies", return_value=self.companies),
                    mock.patch.object(build, "normalize", return_value=catalog),
                    mock.patch.object(build, "data_outputs", return_value=relocated),
                    mock.patch.object(sys, "argv", ["build.py", "--check"]),
                ):
                    build.main()
                    for path in relocated:
                        original = path.read_bytes()
                        for replacement in (b"stale", None):
                            if replacement is None:
                                path.unlink()
                            else:
                                path.write_bytes(replacement)
                            with (
                                contextlib.redirect_stderr(io.StringIO()),
                                self.assertRaises(SystemExit),
                            ):
                                build.main()
                            path.write_bytes(original)

    def test_every_claim_and_source_belongs_to_one_approach(self) -> None:
        catalog = build.normalize(self.records, self.companies)
        self.assertEqual(len(catalog["approaches"]), len(self.records))
        self.assertEqual(
            sum(len(a["claim_ids"]) for a in catalog["approaches"]), len(catalog["claims"])
        )
        self.assertEqual(
            sum(len(a["source_ids"]) for a in catalog["approaches"]), len(catalog["sources"])
        )

    def test_routing_manifest_lists_every_page_of_the_catalog(self) -> None:
        manifest = json.loads((ROOT / "routing-manifest.json").read_text(encoding="utf-8"))
        expected = [
            "/",
            "/infrastructure",
            "/definitions",
            "/methodology",
            "/lessons",
            # The problem pages that the homepage offers as entry points.
            "/problems/code-review-load",
            "/problems/security-alerts",
            "/problems/company-data",
            "/problems/operations",
            *(f"/lessons/{path.stem}" for path in LESSONS.glob("*.md")),
            *(f"/agents/{record['id']}" for record in self.records),
            *(
                f"/organizations/{company_id}"
                for company_id in {
                    record["company_id"]
                    for record in build.normalize(self.records, self.companies)["approaches"]
                }
            ),
        ]
        self.assertEqual(
            sorted(manifest["routes"]),
            sorted(expected),
            "Run npm run build to regenerate routing-manifest.json for the current catalog.",
        )

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
        export = build.normalize(self.records, self.companies)
        company_count = len(
            {
                record["company"]
                for record in self.records
                if build.catalog_section(record["approach_type"]) == "agents"
            }
        )
        overview = build.render_overview(self.records, export)
        self.assertIn(
            f"{sum(build.catalog_section(record['approach_type']) == 'agents' for record in self.records)} agents",
            overview,
        )
        self.assertIn(f"{company_count} organizations", overview)
        self.assertIn(
            f"{len({source.get('canonical_url', source['url']) for source in export['sources']})} distinct sources",
            overview,
        )
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
        self.assertIn(build.render_readme_findings(self.records), readme)

    def test_catalog_statistics_keep_entry_and_workflow_units_separate(self) -> None:
        fixture = [
            {
                "approach_type": "platform",
                "autonomy": "human-in-loop",
                "operating_models": [
                    {"attention_boundary": "work-product-review"},
                    {"attention_boundary": "unknown"},
                ],
                "rubric": {"state": "mixed"},
                "architecture": {"interfaces": ["slack"], "sandbox": "unknown"},
            },
            {
                "approach_type": "supporting-pattern",
                "autonomy": "unknown",
                "operating_models": [{"attention_boundary": "unknown"}],
                "rubric": {"state": "unknown"},
                "architecture": {"interfaces": [], "sandbox": "Docker container"},
            },
        ]
        stats = build.catalog_statistics(fixture)
        self.assertEqual(stats["entries"], 2)
        self.assertEqual(stats["supporting_entries"], 2)
        self.assertEqual(stats["operating_models"], 0)
        self.assertEqual(stats["multi_workflow_entries"], 0)
        self.assertEqual(stats["attention_boundaries"]["work-product-review"], 0)
        self.assertEqual(stats["attention_boundaries"]["unknown"], 0)
        self.assertEqual(stats["autonomy"]["human-in-loop"], 0)

    def test_analysis_snapshots_match_catalog(self) -> None:
        patterns = build.render_patterns_snapshot(self.records)
        adoption = build.render_adoption_snapshot(self.records)
        autonomy_counts = Counter(
            record["autonomy"]
            for record in self.records
            if build.catalog_section(record["approach_type"]) == "agents"
        )
        self.assertIn(f"contains {len(self.records)} entries", patterns)
        self.assertIn(f"draw on {len(self.records)} catalog entries", adoption)
        self.assertIn(
            f"{autonomy_counts['drafts-reviewed']} `drafts-reviewed`",
            adoption,
        )

    def test_markdown_escapes_table_values(self) -> None:
        self.assertEqual(build.markdown("Acme | Corp\nTeam"), "Acme \\| Corp Team")
        self.assertEqual(build.markdown(["slack", "web"]), "slack, web")

    def test_company_registry_loads_and_joins_both_ways(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_registry(root, [self.company_fixture()])
            registry = build.load_companies(self.fixture_records(), root=root)
            self.assertEqual(registry, [self.company_fixture()])

    def assert_registry_error(self, records: list[dict], root: Path) -> str:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            build.load_companies(records, root=root)
        return stderr.getvalue()

    def test_company_registry_must_join_both_ways(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_registry(root, [self.company_fixture()])
            message = self.assert_registry_error(
                [
                    {"id": "fixture-agent", "company": "Fixture"},
                    {"id": "other-agent", "company": "Other"},
                ],
                root,
            )
            self.assertIn(
                "other-agent.yaml: company 'Other' has no record in data/companies.yaml.", message
            )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_registry(
                root,
                [
                    self.company_fixture(),
                    self.company_fixture(
                        id="unused-company",
                        name="Unused",
                        homepage="https://unused.example/",
                    ),
                ],
            )
            message = self.assert_registry_error(self.fixture_records(), root)
            self.assertIn(
                "data/companies.yaml: company 'unused-company' is not used by any approach record.",
                message,
            )

    def test_company_registry_rejects_invalid_records(self) -> None:
        fixtures = (
            self.company_fixture(id="Fixture"),
            self.company_fixture(name=""),
            self.company_fixture(homepage="http://www.fixture.example/"),
            self.company_fixture(logo_note=None),
            self.company_fixture(logo=None),
            self.company_fixture(
                logo={
                    "file": "fixture-company.gif",
                    "source_url": "https://fixture.example/logo",
                    "accessed_at": "2026-09-15",
                }
            ),
            {**self.company_fixture(), "extra": True},
        )
        for company in fixtures:
            with self.subTest(company=company), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.write_registry(root, [company])
                self.assert_registry_invalid(self.fixture_records(), root)
        for companies in (
            [self.company_fixture(), self.company_fixture(homepage="https://other.example/")],
            [
                self.company_fixture(),
                self.company_fixture(id="second-company", homepage="https://other.example/"),
            ],
            [self.company_fixture(id="z-company"), self.company_fixture(id="a-company")],
        ):
            with self.subTest(companies=companies), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.write_registry(root, companies)
                self.assert_registry_invalid(self.fixture_records(), root)

    def test_company_logo_file_rules(self) -> None:
        fixtures = (
            {
                "file": "other.svg",
                "source_url": "https://fixture.example/logo",
                "accessed_at": "2026-09-15",
            },
            {
                "file": "fixture-company.svg",
                "source_url": "http://fixture.example/logo",
                "accessed_at": "2026-09-15",
            },
            {
                "file": "fixture-company.svg",
                "source_url": "https://fixture.example/logo",
                "accessed_at": "2026-9-15",
            },
            {"file": "fixture-company.svg", "source_url": "https://fixture.example/logo"},
        )
        for logo in fixtures:
            with self.subTest(logo=logo), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.write_logo(root, "fixture-company.svg", self.logo_svg())
                self.write_registry(root, [self.company_fixture(logo=logo)])
                self.assert_registry_invalid(self.fixture_records(), root)

    def test_company_logo_asset_must_exist_and_be_named_by_the_registry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_registry(
                root,
                [
                    self.company_fixture(
                        logo={
                            "file": "fixture-company.svg",
                            "source_url": "https://fixture.example/logo",
                            "accessed_at": "2026-09-15",
                        }
                    )
                ],
            )
            self.assert_registry_invalid(self.fixture_records(), root)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_logo(root, "fixture-company.svg", self.logo_svg())
            self.write_logo(root, "stray.svg", self.logo_svg())
            self.write_registry(root, [self.company_fixture(logo="none")])
            self.assert_registry_invalid(self.fixture_records(), root)

    def test_company_logo_must_not_hold_unsafe_svg(self) -> None:
        payloads = (
            b'<!DOCTYPE svg><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 40"/>',
            b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 40"><!ENTITY x "y"/></svg>',
            b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 40"><script>1</script></svg>',
            b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 40">'
            b"<foreignObject><p>1</p></foreignObject></svg>",
            self.logo_svg(onload="alert(1)"),
            self.logo_svg(viewBox="0 0 128 40", href="https://evil.example/logo"),
        )
        for content in payloads:
            with self.subTest(content=content), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.write_logo(root, "fixture-company.svg", content)
                self.write_registry(
                    root,
                    [
                        self.company_fixture(
                            logo={
                                "file": "fixture-company.svg",
                                "source_url": "https://fixture.example/logo",
                                "accessed_at": "2026-09-15",
                            }
                        )
                    ],
                )
                self.assert_registry_invalid(self.fixture_records(), root)

    def test_company_logo_assets_are_limited_in_size(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_logo(
                root, "fixture-company.svg", self.logo_svg() + b" " * build.MAX_SVG_LOGO_BYTES
            )
            self.write_registry(
                root,
                [
                    self.company_fixture(
                        logo={
                            "file": "fixture-company.svg",
                            "source_url": "https://fixture.example/logo",
                            "accessed_at": "2026-09-15",
                        }
                    )
                ],
            )
            self.assert_registry_invalid(self.fixture_records(), root)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_logo(root, "fixture-company.png", self.logo_png(width=127))
            self.write_registry(
                root,
                [
                    self.company_fixture(
                        logo={
                            "file": "fixture-company.png",
                            "source_url": "https://fixture.example/logo",
                            "accessed_at": "2026-09-15",
                        }
                    )
                ],
            )
            self.assert_registry_invalid(self.fixture_records(), root)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_logo(
                root, "fixture-company.png", self.logo_png() + b"\x00" * build.MAX_PNG_LOGO_BYTES
            )
            self.write_registry(
                root,
                [
                    self.company_fixture(
                        logo={
                            "file": "fixture-company.png",
                            "source_url": "https://fixture.example/logo",
                            "accessed_at": "2026-09-15",
                        }
                    )
                ],
            )
            self.assert_registry_invalid(self.fixture_records(), root)

    def test_company_logo_assets_need_a_usable_size(self) -> None:
        payloads = (
            ("fixture-company.svg", b'<svg xmlns="http://www.w3.org/2000/svg"><path/></svg>'),
            ("fixture-company.svg", self.logo_svg(viewBox="0 0 0 40")),
            ("fixture-company.svg", b"<svg viewBox='0 0 128'>path</svg>"),
            ("fixture-company.svg", self.logo_svg(viewBox="0 0 inf 40")),
            ("fixture-company.svg", self.logo_svg(viewBox="0 0 nan 40")),
            ("fixture-company.png", b"\x89PNG\r\n\x1a\n" + b"\x00" * 8),
        )
        for name, content in payloads:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.write_logo(root, name, content)
                self.write_registry(
                    root,
                    [
                        self.company_fixture(
                            logo={
                                "file": name,
                                "source_url": "https://fixture.example/logo",
                                "accessed_at": "2026-09-15",
                            }
                        )
                    ],
                )
                self.assert_registry_invalid(self.fixture_records(), root)

    def test_company_logo_descriptor_derives_hash_bytes_and_size(self) -> None:
        for name, content, media_type, size in (
            ("fixture-company.svg", self.logo_svg(), "image/svg+xml", (128, 40)),
            ("fixture-company.png", self.logo_png(width=200, height=64), "image/png", (200, 64)),
        ):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.write_logo(root, name, content)
                logo = {
                    "file": name,
                    "source_url": "https://fixture.example/logo",
                    "accessed_at": "2026-09-15",
                }
                self.write_registry(root, [self.company_fixture(logo=logo)])
                registry = build.load_companies(self.fixture_records(), root=root)
                companies = build.normalize_companies(registry, root=root)
                self.assertEqual(len(companies), 1)
                descriptor = companies[0]["logo"]
                self.assertEqual(
                    descriptor,
                    {
                        "path": f"logos/{name}",
                        "media_type": media_type,
                        "width": size[0],
                        "height": size[1],
                        "bytes": len(content),
                        "sha256": f"sha256:{hashlib.sha256(content).hexdigest()}",
                        "source_url": "https://fixture.example/logo",
                        "accessed_at": "2026-09-15",
                    },
                )

    def test_company_without_a_logo_publishes_a_monogram_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_registry(root, [self.company_fixture()])
            companies = build.normalize_companies(
                build.load_companies(self.fixture_records(), root=root), root=root
            )
            self.assertEqual(companies[0]["logo"], None)
        self.assertEqual(
            build.company_summary(
                [self.company_fixture(logo="none"), self.company_fixture(logo="none")]
            ),
            "2 organizations, 0 logos, 2 monograms",
        )

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

    def test_featured_must_be_a_boolean(self) -> None:
        record = copy.deepcopy(self.records[0])
        record["featured"] = "yes"
        with (
            tempfile.TemporaryDirectory() as directory,
            contextlib.redirect_stderr(io.StringIO()),
            self.assertRaises(SystemExit),
        ):
            path = Path(directory) / f"{record['id']}.yaml"
            build.validate_record(record, path, set())

    def assert_record_error(self, record: dict) -> str:
        stderr = io.StringIO()
        with (
            tempfile.TemporaryDirectory() as directory,
            contextlib.redirect_stderr(stderr),
            self.assertRaises(SystemExit),
        ):
            build.validate_record(record, Path(directory) / f"{record['id']}.yaml", set())
        return stderr.getvalue()

    def test_primitive_with_an_unexpected_field_fails(self) -> None:
        # An unquoted comma in a flow mapping splits the description into extra keys.
        record = copy.deepcopy(self.records[0])
        record["primitives"] = [
            {"name": "Wake", "desc": "When an incident is detected", "the bot wakes up": None}
        ]
        message = self.assert_record_error(record)
        self.assertIn(f"{record['id']}.yaml: primitives.0:", message)
        self.assertIn("'the bot wakes up' was unexpected", message)

    def test_schema_errors_name_the_field_path(self) -> None:
        record = copy.deepcopy(self.records[0])
        record["rubric"]["invocation"] = ["batch"]
        message = self.assert_record_error(record)
        self.assertIn(f"{record['id']}.yaml: rubric.invocation.0: 'batch' is not one of", message)

    def test_page_content_state_rules_come_from_the_schema(self) -> None:
        record = copy.deepcopy(
            next(record for record in self.records if record.get("page_content"))
        )
        record["page_content"]["questions"]["validation"] = {
            "state": "not-reviewed",
            "claim_paths": [],
        }
        message = self.assert_record_error(record)
        self.assertIn("page_content.questions.validation: 'note' is a required property", message)

    def test_agent_schema_is_a_valid_draft_7_schema(self) -> None:
        build.Draft7Validator.check_schema(build.AGENT_SCHEMA)

    def test_boundary_levels_cover_every_attention_boundary(self) -> None:
        self.assertEqual(set(build.BOUNDARY_LEVELS), build.schema_values("attentionBoundary"))

    def test_generated_typescript_lists_every_schema_value(self) -> None:
        generated = build.render_schema_values()
        self.assertIn(
            "export const RELATION_TYPE_VALUES = "
            "['component-of', 'built-on', 'successor-of', 'related-to'] as const;",
            generated,
        )
        self.assertIn(
            "export type ClaimProvenance = (typeof CLAIM_PROVENANCE_VALUES)[number];", generated
        )

    def test_every_agent_file_declares_the_schema(self) -> None:
        for path in [*sorted(build.AGENTS_DIR.glob("*.yaml")), ROOT / "templates" / "agent.yaml"]:
            with self.subTest(path=path.name):
                self.assertIn(build.SCHEMA_MODELINE, path.read_text(encoding="utf-8").splitlines())

    def test_schema_document_names_every_schema_value(self) -> None:
        guide = (ROOT / "data" / "schema.md").read_text(encoding="utf-8")
        for name, definition in build.AGENT_SCHEMA["definitions"].items():
            for value in definition.get("enum", []):
                with self.subTest(definition=name, value=value):
                    self.assertIn(f"`{value}`", guide)

    def test_featured_reaches_the_export(self) -> None:
        featured = {
            approach["id"]
            for approach in build.normalize(self.records, self.companies)["approaches"]
            if approach.get("featured")
        }
        self.assertEqual(featured, {"linear-agent", "sierra-pinecone", "stripe-minions"})

    def test_impossible_calendar_date_fails(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            build.validate_date("2026-02-31", "last_reviewed_at", "example.yaml")

    def test_json_is_serializable(self) -> None:
        json.dumps(build.normalize(self.records, self.companies))

    def test_template_matches_schema(self) -> None:
        template = yaml.safe_load((ROOT / "templates" / "agent.yaml").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "company-agent.yaml"
            build.validate_record(template, path, set())

    def test_documented_sample_counts_are_current(self) -> None:
        patterns = (ROOT / "docs" / "patterns.md").read_text(encoding="utf-8")
        labels = {
            "agent": "Agent",
            "platform": "Platform",
            "agent-system": "Agent family",
            "orchestration-system": "Orchestration system",
            "supporting-pattern": "Supporting pattern",
        }
        counts = Counter(record["approach_type"] for record in self.records)
        for value, label in labels.items():
            self.assertIn(f"| {label} | {counts[value]} |", patterns)


if __name__ == "__main__":
    unittest.main()
