# Catalog data schema

Each YAML file in `data/agents/` describes one reported approach. An approach can be an agent, a platform, an orchestration system, or an implemented supporting pattern.

The build creates four linked collections in `data/agents.json`:

- `approaches` contains the systems and their comparison fields.
- `claims` contains sourced statements derived from authored fields.
- `sources` contains the evidence and commentary records.
- `companies` contains the organization registry with each logo descriptor.

Copy `templates/agent.yaml` when you add an approach. Omit optional fields when no public source documents them. Use `unknown` for required rubric fields when the sources do not provide an answer.

## Required approach fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | A kebab-case ID that matches the file name. |
| `company` | string | The organization that built or adapted the approach. |
| `agent_name` | string | The reported name. Use a clear description if no name is public. |
| `approach_type` | enum | The type of approach. See the values below. |
| `deployment_stage` | enum | `research`, `prototype`, `pilot`, `deployed`, `scaled`, or `unknown`. |
| `year` | integer | The year of the earliest verified public evidence. |
| `first_public_evidence` | map | The evidence `date` and its `source_id`. |
| `last_reviewed_at` | date | The last catalog review date. |
| `status` | enum | `internal`, `open-sourced`, `commercialized`, or `mixed` for a combined record. |
| `domains` | list | Work domains, such as `coding`, `support`, or `security`. |
| `autonomy` | enum | The autonomy level. See the values below. |
| `operating_models` | list | Scoped catalog assessments of where human attention returns in a normal successful run. |
| `rubric` | map | Shared comparison fields. |
| `summary` | string | A short, factual description. |
| `sources` | list | Structured public sources. |
| `evidence` | map | A link from each authored claim to one or more sources. |

Optional identity fields include `aliases` and `family_id`. Use `relationships` to connect records. Each relationship has a `type` and `approach_id`. Types are `component-of`, `built-on`, `successor-of`, and `related-to`.

### Approach types

- `agent`: One task-performing system. It may be invoked interactively, in the
  background, on a schedule, or by an event. Internal subagents do not by themselves
  turn an agent into an agent system.
- `agent-system`: A documented family of related agents with shared infrastructure.
- `platform`: Reusable infrastructure that supports several agents or workflows.
- `orchestration-system`: A system whose primary responsibility is coordinating agents.
- `supporting-pattern`: A narrower implemented component that enables agent operation.

Classify a compound entry by its documented primary responsibility and explain its
components. Invocation is independent of structural type; an event trigger does not
by itself establish unattended execution.

### Autonomy values

- `assistive`: A person drives the work and the system provides help.
- `human-in-loop`: The system acts, but a person participates in each cycle or approval.
- `drafts-reviewed`: The system prepares work that a person reviews before use.
- `autonomous`: The work takes effect without required human review.
- `unknown`: The sources do not document the review boundary.

### Operating models and derived levels

