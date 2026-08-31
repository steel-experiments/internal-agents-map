> Archived source snapshot  
> Source ID: `atlassian-rovo-dev-source-1`  
> Original URL: <https://www.atlassian.com/blog/atlassian-engineering/improving-coding-agent-experience>  
> Final URL: <https://www.atlassian.com/blog/atlassian-engineering/improving-coding-agent-experience>  
> Title: Improving Coding Agent Experience - Inside Atlassian  
> Captured at: `2026-08-31T17:39:24Z`

---

## Introduction

Atlassian is uniquely positioned to create exceptional coding agents. With offerings like Jira, Confluence, Bitbucket, Loom and many more, you get a one stop solution to manage and organize all of your organization’s work.

## Identifying work items suitable for coding agents

Teams create 100s of Jira Tickets every day. In software teams, a lot of these tickets are code related. These are often created to fix bugs, add features, or improve existing code. However, not all of them are well-defined or actionable. Many tickets lack sufficient context or details for a coding agent to understand and act upon them effectively. With this in mind, we looked to explore how can we accurately scope work items suitable for coding agents. Additionally, if we could identify areas for improvement and provide feedback to the work item creator during this process, it could help craft a more scoped and well defined work item description that can help engineers (or AI) pick up the work. To tackle this problem, we first research on what are the indicators of a good task description for a coding agent.

