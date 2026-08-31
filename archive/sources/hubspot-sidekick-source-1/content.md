> Archived source snapshot  
> Source ID: `hubspot-sidekick-source-1`  
> Original URL: <https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution>  
> Final URL: <https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution>  
> Title: Automated Code Review: The 6-Month Evolution  
> Captured at: `2026-08-31T17:43:10Z`

---

As HubSpot engineers have increasingly started writing more and more of their code with both [local](https://product.hubspot.com/blog/context-is-key-how-hubspot-scaled-ai-adoption) and [cloud coding agents](https://product.hubspot.com/blog/cloud-coding-agents-at-hubspot), we've noticed that now more than ever, code review is taking up a large portion of cycle time on new changes.

Thorough code review is key to maintaining a high quality bar at HubSpot, especially at our scale. We place a lot of value on human review at HubSpot, especially for system design and architectural considerations. At the same time, code review is one of the most significant wait points in an Engineer's workflow. Our Developer Experience AI team saw an opportunity to use AI to provide immediate, consistent feedback grounded in our established norms.

What we found might surprise you: our AI code reviewer catches real issues, understands HubSpot-specific context, and maintains a high signal to noise ratio, often leaving no comments at all. Over the last six months, we started running this system on every pull request, significantly reducing cycle time and ensuring engineers get high quality feedback as fast as possible.

**A concrete example of this change appears in the graph below.**

**![image1](https://product.hubspot.com/hs-fs/hubfs/image1.png?width=3600&height=1800&name=image1.png)** *Sidekick has* ***reduced the time it takes for engineers to get feedback on their code by 90%****, peaking at a 99.76% reduction in September.*

## Evolution of our Review Architecture

Our approach to pull request reviews has undergone a fundamental shift. What began as a fast-moving experiment evolved into a deeper rethink of how and where automated reviews should live. That journey took us from our Kubernetes-based system powered by Claude Code to a framework native to the existing HubSpot Java stack.

### Sidekick Reviews 1.0: Crucible

Our first iteration of automated code review was built on [Crucible](https://product.hubspot.com/blog/cloud-coding-agents-at-hubspot), our internal system for running Claude Code instances inside Kubernetes. Our original approach was extremely simple: give Claude Code access to the GitHub CLI (allowing it to read the pull request and submit comments) then prompt it with a single instruction: **“Review this pull request.”**

This allowed us to validate that LLM-driven code review could provide real signal without committing to a custom service. Within a short time, we had an MVP capable of reviewing real pull requests and delivering actionable feedback.

While Crucible was scalable and operationally independent, it came with significant overhead:

1. **Latency and cost:** Spinning up Kubernetes workloads for each review made reviews slower and more expensive than we wanted.
2. **Limited flexibility:** Claude Code is a powerful tool, but working around its abstractions made it difficult to precisely shape review behavior.
3. **Operational complexity:** Managing Kubernetes infrastructure added friction to iteration and experimentation.
4. **Developer experience gaps:** The agent execution environment is configured primarily through shell scripts, which are significantly less ergonomic than our standard Java tooling.

Ultimately though, we proved that automated reviews were valuable and that it was worthwhile to invest in a longer-term solution.

### Migration to Internal Agent Framework

We rewrote Sidekick’s code review system using **Aviator**, our internal Java-based agent framework. This transition gave us a level of operational freedom that simply wasn’t possible with our previous approach. Aviator’s lightweight, agentic architecture is native to the HubSpot tech stack. It can be embedded directly into services or run across a variety of environments, making it both reusable and adaptable as Sidekick evolved.

**Faster, Simpler, and More Flexible**

From an efficiency standpoint, this migration immediately paid off. Reviews ran faster, with fewer moving parts, and no longer required standing up external infrastructure for each execution. Aviator also introduced first-class support for multiple models, including Claude, GPT, and Gemini, and more, allowing us to experiment more freely and quickly fail over in the case of provider downtime..

**Deliberate Control**

Most importantly, Aviator gave us the precision and control we needed to materially improve review quality. Its structured tool abstractions, built on our internal RPC framework**,** let us be deliberate about giving the code review agent the tools it needed to understand HubSpot’s workflow. Previously, tool integrations in Crucible required an additional intermediary service, such as an MCP server. With Aviator, we could now:

- Select the tools that matter most for code review
- Design new tools around this specific workflow
- Implement these tools directly in our codebase

This made agent behavior more predictable, easier to reason about, and far simpler to refine over time.

**From Experiment to First-Class**

Taken together with the lighter runtime, reusable architecture, multi-model support, and fine-grained tool control, Aviator represented a decisive shift towards making Sidekick code review a more integrated and stable member of the developer workflow.

## Introducing a Judge Agent

### The Problem: Noisy Feedback Erodes Trust

Any automated system that posts feedback faces the critical challenge of ensuring the feedback is genuinely valuable. After migrating Sidekick’s core architecture to Aviator, we unlocked faster execution and tighter control, but we were still struggling with review quality.

![image4](https://product.hubspot.com/hs-fs/hubfs/image4.png?width=4890&height=2142&name=image4.png)

*An example of the original Sidekick implementation being overly effusive.*

**The most common failure mode wasn’t incorrect feedback. It was** ***unhelpful*** **feedback.** Early reviews tended to be overly congratulatory, verbose, or nitpicky. Despite extensive prompt tuning, we couldn’t reliably eliminate low-value feedback this way. Improvements in one area often caused regressions in another.

The result was predictable. Even when the feedback was technically correct, too much noise caused developers to tend to tune Sidekick out entirely.

### The Solution: A Judge Agent

Rather than continuing to fight this problem at the prompt level, we introduced a second agent which we call the “Judge Agent.” This is also referred to as the **evaluator-optimizer workflow.**

The Judge Agent acts as a quality gate between Sidekick’s initial review and the comments that ultimately appear on a GitHub pull request. After Sidekick drafts a review, the agent receives that output and evaluates it against three core criteria:

- **Succinctness**: Is the feedback clear and to the point?
- **Accuracy**: Is the suggestion technically correct within the context of the codebase and change?
- **Actionability**: If the feedback includes a code suggestion, can it be applied directly without additional modification?

Only review comments that pass the judge’s evaluation are posted to GitHub, and everything else is filtered out. While simple in concept, this **two-stage process is arguably the single most important factor** in Sidekick’s effectiveness.

By dramatically reducing noise and eliminating ineffective suggestions, the Judge Agent enforces consistent review quality. It's a small addition on the surface, but it fundamentally changed the user experience. Developers went from dismissing most feedback to expecting Sidekick to catch genuine bugs.

![image2-1](https://product.hubspot.com/hs-fs/hubfs/image2-1.png?width=4500&height=2832&name=image2-1.png)

*A visual interpretation of the Review Agent to Judge Agent evaluation loop.*

## How good are Sidekick AI reviews?

Once Sidekick became the default reviewer, we needed to understand how it was behaving at scale, what it cost, where time and tokens were spent, and whether changes to the system were improving or degrading the user experience.

We built a comprehensive dashboard to serve as our north star. It tracks token usage, API costs, failure counts, and more. We prioritized measuring usage not just per day, but **per tool**, which helped us identify where call volume and token usage could be reduced.

### Continuous Improvement Loop with User Feedback

Firstly, we wanted to understand whether or not the feedback from Sidekick was actually helpful. As Sidekick continued to run at scale, having a fast, low-friction feedback loop became critical.

We implemented the simplest possible interface: **emoji reactions on review comments and thread replies**. After each review, Sidekick adds a short footer inviting developers to react with 👍 or 👎 or reply directly in the thread. This creates an elegant feedback loop that requires minimal effort from users.

- Emoji reactions provide quick, fresh signals on individual comments
- Thread replies enable more nuanced, qualitative feedback

Together, they form a continuous stream of actionable data.

Aggregating this data directly informs our evaluation and model selection decisions. This allows us to move away from cumbersome surveys and toward a continuous, actionable data stream. In the future, we want to use this data to keep improving on AI reviews.

### Additional Metrics

After establishing strong quality metrics, we expanded our evaluation to include cost optimization, volume, and failure rates. Together, these measures gave us a more complete view of how well Sidekick Review performed, and not just in user experience.

This observability has been key in showcasing the impact of our improvements to Sidekick code review. We could finally confirm the value of these reviews for engineers based on hard evidence, rather than intuition. Over the past couple months, **Sidekick has been rocking at an over 80% “thumbs up” reaction rate**, which we are very proud of.

![image3](https://product.hubspot.com/hs-fs/hubfs/image3.png?width=5814&height=3846&name=image3.png) *A snapshot of our Sidekick Code Review metrics dashboard.*

## The Road Ahead

The last six months of growth have set a clear direction for the future of Sidekick code reviews. As we look toward the next phase, our focus is on building a smarter, more autonomous Sidekick.

Here’s what we hope to tackle next:

- **Memory from prior sessions -** remembers past reviews and code patterns within a codebase, allowing it to provide more relevant suggestions faster.
- **Considering adjacent codebases -** draws on related repositories to identify cross-project patterns and maintain consistency.
- **Incorporating user feedback -** rather than just using emoji reactions and thread replies as a satisfaction signal, Sidekick uses the data to validate its current recommendations.
- **Custom instructions (Just launched!) -** can optionally incorporate a set of repo-specific instructions in its user prompt.

By leveraging these additional features, Sidekick will provide smarter, more precise recommendations per project. Here’s to the next chapter of AI-generated PR reviews. 🦾

---

Thank you for reading! I'd also like to give a special shout out to [Michael Goodnow](https://www.linkedin.com/in/mmgoodnow), [Aswath Ilangovan,](https://www.linkedin.com/in/aswath-ilangovan) [Stephan Lensky](https://www.linkedin.com/in/slensky), [Francesco Signoretti](https://www.linkedin.com/in/signorettif/), [Brian LaMattina](https://www.linkedin.com/in/brian-l-577bb6114/), and everyone else on the team who helped make this happen.
