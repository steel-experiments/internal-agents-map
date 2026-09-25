# Lesson and note follow-up review

Reviewed on 2026-09-16–17 against `e10443b` after the implementation audit of Plan 008.
The audit found that a shared confidence disclaimer had replaced the previous one,
the notes retained their template, and the overview contradicted the monday.com
record. This follow-up checks the prose against the preserved source passages.

## Lesson decisions

All 100 lessons across 29 entries were reviewed. The retained set has 70 reported
practices, 24 attributed opinions, and 6 catalog inferences. Each has a distinct
confidence explanation and a locator into its evidence. These counts describe the
editorial decisions, not an objective measure of writing quality.

Reported practices now describe the implementation or workflow. Opinions name their
author or organization. Inferences identify the supporting observation and the
remaining uncertainty. General prescriptions were removed where the source only
documents a particular team's choice. Existing lesson indexes were retained so claim
links continue to resolve.

Some corrections required changing the assertion, not just its qualification:

- Stripe's source describes prepared devboxes; it does not say Minions chooses the
  repository or provisions the workspace.
- Linear completion events notify a support workflow; a person follows up with the
  customer. The agent does not automatically send that customer response.
- WorkOS's MCP tuning account is in its architecture post, not the showcase previously
  cited. Two reported harnesses do not establish a complete platform migration.
- Spotify's sources support CI tools, catalog access, and lint feedback. They do not
  support the discarded credential comparison or a measured context multiplier.
  The same credential assertion was removed from the architecture: the captures
  document containers and Kubernetes pods, not credential inheritance. The optional
  credentials field and its evidence edges were removed, reducing the catalog to
  590 claims. Model and knowledge descriptions now cite the passages that describe
  each version and tool surface.
- Sentry's preference for a general agent remains an opinion. Its concrete evaluation
  practice is retained without extending the author's rejection of unit tests to all
  software.
- Ramp's pivot preceded growing adoption; the report does not isolate a cause.
- Zup's preserved abstract supports the authors' stated conclusions, but cannot supply
  the missing experiments or definitions of oversight modes.
- Worktree separation at Coinbase and cross-round context at Slack do not establish,
  respectively, a security sandbox or recovery after process failure.

## Summaries and cross-page consistency

The pass also reviewed the 40 entry summaries and their component descriptions.
Eighteen records needed wording changes. These remove absolute credential promises,
unqualified cost claims, assumed automatic improvement, and the implication that
WorkOS normally requires only acceptance testing. Sevbot's source contains both
“never executes any” and an engineer-directed application step; the confidence note
now states the interpretation of that ambiguity and uses medium confidence.

The architecture overview now agrees with the two monday.com scopes: Morphex is
exception-only and Atlas is unknown. Recovery examples identify an actual saved
record. Adoption guidance no longer implies that every accepted change was accepted
by a person, or attributes an unmeasured shift in review effort to Harvey.

Supplementary source relationships were retained for the rewritten summaries. No
archive bytes, source retrieval dates, organization records, or logos changed.
Browserbase and Retool remain absent from the active catalog.

## Note decisions

