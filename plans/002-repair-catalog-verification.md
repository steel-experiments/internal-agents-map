# Plan 002: Repair catalog verification and archival failure handling

> Executor: implement in an isolated worktree; the reviewer maintains the index.
> Drift check: `git diff --stat e3a53f7..HEAD -- scripts tests`
> Compare any drift with the excerpts below before adapting. Do not discard other work.

## Status

- Priority: P1
- Effort: M
- Risk: LOW
- Depends on: none
- Category: bug, tests
- Planned at: commit `e3a53f7`, 2026-09-09

## Why this matters

Required local-link validation currently fails on a fenced Markdown example. The
published execution-environment count treats undocumented values as evidence.
Optional Wayback transport failures can prevent local preservation, and archive
containment checks do not consistently enforce independent source bundles.

## Current state

Python 3.12+, PyYAML, unittest, Ruff; uv manages dependencies. The current checkout
has a usable `.venv`. Code uses typed functions, pathlib, and explicit error messages.
Tests use unittest, temporary directories, and unittest.mock; follow the fixtures
in `tests/test_archive_sources.py` and `tests/test_check_links.py`.

- `scripts/check_links.py:92` applies `MARKDOWN_LINK.findall(text)` to all Markdown,
  including fenced examples. `markdown_urls` has the same issue. The failing example
  is in `plans/001-preserve-source-evidence.md:432`. Keep that valid example intact.
- `scripts/build.py:903` counts sandbox values using
  `value not in (None, "", "unknown")`. Eight current strings begin with `Not ` or
  `n/a`; these describe missing/inapplicable detail, not concrete environments.
- `scripts/archive_sources.py:519` calls `response.read(...)` without converting
  network exceptions to `ArchiveError`. `preserve_with_wayback` catches only
  `ArchiveError`; `capture_source` calls it before writing the local bundle.
- `scripts/archive_sources.py:215` checks resolved artifacts against all of
  `archive/sources`, allowing sibling-bundle symlinks. Manifest validation does too.
- `scripts/build.py:317` and `scripts/check_links.py:_safe_archive_path` implement
  related path rules. Ensure source-directory symlinks cannot redefine the boundary.

Baseline: 83 unittest tests pass; archive and build checks and Ruff pass; local
links fail on the fenced example. No live network calls belong in regression tests.

## Scope

In scope: `scripts/build.py`, `scripts/check_links.py`, `scripts/archive_sources.py`,
`tests/test_build.py`, `tests/test_check_links.py`, `tests/test_archive_sources.py`.
Out of scope: authored catalog YAML, archive contents, dependencies, CI configuration,
licenses, source URLs, unrelated parser behavior. Generated outputs are refreshed by
Plan 003 after these fixes are integrated. No commits, pushes, or public messages.

## Commands

Use the original checkout's absolute `.venv/bin/python` and `.venv/bin/ruff` from the
worktree; scripts resolve their repository root from their own locations.

| Purpose | Command | Expected result |
| --- | --- | --- |
| Tests | `python -m unittest discover -s tests` | All pass after outputs regenerated |
| Archive | `python scripts/archive_sources.py --check` | All declared captures valid |
| Build | `python scripts/build.py` then `python scripts/build.py --check` | Current generated outputs |
| Lint | `ruff check .` | Exit 0 |
| Format | `ruff format --check .` | Exit 0 |
| Links | `python scripts/check_links.py --local` | Exit 0 |
| Whitespace | `git diff --check` | Exit 0 |

## Steps

1. Share a small Markdown preprocessing helper between local and external link
   extraction. Ignore fenced code using backticks or tildes, respecting fence length,
   indentation, and unclosed fences. Ignore inline code examples as appropriate.
   Preserve real links and headings. Avoid adding a parser dependency for this fix.
   Test fenced placeholders, real broken links outside fences, and external examples.
   Verify link tests and `python scripts/check_links.py --local` exit 0.
2. Give environment counting explicit missing-value handling (including existing
   legacy `Not specified`, `Not detailed`, and `n/a` strings, case-insensitively).
   Plan 003 normalizes authored missing values. Test an independent mixture of known,
   absent, unknown, legacy, and not-applicable environments; do not assert only that
   output equals the same flawed algorithm. Verify build tests other than generated
   freshness until the final regeneration, and report that expected temporary drift.
3. Convert expected response-read transport failures (including TimeoutError,
   OSError/URLError and http.client.HTTPException/IncompleteRead) to safe ArchiveError
   messages. Never expose raw credential-bearing exception text. Verify Wayback save
   and lookup body failures fall back and a successful Steel capture is written locally.
   Test the real capture orchestration with mocked transports, not only the helper.
   Keep PDF failures fatal when PDF was explicitly requested; batch continuation must
   still work. Verify archive tests pass without any network traffic.
4. Enforce each source's own directory in all three validation paths. Reject sibling
   and external symlink targets, including source-directory and manifest symlinks.
   Preserve temporary staging-bundle validation during atomic capture. Check repository
   and archive parent containment as well. Add regression tests using temp directories
   for ordinary files, sibling/external targets, and staging captures. Verify all archive
   and link tests and archive --check pass.
5. Review the complete diff and report files changed, tests, and any deviations. Wait
   for reviewer approval before applying only owned changes to the main checkout.
   After Plan 003 is applied, regenerate outputs and run every final gate above in
   the main checkout. The user authorized delivering fixes in the current project.

## Done criteria

- [x] Fenced examples no longer fail or pollute link checking; real broken links fail.
- [x] Undocumented and inapplicable environments are excluded from counts.
- [x] Wayback body timeout/incomplete-response regressions preserve local captures.
- [x] Sibling/external archive symlink regressions fail in each validator.
- [x] All tests, archive/build checks, Ruff, local links, and git diff --check pass
      after combined regeneration with Plan 003.
- [x] Only scoped code/tests changed; reviewer updates plans/README.md.

## STOP conditions

Report if a fix needs a dependency/schema migration, changes existing snapshot bytes,
requires credentials or live capture, or invalidates a legitimate existing bundle.
A generated-freshness failure before Plan 003 regeneration is expected, not a blocker.
Do not stop merely for routine implementation choices or a fixable test failure.

## Maintenance notes

Keep the three containment validators consistent. Add regressions before expanding
Markdown parsing. Evidence presence is not proof of a concrete execution environment.

## Execution log

2026-09-09: Implemented in an isolated worktree and reviewed. The reviewer read all
six code/test diffs and independently ran the full verification suite: 93 tests,
88 archive captures, generated freshness, local links, Ruff lint/format, and
whitespace checks passed. Approved for application to the current checkout. Final
combined generation and validation await Plan 003's editorial changes.

## Completion — 2026-09-09

Applied reviewed changes to the current checkout and regenerated the catalog with
both plans integrated. All final gates passed: 97 unittest tests, 88 declared capture
validations, generated-file freshness, local links, Ruff lint/format, and whitespace.
Concurrent commits through `e67e79b` added an email-address check and four tests;
those changes were preserved, and the additional privacy gate also passed.

The reviewer independently verified the new report's local links and privacy check,
its exact ledger of all 115 baseline metric IDs, supporting locators for all 108
remaining metrics, and unchanged archive artifacts. Final export: 555 claims,
639 evidence links, 177 links with locators, and 16 documented environments.
Both plans are complete; unresolved source questions remain explicitly documented
in `docs/evidence-review.md`, rather than represented as verified facts.
