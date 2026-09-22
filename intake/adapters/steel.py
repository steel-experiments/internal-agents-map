# ABOUTME: Steel Python SDK adapter for the intake pipeline (Plan 017, stage 1).
# ABOUTME: Runs the archiver's page checks on the SDK response; the CLI path is untouched.
"""Scrape one URL with the Steel Python SDK and validate it like the archiver does.

The SDK returns the same scrape payload as the CLI, plus the page metadata
(published time, language, canonical URL) that the CLI envelope discards. The
adapter converts the response to the archiver's data shape and runs the
archiver's own page checks, so an interstitial page, an error page, a
``noarchive`` declaration, or a suspiciously short body fails exactly as it
would in ``scripts/archive_sources.py``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Protocol

from intake.catalog import load_archiver

DEFAULT_DELAY_MS = 1000


class MissingApiKeyError(RuntimeError):
    """The Steel API key is absent; the run cannot capture pages."""


@dataclass(frozen=True)
class ScrapedPage:
    """One validated scrape: the archiver's result plus the page metadata."""

    markdown: str
    final_url: str
    title: str
    http_status: int
    pdf_url: str | None
    published_at: str | None
    language: str | None
    canonical_url: str | None
    description: str | None


class _ScrapeResponse(Protocol):
    def model_dump(self, *, by_alias: bool = ...) -> dict[str, Any]: ...


def _response_data(response: _ScrapeResponse) -> dict[str, Any]:
    """Convert one SDK response to the archiver's data mapping."""
    data = response.model_dump(by_alias=True, exclude_none=True)
    return data


class SteelSdkAdapter:
    """Scrape through the Steel Python SDK with the archiver's page checks."""

    def __init__(self, api_key: str | None = None, client_factory: Any = None) -> None:
        self._api_key = api_key
        self._client_factory = client_factory

    def _client(self) -> Any:
        key = self._api_key or os.environ.get("STEEL_API_KEY")
        if not key:
            raise MissingApiKeyError(
                "STEEL_API_KEY is not set; add it to .env (see docs/intake-pipeline.md)."
            )
        if self._client_factory is not None:
            return self._client_factory(key)
        import steel  # imported lazily so offline tests never need the package

        return steel.Client(api_key=key)

    def scrape(
        self, url: str, *, pdf: bool = False, delay_ms: int = DEFAULT_DELAY_MS
    ) -> ScrapedPage:
        """Scrape one URL and return the validated page."""
        archiver = load_archiver()
        client = self._client()
        response = client.scrape(
            url=url,
            format=["markdown"],
            pdf=pdf,
            delay=delay_ms,
        )
        data = _response_data(response)
        result = archiver._validate_scraped_page(data, include_pdf=pdf)
        metadata = data.get("metadata") or {}
        return ScrapedPage(
            markdown=result.markdown,
            final_url=result.final_url,
            title=result.title,
            http_status=result.http_status,
            pdf_url=result.pdf_url,
            published_at=metadata.get("publishedTime"),
            language=metadata.get("language"),
            canonical_url=metadata.get("canonical") or metadata.get("ogUrl"),
            description=metadata.get("description") or metadata.get("ogDescription"),
        )