| Note | Structure and editorial decision | Preserved passages checked |
| --- | --- | --- |
| [Stop a run](../src/content/lessons/stop-a-run.md) | Compare attempt limits with elapsed-time deadlines; retain the quotation about a stuck turn counter; draw conditional exits and a retry branch. Mark the combined handoff as a proposal. | Stripe part 2, 94–98; Dropbox, 58–62; DoorDash reviewer, 162 |
| [Review noise](../src/content/lessons/review-noise.md) | Prose about published findings, missed defects, and human follow-up cost. Remove the quotation and diagram that repeated it. Separate proposed evaluation from reported measurements. | Uber, 84, 128–148; HubSpot, judge-agent account |
| [Split the work](../src/content/lessons/split-the-work.md) | Explain both earlier failures, then draw the scout's shared leads reaching two reviewers. Keep the absence of a controlled version comparison. | DoorDash reviewer, 38–42 |
| [Work can continue](../src/content/lessons/work-can-continue.md) | Draw two workers connected to a session outside either worker. Compare the scope of conversation, file, and external-action recovery. | Shopify, 116–142; Sentry, 136; Sierra Agency, 78–86 |
| [Load tools](../src/content/lessons/load-tools.md) | Compare schema search with provider connection in a table. Name discovery and authorization failures instead of repeating a general context warning. | Cloudflare, 179–189; Sentry, 226–236 |
| [Steps without a model](../src/content/lessons/steps-without-a-model.md) | Explain required execution, publication authority, and approval eligibility as different controls. Remove the generic sequential diagram. | Stripe part 2, 52–60; Dropbox, 32, 80; pinned StampHog README, 19, 119–125 |
| [Test on your work](../src/content/lessons/test-on-your-work.md) | Follow task reconstruction, alternative implementations, and calibration of judges. Explain benchmark scope and coverage limits without a stock ending. | Databricks benchmark, 92–97; coSTAR, 58, 113–117, 167–175; Uber, 84, 108 |

All seven were read together after rewriting. There is one retained quotation and
three diagrams, each with a different job: branching, parallel work, or shared state.
The other notes use prose or a comparison table. No note retains the repeated
observation panel or closing reader question. Notes remain 233–269 words in the
authored body under a simple whitespace count; slugs, source URLs, related IDs, and
publication dates remain stable. The modification date is 2026-09-16.

## Validation

The implementation plan records the final command results. Source and editorial
review above are separate from automated checks. Browser coverage compares headings,
diagram text, table cells, and source links with the Markdown export for every note,
and checks page width on desktop, mobile, and with JavaScript disabled.

## Passage inventory

Lesson indexes below are zero-based and match the YAML field paths. The full
statement and confidence explanation live in the linked record. Line numbers include
the archive header and refer to the immutable `content.md` capture.

