Source: https://internal-agents.com/#salesforce-slackbot

Salesforce Task agent

# Slackbot

Salesforce was 'customer zero' for the rebuilt Slackbot; an employee agent that finds company context, drafts work, and connects Slack context with Salesforce data; now also an external product.

Support Customer success Ops

employee request → drafted work: Work product review

Operating model, claims & sources

#### Scoped operating models

**employee request → drafted work** Work product review · Level 3

#### Summary and context

Summary

Salesforce was 'customer zero' for the rebuilt Slackbot; an employee agent that finds company context, drafts work, and connects Slack context with Salesforce data; now also an external product.

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)
- Supports [Interview with Slackbot about connected work context](https://www.salesforce.com/in/news/stories/salesforce-slackbot-ai-interview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-2/content.md) (first-party)

#### Architecture and primitives

Harness

An employee agent intended as a front door to other agents

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

Model

Not specified

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

Interfaces

slack

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

Tool access

Finds company context, drafts work, manages meetings, connects Slack context with Salesforce data

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

Knowledge

Slack context joined with Salesforce CRM data

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

Credentials

Permission-aware by construction; sees what the employee can see, respects roles and access controls

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

Supporting component

Agent visibility is bounded by the invoking employee's permissions

Fact · Reported · High confidence

Evidence and qualifications

Confidence reason
:   A linked first-party source states the claim.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

#### Lessons and interpretation

Lesson

Dogfood internally first ('customer zero') before shipping externally

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

Lesson

Make permission-awareness a construction property, not a prompt instruction; the agent sees only what the employee can see

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The catalog derives this observation from the linked sources.

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

#### Operating model evidence

Operating model assessment

Level 3 for employee request → drafted work; human attention boundary: work-product-review.

Inference · Catalog judgment · Medium confidence

Evidence and qualifications

Confidence reason
:   The source describes an employee agent that prepares drafts and contextual work for human use.

Observation date
:   2026-01-14

- Supports [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md) (first-party)

#### Sources

1. [Salesforce announces general availability of Slackbot](https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-1/content.md)  <https://www.salesforce.com/ap/news/press-releases/2026/01/14/salesforce-announces-the-general-availability-of-slackbot-your-personal-agent-for-work-sg/> release · first-party · Last source verification: 2026-08-31
2. [Interview with Slackbot about connected work context](https://www.salesforce.com/in/news/stories/salesforce-slackbot-ai-interview/) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-2/content.md)  <https://www.salesforce.com/in/news/stories/salesforce-slackbot-ai-interview/> corporate-article · first-party · Last source verification: 2026-08-31
3. [Salesforce rolls out new Slackbot AI agent](https://venturebeat.com/technology/salesforce-rolls-out-new-slackbot-ai-agent-as-it-battles-microsoft-and) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-3/content.md)  <https://venturebeat.com/technology/salesforce-rolls-out-new-slackbot-ai-agent-as-it-battles-microsoft-and> news · independent-secondary · Last source verification: 2026-08-31
4. [Hacker News submission for the Salesforce Slackbot rollout](https://news.ycombinator.com/item?id=46600760) · [Preserved Markdown](https://github.com/steel-experiments/internal-agents-map/blob/main/archive/sources/salesforce-slackbot-source-4/content.md)  <https://news.ycombinator.com/item?id=46600760> hn-thread · community · Last source verification: 2026-08-31

Entry reviewed 2026-08-31 [Permalink ↗](https://internal-agents.com/#salesforce-slackbot)
