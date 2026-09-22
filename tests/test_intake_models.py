from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml

from intake.models import (
    CLAIM_ID_RE,
    Claim,
    ExtractionRecord,
    RunManifest,
    StagedSource,
    compute_claim_id,
    finalize,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "intake"
SCHEMA_PATH = ROOT / "intake" / "schemas" / "extraction-record.v1.json"
SHA = "sha256:" + "a" * 64


def minimal_record(**overrides: object) -> ExtractionRecord:
    """One valid extraction record; overrides replace top-level fields."""
    payload = {
        "schema_version": 1,
        "run_id": "2026-09-22T19:40:11Z-3f9a",
        "candidate": {"company": "Example", "record_id": "example-agent"},
        "classification": {
            "approach_type": "agent",
            "deployment_stage": "deployed",
            "year": 2026,
            "domains": ["coding"],
            "rubric": {"invocation": ["interactive"], "state": "unknown", "identity": "unknown"},
            "operating_models": [
                {"scope": "task → result", "attention_boundary": "unknown", "claim_ids": ["c-x"]}
            ],
            "agent_name": "Example agent",
        },
        "sources": [
            {
                "local_id": "s1",
                "title": "Example post",
                "url": "https://example.com/post",
                "canonical_url": "https://example.com/post",
                "kind": "engineering-blog",
                "provenance_class": "first-party",
                "content_sha256": SHA,
            }
        ],
        "claims": [
            {
                "id": "c-x",
                "field": "summary",
                "text": "Example built an agent.",
                "kind": "fact",
                "provenance": "reported",
                "quotes": [
                    {
                        "source": "s1",
                        "text": "Example built an agent",
                        "lines": [3, 3],
                        "match": "exact",
                    }
                ],
                "disposition": "accept",
            }
        ],
    }
    payload.update(overrides)
    return ExtractionRecord.model_validate(payload)


class ClaimIdentityTests(unittest.TestCase):
    def test_claim_id_is_deterministic_and_content_addressed(self) -> None:
        first = compute_claim_id(SHA, "a quote", "summary")
        second = compute_claim_id(SHA, "a quote", "summary")
        self.assertEqual(first, second)
        self.assertNotEqual(first, compute_claim_id(SHA, "a quote", "key_metrics[]"))
        self.assertNotEqual(first, compute_claim_id(SHA, "another quote", "summary"))
        other_sha = "sha256:" + "b" * 64
        self.assertNotEqual(first, compute_claim_id(other_sha, "a quote", "summary"))

    def test_finalize_fills_missing_ids_and_verifies_existing_ones(self) -> None:
        record = minimal_record()
        record = record.model_copy(
            update={"claims": [record.claims[0].model_copy(update={"id": None})]}
        )
        finalized = finalize(record)
        computed = compute_claim_id(SHA, "Example built an agent", "summary")
        self.assertEqual(finalized.claims[0].id, computed)
        again = finalize(finalized)
        self.assertEqual(again.claims[0].id, computed)

    def test_finalize_rejects_an_id_that_does_not_match_its_content(self) -> None:
        record = minimal_record()
        tampered = record.model_copy(
            update={"claims": [record.claims[0].model_copy(update={"id": "c-deadbeef"})]}
        )
        with self.assertRaises(ValueError):
            finalize(tampered)


def revalidate(record: ExtractionRecord, **changes: object) -> ExtractionRecord:
    """Rebuild one record with changes, running every validator again."""
    return ExtractionRecord.model_validate(record.model_dump() | changes)


class ReferenceValidationTests(unittest.TestCase):
    def test_quote_referencing_an_unknown_source_is_rejected(self) -> None:
        record = minimal_record()
        claims = [
            claim.model_dump()
            | {"quotes": [quote.model_dump() | {"source": "s9"} for quote in claim.quotes]}
            for claim in record.claims
        ]
        with self.assertRaises(ValueError):
            revalidate(record, claims=claims)

    def test_duplicate_source_local_ids_are_rejected(self) -> None:
        record = minimal_record()
        with self.assertRaises(ValueError):
            revalidate(record, sources=[record.sources[0].model_dump()] * 2)

    def test_questions_referencing_unknown_claims_are_rejected(self) -> None:
        record = minimal_record()
        with self.assertRaises(ValueError):
            revalidate(record, questions={"purpose": {"claim_ids": ["c-missing"]}})

    def test_observation_duplicating_an_unknown_claim_is_rejected(self) -> None:
        record = minimal_record()
        claims = [
            claim.model_dump()
            | {"observation": {"duplicate_of": "c-missing", "reason": "same figure"}}
            for claim in record.claims
        ]
        with self.assertRaises(ValueError):
            revalidate(record, claims=claims)

    def test_metric_claims_must_be_metric_kind(self) -> None:
        with self.assertRaises(ValueError):
            Claim.model_validate(
                {
                    "field": "key_metrics[]",
                    "text": "95%",
                    "kind": "fact",
                    "provenance": "reported",
                    "quotes": [{"source": "s1", "text": "95%"}],
                }
            )

    def test_unknown_field_family_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Claim.model_validate(
                {
                    "field": "vibes[]",
                    "text": "text",
                    "kind": "fact",
                    "provenance": "reported",
                    "quotes": [{"source": "s1", "text": "text"}],
                }
            )

    def test_source_dates_and_urls_follow_the_authored_conventions(self) -> None:
        record = minimal_record()
        source = record.sources[0].model_dump()
        with self.assertRaises(ValueError):
            StagedSource.model_validate(source | {"published_at": "June 2026"})
        with self.assertRaises(ValueError):
            StagedSource.model_validate(source | {"url": "http://example.com/post"})


class SchemaExportTests(unittest.TestCase):
    def test_the_committed_schema_file_matches_the_models(self) -> None:
        committed = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        current = {
            "extraction_record": ExtractionRecord.model_json_schema(),
            "run_manifest": RunManifest.model_json_schema(),
        }
        self.assertEqual(committed, current)

    def test_the_golden_fixtures_parse_and_finalize(self) -> None:
        for path in sorted(FIXTURES.glob("*.extraction.yaml")):
            with self.subTest(fixture=path.name):
                record = ExtractionRecord.model_validate(
                    yaml.safe_load(path.read_text(encoding="utf-8"))
                )
                finalized = finalize(record)
                self.assertTrue(
                    all(CLAIM_ID_RE.fullmatch(claim.id or "") for claim in finalized.claims)
                )


if __name__ == "__main__":
    unittest.main()
