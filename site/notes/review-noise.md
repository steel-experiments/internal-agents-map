Source: https://internal-agents.com/notes/review-noise.html

[← Notes](https://internal-agents.com/notes.html)

02 / Human attention

# More comments can mean more work

A review agent also creates work for its reader.

11 September 2026 · 2 min read

## What the teams report

Uber found that a single prompt produced false alarms and valid comments with little value. Its uReview system checks confidence and removes duplicate comments. It also suppresses categories that engineers rarely use. [[1]](https://internal-agents.com/notes/review-noise.html#source-uber)

> “Precision Is More Valuable than Volume”

A section title in Uber’s uReview report. [[1]](https://internal-agents.com/notes/review-noise.html#source-uber)

HubSpot made its reviewer faster, but review quality remained a problem. It added a judge agent to check comments before publication. [[2]](https://internal-agents.com/notes/review-noise.html#source-hubspot)

01 **Find** Possible issues

02 **Filter** Check the evidence

03 **Review** Human attention

Our simplified illustration. Both teams check comments before publication; their checks differ.

Our observation

## Measure the work after the output

Comment count shows how much an agent writes. It does not show how much useful work the team completes.

A useful evaluation can track accepted findings, review time, and missed defects. A filter can reduce noise and still remove a real issue.

A model judge can also make mistakes. The reports do not establish that an extra agent always improves a review.

**A question for your build** Does each additional comment save more work than it creates?

## Sources

1. [Uber: uReview](https://www.uber.com/us/en/blog/ureview/) Quality filters, duplicate removal, and feedback from engineers.
2. [HubSpot: Sidekick code review](https://product.hubspot.com/blog/automated-code-review-the-6-month-evolution) The change to Aviator and the judge agent.

[Uber in the catalog](https://internal-agents.com/index.html#uber-ureview) [HubSpot in the catalog](https://internal-agents.com/index.html#hubspot-sidekick)

[All notes](https://internal-agents.com/notes.html) [Next: Separate the search from the check →](https://internal-agents.com/notes/split-the-work.html)
