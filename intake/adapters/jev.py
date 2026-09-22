# ABOUTME: Jev adapter for the intake pipeline (Plan 017, stages 3, 6, and 9).
# ABOUTME: Direct HTTP, persistent connection, timeout, no automatic retry.
"""Ask Jev typed questions over supplied state.

Jev answers choice and yes/no (``noul``) questions about a short passage
cluster; it never produces text and never finds a passage it was not given. The
adapter follows the Plan 016 runner: one persistent HTTPS connection, a
timeout, no automatic retry (the run stops on the first error), and the budget
reserved for every attempted request.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from intake.budget import Budget

MODEL = "jev-1.13.0"
API_HOST = "api.typesafe.ai"
API_PATH = "/v1/systemone"
# Published Jev price at planning time: $0.042 per million input tokens.
PRICE_PER_MTOK = 0.042
# Reserve the documented maximum input charge for every attempted request.
MAX_REQUEST_TOKENS = 65_536
WORST_CASE_USD = MAX_REQUEST_TOKENS * PRICE_PER_MTOK / 1_000_000


class JevApiError(RuntimeError):
    """A Jev request failed; the run stops. Contains no credentials."""


class MissingApiKeyError(RuntimeError):
    """The TypeSafe API key is absent; the run cannot call Jev."""


@dataclass(frozen=True)
class JevAnswer:
    """One question's answer: a choice with probabilities, or a noul value."""

    type: str
    choice: str | None = None
    probabilities: dict[str, float] | None = None
    noul: float | None = None

    def probability_of(self, label: str) -> float:
        if self.type == "noul":
            return self.noul or 0.0
        return (self.probabilities or {}).get(label, 0.0)


@dataclass(frozen=True)
class JevResult:
    """One completed Jev request."""

    answers: dict[str, JevAnswer]
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    cache_hit: bool


class JevAdapter:
    """One Jev seam over a persistent connection."""

    def __init__(self, api_key: str | None = None, connection: Any = None) -> None:
        self._api_key = api_key
        self._connection = connection

    def _connect(self) -> Any:
        if self._connection is not None:
            return self._connection
        import http.client
        import os

        key = self._api_key or os.environ.get("TYPESAFE_API_KEY")
        if not key:
            raise MissingApiKeyError(
                "TYPESAFE_API_KEY is not set; add it to .env (see docs/intake-pipeline.md)."
            )
        return http.client.HTTPSConnection(API_HOST, timeout=20)

    def ask(
        self,
        *,
        state: dict[str, Any],
        questions: dict[str, dict[str, Any]],
        budget: Budget,
    ) -> JevResult:
        """One request; every answer's shape is validated before returning."""
        budget.reserve_jev_request()
        payload = {"model": MODEL, "state": state, "questions": questions}
        connection = self._connect()
        try:
            connection.request(
                "POST",
                API_PATH,
                json.dumps(payload, ensure_ascii=False).encode(),
                {
                    "Authorization": "Bearer " + self._authorization(),
                    "Content-Type": "application/json",
                },
            )
            response = connection.getresponse()
            raw = response.read()
        except Exception as error:  # no automatic retry; the run stops
            raise JevApiError(f"Jev request failed: {type(error).__name__}") from error
        if response.status != 200:
            raise JevApiError(f"Jev returned HTTP {response.status}; no automatic retry")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as error:
            raise JevApiError(f"Jev returned malformed JSON: {error}") from error
        answers = _validate_answers(parsed, questions)
        usage = parsed.get("usage") or {}
        input_tokens = int(usage.get("input_tokens", 0) or 0)
        output_tokens = int(usage.get("output_tokens", 0) or 0)
        cost = budget.record_jev_usage(input_tokens)
        model = str(parsed.get("model") or MODEL)
        return JevResult(
            answers=answers,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
            cache_hit=False,
        )

    def _authorization(self) -> str:
        import os

        key = self._api_key or os.environ.get("TYPESAFE_API_KEY")
        if not key:
            raise MissingApiKeyError("TYPESAFE_API_KEY is not set")
        return key


def _validate_answers(
    parsed: dict[str, Any], questions: dict[str, dict[str, Any]]
) -> dict[str, JevAnswer]:
    answers = parsed.get("answers")
    if not isinstance(answers, dict) or set(answers) != set(questions):
        raise JevApiError("Jev answer keys differ from the question keys")
    result: dict[str, JevAnswer] = {}
    for question_id, answer in answers.items():
        if not isinstance(answer, dict):
            raise JevApiError(f"Jev answer {question_id!r} is not an object")
        answer_type = answer.get("type")
        if answer_type == "noul":
            value = answer.get("noul")
            if (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                or not 0 <= value <= 1
            ):
                raise JevApiError(f"Jev noul answer {question_id!r} is invalid")
            result[question_id] = JevAnswer(type="noul", noul=float(value))
        elif answer_type == "choice":
            probabilities = answer.get("probabilities")
            if not isinstance(probabilities, dict) or not probabilities:
                raise JevApiError(f"Jev choice answer {question_id!r} lacks probabilities")
            for label, probability in probabilities.items():
                if (
                    not isinstance(probability, (int, float))
                    or isinstance(probability, bool)
                    or not 0 <= probability <= 1
                ):
                    raise JevApiError(
                        f"Jev choice answer {question_id!r} has an invalid probability"
                    )
            choice = answer.get("choice")
            if choice is not None and choice not in probabilities:
                raise JevApiError(f"Jev choice answer {question_id!r} names an unlisted label")
            result[question_id] = JevAnswer(
                type="choice",
                choice=choice,
                probabilities={k: float(v) for k, v in probabilities.items()},
            )
        else:
            raise JevApiError(f"Jev answer {question_id!r} has an unknown type")
    return result
