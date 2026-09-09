# ABOUTME: Tests for the e-mail scan that guards the public catalog.
# ABOUTME: Uses throwaway git repositories so the scan reads real tracked files.
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "catalog_check_private_data", ROOT / "scripts" / "check_private_data.py"
)
check_private_data = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = check_private_data
SPEC.loader.exec_module(check_private_data)


def address(user: str, domain: str) -> str:
    """Build an e-mail address so the scan does not flag this file."""
    return "@".join([user, domain])


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def make_repo(root: Path, files: dict[str, str | bytes]) -> None:
    git(root, "init", "-q")
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
    git(root, "add", "-A")


class ScanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_reports_email_in_tracked_file(self) -> None:
        jane = address("jane.doe+ai", "example.co.uk")
        make_repo(self.root, {"data/agents/x.yaml": f"notes: ask {jane}\n"})
        self.assertEqual(check_private_data.scan(self.root), [f"data/agents/x.yaml:1: {jane}"])

    def test_ignores_untracked_and_archive_files(self) -> None:
        press = address("press", "example.com")
        make_repo(self.root, {"archive/sources/a/page.md": f"contact: {press}\n"})
        (self.root / "research.md").write_text(address("owner", "example.com"), encoding="utf-8")
        self.assertEqual(check_private_data.scan(self.root), [])

    def test_skips_binary_files_and_handles(self) -> None:
        make_repo(
            self.root,
            {
                "docs/img.png": b"\x89PNG\xff\xfe@\xff",
                "data/agents/y.yaml": "source: https://x.com/@steel_dev posted by @niko\n",
            },
        )
        self.assertEqual(check_private_data.scan(self.root), [])

    def test_this_repository_is_clean(self) -> None:
        self.assertEqual(check_private_data.scan(ROOT), [])


if __name__ == "__main__":
    unittest.main()
