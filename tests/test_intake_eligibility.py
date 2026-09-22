# ABOUTME: The decision policy's eligibility proposal over accepted claims.
"""Categorical eligibility: Add, Update, Needs evidence, or Out of scope."""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

from intake.eligibility import propose_eligibility
from intake.models import ExtractionRecord

ROOT = Path(__file__).resolve().parents[1]


def zup_record() -> ExtractionRecord:
    """The zup fixture: company Zup, decision update, seven accepted claims."""
    payload = yaml.safe_load(
        (ROOT / "tests" / "fixtures" / "intake" / "zup-codegen.extraction.yaml").read_text(
            encoding="utf-8"
        )
    )
    return ExtractionRecord.model_validate(payload)


def with_dispositions(record: ExtractionRecord, disposition: str) -> ExtractionRecord:
    claims = [claim.model_copy(update={"disposition": disposition}) for claim in record.claims]
    return record.model_copy(update={"claims": claims})


class EligibilityTests(unittest.TestCase):
    def test_an_unnamed_organization_needs_evidence(self) -> None:
        record = zup_record()
        # model_copy skips validation, so the empty name reaches the check.
        bare = record.model_copy(
            update={"candidate": record.candidate.model_copy(update={"company": ""})}
        )
        proposal = propose_eligibility(bare)
        self.assertEqual(proposal["decision"], "needs-evidence")
        self.assertIn("inclusion question 1", proposal["reasons"][0])

    def test_no_accepted_claims_needs_evidence(self) -> None:
        proposal = propose_eligibility(with_dispositions(zup_record(), "review"))
        self.assertEqual(proposal["decision"], "needs-evidence")
        self.assertIn("nothing establishes a build", proposal["reasons"][0])

    def test_a_writer_out_of_scope_proposal_reaches_the_person(self) -> None:
        record = zup_record()
        proposal = propose_eligibility(
            record.model_copy(
                update={
                    "candidate": record.candidate.model_copy(update={"decision": "out-of-scope"})
                }
            )
        )
        self.assertEqual(proposal["decision"], "out-of-scope")
        self.assertEqual(proposal["writer_decision"], "out-of-scope")
        self.assertIn("names which inclusion rule fails", proposal["reasons"][0])

    def test_established_claims_carry_the_identity_decision(self) -> None:
        proposal = propose_eligibility(zup_record())
        self.assertEqual(proposal["decision"], "update")
        self.assertEqual(proposal["writer_decision"], "update")
        self.assertIn("10 accepted claims", proposal["reasons"][0])
        self.assertIn("describes the implementation or the use", proposal["reasons"][1])

    def test_no_use_claim_leaves_question_three_to_the_person(self) -> None:
        record = zup_record()
        claims = [
            claim.model_copy(update={"disposition": "review"})
            if claim.field != "summary"
            else claim
            for claim in record.claims
        ]
        record = record.model_copy(update={"claims": claims, "questions": None})
        proposal = propose_eligibility(record)
        self.assertEqual(proposal["decision"], "update")
        self.assertIn("a person confirms it against the sources", proposal["reasons"][1])


if __name__ == "__main__":
    unittest.main()
