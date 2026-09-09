from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "catalog_check_links", ROOT / "scripts" / "check_links.py"
)
check_links = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = check_links
SPEC.loader.exec_module(check_links)


def http_error(code: int) -> urllib.error.HTTPError:
    return urllib.error.HTTPError("https://example.com", code, "error", None, None)


def response(status: int = 200) -> MagicMock:
    result = MagicMock(status=status)
    result.__enter__.return_value = result
    return result


def link_result(url: str, status: str, detail: str | None = None) -> check_links.LinkResult:
    return check_links.LinkResult(url, status, detail or status)


def write_snapshot(
    root: Path,
    target: check_links.SourceTarget,
    *,
    content: bytes = b"# Preserved source\n",
    sha256: str | None = None,
    byte_count: int | None = None,
) -> None:
    bundle = root / "archive" / "sources" / target.source_id
    bundle.mkdir(parents=True)
    (bundle / "content.md").write_bytes(content)
    manifest = {
        "schema_version": 1,
        "source_id": target.source_id,
        "original_url": target.url,
        "final_url": target.url,
        "captured_at": "2026-08-31T12:34:56Z",
        "http_status": 200,
        "tool": {"name": "steel", "version": "0.4.4"},
        "artifacts": {
            "markdown": {
                "path": f"archive/sources/{target.source_id}/content.md",
                "sha256": sha256 or f"sha256:{hashlib.sha256(content).hexdigest()}",
                "bytes": len(content) if byte_count is None else byte_count,
            }
        },
    }
    if target.archived_url:
        manifest["external_archive_url"] = target.archived_url
    (bundle / "metadata.json").write_text(json.dumps(manifest), encoding="utf-8")


class HttpLinkTests(unittest.TestCase):
    def test_healthy_head_is_reported(self) -> None:
        with patch.object(check_links.urllib.request, "urlopen", return_value=response()):
            result = check_links.check_url("https://example.com")
        self.assertEqual(result.status, "healthy")

    def test_get_confirms_missing_head_result(self) -> None:
        with patch.object(
            check_links.urllib.request,
            "urlopen",
            side_effect=[http_error(404), http_error(404)],
        ):
            result = check_links.check_url("https://example.com")
        self.assertEqual(result.status, "missing")
        self.assertEqual(result.detail, "HTTP 404 confirmed by GET")

    def test_get_confirms_gone_head_result(self) -> None:
        with patch.object(
            check_links.urllib.request,
            "urlopen",
            side_effect=[http_error(410), http_error(410)],
        ):
            result = check_links.check_url("https://example.com")
        self.assertEqual(result.status, "missing")
        self.assertEqual(result.detail, "HTTP 410 confirmed by GET")

    def test_get_recovers_from_incorrect_missing_head_result(self) -> None:
        with patch.object(
            check_links.urllib.request,
            "urlopen",
            side_effect=[http_error(404), response()],
        ):
            result = check_links.check_url("https://example.com")
        self.assertEqual(result.status, "healthy")
        self.assertEqual(result.detail, "GET HTTP 200")

    def test_access_control_is_distinguished_from_missing(self) -> None:
        with patch.object(check_links.urllib.request, "urlopen", side_effect=http_error(403)):
            result = check_links.check_url("https://example.com")
        self.assertEqual(result.status, "blocked")

    def test_server_failure_is_unreachable(self) -> None:
        with patch.object(check_links.urllib.request, "urlopen", side_effect=http_error(500)):
            result = check_links.check_url("https://example.com")
        self.assertEqual(result.status, "unreachable")

    def test_timeout_is_unreachable(self) -> None:
        with patch.object(
            check_links.urllib.request, "urlopen", side_effect=TimeoutError("timed out")
        ):
            result = check_links.check_url("https://example.com")
        self.assertEqual(result.status, "unreachable")


