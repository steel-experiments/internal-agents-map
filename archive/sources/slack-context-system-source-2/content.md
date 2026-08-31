> Archived source snapshot  
> Source ID: `slack-context-system-source-2`  
> Original URL: <https://www.infoq.com/news/2026/04/slack-agent-context-management/>  
> Final URL: <https://www.infoq.com/news/2026/04/slack-agent-context-management/>  
> Title: How Slack Manages Context in Long-Running Multi-agent Systems - InfoQ  
> Captured at: `2026-08-31T17:49:20Z`

---

[AI, ML & Data Engineering](https://www.infoq.com/ai-ml-data-eng/ "AI, ML & Data Engineering")

[Online InfoQ Engineering Leadership Certification (Sep 18): Lead strategy, systems, and teams.](https://certification.qconferences.com/engineering-leadership?utm_source=infoq&utm_medium=referral&utm_campaign=infoqyellowbox_onlinecohortleadership26)

Log in to listen to this article

To sustain productivity in long-running agent systems, Slack engineers moved away from accumulating chat logs and started [using structured memory, validation, and distilled truth](https://slack.engineering/managing-context-in-long-run-agentic-applications/) to maintain coherence and accuracy of long-running agent systems.

While short LLM sessions do not usually require explicit context management, this becomes essential in long-running sessions to ensure coherence, as the growth of the message history makes it impractical to include the full context with each request:

> Agent frameworks solve the state management problem for users by accumulating message history between API calls. This fills the agent’s context window, which provides a hard limit on how much information the agent can handle. Even approaching an agent’s context window limit can degrade the quality of responses.

As Slack staff software engineer Dominic Marks explains, one of Slack's multi-agent applications can span over hundreds of requests and generate megabytes of output. To manage this complexity, they followed an approach based on three complementary context channels: a director's journal, which stores the director's structured working memory; a critic's review, which stores an annotated findings report with credibility scores; and a critic's timeline, which stores chronological findings with credibility scores.

![](https://www.infoq.com/news/2026/04/slack-agent-context-management/news/2026/04/slack-agent-context-management/en/resources/1slack-image-1777407895831.jpg)

Slack's approach follows a [*coordinator/dispatcher* multi-agent design](https://www.infoq.com/news/2026/01/multi-agent-design-patterns/), where a central the coordinator acts as a decision maker, receiving requests and dispatching them to specialized agents further down the line, namely experts and critics.

Critics evaluate experts' work, as a portion of their findings "could either be invented or grossly misinterpret the data". They receive summary reports from experts and assess the evidence they contain. This evaluation is the basis for the creation of a scoring system used to identify findings corroborated by multiple sources.

The director's journal includes findings, observations, decisions, questions, and hypotheses, and "provides the common narrative that keeps other agents on track".

The critic's review acts as a truth filter, using evidence-inspection tools to build a credibility-weighted list of findings. To reduce the risk of hallucinations, critics are narrowly instructed to "only make a judgment on the submitted findings".

Finally, the critic's timeline builds a coherent narrative from the director's journal, the latest critic's review, and the previous timeline, retaining only credible evidence, removing duplicates, and resolving any conflicts by preferring the strongest sources.

While Slack's approach is strictly tied to its system, it illustrates a broader principle: rather than passing all information at every step, it builds structured summaries that agents can reliably build on. The three channels:

> work together to maintain coherence across rounds, while preserving the benefits of specialized agent roles. The Director can make informed strategic decisions. Experts can build on previous understanding. The Critic can objectively evaluate findings.
