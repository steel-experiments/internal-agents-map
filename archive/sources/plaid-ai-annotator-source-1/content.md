> Archived source snapshot  
> Source ID: `plaid-ai-annotator-source-1`  
> Original URL: <https://plaid.com/blog/ai-agents-june-2025/>  
> Final URL: <https://plaid.com/blog/ai-agents-june-2025/>  
> Title: Agents in Action: Leveraging AI to improve our core product experiences | Plaid  
> Captured at: `2026-08-31T17:45:23Z`

---

AI is a critical lever in solving some of the most persistent challenges we face, from ensuring data accuracy to maintaining seamless connectivity. Over the past year, we’ve been investing in AI-powered tooling to help with our relentless focus on quality, reliability, and user experience.

Today, we’re highlighting two of these internal AI agents: **AI Annotator**, which accelerates generating high-quality data labeling for model training, and **Fix My Connection**, which proactively repairs bank integrations to reduce downtime and improve conversion. These agents are already making a tangible impact across Plaid’s platform, powering better categorization, faster fixes, and more resilient user experiences at scale.

### AI Annotator

High-quality labeled data is essential for machine learning models to deliver reliable results, especially for complex tasks like categorizing financial transactions. At Plaid, the demand for labeled data spans across Personal Finance, Credit, Payments and other use cases, but has struggled to keep pace. Although we process millions of transactions daily, the scalability of manual labeling was a persistent challenge. Without a faster, more reliable way to generate labeled data, our ability to train, benchmark, and materially improve models has been limited.

**Our Solution:** Advances in large language models (LLMs) paved the way for our AI Annotator, an internally hosted platform that automates large-scale labeling of anonymized transactions while enabling targeted human validation when required for a product use-case. Key capabilities include:

**Impact**: In early use, our AI Annotator is able to produce high quality labels that have greater than 95% human alignment at a fraction of cost and time because of the scale of transaction data we have to train and test it on. This increase in annotation capacity directly enables improving categorization models and enhancing insights.

**What’s next** We're expanding our annotation agent to support a broader range of classification tasks, including income identification, client vertical (industry) detection, and business finance classification. On the platform side, we're enhancing the agent's capabilities by incorporating richer knowledge sources and contextual signals, introducing voting mechanisms across multiple LLMs, and integrating feedback loops to continuously improve performance over time.

### Fix My Connection

Reliable access to thousands of smaller banks and credit unions is critical for our customers, they depend on seamless connectivity to reach every user, drive conversions, and maximize lifetime value. However, manually building and maintaining these connections at scale is challenging and costly. Further, when these institutions inevitably update their login experiences, users can face interruptions - impacting conversions, user satisfaction, and growth potential.

To ensure our customers can always reach their users, we turned the deep knowledge we've gained from managing thousands of integrations into automated tools that swiftly repair and easily expand customer access to user-permissioned data at financial institutions.

**Our Solution:** We built an AI-powered system that proactively detects & automatically repairs access issues to minimize manual effort and ensure seamless experiences for users.

**Impact**: Our automated repairs have already enabled over 2 million successful user-permissioned logins, and reduced the average time to fix a degradation by 90%. With fewer manual repairs required, we're resolving issues faster, improving connection reliability, and helping our customers drive better business outcomes.

**What’s next:** We’re expanding our agent’s capabilities from repairing to proactively creating new integrations - rapidly growing coverage across more institutions. Additionally, we're actively developing new AI-driven capabilities to support even more products and features from financial institutions - empowering our customers to unlock richer, more comprehensive financial scenarios for users, no matter where they bank.

These AI agents are just the beginning. As part of our broader focus on using AI to improve all parts of the Plaid platform we [recently launched a MCP server](https://plaid.com/blog/plaid-mcp-ai-assistant-claude/) that allows developers to more seamlessly use AI to troubleshoot and analyze integrations in real time. We also [opened up MCP Server access](https://plaid.com/blog/anthropic-api-mcp/) to external AI agents via the Anthropic and OpenAI APIs, enabling customers to build smarter internal tools and support experiences powered by real-time Plaid data. Together, these advancements reflect our commitment to making Plaid not just more powerful, but more intelligent, responsive, and developer-friendly than ever before.