class DiscoveryTests(unittest.TestCase):
    def test_unmatched_inline_ticks_do_not_cross_blocks(self) -> None:
        for separator in ("\n\n", "\n   \n", "\n```\nexample\n```\n"):
            text = "Unmatched ` tick" + separator + "[real](https://real.example) `tail"
            self.assertIn("[real](https://real.example)", check_links.markdown_prose(text))

    def test_code_examples_are_excluded_from_local_and_external_links(self) -> None:
        text = """# Real heading
[heading](#real-heading)
`[inline](inline-missing.md)` and ``[double](https://inline.example)``
  ````markdown
[example](missing.md)
```
[example](https://publisher.example)
  ````
~~~
[example](https://wayback.example)
~~~
[real](https://real.example)
[broken](actual-missing.md)
```
[unclosed](unclosed-missing.md)
"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "example.md"
            path.write_text(text)
            with (
                patch.object(check_links, "ROOT", root),
                patch.object(check_links, "tracked_markdown", return_value=[path]),
            ):
                self.assertEqual(check_links.markdown_urls(), {"https://real.example"})
                self.assertEqual(
                    check_links.local_links(),
                    ["example.md: missing local target actual-missing.md"],
                )

    def test_tracked_markdown_excludes_archive_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            completed = SimpleNamespace(
                stdout="README.md\narchive/README.md\narchive/sources/source/content.md\n"
            )
            with (
                patch.object(check_links, "ROOT", root),
                patch.object(check_links, "ARCHIVE_DIR", root / "archive"),
                patch.object(check_links.subprocess, "run", return_value=completed),
            ):
                paths = check_links.tracked_markdown()
        self.assertEqual(paths, [root / "README.md"])

    def test_catalog_urls_are_removed_from_general_markdown_urls(self) -> None:
        source = check_links.SourceTarget(
            "source-1",
            "https://publisher.example/article",
            "https://web.archive.org/example",
        )
        sources, general = check_links.external_targets(
            [source],
            {
                source.url,
                source.archived_url,
                "https://docs.example/general",
            },
        )
        self.assertEqual(sources, [source])
        self.assertEqual(general, ["https://docs.example/general"])

    def test_catalog_sources_preserve_archive_and_manifest_pairing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            agents = Path(directory) / "data" / "agents"
            agents.mkdir(parents=True)
            (agents / "example.yaml").write_text(
                """sources:
- id: source-1
  url: https://publisher.example/article
  archived_url: https://web.archive.org/example
  capture:
    manifest_path: archive/sources/source-1/metadata.json
