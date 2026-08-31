> Archived source snapshot  
> Source ID: `domu-clementino-source-1`  
> Original URL: <https://domu.ai/blog/why-we-split-our-internal-agent-in-two>  
> Final URL: <https://domu.ai/blog/why-we-split-our-internal-agent-in-two>  
> Title: Why we split our internal agent in two — Domu  
> Captured at: `2026-08-31T17:41:45Z`

---

[

![](https://framerusercontent.com/images/hjJfkTqxXdwQyok2h99MD4bE3lc.svg?width=709&height=156)

](https://domu.ai/)

## Why we split Clementino in two

A few months after launching our first AI colleague in Slack, we hit the limits of one interface. Here's how we turned Clementino into a portable toolkit, and gave it a second surface on the desktop*.*

Months ago I wrote about Clementino, our first AI colleague. A single orchestrator running on Claude, plugged into our CRM, our data warehouse, our knowledge base, and a dozen other systems, sitting inside Slack and handling questions for everyone from sales to finance to engineering. That post ended with a teaser: *we're building it live, and in the next post, I'll share more learnings down the road.*

This is that post.

Adoption kept growing. The thread counts kept climbing. People started asking Clementino for things I never imagined when I built the first version. And as the requests got more ambitious, a pattern showed up that I should have probably seen sooner.

## The friction we didn't see coming

Clementino is amazing inside Slack. Ask it "who's stuck this week?" or "send the invoice for that account this month" and you get exactly what you needed in seconds. That use case (quick, conversational, visible to the team, ideally gated by approvals) is what Slack is built for, and it's what we built Clementino for.

But people started asking for things Slack is not built for.

"Build me a deck for tomorrow's client review." Painful. Slack is not a deck editor, and you end up with a wall of text and no way to iterate visually.

"Clean up this spreadsheet for me." Painful. You can't see the file, can't scroll the rows, can't compare before and after.

"Help me think through this proposal." Doable, but awkward. Long form reasoning in a Slack thread is a UX disaster. Things scroll off the screen, attachments stack, you lose your place.

It wasn't that Clementino *couldn't* do these things. The brain was capable. The surface was wrong. Slack is built for messages, not for files and exploration.

## The temptation: just build a web UI

The obvious move would have been to build our own desktop app or a web interface. That felt wrong for a few reasons.

First, we're not a chat UI company. Building a great chat experience is its own entire problem, and we already had one in Slack itself, where our team lives eight hours a day. Replicating it just to escape Slack's limits felt backwards.

Second, building a second interface meant either forking the agent (two brains, two memories, divergent capabilities forever) or routing a remote API to a custom UI we'd have to maintain ourselves. Both options were bad.

Third, and this is the one that actually decided it, we'd been watching Anthropic ship Claude Cowork, a desktop product that brings Claude to your files, apps, and folders. The UX work was already done, the team was already using it. The thing we needed wasn't a new interface. It was a way to plug Clementino's brain into one we didn't have to build.

## What we did instead: pull the brain out

The fix turned out to be a refactor, not a new product.

For the last few weeks, we'd been quietly separating Clementino into layers. The code tied to Slack (webhooks, message formatting, thread handling, approval buttons) lived in one place. Everything else (the tools, the skills, the memory system, the agent core) lived in another. We didn't do that intentionally at first. It just turned out to be the only way to keep adding capabilities without the codebase collapsing.

Once that separation was real, the split became possible. We took the portable half, which we now call the toolkit, and gave it a second home.

The toolkit is everything that has nothing to do with Slack.

**Tool modules.** Our CRM, our data warehouse, our issue tracker, our payments and expense systems, our document and spreadsheet tools, email, calendar, our internal knowledge base. About 35 in total, organized into skills.

**Skills and delegates.** Sales, Finance, Client Ops, Engineering, Recruitment, Knowledge. The same orchestration logic that picks which specialist to call.

**The memory system.** Four layers (conversation context, persistent facts, knowledge RAG, live system state), all stored in the same tables.

**The agent core.** The Anthropic SDK wrapper, model fallback, streaming.

Then two interfaces sit on top of it.

**Clementino in Slack**, unchanged from your team's perspective. Same channels, same @Domu mention, same approval buttons. Scheduled jobs still post at 5am, invoice approvals still show up in #finance.

**The toolkit as a plugin in Claude Cowork**, a desktop interface that opens next to your files. Same brain, same tools, same memory. Different surface.

## What changed in practice

The split is less about "two products" and more about "two workflows."

In Slack, I still use Clementino for everything that should be visible to the team or scheduled. The 5am sales standup. Invoice approvals before they go out. QA sampling. Huddle ingestion. Anything that needs the rest of the team to see "the agent did this, and someone signed off."

In Cowork, I use the toolkit for everything that's just me thinking with help. Preparing for a client review by pulling the right call data from our warehouse and the right notes from our document store, then drafting the slides, all in one place where I can see what's happening. Cleaning up a messy spreadsheet. Drafting a long email with an attachment. The kind of work where you want a window open next to the thing you're working on.

The unlock I didn't expect: shared memory across both surfaces. A fact the agent learns in a Cowork session in the afternoon is available to Clementino in #sales the next morning. If I tell the agent "this account wants quarterly billing now" while I'm building a deck on Tuesday, it remembers that when someone asks about that account's pricing on Thursday. The agent gets smarter regardless of which interface I happened to use.

## What I learned splitting it

A few things I wish I'd internalized earlier.

**The surface isn't the agent.** It's easy to conflate them when your first version only lives in one place. Once you separate them, you can move much faster. And you can put the agent in places you couldn't before.

**Memory is what makes the split safe.** Without a shared memory layer, splitting into two surfaces would have given us two agents that don't know each other. With it, we get one colleague who's just present in two places.

**Approval gates belong in the team's interface, not the individual's.** Anything that touches a customer (invoices, outbound emails, contract changes) runs through Slack approvals where the rest of the team can see them, regardless of which surface initiated the request. Trust requires visibility.

**Build the toolkit, not the agent.** This is the lesson I'd tell myself at the start of the whole project, if I were starting over. A toolkit is portable. An agent welded to its interface is not. The minute we had a toolkit version, our optionality went up dramatically. We could add a third or fourth surface tomorrow (a browser agent, a scheduled CLI, an internal API) without rebuilding integrations.

## What's next

Splitting the agent had a side effect we didn't plan for. The prompt size on every request dropped from about 37k tokens to around 9k. Same capabilities, roughly 73% smaller context. That's not the kind of thing that happens by accident, and it deserves its own post. I'll write that one next.

We're still building this live. Clementino in Slack and the toolkit in Cowork are running side by side now, and the team is moving between them more naturally than I expected. The next frontier is the third surface. Once we know what that is, we'll write about it too.
