> Archived source snapshot  
> Source ID: `brex-agent-platform-source-1`  
> Original URL: <https://www.firstround.com/ai/brex>  
> Final URL: <https://www.firstround.com/ai/brex>  
> Title: Agent + Human Ops: How Brex is Changing Roles and Workflows | First Round  
> Captured at: `2026-08-31T17:40:35Z`

---

Brex CTO spends a lot of time thinking about how AI can make Brex disappear. “Nobody wakes up and says ‘I can’t wait to spend time in Brex,’” he says.

“We believe the best user interface is just the card that lets you swipe and go. Most of our investments on the product AI side are oriented around the thinking of eliminating Brex from your overall experience. The best AI is the AI that you don’t notice because it’s taken work away.”

, Brex’s COO, shares this thinking, except she’s looking inward at the company’s operations — using AI to reduce the toil of the most manual, prescriptive work. **“If I was starting the company today in this new AI era, I’d build operations completely different**,” says Matias. “We can’t just use ChatGPT. The roles must be different. We’re changing what we expect from people.”

Matias quickly found herself staring down into a rabbit hole, running through everything she’d need to do to actually make this fundamental shift within the operational team. “I knew we needed to be AI-native on all our manual tasks, which meant shifting our BPO (business process outsourcing) strategy, which meant agents doing the work, which meant managers overseeing agents and people,” she says. “I was then thinking through all the tech we needed, how we’d train people, how I was going to make the case for this evolution.”

Turns out, Reggio was already building a solution.

Brex has three AI pillars. Reggio is responsible for product AI, the customer-facing AI features. Matias owns operational AI, the internal use of AI to scale the business. And, together, they are also building a corporate AI workstream, the AI tools employees use to do their day-to-day work.

“There’s actually a hidden fourth pillar, which is an AI platform that serves both our product and operational pillars,” says Reggio. “We have a lot of common platform and infrastructure investments that help us deliver those features to our customers as well as build the features that power our operations internally.”

The platform Reggio built became an unlock for Matias. With this tool, her blurry vision for the future of Brex’s operations became clearer — she began to deploy agents, shift the work happening within roles and rebuild workflows based on what AI was best at.

In this exclusive interview, we sit down with both Reggio and Matias to learn about how this platform is serving both the external product and internal operations, how AI is changing necessary skills and hiring processes, and where AI is making the most impact for Brex employee and customer experience.

Let’s dive in.

In order to enable more internal AI adoption, Reggio identified two early hurdles to clear. “The first is how we can shorten the time that it takes to go from, ‘Hey I saw this on Twitter and I want to give it a shot’ to actually doing it safely within Brex,” he says. “The second is how we eliminate the legal, procurement and onboarding barriers a company of our size normally faces when bringing in new tools.”

**To solve the first challenge, he built an internal platform in Retool fashioned from the product’s external AI features, where employees could build, test and deploy agents — all with the underpinning of security and infrastructure core to Brex’s product**.

“This effort started in March 2023, when we started kicking the tires on LLMs, not knowing exactly what we were going to do but trying to figure out how to add value to the org,” Reggio says. “It started as basically a copy of the OpenAI developer platform, but through the years, we’ve kept adding more features to it.”

This “agent platform” now has: a prompt management system that allows users to refine implementations, multi-model testing, evaluation frameworks and API integrations for automated workflows.

The systems engineering team, which is about 25 people out of the whole 350-person EPD department, builds and maintains the internal agent platform. “We treat it like an external product, and in some ways, it is,” says Reggio. “We enable the team to work on the technological frontier. AI explorations happen in these systems. We want them to push the envelope and use LLMs to accelerate our workflows.”

This also creates a product loop, where both internal and external features improve simultaneously. “The functionality of our internal MCP has rapidly evolved because it’s the same as our external MCP. Whenever we add a new tool to Brex’s product via MCP, it’s immediately visible internally — you see it in the agent platform and can start using it, existing agents can start using it. It’s always getting better,” says Reggio.

> You also get all the benefits of doing operational things with a high level of rigor.

James Reggio

