from __future__ import annotations

import importlib.util
import sys
import unittest
import urllib.error
from pathlib import Path
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


class LinkCheckTests(unittest.TestCase):
    def test_healthy_head_is_reported(self) -> None:
        response = MagicMock(status=200)
        response.__enter__.return_value = response
        with patch.object(check_links.urllib.request, "urlopen", return_value=response):
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


if __name__ == "__main__":
    unittest.main()
