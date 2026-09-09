# Catalog evidence review — 2026-09-09

This editorial pass reviewed all **115 original metric claims** in the 39-approach catalog at commit `e3a53f7`, using the linked preserved source passages. It also reviewed the eight originally flagged sandbox records, reconciled Stripe architecture, and sampled retrospectives and commentary for failures and counterevidence. It is not an independent verification of company performance, a review of every nonmetric claim, or an exhaustive search for failures.

Existing archive artifacts and manifests were not changed. Reading a local capture did not advance a source's `last_verified_at`. The approach review date records this editorial work; it does not claim a new live-source verification. The later DoorDash research lead below is explicitly unpreserved.

## Coverage before and after

Counts are computed from the baseline and regenerated `data/agents.json`, counting every evidence link, including repeated source links across claims. “Has metadata” measures documentation coverage, not completeness or independent validity.

| Measure | Before | After |
| --- | ---: | ---: |
| Claims | 558 | 555 |
| Metric claims | 115 | 108 |
| Evidence links | 645 | 639 |
| Evidence links with locators | 51 | 177 |
| Metrics with at least one supporting locator | 20 | 108 |
| Metrics with valid_at | 31 | 38 |
| Metrics with metric_scope | 24 | 108 |
| Metrics with denominator | 12 | 50 |
| Metrics with measurement_method | 11 | 25 |
| Contradicting evidence links | 0 | 2 |

Two unsupported metrics were removed: Airbnb's engineer-onboarding figure and Sierra's automation count. Five claims remain in their authored fields but are no longer classified as metrics: Block's months-to-days opinion, GitHub's qualitative Slack-volume decrease, Notion security-team activity, Ramp's list of dependent agents, and Ramp's desired startup latency. The original 115 claims therefore reconcile to 108 retained metrics, five reclassifications, and two removals. The inapplicable Slack sandbox accounts for the third removed claim overall.

All 108 remaining metrics have precise supporting locators and scopes. Missing measurement methods and dates remain missing. Some scopes explicitly record a missing denominator or the source's own imprecise wording; that is not a substitute for a raw sample. `valid_at` can describe an observation date, while the actual measurement window remains in the wording/scope. Existing report-as-of dates for Brex, Atlassian, Cloudflare, PostHog and Uber should not be interpreted as exact study periods. Newly dated Flux claims use the dated announcement; Airbnb and Ramp history use dates explicitly stated in the source. Unsupported Spotify dates were removed rather than carried forward.

## Execution environments

The eight originally flagged records are complete:

| Record | Outcome | Preserved evidence |
| --- | --- | --- |
| Block Builderbot | `unknown`; no execution isolation implementation found | [Source 1](../archive/sources/block-builderbot-source-1/content.md), [source 2](../archive/sources/block-builderbot-source-2/content.md), [source 3](../archive/sources/block-builderbot-source-3/content.md) |
| Flex investigation agent | `unknown`; partner data isolation is not an execution sandbox | [Source 1, lines 121–129](../archive/sources/flex-investigation-agent-source-1/content.md) |
| Linear Agent | `unknown`; considered execution interfaces are not a documented deployed sandbox | [Source 1, lines 74–78](../archive/sources/linear-agent-source-1/content.md), [source 2](../archive/sources/linear-agent-source-2/content.md), [source 3](../archive/sources/linear-agent-source-3/content.md), [source 6](../archive/sources/linear-agent-source-6/content.md) |
| Replit manager agent | Documented microVMs, remote filesystem and access controls | [Source 1, line 34](../archive/sources/replit-manager-agent-source-1/content.md) |
| Slack context system | Omitted inapplicable sandbox and its claim metadata/evidence | [Source 1, lines 34–38](../archive/sources/slack-context-system-source-1/content.md) |
| Stripe Minions | Pre-warmed EC2 devboxes in QA, no production/user-data/arbitrary-egress access | [Part 2, lines 24–30 and 84](../archive/sources/stripe-minions-source-2/content.md) |
| Uber coding agent | `unknown`; secondary report gives output and review, not runtime | [Source 1, lines 18–26](../archive/sources/uber-coding-agent-source-1/content.md) |
| Y Combinator infrastructure | `unknown`; internal harness discussion lacks a concrete execution environment | [Podcast capture](../archive/sources/ycombinator-agent-infra-source-1/content.md) |

A further consistency correction separates HubSpot's historical Crucible Kubernetes reviewer from its Aviator replacement. The latter's execution isolation is undocumented, so its current sandbox is `unknown`. [Migration description, lines 24–45](../archive/sources/hubspot-sidekick-source-1/content.md). After these corrections, 16 approaches document concrete current execution environments under the catalog's counting convention.

## Completion and remaining gaps by approach

“0 original metrics” means the record is outside the metric pass, not that its nonmetric claims were verified. Each nonzero row accounts for every original metric in that record, including duplicate headline/key-metric statements.