""",
                encoding="utf-8",
            )
            with patch.object(check_links, "AGENTS_DIR", agents):
                targets = check_links.catalog_sources()
        self.assertEqual(
            targets,
            [
                check_links.SourceTarget(
                    "source-1",
                    "https://publisher.example/article",
                    "https://web.archive.org/example",
                    "archive/sources/source-1/metadata.json",
                )
            ],
        )

    def test_normal_project_markdown_still_reports_missing_local_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readme = root / "README.md"
            readme.write_text("[missing](docs/missing.md)\n", encoding="utf-8")
            with (
                patch.object(check_links, "ROOT", root),
                patch.object(check_links, "tracked_markdown", return_value=[readme]),
            ):
                errors = check_links.local_links()
        self.assertEqual(errors, ["README.md: missing local target docs/missing.md"])


class SnapshotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.target = check_links.SourceTarget(
            "source-1",
            "https://publisher.example/article",
            manifest_path="archive/sources/source-1/metadata.json",
        )

    def test_valid_local_snapshot_is_verified(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_snapshot(root, self.target)
            with patch.object(check_links, "ROOT", root):
                result = check_links.local_snapshot_result(self.target)
        self.assertEqual(result.status, "healthy")
        self.assertEqual(result.detail, "verified local Markdown snapshot")

    def test_missing_declared_snapshot_is_invalid(self) -> None:
        with (
            tempfile.TemporaryDirectory() as directory,
            patch.object(check_links, "ROOT", Path(directory)),
        ):
            result = check_links.local_snapshot_result(self.target)
        self.assertEqual(result.status, "invalid")
        self.assertIn("manifest does not exist", result.detail)

    def test_hash_mismatch_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_snapshot(root, self.target, sha256=f"sha256:{'0' * 64}")
            with patch.object(check_links, "ROOT", root):
                result = check_links.local_snapshot_result(self.target)
        self.assertEqual(result.status, "invalid")
        self.assertIn("SHA-256 does not match", result.detail)

    def test_byte_count_mismatch_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_snapshot(root, self.target, byte_count=1)
            with patch.object(check_links, "ROOT", root):
                result = check_links.local_snapshot_result(self.target)
        self.assertEqual(result.status, "invalid")
        self.assertIn("byte count", result.detail)

    def test_manifest_path_traversal_is_invalid(self) -> None:
        target = check_links.SourceTarget(
            "source-1",
            "https://publisher.example/article",
            manifest_path="archive/sources/source-1/../metadata.json",
        )
        result = check_links.local_snapshot_result(target)
        self.assertEqual(result.status, "invalid")
        self.assertIn("safe repository-relative", result.detail)


class SourcePolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.target = check_links.SourceTarget(
            "source-1",
            "https://publisher.example/article",
            "https://web.archive.org/example",
        )
        self.missing = link_result(self.target.url, "missing", "HTTP 404 confirmed by GET")
        self.absent = check_links.SnapshotResult("absent", "no local snapshot declared")

    def test_missing_original_with_valid_local_snapshot_is_archived(self) -> None:
        snapshot = check_links.SnapshotResult("healthy", "verified")
        archive = link_result(self.target.archived_url, "unreachable")
        result = check_links.classify_source(self.target, self.missing, snapshot, archive)
        self.assertEqual(result.status, "archived")
        self.assertIn("verified local snapshot", result.detail)

    def test_missing_original_with_healthy_external_archive_is_archived(self) -> None:
        archive = link_result(self.target.archived_url, "healthy")
        result = check_links.classify_source(self.target, self.missing, self.absent, archive)
        self.assertEqual(result.status, "archived")
        self.assertIn("healthy external archive", result.detail)

    def test_missing_original_without_fallback_fails(self) -> None:
        archive = link_result(self.target.archived_url, "missing")
        result = check_links.classify_source(self.target, self.missing, self.absent, archive)
        self.assertEqual(result.status, "missing")
        self.assertIn("no verified archive fallback", result.detail)

    def test_invalid_declared_snapshot_fails_even_when_original_is_healthy(self) -> None:
        original = link_result(self.target.url, "healthy")
        invalid = check_links.SnapshotResult("invalid", "hash mismatch")
        result = check_links.classify_source(self.target, original, invalid, None)
        self.assertEqual(result.status, "missing")
        self.assertIn("invalid declared local snapshot", result.detail)

    def test_blocked_and_unreachable_originals_remain_warnings(self) -> None:
        for status in ("blocked", "unreachable"):
            with self.subTest(status=status):
                original = link_result(self.target.url, status)
                result = check_links.classify_source(self.target, original, self.absent, None)
                self.assertEqual(result.status, status)

    def test_healthy_original_with_unavailable_wayback_stays_healthy(self) -> None:
        original = link_result(self.target.url, "healthy")
        archive = link_result(self.target.archived_url, "unreachable", "timed out")
        result = check_links.classify_source(self.target, original, self.absent, archive)
        self.assertEqual(result.status, "healthy")
        self.assertEqual(len(result.warnings), 1)
        self.assertIn("external archive unreachable", result.warnings[0])


class MainTests(unittest.TestCase):
    def test_archived_source_warns_and_exits_successfully(self) -> None:
        source = check_links.SourceTarget(
            "source-1",
            "https://publisher.example/article",
            "https://web.archive.org/example",
        )
        results = {
            source.url: link_result(source.url, "missing", "HTTP 404 confirmed by GET"),
            source.archived_url: link_result(source.archived_url, "healthy", "HTTP 200"),
        }
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            patch.object(check_links, "local_links", return_value=[]),
            patch.object(check_links, "catalog_sources", return_value=[source]),
            patch.object(
                check_links,
                "markdown_urls",
                return_value={source.url, source.archived_url},
            ),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            status = check_links.main([], checker=results.__getitem__)
        self.assertEqual(status, 0)
        self.assertIn("1 archived", stdout.getvalue())
        self.assertIn("warning: archived: source-1", stderr.getvalue())

    def test_missing_source_without_fallback_exits_nonzero(self) -> None:
        source = check_links.SourceTarget("source-1", "https://publisher.example/article")
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            patch.object(check_links, "local_links", return_value=[]),
            patch.object(check_links, "catalog_sources", return_value=[source]),
            patch.object(check_links, "markdown_urls", return_value={source.url}),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            status = check_links.main(
                [], checker=lambda url: link_result(url, "missing", "HTTP 410 confirmed by GET")
            )
        self.assertEqual(status, 1)
        self.assertIn("1 missing", stdout.getvalue())
        self.assertIn("no verified archive fallback", stderr.getvalue())

    def test_network_url_is_checked_once_when_two_sources_share_it(self) -> None:
        url = "https://publisher.example/shared"
        sources = [
            check_links.SourceTarget("source-1", url),
            check_links.SourceTarget("source-2", url),
        ]
        calls = []

        def checker(target_url: str) -> check_links.LinkResult:
            calls.append(target_url)
            return link_result(target_url, "healthy")

        source_results, documentation_results = check_links.check_external_targets(
            sources, [], checker
        )
        self.assertEqual(calls, [url])
        self.assertEqual([result.status for result in source_results], ["healthy", "healthy"])
        self.assertEqual(documentation_results, [])

    def test_local_mode_does_not_load_or_check_external_targets(self) -> None:
        stdout = io.StringIO()
        with (
            patch.object(check_links, "local_links", return_value=[]),
            patch.object(check_links, "catalog_sources") as catalog_sources,
            contextlib.redirect_stdout(stdout),
        ):
            status = check_links.main(
                ["--local"], checker=lambda url: self.fail(f"unexpected network check: {url}")
            )
        self.assertEqual(status, 0)
        catalog_sources.assert_not_called()
        self.assertIn("Checked local links.", stdout.getvalue())


class ArchiveContainmentTests(unittest.TestCase):
    def test_symlink_boundaries(self) -> None:
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
                external = Path(outside)
                sibling = bundle.parent / "sibling"
                sibling.mkdir()
                destination = external if "external" in mode else sibling
                filename = "metadata.json" if mode.startswith("manifest") else "content.md"
                (bundle / filename).write_text("{}")
                if mode.startswith("source"):
                    (bundle / filename).unlink()
                    bundle.rmdir()
                    (destination / filename).write_text("{}")
                    bundle.symlink_to(destination, target_is_directory=True)
                elif mode.startswith("archive"):
                    shutil.rmtree(root / "archive")
                    (external / "sources" / "fixture").mkdir(parents=True)
                    (external / "sources" / "fixture" / filename).write_text("{}")
                    (root / "archive").symlink_to(external, target_is_directory=True)
                else:
                    (bundle / filename).unlink()
                    (destination / filename).write_text("{}")
                    (bundle / filename).symlink_to(destination / filename)
                with patch.object(check_links, "ROOT", root):
                    resolved, error = check_links._safe_archive_path(
                        f"archive/sources/fixture/{filename}", "fixture", filename
                    )
                self.assertIsNone(resolved)
                self.assertIn("escapes", error)


if __name__ == "__main__":
    unittest.main()