| Entry | Lesson | Decision | Preserved evidence |
| --- | ---: | --- | --- |
| [block-builderbot](../data/agents/block-builderbot.yaml) | 0 | opinion / reported | [block-builderbot-source-1](../archive/sources/block-builderbot-source-1/content.md), 26 |
| [block-builderbot](../data/agents/block-builderbot.yaml) | 1 | fact / reported | [block-builderbot-source-1](../archive/sources/block-builderbot-source-1/content.md), 16 |
| [block-builderbot](../data/agents/block-builderbot.yaml) | 2 | fact / reported | [block-builderbot-source-1](../archive/sources/block-builderbot-source-1/content.md), 16 |
| [brex-agent-platform](../data/agents/brex-agent-platform.yaml) | 0 | opinion / reported | [brex-agent-platform-source-1](../archive/sources/brex-agent-platform-source-1/content.md), 153-159 |
| [brex-agent-platform](../data/agents/brex-agent-platform.yaml) | 1 | fact / reported | [brex-agent-platform-source-1](../archive/sources/brex-agent-platform-source-1/content.md), 38-40 |
| [brex-agent-platform](../data/agents/brex-agent-platform.yaml) | 2 | fact / reported | [brex-agent-platform-source-1](../archive/sources/brex-agent-platform-source-1/content.md), 159 |
| [brex-agent-platform](../data/agents/brex-agent-platform.yaml) | 3 | fact / reported | [brex-agent-platform-source-1](../archive/sources/brex-agent-platform-source-1/content.md), 195-205 |
| [brex-agent-platform](../data/agents/brex-agent-platform.yaml) | 4 | fact / reported | [brex-agent-platform-source-1](../archive/sources/brex-agent-platform-source-1/content.md), 54-60 |
| [cloudflare-ai-stack](../data/agents/cloudflare-ai-stack.yaml) | 0 | fact / reported | [cloudflare-ai-stack-source-1](../archive/sources/cloudflare-ai-stack-source-1/content.md), 105 |
| [cloudflare-ai-stack](../data/agents/cloudflare-ai-stack.yaml) | 1 | fact / reported | [cloudflare-ai-stack-source-1](../archive/sources/cloudflare-ai-stack-source-1/content.md), 195-212 |
| [cloudflare-ai-stack](../data/agents/cloudflare-ai-stack.yaml) | 2 | fact / reported | [cloudflare-ai-stack-source-1](../archive/sources/cloudflare-ai-stack-source-1/content.md), 179-189 |
| [cloudflare-ai-stack](../data/agents/cloudflare-ai-stack.yaml) | 3 | fact / reported | [cloudflare-ai-stack-source-1](../archive/sources/cloudflare-ai-stack-source-1/content.md), 84-103 |
| [coinbase-forge-mux](../data/agents/coinbase-forge-mux.yaml) | 0 | fact / reported | [coinbase-forge-mux-source-1](../archive/sources/coinbase-forge-mux-source-1/content.md), 12,24 |
| [coinbase-forge-mux](../data/agents/coinbase-forge-mux.yaml) | 1 | fact / reported | [coinbase-forge-mux-source-2](../archive/sources/coinbase-forge-mux-source-2/content.md), 32-36 |
| [coinbase-forge-mux](../data/agents/coinbase-forge-mux.yaml) | 2 | inference / catalog-judgment | [coinbase-forge-mux-source-1](../archive/sources/coinbase-forge-mux-source-1/content.md), 26 |
| [coinbase-forge-mux](../data/agents/coinbase-forge-mux.yaml) | 3 | fact / reported | [coinbase-forge-mux-source-5](../archive/sources/coinbase-forge-mux-source-5/content.md), 120 |
| [coinbase-forge-mux](../data/agents/coinbase-forge-mux.yaml) | 4 | fact / reported | [coinbase-forge-mux-source-3](../archive/sources/coinbase-forge-mux-source-3/content.md), 11 |
| [coinbase-forge-mux](../data/agents/coinbase-forge-mux.yaml) | 5 | opinion / reported | [coinbase-forge-mux-source-5](../archive/sources/coinbase-forge-mux-source-5/content.md), 170-172; [coinbase-forge-mux-source-4](../archive/sources/coinbase-forge-mux-source-4/content.md), 23-25 |
| [domu-clementino](../data/agents/domu-clementino.yaml) | 0 | fact / reported | [domu-clementino-source-1](../archive/sources/domu-clementino-source-1/content.md), 54-72,98 |
| [domu-clementino](../data/agents/domu-clementino.yaml) | 1 | fact / reported | [domu-clementino-source-1](../archive/sources/domu-clementino-source-1/content.md), 64-72,90 |
| [domu-clementino](../data/agents/domu-clementino.yaml) | 2 | fact / reported | [domu-clementino-source-1](../archive/sources/domu-clementino-source-1/content.md), 78,92 |
| [doordash-code-review](../data/agents/doordash-code-review.yaml) | 0 | opinion / reported | [doordash-code-review-source-1](../archive/sources/doordash-code-review-source-1/content.md), 56-68,166 |
| [doordash-code-review](../data/agents/doordash-code-review.yaml) | 1 | inference / catalog-judgment | [doordash-code-review-source-1](../archive/sources/doordash-code-review-source-1/content.md), 56-68 |
| [doordash-flux](../data/agents/doordash-flux.yaml) | 0 | fact / reported | [doordash-flux-source-3](../archive/sources/doordash-flux-source-3/content.md), 85 |
| [doordash-flux](../data/agents/doordash-flux.yaml) | 1 | opinion / reported | [doordash-flux-source-3](../archive/sources/doordash-flux-source-3/content.md), 86 |
| [doordash-flux](../data/agents/doordash-flux.yaml) | 2 | fact / reported | [doordash-flux-source-3](../archive/sources/doordash-flux-source-3/content.md), 87 |
| [doordash-flux](../data/agents/doordash-flux.yaml) | 3 | fact / reported | [doordash-flux-source-2](../archive/sources/doordash-flux-source-2/content.md), 58-66 |
| [doordash-flux](../data/agents/doordash-flux.yaml) | 4 | fact / reported | [doordash-flux-source-2](../archive/sources/doordash-flux-source-2/content.md), 80-82 |
| [doordash-flux](../data/agents/doordash-flux.yaml) | 5 | fact / reported | [doordash-flux-source-2](../archive/sources/doordash-flux-source-2/content.md), 94 |
| [dropbox-nova](../data/agents/dropbox-nova.yaml) | 0 | opinion / reported | [dropbox-nova-source-1](../archive/sources/dropbox-nova-source-1/content.md), 78 |
| [dropbox-nova](../data/agents/dropbox-nova.yaml) | 1 | fact / reported | [dropbox-nova-source-1](../archive/sources/dropbox-nova-source-1/content.md), 26 |
| [dropbox-nova](../data/agents/dropbox-nova.yaml) | 2 | fact / reported | [dropbox-nova-source-1](../archive/sources/dropbox-nova-source-1/content.md), 80 |
| [dropbox-nova](../data/agents/dropbox-nova.yaml) | 3 | fact / reported | [dropbox-nova-source-1](../archive/sources/dropbox-nova-source-1/content.md), 20-22,55 |
| [flex-investigation-agent](../data/agents/flex-investigation-agent.yaml) | 0 | fact / reported | [flex-investigation-agent-source-1](../archive/sources/flex-investigation-agent-source-1/content.md), 152-157 |
| [flex-investigation-agent](../data/agents/flex-investigation-agent.yaml) | 1 | fact / reported | [flex-investigation-agent-source-1](../archive/sources/flex-investigation-agent-source-1/content.md), 99-113 |
| [harvey-spectre](../data/agents/harvey-spectre.yaml) | 0 | fact / reported | [harvey-spectre-source-1](../archive/sources/harvey-spectre-source-1/content.md), 16,24 |
| [harvey-spectre](../data/agents/harvey-spectre.yaml) | 1 | opinion / reported | [harvey-spectre-source-1](../archive/sources/harvey-spectre-source-1/content.md), 88 |
| [harvey-spectre](../data/agents/harvey-spectre.yaml) | 2 | opinion / reported | [harvey-spectre-source-2](../archive/sources/harvey-spectre-source-2/content.md), 115 |
| [linear-agent](../data/agents/linear-agent.yaml) | 0 | fact / reported | [linear-agent-source-2](../archive/sources/linear-agent-source-2/content.md), 28-38,60 |
| [linear-agent](../data/agents/linear-agent.yaml) | 1 | opinion / reported | [linear-agent-source-2](../archive/sources/linear-agent-source-2/content.md), 134 |
| [linear-agent](../data/agents/linear-agent.yaml) | 2 | opinion / reported | [linear-agent-source-2](../archive/sources/linear-agent-source-2/content.md), 98 |
| [linear-agent](../data/agents/linear-agent.yaml) | 3 | opinion / reported | [linear-agent-source-2](../archive/sources/linear-agent-source-2/content.md), 60 |
| [linear-agent](../data/agents/linear-agent.yaml) | 4 | fact / reported | [linear-agent-source-2](../archive/sources/linear-agent-source-2/content.md), 70,102 |
| [monday-sphera-atlas-morphex](../data/agents/monday-sphera-atlas-morphex.yaml) | 0 | opinion / reported | [monday-sphera-atlas-morphex-source-1](../archive/sources/monday-sphera-atlas-morphex-source-1/content.md), 114-116,188 |
| [monday-sphera-atlas-morphex](../data/agents/monday-sphera-atlas-morphex.yaml) | 1 | fact / reported | [monday-sphera-atlas-morphex-source-1](../archive/sources/monday-sphera-atlas-morphex-source-1/content.md), 118-120 |
| [monday-sphera-atlas-morphex](../data/agents/monday-sphera-atlas-morphex.yaml) | 2 | fact / reported | [monday-sphera-atlas-morphex-source-1](../archive/sources/monday-sphera-atlas-morphex-source-1/content.md), 122-124 |
| [monday-sphera-atlas-morphex](../data/agents/monday-sphera-atlas-morphex.yaml) | 3 | fact / reported | [monday-sphera-atlas-morphex-source-1](../archive/sources/monday-sphera-atlas-morphex-source-1/content.md), 150 |
| [monday-sphera-atlas-morphex](../data/agents/monday-sphera-atlas-morphex.yaml) | 4 | fact / reported | [monday-sphera-atlas-morphex-source-1](../archive/sources/monday-sphera-atlas-morphex-source-1/content.md), 116,128-130 |
| [openai-sevbot](../data/agents/openai-sevbot.yaml) | 0 | fact / reported | [openai-sevbot-article](../archive/sources/openai-sevbot-article/content.md), 195 |
| [openai-software-factory](../data/agents/openai-software-factory.yaml) | 0 | opinion / reported | [openai-factory-article](../archive/sources/openai-factory-article/content.md), 52-56 |
| [openai-software-factory](../data/agents/openai-software-factory.yaml) | 1 | opinion / reported | [openai-factory-article](../archive/sources/openai-factory-article/content.md), 64-66 |
| [posthog-stamphog](../data/agents/posthog-stamphog.yaml) | 0 | fact / reported | [posthog-stamphog-source-3](../archive/sources/posthog-stamphog-source-3/content.md), 119-125 |
| [posthog-stamphog](../data/agents/posthog-stamphog.yaml) | 1 | fact / reported | [posthog-stamphog-source-3](../archive/sources/posthog-stamphog-source-3/content.md), 202-214 |
| [posthog-stamphog](../data/agents/posthog-stamphog.yaml) | 2 | fact / reported | [posthog-stamphog-source-3](../archive/sources/posthog-stamphog-source-3/content.md), 19 |
| [ramp-inspect](../data/agents/ramp-inspect.yaml) | 0 | opinion / reported | [ramp-inspect-source-1](../archive/sources/ramp-inspect-source-1/content.md), 26 |
| [ramp-inspect](../data/agents/ramp-inspect.yaml) | 1 | opinion / reported | [ramp-inspect-source-1](../archive/sources/ramp-inspect-source-1/content.md), 24,104 |
| [ramp-inspect](../data/agents/ramp-inspect.yaml) | 2 | opinion / reported | [ramp-inspect-source-1](../archive/sources/ramp-inspect-source-1/content.md), 16-22 |
| [ramp-inspect](../data/agents/ramp-inspect.yaml) | 3 | fact / reported | [ramp-inspect-source-1](../archive/sources/ramp-inspect-source-1/content.md), 36-43,69-72 |
| [ramp-inspect](../data/agents/ramp-inspect.yaml) | 4 | fact / reported | [ramp-inspect-source-5](../archive/sources/ramp-inspect-source-5/content.md), 58-66,82-90 |
| [replit-manager-agent](../data/agents/replit-manager-agent.yaml) | 0 | fact / reported | [replit-manager-agent-source-1](../archive/sources/replit-manager-agent-source-1/content.md), 50-62,78 |
| [replit-manager-agent](../data/agents/replit-manager-agent.yaml) | 1 | inference / catalog-judgment | [replit-manager-agent-source-1](../archive/sources/replit-manager-agent-source-1/content.md), 10,50-62 |
| [salesforce-slackbot](../data/agents/salesforce-slackbot.yaml) | 0 | fact / reported | [salesforce-slackbot-source-1](../archive/sources/salesforce-slackbot-source-1/content.md), 88-90,104-108 |
| [salesforce-slackbot](../data/agents/salesforce-slackbot.yaml) | 1 | fact / reported | [salesforce-slackbot-source-1](../archive/sources/salesforce-slackbot-source-1/content.md), 36,72 |
| [sentry-junior](../data/agents/sentry-junior.yaml) | 0 | opinion / reported | [sentry-junior-source-1](../archive/sources/sentry-junior-source-1/content.md), 28-32 |
| [sentry-junior](../data/agents/sentry-junior.yaml) | 1 | fact / reported | [sentry-junior-source-1](../archive/sources/sentry-junior-source-1/content.md), 247-257 |
| [sentry-junior](../data/agents/sentry-junior.yaml) | 2 | fact / reported | [sentry-junior-source-1](../archive/sources/sentry-junior-source-1/content.md), 136 |
| [sentry-junior](../data/agents/sentry-junior.yaml) | 3 | fact / reported | [sentry-junior-source-1](../archive/sources/sentry-junior-source-1/content.md), 311-337 |
| [sentry-junior](../data/agents/sentry-junior.yaml) | 4 | fact / reported | [sentry-junior-source-1](../archive/sources/sentry-junior-source-1/content.md), 212-216 |
| [shopify-internal-agents](../data/agents/shopify-internal-agents.yaml) | 0 | opinion / reported | [shopify-internal-agents-source-1](../archive/sources/shopify-internal-agents-source-1/content.md), 24-25,38-47 |
| [shopify-internal-agents](../data/agents/shopify-internal-agents.yaml) | 1 | fact / reported | [shopify-internal-agents-source-1](../archive/sources/shopify-internal-agents-source-1/content.md), 57,71,79,87 |
| [shopify-internal-agents](../data/agents/shopify-internal-agents.yaml) | 2 | fact / reported | [shopify-internal-agents-source-1](../archive/sources/shopify-internal-agents-source-1/content.md), 116-134 |
| [shopify-internal-agents](../data/agents/shopify-internal-agents.yaml) | 3 | fact / reported | [shopify-internal-agents-source-1](../archive/sources/shopify-internal-agents-source-1/content.md), 142 |
| [sierra-pinecone](../data/agents/sierra-pinecone.yaml) | 0 | fact / reported | [sierra-pinecone-source-1](../archive/sources/sierra-pinecone-source-1/content.md), 56-60 |
| [sierra-pinecone](../data/agents/sierra-pinecone.yaml) | 1 | fact / reported | [sierra-pinecone-source-1](../archive/sources/sierra-pinecone-source-1/content.md), 120-124 |
| [sierra-pinecone](../data/agents/sierra-pinecone.yaml) | 2 | fact / reported | [sierra-pinecone-source-2](../archive/sources/sierra-pinecone-source-2/content.md), 52-66,93 |
| [sierra-pinecone](../data/agents/sierra-pinecone.yaml) | 3 | inference / catalog-judgment | [sierra-pinecone-source-1](../archive/sources/sierra-pinecone-source-1/content.md), 118,136-141 |
| [slack-context-system](../data/agents/slack-context-system.yaml) | 0 | fact / reported | [slack-context-system-source-1](../archive/sources/slack-context-system-source-1/content.md), 36-42,272 |
| [slack-context-system](../data/agents/slack-context-system.yaml) | 1 | fact / reported | [slack-context-system-source-1](../archive/sources/slack-context-system-source-1/content.md), 119-142,172-176 |
| [slack-context-system](../data/agents/slack-context-system.yaml) | 2 | inference / catalog-judgment | [slack-context-system-source-1](../archive/sources/slack-context-system-source-1/content.md), 272-284 |
| [spotify-honk-xirp](../data/agents/spotify-honk-xirp.yaml) | 0 | fact / reported | [spotify-honk-xirp-source-1](../archive/sources/spotify-honk-xirp-source-1/content.md), 64 |
| [spotify-honk-xirp](../data/agents/spotify-honk-xirp.yaml) | 1 | fact / reported | [spotify-honk-xirp-source-2](../archive/sources/spotify-honk-xirp-source-2/content.md), 56 |
| [spotify-honk-xirp](../data/agents/spotify-honk-xirp.yaml) | 2 | fact / reported | [spotify-honk-xirp-source-2](../archive/sources/spotify-honk-xirp-source-2/content.md), 88-104 |
| [spotify-honk-xirp](../data/agents/spotify-honk-xirp.yaml) | 3 | fact / reported | [spotify-honk-xirp-source-3](../archive/sources/spotify-honk-xirp-source-3/content.md), 12 |
| [stripe-minions](../data/agents/stripe-minions.yaml) | 0 | fact / reported | [stripe-minions-source-1](../archive/sources/stripe-minions-source-1/content.md), 14-18,50 |
| [stripe-minions](../data/agents/stripe-minions.yaml) | 1 | fact / reported | [stripe-minions-source-2](../archive/sources/stripe-minions-source-2/content.md), 24-32 |
| [strongdm-software-factory](../data/agents/strongdm-software-factory.yaml) | 0 | opinion / reported | [strongdm-factory-techniques](../archive/sources/strongdm-factory-techniques/content.md), 45 |
| [strongdm-software-factory](../data/agents/strongdm-software-factory.yaml) | 1 | fact / reported | [strongdm-factory-principles](../archive/sources/strongdm-factory-principles/content.md), 12-34 |
| [strongdm-software-factory](../data/agents/strongdm-software-factory.yaml) | 2 | opinion / reported | [strongdm-factory-overview](../archive/sources/strongdm-factory-overview/content.md), 23 |
| [uber-ureview](../data/agents/uber-ureview.yaml) | 0 | opinion / reported | [uber-ureview-source-1](../archive/sources/uber-ureview-source-1/content.md), 128-140 |
| [uber-ureview](../data/agents/uber-ureview.yaml) | 1 | fact / reported | [uber-ureview-source-1](../archive/sources/uber-ureview-source-1/content.md), 132-138 |
| [uber-ureview](../data/agents/uber-ureview.yaml) | 2 | fact / reported | [uber-ureview-source-1](../archive/sources/uber-ureview-source-1/content.md), 146-148 |
| [workos-project-horizon](../data/agents/workos-project-horizon.yaml) | 0 | fact / reported | [workos-project-horizon-source-1](../archive/sources/workos-project-horizon-source-1/content.md), 68-94 |
| [workos-project-horizon](../data/agents/workos-project-horizon.yaml) | 1 | fact / reported | [workos-project-horizon-source-1](../archive/sources/workos-project-horizon-source-1/content.md), 110-120 |
| [workos-project-horizon](../data/agents/workos-project-horizon.yaml) | 2 | inference / catalog-judgment | [workos-project-horizon-source-1](../archive/sources/workos-project-horizon-source-1/content.md), 56,153-157; [workos-project-horizon-source-2](../archive/sources/workos-project-horizon-source-2/content.md), 50 |
| [workos-project-horizon](../data/agents/workos-project-horizon.yaml) | 3 | fact / reported | [workos-project-horizon-source-1](../archive/sources/workos-project-horizon-source-1/content.md), 124-149 |
| [workos-project-horizon](../data/agents/workos-project-horizon.yaml) | 4 | fact / reported | [workos-project-horizon-source-1](../archive/sources/workos-project-horizon-source-1/content.md), 104 |
| [ycombinator-agent-infra](../data/agents/ycombinator-agent-infra.yaml) | 0 | fact / reported | [ycombinator-agent-infra-source-1](../archive/sources/ycombinator-agent-infra-source-1/content.md), 154 |
| [ycombinator-agent-infra](../data/agents/ycombinator-agent-infra.yaml) | 1 | fact / reported | [ycombinator-agent-infra-source-1](../archive/sources/ycombinator-agent-infra-source-1/content.md), 120 |
| [zup-codegen](../data/agents/zup-codegen.yaml) | 0 | opinion / reported | [zup-codegen-source-1](../archive/sources/zup-codegen-source-1/content.md), 18 |
| [zup-codegen](../data/agents/zup-codegen.yaml) | 1 | opinion / reported | [zup-codegen-source-1](../archive/sources/zup-codegen-source-1/content.md), 18 |