| Approach | Completion, corrections, and gaps |
| --- | --- |
| [airbnb-airchat](../data/agents/airbnb-airchat.yaml) | 3/3 reviewed. Removed original key_metrics.1: the cited newsletter does not report 60% engineer onboarding in 12 months. Its 64% PR figure is explicitly tied to an October 2025 talk; secondary attribution remains low confidence. No raw PR cohort or independent count. |
| [atlassian-rovo-dev](../data/agents/atlassian-rovo-dev.yaml) | 3/3 reviewed. Repository evaluation and ModernBERT training-comment dataset are separate scopes. Over-a-year duration is reported; exact interval, repository cohort definition, and dataset export remain unavailable. |
| [block-builderbot](../data/agents/block-builderbot.yaml) | 4/4 reviewed. Weekly PR share and daily operations have locators; operations are undefined. Months-to-days is a qualitative company opinion, reclassified from metric. Sandbox remains unknown after source review. |
| [brex-agent-platform](../data/agents/brex-agent-platform.yaml) | 5/5 reviewed. Dispute figure covers preparing submissions, not settlement. QA covers support interactions; the source does not substantiate the previous sample-based wording. Exact samples, accuracy test protocol, and measurement periods remain missing. |
| [browserbase-bb](../data/agents/browserbase-bb.yaml) | 4/4 reviewed. Feature scanning covers closed tickets and meeting transcripts. The awkward 99% first-response wording lacks raw times. A Slack request replaces manual log-diving; automated end-to-end investigation latency is not measured. |
| [cloudflare-ai-stack](../data/agents/cloudflare-ai-stack.yaml) | 5/5 reviewed. Traffic and adoption refer to the preceding 30 days; 10,952 is the week of March 23, distinct from the rolling average. Employee denominator and Gateway counts are documented. No causal isolation of AI impact. |
| [coinbase-forge-mux](../data/agents/coinbase-forge-mux.yaml) | 2/2 reviewed. 600+ includes engineers, PMs, and designers, with 335 active and 197 power users. Removed unsupported April label. Active/power-user definitions and measurement window are missing; source warns about selection bias. |
| [databricks-costar](../data/agents/databricks-costar.yaml) | No original metric claims. Nonmetric evidence was not part of this metric traceability pass. |
| [domu-clementino](../data/agents/domu-clementino.yaml) | 2/2 reviewed. Approximately 35 is toolkit integration modules, organized into skills. No inventory version or dated measurement cutoff. |
| [doordash-code-review](../data/agents/doordash-code-review.yaml) | 3/3 reviewed. Weekly PR reviews and settled high/critical action rate have exact locators; sample is 2,256 findings. Action rate does not measure missed bugs; calendar window unavailable. |
| [doordash-flux](../data/agents/doordash-flux.yaml) | 4/4 reviewed. August 11 is the dated announcement, not the unspecified one-month measurement window. Weekly review and playbook counts are distinct; task definitions and deduplication remain unclear. |
| [dropbox-nova](../data/agents/dropbox-nova.yaml) | 4/4 reviewed. Thousands of migration entries belong to the predecessor Goose migrator. Deflaker runs each proposed fix 100+ times according to flake rate, with bounded retries. Dozens of agents is a qualitative orchestration description, not an observed concurrency benchmark. |
| [flex-investigation-agent](../data/agents/flex-investigation-agent.yaml) | No original metric claims. Reviewed architecture sources: partner data isolation is documented, but an execution sandbox is not; sandbox normalized to unknown. |
| [github-qubot](../data/agents/github-qubot.yaml) | 3/3 reviewed. Hundreds of users/thousands of queries are qualitative counts without a window. Falling Slack question volume reclassified as a qualitative fact; no before/after counts. |
| [harvey-spectre](../data/agents/harvey-spectre.yaml) | No original metric claims. Nonmetric evidence was not part of this metric traceability pass. |
| [hubspot-sidekick](../data/agents/hubspot-sidekick.yaml) | 4/4 reviewed. Over 80% is reactions in the past couple months, not all engineers over six months. Reactions and feedback-time measures have scopes; sample and raw latency missing. Corrected Aviator/Crucible migration; current reviewer sandbox unknown. |
| [linear-agent](../data/agents/linear-agent.yaml) | No original metric claims. Sources reviewed for sandbox: lower-level execution interfaces were considered, but no concrete deployed sandbox is documented. Normalized to unknown. |
| [microsoft-prassistant](../data/agents/microsoft-prassistant.yaml) | 4/4 reviewed. 600,000 is pull requests impacted, not a count of review executions; 5,000 repositories refers to early evaluation. No exact measurement interval or coverage denominator count. |
| [monday-sphera-atlas-morphex](../data/agents/monday-sphera-atlas-morphex.yaml) | 5/5 reviewed. 90% applies to Builders; annual adoption trend is explicit in line 22. Morphex automatic merges differ from the broader top-agent cohort and its filtered revert rate. Missing sample sizes/windows; no universal success-rate inference. |
| [notion-custom-agents](../data/agents/notion-custom-agents.yaml) | 4/4 reviewed. Internal alpha agents exclude customer alpha agents. Security-team activity reclassified as qualitative fact. Participant rebuild estimates vary from three to five across harness/framework/feature; no precise inventory. |
| [plaid-ai-annotator](../data/agents/plaid-ai-annotator.yaml) | 3/3 reviewed. Early transaction labels align with humans above 95%; no sample, evaluator protocol, or actual cost/time data. Cheaper/faster remains a qualitative self-report. |
| [plaid-fix-my-connection](../data/agents/plaid-fix-my-connection.yaml) | 3/3 reviewed. Counts concern logins enabled by automated bank-connection repairs. No measurement window, baseline repair duration, or independent quality check. |
| [plaid-internal-mcp-server](../data/agents/plaid-internal-mcp-server.yaml) | 3/3 reviewed. Corrected summary and metrics: over 80% applies to Claude Code/Cursor users, not internal MCP adoption. Thousands of tool calls/dozens of agents concern the server. Missing server adoption denominator and window. |
| [posthog-stamphog](../data/agents/posthog-stamphog.yaml) | 4/4 reviewed. Kept the quarterly main-repository share, previous-month count in the July 9 report, and July 28 PR share/token cost separate. July 9 is an observation date, not an invented rolling interval. Exact period/cohort comparability unresolved. |
| [ramp-inspect](../data/agents/ramp-inspect.yaml) | 12/12 reviewed. Corrected 60% from April to January 2026; kept 75% by May and million sessions in July. Older 30% is frontend/backend repositories; 90% is the Inspect repository. Removed unsupported August labels; agent examples and startup target reclassified as fact/opinion. Code-volume method and several observation cutoffs missing. |
| [replit-manager-agent](../data/agents/replit-manager-agent.yaml) | 3/3 reviewed. 2.9x is a consistent author cohort; whole-company lines of code rose 5.8x. Early January–late June is stated without a year in the body. Quality trends do not independently establish causation. Source-backed microVM environment added. |
| [retool-retoolgpt](../data/agents/retool-retoolgpt.yaml) | No original metric claims. Nonmetric evidence was not part of this metric traceability pass. |
| [salesforce-slackbot](../data/agents/salesforce-slackbot.yaml) | No original metric claims. Nonmetric evidence was not part of this metric traceability pass. |
| [sentry-junior](../data/agents/sentry-junior.yaml) | 3/3 reviewed. Lines of code exclude tests, evals, docs, and lockfiles. Four months is author-reported effort before the writeup; no dated code revision or reproducible LOC command. Apache license linked separately. |
| [shopify-internal-agents](../data/agents/shopify-internal-agents.yaml) | 4/4 reviewed. Session/channel/PR counts refer to a recent 30-day window and the river_sessions table. Median duration/tool calls and company-wide merged-PR share stay scoped separately. Exact date boundaries and full PR denominator unavailable. |
| [sierra-pinecone](../data/agents/sierra-pinecone.yaml) | 4/4 reviewed. 600 people and 75,000+ sessions are in the preceding month, not cumulative lifetime totals; 70% concerns opened PRs in that month. Removed unsupported July label and original key_metrics.2 (hundreds of automations), absent from the capture. |
| [slack-context-system](../data/agents/slack-context-system.yaml) | 2/2 reviewed. Hundreds of requests/megabytes describe investigation workload scale, not a measured guarantee against overflow. Inapplicable sandbox and its evidence removed. No capacity benchmark or calendar measurement window. |
| [spotify-honk-xirp](../data/agents/spotify-honk-xirp.yaml) | 4/4 reviewed. Removed unsupported June 2026 dates for cumulative Honk PR counts. Wider Fleet Management automation applies since mid-2024, including deterministic changes. Selected migration time savings are not all engineering work; exact comparison method unavailable. |
| [stripe-minions](../data/agents/stripe-minions.yaml) | 2/2 reviewed. Part 1 over 1,000 and Part 2 over 1,300 completely minion-produced merged PRs/week retained as earlier/later reports. Both require human review; no calendar measurement cutoff in captured articles. EC2 devboxes, goose blueprints, Toolshed and QA isolation reconciled. Community doubts remain context. |
| [uber-coding-agent](../data/agents/uber-coding-agent.yaml) | 3/3 reviewed. Human-reviewed agent-authored changes differ from broad monthly AI-tool adoption. Secondary reporting of CTO statements remains limited; measurement windows and agent runtime missing. Sandbox normalized to unknown. |
| [uber-ureview](../data/agents/uber-ureview.yaml) | 6/6 reviewed. Preserved internal weekly/monthly conflict with low confidence and separate contradicting locators. Useful/addressed rates have different denominators and methods. Rounded modeled time savings do not reconcile exactly; no observed time-saved experiment. |
| [workos-project-horizon](../data/agents/workos-project-horizon.yaml) | No original metric claims. Nonmetric evidence was not part of this metric traceability pass. |
| [ycombinator-agent-infra](../data/agents/ycombinator-agent-infra.yaml) | No original metric claims. Podcast transcript reviewed for execution infrastructure; no concrete sandbox implementation documented. Normalized to unknown. |
| [zup-codegen](../data/agents/zup-codegen.yaml) | No original metric claims. Nonmetric evidence was not part of this metric traceability pass. |

