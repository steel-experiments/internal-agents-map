# Plan 001: Preserve sources proactively and use verified archive fallbacks

> **Executor instructions**: Follow this plan step by step. Run every verification command
> and confirm the expected result before moving to the next step. If anything in the
> "STOP conditions" section occurs, stop and report; do not improvise. When done, update the
> status row for this plan in `plans/README.md`, unless a reviewer dispatched you and said they
> maintain the index.
>
> **Drift check (run first)**:
>
> ```bash
> git diff --stat e943ed1..HEAD -- \
>   scripts/build.py scripts/check_links.py scripts/archive_sources.py \
>   tests/test_build.py tests/test_check_links.py tests/test_archive_sources.py \
>   data/schema.md templates/agent.yaml CONTRIBUTING.md README.md \
>   .github/workflows/validate.yml .github/workflows/links.yml \
>   .github/pull_request_template.md .claude/skills/add-agent-from-url \
>   docs/source-preservation.md archive data/agents docs/landscape.md data/agents.json
> ```
>
> If an in-scope file changed since this plan was written, compare the "Current state"
> excerpts against the live code before proceeding. A semantic mismatch is a STOP condition.

## Status

- **Priority**: P1
- **Effort**: L (multi-day, including migration and review of preserved content)
- **Risk**: MED (schema/export changes, network handling, third-party-content policy, bulk data)
- **Depends on**: none
- **Category**: direction
- **Planned at**: commit `e943ed1`, 2026-08-31
- **Completed at**: 2026-08-31

## Why this matters

The catalog's claims depend on public sources that publishers may legitimately edit or remove.
The weekly checker currently discovers that loss only after the page is gone, when neither Steel
nor the Wayback Machine may be able to recover it. A confirmed missing URL therefore breaks CI
and can leave an otherwise legitimate catalog record without auditable evidence.

This change captures evidence while a source is live, preserves the publisher URL as immutable
provenance, and exposes explicit local and Wayback copies beside it. A missing original passes the
scheduled check only when a verified preserved copy exists. The workflow must never fabricate a
snapshot from a 404 page or silently rewrite the original citation.

## Chosen design

These decisions are part of the plan and should not be reopened during implementation unless a
STOP condition applies:

1. `source.url` remains the immutable original publisher URL. Do not add a redundant
   `original_url` field and do not replace `url` with an archive.
2. `source.canonical_url` keeps its current meaning: the normalized publisher URL after redirects
   and tracking removal.
3. `source.archived_url` means the preferred external archive, normally an immutable Wayback URL.
4. A new optional `source.capture` map points to a repository-owned JSON manifest. The manifest
   describes a Steel Markdown snapshot and an optional PDF, with retrieval metadata and SHA-256
   hashes.
5. Repository layout is deterministic and one capture is immutable per source ID:

   ```text
   archive/sources/<source-id>/metadata.json
   archive/sources/<source-id>/content.md
   archive/sources/<source-id>/page.pdf        # optional
   ```

   If materially different source content must support new claims later, add a new source record
   with a new source ID instead of overwriting the old capture.
6. Markdown is the default local artifact. PDF is opt-in only when layout, diagrams, screenshots,
   or tables materially support a claim. Do not store raw or executable HTML in version 1.
7. The generated catalog always shows the original citation plus available `snapshot` and
   `Wayback` links. Scheduled CI remains read-only and never commits link rewrites.
8. Link-check result policy:
   - live original: pass;
   - confirmed 404/410 original plus valid local or external archive: warning/pass as `archived`;
   - confirmed 404/410 original without a valid fallback: fail;
   - blocked or transiently unreachable original: preserve the existing warning behavior;
   - missing, corrupt, path-escaping, or hash-mismatched declared artifact: fail.
9. Capture only pages available without a login. Do not use stored credentials, CAPTCHA solving,
   or residential proxies for this archival workflow. Honor an explicit `noarchive` directive and
   record it as a reviewed exception instead of bypassing it.
10. Keep the Markdown captures in Git. Do not use expiring GitHub Actions artifacts as the archive.
    Cap an individual PDF at 10 MiB and review aggregate repository growth before committing PDFs.

