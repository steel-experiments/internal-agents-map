> Archived source snapshot  
> Source ID: `notion-custom-agents-source-2`  
> Original URL: <https://www.notion.com/en-gb/blog/how-we-built-security-into-custom-agents>  
> Final URL: <https://www.notion.com/en-gb/blog/how-we-built-security-into-custom-agents>  
> Title: How we built security into Custom Agents  
> Captured at: `2026-08-31T17:45:14Z`

---

Published in [Tech](https://www.notion.com/en-gb/blog/topic/tech)

![](https://www.youtube.com/watch?v=oE3IhArWb2I)

A critical component of our Custom Agents launch was making sure this new kind of AI workflow was as secure as possible for our customers.

Most AI agents today are built for a single user with a relatively simple set of permissions that map to that user. However, agents in a collaborative environment have different needs. Giving them permission to do everything is dangerous, and having permission to do nothing is rarely useful.

With our Custom Agents, we’ve been meticulous in trying to balance both: Have enough access in collaborative environments to be just the right amount of helpful (e.g., assigning a task), but by default, employ strict constraints that ensure the agent can’t take dangerous actions (e.g., deleting all content). Over the years, we’ve built sophisticated permissioning and governance controls for our customers to manage workspaces, and we’ve leveraged those same structures to give our users fine-grain controls of their agents so that they can be as secure as possible in their workspaces.

### Control by default

Custom Agents use a build-from-nothing security model where agents start without access to most resources, meaning no permissions to read, write, or interact with anything.

This approach is a deliberate contrast to many personal AI assistants, which often start with broad access and require users to ensure that safety instructions don’t get compressed out. We don’t want to leave safety to the model’s decision-making. Instead, we wanted safety baked into the access control and deterministic layer.

In this way, we’ve been able to give users granular controls to make the right security decisions for their use cases while enabling advanced users to build incredibly capable autonomous agents.

### Resource-level permissions

Being least permissive by default is a great, but it's important that users can easily build up and understand the permissions they need for their application.

Here are a few notable ones:

- **Page-level granularity for permissions:** Users can grant view or edit access to specific pages, not just broad workspace access
- **First party Slack Integration:** Offering a first party integration for Slack allows us to bring easy-to-configure granular permissions in a way MCP doesn’t
- **Email:** You can choose if you want to confirm before sending emails
- **MCP integrations:** When using an MCP integration, it’s not resource-based, but you can specify the tools you want to be made available, and if you want to ask or always allow certain types of actions

### Security safeguards and warnings

We also had to think about unexpected behaviors during runtime when the agent is actually doing work. Here, we took a multilayer security approach, meaning permission controls plus runtime prompt injection mitigations.

**Prompt-injection protection**: [Prompt injection](https://www.notion.com/help/how-notion-protects-against-prompt-injection-risks) is one of the biggest and most well-known challenges for AI agents. While it remains an unsolved problem, we don’t design our system assuming that all prompt injections will get caught (though we catch many of them). Instead, we designed it such that we have layered controls to block the impact of prompt injection while paying special attention to tagging and monitoring external data to identify potential attacks. In the event that something looks suspicious or the agent performs actions that indicate a potential attack, we can stop the agent and ask a user for confirmation.

**Warning system**: When the agent is about to do something potentially risky, it pauses and asks the user first. How this happens depends on whether the user is configuring or running the agent. When configuring an agent that might do something risky, we give users a set of pop-ups that can range from a simple confirmation to needing to get workspace-admin approvals. When the agent does something risky during runtime, we force it to confirm that action with an owner of the custom agent. This work mirrors our multi-pronged approach to permissions and security broadly across our platform.

**Remediation (i.e., a delete button):** If an agent does mess up, like if it posts something incorrect to Slack, the agent owner can delete that message. This sounds simple but it’s important to give users a way to undo damage if it happens, not just prevent it.

### How we evolved our permission model

To get to this model, we ran an extensive alpha-testing program, both internally across Notion and externally with customers. We specifically wanted to stress-test how security worked in practice at increasing scale. By the end of our alpha testing period, Notion had more than 3,000 internal Custom Agents and our alpha customers had created more than 25,000.

We learned some lessons very quickly. For example, early internal versions of Custom Agents encouraged users to be too permissive without understanding the potential consequences. Users ended up giving agents broad write access to Slack, and on several occasions, those agents even posted to #general (the agent knows every Slack workspace has #general!), the company-wide channel with hundreds of people in it. Clearly, this was not the users’ intent! This is what led us to introduce a new custom “read and reply” permission for Slack that allows agents to reply on to threads they were triggered in explicitly. We view it as our job to introduce permissions like this that allow users to safely get their work done, instead of forcing users to “allow everything.”

This also led us to the deliberate decision to build some first-party integrations rather than relying solely on MCPs. As already discussed, because most MCPs today are designed more for single-player use cases, they generally don’t natively handle resource-based permissions or triggers. Building first-party integrations gave us the control to enforce our permission model without extra work for our customers.

One thing we’re especially proud of: through this process, our own security team has become one of the most active internal users of Custom Agents. For example, they built an agent called [Scruff](https://www.notion.com/blog/meet-scruff-securitys-new-ai-teammate) to triage and enrich security alerts, and they’re using agents for AppSec automation, generating code fixes, and running adversarial tests. It’s been a true collaboration between our AI product team and our security team.

### What’s next

Launch was just the beginning, and we’re investing heavily in better safety and security safeguards as our products and the entire field moves forward. Our Custom Agents beta period over the next couple of months will also help us to continue to improve alongside our customers.

In the coming weeks and months, we expect to tackle:

- Reintroducing broader permission scopes which require workspace admin approval for advanced use cases
- Extend granular permission capabilities to external integrations built on the Workers platform
- Consider additional permission modes for different use cases once more guardrails are in place

We’re still in the early phases of building out this technology, and we welcome feedback from the community on how to improve.
