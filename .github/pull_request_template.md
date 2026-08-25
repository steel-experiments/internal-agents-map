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

## Verification

- [ ] `uv run python scripts/build.py`
- [ ] `uv run python scripts/build.py --check`
- [ ] `uv run ruff check .`
- [ ] `uv run ruff format --check .`
- [ ] `uv run python -m unittest discover -s tests`
- [ ] `uv run python scripts/check_links.py --local`
- [ ] `git diff --check`

## Sources

List the main source URLs and explain any conflicting evidence.
