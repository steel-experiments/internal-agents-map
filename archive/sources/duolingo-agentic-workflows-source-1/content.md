> Archived source snapshot  
> Source ID: `duolingo-agentic-workflows-source-1`  
> Original URL: <https://blog.duolingo.com/agentic-workflows/>  
> Final URL: <https://blog.duolingo.com/agentic-workflows/>  
> Title: Scaling Engineering with Agentic Workflows  
> Captured at: `2026-09-21T12:59:59Z`

---

TL;DR: A good prompt in tools like Cursor helps individual Duos move faster to scale our mission to develop the best education in the world and make it universally accessible. But what if Duos would like to unlock usage of the prompt for an entire team, or even Duolingo as a whole? That’s the goal of agentic workflows. Duos are already building a growing fleet of coding agents customized to Duolingo’s most repetitive tasks. Our engineers use these custom agents to take routine tasks off their plates so they can focus on product thinking and core logic. Better yet, for workflows that follow typical patterns, Duos can now create an agent in under five minutes.

## The agents we have

We have already deployed agents for many routine purposes. Some existing agent capabilities:

- Remove Deprecated Feature Flags
- Launch / Shut Down an Experiment
- Modify Terraform and Create PR

## “The pattern”

As we developed coding agents, we found the same pattern emerged again and again as the simple way to make code changes.

1. Clone the repo
2. The AI agent makes a code change
3. Commit the code and optionally open a PR

When a creator only needs a single agentic pass for an agent to make its change, this pattern can cover a large number of scenarios.

## Make your first agentic workflow in less than 5 minutes!

For common patterns like this, we’ve made it easy for Duos to create a new workflow and share it internally without requiring any custom code. This is not limited to Engineers—PMs, researchers, everyone can set up an agent.

### How to create

Our Duos start by filling out a simple JSON form about the workflow. This form allows them to provide a prompt, a code repo for it to run against, and 0 or more parameters (useful for sharing and reusing the workflow).

![A screenshot of the form, including parameters, prompt, and repository fields.](https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/2025/12/1-1.png)

A screenshot of the form, including parameters, prompt, and repository fields.

### Testing

The prompt is the core of a workflow, so Duos test this prompt until they judge it successful. Generally, we take some time to craft it in [Codex](https://chatgpt.com/codex?ref=blog.duolingo.com) or [Claude](https://duolingo.atlassian.net/wiki/spaces/DUO/pages/4217241800/Getting+Started+with+Claude+Code?ref=blog.duolingo.com), and make sure it works as intended in a variety of situations. Once the prompt is ready and the form filled out, the workflow can be staged for end to end testing. Faster iteration means we can test more ideas to improve learning efficacy for our learners.

### How to run

Once ready, Duos can easily merge their forms for them to automatically show up in a list of internal tools that any Duo can run. We also added Slack notifications to keep users informed about its progress.

## Build your own (on Temporal)

The simple JSON workflow covers a number of scenarios, but it is too simplistic for others, which may need to make multiple agentic passes, run additional tools, determine which tasks to run at runtime, or otherwise do some more interesting work.

Custom workflows are still very easy to make! By running the BootstrapTemporalWorkflow and copying from the existing workflows, our average time for new workflow creation is 1-2 days. The infrastructure around Temporal is evolving quickly, and the platform is flexible. It is likely set up to meet needs, or can be easily made to do so.

## Coding agent library

We have created a single library, CodingAgent, which wraps both Codex CLI and Claude Code SDK into a single library. Once a creator has set up its API keys as environment variables, calling an agent is as simple as declaring a prompt, and in most cases switching agents is as simple as changing a single enum parameter. This is how easy it is to get started:

```
async def simple_codex_prompt(current_working_dir: str):
  agent = CodingAgent()

  result = await agent.prompt(

    prompt="Create a Python function that calculates fibonacci numbers",

    cwd=current_working_dir

  )

  return result

async def simple_claude_prompt(current_working_dir: str):
  agent = CodingAgent(coding_agent_type=CodingAgentType.CLAUDE)

  result = await agent.prompt(

    prompt="Refactor this code to use modern Python best practices",

    cwd=current_working_dir

  )

  return result
```

## Github library

We have set up a util directory for common interactions (cloning a repo, opening a PR, etc.) This repo common code package is used in all of our agents to avoid repeated code, make it easier to follow our key patterns, and generally support development velocity. This library is able to use a shared Github App token to have all of our PRs correctly come from a bot account with centrally controlled permissions.

## Multi-step workflows

While the simple pattern allows us to do interesting work in a single activity, we need multi-step workflows to do more complex work. These workflows are able to do more advanced and long-running work without sacrificing durability. In a multi-step pattern, each step contains a single, retryable activity, with its own timeouts and retry policy. This allows us to make many LLM calls within a single agent without AI non-determinism causing the whole process to restart.

![Screenshot of a temporal workflow, representing 5 different tasks spread across an 11 minute runtime.](https://storage.ghost.io/c/7a/33/7a33d0f4-927d-4fe8-a6bf-96131b5e76d4/content/images/size/w2400/2025/12/2-2.png)

Screenshot of a temporal workflow, representing 5 different tasks spread across an 11 minute runtime.

## Next steps

There are a few key features coming down the pipeline which will enable the agents our Duos build to be even more impactful. A large set of features is blocked by issues running Docker in Docker on Temporal, an issue which is being actively addressed and is expected to be solved within the next month.

### MCP

MCP access is well-established as a way to grant more abilities to any given agent. Prototype agents with access to the Github MCP are able to make reference to other codebases while upgrading their own, significantly improving their ability to solve problems. Other MCP servers, in particular Atlassian, should allow agentic workflows to connect to other portions of Duolingo’s business besides the codebase.

### Expanding agent.json

The JSON created agents run a common workflow under the hood. We can expand its functionality to more flexibly accommodate other common patterns (e.g. multi-step workflows).

## Final thoughts

Agentic workflows are still in their early days at Duolingo, and the pattern captured by this blog post is only one of many. More broadly, both the capabilities of agentic workflows and the best ways to support them with infrastructure remain very much open questions.

With that in mind, this is an early, and by no means definitive, attempt to answer these questions. We expect the space to evolve rapidly.

If you want to work at a place that creates innovative internal tools that make complex engineering tasks easier and is innovating in service of a clear mission, we’re hiring!
