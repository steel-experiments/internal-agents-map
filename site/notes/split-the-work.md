Source: https://internal-agents.com/notes/split-the-work.html

[← Notes](https://internal-agents.com/notes.html)

03 / Agent roles

# Separate the search from the check

The division of work can matter more than the number of agents.

11 September 2026 · 2 min read

## What DoorDash reports

DoorDash first used specialist reviewers. They found local errors but missed problems across system boundaries.

The next design used two reviewers with broader context. Each had too much to check, and some findings were lost.

The third design added a scout. It identifies possible issues. Two reviewers then investigate those issues. [[1]](https://internal-agents.com/notes/split-the-work.html#source-doordash)

> “The lead scout's job isn't to verify anything.”

DoorDash, on the scout’s role. [[1]](https://internal-agents.com/notes/split-the-work.html#source-doordash)

Version 1 **Specialists**

Narrow context

Version 2 **Broad reviewers**

Too much to check

Version 3 **Scout → Reviewers**

Find leads, then verify

Our illustration of the three reported designs. The sequence does not represent measured performance.

Our observation

## Each role needs a clear result

A possible issue and a verified issue are different results. Separate roles can make that difference explicit.

This design may help when a broad search precedes a detailed check. It may add unnecessary work when one agent can complete both steps.

This is one team’s report. It does not prove that three agents are better than two.

**A question for your build** What must each agent produce before the next agent can use its result?

## Source

1. [DoorDash: How we built an AI code reviewer](https://careersatdoordash.com/blog/doordash-built-an-ai-code-reviewer-engineers-actually-listen-to/) The “How we got here” section describes all three designs.

[DoorDash in the catalog](https://internal-agents.com/index.html#doordash-code-review)

[All notes](https://internal-agents.com/notes.html) [Next: The worker can stop. The work can continue. →](https://internal-agents.com/notes/work-can-continue.html)
