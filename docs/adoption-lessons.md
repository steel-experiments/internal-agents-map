# Adoption lessons: how internal agents actually get used

Architecture is half the story; the other half is how these systems get adopted by real
engineering and operations organizations. These are the non-technical (or
not-only-technical) lessons that repeat across the catalog. Each is grounded in a specific
company's experience. Follow the links to [the catalog](landscape.md).

---

## 1. Start narrow, measurable, and easy to evaluate

Don't launch a general-purpose autonomous agent on day one. Pick one frequent, measurable,
low-stakes workflow, prove it, and expand.

- **DoorDash** began with automated code review (10,000+ PRs/week across 56 repos) and
  deterministic reporting/SQL before pursuing deep agents.
- **Spotify** began with migrations; **Stripe** and **Ramp** with code; **Flex** with payment
  investigation.
- **Linear** starts by asking for suggestions, observes, and automates only once proven.

> Start where correctness is observable: coding, migrations, investigation, review, and
> reporting produce artifacts you can *check* (tests pass, a diff exists, SQL validates, a
> hypothesis matches telemetry).

## 2. Make the work visible: public beats private

Adoption is a social phenomenon. Work in public channels spreads; work in private DMs doesn't.

- **Shopify (River)** is public-by-default, public channels only, so every session is
  observable and good patterns propagate.
- **Ramp** and **DoorDash** report public Slack threads drove adoption; private per-run
  channels didn't.
- **Sentry** mirrors this: public-channel conversations are fully captured; private ones
  redacted. Visibility is a feature.

> If only the person at the keyboard can see the agent work, you've capped how much the org
> learns.

## 3. Enablement beats infrastructure

Shipping the platform isn't enough; you have to teach people to use it.

- **DoorDash** runs workshops and hackathons to turn operational work into reusable playbooks.
- **Brex** built a prompt + eval studio so non-technical ops staff design and deploy agents.
- **monday.com** gave agents identities, managers, scopes, and performance scores, treating
  adoption as an org-design problem.

## 4. Meet people where they already are

Don't ask anyone to open a new tool. The agent goes to Slack, GitHub, Linear, Jira.

- **Block, Browserbase, Sentry, Shopify, monday.com, Brex, WorkOS, Coinbase, Sierra, Stripe,
  Flex, Replit** all center on Slack.
- **Coinbase** is explicit: normal behavior stays "ask a question in Slack"; the change is
  that an agent, not an interrupted colleague, answers or converts it to work.
- **Linear** closes the loop by auto-notifying the customer when a request ships.

## 5. Own the primitives that carry your value: rent the rest

Several teams argue building your own harness/sandbox pays off because it only has to work on
*your* code.

- **Ramp:** "it only has to work on your code, which lets you build something more powerful
  than off-the-shelf."
- **WorkOS:** "you need purpose-built agent infrastructure — a runtime you could control
  end-to-end."
- **Y Combinator** built its harnesses from the ground up rather than bolting onto a hosted
  agent.

The flip side is **modularity**: own the layer that differentiates you, keep the rest
replaceable (Shopify, Sierra, WorkOS, Coinbase all optimize for this).

## 6. Make the system self-improving

The best platforms get better simply by being used.

- **WorkOS (Horizon):** every run ships work and produces the next set of fixes, surfacing the
  platform's own brittleness (a flaky test, an unclear convention).
- **monday.com's** PR Guardrails tighten the standard with every review.
- **Linear:** "AI mistakes are useful — they surface failure modes to engineers."

## 7. Don't mandate; let the product do the talking

- **Ramp** avoids mandates and relies on virality loops in public spaces.
- **Shopify** lets River spread channel by channel (5,170 channels, 7,000+ people in 30 days).

> Forcing adoption produces compliance, not enthusiasm.

## 8. Centralize the control plane early

Direct-to-model-provider looks simpler but becomes a trap.

- **Cloudflare** centralizes through an AI Gateway + MCP Server Portal from the start.
- **Browserbase, Sentry, WorkOS, Sierra** all put a proxy/gateway between the agent and the
  world: one place to enforce scope, log, and inject credentials.

## 9. Reuse the org's existing machinery

Agents don't need a parallel universe of auth, identity, CI, and deploy.

- **monday.com:** existing auth/identity/deploy pipeline applies to agents; real accounts,
  same RBAC as humans.
- **Dropbox (Nova):** integrate existing infra; agents run inside existing Bazel/remote-exec.
- **Brex:** approvals follow data-handling characteristics, not the tool name.
- **Salesforce:** the agent inherits the employee's existing permissions by construction.

## 10. Treat internal tooling with external rigor

- **Brex:** "treat internal ops with external rigor — build internal platforms to product
  quality."
- **monday.com** and **Shopify** invest in evals, guardrails, and reliability as if the agent
  were a shipped product.

## 11. Track outcomes, not activity

The most repeated measurement warning in the catalog.

- **Sierra** is explicit: session counts and tool calls are evidence of *usage*, not *value*.
- **DoorDash** measures whether engineers actually act on a review finding (60.2% action rate
  on high/critical findings), not comment volume.
- **Ramp** and **Stripe** measure production-PR contribution; **Spotify** tracked migration
  time savings; **Replit** tracked that ~3× code output came *without* degradation in
  review/revert/incident metrics.

> Useful KPIs: cycle time, accepted output, human review time, escaped defects, incident
> resolution, time-to-first-response, cost per successfully completed task, percentage of runs
> that finish without human rescue, *not* total prompts.

## 12. The bottleneck moves: plan for it

Agents don't simply "replace coding time"; they increase the premium on judgment.

- **Spotify** reports increased coding velocity created more review pressure.
- **Harvey** says implementation speed is shifting bottlenecks toward review, prioritization,
  and coordination.

> As implementation cheapens, invest in **requirements, taste, evaluation, review,
> authorization design, and prioritization**, the work the agent can't do for you.

---

### The short version

Start narrow. Work in public. Teach people to use it. Meet them in Slack. Own what
differentiates you, rent the rest. Let usage improve the platform. Don't mandate. Centralize
the control plane early. Reuse your existing org machinery. Build it like a product. Track
outcomes, not activity. Plan for the bottleneck to move.