## Failures, costs, and counterevidence

These selected cases do not supply a catalog-wide failure rate. They retain the system version and workflow where the limitation occurred.

| Case | Observed limitation in preserved reporting | Evidence |
| --- | --- | --- |
| DoorDash code review | Specialist-agent v1 missed architectural issues; two-reviewer v2 still lost findings. Repeated model requests bypassed turn counting and consumed up to 20 minutes before timeout; weaker models retried invalid JSON. Per-agent timeouts and staged investigation addressed specific problems. | [Source 1, lines 38–42 and 162–164](../archive/sources/doordash-code-review-source-1/content.md) |
| Dropbox migration predecessor | Goose migrator failures lacked a practical interactive recovery path. Nova added interactive sessions and shared controls. Thousands of migration entries are predecessor results. | [Source 1, lines 65–69](../archive/sources/dropbox-nova-source-1/content.md) |
| HubSpot code review predecessor | Per-review Kubernetes startup added latency, cost, operational friction, and shell-based configuration difficulty. The reviewer moved from Crucible to Aviator. | [Source 1, lines 24–45](../archive/sources/hubspot-sidekick-source-1/content.md) |
| Stripe Minions | A branch still failing after the second CI run returns for manual scrutiny. The cap addresses token, compute, and time costs; incomplete runs may still be useful to engineers. | [Part 2, lines 96–98](../archive/sources/stripe-minions-source-2/content.md), [Part 1, lines 48–50](../archive/sources/stripe-minions-source-1/content.md) |
| Ramp Inspect v1 | The visual-editing extension saw little adoption: developers could edit directly and nondevelopers faced local environment setup. The later remote environment is a different iteration. | [Interview, lines 82–86](../archive/sources/ramp-inspect-source-5/content.md) |
| monday agent memory | Context stuffing and vector retrieval over prior sessions worked poorly in the reported workflow. The team used memory/diary files and acknowledged delayed eval investment. | [Source 1, lines 118–120 and 186–188](../archive/sources/monday-sphera-atlas-morphex-source-1/content.md) |
| Sentry Junior engineering cost | The author reports four months and around 100,000 TypeScript lines, with more ongoing effort than expected. This is maintenance cost evidence, not a failed deployment. | [Source 1, lines 10–22 and 353](../archive/sources/sentry-junior-source-1/content.md) |
| Spotify review pressure | Increased coding output shifted work toward human decisions and review; the source reports 76% more PRs to review. It does not isolate Honk as the cause or quantify escaped defects. | [Source 2, lines 106–112](../archive/sources/spotify-honk-xirp-source-2/content.md) |
| Uber uReview internal inconsistency | The opening reports about 65,000 diffs weekly, but the cost discussion says 65,000 monthly. Both are present in the same snapshot. The headline and coverage claim now have low confidence and separate supporting/contradicting locators. The source's roughly 1,500 saved hours also does not exactly reconcile with its rounded commit count and 10-minute assumption. | [Source 1, lines 34, 104 and 120](../archive/sources/uber-ureview-source-1/content.md) |