## Current state

Relevant files and behavior:

- `data/schema.md:101-119` documents `archived_url` and `content_fingerprint` as optional source
  fields, but neither field has defined behavior and neither is used by any current source.
- `scripts/build.py:74-90` allows those dormant fields in `SOURCE_FIELDS`.
- `scripts/build.py:288-325` validates the required source fields but does not validate an archive
  URL, fingerprint, timestamp, artifact path, or artifact content.
- `scripts/build.py:830-837` renders every source title directly to `source["url"]` and has no
  preserved-copy link.
- `scripts/build.py:842-914` spreads source fields into `data/agents.json` and hard-codes export
  schema version 3.
- `scripts/check_links.py:32-40` discovers every tracked Markdown file. Without an exclusion,
  committed article snapshots would recursively add all links inside those articles to CI.
- `scripts/check_links.py:75-90` flattens source URLs and general Markdown URLs into one set, losing
  the original/archive relationship required for fallback behavior.
- `scripts/check_links.py:93-124` confirms a `HEAD` 404 with a ranged `GET`, but does not treat 410
  as confirmed removal.
- `scripts/check_links.py:127-159` fails every confirmed missing URL, regardless of whether a
  preserved copy exists.
- `.github/workflows/links.yml:8-20` correctly has only `contents: read`; keep it read-only.
- `.github/workflows/validate.yml:20-25` already runs build validation and unit tests, so archive
  integrity can be added without introducing a secret-bearing capture step.
- `.claude/skills/add-agent-from-url/SKILL.md:22-42` fetches and extracts source facts, while
  lines 95-120 write and verify a new record. It currently does not preserve the fetched source.
- `README.md:123-126` applies CC BY-SA 4.0 to repository content/data. Third-party archived content
  must be explicitly excluded from that grant and retain its original ownership and attribution.
- `data/agents/atlassian-dot.yaml:30-39` is the current failure case: its only source is now a
  confirmed 404 and no pre-removal Steel or Wayback capture exists.

Existing patterns to match:

```python
# scripts/build.py:288-325
def validate_source(source: Any, filename: str, seen: set[str]) -> None:
    ...
    if not source["url"].startswith("https://"):
        die(f"{filename}: source {source_id!r} must use an HTTPS URL.")
```

```python
# scripts/check_links.py:25-29
@dataclass(frozen=True)
class LinkResult:
    url: str
    status: Literal["healthy", "missing", "blocked", "unreachable"]
    detail: str
```

```python
# tests/test_check_links.py:32-39
with patch.object(
    check_links.urllib.request,
    "urlopen",
    side_effect=[http_error(404), http_error(404)],
):
    result = check_links.check_url("https://example.com")
self.assertEqual(result.status, "missing")
```

Use the existing standard-library-first style, `unittest`, dataclasses, `urllib`, `pathlib`, and
100-character Ruff line length. Do not add a Python dependency solely for this feature.

## Commands you will need

| Purpose | Command | Expected on success |
| --- | --- | --- |
| Sync | `uv sync --locked` | exit 0; lock remains unchanged |
| Build | `uv run --locked python scripts/build.py` | generated files updated; exit 0 |
| Build check | `uv run --locked python scripts/build.py --check` | validates all approaches; exit 0 |
| Archive integrity | `uv run --locked python scripts/archive_sources.py --check` | every declared capture valid; exit 0 |
| Unit tests | `uv run --locked python -m unittest discover -s tests` | all tests pass |
| Lint | `uv run --locked ruff check .` | exit 0, no findings |
| Format | `uv run --locked ruff format --check .` | exit 0, all files formatted |
| Local links | `uv run --locked python scripts/check_links.py --local` | exit 0 |
| External links | `uv run --locked python scripts/check_links.py` | exit 0; warnings allowed, no unpreserved missing URL |
| Patch hygiene | `git diff --check` | no output; exit 0 |

The verified baseline at `e943ed1` is 40 approaches, 22 passing tests, current generated files,
clean Ruff checks, and a passing local-link check.

## Suggested executor toolkit

