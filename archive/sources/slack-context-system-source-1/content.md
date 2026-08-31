> Archived source snapshot  
> Source ID: `slack-context-system-source-1`  
> Original URL: <https://slack.engineering/managing-context-in-long-run-agentic-applications/>  
> Final URL: <https://slack.engineering/managing-context-in-long-run-agentic-applications/>  
> Title: Managing context in long-run agentic applications | Engineering at Slack  
> Captured at: `2026-08-31T17:49:11Z`

---

Dominic MarksStaff Software Engineer

![Investigation Journal](https://slack.engineering/wp-content/uploads/sites/7/2026/03/investigation_notebook.png)

Investigation Journal

#### Excerpt

In complex, long-running agentic systems, maintaining alignment and coherent reasoning between agents requires careful design. In this second article of our series, we explore these challenges and the mechanisms we built to keep teams of agents working productively over long time spans. We present a range of complementary techniques that balance the conflicting requirements of continuity and creativity.

---

In our [first article](http://slack.engineering/streamlining-security-investigations), we introduced our agentic security investigation service. We described how teams of AI agents collaboratively investigate security alerts. A Director orchestrates the investigation, many specialist Experts gather evidence, and a Critic reviews the Experts’ findings. We suggest you read the series in order.

To briefly recap, our investigation process proceeds through a series of defined phases. Each phase implements a distinct set of agent interactions. Within phases, we may have multiple rounds, where each round is one full iteration through the phase. There’s no preset limit on the number of rounds that make up an investigation: investigations continue until concluded by the Director agent.

## The Challenge of Long-run Coherence

Language model APIs are stateless: to provide continuity between requests, the caller must provide the complete message history with each request. Agent frameworks solve the state management problem for users by accumulating message history between API calls. This fills the agent’s context window, which provides a hard limit on how much information the agent can handle. Even approaching an agent’s context window limit can degrade the quality of responses. For short-run applications, no extra context window management is typically required.

![High-level overview of how agent frameworks manage context across inference API calls](https://slack.engineering/wp-content/uploads/sites/7/2026/03/pydantic_ai_agentic_loop.png)

High-level overview of how agent frameworks manage context across inference API calls

Complex security investigations can span hundreds of inference requests and generate megabytes of output, requiring special handling. Multi-agent applications, like ours, add further complexities. For each agent to optimally execute its role, it requires a tailored view of the investigation state. Each view must be carefully balanced. If agents are not anchored to the wider team, the investigation will be disconnected and incoherent. Conversely, sharing too much information stifles creativity and encourages confirmation bias.

Our solution uses three complementary context channels:

- **Director’s Journal**: The Director’s structured working memory
- **Critic’s Review**: Annotated findings report with credibility scores
- **Critic’s Timeline**: Consolidated chronological findings with credibility scores

Each channel serves a different purpose, and together they provide the context each agent needs without overwhelming any of them.

![How our agents consume and produce different context sources](https://slack.engineering/wp-content/uploads/sites/7/2026/03/context_channels.png)

How our agents consume and produce different context sources

### Specimen Content

We include edited extracts of the Journal, Review, and Timeline from one investigation in this article. These extracts should give a meaningful sense of what these context resources look like in practice. They have been edited to generalize the content, but they are derived from a real investigation. The alert was generated in response to the loading of a kernel module. In fact, the event was a false positive caused by a developer installing a package in a development environment, and the triggered detection rule being overly sensitive. Specimen extracts are shown in italics.

## The Director’s Journal

The Director is responsible for orchestrating the investigation: deciding what questions to ask, which Experts to engage, and when to conclude the investigation. To make coherent decisions across rounds, it needs memory of what’s been discovered and decided.

The Director has a journaling tool. The Director’s system prompt encourages it to update the Journal often and use it for short notes. The Journal captures decisions, observations, hypotheses, and open questions in a structured format. It serves as the Director’s working memory.

### Entry Types

The Journal supports six entry types:

| **Type** | **Purpose** | **Example** |
| --- | --- | --- |
| **decision** | Strategic choices | “Focus investigation on authentication anomalies rather than network activity” |
| **observation** | Patterns noticed | “Multiple failed logins preceded the successful authentication” |
| **finding** | Confirmed facts | “User authenticated from IP 203.0.113.45, not in historical baseline” |
| **question** | Open items | “Was the VPN connection established before or after the suspicious activity?” |
| **action** | Steps taken/planned | “Requested Cloud Expert to examine EC2 instance activity” |
| **hypothesis** | Working theories | “This pattern suggests credential stuffing rather than account compromise” |

In addition to classifying its entries, the Director can also assign priority, list follow-up actions, and include citation references to evidential artifacts. When the journaling tool is used, each entry is annotated with the investigation context: the phase, round number, and timestamp. The tool itself does nothing more than accumulate entries.

Every agent receives the current content of the Director’s Journal in their prompt, presented as chronology. Their system prompts include guidance that explains the Director’s role, their relationship to the Director, the purpose of the Journal, and how to interpret it.

### How It Maintains Alignment

The Journal allows the Director to lead the investigation towards a conclusion, to observe and measure its progress, to identify dead-ends, and to make course corrections in response. It provides the common narrative that keeps other agents on track.

![Breakdown of entry types in the Journal](https://slack.engineering/wp-content/uploads/sites/7/2026/03/journal_usage.png)

Breakdown of entry types in the Journal

## Example Director’s Journal

***Time:*** *09:32:21 |* ***Priority:*** *High*

*Identified event as endpoint process start, user running as root on dev workstation. Command is a package hook script (not direct modprobe). Listed key questions about user roles, host type, and log sources.*

***Time:*** *09:32:29 |* ***Priority:*** *Medium*

*Identified 4 relevant expert domains needed: endpoint telemetry, identity/access (user roles), configuration management (host config), user-behavior (activity patterns).*

***Time:*** *09:33:10 |* ***Priority:*** *Medium*

*Noted cgroup indicates user session, hostname suggests personal workstation. Realized command runs during package installation sequence, not actual module loading.*

***Time:*** *09:34:06 |* ***Priority:*** *High*

*Alert rule matching “kmod” in script path, not actual modprobe execution. Host identified as personal dev environment. Activity appears to be legitimate system administration.*

***Time:*** *09:35:15 |* ***Priority:*** *Medium*

*Confirmed dev environment grants root by design. Summarized investigation resources (endpoint queries, process ancestry, SSH cert logs). Preliminary assessment: false positive.*

***Time:*** *09:35:51 |* ***Priority:*** *High*

*Need to verify parent process chain, check for actual modprobe/insmod execution, reconstruct full session activity. Formulated targeted query for endpoint expert.*

***Time:*** *09:40:47 |* ***Priority:*** *Critical*

*Reviewed expert findings (6,046 events showing package install triggered event). All 4 experts agree: FALSE POSITIVE. Timeline confidence 0.83. Decision: advance to conclude.*

***Time:*** *09:41:15 |* ***Priority:*** *High*

*Summarized all findings. Root cause: detection rule matched pathname not actual operation. Recommended action: tune detection rule to distinguish hook scripts from real modprobe.*

## The Critic’s Review Tools

To progress the investigation, the Director poses questions to Experts. Each Expert has a subject domain and tools to allow them to interrogate relevant data sources. At the end of their run, the Experts produce findings, citing investigation artifacts (tool calls) to support their conclusions. Even with strict guidelines, this process is not, by itself, sufficiently robust. Language models are known to hallucinate, and a proportion of the Experts’ findings could either be invented or grossly misinterpret the data.

The Critic’s role is to assess the Experts’ work, checking that reported findings are supported by evidence and that interpretations are sound. To do this accurately, it needs to be able to inspect not only each Expert’s claims and the cited evidence, but the methodology.

In the Review task, the Critic examines all the Experts’ findings in a single pass. Aggregating the findings together allows it to identify where the findings support or contradict each other. Due to the number of findings that can be produced, it’s not practical to provide all of the information to the Critic directly. Instead, the Critic receives a summary report and uses a suite of tools to examine the cited evidence.

![How Critic’s review tools are used](https://slack.engineering/wp-content/uploads/sites/7/2026/03/critic_tools_v2.png)

How Critic’s review tools are used

We provide the Critic with four tools:

| **Tool** | **Purpose** |
| --- | --- |
| **get\_tool\_call** | Inspect the arguments and metadata of any tool call |
| **get\_tool\_result** | Examine the actual output returned by a tool use |
| **get\_toolset\_info** | List what tools were available to a specific Expert |
| **list\_toolsets** | List all available toolsets organized by Expert |

Collectively, these tools allow the Critic to examine evidence and data gathering methodology. When an Expert cites **tooluse\_abc123** as supporting a finding, the Critic can use **get\_tool\_call** to examine the tool parameters used to obtain the result, and **get\_tool\_result** to see exactly what data the Expert was looking at. It can also use **get\_tool\_info** to access each tool’s inline documentation to determine if the tool was correctly used, and list\_toolsets to understand if the Director made an error by posing a question to an Expert that was not properly equipped to answer, or if an Expert made a poor tool selection.

### The Review Scoring System

The output of the Critic’s Review task is an annotated findings report containing an overall summary and scored findings. Not all findings are equally reliable. A finding corroborated by multiple sources deserves more weight than speculation based on partial data. By assigning numeric scores, we enable:

1. **Informed decision-making**: Highly credible findings can be prioritized
2. **Timeline quality**: Only credible findings make it into the consolidated timeline
3. **Audit trails**: Staff can quickly identify which conclusions need scrutiny

**Operational insights**: Dashboards illustrating system performance

### The Critic’s Rubric

We use a five-level credibility scale:

| **Score** | **Label** | **Criteria** |
| --- | --- | --- |
| 0.9-1.0 | **Trustworthy** | Supported by multiple sources with no contradictory indicators |
| 0.7-0.89 | **Highly-plausible** | Corroborated by a single source |
| 0.5-0.69 | **Plausible** | Mixed evidence support |
| 0.3-0.49 | **Speculative** | Poor evidence support |
| 0.0-0.29 | **Misguided** | No evidence provided or misinterpreted |

The following table shows the distribution of classifications over 170,000 reviewed findings. Slightly over a quarter of findings don’t meet the plausibility threshold.

| **Score** | **Label** | **%** |
| --- | --- | --- |
| 0.9-1.0 | **Trustworthy** | 37.7 |
| 0.7-0.89 | **Highly-plausible** | 25.4 |
| 0.5-0.69 | **Plausible** | 11.1 |
| 0.3-0.49 | **Speculative** | 10.4 |
| 0.0-0.29 | **Misguided** | 15.4 |

It’s reasonable to question whether the Critic’s Review provides a false sense of assurance; it’s also conducted by model inference. We approach this problem from several directions with a range of mitigations.

The first mitigation is to use a stronger model for the Critic. Because the Critic only reviews submitted findings rather than the entire Expert run, the number of tokens required is kept within reasonable limits. While stronger models are still subject to hallucination, [research suggests they err less frequently](https://arxiv.org/html/2411.04368v1#S3). Equally important is the capacity of the Critic to interpret nuances in the evidence, which is also improved with a stronger model.

The second mitigation is the formulation of the Critic’s instructions. Language models are more likely to hallucinate when posed larger, open-ended questions. The agent is instructed to only make a judgement on the submitted findings.

## Example Critic’s Review

***Cloud Expert*** *delivered a strong investigation with a comprehensive search query retrieving 6,046 session events and correctly identifying: (1) legitimate package operations, (2) kernel regeneration during system updates, (3)* *modprobe –show-depends* *queries for boot ramdisk configuration (not actual module loading), and (4) false positive detection rule matching on hook script name rather than kernel operations.*

## Annotated Findings

***\[0.92\]*** *Package operations triggered legitimate kernel regeneration on the target development host. Comprehensive query shows package management operations with expected package names confirmed in process event fields.*

***\[0.90\]*** *Parent process executed hooks including framebuffer, mdadm, and busybox scripts as part of normal operation. Parent process spawned multiple child processes executing hook scripts.\**

***\[0.88\]*** *Modprobe operations were information-gathering queries (**–show-depends –ignore-install* *flags) for thermal, dm-cache, raid0 modules, not actual kernel module insertion. Verified executable=/usr/bin/kmod with flags that query dependencies without loading.*

***\[0.87\]*** *Activity is expected system maintenance on a personal development environment by an authorized user with expected roles and root access during business hours.*

***\[0.85\]*** *Alert triggered on shell script name pattern rather than actual modprobe/insmod execution. Detection rule overly-broad: flagged dash interpreter running script with ‘kmod’ in pathname.*

The third mitigation is the Critic’s Timeline task, which we will now describe.

## Critic’s Timeline

The Critic’s Timeline task immediately follows the Review task in the investigation sequence. It is challenged to construct the most plausible consolidated timeline from three sources:

1. The most recent Review
2. The previous Critic’s Timeline
3. The Director’s Journal

Whereas the Review task is token intensive and requires the correct use of many tools, Timeline assembly operates entirely on data in the prompt. The intuition is that the more narrowly scoped task leaves a greater capacity for reasoning in the problem domain, rather than methods of data gathering or judgements of Expert methodology.

### Consolidation Rules

The Critic follows explicit rules when assembling Timelines:

1. **Include only events supported by credible citations** – Speculation doesn’t belong on the Timeline
2. **Remove duplicate entries describing the same event** – An event shouldn’t appear twice because two Experts mentioned it
3. **When timestamps conflict, prefer sources with stronger evidence** – A log entry timestamp beats an inferred time

**Maintain chronological ordering based on best available evidence** – Events must flow logically in time

### Gap Identification

Not every Timeline is complete. The Critic identifies significant gaps that should be addressed:

1. **Evidential gaps**: Missing data that would strengthen conclusions
2. **Temporal gaps**: Unexplained periods between events
3. **Logical inconsistencies**: Events that don’t fit the emerging narrative

We limit gap identification to the top 3 most significant gaps. This focuses the Director’s attention on what matters most rather than presenting an exhaustive list of unknowns.

The Critic is instructed to score the Timeline using a narrative-building rubric.

| **Score** | **Label** | **Meaning** |
| --- | --- | --- |
| 0.9-1.0 | **Trustworthy** | Strong corroboration across multiple sources, consistent timestamps, no significant gaps |
| 0.7-0.89 | **Highly-plausible** | Good evidence support, minor gaps present, mostly consistent Timeline |
| 0.5-0.69 | **Plausible** | Some uncertainty in event ordering, notable gaps exist |
| 0.3-0.49 | **Speculative** | Poor evidence support, significant gaps, conflicted narrative |
| 0.0-0.29 | **Invalid** | No evidence, confounding inconsistencies present |

The Timeline task raises the bar for hallucinated findings by enforcing narrative coherence. To be preserved, each finding must be consistent with the full chain of evidence; findings that contradict or lack support from the broader narrative are pruned. A hallucination can only survive this process if it is more coherent with the body of evidence than any real observation it competes with.

## Example Critic’s Timeline

***Confidence Score:*** *0.83*

*False positive security alert triggered during legitimate system maintenance on a personal development environment. Detection rule*

*incorrectly flagged a package hook script based on pathname string matching, rather than actual kernel module loading operations. All modprobe executions were dependency queries (**–show-depends* *flags) for boot ramdisk configuration, not live kernel modifications. Activity occurred during business hours with proper audit trail preservation, consistent with the development environment’s intended use.*

## Event Sequence

***09:29:01Z*** *– User session begins on development workstation*

***09:30:39Z*** *– Package management operations initiated by developer*

***09:30:48Z*** *– Package management triggered system maintenance hooks*

***09:31:26Z*** *–* ***ALERT TRIGGERED*** *– Hook script invoked*

***09:31:27Z*** *– modprobe information-gathering for modules to determine ramdisk dependencies*

***09:31:29Z*** *– modprobe dependency queries complete*

***09:31:29Z*** *– Additional hook scripts executed as part of ramdisk regeneration process*

## Evidence Gaps

- *Exact session initiation timestamp unknown – session activity observed from 09:29:01Z but SSH login event not captured*
- *Specific command that initiated apt/dpkg operations not identified – timeline shows package operations beginning at 09:30:39Z but triggering command not documented*
- *Secondary analyst failed to locate parent process using incorrect field name and missed modprobe operations by searching wrong path – reduces confidence in independent verification*

## Message History

As we explained in the introduction, agentic frameworks manage message history by accumulating messages and tool calls through the chain of inference requests that make up each agent invocation. In long-run agentic applications, you cannot simply carry the message history forward indefinitely. As more of the model’s context window is consumed, costs and inference latencies increase, model performance declines, and eventually the accumulated messages will exceed the context window.

Our approach is to rely entirely on the context channels presented in this article: the Journal, Review, and Timeline. **Besides these resources, we do not pass any message history forward between agent invocations.** Collectively, these channels provide a means of online context summarisation, negating the need for extensive message histories. Even if context windows were infinitely large, passing message history between rounds would not necessarily be desirable: the accumulated context could impede the agents’ capacity to respond appropriately to new information.

## Conclusion

Maintaining alignment and orientation in multi-agent investigations requires deliberate design. Each agent should have specific responsibilities, and a view of the investigation state tailored to its task. With proper design, context window limitations are not a major obstacle to building complex, long-running agentic applications.

We addressed these challenges with complementary mechanisms:

- **Journal**: Structured, shared memory for investigation orchestration
- **Review**: Credibility-scored findings that prune out inaccuracies and hallucinations
- **Timeline**: Most plausible chronology, constructed from credible evidence

These mechanisms work together to maintain coherence across rounds, while preserving the benefits of specialized agent roles. The Director can make informed strategic decisions. Experts can build on previous understanding. The Critic can objectively evaluate findings. The result is investigations that are more thorough and more trustworthy than any single agent could produce alone.

In our next article, we’ll explore how artifacts serve as a communication channel between investigation participants, examining the artifact system that connects findings to evidence and enables the verification workflows described in this article.

### Acknowledgements

We wanted to give a shout out to all the people that have contributed to this journey:

- Chris Smith
- Abhi Rathod
- Dave Russell
- Nate Reeves

Interested in taking on interesting projects, making people’s work lives easier, or just building some pretty cool forms? We’re hiring! 💼

[Apply now](https://slack.com/jobs/dept/engineering)

###
