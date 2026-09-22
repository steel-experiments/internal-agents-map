# ABOUTME: Import shim that loads the catalog builder's validators once for the package.
# ABOUTME: The pipeline reuses build.py's rules instead of implementing them a second time.
"""Load ``scripts/build.py`` the same way the coverage script and the tests do."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
MODULE_NAME = "catalog_build"


def load_build() -> ModuleType:
    """Import ``scripts/build.py`` as a module and return it."""
    if MODULE_NAME in sys.modules:
        return sys.modules[MODULE_NAME]
    spec = importlib.util.spec_from_file_location(MODULE_NAME, ROOT / "scripts" / "build.py")
    if spec is None or spec.loader is None:  # pragma: no cover - unreachable on a valid install
        raise ImportError("could not load scripts/build.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


def die_on_invalid(record: dict[str, Any], stem: str) -> None:
    """Validate one rendered draft against the catalog's own record rules.

    ``record`` is the rendered mapping; ``stem`` is the filename the draft will use.
    Raises ``SystemExit`` through the builder's ``die`` on any violation.
    """

    build = load_build()
    build.validate_record(record, Path(f"{stem}.yaml"), set())