- Use the installed Steel CLI and inspect its live contract with `steel describe scrape --json`
  before coding the response parser.
- Steel's official browser-tools documentation explains that Markdown is inline at
  `content.markdown`, while bundled PDF output is a hosted URL that must be downloaded:
  <https://docs.steel.dev/overview/browser-tools/overview>.
- Steel's CLI reference is at
  <https://github.com/steel-dev/cli/blob/main/docs/cli-reference.md>.
- Internet Archive's Save Page Now behavior and limitations are documented at
  <https://archivesupport.zendesk.com/hc/en-us/articles/360001513491-Save-Pages-in-the-Wayback-Machine>.
- Do not depend on GitHub workflow artifacts for retention; public-repository artifacts have a
  finite retention window:
  <https://docs.github.com/en/organizations/managing-organization-settings/configuring-the-retention-period-for-github-actions-artifacts-and-logs-in-your-organization>.

## Scope

**In scope** (the only files or path families the executor may modify):

- `scripts/archive_sources.py` (create)
- `scripts/build.py`
- `scripts/check_links.py`
- `tests/test_archive_sources.py` (create)
- `tests/test_build.py`
- `tests/test_check_links.py`
- `data/schema.md`
- `templates/agent.yaml`
- `docs/source-preservation.md` (create)
- `archive/README.md` (create)
- `archive/sources/**` (created by reviewed captures)
- `archive/backfill-report.json` (temporary audit output; commit only after sanitization/review)
- `CONTRIBUTING.md`
- `README.md`
- `.github/pull_request_template.md`
- `.github/workflows/validate.yml`
- `.github/workflows/links.yml` only if output annotations need a static change; do not broaden
  its permissions
- `.claude/skills/add-agent-from-url/SKILL.md`
- `.claude/skills/add-agent-from-url/evals/evals.json`
- `data/agents/*.yaml` during the reviewed backfill
- generated `docs/landscape.md`, `data/agents.json`, `docs/patterns.md`,
  `docs/adoption-lessons.md`, and the generated section of `README.md`

**Out of scope** (do not touch):

- `pyproject.toml` and `uv.lock`: use the standard library and the Steel executable.
- `LICENSE`: do not rewrite legal license text. Clarify the snapshot carve-out in README and the
  archive policy, then obtain maintainer/legal review before bulk publication.
- GitHub Releases, Git LFS, Pages, or a new object-storage service.
- Authenticated, paywalled, private, or confidential pages.
- Steel credentials/profiles, CAPTCHA solving, stealth, or proxy configuration.
- Raw HTML or screenshots in the first version.
- A workflow that commits directly to `main` or opens bot PRs after a link failure.
- Reconstructing the missing Atlassian article from search-engine snippets.

## Git workflow

- Branch: `advisor/001-source-preservation`
- Use logical Conventional Commit messages matching recent history, for example:
  - `feat(archive): add source capture model`
  - `ci(links): accept verified archive fallbacks`
  - `data(archive): backfill source snapshots`
- Keep capture-tooling/link-check changes separate from the large data backfill so reviewers can
  inspect logic without binary or bulk-content noise.
- Do not push or open a pull request unless the operator explicitly instructs it.

## Steps

### Step 1: Define the preservation and ownership contract

Create `docs/source-preservation.md` and `archive/README.md`. Document:

- the immutable meanings of `url`, `canonical_url`, and `archived_url`;
- proactive capture at source intake, never only after a failed check;
- Markdown as the default artifact, PDF as selective, and raw HTML as unsupported;
- the deterministic bundle layout and append-only rule;
- original publisher attribution, capture timestamp, final URL, and hashes;
- no login/paywall/private-content capture and respect for `noarchive`;
- snapshots preserve evidence but do not strengthen provenance or independently verify a claim;
- third-party snapshots retain the publisher's copyright and are not relicensed under the
  repository's CC BY-SA declaration;
- a contact/takedown path appropriate for this repository;
- Wayback as the preferred public replay and the local Steel capture as the repository fallback;
- why GitHub Actions artifacts are not permanent storage.

