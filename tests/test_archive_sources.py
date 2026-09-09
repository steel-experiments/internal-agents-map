from __future__ import annotations

import contextlib
import hashlib
import http.client
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock, patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "archive_sources", ROOT / "scripts" / "archive_sources.py"
)
archive_sources = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = archive_sources
SPEC.loader.exec_module(archive_sources)


LONG_MARKDOWN = (
    "This is preserved source material with enough meaningful text to pass the short-page "
    "safety check. It records implementation details and supporting evidence."
)
SOURCE = {"id": "acme-agent-source-1", "url": "https://example.com/article"}
CAPTURED_AT = datetime(2026, 8, 31, 12, 34, 56, tzinfo=timezone.utc)


def steel_envelope(
    *,
    markdown: str = LONG_MARKDOWN,
    title: str = "An internal agent at Acme",
    status: int = 200,
    final_url: str = "https://example.com/article",
    pdf_url: str | None = None,
    metadata_extra: dict[str, object] | None = None,
) -> str:
    metadata: dict[str, object] = {
        "statusCode": status,
        "title": title,
        "urlSource": final_url,
    }
    if metadata_extra:
        metadata.update(metadata_extra)
    data: dict[str, object] = {
        "content": {"markdown": markdown},
        "metadata": metadata,
    }
    if pdf_url is not None:
        data["pdf"] = {"url": pdf_url}
    return json.dumps({"success": True, "data": data})


class FakeResponse(io.BytesIO):
    def __init__(
        self,
        data: bytes,
        *,
        status: int = 200,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(data)
        self.status = status
        self.headers = headers or {}

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *_args: object) -> None:
        self.close()


class QueueOpener:
    def __init__(self, *responses: FakeResponse | Exception) -> None:
        self.responses = list(responses)
        self.requests: list[object] = []

    def __call__(self, request: object, *, timeout: int) -> FakeResponse:
        self.requests.append(request)
        if not self.responses:
            raise AssertionError("unexpected network request")
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def scrape_runner(stdout: str) -> Mock:
    return Mock(
        return_value=subprocess.CompletedProcess(
            args=["steel"],
            returncode=0,
            stdout=stdout,
            stderr="",
        )
    )


def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


class SourceLoadingTests(unittest.TestCase):
    def write_agent(self, directory: Path, name: str, sources: list[dict[str, object]]) -> None:
        (directory / name).write_text(yaml.safe_dump({"sources": sources}), encoding="utf-8")

    def test_load_and_lookup_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            agents = Path(directory)
            self.write_agent(agents, "agent.yaml", [SOURCE])
            sources = archive_sources.load_sources(agents)
        self.assertEqual(sources[SOURCE["id"]]["url"], SOURCE["url"])
        self.assertEqual(archive_sources.get_source(SOURCE["id"], sources), SOURCE)
        with self.assertRaisesRegex(archive_sources.ArchiveError, "Unknown source ID"):
            archive_sources.get_source("missing-source", sources)

    def test_duplicate_source_id_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            agents = Path(directory)
            self.write_agent(agents, "a.yaml", [SOURCE])
            self.write_agent(agents, "b.yaml", [SOURCE])
            with self.assertRaisesRegex(archive_sources.ArchiveError, "Duplicate source ID"):
                archive_sources.load_sources(agents)

    def test_missing_source_id_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            agents = Path(directory)
            self.write_agent(agents, "agent.yaml", [{"url": SOURCE["url"]}])
            with self.assertRaisesRegex(archive_sources.ArchiveError, "missing or invalid ID"):
                archive_sources.load_sources(agents)