CTO at Brex

Another example (this time, going from internal product to external) is something they’re still working on: an onboarding agent. The process of onboarding to Brex can be fairly long and complicated, especially for mid-market or enterprise customers — which actually receive an implementation consultant who collects policy and operating documents, connects HRIS and ERP software and more.

“This is the type of thing the implementation consultant would do through a lot of discovery calls. We’ve built an agent they can use on the back end to speed this process up, but we’re also trying to expose it in the product so customers can do it themselves,” he says.

The other hurdle was legal and procurement. Many 1,000+ employee companies might conduct lengthy RFP processes for expensive new tools, do a bake-off between vendors, run a pilot, then have to navigate complex licensing and contracting. “By the time we complete that process, whatever tool that was the front runner at the beginning would be displaced by a different tool,” says Reggio.

**To streamline legal approvals, Brex created approval tracks based on what happens to data rather than who provides the tool** — this lifecycle-based approach recognizes that architectural characteristics matter more than vendor identity for risk mitigation.

### Stay ahead.

Get Applied Intelligence in your inbox.

Brex pre-approves sub-categories of AI tools under a set of defined controls, like those that don’t retain data for 30 days, don’t use inputs for model training and maintain data segregation. Product and legal teams established a process for structured experimentation within predefined guardrails — like the company’s reclassification of development codebases as “low-risk corporate data” and requiring SSO authentication through internal Retool proxies rather than individual accounts. This approach eliminates redundant, case-by-case legal reviews.

Brex routes all AI tools through provisioning tool and lets employees pick the ones they’re most comfortable and productive with — and build their own AI stack. “We built this system where in Slack you can type /c1 and a modal pops up where you configure what AI tools you want to use. And once you save it, in the background, everything gets provisioned in Okta and makes sure you have access to those tools,” Reggio says. An added benefit of this process is that it creates leverage in contracting and renewal conversations. “Philosophically, we don’t want to pick winners among tools. But we have the data to show which ones our employees want.”

With the tooling and procurement challenges mostly resolved, Reggio enabled Matias and her team to develop their own custom tools and workflows with speed.

For Brex, and any financial services company, roles are very specialized — customers are different, the tasks to serve them are different and the context required to complete those tasks is different.

“Before AI, if you wanted extremely efficient operations, you needed very specific teams dealing with specific client segments. I needed a credit specialist, a KYC (know your customer) specialist, a payments specialist,” says Matias. “But that’s constrained by how many groups you have and how you enable connection between them. It forces you to have a robust infrastructure, which slows you down. I wanted to move quicker. With AI, that’s not a bottleneck anymore.”

Reggio has a mental model that Matias has also adopted: “We take a persona-based approach, but not persona as in a user. We do a lot of product thinking around what it would look like to embody different roles that could be doing work on behalf of the user in AI agents.”

Without reliance on specialists, Matias is free to reimagine workflows across operations: a platform approach where functions are horizontal and stretch across all products.

L1 is the first level, which handles all process-driven work. Take customer onboarding as an example: “If we were going to launch a new product, we’d create an SOP (standard operating procedure) and train our BPOs, enable them with basic tooling and allow them to handle some of the basic operations, like scheduling customer payouts, reviewing documentation or handling customer clarifying questions,” says Matias. “It’s prescriptive and I expect people to follow very specific guidance.”

**This is the level that’s changing most drastically with AI, becoming fully-automated with no human involvement in most cases**. “Anywhere you have a BPO, you usually have a well-defined SOP and work that’s parceled up effectively to be handled by an LLM,” says Reggio. “So we’re having really good success taking defined processes and mapping them to agents.” Since rolling out its generative AI customer support agents, over 50% of cases are resolved by the chatbot as the first customer touchpoint. Matias has also migrated over 15 CS roles to L2, which handles more complex cases.

L2s take cases that have been escalated and haven’t been resolved by L1s. This level is composed mostly of senior analysts and managers who oversee certain cases and processes executed in L1 (by internal teams or BPOs), communicating directly with customers on more sensitive tickets.

