# Coverage backlog

This page tracks companies and reported internal-agent approaches that are **not yet** in the
catalog. Each candidate links to the primary sources found so far. A position on this page is not
a catalog entry. An entry is added only after a contributor writes the YAML record, links every
claim to a source, and runs `python3 scripts/build.py`.

The list comes from a coverage audit. The first pass ran on 2026-08-12. A follow-up pass ran on
2026-08-13. Both passes searched for gaps: companies that built or adapted an agent for their own
work but do not appear in the [landscape](landscape.md). They excluded the 25 companies already
cataloged.

The audit used adversarial verification. Each verified claim passed a three-vote check. Claims
that failed appear in [Refuted or excluded](#refuted-or-excluded) so contributors do not re-add
them.

## Promoted to the catalog

On 2026-08-13, seven Tier 1 entries moved off this backlog and into the
[landscape](landscape.md). Their detail blocks stay on this page as source collections.

- GitHub — Qubot → [landscape](landscape.md#github-qubot)
- Retool — RetoolGPT → [landscape](landscape.md#retool-retoolgpt)
- Atlassian — DOT → [landscape](landscape.md#atlassian-dot)
- Atlassian — Rovo Dev → [landscape](landscape.md#atlassian-rovo-dev)
- Notion — Custom Agents → [landscape](landscape.md#notion-custom-agents)
- Microsoft — PRAssistant → [landscape](landscape.md#microsoft-prassistant)
- Airbnb — Airchat → [landscape](landscape.md#airbnb-airchat)

## Editorial rule

A company that uses its **own shipping consumer product** internally does not qualify on that
basis alone. Such a story is product promotion, not an internal-agent build. The rule applies
strictly to consumer products that the company sells. Entries that straddle the line stay on this
page with a caveat and a case-by-case judgment when they become records.

## How to read the status

| Status | Meaning |
| --- | --- |
| Verified, ready | A first-party source documents the build. The claim passed three-vote verification. A contributor can write the YAML record. |
| Ready (single-pass) | Strong primary sources back the build, but it has not passed three-vote verification yet. Confirm before you write a record. |
| Border case | A source exists, but one inclusion rule is unclear. Examples: a commercial product whose internal dogfooding is thin, or heavy internal adaptation of a shipping product. Needs a catalog judgment. |
| Needs verification | A lead surfaced in search but did not pass full verification. Confirm the source and the dogfooding claim before you write a record. |

Confidence values follow the [data schema](../data/schema.md).

- **high**: a first-party engineering source, repository, talk, or paper documents the internal build.
- **medium**: an executive quote or a strong secondary source confirms the build, or a first-party source has one weak point.
- **low**: a rumor or an unattributed claim.

---

## Tier 1 — Product and engineering companies

These companies match the shape of the current catalog. They published engineering blogs, talks,
or repos that describe an agent they built for their own teams.

### GitHub — Qubot

- **Status**: Verified, ready.
- **Confidence**: high.
- **What it does**: Qubot is an internal data-analytics agent. Any GitHub employee can ask a
  question about the company data warehouse in plain language and get an answer in seconds.
- **Reported stage**: scaled. Hundreds of users run thousands of queries. The volume of data
  questions in internal Slack channels dropped.
- **Sources**:
  - [How we built an internal data analytics agent](https://github.blog/ai-and-ml/github-copilot/how-we-built-an-internal-data-analytics-agent/) — GitHub engineering blog, 2026-06-19. First-party.

### Retool — RetoolGPT

- **Status**: Verified, ready.
- **Confidence**: high.
- **What it does**: RetoolGPT is an internal assistant built on ChatGPT. It reads Retool's
  internal Confluence documents, Retool documentation, and Linear tickets.
- **Reported stage**: deployed across the team. Retool deployed it into a read-only environment so
  the whole team could use it.
- **Sources**:
  - [How we built RetoolGPT](https://retool.com/blog/how-we-built-retoolgpt) — Retool engineering blog, 2025-08-05. First-party.
  - [AI Build Week, Day 3 talk](https://www.youtube.com/watch?v=8VTdYUBAZsY) — YouTube.
  - [Retool Community thread](https://community.retool.com/t/ai-build-week-day-3-how-we-made-retoolgpt/59997).
  - [Retool post on X](https://x.com/retool/status/1953886454012141871).

### Atlassian — DOT (Design Org Teammate)

- **Status**: Verified, ready.
- **Confidence**: high.
- **What it does**: DOT is an internal agent for Atlassian's Design Operations team. It answers
  common tooling questions in the team help channel. The team built it in Rovo Studio, Atlassian's
  no-code agent builder, so Atlassian materially adapted its own platform.
- **Reported stage**: deployed and in use. Do not cite the "~70% of threads" or "zero unanswered"
  figures; see [Refuted or excluded](#refuted-or-excluded).
- **Sources**:
  - [How Design Ops built an AI teammate with no engineering lift](https://www.atlassian.com/blog/ai-at-work/how-design-ops-built-an-ai-teammate-with-no-engineering-lift) — Atlassian blog. First-party.

### Atlassian — Rovo Dev (RovoDev) and the HULA framework

- **Status**: Verified, ready.
- **Confidence**: high.
- **What it does**: Rovo Dev is an internal coding agent that works inside Jira. It runs a
  four-step cycle from the HULA framework: set context, generate a plan, generate code, and raise
  a pull request. Atlassian dogfooded it across all Jira sites for more than a year across 1,900+
  repositories, and used a 50,000-comment internal dataset to train the model. It later reached
  general availability.
- **Reported stage**: scaled internally, then commercialized.
- **Sources**:
  - [Improving the coding agent experience](https://www.atlassian.com/blog/atlassian-engineering/improving-coding-agent-experience) — Atlassian engineering blog. First-party.
  - [Developer productivity improved with Rovo Dev](https://www.atlassian.com/blog/atlassian-engineering/developer-productivity-improved-with-rovo-dev) — Atlassian engineering blog. First-party.
  - [HULA: Human-in-the-loop software development agents (arXiv 2411.12924)](https://arxiv.org/abs/2411.12924) — paper, 2024-11.

### Notion — Custom Agents platform

- **Status**: Verified, ready.
- **Confidence**: high.
- **What it does**: Notion built a Custom Agents platform and dogfoods it internally across
  non-engineering teams such as IT ticketing, supply chain, procurement, and recruiting. By the
  end of alpha testing, Notion had more than 3,000 internal Custom Agents. Notion's own security
  team is one of the most active internal users. Notion rebuilt the agent harness three to five
  times as frontier models improved.
- **Reported stage**: scaled internally.
- **Sources**:
  - [Notion's Token Town: 5 Rebuilds, 100+ Tools (Latent Space podcast)](https://latent.space/p/notion) and the
    [YouTube version](https://www.youtube.com/watch?v=ATt7QJgt-2k) — interview with cofounder
    Simon Last and head of AI engineering Sarah Sachs, 2026-04-14.
  - [How we built security into Custom Agents](https://www.notion.com/en-gb/blog/how-we-built-security-into-custom-agents) — Notion engineering blog. First-party.
- **Caveat**: a "Scruff" named security agent did **not** pass verification. See
  [Refuted or excluded](#refuted-or-excluded).

### Microsoft — PRAssistant

- **Status**: Verified, ready (3-vote, follow-up pass).
- **Confidence**: high.
- **What it does**: PRAssistant is an internal AI code-review agent. When an engineer opens a pull
  request, PRAssistant joins as a reviewer and leaves comments like a human reviewer. It is a
  distinct internal build, not the shipping product. Microsoft later folded the lessons into
  GitHub Copilot Pull Request Reviews.
- **Reported stage**: scaled. More than 90% of pull requests, over 600,000 reviews per month, and
  about 5,000 repositories in early onboarding.
- **Why it qualifies**: the source names PRAssistant as a Microsoft-internal tool that predates
  and informed a separate external product. This is a genuine internal build, not dogfooding of a
  consumer product.
- **Sources**:
  - [Enhancing code quality at scale with AI-powered code reviews](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/) — Microsoft engineering blog, 2025-07-14. First-party. Author: Sneha Tuli, Principal PM.
- **Caveat**: single first-party source. No public repository. Treat the scale figures as
  self-reported.

### Airbnb — Airchat CLI (airchat-cli)

- **Status**: Verified, ready (3-vote, follow-up pass).
- **Confidence**: high.
- **What it does**: Airbnb's Dev AI team built an internal agentic-coding harness called Airchat.
  It is a wrapper over Claude Code, with a unified gateway for cost and metrics, an internal
  plugin marketplace, AirDev Workspaces for parallel sessions, and more than a dozen internal MCP
  servers that connect agents to internal systems. Airbnb abandoned an earlier attempt to build a
  full orchestrator from scratch and shipped a thin shim over Airchat instead.
- **Reported stage**: scaled. The team reports about 64% of pull requests materialized through
  agentic coding, and about 60% of engineers onboarded within 12 months.
- **Why it qualifies**: Airbnb does not sell a coding product. The wrapper, the MCP servers, the
  marketplace, and the sandboxed environments are distinct internal assets. This is material
  adaptation of a vendor agent, not dogfooding.
- **Sources**:
  - [Agentic coding at Airbnb (DPE.org talk)](https://dpe.org/sessions/szczepan-faber-mike-nakhimovich/agentic-coding-at-airbnb/) — talk by Szczepan Faber and Mike Nakhimovich.
  - [Beyond the CLI (DX podcast)](https://getdx.com/podcast/beyond-the-cli-agentic-ai-for-async-workloads-and-non-developers/) — transcript.
  - [How to get your team past the AI (The AI Thinker newsletter)](https://www.theaithinker.com/p/how-to-get-your-team-past-the-ai) — secondary, quotes the engineers.
- **Caveat**: the harness is a wrapper over Claude Code, not a from-scratch orchestrator. The 64%
  figure comes from a third-party newsletter, not a first-party blog. Find a first-party Airbnb
  source before you write the record.

### Plaid — AI Annotator, Fix My Connection, internal MCP server

- **Status**: Verified, ready (3-vote, 2026-08-13).
- **Confidence**: high.
- **Verification note**: all three voters confirmed a genuine internal build and a real deployment.
  Caveat: all sources are first-party Plaid blogs, so the metrics are self-reported. The
  `ai-coding-adoption` URL describes vendor Cursor adoption and does not support the three named
  agents; the claim rests on the other two sources.
- **What it does**: Plaid built several internal agents for its own operations. AI Annotator
  automates large-scale transaction-data labeling for model training. Fix My Connection detects
  bank-integration failures and generates repair scripts automatically. A separate internal MCP
  server ties more than 20 tools and several internal services together for engineer productivity.
- **Reported stage**: scaled. AI Annotator reached more than 95% human alignment at lower cost and
  time. Fix My Connection enabled more than 2 million successful logins and cut average repair
  time by 90%.
- **Why it qualifies**: Plaid frames both agents as internal builds for its own data-labeling and
  integration-ops work. They are not vendor usage and not dogfooding of a Plaid consumer product.
- **Sources**:
  - [AI agents at Plaid (June 2025)](https://plaid.com/blog/ai-agents-june-2025/) — Plaid blog. First-party.
  - [The Plaid internal MCP server](https://engineering.plaid.com/the-plaid-internal-mcp-server-8eff08bb6bdb) — Plaid engineering blog. First-party.
  - [AI coding adoption at Plaid](https://plaid.com/blog/ai-coding-adoption-plaid/) — Plaid blog. First-party.

### Databricks — internal engineering agents and the coSTAR framework

- **Status**: Verified, ready (3-vote, 2026-08-13), scoped.
- **Confidence**: high.
- **Verification note**: the claim survived 0 to 3. Two of three voters called the internal build
  genuine, and one called it partial. All three confirmed a real deployment. Scope caveat: Omnigent
  is a shipping open-source product under the `omnigent-ai` org and is co-attributed to Neon. It is
  not a distinct Databricks internal build. Record only the internal engineering agents (code review
  and on-call) and the coSTAR testing framework on Databricks' private codebase benchmark. Treat
  Omnigent as an excluded shipping product under the editorial rule.
- **What it does**: Databricks built internal agents for its own engineering work, including
  code-reviewer and on-call support agents. Omnigent is a meta-harness that composes and governs
  several coding tools (Claude Code, Codex, and others) for internal multi-agent use. Databricks
  tests agents with its coSTAR framework on a private benchmark built from its own multi-million
  line codebase.
- **Reported stage**: deployed as daily coding drivers on the Databricks codebase. Omnigent was
  open-sourced under Apache 2.0 after internal use.
- **Why it qualifies**: the coSTAR post names internal engineering workflow agents. Omnigent is a
  distinct Databricks build. Genie Code and Agent Bricks are shipping products and are excluded.
- **Sources**:
  - [coSTAR: how we ship AI agents at Databricks fast](https://www.databricks.com/blog/costar-how-we-ship-ai-agents-databricks-fast-without-breaking-things) — Databricks blog. First-party.
  - [Introducing Omnigent](https://www.databricks.com/blog/introducing-omnigent-meta-harness-combine-control-and-share-your-agents) — Databricks blog. First-party.
  - [Benchmarking coding agents on a multi-million line codebase](https://www.databricks.com/blog/benchmarking-coding-agents-databricks-multi-million-line-codebase) — Databricks blog. First-party.
  - [Matei Zaharia on the Omnigent open-source release](https://www.linkedin.com/posts/mateizaharia_really-excited-to-open-source-a-new-project-activity-7471594037934723073-YCPO) — social post.

### HubSpot — Sidekick, Crucible, Aviator

- **Status**: Verified, ready (3-vote, 2026-08-13).
- **Confidence**: high.
- **Verification note**: all three voters confirmed a genuine internal build and a real deployment.
  The technical detail (Kubernetes Jobs, about 3,000 EC2 instances, a multi-model Judge Agent) goes
  beyond marketing copy. Caveat: all metrics are self-reported on HubSpot's engineering blog, and the
  InfoQ article rephrases first-party content.
- **What it does**: Sidekick is an internal AI code-review agent that reviews every pull request.
  A multi-model "Judge Agent" checks each comment for accuracy and action before it posts. Sidekick
  runs on Aviator, a Java agent framework HubSpot built for precise tool control. Aviator runs on
  Crucible, a self-hosted cloud platform that runs agents in isolated containers and mirrors a real
  developer environment.
- **Reported stage**: scaled. Sidekick reviews every pull request. It cut engineer feedback time
  by 90% and held more than 80% positive developer reaction over six months.
- **Why it qualifies**: HubSpot did not just adopt a vendor agent. It built its own framework,
  orchestration layer, and review agent. This is material internal adaptation.
- **Sources**:
  - [Automated code review: the 6-month evolution](https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution) — HubSpot product blog. First-party.
  - [Cloud coding agents at HubSpot](https://product.hubspot.com/blog/cloud-coding-agents-at-hubspot) — HubSpot product blog. First-party.
  - [How we build with AI](https://www.hubspot.com/company-news/how-we-build-with-ai) — HubSpot company blog. First-party.
  - [HubSpot AI code review agent (InfoQ)](https://www.infoq.com/news/2026/03/hubspot-ai-code-review-agent/) — secondary.

### Datadog — Bits Investigation (Bits AI SRE)

- **Status**: Border case.
- **Confidence**: high for the build; medium for internal dogfooding.
- **What it does**: Bits Investigation is an autonomous agent that investigates production
  incidents. It forms hypotheses, queries live telemetry, and recurses into sub-hypotheses to
  produce a root-cause analysis. It can run without initial prompting.
- **Reported stage**: scaled as a commercial product.
- **Why it is a border case**: Bits Investigation is also a Datadog product. The internal
  dogfooding claim passed on a split 2 to 1 vote. The source shows Datadog collected and labeled
  real incidents from hundreds of internal teams to build the benchmark dataset, and runs Bits AI
  across 8,000+ internal services. It does not directly confirm that Bits runs on Datadog's own
  production outages. Resolve that gap before you write a record.
- **Sources**:
  - [Bits AI SRE](https://www.datadoghq.com/blog/bits-ai-sre/) — Datadog blog. First-party.
  - [Building Bits AI SRE](https://www.datadoghq.com/blog/building-bits-ai-sre/) — Datadog engineering blog. First-party.
  - [The Bits AI evaluation platform](https://www.datadoghq.com/blog/engineering/bits-ai-eval-platform/) — Datadog engineering blog. First-party.
  - [Press release: Datadog launches Bits AI SRE](https://datadog.gcs-web.com/news-releases/news-release-details/datadog-launches-bits-ai-sre-agent-resolve-incidents-faster).
  - [Bits Investigation docs](https://docs.datadoghq.com/bits_ai/bits_investigation/).

### Snowflake — Cortex Code internal adaptation

- **Status**: Border case.
- **Confidence**: low.
- **What it does**: Snowflake rolls out Cortex Code (also called CoCo), its coding agent, across
  its own engineering organization. On top of the product, Snowflake built an internal skills
  system with about 7,000 skills written by roughly 1,000 engineers, domain profiles, a
  14-pattern proficiency framework, and integration into PagerDuty and Slack on-call workflows.
- **Reported stage**: scaled internally.
- **Why it is a border case**: Cortex Code is a shipping Snowflake product. The internal use alone
  is dogfooding. The argument for inclusion is the large internal adaptation layer: the skills
  system and the on-call integration go beyond the shipped product. Decide whether that adaptation
  clears the bar for a distinct internal build.
- **Sources**:
  - [AI coding chaos into a repeatable playbook (Stack Overflow Blog)](https://stackoverflow.blog/2026/07/02/ai-coding-chaos-into-a-repeatable-playbook/) — secondary, 2026-07-02.
  - [Snowflake CoCo coding agent](https://www.snowflake.com/en/blog/snowflake-coco-ai-coding-agent-modern-data-stack/) — Snowflake blog. First-party.
  - [ArcticMem persistent memory](https://www.snowflake.com/en/blog/engineering/arcticmem-persistent-memory-ai-agents/) — Snowflake engineering blog. First-party.

## Tier 2 — Hyperscalers and AI-native vendors

These leads qualify only where a source documents internal use of an agent the organization built.
A product the company sells is not enough on its own.

### OpenAI — in-house data agent

- **Status**: Verified, ready.
- **Confidence**: high.
- **What it does**: OpenAI built a bespoke, internal-only data agent that explores and reasons
  over OpenAI's own data platform. It serves Engineering, Data Science, Go-To-Market, Finance, and
  Research. It has more than 3,500 internal users across 70,000 datasets and 600 PB. It inherits
  existing permissions. It is built on Codex and GPT-5.
- **Reported stage**: scaled internally.
- **Sources**:
  - [Inside our in-house data agent](https://openai.com/index/inside-our-in-house-data-agent/) — OpenAI engineering blog. First-party.

### Amazon — Amazon Q Developer

- **Status**: Verified, ready.
- **Confidence**: high.
- **What it does**: Amazon built Amazon Q Developer and adopted it at scale across Amazon for its
  own engineers. Amazon's internal Software Builder Experience team ran a nine-month econometric
  study of thousands of two-pizza teams to measure the causal effect on code review and deployment
  speed.
- **Reported stage**: scaled internally.
- **Why it qualifies**: Amazon built the tool and documented its own internal adoption with a
  first-party study.
- **Sources**:
  - [Measuring the effectiveness of software development tools and practices](https://www.amazon.science/blog/measuring-the-effectiveness-of-software-development-tools-and-practices) — Amazon Science blog, 2025-07-29. First-party.

### Meta — TestGen-LLM

- **Status**: Border case.
- **Confidence**: high.
- **What it does**: TestGen-LLM improves existing human-written unit tests. Meta deployed it at
  internal test-a-thons for the Instagram and Facebook platforms. It improved 11.5% of the classes
  it touched, and engineers accepted 73% of its recommendations for production deployment.
- **Reported stage**: scaled internally.
- **Why it is a border case**: the paper frames TestGen-LLM as a system or tool rather than an
  autonomous agent. The internal build and deployment are clear. Whether it fits the `task-agent`
  definition is a catalog judgment.
- **Sources**:
  - [Automated unit test improvement using LLMs at Meta (arXiv 2402.09171)](https://arxiv.org/abs/2402.09171) — paper.
  - [ACM Digital Library, DOI 10.1145/3663529.3663839](https://dl.acm.org/doi/10.1145/3663529.3663839).

## Needs verification

These leads surfaced during the search but did not pass full verification. Confirm the source and
the dogfooding claim before you write a record.

### Anthropic — internal use of Claude Code ("antfooding")

- **Confidence**: medium. The first-party study exists, but Claude Code is also an Anthropic
  product.
- **What it does**: Anthropic studied how its own engineers use Claude Code. The study draws on
  200,000 Claude Code transcripts, 132 engineer surveys, and 53 interviews.
- **Next step**: locate the primary Anthropic paper or post and confirm it describes internal use.
  The audit found a secondary summary, not the primary source.
- **Source**:
  - [Eat Your Own AI (Cobus Greyling, summary of the Anthropic study)](https://cobusgreyling.medium.com/eat-your-own-ai-7c6cbdb8205c) — secondary, 2026-03-12.

### Google — AI-generated code

- **Confidence**: low.
- **What it does**: On the Q3 2024 earnings call, CEO Sundar Pichai said more than 25% of new code
  at Google is generated by AI and then reviewed by employees.
- **Why it is low confidence**: the quote documents AI-assisted coding at scale, not a specific
  internal agent that Google built. Keep as a watch item unless a first-party source names a
  system.
- **Source**:
  - [Business Insider report on Google Q3 2024 earnings](https://www.businessinsider.com/google-earnings-q3-2024-new-code-created-by-ai-2024-10) — secondary, 2024-10-29.

---

## Refuted or excluded

The audit refuted these claims or excluded these leads. Do not add them without a new, stronger
source.

- **Notion "Scruff" security agent**: the claim that Notion built a named agent called Scruff that
  triaged alerts and saved six hours per week failed verification 0 to 3. Record only that
  Notion's security team is an active Custom Agents user. Do not cite the Scruff metrics.
- **Atlassian DOT scale metrics**: the claim that DOT handles roughly 70% of help-channel threads
  and reduced the unanswered-question rate to zero failed verification 0 to 3. Record only that
  DOT launched and is in use.
- **Vercel v0**: v0 is an end-consumer product. A story of Vercel using v0 internally is product
  promotion, not an internal-agent build. Excluded under the editorial rule.
- **GitLab Duo**: GitLab dogfoods its own shipping Duo product. Verification found no distinct
  internal build or material adaptation beyond the shipped features. Excluded as promotional
  dogfooding, the same pattern as Vercel v0.
- **Netflix in-house LLM serving**: Netflix runs its own model inference stack (Model Scoring
  Service on vLLM and NVIDIA Triton). This is serving infrastructure, not an agent. Excluded.

## Confirmed gaps

The follow-up sweep checked these Tier 1 candidates and found no qualifying internal-agent build.
Most have only shipping products, vendor-tool usage, or aspirational job postings.

- **PagerDuty**: the AI agents (Insights, SRE, Scribe, Shift) are the shipping PagerDuty Advance
  product suite, not a distinct internal build.
- **Postman**: the "AI Engineer" and "Agent Mode" are shipping product features. No internal build
  documented.
- **Twilio**: the AI offerings are shipping products. A narrow sales tool ("RFP Genie") exists but
  falls outside the catalog domains.
- **Asana**: "AI Teammates" and "AI Studio" are products. Only job postings describe an internal
  team, not a shipped build.
- **Canva**: the documented AI work is a consumer support product or vendor-tool usage. No
  internal build documented.
- **Roblox**: every public AI story is a creator-facing product feature. Note: the engineering blog
  domain did not resolve during the audit, so a direct check may yet surface a build.
- **Discord**: the public AI work builds features for the consumer product. No internal agent
  harness documented.
- **Samsara**: the concrete cases are vendor-tool usage (Workato, Cursor, Gong) or the shipping
  Connected Operations product. No internal build documented.

---

## Open questions for the next search

- Does Datadog run Bits Investigation on its own production incidents, or is the dogfooding limited
  to the benchmark dataset? This split vote is the weakest point in the Tier 1 set.
- Is the Snowflake internal adaptation layer (about 7,000 skills, on-call integration) enough to
  count as a distinct internal build, or does it stay excluded as product dogfooding?
- Anthropic: locate the primary first-party "antfooding" paper to confirm it documents internal
  use and to capture the real figures.
- Airbnb: find a first-party engineering blog or repository to firm up the "64% of PRs" figure,
  which currently comes from a third-party newsletter.
- Plaid and HubSpot passed three-vote verification on 2026-08-13 and are ready for records.
  Databricks passed but stays scoped: record the internal engineering agents and coSTAR, and exclude
  Omnigent as a shipping open-source product.
- Roblox: the engineering blog domain did not resolve in the audit environment. A direct check may
  surface an internal build that the sweep missed.

---

## Audit method

The audit ran in two passes.

The first pass ran on 2026-08-12 as a five-angle search: a broad engineering-blog sweep, a
named-systems sweep, a hyperscaler dogfooding sweep, a functional-vertical sweep, and a
talks-and-practitioner-posts sweep. It fetched 23 sources, extracted 98 claims, and verified the
top 25 claims with three adversarial votes each. 22 passed and 3 failed.

The follow-up pass ran on 2026-08-13. It ran three-vote verification on the Microsoft, Airbnb, and
GitLab leads, and it swept 12 candidate companies in parallel. It confirmed Microsoft and Airbnb
as distinct internal builds and excluded GitLab as promotional dogfooding. The sweep found new
internal builds at Plaid, Databricks, and HubSpot, and confirmed eight companies as gaps. The same
day a third three-vote pass verified Plaid, Databricks, and HubSpot. Plaid and HubSpot passed
cleanly; Databricks passed scoped (the internal engineering agents qualify, Omnigent does not).