![](https://atlassianblog.wpengine.com/wp-content/uploads/2025/08/7f62db7f-0eda-4fac-ad3a-695a1bc0d62c.png)

### Indicators of a Good Task description

In order to identify suitable work items, we first need to understand what makes a task description good for a coding agent. Based on our research and analysis of internal adoption, we identified the following indicators:

1. **Work item Description Length**: Usually, a lot of work items contain only the task summary and no description. Summary alone gives very little context to the coding Agent.
2. **Work item Description Link Ratio**: Work items with high work item Description Link Ratio are those work items where most of the the characters of the description belong to a link. Think of scenarios where the description is just a link to slack thread or confluence page. Such work items had a fewer chance of completion since the link may not be accessible to the coding agent, If the link is accessible, it may not know how to interpret the information in the link.
3. **Presence of File Paths**: Work item that contain file-paths most likely indicate where the code changes need to be made. This is a strong indicator that the work item is related to code and can be handled by a coding agent.
4. **Presence of Code Snippets**: Work items that contain code snippets usually serve as a reference for the coding agent. They provide context and help the agent understand the existing codebase, making it easier to implement changes or fixes.
5. **Presence of Technical Terms**: Usually, a good prompt to coding agent might refer to the variable name, or function that needs to be modified. It might also instruct on which library needs to be upgraded, etc. This behavior can be captured by looking for technical terms in the work item description.

These are some of the primary indicators we identified. However, there might be more indicators that may be useful.

### Modeling the problem

Given that we have reliable indicators for a good task description (or to identify a not good task!) we now have to choose what model we use?

- **Option 1**: We can use a simple rule based model that checks for the presence of these indicators. This would be fast and easy to implement, but may not capture all the nuances of a good task description.
- **Option 2**: We use a classical ML model, nothing fancy but just good enough to capture the patterns of the indicators using data.
- **Option 3**: We use a large language model (LLM) to classify the work items based on the indicators. This would be powerful, more accurate but slow and expensive. Another problem might be with inconsistent results, as LLM may generate different results for the same input.

We decided to go with **Option 2**. We used a classical ML model to classify the work items based on the indicators. This would be fast, easy to implement and would give us a good baseline to work with. We wanted a fast tunable model that can be retrained quickly as we gather more data.

### Process

For training the model, we used data from internal dogfooding of [Rovo Dev](https://www.atlassian.com/software/rovo-dev) coding agent. The agent is available internally on all Jira sites and we have quite an active user base. Our coding agent on Jira is based on the [HULA](https://www.atlassian.com/blog/atlassian-engineering/hula-blog-autodev-paper-human-in-the-loop-software-development-agents) framework. According to this framework, the development cycle is divided into 4 phases:

1. **Setting the context**: The coding agent needs to understand the context to solve the problem. Here the user can provide the right repository the agent needs to work on. Also this is where we have the opportunity to guide the user to provide a better description of the work item using the indicators we identified.
2. **Generating the plan**: Once the context is satisfactory, the coding agent generates a plan to solve the work item. This plan may get reviewed and/or refined by the user in order to proceed.
3. **Generating the code**: The coding agent generates the code based on the plan. At this point the human can review the code and ask the agent to make any changes.
4. **Raising the PR**: Once the code is ready, the coding agent raises a PR with the generated code. The user can then review the PR and merge it if everything looks good.

To gather data for the model, we took a close look at each instance where the developer engaged with the coding agent. We tracked the phase each work item moved through and made sure to document any changes made to the work item description along the way. Finally, to convert this data into binary classification, we label all work items that were successfully completed by the coding agent, i.e where the developer raised and merged the PR as “positive” samples and all other work items as “negative” samples.

![](https://atlassianblog.wpengine.com/wp-content/uploads/2025/08/a678808a-a0e2-44a7-84b9-ce9c81daf89c.png)

### Results and next steps

The resulting model got us pretty satisfactory results with around **97%** precision in identifying out of scope work items and around **50%** recall in identifying suitable work items. This means that the model is able to identify most of the work items that are not suitable for coding agents, while also being able to identify a good number of work items that are suitable for coding agents. We chose not to show the output of the model to the user as it may confuse them and lead to frustration. Instead we decided to use the model’s features i.e Presence of file paths, code snippets, technical terms, etc. to provide feedback to the user on how to improve the work item description. As to models’s output, we are currently in the works for using it to proactively run the coding agents on simple work items. However, here we have the liberty to use complex models like LLMs to further improve the results.

## Similar work items as code context

Whenever a developer encounters a large new codebase and are tasked with solving a bug or a task, they usually refer to how folks have solved similar work items. This could be talking to folks who have worked on that component, looking at previous commits or looking at PRs on related changes. Coding agents can also harness a similar power by leveraging Jira AI’s similar work items feature. By looking at similar Jira work items and their path to resolution (usually the associated PR), coding agents can learn about the styles, conventions and patterns that teams used within a codebase. This is a feature unique to the Atlassian ecosystem as Atlassian has access to work items of the entire journey from creation → to resolution.

![](https://atlassianblog.wpengine.com/wp-content/uploads/2025/08/similar-issues-flowchart-1-scaled.jpg)

### Methodology

- For a given Jira Work Item, we first fetch the top 50 similar work items.
	- These work items are ranked according to their semantic similarity to the query work item
- Filter out irrelevant work items
	- Items that do not have an associated PR
		- Items with associated PR that is not merged or is declined
		- Items that were created after the query work item
- For the remaining work items, fetch their associated PR diff
- Attach the PR diff and the work item summary and description as additional context to the coding agent

### Results

We regularly benchmark our coding agents against open-source datasets. In fact recently (as of ) RovoDev topped the [SWE-bench full leaderboard](https://www.swebench.com/index.html) with a **41.98%** resolve rate. However, for this particular feature we wanted to see the performance on real Jira work items. So we collected a subset of dogfooding work items from internal usage and evaluated our feature on it. The feature activated for 1/3rd of the dataset i.e 33% of the dataset has eligible similar work items with PR diffs as context. For these similar work items we say a quality gain of around **22.5%.** On closer analysis, we found a few archetypes of work items where similar work items feature played an important role

1. Infra update work items – In software development, there are a lot of small repetitive tasks which revolve around updating DBs, change names of queues changing alarm thresholds.
2. Feature change – changing an existing feature, this revolves around performing minor improvements to an existing feature.
![](https://atlassianblog.wpengine.com/wp-content/uploads/2025/08/3d343666-4d27-4a14-b7ba-6162fd787947.png)

## Conclusion

LLMs which power the coding agents have jagged intelligence, and they suffer from several fundamental problems – hallucination and lack of context being the most pertinent problems. While increasing the model size or algorithmic improvements may address them in the future, we feel current LLMs are capable enough to help solve the low hanging problems that are annoying and time consuming for developers. There are several interesting ways we can augment the coding agent with additional context and scoping that can improve its performance. These features do not require fundamental research into LLMs or investing large amounts of resources on training the next biggest LLM model. These augmentations if implemented smartly can improve the experience of using a coding agent and build trust around the product. Stay tuned for more exciting updates in this domain!