An important part of that work is QA, but even that has shifted. “Instead of five QA specialists analyzing responses from BPOs, it’s now one person doing every single interaction leveraging AI,” says Matias. “Every response gets put through an agent that uses our quality rubric. AI is now doing 100% of the QA while leads and managers focus on coaching and improving the agents.”

Because many L1 responses are now AI-generated, AI is actually QAing AI here — and instead of using sample cases for training, AI QAs all human cases, identifying response trends that are leveraged in a closed feedback loop to improve agent and human performance.

> L2s used to manage people. Now my expectation is that they’re managing agents as well.

Camilla Matias

COO at Brex

This changing role also requires new skills. They’re prompt engineers and workflow analysts who need to understand both how to drive value for the business and how to use the technology to achieve their goals.

“Previously, you needed to be good at managing humans, doing performance reviews and motivating the team,” says Matias. “The reality is that now, you also need to be able to manage agents, be good analytically, improve prompts and provide feedback. Instead of doing a performance review, you’re giving feedback to a prompt.”

The final level is L3 — composed of experts and specialists who retain that deep, industry knowledge on specific subjects. While they’re still interacting with customers and handling the highest escalations, the roles have more breadth.

### Skip the AI theater.

See what’s already running in production.

For example, L3s in credit and fraud strategy are responsible for identifying overall portfolio performance, understanding loss trends, reporting to investors/lenders and creating policies to grow new markets and segments. In compliance, L3s are required to make sure L2s (humans and agents) understand regulatory requirements and follow changes. “Instead of thinking about designing human relationships, they’re designing the system of agents plus humans,” says Matias.

**With AI becoming central to everyone’s role on the operations team (and across the entire company), Brex launched an org-wide AI training program**. “All my direct reports, regardless of seniority, must go through it — including myself,” says Matias.

- It starts with prompting techniques: understanding the difference between models and what RAG is, how to properly give context in a prompt and ask very specific questions.
- Then it gets more specific — breaking down each of the tools people should be using in their specific roles and how to use them. “How we use Notebook LLM to create notes or use a different model to create an output that’s knowledge management-based,” Matias says. “We use different tools for different use cases and we want to make sure everyone knows how to use them.”
- It then gets more advanced, where people are designing workflows and creating agents. “We also have separate segments based on folks’ roles. For example, one training is data-focused, like how we use LLMs to work with data,” she says. “You don’t need to know how to use SQL but if you can use Cursor, you can get most of the way there.”

At the end of the course, employees on the operations team are asked to rank themselves on one of four AI fluency levels, supporting their choice with specific examples (and using this form to assess performance at quarterly check-ins with their managers):

1. User:
	Uses available AI tools to assist with simple processes and their defined responsibilities and day to day workflows. Understands basic prompting and limitations.
2. Advocate:
	Actively integrates AI into independent or team workflows. Can design or manage small to medium "human-in-the-loop" AI workflows and processes.
3. Builder:
	Can proactively build, design, refine, or manage AI-driven solutions or tools that create significant business value.
4. Native:
	Can set the AI vision and strategy for a team or department. Can pioneer novel applications of AI.

“And if they’re in the bottom quartile, I work with their managers directly to assign these individuals projects to help build their fluency,” says Matias. Most of these projects are role-specific, generally automating tasks they do more than 3-5 times per day. Some examples of projects include automating reporting cadences and creating FAQ chatbots for cross-functional partners.

### The ascension of the generalist

With AI making knowledge more accessible — and the resulting changes to roles within the operations team — Matias has shifted her hiring focus to bring in more generalists instead of specialists. “The generalist becomes very powerful because you can do multiple functions within one. We have more generalists covering different parts of the org,” she says.

To actually assess AI-specific, generalist skills in the hiring process, Matias has adjusted questions in both screening and interviews. “For every single hire outside of support, we require a case study in how folks are using AI,” Matias says.

> We request to see how they’re prompting and see how they did the work using AI. The outputs don’t really matter. It’s more about how people think.

Camilla Matias

COO at Brex

