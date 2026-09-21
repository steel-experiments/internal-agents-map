> Archived source snapshot  
> Source ID: `cursor-support-workflow-source-1`  
> Original URL: <https://cursor.com/blog/cursor-support>  
> Final URL: <https://cursor.com/blog/cursor-support>  
> Title: How technical support at Cursor uses Cursor · Cursor  
> Captured at: `2026-09-21T13:01:02Z`

---

Support investigations are fundamentally research problems, which is why the slowest part of responding to customer challenges has always been gathering the right context. By collapsing code, logs, team knowledge, and past conversations into a single Cursor session, we've removed that bottleneck for most of our work.

Today, over 75% of Cursor's support interactions run through Cursor itself, increasing support engineer throughput 5–10x. This has led to a step-change in what is possible for support engineers from just a year ago.

## Starting from the codebase

When we investigate, we typically begin in Ask Mode. We point it at the symptom and let it trace backward through the relevant product behavior. Because our full codebase is available locally, Cursor can index and use semantic search across product code, docs, and internal tooling in the same session.

This is where multi-root workspaces become powerful. Product context almost always spans multiple repositories. Answering the user question, "Why is this button disabled?" might involve frontend logic, backend policy checks, and docs describing the expected behavior. We keep related repositories together in one workspace so that kind of question is answerable in a single thread.

## Integrating support sources with MCP

We use MCP servers to retrieve context and bring it into our investigations. Our support engineers no longer need to search across several tools to retrieve pertinent context because it is available in Cursor.

MCP servers allow us to integrate:

- Databases with customer information, such as subscription tier, team settings, and privacy settings
- Streamed event logs containing details on services used, telemetry errors, and network issues
- Communication platforms like Slack, filled with threads and conversations that fill out our understanding of how customers interact with the product.
- Engineering ticket platforms containing potentially dozens of unique teams that each operate differently
- An internal documentation service that contains run books and troubleshooting guides
- An account management service containing crucial customer information that may change the tone of how you approach a customer

With Cursor and MCP servers, our support engineers can quickly pull necessary information directly into their codebase investigations.

### Identifying where the failure occurred

When a customer reports an error, we need to understand: Is the problem they're experiencing reproducible or transient, and where exactly did Cursor fail (client-side, API edge, downstream dependency, auth). Datadog MCP lets us pull the relevant logs and traces directly into the investigation thread, allowing us to start narrowing down the possibilities.

### Tracking down similar cases

When a new support ticket comes in, the issue has likely been seen by another customer or someone on our team. An MCP that integrates with your support platform, as well as Slack, allows us to search that context directly and bring the most relevant threads back into the investigation. We search for hard identifiers first (error strings, request IDs), broaden if needed, and look for the newest thread that includes a current status, a workaround, and an owner.

### Determining whether it was a bug

A lot of investigations come down to "bug or expected behavior?" Notion MCP lets us pull the relevant runbook into the thread, cross-reference it against what we're seeing, and either confirm the behavior or escalate with a much clearer bug report.

### Filing a bug report

By the time we finish an investigation in Cursor, we've gathered all the material we need to file a ticket with engineering if something needs to be fixed. The Linear MCP lets us take all of that context and turn it into a formatted escalation directly from the same thread.

### Documentation updates

When multiple customers run into the same questions, it's often a sign that we need to improve our documentation. Technical support is well-positioned to implement these kinds of fixes directly. We just mention @Cursor in Slack with what needs updating, and a cloud agent will open a PR against our docs repo.

## Automating the process

### Commands for common steps

We use slash commands for the most frequently repeated steps in the process:

### Rules and Skills for repeated patterns

We use Rules and Skills to automate common processes in support investigations.

### Subagents to run steps in parallel

Subagents let us run common steps in the support process in parallel rather than sequentially.

- **LogInvestigator** searches Datadog for the failure point and supporting evidence.
- **KnownIssueMiner** scans Slack and Notion for prior threads and workarounds.
- **TicketWriter** formats the evidence into a complete escalation.
- **CustomerReplyDrafter** writes the customer response, stripping out internal details.

The results merge into a single output that we review and send.

## AI-native technical support

By combining these tools, we bring code research directly into the technical support process. We estimate this allows our team to be as much as an order of magnitude more productive compared to traditional approaches, which require more jumping between tools and across teams. This productivity gain enables our small (but growing) team of support engineers to effectively support our rapidly scaling user base.

If you're interested in learning more about how to bring Cursor into your CX workflow, [get in touch](https://cursor.com/).
