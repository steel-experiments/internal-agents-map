> Archived source snapshot  
> Source ID: `spotify-honk-xirp-source-1`  
> Original URL: <https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1>  
> Final URL: <https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1>  
> Title: 1,500+ PRs Later: Spotify’s Journey with Our Background Coding Agent (Honk, Part 1) | Spotify Engineering  
> Captured at: `2026-08-31T17:49:28Z`

---

**Spotify Portal for Backstage is now GA!** [Read the announcement](https://backstage.spotify.com/discover/blog/spotify-portal-ga-webinar-october-2025/)

![Feature Image](https://images.ctfassets.net/p762jor363g1/6yHrb91pjUnOVWe2W5tTkW/7aa7ce0f1ad1b0e271e7574fbe2c05b0/honk-pt1.png)

*This is part 1 in our series about Spotify's journey with background coding agents (internal codename: “Honk”) and the future of large-scale software maintenance. See also* [*part 2*](https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2)*,* [*part 3*](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3)*, and* [*part 4*](https://engineering.atspotify.com/2026/4/background-coding-agents-dataset-migrations-honk-part-4)*.*

For years, developer productivity has improved through better tooling. We have smarter IDEs, faster builds, better tests, and more reliable deployments. But even so, maintaining a codebase, keeping dependencies up to date, and ensuring that the code follows best practices demands a surprising amount of manual work. At Spotify, our [Fleet Management system](https://engineering.atspotify.com/2023/04/spotifys-shift-to-a-fleet-first-mindset-part-1) automated much of that toil, yet any moderately complex migration still requires many human hands.

What if we could close that final gap?

This post explores how we have evolved our Fleet Management platform with background coding agents and what more than 1,500 merged AI-generated pull requests have taught us about the future of large-scale software maintenance.

## Automating toil using Fleet Management

Fleet Management is a powerful framework for applying code transformations across all of Spotify’s repositories. The idea is simple: We write small snippets of code that themselves modify source code and apply these transformations to thousands of software components. This way we can take care of maintenance tasks across our codebase.

On a high level, Fleet Management has been a roaring success. It has allowed us to automate away countless hours of toil, vastly reducing the time to roll out fleet-wide changes. The system works by running these source-to-source transformations as jobs, in a containerized environment, which then automatically open pull requests against the target repositories.

![Figure 1: Creating pull requests using Fleet Management.](https://images.ctfassets.net/p762jor363g1/70GvT50eAkvc3jymOnrRAI/efd3cbfcceb45d8a7132e435492932f7/Background_Coding_Agents_Chart_1.png)

Figure 1: Creating pull requests using Fleet Management.

This approach has excelled in several areas, including:

- **Bumping dependencies** in build files, such as in a Maven Project Object Model (POM) files
- **Updating configuration files**, such as deployment manifests
- **Executing simple code refactors**, like removing or replacing a deprecated method call

The impact has been significant, with a steady stream of automated pull requests being merged daily, keeping our codebases consistent, up to date, and secure. Since mid-2024, around half of Spotify’s pull requests have been automated by this system.

![Background coding agent_graph 1.png](https://images.ctfassets.net/p762jor363g1/220g9TGAQEjsqZP5SLM1bF/be499e0d9cbfba606d71a6f749f57a36/Background_coding_agent_graph_1.png)

Figure 2: Ratio of merged PRs that are coming from Fleetshift versus from human authors.

But we knew from the beginning that this approach has its limits. While it is great for simple, repeatable tasks, making *complex* *code changes* is a challenge we’ve never fully solved. Defining source code transformations programmatically, by manipulating a program’s abstract syntax tree (AST) or using regular expressions, requires a high degree of specialized expertise. One example is our automated Maven dependency updater. While its core function — identifying pom.xml files and updating Java dependencies — is straightforward, handling all corner cases has led to the transformation script growing to over 20,000 lines of code. Because of this complexity, most of the automated changes we could implement were simple ones. Only a few teams have the required expertise and time to implement more sophisticated Fleetshifts over our entire codebase.

At the same time, AI tools are becoming much more capable of making complex code changes. This presented a clear and promising opportunity:

👉 Can we apply AI to lower the barrier to entry and unlock the power of Fleet Management for more complex changes?

## Enter AI coding agents

Last February, we began an investigation into using AI agents within our Fleet Management system. The goal was to allow engineers to define and run fleet-wide changes using natural language.

![Background coding agent_final_chart 2.png](https://images.ctfassets.net/p762jor363g1/6EtDC6ht4fO6iTqLvME9M9/df370472e190546d5d8482b4b860f4ed/Background_coding_agent_final_chart_2.png)

Figure 3: Integration of coding agents into our Fleet Management architecture.

We started with the part of the process that needed the most help: the declaration of the code transformation itself. We replaced deterministic migration scripts with an agent that takes instructions from a prompt. All the surrounding Fleet Management infrastructure — targeting repositories, opening pull requests, getting reviews, and merging into production — remains exactly the same.

![Background coding agents_coding block image 1_final.png](https://images.ctfassets.net/p762jor363g1/6MGCD8hOs31qnrvGEFKk4q/02b6d92aab92e7c7d2b569c22d40dcda/Background_coding_agents_coding_block_image_1_final.png)

Figure 4: Configuring a Fleetshift with a prompt.

Instead of adopting an off-the-shelf coding agent as it is, we decided to build a small internal CLI. This CLI can delegate executing a prompt to an agent, run custom formatting and linting tasks using local Model Context Protocol (MCP), evaluate a diff using LLMs as a judge, upload logs to Google Cloud Platform (GCP), and capture traces in MLflow. Crucially, having that CLI allows us to seamlessly switch between different agents and LLMs. In the fast-moving environment that is GenAI, being flexible and pluggable this way has already allowed us to swap out pieces multiple times, giving our users a preconfigured and well-integrated tool out of the box, without exposing them to the nitty-gritty details.

![Background coding agents_graph 2_final.png](https://images.ctfassets.net/p762jor363g1/63WgLl3xBhluKB1VOG25R/745368205524d9cb28fca68cfed5c105/Background_coding_agents_graph_2_final.png)

Figure 5: Total number of pull requests from our coding agent merged into production.

We saw an immediate need for this type of product internally. We were codeveloping the tooling alongside early adopters who applied it to their in-flight migrations. To date, our agents have generated more than 1,500 pull requests that teams across Spotify have merged into our production codebase. And not trivial changes, either — we’re now starting to tackle changes such as:

- **Language modernization,** such as replacing Java value types with [records](https://openjdk.org/jeps/395)
- **Upgrades with breaking changes,** such as migrating data pipelines to the newest version of [Scio](https://github.com/spotify/scio)
- **Migrating between UI components,** such as moving to the [new frontend system](https://backstage.io/docs/frontend-system/building-plugins/migrating/) in Backstage
- **Config changes**, such as updating parameters in YAML or JSON files and still adhering to schemas and formatting

For these migrations we’ve seen a total time saving of 60–90% compared to writing the code by hand the good old-fashioned way. The ROI for an automated change also continues to increase as we scale it out to more and more codebases over time. We consider this a very promising start, and we strongly believe that we are only scratching the surface of what’s possible in terms of leveraging AI in the migration space.

## Beyond just migrations

What if you could also trigger the same agent from your IDE or chat, give it a task, and then go to lunch? Over time, it became clear that there is a need for a background coding agent not only for migrations, but also for ad hoc tasks.

![Background Coding Agents Chart 3.png](https://images.ctfassets.net/p762jor363g1/3rZBv0n051aDu7m7tqjsfS/536f6aa99320bbccf5b2140809fc2af3/Background_Coding_Agents_Chart_3.png)

Figure 6: Current multi-agent architecture for planning, generating, and reviewing pull requests.

By exposing our background coding agent via MCP, Spotifiers can now kick off coding agent tasks from both Slack and GitHub Enterprise. They first talk to an interactive agent that helps to gather information about the task at hand. This interaction results in a prompt that is then handed off to the coding agent, which produces a pull request.

![Background coding Agents_Coding Block 2_Final.png](https://images.ctfassets.net/p762jor363g1/2ol97tzSD0OtbY6GYLk0q6/8c474e9297bd301ecd3868814458b652/Background_coding_Agents_Coding_Block_2_Final.png)

Figure 7: Employee interacting with our workflow agent in our internal chat.

We quickly found enthusiastic users for this feature, for example, as a lightweight way for engineers to capture architecture decision records (ADRs) from a thread in Slack, or product managers that can now propose simple changes without cloning and building repos on their laptops.

We have seen a nice symbiosis between the migration and background agent use cases. For example, improvements to the agent configuration and tools now apply to any PRs generated, no matter the source of the task. We also benefit from the standardization, say, in terms of tagging commits, managing LLM quotas, or collecting traces.

## New challenges with background agents

Introducing AI agents into our migration and developer workflows is a new and exciting space for us. We see great impact and momentum from our first iteration of tools: hundreds of developers now interact with our agent, and we’ve already merged more than 1500 pull requests.

But coding agents come with an interesting set of trade-offs. Performance is a key consideration, as agents can take a long time to produce a result, and their output can be unpredictable. This creates a need for new validation and quality control mechanisms. Beyond performance and predictability, we also have to consider safety and cost. We need robust guardrails and sandboxing to ensure agents operate as intended, all while managing the significant computational expense of running LLMs at scale.

We don’t have all the answers yet, but addressing these challenges is where our team is focusing its efforts. We’re excited to share more of what we’re learning as we explore this space. Stay tuned for our follow-up posts on effective context engineering and using feedback loops to achieve more predictable results.