In screening, it’s a simple qualification question asked during initial conversations. “It’s more trying to understand how familiar and fluent they are — how have you been using AI? What tools do you use? Which LLMs do you prefer, and why?” she says.

But as candidates progress through the interview process, they’re expected to conduct a case study that is meant specifically to assess their ability to use AI. One example asks how a candidate might navigate and price complex, high-value sales deals. They receive seven different real-life scenarios (high risk, low cash flow, reward-based, etc.) and are asked to come up with pricing for each of these and present their findings to a panel.

Because there are so many different paths to these deal desk scenarios, Matias expects candidates to have used AI to figure them out, even if it’s not explicit during the assignment. They’re given a few days to complete the case, which is challenging because they’re solving real business problems they haven’t encountered before.

Candidates are also asked to share their prompts for analysis. “We’re asking about how they addressed the pricing of a situation, why they decided X and what the resulting Y is, what the right response is to each of these scenarios,” she says. “It’s important to be thinking about all these problems and come up with solutions for the different scenarios — even if it’s not correct, it shows they’re AI fluent, and that’s very relevant.”

Instead of trying to force AI into existing human processes and workflows, Brex takes a different approach: find the places where AI has a fundamental advantage and redesign workflows around those strengths.

“The key insight is don’t overthink it,” says Reggio. “If you can break down a workflow into an SOP that you can describe to a human, then an LLM can probably perform it pretty well. Then it’s just basic prompt engineering.” For example, in the KYC process, an application would come in for manual review and an ops analyst would follow their SOP to check off each requirement to onboard the account: verify the address, assign an industry, etc. To automate this process, the SOP was broken down for each step, making it capable for an agent to perform (with human checks).

In addition to considering AI’s innate skills, Matias established criteria for what they’d automate first:

- **Time consumption**. “How many hours does an individual spend doing a task?” says Matias. High-volume, time-intensive processes were flashing targets, like disputes and KYC.
- **AI’s advantage over a human**. “How much better can the LLM perform than the human?” Matias says. It’d depend on the needs of the tasks, like context gathering, speed of execution, pattern matching, etc.
- **Implementation speed**. Matias wanted quick wins to prove value.

**But there’s also one important parameter for how they approach the general thinking around AI’s impact: It isn’t all or nothing**.

> When you set the goal at 100% automation as opposed to 40% automation, you end up making investments that are oftentimes going to yield zero value because they have a binary outcome.

James Reggio

CTO at Brex

For Brex’s fraud agent, getting to the point where they could have 100% confidence in the agent’s recommendation would’ve been a massive undertaking. Instead, they only automated the cases with high confidence in its recommendation — and the remainder are still reviewed by an analyst (assisted with AI-generated findings). This incremental approach delivered immediate value while building toward more comprehensive solutions.

### Subjective judgement (surprisingly)

Perhaps most shocking was AI’s performance on ambiguous tasks requiring human judgement.

Adverse media recognition — which is part of the KYC process — is a task that requires analyzing news to identify events that would disqualify companies from underwriting. It’s work that requires synthesizing low-quality, unstructured data sources. “There’s a lot of gray in KYC. There’s a lot of human judgement required when you’re looking up a business and trying to ascertain from different media about the business’s legitimacy. There’s a lot of human quality control,” says Reggio.

An agent created in the agent platform now handles this adverse media recognition in the KYC process, and actually outperformed humans by a couple of percentage points. “ **It went from 85% to 88% accuracy. It’s still not greater than 90% though, which speaks to how difficult it is to define what meets the criteria of ‘adverse media,**’” Reggio says. “But that gives us more confidence to crank it up. Maybe from 10% of traffic to 50% to maybe 100% of applications over time.”

Another workflow requiring subjective judgement is the personalization of emails as part of delinquent account servicing — which involves multiple touchpoints with customers who haven’t paid their statements. There’s a whole set of workflow SOPs that get followed: account research, reaching out via several channels and possibly generating a payment plan.

“You can imagine a pretty complex flowchart for us to maximize recoveries,” says Reggio. “We chose that workflow not because of the shape of the problem, but more so because it’s a high-cost area we wanted to improve upon. So it was a great place for us to experiment.”

