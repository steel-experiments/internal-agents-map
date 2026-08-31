# Source preservation

The catalog keeps the publisher URL as the canonical citation and preserves a copy of the
evidence while that URL is live. Preservation protects the audit trail when a publisher later
edits or removes a page. It does not independently verify the publisher's claims or strengthen a
source's provenance class.

## Preservation model

Each source can have three locations:

- `url` is the immutable publisher URL cited by the catalog.
- `archived_url` is an immutable external archive, normally a Wayback Machine capture.
- `capture.manifest_path` identifies a repository-owned Steel capture under
  `archive/sources/<source-id>/`.

The catalog always displays the original URL. When available, it displays the local snapshot and
Wayback capture beside the original rather than replacing it.

Capture happens during source intake. Waiting for the scheduled link check is too late: a page
that returns 404 or 410 may no longer be recoverable.

## Capture formats

Markdown is the default preserved format because it is compact, searchable, diffable, and useful
for reviewing textual evidence. A PDF is optional when layout, charts, diagrams, screenshots, or
tables materially support a catalog claim. Raw or executable HTML is not stored.

Every local capture records:

- the source ID and original and final URLs;
- the capture time in UTC;
- the successful HTTP status observed by Steel;
- the Steel version used;
- each artifact's repository path, byte count, and SHA-256 digest.

Captures are append-only. Do not overwrite a source bundle. If materially changed source content
supports new claims, add a new source record and capture it under a new source ID.

## Collection boundaries

Capture only public pages that are available without a login. Do not use stored credentials,
CAPTCHA solving, residential proxies, or other access-control bypasses for preservation. Do not
capture paywalled, private, confidential, or personal account content. Honor an explicit
`noarchive` directive and document the resulting evidence gap.

An HTTP 200 response is not sufficient by itself. Review the preserved Markdown and optional PDF
to confirm that they contain the intended source rather than an error page, consent wall,
anti-bot interstitial, or unrelated redirect.

## Link-check policy

The scheduled checker uses these outcomes:

- A healthy original passes.
- A confirmed 404 or 410 with a verified local or external archive passes with an `archived`
  warning.
- A confirmed 404 or 410 without a verified fallback fails.
- Access-controlled and temporarily unreachable originals remain warnings rather than being
  treated as missing.
- A declared local artifact that is absent, corrupt, outside its source directory, or does not
  match its recorded hash fails validation.

The workflow is read-only. It never rewrites citations or commits snapshots in response to a
network check.

## Storage and retention

Local Markdown and selected PDFs are committed under `archive/sources/`. GitHub Actions artifacts
are not archival storage because they expire. Wayback is the preferred public replay when it can
capture the page; the repository copy is the deterministic fallback.

PDFs are selective and must not exceed 10 MiB each. Review aggregate repository growth before
committing a batch of PDFs. If archive size later becomes material, move artifacts through a
separately reviewed storage migration rather than introducing Git LFS or another service ad hoc.

## Copyright, attribution, and takedown

Archived pages remain the property of their original publishers and authors. They are preserved
for citation, verification, research, and historical reference and are not relicensed under this
repository's CC BY-SA license. Every capture retains its original URL and capture metadata.

To request removal of a preserved source, open an issue in this repository identifying the source
ID and the rights or privacy concern. Maintainers should remove access to the local artifact while
preserving non-infringing catalog metadata and the original citation where appropriate.
