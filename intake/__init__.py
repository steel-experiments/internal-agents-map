# ABOUTME: Source intake pipeline package (Plan 017); stages run as separate commands.
# ABOUTME: Drafts a record from captured sources; a person reviews, edits, and merges.
"""Turn captured sources into a reviewed catalog record draft."""

from intake.models import (
    SCHEMA_VERSION,
    Claim,
    ExtractionRecord,
    RunManifest,
    compute_claim_id,
    finalize,
)

__version__ = "0.1.0"

__all__ = [
    "SCHEMA_VERSION",
    "Claim",
    "ExtractionRecord",
    "RunManifest",
    "__version__",
    "compute_claim_id",
    "finalize",
]
