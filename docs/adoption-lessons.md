# Adoption lessons: how internal agents actually get used

Architecture is half the story; the other half is how these systems get adopted by real
engineering and operations organizations. These are the non-technical (or
not-only-technical) lessons that repeat across the catalog. Each is grounded in a specific
company's experience — follow the links to [the catalog](landscape.md).

---

## 1. Start narrow, measurable, and easy to evaluate

Don't launch a general-purpose autonomous agent on day one. Pick one frequent, measurable,
low-stakes workflow, prove it, and expand.

- **DoorDash (Flux)** began with *automated code review* — frequent, easy to evaluate, easy
  to trust — before expanding to CI triage, on-call, maintenance, and ticket-driven dev.
- **Linear** starts by *asking for suggestions*, observes, adds guidance, and automates only
  once a workflow is proven reliable.
- **Brex** maps a workflow to the discrete steps a human takes today, then automates them one
  at a time.

> Pick the workflow where a win is undeniable and a failure is cheap.

## 2. Make the work visible — public beats private

Adoption is a social phenomenon. Work that happens in public channels spreads; work in
private DMs doesn't.

- **Shopify (River)** is *public-by-default*: it operates only in public Slack channels,
  never DMs, so every session is observable and good patterns propagate.
- **Ramp** and **DoorDash** both report that public Slack threads drove adoption, while
  private per-run channels failed to build team habits.
- **Sentry** mirrors this in its privacy stance: public-channel conversations are fully
  captured; private ones are redacted — visibility is a feature, not a bug.

> If only the person at the keyboard can see the agent work, you've capped how much the org
> learns. (Shopify: "local agents have a ceiling.")

## 3. Enablement beats infrastructure

Shipping the platform isn't enough; you have to teach people to use it. The most adopted
systems invest in enablement, not just features.

- **DoorDash** runs workshops and hackathons to turn repeated operational work into reusable
  playbooks — the playbooks don't write themselves.
- **Brex** built a *prompt + eval studio* so non-technical operations staff can design, test,
  and deploy agents without engineering involvement.
- **monday.com** gave agents *identities, managers, scopes, and performance scores* — treating
  adoption as an org-design problem, not just a tooling one.

## 4. Meet people where they already are

Don't ask anyone to open a new tool. The agent goes to Slack, GitHub, Linear, Jira — wherever
the work already lives.

- **Block (`@builderbot`)**, **Browserbase (`bb`)**, **Sentry (Junior)**, **Shopify (River)**,
  **monday.com**, **Brex (`/c1`)**, and **WorkOS** all center on Slack.
- **Linear** keeps the agent adjacent to the source of work (Intercom, Slack, Linear) and
  *closes the loop* by auto-notifying the customer when a request ships.

> Distribution is a feature of the agent, not an afterthought.

## 5. Own the primitives that carry your value — rent the rest

Several teams argue that building your own harness/sandbox pays off specifically because it
only has to work on *your* code, which lets you build something more capable than off-the-shelf.

- **Ramp:** "it only has to work on your code, which lets you build something more powerful
  than off-the-shelf."
- **WorkOS:** "you need purpose-built agent infrastructure — a runtime you could control
  end-to-end."
- **Y Combinator** built its harnesses from the ground up rather than bolting onto a hosted
  agent.

The flip side is **modularity**: build so you can swap any layer (Shopify, Spotify, monday.com
all optimize for this) — own the layer that carries your differentiation, keep the rest
replaceable.

## 6. Make the system self-improving

The best platforms get better simply by being used.

- **WorkOS (Horizon):** "every run ships work and produces the next set of fixes — better
  verification, clearer guidelines, tighter paved paths." The agent surfaces the platform's
  own brittleness (a flaky test, an unclear convention) as the work it does.
- **monday.com's** PR Guardrails turn every review into a tightening of the standard.
- **Linear:** "AI mistakes are useful — they surface failure modes to engineers."

## 7. Don't mandate; let the product do the talking

- **Ramp** explicitly avoids mandates and relies on virality loops in public spaces.
- **Shopify** lets River spread channel by channel (5,170 channels, 7,000+ people in 30 days)
  rather than imposing it.

> Forcing adoption produces compliance, not enthusiasm. Make the agent obviously useful and
> let it spread.

## 8. Centralize the control plane early

It's tempting to let each team connect directly to a model provider. Several teams warn this
becomes a trap.

- **Cloudflare** centralizes through an AI Gateway + MCP Server Portal from the start, because
  direct-to-provider blocks per-user attribution, model cataloging, cost control, and policy
  later — exactly the things you'll want once usage grows.
- **Browserbase**, **Sentry**, and **WorkOS** all put a proxy/gateway between the agent and
  the world for the same reason: one place to enforce scope, log, and inject credentials.

## 9. Reuse the org's existing machinery

Agents don't need a parallel universe of auth, identity, CI, and deploy. The teams that moved
fastest reused what already existed.

- **monday.com:** the existing auth/identity/deploy pipeline applies to agents — reuse it;
  agents get real Slack/GitHub/monday accounts and the same RBAC as humans.
- **Dropbox (Nova):** integrate with existing engineering infrastructure rather than building
  separate AI-specific workflows; agents run inside the existing Bazel/remote-exec paths.
- **Brex:** legal/data approvals should follow *data-handling characteristics*, not the tool
  name — don't re-litigate compliance for each new agent.

## 10. Treat internal tooling with external rigor

- **Brex:** "treat internal ops with external rigor — build internal platforms to product
  quality." A 25-person team runs the platform like a product, because internal users deserve
  the same reliability external customers do.
- **monday.com** and **Shopify** both invest in evals, guardrails, and reliability as if the
  agent were a shipped product.

---

### The short version

Start narrow. Work in public. Teach people to use it. Meet them in Slack. Own what
differentiates you, rent the rest. Let usage improve the platform. Don't mandate. Centralize
the control plane early. Reuse your existing org machinery. Build it like a product.
