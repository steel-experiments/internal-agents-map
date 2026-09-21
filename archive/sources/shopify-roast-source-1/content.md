> Archived source snapshot  
> Source ID: `shopify-roast-source-1`  
> Original URL: <https://shopify.engineering/introducing-roast>  
> Final URL: <https://shopify.engineering/introducing-roast>  
> Title: Introducing Roast: Structured AI workflows made easy (2025) - Shopify  
> Captured at: `2026-09-21T13:02:03Z`

---

This past year, we started exploring how AI agents could boost developer productivity. In thinking about big developer problems such as flaky tests or lack of test coverage, we found immediate opportunities in grading and optimizing unit tests at scale, with minimal human intervention. Once we began implementing AI workflows, we quickly learned that AI agents need help staying on track, and work much better when you break down complicated prompts into discrete steps. Allowing AI to roam free around millions of lines of code just didn’t work very well. Non-determinism is the enemy of reliability.

To address this challenge, and give AI the structure it needs, the Augmented Engineering Developer Experience (DX) team at Shopify built and open-sourced a new tool called **Roast**.

## What is Roast?

Roast is a convention-oriented workflow orchestration framework designed specifically for creating structured AI workflows that interleave non-deterministic AI behavior with normal non-AI code execution. It provides a declarative approach using YAML configuration and markdown prompts, giving AI agents the guardrails needed to solve developer productivity problems at scale.We extracted Roast from our internal AI tools once we realized its potential to help the broader developer community inside and outside of the company. And while Roast is itself implemented in Ruby, it’s a command line tool that can be used with any other programming languages.

What makes Roast most exciting is its ability to turn complex, multi-step agentic AI processes into reproducible, testable workflows. Whether you're analyzing code quality, generating documentation, or anything else that involves a series of AI and non-AI steps, Roast provides the structure to make the AI parts work reliably at scale. Roast workflows can be version-controlled, tested, and integrated into development workflows easily.

By open-sourcing Roast, we have invited the community to help shape the future of AI-assisted task execution. We believe that structured AI workflows will become as essential to modern development as CI/CD pipelines are today. As a result, a dozen Engineers have already contributed features and workflows to Roast on GitHub.

The name "Roast" comes from our initial use case: roasting your tests to find areas for improvement. Just like a good roast brings out hidden flavors, Roast helps uncover opportunities to enhance your code quality. I have also joked that Roast helps you set your money on fire as you find new ways to burn millions of tokens, but I digress.

### Convention over configuration

Roast follows Ruby on Rails' philosophy of convention over configuration. Simply create a `workflow.yml` file and corresponding prompt files, and you're ready to go:

