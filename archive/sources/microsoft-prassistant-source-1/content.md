> Archived source snapshot  
> Source ID: `microsoft-prassistant-source-1`  
> Original URL: <https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/>  
> Final URL: <https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/>  
> Title: Enhancing Code Quality at Scale with AI-Powered Code Reviews - Engineering@Microsoft  
> Captured at: `2026-08-31T17:55:39Z`

---

At Microsoft, we are constantly looking for ways to improve developer productivity and code quality. One of our most impactful innovations in this space is **AI-powered code review assistant** — an AI tool that augments pull request (PR) reviews. This AI Assistant started as an internal experiment and now has scaled to support over 90% of PRs across the company impacting more than 600K pull requests per month. It helps our engineers catch issues faster, complete PRs sooner, and enforce consistent best practices – all within our standard development workflow. We built this capability in close collaboration with our Developer Division’s Data & AI team. The learning and experiences developed internally were incorporated into [GitHub’s AI-powered code review](https://docs.github.com/en/copilot/how-tos/agents/copilot-code-review/using-copilot-code-review) offering and now benefit external customers. This is an example of how first-party (1P) innovation has shaped third-party (3P) products—and how external usage continues to inform internal improvements.

### Solving the real problems in PR reviews with AI

Pull requests (PRs) are a critical part of the development workflow—but also there is some friction. Reviewers often spend time on low-value feedback like syntax issues or naming inconsistencies, while more meaningful concerns—like architectural decisions or security implications—can be overlooked or delayed. Authors, on the other hand, may struggle to provide enough context, especially when PRs are large or span multiple files. There is also the challenge of scale: with thousands of developers and repositories, ensuring every PR gets a timely and thorough review is hard. We have seen scenarios where PRs waited days and even weeks before getting merged, or where important feedback was missed. These pain points motivated us to try AI assistance in the review process. The goal was to let AI handle the repetitive or easily overlooked aspects of reviews, freeing human reviewers to focus on higher-level concerns.

Our solution was to integrate an AI code reviewer into the existing PR workflow. Whenever a pull request is created, the AI assistant automatically kicks in as one of the reviewers. Here’s what it does:

- **Automated Checks and Comments:** AI reviews the code changes and leaves comments just like a human reviewer would. It flags a range of issues – from simple things like style inconsistencies and minor bugs, to more subtle concerns like a potential null reference or an inefficient algorithm. For example, if a developer introduces a method that does not properly handle an error condition, AI might comment on that specific diff line with a warning and an explanation. These comments show up in the PR discussion thread, so the author and other reviewers see them and can act (just as if a colleague had made the remarks). Each suggestion has a category associated with it e.g. exceptional handling, null check, sensitive data, which helps in understanding the associated impact. By catching such issues early, the AI reduces the review overhead for human peers and ensures that obvious problems are not missed
- **Suggested Improvements:** Alongside reviews, the assistant even suggests specific code improvements. If it identifies a bug or a suboptimal code pattern, it proposes a corrected code snippet or an alternative implementation for the author to implement. While it is powerful, it is also designed with safeguards in mind. When AI suggests code changes, it does not commit them directly. The author remains in control—reviewing, editing, and deciding whether to accept the suggestion by explicitly clicking ‘apply change’ option. All changes are attributed to the commit history, preserving accountability and transparency.

[![Screenshot of a pull request with suggestions from the AI code reviewer](https://devblogs.microsoft.com/engineering-at-microsoft/wp-content/uploads/sites/72/2025/07/word-image-1134-1.png)](https://devblogs.microsoft.com/engineering-at-microsoft/wp-content/uploads/sites/72/2025/07/word-image-1134-1.png)

- **PR Summary Generation:** AI also generates a summary of the PR – essentially an AI-written description of what the code change is doing. This addresses a common issue of several PRs not having a well written description. The AI looks through the diffs and tries to explain the intent of the change and highlights key changes. Reviewers have found this extremely useful: it helps us to understand the big picture without having to manually decipher every file.

[![Screenshot of a pull request AI generated summary of the changes](https://devblogs.microsoft.com/engineering-at-microsoft/wp-content/uploads/sites/72/2025/07/a-screenshot-of-a-computer-ai-generated-content-m.png)](https://devblogs.microsoft.com/engineering-at-microsoft/wp-content/uploads/sites/72/2025/07/a-screenshot-of-a-computer-ai-generated-content-m.png)

- **Interactive Q&A (“Ask the AI”):** Reviewers can also engage the assistant in a conversation within the PR discussion. If something in the code is unclear, a reviewer can ask the AI questions about the code or request clarification. For example, “Why is this parameter needed here?” or “What’s the impact of this change on module X?” The AI can analyze the code and provide answers, acting like a knowledgeable co-reviewer available on demand.

What makes using AI reviewer effective is how naturally it fits into existing workflows. It is treated just like any other reviewer—no new UI to learn, no extra tools to install. Developers can engage with it conversationally, right within the PR thread, making it feel like a seamless extension of the team. It can even be configured to automatically engage the moment a PR is created, acting as the first reviewer—always present, always ready. This frictionless integration has been key to its high adoption and impact.

### Impact on quality and velocity

The adoption and impact of AI reviewer have been significant. Some benefits are:

- **Faster Review Cycles:** With the AI doing an initial pass on each PR, teams have noticed that the overall time to complete a pull request has gone down. Per early experiments and data science studies, 5000 repositories onboarded to AI code reviewer observed 10 – 20% median PR completion time improvements. AI often catches issues and suggests improvements within minutes of the PR’s creation, which means authors can address those early, without waiting for a human reviewer’s schedule. It also means fewer back-and-forth cycles for minor fixes, so PRs can get approved and merged more quickly.
- **Improved Code Quality:** It helps raise the baseline quality of code reviews by providing guidance around coding standards and best practices across the board. In several cases, AI flagged bugs that might have been overlooked – for example, spotting a missing null-check or an incorrectly ordered API call that could have caused a runtime error. By catching such problems before the code is merged, we prevent potential incidents downstream.
- **Developer Learning:** It can act like a mentor who reviews every line of the code and explains possible improvements. Especially for new hires it can serve as a useful guide, accelerating onboarding and learning of best practices.

### Customization: tailoring review for your team

One of the powerful features offered is its configurability and extensibility. Teams can customize the experience to provide repository specific guidelines. Also, teams can define custom review prompts that are specific to their scenarios. Teams across the company are leveraging these customizations to perform specialized reviews, like identifying regressions based on historical crash patterns or ensuring flight and change gates are in place.

[![Screenshot of pull request code review with customized review](https://devblogs.microsoft.com/engineering-at-microsoft/wp-content/uploads/sites/72/2025/07/word-image-1134-3.png)](https://devblogs.microsoft.com/engineering-at-microsoft/wp-content/uploads/sites/72/2025/07/word-image-1134-3.png)

### Co-evolution of 1P & 3P solutions

A natural question is: How does Microsoft’s internal AI review benefit the broader developer community? Being the first adopters and internal testers of AI-powered code reviews gave us an early exposure, allowing us to rapidly iterate on review quality, usability, and developer trust—based on direct feedback from our engineering teams. The insights, patterns, and success we saw internally not only validated the value of AI-assisted reviews but also helped define the experiences like inline suggestions, and human in the loop review flows. This feedback loop became a significant contributor in GitHub’s launch of [Copilot for Pull Request Reviews](https://github.blog/changelog/2025-04-04-copilot-code-review-now-generally-available/?utm_source=chatgpt.com), which reached general availability in April 2025, bringing these innovations to millions of developers worldwide.

At the same time, learnings gathered using GitHub Copilot for Pull Request Reviews are being incorporated back into Microsoft’s internal development process. This co-evolution ensures that Microsoft’s developers and the broader developer community both benefit from AI advancements in code review.

### Final thoughts

AI powered code reviews are a catalyst for transforming how we approach code reviews at scale. By combining the power of large language models with the rigor of human workflows, it empowers developers to write better code faster. Reviewers gain deeper insights, authors get actionable feedback, and teams move with greater confidence.

And this is just the beginning. With ongoing investments in customization and quality, AI is poised to redefine the developer experience across Microsoft. Looking ahead, we are focused on deepening its contextual awareness—bringing in repository-specific guidance, referencing past PRs, and learning from human review patterns to deliver insights that align more closely with team norms and expectations. This will enable reviewers to focus entirely on high-value feedback while AI handles major routine checks, streamlining the review process and elevating both speed and consistency. That’s a future we are excited about – one where shipping high-quality code is easier and faster, supported by AI every step of the way.

Whether you are at Microsoft or contributing from the broader dev community, AI can help code smarter. [Try GitHub Copilot’s code review](https://docs.github.com/en/copilot/how-tos/agents/copilot-code-review/using-copilot-code-review) and bring AI into your workflow.
