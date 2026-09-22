# ABOUTME: Import shim that loads the catalog builder's validators once for the package.
# ABOUTME: The pipeline reuses build.py's rules instead of implementing them a second time.
"""Load ``scripts/build.py`` and ``scripts/archive_sources.py`` for reuse."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
BUILD_NAME = "catalog_build"
ARCHIVER_NAME = "catalog_archive_sources"


def _load_script(module_name: str, relative: Path) -> ModuleType:
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, ROOT / relative)
    if spec is None or spec.loader is None:  # pragma: no cover - unreachable on a valid install
        raise ImportError(f"could not load {relative}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_build() -> ModuleType:
    """Import ``scripts/build.py`` as a module and return it."""
    return _load_script(BUILD_NAME, Path("scripts") / "build.py")


def load_archiver() -> ModuleType:
    """Import ``scripts/archive_sources.py`` as a module and return it."""
    return _load_script(ARCHIVER_NAME, Path("scripts") / "archive_sources.py")


def die_on_invalid(record: dict[str, Any], stem: str) -> None:
    """Validate one rendered draft against the catalog's own record rules.

    ``record`` is the rendered mapping; ``stem`` is the filename the draft will use.
    Raises ``SystemExit`` through the builder's ``die`` on any violation.
    """

    build = load_build()
    build.validate_record(record, Path(f"{stem}.yaml"), set())