![](https://cdn.shopify.com/s/files/1/0779/4361/files/workflowyml.png?v=1762811679)

Roast intelligently interprets different step formats based on their structure:

#### 1\. Directory-based steps

The most common type - create a directory with the step name containing a `prompt.md` file:

![](https://cdn.shopify.com/s/files/1/0779/4361/files/workflowyml.png?v=1762811679)

The prompt file can use ERB templating to access workflow context:

![](https://cdn.shopify.com/s/files/1/0779/4361/files/erbtemplate.png?v=1762811863)

#### 2\. Command Execution steps

Wrap shell commands in `$()` to execute them and capture output:

![](https://cdn.shopify.com/s/files/1/0779/4361/files/Screenshot_2025-11-10_at_4.07.35_PM.png?v=1762812478)

#### 3\. Inline Prompt steps

Any string with spaces becomes a direct prompt to the AI model associated with the step. Prefix an inline prompt with a `^` character to prompt Roast’s built-in Coding Agent tool (powered by Claude Code):

![](https://cdn.shopify.com/s/files/1/0779/4361/files/Screenshot_2025-11-10_at_4.08.37_PM.png?v=1762812593)

#### 4\. Custom Ruby steps

For complex logic, Roast allows creation of Ruby step classes that inherit from `BaseStep`:

![](https://cdn.shopify.com/s/files/1/0779/4361/files/Screenshot_2025-11-10_at_4.09.39_PM.png?v=1762812609)

#### 5\. Parallel steps

Use nested arrays to run some steps of your workflow concurrently:

![](https://cdn.shopify.com/s/files/1/0779/4361/files/Screenshot_2025-11-10_at_4.15.54_PM.png?v=1762812966)

### Built-in tools

Roast provides a comprehensive toolkit out of the box:

- **ReadFile**: Reads file contents with line numbers
- **WriteFile**: Writes content to files with security restrictions
- **UpdateFiles**: Applies diffs/patches to multiple files
- **Grep**: Searches file contents using regex patterns
- **SearchFile**: Advanced file search with glob patterns
- **Cmd**: Executes shell commands (with configurable restrictions)
- **Bash**: Unix command execution with proper error handling
- **CodingAgent**: Our most powerful tool—integrates Claude Code directly into workflows

### The CodingAgent: Roast's secret weapon

The CodingAgent is what truly sets Roast apart. It's not just another tool—it's a full integration with Claude Code that brings agentic capabilities into structured workflows. This creates a powerful hybrid approach where you get the best of both worlds:

![](https://cdn.shopify.com/s/files/1/0779/4361/files/Screenshot_2025-11-10_at_4.17.26_PM.png?v=1762813060)

The CodingAgent excels at tasks that require iteration and adaptation:

- **Complex code modifications** that need multiple attempts to get right
- **Bug fixing** where the solution requires exploration and testing
- **Performance optimization** through iterative improvements
- **Test generation** that adapts based on coverage feedback

What makes this revolutionary is how it combines Roast's structured approach with Claude Code's adaptive problem-solving. You define the guardrails and objectives, but the agent has autonomy within those boundaries to iterate, test, and improve until it achieves the goal.

For example, in our workflow for adding Sorbet types (known as “Boba”), we use deterministic steps to clean up the code and run Sorbet's autocorrect, then hand off remaining issues to the CodingAgent. It will iteratively fix type errors, run tests, and ensure everything passes—something that would be nearly impossible with pure deterministic automation.

### Shared context & smart data flow

Steps in a workflow share their conversation transcript, building upon each other's context. This allows for sophisticated workflows where later steps can automatically reference and build upon earlier discoveries without any additional configuration by the workflow author needed:

![](https://cdn.shopify.com/s/files/1/0779/4361/files/Screenshot_2025-11-10_at_4.18.06_PM.png?v=1762813537)

### Advanced control flow

Roast supports sophisticated control structures that go beyond simple sequential execution:

**Iteration over collections:**

![](https://cdn.shopify.com/s/files/1/0779/4361/files/Screenshot_2025-11-10_at_4.18.19_PM.png?v=1762813557)

**Conditional execution:**

![](https://cdn.shopify.com/s/files/1/0779/4361/files/Screenshot_2025-11-10_at_4.18.34_PM.png?v=1762813572)

**Case statements for multi-branch logic:**

![](https://cdn.shopify.com/s/files/1/0779/4361/files/Screenshot_2025-11-10_at_4.18.46_PM.png?v=1762813618)

### Session replay & development experience

One of Roast's killer features is session replay. Every workflow execution is automatically saved, allowing you to resume from any step:

![](https://cdn.shopify.com/s/files/1/0779/4361/files/Screenshot_2025-11-10_at_4.18.59_PM.png?v=1762813636)

This dramatically speeds up workflow development by eliminating the need to rerun expensive AI operations over and over again.

## Example: Grading a Ruby unit test

Let's walk through a real example that showcases Roast's power. Our test grading workflow acts like a senior engineer reviewing your tests:

![](https://cdn.shopify.com/s/files/1/0779/4361/files/Screenshot_2025-11-10_at_4.19.24_PM.png?v=1762813670)

When you run this workflow:

![](https://cdn.shopify.com/s/files/1/0779/4361/files/Screenshot_2025-11-10_at_4.19.41_PM.png?v=1762813694)

You get a comprehensive report:

![](https://cdn.shopify.com/s/files/1/0779/4361/files/Screenshot_2025-11-10_at_4.20.18_PM.png?v=1762813707)

## Getting started with Roast

Roast is distributed as a [Ruby gem](https://rubygems.org/gems/roast-ai), so getting started is pretty straightforward:

![](https://cdn.shopify.com/s/files/1/0779/4361/files/Screenshot_2025-11-10_at_4.20.59_PM.png?v=1762813722)

Prerequisites:

- Ruby 3.0+
- An OpenAI API key (or OpenRouter for other models)
- Optional: `shadowenv` and `ripgrep` for enhanced functionality

## Built on Raix (Ruby AI eXtensions)

Roast leverages [Raix](https://obie.medium.com/announcing-raix-1-0-7c3093de5f54), a library that provides a powerful abstraction layer for AI interactions. Raix enables Roast to work seamlessly with different AI providers and adds advanced features like retry logic, response caching, and structured output handling.

You can customize Raix behavior through initializers in your `.roast/initializers` directory. Here's an example that adds automatic retry logic and debugging:

![](https://cdn.shopify.com/s/files/1/0779/4361/files/Screenshot_2025-11-10_at_4.21.25_PM.png?v=1762813739)

This integration gives you fine-grained control over AI interactions, including:

- Custom authentication schemes
- Request retry strategies
- Response logging and debugging
- Provider-specific configurations
- Token usage tracking

## Real-world impact at Shopify

Since deploying Roast internally, we've seen some fascinating use cases emerge:

**Test quality at scale**: Our engineers have analyzed thousands of test files, automatically identifying and fixing common antipatterns and significantly increasing test coverage across the board.

**Automated type safety with Boba**: We created a Roast workflow called "Boba" that automatically adds Sorbet type annotations to our test files. The workflow performs cleanup with sed, bumps tests to strict typing, runs Sorbet's autocorrect, and then feeds any remaining issues to our coding agent. For example, running boba fully typed a test file that previously had no type annotations, ensuring both tests and type checking pass.

**Proactive site reliability monitoring**: Our SRE team uses Roast to periodically scan internal Slack channels for early indicators of emerging issues. The workflow analyzes conversation patterns, identifies potential problems before they escalate, and alerts the appropriate teams—turning reactive firefighting into proactive incident prevention.

**Competitive intelligence aggregation**: We built a Roast workflow that gathers and consolidates competitive information from multiple sources:

- News and market analysis from third-party web sources
- Migration patterns and brand switching data
- Market trends (gathered via API from customer conversations captured in CRM tools) The workflow synthesizes this disparate data into actionable intelligence reports, saving hours of manual research.

**"Chesterton's Fence" code research tool**: One of our most innovative workflows helps developers understand the historical context of code decisions. When encountering puzzling code, developers can run a Roast workflow that researches the commit history, analyzes related PRs, and explains why particular lines of code exist—preventing the removal of seemingly unnecessary but actually critical code.

## The future of structured AI workflows

When preparing this blog post, I found an amazing quote from [Sam Schmidt](https://github.com/dersam) that captures something truly innovative about Roast:

This is revolutionary thinking. Traditional development forces you to fully understand a problem before automating it. Roast flips this on its head—you can use AI as a placeholder to keep your workflow moving, then replace it with deterministic code once you understand the problem better. It's like having a junior developer who can handle the parts you haven't figured out yet, allowing you to prototype entire workflows before committing to specific implementations. This approach dramatically accelerates the development of complex automation.

We believe Roast represents the future of how developers will work with AI. Rather than ad-hoc prompts in chat interfaces, we see a world where:

- **AI workflows are first-class citizens** in the development process, version-controlled and tested like any other code
- **Hybrid workflows** seamlessly blend deterministic steps with AI-powered analysis
- **Workflow marketplaces** emerge where teams share battle-tested workflows for common tasks
- **AI becomes predictable and reliable when it needs to be** through structured execution rather than free-form generation

Our dream is to see Roast workflows become as ubiquitous as GitHub Actions or Jenkins pipelines—a standard part of every development team's toolkit.