The two `contradicts` links concern the same unresolved weekly/monthly inconsistency in one Uber article, repeated on the headline and coverage claim. They are not two independent counter-studies. The passage does not resolve which period is correct; displayed text preserves the conflict rather than choosing a winner.

Stripe community comments ask for example PRs, review substance, maintained output, and value beyond raw PR counts. They remain `contextualizes`: speculation about defects or wasted reviewer time is not verified counterevidence to Stripe's scoped count. [Examples/review comment, line 12](../archive/sources/stripe-minions-source-4/content.md), [detail question, lines 12–14](../archive/sources/stripe-minions-source-5/content.md), [shipping/maintenance question, line 12](../archive/sources/stripe-minions-source-6/content.md), [PR-value critique, lines 12–14](../archive/sources/stripe-minions-source-7/content.md). Block's captured community thread only points to a repository; it supplies no measured negative result. [Thread, lines 16–18](../archive/sources/block-builderbot-source-4/content.md).

No independently verified retirement of a cataloged deployed system was established in this bounded pass. Predecessor replacements, unfinished designs, operational cost, skeptical comments, and direct conflicting measurements remain distinct outcomes.

### Unpreserved follow-up lead

Reviewed live on 2026-09-09: DoorDash's [How we learned to trust our AI code reviewer](https://careersatdoordash.com/blog/how-we-learned-to-trust-our-ai-code-reviewer-at-doordash/) (published July 6, 2026). “Why the obvious signals lie” discusses acceptance metrics missing false negatives; “Staging benefits” describes the cost/latency tradeoff of broader coverage. This is a research lead only: it has no repository capture and adds no catalog source or numeric claim. Preserve and review it before promotion.

## Ledger of the original 115 metric claims

Original IDs refer to the baseline export. No remaining key-metric indices shifted: both removed entries were the final item in their respective lists. The table records each original claim's disposition and exact supporting source locator in the final export. Full corrected text and structured metadata are in the linked YAML and generated JSON. Reclassified claims remain source-linked.