class SteelTests(unittest.TestCase):
    def test_steel_success_is_parsed_and_invoked_without_a_shell(self) -> None:
        runner = scrape_runner(steel_envelope())
        result = archive_sources.scrape_with_steel(SOURCE["url"], delay_ms=250, runner=runner)
        self.assertEqual(result.http_status, 200)
        self.assertEqual(result.final_url, SOURCE["url"])
        self.assertEqual(result.markdown, LONG_MARKDOWN)
        runner.assert_called_once_with(
            [
                "steel",
                "--json",
                "scrape",
                SOURCE["url"],
                "--format",
                "markdown",
                "--delay",
                "250",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_steel_version_is_recordable(self) -> None:
        runner = Mock(
            return_value=subprocess.CompletedProcess(
                args=["steel", "--version"],
                returncode=0,
                stdout="steel 0.4.4\n",
                stderr="",
            )
        )
        self.assertEqual(archive_sources.steel_version(runner=runner), "0.4.4")

    def test_malformed_json_and_missing_fields_are_rejected(self) -> None:
        cases = (
            ("not json", "malformed JSON"),
            (json.dumps({"success": False}), "scrape failed"),
            (json.dumps({"success": True}), "response.data"),
            (
                json.dumps({"success": True, "data": {"content": {}}}),
                "data.metadata",
            ),
            (
                json.dumps(
                    {
                        "success": True,
                        "data": {
                            "content": {"markdown": LONG_MARKDOWN},
                            "metadata": {"statusCode": 200},
                        },
                    }
                ),
                "metadata.title",
            ),
        )
        for value, message in cases:
            with (
                self.subTest(message=message),
                self.assertRaisesRegex(archive_sources.ArchiveError, message),
            ):
                archive_sources.parse_steel_response(value)

    def test_non_2xx_empty_and_interstitial_pages_are_rejected(self) -> None:
        cases = (
            (steel_envelope(status=404), "non-success HTTP status"),
            (steel_envelope(markdown=""), "suspiciously short"),
            (steel_envelope(markdown="too short"), "suspiciously short"),
            (steel_envelope(title="Just a moment..."), "interstitial"),
            (steel_envelope(title="403 Forbidden"), "interstitial"),
            (steel_envelope(title="LinkedIn: Log In or Sign Up"), "interstitial"),
            (
                steel_envelope(
                    markdown=(
                        LONG_MARKDOWN
                        + "\n\nSorry, the page you're looking for cannot be found. Visit our homepage."
                    )
                ),
                "interstitial",
            ),
        )
        for value, message in cases:
            with (
                self.subTest(message=message),
                self.assertRaisesRegex(archive_sources.ArchiveError, message),
            ):
                archive_sources.parse_steel_response(value)

    def test_explicit_noarchive_is_rejected(self) -> None:
        for value in (
            steel_envelope(metadata_extra={"robots": "index, noarchive"}),
            steel_envelope(metadata_extra={"noarchive": True}),
            steel_envelope(
                markdown=('<meta name="robots" content="noarchive">\n\n' + LONG_MARKDOWN)
            ),
        ):
            with (
                self.subTest(value=value),
                self.assertRaisesRegex(archive_sources.ArchiveError, "noarchive"),
            ):
                archive_sources.parse_steel_response(value)

    def test_pdf_field_is_required_when_requested(self) -> None:
        with self.assertRaisesRegex(archive_sources.ArchiveError, "data.pdf"):
            archive_sources.parse_steel_response(steel_envelope(), include_pdf=True)
        result = archive_sources.parse_steel_response(
            steel_envelope(pdf_url="https://files.steel.dev/page.pdf"), include_pdf=True
        )
        self.assertEqual(result.pdf_url, "https://files.steel.dev/page.pdf")


class PdfTests(unittest.TestCase):
    def test_valid_pdf_is_downloaded(self) -> None:
        data = b"%PDF-1.7\nbody"
        opener = QueueOpener(FakeResponse(data, headers={"Content-Length": str(len(data))}))
        self.assertEqual(
            archive_sources.download_pdf("https://files.steel.dev/page.pdf", opener=opener),
            data,
        )

    def test_invalid_magic_and_oversized_pdf_are_rejected(self) -> None:
        with self.assertRaisesRegex(archive_sources.ArchiveError, "%PDF-"):
            archive_sources.download_pdf(
                "https://files.steel.dev/page.pdf", opener=QueueOpener(FakeResponse(b"not pdf"))
            )
        oversized = FakeResponse(
            b"",
            headers={"Content-Length": str(archive_sources.MAX_PDF_BYTES + 1)},
        )
        with self.assertRaisesRegex(archive_sources.ArchiveError, "allowed size"):
            archive_sources.download_pdf(
                "https://files.steel.dev/page.pdf", opener=QueueOpener(oversized)
            )

    def test_truncated_pdf_is_rejected(self) -> None:
        data = b"%PDF-1.7\nbody"
        response = FakeResponse(data, headers={"Content-Length": str(len(data) + 5)})
        with self.assertRaisesRegex(archive_sources.ArchiveError, "truncated"):
            archive_sources.download_pdf(
                "https://files.steel.dev/page.pdf", opener=QueueOpener(response)
            )


class BundleTests(unittest.TestCase):
    def capture(
        self,
        root: Path,
        *,
        response: str | None = None,
        pdf_response: FakeResponse | None = None,
    ) -> archive_sources.CaptureResult:
        include_pdf = pdf_response is not None
        response = response or steel_envelope(
            pdf_url="https://files.steel.dev/page.pdf" if include_pdf else None
        )
        return archive_sources.capture_source(
            SOURCE,
            pdf=include_pdf,
            delay_ms=0,
            repo_root=root,
            runner=scrape_runner(response),
            opener=QueueOpener(pdf_response) if pdf_response is not None else None,
            captured_at=CAPTURED_AT,
            steel_version_value="0.4.4",
        )

    def test_attribution_newlines_hashes_and_bytes_are_exact(self) -> None:
        response = steel_envelope(markdown="\r\n" + LONG_MARKDOWN + "\r\n")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.capture(root, response=response)
            bundle = root / "archive" / "sources" / SOURCE["id"]
            markdown = (bundle / "content.md").read_bytes()
            manifest = json.loads((bundle / "metadata.json").read_text(encoding="utf-8"))

            self.assertNotIn(b"\r", markdown)
            self.assertTrue(markdown.endswith(b"\n"))
            text = markdown.decode()
            for expected in (
                SOURCE["id"],
                SOURCE["url"],
                "An internal agent at Acme",
                "2026-08-31T12:34:56Z",
            ):
                self.assertIn(expected, text)
            artifact = manifest["artifacts"]["markdown"]
            self.assertEqual(artifact["bytes"], len(markdown))
            self.assertEqual(artifact["sha256"], sha256(markdown))
            self.assertEqual(manifest["tool"], {"name": "steel", "version": "0.4.4"})
            self.assertEqual(
                result.yaml_snippet(),
                (f'capture:\n  manifest_path: "archive/sources/{SOURCE["id"]}/metadata.json"\n'),
            )
            archive_sources.validate_bundle(
                bundle / "metadata.json",
                SOURCE["id"],
                SOURCE["url"],
                repo_root=root,
            )

    def test_optional_pdf_metadata_is_exact(self) -> None:
        pdf = b"%PDF-1.7\nexample"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.capture(root, pdf_response=FakeResponse(pdf))
            bundle = root / "archive" / "sources" / SOURCE["id"]
            manifest = json.loads((bundle / "metadata.json").read_text(encoding="utf-8"))
            artifact = manifest["artifacts"]["pdf"]
            self.assertEqual((bundle / "page.pdf").read_bytes(), pdf)
            self.assertEqual(artifact["bytes"], len(pdf))
            self.assertEqual(artifact["sha256"], sha256(pdf))

    def test_atomic_cleanup_after_validation_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with (
                patch.object(
                    archive_sources,
                    "validate_bundle",
                    side_effect=archive_sources.ArchiveError("invalid bundle"),
                ),
                self.assertRaisesRegex(archive_sources.ArchiveError, "invalid bundle"),
            ):
                self.capture(root)
            archive_root = root / "archive" / "sources"
            self.assertFalse((archive_root / SOURCE["id"]).exists())
            self.assertEqual(list(archive_root.iterdir()), [])

    def test_existing_bundle_is_never_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "archive" / "sources" / SOURCE["id"]
            target.mkdir(parents=True)
            marker = target / "keep.txt"
            marker.write_text("keep", encoding="utf-8")
            runner = Mock(side_effect=AssertionError("Steel must not run"))
            with self.assertRaisesRegex(archive_sources.ArchiveError, "append-only"):
                archive_sources.capture_source(SOURCE, repo_root=root, runner=runner)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")
            runner.assert_not_called()

    def test_check_is_network_free_and_detects_corruption(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.capture(root)
            relative = f"archive/sources/{SOURCE['id']}/metadata.json"
            sources = {
                SOURCE["id"]: {
                    **SOURCE,
                    "capture": {"manifest_path": relative},
                }
            }
            with (
                patch.object(
                    archive_sources.urllib.request,
                    "urlopen",
                    side_effect=AssertionError("network call"),
                ) as urlopen,
                patch.object(
                    archive_sources.subprocess,
                    "run",
                    side_effect=AssertionError("process call"),
                ) as run,
            ):
                self.assertEqual(
                    archive_sources.check_declared_captures(sources, repo_root=root), []
                )
            urlopen.assert_not_called()
            run.assert_not_called()

            content = root / "archive" / "sources" / SOURCE["id"] / "content.md"
            content.write_text("corrupt", encoding="utf-8")
            errors = archive_sources.check_declared_captures(sources, repo_root=root)
            self.assertEqual(len(errors), 1)
            self.assertRegex(errors[0], "byte count|SHA-256")

    def test_manifest_external_archive_must_match_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.capture(root)
            bundle = root / "archive" / "sources" / SOURCE["id"]
            manifest_path = bundle / "metadata.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["external_archive_url"] = (
                "https://web.archive.org/web/20260831123456/https://example.com/article"
            )
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(archive_sources.ArchiveError, "does not match"):
                archive_sources.validate_bundle(
                    manifest_path,
                    SOURCE["id"],
                    SOURCE["url"],
                    repo_root=root,
                    archived_url="https://web.archive.org/web/20250101000000/https://example.com",
                )


class WaybackTests(unittest.TestCase):
    def test_authenticated_save_polls_to_immutable_url(self) -> None:
        opener = QueueOpener(
            FakeResponse(json.dumps({"status": "pending", "job_id": "job-1"}).encode()),
            FakeResponse(
                json.dumps(
                    {
                        "status": "success",
                        "timestamp": "20260831123456",
                    }
                ).encode()
            ),
        )
        result = archive_sources.preserve_with_wayback(
            SOURCE["url"],
            opener=opener,
            sleep=lambda _seconds: None,
            environ={"IA_ACCESS_KEY_ID": "access", "IA_SECRET_ACCESS_KEY": "secret"},
        )
        self.assertEqual(
            result,
            "https://web.archive.org/web/20260831123456/https://example.com/article",
        )
        first_request = opener.requests[0]
        self.assertEqual(first_request.get_method(), "POST")
        self.assertEqual(first_request.get_header("Authorization"), "LOW access:secret")

    def test_without_credentials_existing_capture_is_used(self) -> None:
        archived_url = "https://web.archive.org/web/20260831123456/https://example.com/article"
        payload = {
            "archived_snapshots": {
                "closest": {"available": True, "status": "200", "url": archived_url}
            }
        }
        warnings = io.StringIO()
        result = archive_sources.preserve_with_wayback(
            SOURCE["url"],
            opener=QueueOpener(FakeResponse(json.dumps(payload).encode())),
            environ={},
            warning_stream=warnings,
        )
        self.assertEqual(result, archived_url)
        self.assertIn("credentials unavailable", warnings.getvalue())

    def test_wayback_failure_is_a_redacted_warning(self) -> None:
        secret = "never-print-this-secret"
        warnings = io.StringIO()
        opener = QueueOpener(
            urllib.error.URLError("save failed"),
            urllib.error.URLError("query failed"),
        )
        result = archive_sources.preserve_with_wayback(
            SOURCE["url"],
            opener=opener,
            environ={"IA_ACCESS_KEY_ID": "access", "IA_SECRET_ACCESS_KEY": secret},
            warning_stream=warnings,
        )
        self.assertIsNone(result)
        self.assertIn("continuing locally", warnings.getvalue())
        self.assertNotIn(secret, warnings.getvalue())

    def test_yaml_snippet_includes_only_verified_wayback(self) -> None:
        archived_url = "https://web.archive.org/web/20260831123456/https://example.com/article"
        result = archive_sources.CaptureResult(
            SOURCE["id"],
            f"archive/sources/{SOURCE['id']}/metadata.json",
            archived_url,
        )
        self.assertEqual(
            result.yaml_snippet(),
            f'archived_url: "{archived_url}"\n'
            "capture:\n"
            f'  manifest_path: "archive/sources/{SOURCE["id"]}/metadata.json"\n',
        )


class CliTests(unittest.TestCase):
    def test_check_mode_rejects_network_options(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            archive_sources._parser().parse_args(["--check", "--source-id", "x"])

    def test_continue_on_error_requires_all(self) -> None:
        with (
            patch.object(archive_sources, "load_sources", return_value={}),
            contextlib.redirect_stderr(io.StringIO()),
            self.assertRaises(SystemExit),
        ):
            archive_sources.main(["--source-id", SOURCE["id"], "--continue-on-error"])


class CaptureRegressionTests(unittest.TestCase):
    def test_batch_continues_after_pdf_body_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            failed = FakeResponse(b"")
            failed.read = Mock(side_effect=TimeoutError("credential-secret"))
            opener = QueueOpener(failed, FakeResponse(b"%PDF-1.7\nfixture"))
            sources = {
                "a-source": {"id": "a-source", "url": SOURCE["url"]},
                "b-source": {"id": "b-source", "url": SOURCE["url"]},
            }
            capture = archive_sources.capture_source

            def capture_locally(source, **kwargs):
                return capture(
                    source,
                    **kwargs,
                    repo_root=root,
                    runner=scrape_runner(
                        steel_envelope(pdf_url="https://files.steel.dev/page.pdf")
                    ),
                    opener=opener,
                )

            output = io.StringIO()
            with (
                patch.object(archive_sources, "ROOT", root),
                patch.object(archive_sources, "load_sources", return_value=sources),
                patch.object(archive_sources, "steel_version", return_value="0.4.4"),
                patch.object(archive_sources, "capture_source", side_effect=capture_locally),
                contextlib.redirect_stdout(output),
            ):
                code = archive_sources.main(
                    ["--all", "--pdf", "--continue-on-error", "--delay", "0"]
                )
            summary = json.loads(output.getvalue())
            self.assertEqual(code, 1)
            self.assertEqual([row["source_id"] for row in summary["failed"]], ["a-source"])
            self.assertEqual([row["source_id"] for row in summary["captured"]], ["b-source"])
            self.assertTrue((root / "archive" / "sources" / "b-source" / "page.pdf").is_file())
            self.assertNotIn("credential-secret", output.getvalue())

    def test_wayback_header_transport_failures_preserve_local_capture(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            opener = QueueOpener(
                http.client.RemoteDisconnected("credential-secret"),
                http.client.BadStatusLine("credential-secret"),
            )
            warnings = io.StringIO()
            root = Path(directory)
            archive_sources.capture_source(
                SOURCE,
                repo_root=root,
                runner=scrape_runner(steel_envelope()),
                opener=opener,
                save_wayback=True,
                environ={"IA_ACCESS_KEY_ID": "access", "IA_SECRET_ACCESS_KEY": "credential-secret"},
                warning_stream=warnings,
                steel_version_value="0.4.4",
            )
            self.assertTrue((root / "archive" / "sources" / SOURCE["id"] / "content.md").is_file())
            self.assertNotIn("credential-secret", warnings.getvalue())

    def test_wayback_body_transport_failures_preserve_local_capture(self) -> None:
        for error_type in (
            TimeoutError,
            OSError,
            urllib.error.URLError,
            http.client.HTTPException,
            http.client.IncompleteRead,
        ):
            with self.subTest(error=error_type), tempfile.TemporaryDirectory() as directory:
                responses = [FakeResponse(b""), FakeResponse(b"")]
                for response in responses:
                    error = (
                        error_type(b"credential-secret")
                        if error_type is http.client.IncompleteRead
                        else error_type("credential-secret")
                    )
                    response.read = Mock(side_effect=error)
                warnings = io.StringIO()
                root = Path(directory)
                opener = QueueOpener(*responses)
                archive_sources.capture_source(
                    SOURCE,
                    repo_root=root,
                    runner=scrape_runner(steel_envelope()),
                    opener=opener,
                    save_wayback=True,
                    environ={
                        "IA_ACCESS_KEY_ID": "access",
                        "IA_SECRET_ACCESS_KEY": "credential-secret",
                    },
                    warning_stream=warnings,
                    steel_version_value="0.4.4",
                    captured_at=CAPTURED_AT,
                )
                bundle = root / "archive" / "sources" / SOURCE["id"]
                manifest = archive_sources.validate_bundle(
                    bundle / "metadata.json", SOURCE["id"], SOURCE["url"], repo_root=root
                )
                self.assertNotIn("external_archive_url", manifest)
                self.assertEqual(len(opener.requests), 2)
                self.assertIn("continuing locally", warnings.getvalue())
                self.assertNotIn("credential-secret", warnings.getvalue())

    def test_pdf_body_failure_is_fatal_and_redacted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            response = FakeResponse(b"")
            response.read = Mock(side_effect=TimeoutError("credential-secret"))
            with self.assertRaises(archive_sources.ArchiveError) as caught:
                archive_sources.capture_source(
                    SOURCE,
                    pdf=True,
                    repo_root=Path(directory),
                    runner=scrape_runner(
                        steel_envelope(pdf_url="https://files.steel.dev/page.pdf")
                    ),
                    opener=QueueOpener(response),
                    steel_version_value="0.4.4",
                )
            self.assertNotIn("credential-secret", str(caught.exception))
            self.assertFalse((Path(directory) / "archive" / "sources" / SOURCE["id"]).exists())

    def test_bundle_symlink_boundaries(self) -> None:
        for mode in (
            "content-sibling",
            "manifest-sibling",
            "content-external",
            "manifest-external",
            "source-sibling",
            "source-external",
            "archive-external",
            "staging-manifest",
            "staging-content",
        ):
            with (
                self.subTest(mode=mode),
                tempfile.TemporaryDirectory() as directory,
                tempfile.TemporaryDirectory() as outside,
            ):
                root = Path(directory)
                archive_sources.capture_source(
                    SOURCE,
                    repo_root=root,
                    runner=scrape_runner(steel_envelope()),
                    steel_version_value="0.4.4",
                )
                bundle = root / "archive" / "sources" / SOURCE["id"]
                sibling = bundle.parent / "sibling"
                destination = Path(outside) / "copy" if "external" in mode else sibling
                shutil.copytree(bundle, destination)
                staging = None
                if mode.startswith("source"):
                    shutil.rmtree(bundle)
                    bundle.symlink_to(destination, target_is_directory=True)
                elif mode.startswith("archive"):
                    shutil.copytree(root / "archive", Path(outside) / "archive")
                    shutil.rmtree(root / "archive")
                    (root / "archive").symlink_to(
                        Path(outside) / "archive", target_is_directory=True
                    )
                else:
                    name = "metadata.json" if "manifest" in mode else "content.md"
                    (bundle / name).unlink()
                    (bundle / name).symlink_to(destination / name)
                    if mode.startswith("staging"):
                        staging = bundle
                with self.assertRaises(archive_sources.ArchiveError):
                    archive_sources.validate_bundle(
                        bundle / "metadata.json",
                        SOURCE["id"],
                        SOURCE["url"],
                        repo_root=root,
                        bundle_dir=staging,
                    )


if __name__ == "__main__":
    unittest.main()