Update the `README.md` license section with one sentence pointing to `archive/README.md` and
excluding preserved third-party snapshots from the repository's CC BY-SA content grant. Do not
alter `LICENSE` itself.

**Verify**:

```bash
rg -n "immutable|Wayback|Markdown|PDF|noarchive|copyright|takedown" \
  docs/source-preservation.md archive/README.md README.md
```

Expected: each policy topic is present, and `git diff -- LICENSE` has no output.

### Step 2: Add an explicit capture manifest to the source schema

Add optional `capture` to `SOURCE_FIELDS` in `scripts/build.py`. Its version-1 authored shape is:

```yaml
archived_url: "https://web.archive.org/web/<timestamp>/<original-url>"
capture:
  manifest_path: "archive/sources/company-agent-source-1/metadata.json"
```

The JSON manifest at that path must have this exact conceptual schema:

```json
{
  "schema_version": 1,
  "source_id": "company-agent-source-1",
  "original_url": "https://example.com/article",
  "final_url": "https://example.com/article",
  "captured_at": "2026-08-31T12:34:56Z",
  "http_status": 200,
  "tool": {"name": "steel", "version": "0.4.4"},
  "artifacts": {
    "markdown": {
      "path": "archive/sources/company-agent-source-1/content.md",
      "sha256": "sha256:<64 lowercase hex characters>",
      "bytes": 12345
    }
  }
}
```

An optional `pdf` artifact has the same `path`, `sha256`, and `bytes` keys. The manifest may also
contain `external_archive_url`; when present it must exactly equal the source's `archived_url`.

Implement validation in `scripts/build.py` with small dedicated helpers near `validate_source()`:

- `archived_url`, when present, is a non-empty HTTPS URL;
- `capture` is a map with exactly `manifest_path`;
- paths are POSIX, repository-relative, contain no `..`, resolve beneath `archive/sources/`, and
  follow `archive/sources/<source-id>/...`;
- the manifest file exists, parses as JSON, has no unexpected/missing keys, names the same source
  ID and original URL, reports a 2xx HTTP status, and uses an RFC 3339 UTC timestamp;
- `final_url` is HTTPS;
- the tool name is `steel` and its version is non-empty;
- Markdown is mandatory, non-empty, and its actual byte count and SHA-256 match the manifest;
- optional PDF exists, is at most 10 MiB, begins with `%PDF-`, and matches byte count/SHA-256;
- artifact paths remain inside the same source bundle;
- a source may temporarily have neither archive field during migration, but if it declares either
  field that declaration must be completely valid.

Remove the unused `content_fingerprint` field from the documented schema and `SOURCE_FIELDS`; the
per-artifact hashes replace it. If repository drift reveals actual uses, STOP instead of silently
migrating them.

In `normalize()`, resolve the manifest and emit its capture metadata on the normalized source.
Bump `schema_version` from 3 to 4 and update tests that assert the version.

Add schema examples to `data/schema.md` and `templates/agent.yaml`.

Extend `tests/test_build.py` with temporary-directory fixtures covering:

- a valid Markdown-only capture;
- a valid Markdown+PDF capture;
- invalid HTTPS/archive URL;
- malformed RFC 3339 timestamp;
- source ID or original URL mismatch;
- absolute path and `..` traversal rejection;
- missing/empty Markdown;
- byte-count and SHA mismatch;
- invalid/oversized PDF;
- normalized schema version 4 and capture metadata.

**Verify**:

```bash
uv run --locked python -m unittest tests.test_build
```

Expected: all build tests pass, including the new capture-validation cases.

### Step 3: Implement append-only Steel capture tooling

Create `scripts/archive_sources.py` with these modes:

```text
archive_sources.py --source-id <id> [--pdf] [--delay <ms>] [--save-wayback]
archive_sources.py --all [--continue-on-error] [--delay <ms>] [--save-wayback]
archive_sources.py --check
```

Required behavior:

1. Load `data/agents/*.yaml`, enforce a unique source ID, and use the source's immutable `url`.
2. Invoke Steel as an argument array, never through a shell. Inspect the installed contract first,
   then call the equivalent of:

   ```bash
   steel --json scrape "$url" --format markdown
   ```

   Add `--pdf` only when requested. Normalize the CLI envelope explicitly instead of guessing.
