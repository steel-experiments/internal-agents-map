# Write confidence reasons for accepted claims (write.v1)

You receive accepted claims of one catalog candidate. Each claim already has
its verbatim quote and its verified locator. Write exactly one confidence
reason per claim that lacks one.

A confidence reason names the evidence and any unsupported step. It states why
the claim's confidence level is what it is: what the source establishes, what
it does not, and any qualification the reader needs. Do not turn a company's
preference into general advice, do not reuse one reason across unrelated
claims, and do not introduce numbers, dates, or names that are not in the
claim or its quote.

Return JSON: `{"reasons": {"<claim id>": "<one or two sentences>"}}`. Use every
claim ID you were given exactly once; add no others.
