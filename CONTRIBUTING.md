# Contributing to Internal Agents Map

Contributions can add an approach, add a source, correct a claim, or improve the analysis.

The catalog favors broad collection and explicit provenance. Do not invent missing details. Record unknown values as `unknown`. Keep commentary and conflicting evidence, but label them.

The catalog is public. Do not add personal contact data, such as e-mail addresses or private notes about people, to any file. Only public sources belong here. CI rejects e-mail addresses in tracked files.

## Set up the project

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/).
2. Run `uv sync --locked`.
3. Run `uv run python scripts/build.py --check`.
4. Run `uv run python -m unittest discover -s tests`.

uv installs the required Python version and manages the project environment. You do not need to
create or activate a virtual environment yourself.

## Add an approach

1. Copy `templates/agent.yaml` to `data/agents/<id>.yaml`.
2. Give the record a kebab-case ID that matches its file name.
3. Add the shared rubric fields. Use `unknown` when the sources do not document a value.
4. Add a scoped `operating_models` assessment. Record where human attention normally returns, not a company-wide maturity estimate.
5. Add structured source records before you summarize them.
6. Preserve each accepted source while it is still live:
   `uv run python scripts/archive_sources.py --source-id <source-id>`. Review the captured
   Markdown, then add the emitted `capture` and `archived_url` fields to the source record.
7. Link every claim path to evidence. Add a locator when the source has a stable section, timestamp, comment ID, commit, or line.
8. Run `uv run python scripts/build.py`.
9. Run all verification commands in the pull request template.

The approach must describe a system that a named organization built or materially adapted for its own teams. It can be a task agent, background agent, agent system, platform, orchestration system, or implemented supporting pattern.

Do not add a generic vendor product without a documented internal adaptation. Do not add an unattributed rumor as an approach.

## Add a source or commentary

Sources can include:

- Company articles and documentation
- Source code, repositories, releases, and commits
- Talks, transcripts, podcasts, and papers
- News reports and case studies
- Social posts
- Hacker News threads and material comments
- Other forum discussions

Set `kind` to the source format. Set `provenance_class` to the publisher relationship. These fields do not state whether a claim is true.

Use `first-party` for organization publications. Use `direct-participant` for a statement from a person who worked on the system. Use `independent-secondary` for outside reporting. Use `community` for Hacker News and forum commentary.

A commentary source can contextualize or contradict a claim. It does not need to support one. Use the corresponding evidence relation.

For Hacker News, keep the thread and each material comment as separate source records. Use the permanent item or comment URL. For source code, record a commit and file locator when possible.

### Preserve a source

The original `url` remains the catalog citation. The preservation command creates a reviewed,
append-only Steel Markdown capture and reports any existing or newly created Wayback URL:

```bash
uv run python scripts/archive_sources.py --source-id <source-id>
```

Add `--pdf` only when visual layout materially supports a claim. Add `--save-wayback` when Save
Page Now credentials are configured in the environment. Never put archive credentials in source
records, command arguments, logs, or pull requests.

The command refuses authenticated/private pages, explicit `noarchive` directives, error pages,
and existing bundles. Review `archive/sources/<source-id>/content.md` before linking the capture
from YAML. See the [source-preservation policy](docs/source-preservation.md) for ownership,
retention, and takedown rules.

## Write claims and analysis

- Use quotation marks only for exact source text.
- Mark company metrics as self-reported unless an independent source verifies them.
- Include a metric date, scope, denominator, and method when available.
- Mark editorial conclusions as `inferred` or `catalog-judgment`.
- Preserve conflicting reports when they refer to different dates or methods.
- Do not treat an undocumented field as evidence that a feature is absent.
- Never assign an operating level without naming the workflow scope. Treat it as a dated catalog judgment, not a reported company fact.

When you edit `docs/patterns.md` or `docs/adoption-lessons.md`, compare similar approach types and deployment stages. State the sample size. Include counterexamples before you call a pattern common.

## Generated files

The build updates these files:

- `README.md`, between the overview markers
- `docs/patterns.md`, between the catalog snapshot markers
- `docs/adoption-lessons.md`, between the catalog snapshot markers
- `docs/landscape.md`
- `data/agents.json`

Do not edit generated content by hand. Commit these files with the source YAML change.

## Verify a change

Run:

```bash
uv run python scripts/build.py
uv run python scripts/archive_sources.py --check
uv run python scripts/build.py --check
uv run ruff check .
uv run ruff format --check .
uv run python -m unittest discover -s tests
uv run python scripts/check_links.py --local
git diff --check
```

The scheduled link check tests external URLs. A confirmed 404 or 410 passes with an `archived`
warning when a verified fallback exists and fails otherwise. Blocked and temporarily unreachable
URLs are reported separately as warnings. A pull request does not depend on remote sites being
available.

## Generated website

The mini page is generated from the same validated catalog as the Markdown and JSON.
Edit `data/agents/*.yaml` for evidence and `templates/site.html`, `templates/site.css`,
or `templates/site.js` for the page. Run `uv run --locked python scripts/build.py`
and commit the regenerated `site/` outputs with the change. Do not hand-edit generated files.

Run `uv run --locked python scripts/check_site.py --root site` along with the existing
checks. Pull requests validate only; accepted updates on `main` can publish the validated
`site/` artifact through GitHub Pages. See [website maintenance and preview](docs/site.md)
for local serving, browser checks, initial Pages setup, and rollback.