3. Reject a non-2xx `metadata.statusCode`, missing/short Markdown, an obvious error/interstitial
   title, or an explicit `noarchive` directive. Never save an error page as evidence.
4. Add a short attribution header to `content.md` containing the source ID, original URL, final URL,
   title, and UTC capture timestamp. Hash the exact final committed bytes after newline
   normalization.
5. When `--pdf` is requested, immediately download the hosted Steel PDF URL with a byte limit,
   require `%PDF-`, reject files over 10 MiB, and hash the downloaded bytes. Do not rely on the
   hosted URL as the only copy.
6. Write `content.md`, optional `page.pdf`, and `metadata.json` into a temporary sibling directory;
   validate the complete bundle; then atomically rename it to
   `archive/sources/<source-id>/`. On any failure, leave no partial target directory.
7. Refuse to overwrite an existing bundle. Do not implement `--force`. The archive is append-only.
8. `--save-wayback` is optional. Use documented Save Page Now authentication from environment
   variables, never CLI arguments, and never log secret values. Poll for the immutable capture URL.
   A Wayback failure is a warning when the Steel bundle succeeded. Without credentials, query for
   an existing capture and otherwise continue with the local bundle.
9. Print the exact YAML snippet the contributor must add:

   ```yaml
   archived_url: "..." # only when verified
   capture:
     manifest_path: "archive/sources/<source-id>/metadata.json"
   ```

   Do not round-trip entire agent YAML files through `yaml.safe_dump`; that would cause unrelated
   formatting churn.
10. `--all` processes only uncaptured sources, uses bounded sequential/rate-limited requests, and
    writes a machine-readable summary to stdout. `--continue-on-error` records failures without
    pretending they were captured.
11. `--check` performs no network calls. It validates every declared capture using the same
    manifest/hash/path rules and exits nonzero on any mismatch.

Create `tests/test_archive_sources.py` using mocks and temporary directories. Test:

- source lookup and duplicate/missing ID errors;
- Steel success response parsing;
- malformed JSON and missing response fields;
- non-2xx, empty content, block/interstitial, and `noarchive` rejection;
- attribution header and deterministic newline normalization;
- valid PDF download, invalid magic bytes, oversize rejection, and truncated download;
- exact SHA-256 and byte counts;
- atomic success and cleanup after failure;
- overwrite refusal;
- Wayback success, failure-as-warning, and secret redaction;
- `--check` is network-free and detects corruption.

**Verify**:

```bash
uv run --locked python -m unittest tests.test_archive_sources
uv run --locked ruff check scripts/archive_sources.py tests/test_archive_sources.py
uv run --locked ruff format --check scripts/archive_sources.py tests/test_archive_sources.py
```

Expected: all new tests pass; Ruff reports no issues; no real Steel or Wayback request occurs in
tests.

### Step 4: Render preserved copies without replacing provenance

Extract a `render_source_reference(source)` helper in `scripts/build.py` and use it from
`render_landscape()`.

For a captured and externally archived source, render the equivalent of:

```markdown
[Source title](https://publisher.example/article)
([snapshot](../archive/sources/source-id/content.md),
[Wayback](https://web.archive.org/web/...), captured 2026-08-31)
```

Keep the existing `(kind; provenance_class; role)` detail. Omit unavailable links cleanly:

- no capture and no Wayback: current original-only rendering;
- local capture only: original plus snapshot and date;
- Wayback only: original plus Wayback;
- both: original plus both fallbacks.

Add tests in `tests/test_build.py` for all four cases. Ensure `docs/landscape.md` uses a local path
that resolves correctly from `docs/`.

**Verify**:

```bash
uv run --locked python -m unittest tests.test_build
uv run --locked python scripts/build.py
uv run --locked python scripts/check_links.py --local
```

Expected: tests pass, generated files update, and every rendered local snapshot link resolves.

### Step 5: Make the link checker archive-aware

