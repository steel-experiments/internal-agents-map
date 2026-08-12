# Catalog data schema

Each YAML file in `data/agents/` describes one reported approach. An approach can be an agent, a platform, an orchestration system, or an implemented supporting pattern.

The build creates three linked collections in `data/agents.json`:

- `approaches` contains the systems and their comparison fields.
- `claims` contains sourced statements derived from authored fields.
- `sources` contains the evidence and commentary records.

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
| `rubric` | map | Shared comparison fields. |
| `summary` | string | A short, factual description. |
| `sources` | list | Structured public sources. |
| `evidence` | map | A link from each authored claim to one or more sources. |

Optional identity fields include `aliases` and `family_id`. Use `relationships` to connect records. Each relationship has a `type` and `approach_id`. Types are `component-of`, `built-on`, `successor-of`, and `related-to`.

### Approach types

- `task-agent`: An agent that performs a bounded task.
- `background-agent`: An agent that runs after delegation or an event.
- `agent-system`: A set of related agents with shared infrastructure.
- `platform`: Infrastructure that supports several agents or workflows.
- `orchestration-system`: A system that coordinates other agents.
- `supporting-pattern`: An implemented design that supports agent operation.

### Autonomy values

- `assistive`: A person drives the work and the system provides help.
- `human-in-loop`: The system acts, but a person participates in each cycle or approval.
- `drafts-reviewed`: The system prepares work that a person reviews before use.
- `autonomous`: The work takes effect without required human review.
- `unknown`: The sources do not document the review boundary.

## Comparison rubric

The rubric organizes different definitions and designs. It does not determine whether an approach belongs in the catalog.

| Field | Allowed values |
| --- | --- |
| `invocation` | A list of `interactive`, `background`, `scheduled`, `event-driven`, or `unknown`. |
| `state` | `run-only`, `durable-session`, `cross-session-memory`, `mixed`, or `unknown`. |
| `identity` | `user`, `dedicated-agent`, `service`, `mixed`, or `unknown`. |
| `evidence_strength` | `detailed-primary`, `limited-primary`, `secondary-only`, `mixed`, or `unknown`. |

Evidence strength describes the available detail. It does not measure whether a claim is true. A company article can provide detailed architecture and still contain marketing claims.

## Optional description fields

`architecture` can contain short strings for `sandbox`, `harness`, `model`, `tool_access`, `knowledge`, `credentials`, and `context_mgmt`. Its `interfaces` field is a list.

Domain values are `coding`, `code-review`, `support`, `on-call`, `research`, `customer-success`, `security`, `finance-ops`, `data`, `ci-triage`, `maintenance`, `ops`, `recruitment`, and `migrations`.

Interface values are `slack`, `github`, `web`, `cli`, `linear`, `chrome-extension`, `webhook`, `desktop`, `scheduled`, `skill`, `cursor`, `api`, `automation`, `ci`, `intercom`, `jira`, `internal-ui`, `mobile`, and `monday`.

`primitives` is a list of maps with `name` and `desc` fields. `key_metrics` and `lessons_learned` are lists of strings. `headline_metric` is a short reported result.

Treat all company metrics as self-reported unless an independent source verifies them. Include the date, scope, denominator, and measurement method when the source provides them.

## Source records

Every source requires these fields:

| Field | Description |
| --- | --- |
| `id` | A repository-wide unique kebab-case ID. |
| `title` | The source title. |
| `url` | The source URL. It must use HTTPS. |
| `canonical_url` | The normalized URL after redirects and tracking removal. |
| `kind` | The source format. |
| `provenance_class` | The relationship between the publisher and the approach. |
| `accessed_at` | The collection date. |
| `last_verified_at` | The last successful review date. |
| `role` | `evidence`, `commentary`, or `discovery`. The default is `evidence`. |

Optional fields include `publisher`, `authors`, `published_at`, `archived_url`, `content_fingerprint`, and `duplicate_of`.

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

The relation is `supports`, `contradicts`, or `contextualizes`. Use a stable locator when one exists. For source code, record the commit, path, and line. For a talk, record the timestamp.

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

Claim kinds are `fact`, `metric`, `inference`, and `opinion`. Provenance values are `reported`, `observed`, `inferred`, and `catalog-judgment`. Confidence values are `high`, `medium`, `low`, and `unverified`.

Metric metadata can also include `value`, `unit`, `reported_by`, `metric_scope`, `denominator`, and `measurement_method`. The generated export uses the company as `reported_by` when a reported metric does not override it.

## Collection rules

1. Resolve the approach identity before you extract claims.
2. Capture source metadata before you summarize the source.
3. Keep each authored claim short and specific.
4. Link every claim to exact evidence.
5. Preserve supporting, conflicting, and contextual sources.
6. Mark catalog interpretation as `inferred` or `catalog-judgment`.
7. Record unknown values instead of inferring absence.

Normalize URLs and remove tracking parameters. Link mirrors and translations with `duplicate_of`. Do not merge two approaches only because one company built both. Use relationship metadata in a future record revision when systems share a platform or change names.

Run `python3 scripts/build.py` after each data change. Run `python3 scripts/build.py --check` to verify committed output.