| Original claim ID | Disposition | Supporting passage after review |
| --- | --- | --- |
| `airbnb-airchat--headline-metric` | Retained metric | [airbnb-airchat-source-3](../archive/sources/airbnb-airchat-source-3/content.md): lines 16, 24, 194 |
| `airbnb-airchat--key-metrics-0` | Retained metric | [airbnb-airchat-source-3](../archive/sources/airbnb-airchat-source-3/content.md): lines 16, 24, 194 |
| `airbnb-airchat--key-metrics-1` | Removed: cited newsletter does not report 60% engineer onboarding within 12 months | No supporting passage for the original claim; removed |
| `atlassian-rovo-dev--headline-metric` | Retained metric | [atlassian-rovo-dev-source-2](../archive/sources/atlassian-rovo-dev-source-2/content.md): lines 66, 87 |
| `atlassian-rovo-dev--key-metrics-0` | Retained metric | [atlassian-rovo-dev-source-2](../archive/sources/atlassian-rovo-dev-source-2/content.md): lines 87 |
| `atlassian-rovo-dev--key-metrics-1` | Retained metric | [atlassian-rovo-dev-source-2](../archive/sources/atlassian-rovo-dev-source-2/content.md): lines 66 |
| `block-builderbot--headline-metric` | Retained metric | [block-builderbot-source-1](../archive/sources/block-builderbot-source-1/content.md): lines 24 |
| `block-builderbot--key-metrics-0` | Retained metric | [block-builderbot-source-1](../archive/sources/block-builderbot-source-1/content.md): lines 24 |
| `block-builderbot--key-metrics-1` | Retained metric | [block-builderbot-source-1](../archive/sources/block-builderbot-source-1/content.md): lines 24 |
| `block-builderbot--key-metrics-2` | Reclassified as opinion | [block-builderbot-source-1](../archive/sources/block-builderbot-source-1/content.md): lines 24–26 |
| `brex-agent-platform--headline-metric` | Retained metric | [brex-agent-platform-source-1](../archive/sources/brex-agent-platform-source-1/content.md): lines 179–189 |
| `brex-agent-platform--key-metrics-0` | Retained metric | [brex-agent-platform-source-1](../archive/sources/brex-agent-platform-source-1/content.md): lines 76 |
| `brex-agent-platform--key-metrics-1` | Retained metric | [brex-agent-platform-source-1](../archive/sources/brex-agent-platform-source-1/content.md): lines 179–189 |
| `brex-agent-platform--key-metrics-2` | Retained metric; wording/scope corrected | [brex-agent-platform-source-1](../archive/sources/brex-agent-platform-source-1/content.md): lines 80 |
| `brex-agent-platform--key-metrics-3` | Retained metric | [brex-agent-platform-source-1](../archive/sources/brex-agent-platform-source-1/content.md): lines 163–167 |
| `browserbase-bb--headline-metric` | Retained metric | [browserbase-bb-source-1](../archive/sources/browserbase-bb-source-1/content.md): lines 26 |
| `browserbase-bb--key-metrics-0` | Retained metric | [browserbase-bb-source-1](../archive/sources/browserbase-bb-source-1/content.md): lines 26 |
| `browserbase-bb--key-metrics-1` | Retained metric | [browserbase-bb-source-1](../archive/sources/browserbase-bb-source-1/content.md): lines 26 |
| `browserbase-bb--key-metrics-2` | Retained metric | [browserbase-bb-source-1](../archive/sources/browserbase-bb-source-1/content.md): lines 26 |
| `cloudflare-ai-stack--headline-metric` | Retained metric | [cloudflare-ai-stack-source-1](../archive/sources/cloudflare-ai-stack-source-1/content.md): lines 14–20 |
| `cloudflare-ai-stack--key-metrics-0` | Retained metric | [cloudflare-ai-stack-source-1](../archive/sources/cloudflare-ai-stack-source-1/content.md): lines 14–16 |
| `cloudflare-ai-stack--key-metrics-1` | Retained metric; wording/scope corrected | [cloudflare-ai-stack-source-1](../archive/sources/cloudflare-ai-stack-source-1/content.md): lines 14–20 |
| `cloudflare-ai-stack--key-metrics-2` | Retained metric; wording/scope corrected | [cloudflare-ai-stack-source-1](../archive/sources/cloudflare-ai-stack-source-1/content.md): lines 25–29 |
| `cloudflare-ai-stack--key-metrics-3` | Retained metric | [cloudflare-ai-stack-source-1](../archive/sources/cloudflare-ai-stack-source-1/content.md): lines 14–18 |
| `coinbase-forge-mux--headline-metric` | Retained metric; wording/scope corrected | [coinbase-forge-mux-source-1](../archive/sources/coinbase-forge-mux-source-1/content.md): lines 24–34 |
| `coinbase-forge-mux--key-metrics-0` | Retained metric; wording/scope corrected | [coinbase-forge-mux-source-1](../archive/sources/coinbase-forge-mux-source-1/content.md): lines 24–34 |
| `domu-clementino--headline-metric` | Retained metric | [domu-clementino-source-1](../archive/sources/domu-clementino-source-1/content.md): lines 58–60 |
| `domu-clementino--key-metrics-0` | Retained metric | [domu-clementino-source-1](../archive/sources/domu-clementino-source-1/content.md): lines 58–60 |
| `doordash-code-review--headline-metric` | Retained metric | [doordash-code-review-source-1](../archive/sources/doordash-code-review-source-1/content.md): lines 23 |
| `doordash-code-review--key-metrics-0` | Retained metric | [doordash-code-review-source-1](../archive/sources/doordash-code-review-source-1/content.md): lines 23 |
| `doordash-code-review--key-metrics-1` | Retained metric | [doordash-code-review-source-1](../archive/sources/doordash-code-review-source-1/content.md): lines 27 |
| `doordash-flux--headline-metric` | Retained metric | [doordash-flux-source-1](../archive/sources/doordash-flux-source-1/content.md): lines 10–12 |
| `doordash-flux--key-metrics-0` | Retained metric | [doordash-flux-source-1](../archive/sources/doordash-flux-source-1/content.md): lines 10–12 |
| `doordash-flux--key-metrics-1` | Retained metric | [doordash-flux-source-1](../archive/sources/doordash-flux-source-1/content.md): lines 10–12 |
| `doordash-flux--key-metrics-2` | Retained metric | [doordash-flux-source-3](../archive/sources/doordash-flux-source-3/content.md): lines 10 |
| `dropbox-nova--headline-metric` | Retained metric | [dropbox-nova-source-1](../archive/sources/dropbox-nova-source-1/content.md): lines 65–69 |
| `dropbox-nova--key-metrics-0` | Retained metric | [dropbox-nova-source-1](../archive/sources/dropbox-nova-source-1/content.md): lines 58–62 |
| `dropbox-nova--key-metrics-1` | Retained metric; wording/scope corrected | [dropbox-nova-source-1](../archive/sources/dropbox-nova-source-1/content.md): lines 65–69 |
| `dropbox-nova--key-metrics-2` | Retained metric | [dropbox-nova-source-1](../archive/sources/dropbox-nova-source-1/content.md): lines 65–69 |
| `github-qubot--headline-metric` | Retained metric | [github-qubot-source-1](../archive/sources/github-qubot-source-1/content.md): lines 70 |
| `github-qubot--key-metrics-0` | Retained metric | [github-qubot-source-1](../archive/sources/github-qubot-source-1/content.md): lines 70 |
| `github-qubot--key-metrics-1` | Reclassified as fact | [github-qubot-source-1](../archive/sources/github-qubot-source-1/content.md): lines 70 |
| `hubspot-sidekick--headline-metric` | Retained metric | [hubspot-sidekick-source-1](../archive/sources/hubspot-sidekick-source-1/content.md): lines 14–18 |
| `hubspot-sidekick--key-metrics-0` | Retained metric | [hubspot-sidekick-source-1](../archive/sources/hubspot-sidekick-source-1/content.md): lines 14 |
| `hubspot-sidekick--key-metrics-1` | Retained metric | [hubspot-sidekick-source-1](../archive/sources/hubspot-sidekick-source-1/content.md): lines 14–18 |
| `hubspot-sidekick--key-metrics-2` | Retained metric; wording/scope corrected | [hubspot-sidekick-source-1](../archive/sources/hubspot-sidekick-source-1/content.md): lines 99–116 |
| `microsoft-prassistant--headline-metric` | Retained metric; wording/scope corrected | [microsoft-prassistant-source-1](../archive/sources/microsoft-prassistant-source-1/content.md): lines 10 |
| `microsoft-prassistant--key-metrics-0` | Retained metric | [microsoft-prassistant-source-1](../archive/sources/microsoft-prassistant-source-1/content.md): lines 10 |
| `microsoft-prassistant--key-metrics-1` | Retained metric; wording/scope corrected | [microsoft-prassistant-source-1](../archive/sources/microsoft-prassistant-source-1/content.md): lines 10 |
| `microsoft-prassistant--key-metrics-2` | Retained metric | [microsoft-prassistant-source-1](../archive/sources/microsoft-prassistant-source-1/content.md): lines 35 |
| `monday-sphera-atlas-morphex--headline-metric` | Retained metric | [monday-sphera-atlas-morphex-source-1](../archive/sources/monday-sphera-atlas-morphex-source-1/content.md): lines 148–152 |
| `monday-sphera-atlas-morphex--key-metrics-0` | Retained metric | [monday-sphera-atlas-morphex-source-1](../archive/sources/monday-sphera-atlas-morphex-source-1/content.md): lines 148–152 |
| `monday-sphera-atlas-morphex--key-metrics-1` | Retained metric; wording/scope corrected | [monday-sphera-atlas-morphex-source-1](../archive/sources/monday-sphera-atlas-morphex-source-1/content.md): lines 10, 16, 22 |
| `monday-sphera-atlas-morphex--key-metrics-2` | Retained metric; wording/scope corrected | [monday-sphera-atlas-morphex-source-1](../archive/sources/monday-sphera-atlas-morphex-source-1/content.md): lines 10, 23 |
| `monday-sphera-atlas-morphex--key-metrics-3` | Retained metric | [monday-sphera-atlas-morphex-source-1](../archive/sources/monday-sphera-atlas-morphex-source-1/content.md): lines 154–158 |
| `notion-custom-agents--headline-metric` | Retained metric | [notion-custom-agents-source-2](../archive/sources/notion-custom-agents-source-2/content.md): lines 51 |
| `notion-custom-agents--key-metrics-0` | Retained metric | [notion-custom-agents-source-2](../archive/sources/notion-custom-agents-source-2/content.md): lines 51 |
| `notion-custom-agents--key-metrics-1` | Reclassified as fact | [notion-custom-agents-source-2](../archive/sources/notion-custom-agents-source-2/content.md): lines 57 |
| `notion-custom-agents--key-metrics-2` | Retained metric | [notion-custom-agents-source-1](../archive/sources/notion-custom-agents-source-1/content.md): lines 115, 275–277, 819 |
| `plaid-ai-annotator--headline-metric` | Retained metric | [plaid-ai-annotator-source-1](../archive/sources/plaid-ai-annotator-source-1/content.md): lines 16–20 |
| `plaid-ai-annotator--key-metrics-0` | Retained metric | [plaid-ai-annotator-source-1](../archive/sources/plaid-ai-annotator-source-1/content.md): lines 16–20 |
| `plaid-ai-annotator--key-metrics-1` | Retained metric | [plaid-ai-annotator-source-1](../archive/sources/plaid-ai-annotator-source-1/content.md): lines 20 |
| `plaid-fix-my-connection--headline-metric` | Retained metric | [plaid-fix-my-connection-source-1](../archive/sources/plaid-fix-my-connection-source-1/content.md): lines 26–32 |
| `plaid-fix-my-connection--key-metrics-0` | Retained metric | [plaid-fix-my-connection-source-1](../archive/sources/plaid-fix-my-connection-source-1/content.md): lines 26–32 |
| `plaid-fix-my-connection--key-metrics-1` | Retained metric | [plaid-fix-my-connection-source-1](../archive/sources/plaid-fix-my-connection-source-1/content.md): lines 26–32 |
| `plaid-internal-mcp-server--headline-metric` | Retained metric; wording/scope corrected | [plaid-internal-mcp-server-source-1](../archive/sources/plaid-internal-mcp-server-source-1/content.md): lines 38, 89 |
| `plaid-internal-mcp-server--key-metrics-0` | Retained metric; wording/scope corrected | [plaid-internal-mcp-server-source-1](../archive/sources/plaid-internal-mcp-server-source-1/content.md): lines 38, 89 |
| `plaid-internal-mcp-server--key-metrics-1` | Retained metric | [plaid-internal-mcp-server-source-1](../archive/sources/plaid-internal-mcp-server-source-1/content.md): lines 89 |
| `posthog-stamphog--headline-metric` | Retained metric; wording/scope corrected | [posthog-stamphog-source-1](../archive/sources/posthog-stamphog-source-1/content.md): lines 105, 118 |
| `posthog-stamphog--key-metrics-0` | Retained metric; wording/scope corrected | [posthog-stamphog-source-1](../archive/sources/posthog-stamphog-source-1/content.md): lines 118 |
| `posthog-stamphog--key-metrics-1` | Retained metric | [posthog-stamphog-source-1](../archive/sources/posthog-stamphog-source-1/content.md): lines 105 |
| `posthog-stamphog--key-metrics-2` | Retained metric | [posthog-stamphog-source-2](../archive/sources/posthog-stamphog-source-2/content.md): lines 131 |
| `ramp-inspect--headline-metric` | Retained metric | [ramp-inspect-source-5](../archive/sources/ramp-inspect-source-5/content.md): lines 58–68 |
| `ramp-inspect--key-metrics-0` | Retained metric; wording/scope corrected | [ramp-inspect-source-5](../archive/sources/ramp-inspect-source-5/content.md): lines 58–68 |
| `ramp-inspect--key-metrics-1` | Retained metric | [ramp-inspect-source-5](../archive/sources/ramp-inspect-source-5/content.md): lines 58–68; [ramp-inspect-source-2](../archive/sources/ramp-inspect-source-2/content.md): lines 10 |
| `ramp-inspect--key-metrics-2` | Retained metric; wording/scope corrected | [ramp-inspect-source-1](../archive/sources/ramp-inspect-source-1/content.md): lines 24 |
| `ramp-inspect--key-metrics-3` | Retained metric; wording/scope corrected | [ramp-inspect-source-5](../archive/sources/ramp-inspect-source-5/content.md): lines 96–102 |
| `ramp-inspect--key-metrics-4` | Retained metric | [ramp-inspect-source-5](../archive/sources/ramp-inspect-source-5/content.md): lines 66–72 |
| `ramp-inspect--key-metrics-5` | Retained metric | [ramp-inspect-source-5](../archive/sources/ramp-inspect-source-5/content.md): lines 100 |
| `ramp-inspect--key-metrics-6` | Reclassified as fact | [ramp-inspect-source-5](../archive/sources/ramp-inspect-source-5/content.md): lines 134–141 |
| `ramp-inspect--key-metrics-7` | Retained metric; wording/scope corrected | [ramp-inspect-source-5](../archive/sources/ramp-inspect-source-5/content.md): lines 102 |
| `ramp-inspect--key-metrics-8` | Retained metric | [ramp-inspect-source-5](../archive/sources/ramp-inspect-source-5/content.md): lines 101 |
| `ramp-inspect--key-metrics-9` | Retained metric | [ramp-inspect-source-5](../archive/sources/ramp-inspect-source-5/content.md): lines 111 |
| `ramp-inspect--key-metrics-10` | Reclassified as opinion; wording/scope corrected | [ramp-inspect-source-1](../archive/sources/ramp-inspect-source-1/content.md): lines 22 |
| `replit-manager-agent--headline-metric` | Retained metric; wording/scope corrected | [replit-manager-agent-source-1](../archive/sources/replit-manager-agent-source-1/content.md): lines 10, 38–56 |
| `replit-manager-agent--key-metrics-0` | Retained metric; wording/scope corrected | [replit-manager-agent-source-1](../archive/sources/replit-manager-agent-source-1/content.md): lines 10, 38–56 |
| `replit-manager-agent--key-metrics-1` | Retained metric | [replit-manager-agent-source-1](../archive/sources/replit-manager-agent-source-1/content.md): lines 50–56 |
| `sentry-junior--headline-metric` | Retained metric | [sentry-junior-source-1](../archive/sources/sentry-junior-source-1/content.md): lines 10–24, 34–60; [sentry-junior-source-4](../archive/sources/sentry-junior-source-4/content.md): lines 412–414 |
| `sentry-junior--key-metrics-0` | Retained metric; wording/scope corrected | [sentry-junior-source-1](../archive/sources/sentry-junior-source-1/content.md): lines 22 |
| `sentry-junior--key-metrics-1` | Retained metric | [sentry-junior-source-1](../archive/sources/sentry-junior-source-1/content.md): lines 10–22 |
| `shopify-internal-agents--headline-metric` | Retained metric | [shopify-internal-agents-source-1](../archive/sources/shopify-internal-agents-source-1/content.md): lines 12 |
| `shopify-internal-agents--key-metrics-0` | Retained metric | [shopify-internal-agents-source-1](../archive/sources/shopify-internal-agents-source-1/content.md): lines 83 |
| `shopify-internal-agents--key-metrics-1` | Retained metric | [shopify-internal-agents-source-1](../archive/sources/shopify-internal-agents-source-1/content.md): lines 12, 83 |
| `shopify-internal-agents--key-metrics-2` | Retained metric | [shopify-internal-agents-source-1](../archive/sources/shopify-internal-agents-source-1/content.md): lines 65 |
| `sierra-pinecone--headline-metric` | Retained metric; wording/scope corrected | [sierra-pinecone-source-1](../archive/sources/sierra-pinecone-source-1/content.md): lines 134–139 |
| `sierra-pinecone--key-metrics-0` | Retained metric; wording/scope corrected | [sierra-pinecone-source-1](../archive/sources/sierra-pinecone-source-1/content.md): lines 134–139 |
| `sierra-pinecone--key-metrics-1` | Retained metric; wording/scope corrected | [sierra-pinecone-source-1](../archive/sources/sierra-pinecone-source-1/content.md): lines 138 |
| `sierra-pinecone--key-metrics-2` | Removed: hundreds of automations absent from the cited capture | No supporting passage for the original claim; removed |
| `slack-context-system--headline-metric` | Retained metric; wording/scope corrected | [slack-context-system-source-1](../archive/sources/slack-context-system-source-1/content.md): lines 34–38; [slack-context-system-source-2](../archive/sources/slack-context-system-source-2/content.md): lines 22 |
| `slack-context-system--key-metrics-0` | Retained metric | [slack-context-system-source-1](../archive/sources/slack-context-system-source-1/content.md): lines 34–38; [slack-context-system-source-2](../archive/sources/slack-context-system-source-2/content.md): lines 22 |
| `spotify-honk-xirp--headline-metric` | Retained metric | [spotify-honk-xirp-source-1](../archive/sources/spotify-honk-xirp-source-1/content.md): lines 70 |
| `spotify-honk-xirp--key-metrics-0` | Retained metric | [spotify-honk-xirp-source-1](../archive/sources/spotify-honk-xirp-source-1/content.md): lines 70 |
| `spotify-honk-xirp--key-metrics-1` | Retained metric | [spotify-honk-xirp-source-1](../archive/sources/spotify-honk-xirp-source-1/content.md): lines 70–77 |
| `spotify-honk-xirp--key-metrics-2` | Retained metric; wording/scope corrected | [spotify-honk-xirp-source-1](../archive/sources/spotify-honk-xirp-source-1/content.md): lines 22–38 |
| `stripe-minions--headline-metric` | Retained metric; wording/scope corrected | [stripe-minions-source-2](../archive/sources/stripe-minions-source-2/content.md): lines 12 |
| `stripe-minions--key-metrics-0` | Retained metric; wording/scope corrected | [stripe-minions-source-1](../archive/sources/stripe-minions-source-1/content.md): lines 14 |
| `uber-coding-agent--headline-metric` | Retained metric | [uber-coding-agent-source-1](../archive/sources/uber-coding-agent-source-1/content.md): lines 24–26 |
| `uber-coding-agent--key-metrics-0` | Retained metric | [uber-coding-agent-source-1](../archive/sources/uber-coding-agent-source-1/content.md): lines 24–26 |
| `uber-coding-agent--key-metrics-1` | Retained metric | [uber-coding-agent-source-1](../archive/sources/uber-coding-agent-source-1/content.md): lines 18 |
| `uber-ureview--headline-metric` | Retained metric; wording/scope corrected | [uber-ureview-source-1](../archive/sources/uber-ureview-source-1/content.md): lines 34, 98 |
| `uber-ureview--key-metrics-0` | Retained metric; wording/scope corrected | [uber-ureview-source-1](../archive/sources/uber-ureview-source-1/content.md): lines 34 |
| `uber-ureview--key-metrics-1` | Retained metric | [uber-ureview-source-1](../archive/sources/uber-ureview-source-1/content.md): lines 76, 98 |
| `uber-ureview--key-metrics-2` | Retained metric | [uber-ureview-source-1](../archive/sources/uber-ureview-source-1/content.md): lines 82, 98 |
| `uber-ureview--key-metrics-3` | Retained metric | [uber-ureview-source-1](../archive/sources/uber-ureview-source-1/content.md): lines 94 |
| `uber-ureview--key-metrics-4` | Retained metric | [uber-ureview-source-1](../archive/sources/uber-ureview-source-1/content.md): lines 104 |

## Verification boundary

Both metric batches passed YAML build validation and all 88 declared capture checks. Final output freshness, tests, lint/format, local links, and whitespace checks are run after integration with Plan 002's tooling fixes. Existing captures remain byte-for-byte unchanged. Future intake should attach precise locators immediately and preserve raw measurement definitions when the publisher supplies them.
