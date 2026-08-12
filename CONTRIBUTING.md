# Contributing to Internal Agents Map

Thanks for helping map how companies build internal agents. There are two ways to contribute,
and both are welcome.

> **The one rule: don't invent.** Every claim in an entry should trace to a source. A thin,
> sourced entry is better than a rich, guessed one. If a field isn't documented anywhere, omit
> it (the build hides empty fields automatically) or flag it with a `# NOTE:` comment.

---

## Add or update an agent (~15 min)

1. **Copy the template** — `cp templates/agent.yaml data/agents/<id>.yaml`.
   - `<id>` is kebab-case (e.g. `acme-copilot`) and **must match the filename**.
2. **Fill it in** using the [schema reference](data/schema.md). Required fields: `id`,
   `company`, `agent_name`, `year`, `status`, `domains`, `autonomy`, `summary`. Add
   `architecture`, `primitives`, `key_metrics`, `lessons_learned`, and `sources` where you
   have evidence.
3. **Run the build** — `python scripts/build.py`. This regenerates the README landscape table,
   `docs/landscape.md`, and `data/agents.json` from your YAML.
4. **Commit all three generated files together with your YAML.**
5. **Open a PR** — the [PR template](.github/pull_request_template.md) has a checklist.

### Setup

You need Python 3 and PyYAML:

```bash
pip install pyyaml
python scripts/build.py
```

If PyYAML is missing the build prints a clear install hint.

### Field quick reference

| Field | Required | Example |
| --- | --- | --- |
| `id` | ★ | `doordash-flux` (matches filename) |
| `company` / `agent_name` | ★ | `DoorDash` / `Flux` |
| `year` | ★ | `2026` (first public evidence) |
| `status` | ★ | `internal` \| `open-sourced` \| `commercialized` |
| `domains` | ★ | `[coding, code-review, ci-triage]` |
| `autonomy` | ★ | `assistive` \| `human-in-loop` \| `drafts-reviewed` \| `autonomous` |
| `summary` | ★ | one sentence |
| `architecture.*` | optional | `sandbox`, `harness`, `model`, `tool_access`, `interfaces`, `knowledge`, `credentials`, `context_mgmt` |

Allowed values and full descriptions are in [`data/schema.md`](data/schema.md).

### Scope check before you add

The entry must be **one organization's internal/proprietary build** — built to run inside its
own walls for its own people. Commercial agents (Devin, Cursor, Claude Code) and frameworks
(Claude Agent SDK, LangGraph) are out of scope as entries; they belong only as a `harness` or
`tool_access` note inside an entry, or in [`docs/further-reading.md`](docs/further-reading.md).
See [further reading](docs/further-reading.md#why-these-arent-catalog-entries) for the
boundary.

### The marker convention — don't hand-edit the table

The README table lives between these markers and is regenerated on every build:

```
<!-- BEGIN LANDSCAPE -->
<!-- END LANDSCAPE -->
```

Never edit anything between them by hand — your changes will be overwritten. Edit the YAML and
re-run the build. Everything *outside* the markers (intro, thesis, CTAs) is hand-authored and
safe to edit directly.

---

## Add or edit a pattern or lesson

The synthesis docs are hand-curated (no build step):

- [`docs/patterns.md`](docs/patterns.md) — recurring architecture primitives.
- [`docs/adoption-lessons.md`](docs/adoption-lessons.md) — how agents get adopted.
- [`docs/further-reading.md`](docs/further-reading.md) — adjacent refs.

Edit them directly and cite the companies you draw from. Open a PR.

---

## Committing generated files

Always commit the regenerated `README.md`, `docs/landscape.md`, and `data/agents.json` in the
same PR as your data change, so the repo is always in a built state.

To verify your change locally:

```bash
python scripts/build.py        # should run clean
python scripts/build.py        # second run → "unchanged README.md" (idempotent)
python -c "import json; print(len(json.load(open('data/agents.json'))), 'agents')"
```

Thanks for contributing — and please be excellent to one another (see
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)).
