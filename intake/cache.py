# ABOUTME: Content-addressed cache for model-call stages (Plan 017, stage 6).
# ABOUTME: Keys cover every input that can change a judgment's meaning.
"""Cache Jev judgments by every input that can change them.

The key hashes the claim text and its qualifications, the capture content hash,
the selected span, the question version, and the model version. A cache hit is
free and byte-identical; an input change invalidates exactly the affected
decisions. The cache lives under ``.intake/cache/`` and is regenerable.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CACHE_ROOT = ROOT / ".intake" / "cache"


def cache_key(*parts: str) -> str:
    """Hash the cache key parts into one hexadecimal digest."""
    digest = hashlib.sha256()
    for part in parts:
        digest.update(part.encode("utf-8"))
        digest.update(b"\x00")
    return digest.hexdigest()


class JsonCache:
    """A JSON-file cache with explicit keys; reads once, writes on demand."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._entries: dict[str, Any] | None = None
        self.hits = 0

    def _load(self) -> dict[str, Any]:
        if self._entries is None:
            if self.path.is_file():
                try:
                    payload = json.loads(self.path.read_text(encoding="utf-8"))
                    self._entries = payload if isinstance(payload, dict) else {}
                except (OSError, json.JSONDecodeError):
                    self._entries = {}
            else:
                self._entries = {}
        return self._entries

    def get(self, key: str) -> Any | None:
        entries = self._load()
        if key in entries:
            self.hits += 1
        return entries.get(key)

    def put(self, key: str, value: Any) -> None:
        entries = self._load()
        entries[key] = value
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(entries, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def __contains__(self, key: str) -> bool:
        return key in self._load()


def jev_cache(path: Path | None = None) -> JsonCache:
    """The default Jev judgment cache."""
    return JsonCache(path or CACHE_ROOT / "jev.json")


def writer_cache(path: Path | None = None) -> JsonCache:
    """The default writer-response cache (stages 4 and 8)."""
    return JsonCache(path or CACHE_ROOT / "writer.json")