`operating_models` adapts [Dan Shapiro's five levels of AI-assisted software development](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/) to a documented internal-agent workflow, not to an organization as a whole. Shapiro's original framework is coding-oriented; this catalog generalizes it by asking where human attention normally returns. Each item contains only:

| Field | Description |
| --- | --- |
| `scope` | A short description of the workflow being assessed, preferably from input to output. |
| `attention_boundary` | Where human attention normally returns during a successful run. |

The build derives the level from the attention boundary:

| Attention boundary | Derived level | Meaning |
| --- | ---: | --- |
| `continuous-steering` | 2 | A person pairs with the agent throughout execution. |
| `work-product-review` | 3 | The agent produces a draft or implementation that a person reviews. |
| `outcome-review` | 4 | A person delegates from a specification and evaluates tests, behavior, or outcomes rather than routinely inspecting implementation. |
| `exception-only` | 5 | A person is normally involved only when the system raises an exception. |
| `unknown` | — | The collected evidence does not locate the human attention boundary. |

Never render or interpret a level without its scope. Compound systems can have multiple scoped assessments. Use `unknown` rather than averaging different workflows or guessing from `autonomy`, invocation mode, output volume, or company identity.

The boundary describes required human attention, not tool authority or elapsed unattended
execution. Record permissions and publication controls in the supported claims. A Level 5
workflow can still be unable to merge, deploy, spend, or act in production without approval.

Each `operating_models.N` item is an evidence-linked inference with `catalog-judgment` provenance. Its claim metadata must include `confidence`, `confidence_reason`, and `valid_at`. The level itself is generated and is never authored as a reported company fact.

## Comparison rubric

The rubric organizes different definitions and designs. It does not determine whether an approach belongs in the catalog.

| Field | Allowed values |
| --- | --- |
| `invocation` | A list of `interactive`, `background`, `scheduled`, `event-driven`, or `unknown`. |
| `state` | `run-only`, `durable-session`, `cross-session-memory`, `mixed`, or `unknown`. |
| `identity` | `user`, `dedicated-agent`, `service`, `mixed`, or `unknown`. |
| `evidence_strength` | `detailed-primary`, `limited-primary`, `secondary-only`, `mixed`, or `unknown`. |

Evidence strength describes the available detail. It does not measure whether a claim is true. A company article can provide detailed architecture and still contain marketing claims.

Structural type and invocation answer different questions. `approach_type` identifies what
kind of system the record describes. `rubric.invocation` identifies how work starts or proceeds.
Do not infer either field from the other, and use `unknown` when the source is silent.

## Optional description fields

`architecture` can contain short strings for `sandbox`, `harness`, `model`, `tool_access`, `knowledge`, `credentials`, and `context_mgmt`. Its `interfaces` field is a list. For a reviewed but undocumented execution sandbox, use the canonical string `unknown`; omit an inapplicable sandbox for a supporting pattern. An earlier implementation's environment must be labeled as historical, not attributed to its replacement.

Domain values are `coding`, `code-review`, `support`, `on-call`, `research`, `customer-success`, `security`, `finance-ops`, `data`, `ci-triage`, `maintenance`, `ops`, `recruitment`, `migrations`, and `design`.

Interface values are `slack`, `github`, `web`, `cli`, `linear`, `chrome-extension`, `webhook`, `desktop`, `scheduled`, `skill`, `cursor`, `api`, `automation`, `ci`, `intercom`, `jira`, `internal-ui`, `mobile`, and `monday`.

`primitives` is a list of maps with `name` and `desc` fields. `key_metrics` and `lessons_learned` are lists of strings. `headline_metric` is a short reported result.

Treat all company metrics as self-reported unless an independent source verifies them. Include the date, scope, denominator, and measurement method when the source provides them.

## Company registry

`data/companies.yaml` holds one record per organization, sorted by `id`. The registry links every approach record to one organization and names the logo asset of each organization.

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | A kebab-case ID. It is also the logo file stem. |
| `name` | string | The organization name. It must equal the `company` value of the approach records. |
| `homepage` | string | The organization homepage. It must use HTTPS. |
| `logo` | map or `none` | The logo asset record, or `none` while no asset is collected. A logo map holds exactly `file`, `source_url`, and `accessed_at`. |
| `logo_note` | string | Required with `logo: none`. It states the reason no logo is shown. It is not allowed when a logo file is named. |

The join runs both ways. Every `company` value in `data/agents/` must have a registry record. Every registry record must be used by at least one approach. `public/logos/` may hold only files the registry names.

Logo files live in `public/logos/<id>.svg` or `public/logos/<id>.png`. The build rejects an SVG larger than 64 KiB and a PNG larger than 128 KiB or narrower than 128 pixels. An SVG needs a `viewBox`. It must not hold a DOCTYPE, an ENTITY declaration, a script, a `foreignObject`, an `on*` attribute, a `javascript:` value, or a non-fragment `href`. The intrinsic size comes from the `viewBox` or from the PNG header.

The build derives the `companies` collection into `data/agents.json` (schema version 7) and adds `company_id` to every approach. Each company record carries `id`, `name`, `homepage`, and `logo`. The `logo` is `null` when no asset exists. Otherwise it is a descriptor with `path`, `media_type`, `width`, `height`, `bytes`, `sha256`, `source_url`, and `accessed_at`. The build derives the hash, the byte count, and the size from the asset. Never author them.

Schema 6 replaces the old `task-agent` and `background-agent` approach types with
`agent`. Consumers that used those values should filter structural type with
`approach_type: agent` and use `rubric.invocation` to distinguish interactive,
background, scheduled, and event-driven operation. The compact index schema is 3.

## Source records

Every source requires these fields:

| Field | Description |
| --- | --- |
| `id` | A repository-wide unique kebab-case ID. |
| `title` | The source title. |
| `url` | The immutable original publisher URL. It must use HTTPS and must never be replaced with an archive URL. |
| `canonical_url` | The normalized publisher URL after redirects and tracking removal. |
| `kind` | The source format. |
| `provenance_class` | The relationship between the publisher and the approach. |
| `accessed_at` | The collection date. |
| `last_verified_at` | The last successful review date. |
| `role` | `evidence`, `commentary`, or `discovery`. The default is `evidence`. |

Optional fields include `publisher`, `authors`, `published_at`, `archived_url`, `capture`, and `duplicate_of`. `archived_url` is the preferred verified external archive URL and must use HTTPS. `capture` points to a repository-owned Steel capture manifest:

```yaml
archived_url: "https://web.archive.org/web/20260831123456/https://example.com/article"
capture:
  manifest_path: "archive/sources/company-agent-source-1/metadata.json"
```

The capture map contains exactly `manifest_path`. Capture bundles use this deterministic layout:

```text
archive/sources/<source-id>/metadata.json
archive/sources/<source-id>/content.md
archive/sources/<source-id>/page.pdf        # optional
```

The version 1 JSON manifest contains `schema_version`, `source_id`, `original_url`, `final_url`, `captured_at`, `http_status`, `tool`, and `artifacts`. It may also contain `external_archive_url`, which must equal `archived_url`. The `tool` map records `name: steel` and a non-empty version. `artifacts.markdown` is mandatory; `artifacts.pdf` is optional. Each artifact records its repository-relative `path`, exact `bytes`, and a lowercase `sha256:<digest>`. Markdown must be non-empty. PDFs must begin with `%PDF-` and cannot exceed 10 MiB. Paths and hashes are validated during every build.

Captures are append-only evidence snapshots: never overwrite an existing bundle or use a capture to replace the original `url`. Create a new source ID when materially changed source content is needed for new claims.

Source kinds are `engineering-blog`, `corporate-article`, `documentation`, `source-code`, `repository`, `release`, `social-post`, `talk`, `transcript`, `podcast`, `paper`, `case-study`, `news`, `hn-thread`, `hn-comment`, `forum`, and `other`.

Provenance classes are:

- `first-party`: The organization published the source.
- `direct-participant`: A person who worked on the system published the source.
- `independent-secondary`: An outside publication reported the information.
- `community`: A community member supplied analysis or commentary.
- `aggregator`: The source collects information from other sources.

Use source records for evidence, context, and commentary. A Hacker News thread and each material comment are separate sources. Store item and comment IDs in the URL or optional metadata.

## Claim evidence

Every descriptive field becomes a claim in the generated JSON file. The `evidence` map links its field path to source records.

```yaml
evidence:
  summary:
    - source_id: acme-agent-source-1
      relation: supports
      locator: "Architecture, paragraph 3"
  key_metrics.0:
    - source_id: acme-agent-source-2
      relation: supports
      locator: "12:40"
```

The relation is `supports`, `contradicts`, or `contextualizes`. Use a stable locator when one exists. For preserved sources, `Preserved content.md, lines 23–27` refers to the immutable artifact in that source's capture bundle, including its archive header. A locator must identify the supporting passage, not merely a broad topic. For source code, record the commit, path, and line. For a talk, record the timestamp.

For each lesson, use claim metadata to distinguish a reported practice (`fact`,
`reported`), an attributed preference (`opinion`, `reported`), and a catalog inference
(`inference`, `catalog-judgment`). Its `confidence_reason` names the supporting
observation and any missing link in the reasoning. A generic claim that the source
supports the lesson does not explain that reasoning. The lesson text must also carry
its scope: a team's implementation is not a recommendation for every organization.

Use `claim_metadata` when the default classification is not correct:

```yaml
claim_metadata:
  key_metrics.0:
    kind: metric
    provenance: reported
    confidence: medium
    confidence_reason: "A direct participant reported the number without a method."
    valid_at: 2026-04
    reported_by: Acme
    metric_scope: "Merged agent-authored pull requests"
    denominator: "All merged pull requests"
    measurement_method: "Company dashboard"
```

A metric's `valid_at` can identify a dated reported observation, but does not by itself define a measurement interval. Keep the interval explicit in `metric_scope` or `measurement_method`; never derive it from a capture or review timestamp. If a source says only “last month” or “as of Part 2,” preserve that wording and leave unsupported calendar dates unset.

Claim kinds are `fact`, `metric`, `inference`, and `opinion`. Provenance values are `reported`, `observed`, `inferred`, and `catalog-judgment`. Confidence values are `high`, `medium`, `low`, and `unverified`.

Metric metadata can also include `value`, `unit`, `reported_by`, `metric_scope`, `denominator`, and `measurement_method`. The generated export uses the company as `reported_by` when a reported metric does not override it.

## Optional reviewed page content

`page_content` version 1 records an editorial review without changing existing claim
identities. It is optional during the pilot. `reviewed_at` is a full `YYYY-MM-DD` date,
and `source_ids` lists the entry sources actually read. `questions` contains exactly
`purpose`, `workflow`, `human_involvement`, `implementation`, `validation`,
`observations`, and `lessons`. `implementation_fields` contains all eight architecture
keys. Every disposition has a `state`, `claim_paths`, and optionally a `note`.

States are `reported`, `unreported`, `not-applicable`, and `not-reviewed`. Reported
slots require one or more same-entry claims supported by a reviewed source. All other
states require no claim paths and a concrete note; for `not-reviewed`, the note is the
next research action. An `unreported` implementation field is the one exception: the
state already says the captures were read and name nothing, so the note is optional
there and must be left out unless it adds a fact the state does not carry — what the
source says instead, which claim stays in research details, or the scope that limits
the answer. A reported workflow also requires `workflow_scope`.

`primitive_roles` classifies every primitive as `workflow`, `mechanism`, or
`validation`; the workflow question lists every workflow primitive in reading order.
`observations` covers the headline and every key metric. A canonical observation has a
`category` (`effectiveness`, `adoption-output`, `cost-latency`,
`implementation-scale`, or `runtime-capacity`), a `basis`
(`reported-measurement`, `qualitative`, `estimate`, or `target`), and a specific
`subject`. A duplicate representation instead has `duplicate_of` and `reason`.
Targets must be same-entry canonical observations; self references, cycles, and chains
are invalid. Confirm equal subject, statement/value, period, scope, and qualifications
before marking a duplicate. The working criterion: an alias must add nothing the
canonical lacks. A component of a compound observation can alias the compound;
an observation carrying an extra qualification or absence note cannot, however
similar its number.

Run `uv run --locked python scripts/content_coverage.py --check` to validate the
coverage view, or add `--output <path>` to write deterministic JSON. Records without
the optional block are reported as `legacy-unassessed`.

## Collection rules

1. Resolve the approach identity before you extract claims.
2. Capture source metadata before you summarize the source.
3. Keep each authored claim short and specific.
4. Link every claim to exact evidence.
5. Preserve supporting, conflicting, and contextual sources.
6. Mark catalog interpretation as `inferred` or `catalog-judgment`.
7. Record unknown values instead of inferring absence.

Normalize URLs and remove tracking parameters. Link mirrors and translations with `duplicate_of`. Do not merge two approaches only because one company built both. Use relationship metadata in a future record revision when systems share a platform or change names.

Run `uv run python scripts/build.py` after each data change. Run
`uv run python scripts/build.py --check` to verify committed output.

## Collection migration (catalog 7 / compact index 3)

The build derives `catalog_section`: `agent` and `agent-system` become `agents`;
`platform`, `supporting-pattern`, and `orchestration-system` become `infrastructure`.
Do not author this field. Unknown structural types fail validation. Existing fields,
IDs, claim anchors, and detail URLs remain available. `/agents.json` and
`/agents/index.json` retain their historical names and include both collections.
Consumers must select `catalog_section` explicitly for agent counts or comparisons.
One agent family counts once, not as an estimated number of constituent agents.

`/` and `/index.md` represent Agents. `/infrastructure` and `/infrastructure.md`
represent Infrastructure. `/?collection=all` shows two labeled groups. Legacy
infrastructure type queries on `/` switch to All while retaining OR filters.
Seven `page_content.questions` keys remain the common evidence contract; HTML and
Markdown apply collection profiles without changing evidence or hiding unknowns.
