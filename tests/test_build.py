from __future__ import annotations

import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

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
        export = build.normalize(self.records)
        self.assertEqual(export["schema_version"], 4)
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

    def test_valid_markdown_only_capture(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, manifest, _ = self.write_capture(root)
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
                export = build.normalize([record])
            normalized_source = next(
                item for item in export["sources"] if item["id"] == source["id"]
            )
            self.assertEqual(export["schema_version"], 4)
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
