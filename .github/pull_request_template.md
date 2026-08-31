# Change summary

Describe the approach, source, correction, analysis, or tooling change.

## Change type

- [ ] Approach or claim data
- [ ] Source or commentary
- [ ] Analysis or documentation
- [ ] Build or validation code

## Evidence review

- [ ] Each claim links to one or more source IDs.
- [ ] Each evidence link uses the correct relation.
- [ ] Direct quotations match the source text.
- [ ] Company metrics are identified as self-reported.
- [ ] Unknown details remain unknown.
- [ ] I have the right to submit this content under the repository licenses.
- [ ] The change contains no private or confidential information.
- [ ] Preservation was attempted while each new source was live.
- [ ] I reviewed each capture and confirmed it is the intended source, not an error or interstitial.
- [ ] Captures contain no authenticated, paywalled, private, or `noarchive` content.
- [ ] I have the right to submit any preserved third-party material under the archive policy.

## Verification

- [ ] `uv run python scripts/build.py`
- [ ] `uv run python scripts/archive_sources.py --check`
- [ ] `uv run python scripts/build.py --check`
- [ ] `uv run ruff check .`
- [ ] `uv run ruff format --check .`
- [ ] `uv run python -m unittest discover -s tests`
- [ ] `uv run python scripts/check_links.py --local`
- [ ] `git diff --check`

## Sources

List the main source URLs and explain any conflicting evidence.
