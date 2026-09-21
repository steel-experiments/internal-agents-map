> Archived source snapshot  
> Source ID: `shopify-roast-source-2`  
> Original URL: <https://github.com/Shopify/roast>  
> Final URL: <https://github.com/Shopify/roast>  
> Title: GitHub - Shopify/roast: Structured AI workflows made easy · GitHub  
> Captured at: `2026-09-21T13:04:59Z`

---

[![roast-horiz-logo](https://private-user-images.githubusercontent.com/3908/442207502-f9b1ace2-5478-4f4a-ac8e-5945ed75c5b4.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODk5OTYxOTIsIm5iZiI6MTc4OTk5NTg5MiwicGF0aCI6Ii8zOTA4LzQ0MjIwNzUwMi1mOWIxYWNlMi01NDc4LTRmNGEtYWM4ZS01OTQ1ZWQ3NWM1YjQucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDkyMSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA5MjFUMTMwNDUyWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9Y2VmNmI2YWY2ODVlN2IzMTdmNTY2ZmIxNzYwZGI4N2M0NWM0M2ZmN2NmZDNmNmJiODEzOGI4OWJmY2U2MDM3NyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.SPAbtfmAnrPA76Eh8PG7cVdg38WNK0lQMgeNoXooepY)](https://private-user-images.githubusercontent.com/3908/442207502-f9b1ace2-5478-4f4a-ac8e-5945ed75c5b4.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODk5OTYxOTIsIm5iZiI6MTc4OTk5NTg5MiwicGF0aCI6Ii8zOTA4LzQ0MjIwNzUwMi1mOWIxYWNlMi01NDc4LTRmNGEtYWM4ZS01OTQ1ZWQ3NWM1YjQucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDkyMSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA5MjFUMTMwNDUyWiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9Y2VmNmI2YWY2ODVlN2IzMTdmNTY2ZmIxNzYwZGI4N2M0NWM0M2ZmN2NmZDNmNmJiODEzOGI4OWJmY2U2MDM3NyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.SPAbtfmAnrPA76Eh8PG7cVdg38WNK0lQMgeNoXooepY)

## Roast

A Ruby-based domain-specific language for creating structured AI workflows. Build complex AI-powered automation with simple, declarative Ruby syntax.

## Overview

Roast lets you orchestrate AI workflows by combining "cogs" - building blocks that interact with LLMs, run code, execute commands, and process data. Write workflows that:

- **Chain AI steps together** - Output from one cog flows seamlessly to the next
- **Run coding agents locally** - Full filesystem access with Pi, Claude Code, or other providers
- **Process collections** - Map operations over arrays with serial or parallel execution
- **Control flow intelligently** - Conditional execution, iteration, and error handling
- **Reuse workflow components** - Create modular, parameterized scopes

## Quick Example

```
# analyze_codebase.rb
execute do
  # Get recent changes
  cmd(:recent_changes) { "git diff --name-only HEAD~5..HEAD" }

  # AI agent analyzes the code
  agent(:review) do
    files = cmd!(:recent_changes).lines
    <<~PROMPT
      Review these recently changed files for potential issues:
      #{files.join("\n")}

      Focus on security, performance, and maintainability.
    PROMPT
  end

  # Summarize for stakeholders
  chat(:summary) do
    "Summarize this for non-technical stakeholders:\n\n#{agent!(:review).response}"
  end
end
```

Run with:

```
bin/roast execute analyze_codebase.rb
```

## Core Cogs

- **`chat`** - Send prompts to cloud-based LLMs (OpenAI, Anthropic, Perplexity & Gemini)
- **`agent`** - Run local coding agents with filesystem access (Pi CLI, Claude Code CLI, etc.)
- **`ruby`** - Execute custom Ruby code within workflows
- **`cmd`** - Run shell commands and capture output
- **`map`** - Process collections in serial or parallel
- **`repeat`** - Iterate until conditions are met
- **`call`** - Invoke reusable workflow scopes

## Installation

```
gem install roast-ai
```

Or add to your Gemfile:

```
gem 'roast-ai'
```

## Requirements

- Ruby 3.0+
- API keys or local credentials for your AI provider
- Pi CLI installed (for the default agent provider)

## Provider Configuration

Roast provider settings are configured in workflow `config` blocks. To change the default **chat** provider without editing each workflow, set the `ROAST_DEFAULT_CHAT_PROVIDER` environment variable (e.g. `export ROAST_DEFAULT_CHAT_PROVIDER=anthropic`). To change the default **agent** provider, set `ROAST_DEFAULT_AGENT_PROVIDER`. A `provider` set in a workflow's `config` always takes precedence over these variables, and an invalid value raises an error.

### Chat cog

The `chat` cog supports **OpenAI**, **Anthropic**, **Perplexity**, and **Gemini**. It defaults to `:openai` (override globally with `ROAST_DEFAULT_CHAT_PROVIDER`). Each provider reads its API key from a provider-specific environment variable:

| Provider | API key env var | Base URL env var |
| --- | --- | --- |
| `:openai` | `OPENAI_API_KEY` | `OPENAI_API_BASE` |
| `:anthropic` | `ANTHROPIC_API_KEY` | `ANTHROPIC_API_BASE` |
| `:perplexity` | `PERPLEXITY_API_KEY` | — |
| `:gemini` | `GEMINI_API_KEY` | `GEMINI_API_BASE` |

You can configure the provider directly in a workflow:

```
config do
  chat do
    provider :anthropic
    model "claude-haiku-4-5"
  end
end
```

### Agent cog

The `agent` cog runs local agent CLIs. It defaults to `:pi` (override globally with `ROAST_DEFAULT_AGENT_PROVIDER`) and currently supports:

- `:claude` - Claude Code CLI
- `:pi` - Pi CLI

Select a provider in the workflow config:

```
config do
  agent do
    provider :pi
  end
end
```

Agent providers must be installed and authenticated according to their own CLI requirements.

## Configuration

Roast currently supports four LLM providers for the `chat` cog: **OpenAI**, **Anthropic**, **Perplexity** and **Gemini**.

- Set `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `PERPLEXITY_API_KEY` and/or `GEMINI_API_KEY` in your environment.
- Optionally set `OPENAI_API_BASE`, `ANTHROPIC_API_BASE` and/or `GEMINI_API_BASE` to override the default endpoint. Perplexity does not support base URL override.

The default model is set per-provider and can only be overridden inside a `config` block. See the [tutorial](https://github.com/Shopify/roast/blob/main/tutorial/01_your_first_workflow/README.md#adding-configuration) for examples.

The `agent` cog is powered by the Pi CLI by default, which handles its own authentication.

## Getting Started

The best way to learn Roast is through the interactive tutorial:

📚 **[Start the Tutorial](https://github.com/Shopify/roast/blob/main/tutorial/README.md)**

The tutorial covers:

1. Your first workflow
2. Chaining cogs together
3. Accepting targets and parameters
4. Configuration options
5. Control flow
6. Reusable scopes
7. Processing collections
8. Iterative workflows
9. Async execution

## Documentation

- [Tutorial](https://github.com/Shopify/roast/blob/main/tutorial/README.md) - Step-by-step guide with examples
- [Workflow Examples](https://github.com/Shopify/roast/tree/main/examples) - Toy workflows that demonstrate all functional patterns, use for end-to-end test

## Documentation & References

- **Source code root**: [https://github.com/Shopify/roast/tree/main/lib/roast](https://github.com/Shopify/roast/tree/main/lib/roast)

The public interfaces of Roast are extensively documented in class and method comments on the relevant classes.

- **Tutorial and Examples**
	- [Tutorial -- Table of Contents](https://github.com/Shopify/roast/tree/main/tutorial) (contains step-by-step guides and runnable examples showing real-world usage)
		- Additional Example Workflows (these comprise the Roast end-to-end test suite)
- **Configuation**
	- [General configuration block: `config-context.rbi`](https://github.com/Shopify/roast/blob/main/sorbet/rbi/shims/lib/roast/config_context.rbi)
		- [Workflow params in cog config blocks: `cog/config.rbi`](https://github.com/Shopify/roast/blob/main/sorbet/rbi/shims/lib/roast/cog/config.rbi)
		- [Global cog configuration: `cog/config.rb`](https://github.com/Shopify/roast/blob/main/lib/roast/cog/config.rb)
		- [Agent cog configuration: `agent/config.rb`](https://github.com/Shopify/roast/blob/main/lib/roast/cogs/agent/config.rb)
		- [Chat cog configuration: `chat/config.rb`](https://github.com/Shopify/roast/blob/main/lib/roast/cogs/chat/config.rb)
		- [Cmd cog configuration: `cmd/config.rb`](https://github.com/Shopify/roast/blob/main/lib/roast/cogs/cmd.rb)
		- [Map cog configuration: `map.rb`](https://github.com/Shopify/roast/blob/main/lib/roast/system_cogs/map.rb)
- **Execution**
	- [General Execution block: `execution-context.rbi`](https://github.com/Shopify/roast/blob/main/sorbet/rbi/shims/lib/roast/execution_context.rbi)
- **Input and Output**
	- [General cog input block: `cog-input-context.rbi`](https://github.com/Shopify/roast/blob/main/sorbet/rbi/shims/lib/roast/cog_input_context.rbi)
		- [Global cog output: `cog/output.rb`](https://github.com/Shopify/roast/blob/main/lib/roast/cog/output.rb)
		- [Agent cog input `agent/input.rb`](https://github.com/Shopify/roast/blob/main/lib/roast/cogs/agent/input.rb)
		- [Agent cog output `agent/output.rb`](https://github.com/Shopify/roast/blob/main/lib/roast/cogs/agent/output.rb)
		- [Call cog input: `call.rb`](https://github.com/Shopify/roast/blob/main/lib/roast/system_cogs/call.rb)
		- [Chat cog input: `chat.rb`](https://github.com/Shopify/roast/blob/main/lib/roast/cogs/chat/input.rb)
		- [Chat cog output: `chat.rb`](https://github.com/Shopify/roast/blob/main/lib/roast/cogs/chat/output.rb)
		- [Cmd cog input: `cmd.rb:159`](https://github.com/Shopify/roast/blob/main/lib/roast/cogs/cmd.rb#L159) (scroll down)
		- [Cmd cog output: `cmd.rb:214`](https://github.com/Shopify/roast/blob/main/lib/roast/cogs/cmd.rb#L214) (scroll down)
		- [Map cog input: `map.rb:116`](https://github.com/Shopify/roast/blob/main/lib/roast/system_cogs/map.rb#L116) (scroll down)
		- [Repeat cog input: `repeat.rb`](https://github.com/Shopify/roast/blob/main/lib/roast/system_cogs/repeat.rb)
		- [Ruby cog input: `ruby.rb`](https://github.com/Shopify/roast/blob/main/lib/roast/cogs/ruby.rb)
		- [Ruby cog output: `ruby.rb:63`](https://github.com/Shopify/roast/blob/main/lib/roast/cogs/ruby.rb#L63) (scroll down)