Refactor `scripts/check_links.py` so catalog sources are structured targets rather than flattened
URLs. Add a frozen `SourceTarget`/`SourceResult` dataclass containing at least source ID, original
URL, optional external archive URL, and optional local artifact path/result.

Collection rules:

- load catalog source records first and retain original/archive/capture association;
- collect general Markdown URLs separately;
- subtract catalog original/archive URLs from the general set so generated catalog links are not
  checked a second time without fallback context;
- exclude tracked files beneath `archive/` from both local-link traversal and external-link
  discovery; archived article links are historical content, not maintained project links;
- still check that project documentation links to an existing snapshot file.

HTTP rules:

- keep the `HEAD`, then ranged-`GET` confirmation behavior;
- treat confirmed 410 like confirmed 404;
- check a declared external archive as its own HTTP target;
- if the original is missing and either the verified local artifact exists or external archive is
  healthy, return composite status `archived`, print a warning, and do not add an error;
- if the original is missing and no verified fallback works, fail;
- if the original is healthy but a declared fallback is broken/corrupt, fail archive integrity in
  local validation and emit an external-archive warning for transient remote failure;
- retain blocked/unreachable warnings without classifying them as missing;
- report counts for `healthy`, `archived`, `missing`, `blocked`, and `unreachable`.

Do not let `check_links.py` mutate YAML, generated Markdown, or workflow permissions.

Extend `tests/test_check_links.py` with:

- confirmed 410;
- missing original + valid local snapshot = archived/pass;
- missing original + healthy Wayback only = archived/pass;
- missing original + no fallback = fail;
- missing original + corrupt/missing declared local snapshot = fail;
- blocked/unreachable original remains warning;
- healthy original + unavailable Wayback behavior;
- catalog/Markdown de-duplication;
- `archive/**` Markdown excluded from recursive discovery;
- normal project Markdown missing links still fail.

Refactor `main()` just enough to inject mocked URL results in tests; do not require real networking
for policy tests.

**Verify**:

```bash
uv run --locked python -m unittest tests.test_check_links
uv run --locked python scripts/check_links.py --local
```

Expected: tests pass and local links pass without crawling links inside archived source content.

### Step 6: Integrate capture into intake and validation

Update contributor-facing files:

- `CONTRIBUTING.md`: after adding a source record and before summarizing claims, run
  `archive_sources.py --source-id <id>`, review the captured Markdown, add the emitted capture
  fields, then build. Explain `--pdf`, `--save-wayback`, and `--check`.
- `templates/agent.yaml`: include commented `archived_url` and `capture.manifest_path` examples.
- `.github/pull_request_template.md`: add checks that preservation was attempted, the captured
  content was reviewed against the original, no private/paywalled content was included, and the
  contributor has the right to submit the snapshot.
- `.claude/skills/add-agent-from-url/SKILL.md`: on the Add path, capture every accepted source while
  it is still reachable, before claims are finalized. A capture failure must stop the automated
  Add path and report a border case; it must not weaken validation or save an error page.
- `.claude/skills/add-agent-from-url/evals/evals.json`: update the Add-path expectation to require a
  reviewed capture and archive metadata; exclusion/border-case paths should not create captures
  unless their source is being retained as catalog evidence.
- `.github/workflows/validate.yml`: add
  `uv run --locked python scripts/archive_sources.py --check`. This check is local/read-only and
  requires no Steel or Wayback secret.
- `.github/workflows/links.yml`: keep `contents: read`; its existing command should acquire fallback
  behavior through the updated Python script. Add no capture or commit step.

**Verify**:

```bash
rg -n "archive_sources.py|capture|preserv" \
  CONTRIBUTING.md templates/agent.yaml .github/pull_request_template.md \
  .claude/skills/add-agent-from-url/SKILL.md \
  .claude/skills/add-agent-from-url/evals/evals.json \
  .github/workflows/validate.yml
```

Expected: every Add-path instruction captures before merge; scheduled CI remains read-only and
contains no Steel/API credentials.

### Step 7: Backfill all recoverable current references

Do this only after Steps 1-6 are separately reviewed and committed.