Previously, Brex employees would modify email templates when reaching out to delinquent accounts. It turns out, AI was actually better at this too. Initial outreach is automated by an agent using a personalized template, but it’s really in subsequent interactions where AI shines by providing context to humans. It analyzes responses and layers in context about the account and the company’s negotiating guidelines. Then, it provides the servicing team with multiple options with various tones and levels of assertiveness based on the situation. The team can pick a draft and choose to further customize or send.

“Having an LLM personalize an email to get the attention of somebody who's late on their credit card statement is actually better than having a human take a template and lightly modify it. We got better response rates from that,” Reggio says.

### Understanding complex rules and guides

Disputes are an important workflow to get right — when a customer doesn’t recognize a charge on their card, they file a dispute and it’s Brex’s job to get that money back for the customer. To do that, employees must follow a huge guide with very specific rules that frequently change. “The process is very time-consuming. You have to complete every single detail, there are differences across merchants, different codes,” says Matias.

Then , Payment Operations Manager, used Brex’s internal agent-building platform to automate the entire process. He started by putting the 100+ page dispute guide into the platform. Then, he added the standard operating procedure that the BPO unit was using and iterated through prompts and results until creating an agent that hit his quality bar.

### Real AI implementation stories.

Straight to your inbox.

“ **We were able to not only turn a process that used to be three hours into three seconds, we were also able to get more robust submissions with better articulated reasons for our dispute than we were getting with the BPO**,” Matias says.

“In the past, we may have filed a dispute with four to five strong points based on the Mastercard rules. With AI as an expert, it may review the same case and find two to three additional points we hadn’t considered or have time to research, summarizing those findings in a more compelling way.”

### Following clearly-laid out steps at scale

KYC is the first step that any regulated financial institution goes through before bringing on a customer, verifying their identity and assessing risk. It’s a multi-step process with many deterministic factors, requiring pattern recognition with clear, objective criteria — making it perfect for automation.

Brex’s process is 14 steps; one of them is confirming the NAICS (North American Industry Classification System) business codes customers put on their application are correct. Teams would need to do manual research and cross-referencing to confirm these codes were accurate. “In the past, you’d have a human going through this, searching the web, and making sure it was the correct code for a particular industry,” Matias says. “But the reality is the LLM performs better than the human right away.”

The key input here is that each step in the process is so clearly documented in Brex’s SOP. In a live working session, ops leadership and engineers went line-by-line through SOPs and broke each down into the individual decisions and actions a person would take — effectively translating human workflows in clear instructions an LLM could follow.

> The more we can map operations workflows to a series of discrete steps a human might take, the more effective it is to throw the same SOPs you give to a human — inputs, account details — and have really good success routing those to an LLM.

James Reggio

CTO at Brex

“We can set up all the same QA and quality control processes we have internally, where humans review humans. Now humans review LLMs,” says Reggio.

By taking an approach that is more incremental, Brex is able to deliver an end product with a much higher level of confidence in its accuracy.

“If we tried to jump from someone applying for an account to a yes or no on the KYC, it wouldn’t have worked. Many third parties try this, throwing out how humans would normally do it and jumping straight to the end. They fail to such a high degree because they’re not accurate enough,” Reggio says.

“But we can take maybe eight to ten of the 14-step workflow and have really high confidence an LLM can complete those steps. So we’re able to shift human resources from reviewing documents and checking balances to actually reviewing trends of how customers and prospects are performing, shifting human effort to areas where it’s providing differentiated value.”

As Brex transforms its internal operations, the ceiling is pretty difficult for Matias to see. “I think we can operate 5x to 10x more efficiently, which sounds insane,” she says. But with the fundamental change that’s happening to almost every aspect of their work, it’s easy to think in exponents.

“When the operations team can fully own the automation of their processes, whenever we have a new process or go into a new market, it doesn’t require any engineering or data science effort,” says Reggio. This enables Matias to operate under a completely different set of constraints that aren’t limited by human scalability.
