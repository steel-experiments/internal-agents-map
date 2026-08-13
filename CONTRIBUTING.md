# Contributing to Internal Agents Map

Contributions can add an approach, add a source, correct a claim, or improve the analysis.

The catalog favors broad collection and explicit provenance. Do not invent missing details. Record unknown values as `unknown`. Keep commentary and conflicting evidence, but label them.

## Set up the project

1. Create and activate a Python 3 virtual environment.
2. Run `python3 -m pip install -r requirements-dev.txt`.
3. Run `python3 scripts/build.py --check`.
4. Run `python3 -m unittest discover -s tests`.

## Add an approach

1. Copy `templates/agent.yaml` to `data/agents/<id>.yaml`.
2. Give the record a kebab-case ID that matches its file name.
3. Add the shared rubric fields. Use `unknown` when the sources do not document a value.
4. Add a scoped `operating_models` assessment. Record where human attention normally returns, not a company-wide maturity estimate.
5. Add structured source records before you summarize them.
6. Link every claim path to evidence. Add a locator when the source has a stable section, timestamp, comment ID, commit, or line.
7. Run `python3 scripts/build.py`.
8. Run all verification commands in the pull request template.

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

- `README.md`, between the catalog markers
- `docs/landscape.md`
- `data/agents.json`

Do not edit generated content by hand. Commit these files with the source YAML change.

## Verify a change

Run:

```bash
python3 scripts/build.py
python3 scripts/build.py --check
python3 -m unittest discover -s tests
python3 scripts/check_links.py --local
git diff --check
```

The scheduled link check tests external URLs. A pull request does not depend on remote sites being available.