1. Run a Markdown-only backfill first:

   ```bash
   uv run --locked python scripts/archive_sources.py \
     --all --continue-on-error --delay 2000 --save-wayback \
     > archive/backfill-report.json
   ```

   If Wayback credentials are not configured, omit `--save-wayback`; do not expose credentials in
   shell history, logs, artifacts, or committed files.
2. Review every successful `content.md` for title/source match and obvious error/interstitial text.
   Never accept a capture based only on HTTP 200.
3. Add each emitted `capture` block and verified `archived_url` to the matching source record.
   Regenerate derived files after the YAML batch.
4. Run PDF capture selectively in a second pass only for sources whose visual layout materially
   supports claims. Review each PDF and the aggregate size:

   ```bash
   du -sh archive/sources
   find archive/sources -name '*.pdf' -size +10M -print
   ```

   Expected: total size is reviewed explicitly; the second command prints nothing.
5. Classify every backfill failure in the report. A failure may be:
   - already missing before preservation;
   - explicitly non-archivable (`noarchive` or publisher restriction);
   - authenticated/private and therefore ineligible;
   - unsupported media where a page snapshot would not preserve the cited evidence;
   - transient, in which case retry once later.
6. Do not mark a failed capture as preserved. For an already-missing evidence source, locate a
   legitimate publisher/author archive or replacement evidence and narrow/remove unsupported
   claims. This editorial work is separate from capture mechanics.
7. The Atlassian DOT article is a known pre-existing miss with no available Wayback capture. Do
   not turn its 404 page or search snippets into a snapshot. If no legitimate replacement source
   can be linked and captured, STOP and ask the maintainer whether to narrow/remove the DOT claims
   or remove the record.

The backfill report is an audit aid, not evidence. Remove transient error details and review it for
sensitive data before deciding whether to commit it. It must never contain credentials.

**Verify**:

```bash
uv run --locked python scripts/archive_sources.py --check
uv run --locked python scripts/build.py
uv run --locked python scripts/build.py --check
uv run --locked python -m unittest discover -s tests
uv run --locked python scripts/check_links.py --local
git diff --check
```

Expected: every declared capture validates, generated files are current, all tests pass, and local
links pass. Run the external check only after all known pre-existing missing sources have received
legitimate replacement evidence or a real archive:

```bash
uv run --locked python scripts/check_links.py
```

Expected: exit 0; blocked/unreachable warnings are allowed; there are no missing sources without a
verified fallback.

### Step 8: Run final quality and scope gates

Run the entire repository verification block:

```bash
uv run --locked python scripts/archive_sources.py --check
uv run --locked python scripts/build.py --check
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m unittest discover -s tests
uv run --locked python scripts/check_links.py --local
git diff --check
git status --short
```

Expected: every command exits 0. `git status --short` lists only files allowed by this plan.

## Test plan

New tests must use `unittest`, `unittest.mock`, and temporary directories, matching existing test
style. No test may contact Steel, Wayback, or arbitrary external URLs.

- `tests/test_archive_sources.py`
  - good Markdown-only and Markdown+PDF captures;
  - malformed/missing Steel response fields;
  - HTTP error, empty body, interstitial, and `noarchive` rejection;
  - hosted PDF download validation and size cap;
  - exact hashes/byte counts;
  - path containment and overwrite refusal;
  - atomic cleanup;
  - Wayback optional success/failure and secret redaction;
  - offline `--check` corruption detection.
- `tests/test_build.py`
  - capture and manifest schemas;
  - archive URL validation;
  - RFC 3339 timestamp validation;
  - traversal/absolute/cross-source path rejection;
  - artifact existence, content, hash, bytes, PDF magic and size;
  - original/snapshot/Wayback rendering combinations;
  - normalized export schema version 4.
- `tests/test_check_links.py`
  - 404 and 410 confirmation;
  - local and Wayback fallback policy;
  - no-fallback failure;
  - blocked/unreachable behavior;
  - source/general-Markdown de-duplication;
  - archive-directory crawl exclusion;
  - summary counts including `archived`.
- `.claude/skills/add-agent-from-url/evals/evals.json`
  - Add-path expected output explicitly includes preservation;
  - exclusion/border-case behavior remains unchanged.

