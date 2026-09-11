Source: https://internal-agents.com/#monday-sphera-atlas-morphex

monday.com Agent system

# Sphera / Atlas / Morphex

An internal agent system on Amazon Bedrock where agents have identities, managers, scopes, and performance scores; Atlas ships features, Morphex ships PRs autonomously.

Coding Code review

Atlas or Morphex feature task → tested and merged pull request: Outcome review

Operating model, claims & sources

#### Scoped operating models

**Atlas or Morphex feature task → tested and merged pull request** Outcome review · Level 4

#### Summary and context

Summary

An internal agent system on Amazon Bedrock where agents have identities, managers, scopes, and performance scores; Atlas ships features, Morphex ships PRs autonomously.

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

#### Reported metrics

Headline claim

Morphex: 19 of 20 PRs merge without human review

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   monday.com

Scope
:   Morphex PRs that merge automatically after CI and Guardrails pass

Denominator
:   Morphex pull requests; sample size and period not supplied

Method
:   Unknown

Observation date
:   Unknown

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary) Preserved content.md, lines 148–152

Key observation

Morphex: 19 of 20 PRs merge automatically without human review

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   monday.com

Scope
:   Morphex PRs that merge automatically after CI and Guardrails pass

Denominator
:   Morphex pull requests; sample size and period not supplied

Method
:   Unknown

Observation date
:   Unknown

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary) Preserved content.md, lines 148–152

Key observation

90% of Builders use AI coding tools monthly; adoption nearly doubled year over year

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   monday.com

Scope
:   Monthly AI coding-tool adoption among monday Builders, including engineers, PMs, analysts, and designers

Denominator
:   Builders; not exclusively engineers

Method
:   Unknown

Observation date
:   Unknown

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary) Preserved content.md, lines 10, 16, 22

Key observation

Per-engineer PR throughput increased by more than 50%

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   monday.com

Scope
:   Per-engineer pull-request throughput

Denominator
:   Engineers; baseline period and cohort size not specified

Method
:   Unknown

Observation date
:   Unknown

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary) Preserved content.md, lines 10, 23

Key observation

Guardrails catches ~25% of agent PRs before human review; low single-digit revert rate

Metric · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

Reported by
:   monday.com

Scope
:   Recent cut of top PR-generating agents; Guardrails rejection before review and reverts among merged PRs

Denominator
:   Agent PRs for Guardrails rejection; merged PRs for revert rate

Method
:   Unknown

Observation date
:   Unknown

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary) Preserved content.md, lines 154–158

#### Architecture and primitives

Sandbox

Amazon EKS, one pod per active session; a remote sandbox tests each PR before review; EFS workspace mount

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Harness

Claude Agent SDK behind a thin monday-agent-sdk wrapper (provider neutrality, cold-start optimization, custom harness opinions)

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Model

Amazon Bedrock; Application Inference Profiles for routing; cross-region failover; PrivateLink (traffic stays in VPC)

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Interfaces

slack, monday, github

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Tool access

Triggers via Slack @mention, monday item assignment, or GitHub PR review → SNS → per-team SQS → consumers; monday MCP servers underpin the Guardrails

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Knowledge

File-based memory: MEMORY.md (cross-session) + diary/YYYY-MM-DD.md; sessions/repos/secrets on EFS; durable records on S3

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Credentials

Per-session secrets in AWS Secrets Manager; same RBAC as humans; real Slack/GitHub/monday accounts

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Context management

Live state in ElastiCache (sub-ms); monday boards (Builders CoWORK) as shared state for tasks, status, handoffs

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Supporting component

Stable identity + assigned human manager + scope + performance score

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Supporting component

Automated review against monday standards (metrics, feature flags, security)

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Supporting component

MEMORY.md + daily diary instead of vector retrieval

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Supporting component

monday boards as the shared-state layer for human/agent collaboration

Fact · Reported · Medium confidence

Evidence and qualifications

Confidence reason
:   A linked participant or independent source reports the claim.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

#### Lessons and interpretation

Lesson

Evals from day one; should have been day one, not month nine

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Lesson

Skip the vector store; file-based memory (MEMORY.md) was the right answer

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Lesson

Remote-sandbox every PR before human review, with production-traffic replay

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Lesson

The existing auth/identity/deploy pipeline applies to agents; reuse it

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

Lesson

AI engineering is building the feedback loops that let imperfect agents be trusted safely

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

#### Operating model evidence

Operating model assessment

Level 4 for Atlas or Morphex feature task → tested and merged pull request; human attention boundary: outcome-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The secondary source reports predominantly automatic merges and automated guardrails, while humans manage tasks and outcomes.

Observation date
:   2026

- Supports [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md) (independent-secondary)

#### Sources

1. [AI Teammates: how monday.com runs production AI agents on Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/monday-sphera-atlas-morphex-source-1/content.md)  <https://aws.amazon.com/blogs/machine-learning/ai-teammates-how-monday-com-runs-production-ai-agents-on-amazon-bedrock/> case-study · independent-secondary · Last source verification: 2026-08-31

Entry reviewed 2026-09-09 [Permalink ↗](https://internal-agents.com/#monday-sphera-atlas-morphex)
