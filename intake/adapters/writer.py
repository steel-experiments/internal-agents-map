# ABOUTME: Writer-model adapter for the intake pipeline (Plan 017, stages 4 and 8).
# ABOUTME: Structured output, one retry on schema violation, usage recorded per call.
"""Call the writer model with structured output and record what it returns.

The adapter is the only seam to the OpenAI Responses API. It pins the model
string, records the model string the API returns, reports token usage for the
budget ledger, and never retries on its own: one retry on a schema violation
belongs to the calling stage, an API error stops the run.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Protocol

from intake.budget import Budget

DEFAULT_MODEL = "gpt-6-sol"
DEFAULT_REASONING_EFFORT = "medium"


class WriterApiError(RuntimeError):
    """A writer-model call failed; the run stops."""


class MissingApiKeyError(RuntimeError):
    """The OpenAI API key is absent; the run cannot call the writer model."""


@dataclass(frozen=True)
class WriterResult:
    """One completed writer-model call."""

    payload: dict[str, Any]
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


class _ResponsesProtocol(Protocol):
    def create(self, **kwargs: Any) -> Any: ...


class WriterAdapter:
    """One writer-model seam with structured output."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
        reasoning_effort: str = DEFAULT_REASONING_EFFORT,
        responses: _ResponsesProtocol | None = None,
    ) -> None:
        self._api_key = api_key
        self.model = model
        self.reasoning_effort = reasoning_effort
        self._responses = responses

    def _client_responses(self) -> _ResponsesProtocol:
        if self._responses is not None:
            return self._responses
        key = self._api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise MissingApiKeyError(
                "OPENAI_API_KEY is not set; add it to .env (see docs/intake-pipeline.md)."
            )
        from openai import OpenAI  # imported lazily so offline tests need no client

        return OpenAI(api_key=key).responses

    def complete_json(
        self,
        *,
        instructions: str,
        input_text: str,
        schema: dict[str, Any],
        schema_name: str,
        budget: Budget,
    ) -> WriterResult:
        """One structured-output call; returns the parsed JSON payload."""
        try:
            response = self._client_responses().create(
                model=self.model,
                instructions=instructions,
                input=input_text,
                reasoning={"effort": self.reasoning_effort},
                text={
                    "format": {
                        "type": "json_schema",
                        "name": schema_name,
                        "schema": schema,
                        "strict": True,
                    }
                },
            )
        except Exception as error:  # the run stops on the first API error
            raise WriterApiError(f"writer-model call failed: {error}") from error
        usage = getattr(response, "usage", None)
        input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
        output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
        cost = budget.record_usage(input_tokens, output_tokens)
        model = str(getattr(response, "model", self.model))
        try:
            payload = json.loads(response.output_text)
        except (TypeError, json.JSONDecodeError) as error:
            raise WriterApiError(f"writer model returned invalid JSON: {error}") from error
        if not isinstance(payload, dict):
            raise WriterApiError("writer model returned a non-object JSON payload")
        return WriterResult(
            payload=payload,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
        )