## Done criteria

All criteria must hold:

- [x] `url` remains the immutable original citation; no build or workflow rewrites it.
- [x] `archived_url` has one documented meaning: verified external archive URL.
- [x] Every declared Steel capture has an explicit manifest, Markdown artifact, timestamp, final
      URL, HTTP status, tool version, byte count, and validated SHA-256.
- [x] PDF is optional, capped at 10 MiB, validated, and used only after review.
- [x] No raw HTML, credentials, authenticated content, or private data is committed.
- [x] `archive/**` Markdown is excluded from recursive link discovery.
- [x] A confirmed 404/410 plus a verified fallback yields `archived` warning/pass.
- [x] A confirmed 404/410 without a verified fallback still fails.
- [x] The catalog renders the original and available preserved links together.
- [x] JSON export schema is 4 and includes validated capture metadata.
- [x] New-source intake captures before claims are merged.
- [x] Validation CI verifies archive integrity without network access or secrets.
- [x] Scheduled link CI remains read-only.
- [x] Third-party snapshot ownership/takedown policy is documented and reviewed before bulk
      publication.
- [x] Every recoverable existing source is backfilled; failures are explicitly reviewed and no
      error page is represented as evidence.
- [x] `uv run --locked python scripts/archive_sources.py --check` exits 0.
- [x] `uv run --locked python scripts/build.py --check` exits 0.
- [x] `uv run --locked ruff check .` exits 0.
- [x] `uv run --locked ruff format --check .` exits 0.
- [x] `uv run --locked python -m unittest discover -s tests` exits 0.
- [x] `uv run --locked python scripts/check_links.py --local` exits 0.
- [x] `git diff --check` exits 0.
- [x] No files outside the in-scope list are modified.
- [x] `plans/README.md` status is updated.

## STOP conditions

Stop and report rather than improvising if:

- The maintainer has not approved storing full third-party Markdown snapshots in this public
  repository or has not accepted the ownership/takedown wording before the bulk backfill.
- In-scope code no longer matches the current-state excerpts after the drift check.
- `content_fingerprint` has acquired real usages since `e943ed1`; its removal then needs a separate
  migration decision.
- Steel's actual JSON output cannot be mapped unambiguously to content, metadata status, and hosted
  PDF URL after consulting current official documentation and `steel describe`.
- A target requires authentication, a proxy, CAPTCHA bypass, or a private profile.
- A page declares `noarchive` or its publisher terms explicitly prohibit the planned capture.
- Implementing Save Page Now would require placing secrets in source YAML, command arguments, logs,
  or an untrusted pull-request workflow.
- Any archive artifact path resolves outside `archive/sources/<source-id>/`.
- A capture returns 200 but is an error/interstitial page or does not contain the evidence used by
  the catalog.
- A source was already removed and no legitimate pre-removal archive exists. Do not reconstruct it
  from snippets.
- The archive backfill adds more than 25 MiB of PDFs or any single PDF exceeds 10 MiB without an
  explicit storage decision from the maintainer.
- A verification step fails twice after a reasonable, scoped correction.
- Completion appears to require a new dependency, broader workflow permissions, a storage service,
  or an out-of-scope file.

## Maintenance notes

- Reviewers should inspect capture contents, not only hashes. A perfectly hashed CAPTCHA page is
  still invalid evidence.
- Hashes establish integrity against the committed capture, not truth or independent provenance.
- Never refresh a capture in place. A material source revision should get a new source ID/capture.
- Keep Wayback submission best-effort; its crawler can reject or incompletely replay some dynamic
  pages. Local Markdown remains the deterministic fallback.
- The link checker should not use current network state during `build.py`; builds must remain
  deterministic and offline.
- If repository size becomes material, design an object-storage migration as a separate plan. Do
  not introduce Git LFS or expiring Actions artifacts opportunistically.
- The current Atlassian DOT failure cannot be repaired by this feature retroactively. It needs a
  legitimate alternate source/archive and corresponding claim review.
- Revisit PDF policy only when preserved visual evidence is routinely needed; do not make it the
  default merely because Steel can generate it.
