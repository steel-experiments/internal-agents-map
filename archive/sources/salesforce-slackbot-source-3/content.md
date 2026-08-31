> Archived source snapshot  
> Source ID: `salesforce-slackbot-source-3`  
> Original URL: <https://venturebeat.com/technology/salesforce-rolls-out-new-slackbot-ai-agent-as-it-battles-microsoft-and>  
> Final URL: <https://venturebeat.com/technology/salesforce-rolls-out-new-slackbot-ai-agent-as-it-battles-microsoft-and>  
> Title: Salesforce rolls out new Slackbot AI agent as it battles Microsoft and Google in workplace AI | VentureBeat  
> Captured at: `2026-08-31T17:47:51Z`

---

![nuneybits Vector art of chat bubbles on a computer screen in th 5018a7ea-3496-4103-8453-7ba1b129189a](https://venturebeat.com/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fjdtwqhzvc2n1%2F4Xrcg14GLKFlwSEnuEzxyS%2F21c85d29d03c4c974076475c009e3b38%2Fnuneybits_Vector_art_of_chat_bubbles_on_a_computer_screen_in_th_5018a7ea-3496-4103-8453-7ba1b129189a.webp%3Fw%3D1000%26q%3D100&w=3840&q=85)

Credit: VentureBeat made with Midjourney

[Salesforce](https://www.salesforce.com/) on Tuesday launched an entirely rebuilt version of [Slackbot](https://slack.com/help/articles/202026038-An-introduction-to-Slackbot), the company's workplace assistant, transforming it from a simple notification tool into what executives describe as a fully powered AI agent capable of searching enterprise data, drafting documents, and taking action on behalf of employees.

The new Slackbot, now generally available to [Business+](https://slack.com/pricing/businessplus) and [Enterprise+](https://slack.com/enterprise) customers, is Salesforce's most aggressive move yet to position Slack at the center of the emerging "agentic AI" movement — where software agents work alongside humans to complete complex tasks. The launch comes as Salesforce attempts to convince investors that artificial intelligence will bolster its products rather than render them obsolete.

"Slackbot isn't just another copilot or AI assistant," said [Parker Harris](https://www.salesforce.com/company/parker-harris-bio/), Salesforce co-founder and Slack's chief technology officer, in an exclusive interview with Salesforce. "It's the front door to the agentic enterprise, powered by Salesforce."

## From tricycle to Porsche: Salesforce rebuilt Slackbot from the ground up

Harris was blunt about what distinguishes the new Slackbot from its predecessor: "The old Slackbot was, you know, a little tricycle, and the new Slackbot is like, you know, a Porsche."

The original Slackbot, which has existed since Slack's early days, performed basic algorithmic tasks — reminding users to add colleagues to documents, suggesting channel archives, and delivering simple notifications. The new version runs on an entirely different architecture built around a large language model and sophisticated search capabilities that can access Salesforce records, Google Drive files, calendar data, and years of Slack conversations.

"It's two different things," Harris explained. "The old Slackbot was algorithmic and fairly simple. The new Slackbot is brand new — it's based around an LLM and a very robust search engine, and connections to third-party search engines, third-party enterprise data."

Salesforce chose to retain the Slackbot brand despite the fundamental technical overhaul. "People know what Slackbot is, and so we wanted to carry that forward," Harris said.

## Why Anthropic's Claude powers the new Slackbot — and which AI models could come next

The new Slackbot runs on [Claude](https://claude.ai/), Anthropic's large language model, a choice driven partly by compliance requirements. Slack's commercial service operates under [FedRAMP Moderate certification](https://www.fedramp.gov/archive/2017-11-16-understanding-baselines-and-impact-levels/) to serve U.S. federal government customers, and Harris said Anthropic was "the only provider that could give us a compliant LLM" when Slack began building the new system.

But that exclusivity won't last. "We are, this year, going to support additional providers," Harris said. "We have a great relationship with Google. Gemini is incredible — performance is great, cost is great. So we're going to use Gemini for some things." He added that OpenAI remains a possibility as well.

Harris echoed Salesforce CEO Marc Benioff's view that large language models are becoming commoditized: "You've heard Marc talk about LLMs are commodities, that they're democratized. I call them CPUs."

On the sensitive question of training data, Harris was unequivocal: Salesforce does not train any models on customer data. "Models don't have any sort of security," he explained. "If we trained it on some confidential conversation that you and I have, I don't want Carolyn to know — if I train it into the LLM, there is no way for me to say you get to see the answer, but Carolyn doesn't."

## Inside Salesforce's internal experiment: 80,000 employees tested Slackbot with striking results

Salesforce has been [testing the new Slackbot internally for months](https://www.theverge.com/news/797890/slack-slackbot-ai-assistant-upgrade), rolling it out to all 80,000 employees. According to Ryan Gavin, Slack's chief marketing officer, the results have been striking: "It's the fastest adopted product in Salesforce history."

Internal data shows that two-thirds of Salesforce employees have tried the new Slackbot, with 80% of those users continuing to use it regularly. Internal satisfaction rates reached 96% — the highest for any AI feature Slack has shipped. Employees report saving between two and 20 hours per week.

The adoption happened largely organically. "I think it was about five days, and a Canvas was developed by our employees called 'The Most Stealable Slackbot Prompts,'" Gavin said. "People just started adding to it organically. I think it's up to 250-plus prompts that are in this Canvas right now."

Kate Crotty, a principal UX researcher at Salesforce, found that 73% of internal adoption was driven by social sharing rather than top-down mandates. "Everybody is there to help each other learn and communicate hacks," she said.

## How Slackbot transforms scattered enterprise data into executive-ready insights

During a product demonstration, Amy Bauer, Slack's product experience designer, showed how Slackbot can synthesize information across multiple sources. In one example, she asked Slackbot to analyze customer feedback from a pilot program, upload an image of a usage dashboard, and have Slackbot correlate the qualitative and quantitative data.

"This is where Slackbot really earns its keep for me," Bauer explained. "What it's doing is not just simply reading the image — it's actually looking at the image and comparing it to the insight it just generated for me."

Slackbot can then query Salesforce to find enterprise accounts with open deals that might be good candidates for early access, creating what Bauer called "a really great justification and plan to move forward." Finally, it can synthesize all that information into a Canvas — Slack's collaborative document format — and find calendar availability among stakeholders to schedule a review meeting.

"Up until this point, we have been working in a one-to-one capacity with Slackbot," Bauer said. "But one of the benefits that I can do now is take this insight and have it generate this into a Canvas, a shared workspace where I can iterate on it, refine it with Slackbot, or share it out with my team."

Rob Seaman, Slack's chief product officer, said the Canvas creation demonstrates where the product is heading: "This is making a tool call internally to Slack Canvas to actually write, effectively, a shared document. But it signals where we're going with Slackbot — we're eventually going to be adding in additional third-party tool calls."

## MrBeast's company became a Slackbot guinea pig—and employees say they're saving 90 minutes a day

Among Salesforce's pilot customers is [Beast Industries](https://www.thecashmerefund.com/portfolio-company/beast-industries), the parent company of YouTube star MrBeast. Luis Madrigal, the company's chief information officer, joined the launch announcement to describe his experience.

"As somebody who has rolled out enterprise technologies for over two decades now, this was practically one of the easiest," Madrigal said. "The plumbing is there. Slack as an implementation, Enterprise Tools — being able to turn on the Slackbot and the Slack AI functionality was as simple as having my team go in, review, do a quick security review."

Madrigal said his security team signed off "rather quickly" — unusual for enterprise AI deployments — because Slackbot accesses only the information each individual user already has permission to view. "Given all the guardrails you guys have put into place for Slackbot to be unique and customized to only the information that each individual user has, only the conversations and the Slack rooms and Slack channels that they're part of—that made my security team sign off rather quickly."

One Beast Industries employee, Sinan, the head of Beast Games marketing, reported saving "at bare minimum, 90 minutes a day." Another employee, Spencer, a creative supervisor, described it as "an assistant who's paying attention when I'm not."

Other pilot customers include Slalom, reMarkable, Xero, Mercari, and Engine. Mollie Bodensteiner, SVP of Operations at Engine, called Slackbot "an absolute 'chaos tamer' for our team," estimating it saves her about 30 minutes daily "just by eliminating context switching."

## Slackbot vs. Microsoft Copilot vs. Google Gemini: The fight for enterprise AI dominance

The launch puts Salesforce in direct competition with [Microsoft's Copilot](https://copilot.microsoft.com/), which is integrated into Teams and the broader Microsoft 365 suite, as well as Google's Gemini integrations across Workspace. When asked what distinguishes Slackbot from these alternatives, Seaman pointed to context and convenience.

"The thing that makes it most powerful for our customers and users is the proximity — it's just right there in your Slack," Seaman said. "There's a tremendous convenience affordance that's naturally built into it."

The deeper advantage, executives argue, is that Slackbot already understands users' work without requiring setup or training. "Most AI tools sound the same no matter who is using them," the company's announcement stated. "They lack context, miss nuance, and force you to jump between tools to get anything done."

Harris put it more directly: "If you've ever had that magic experience with AI — I think ChatGPT is a great example, it's a great experience from a consumer perspective — Slackbot is really what we're doing in the enterprise, to be this employee super agent that is loved, just like people love using Slack."

Amy Bauer emphasized the frictionless nature of the experience. "Slackbot is inherently grounded in the context, in the data that you have in Slack," she said. "So as you continue working in Slack, Slackbot gets better because it's grounded in the work that you're doing there. There is no setup. There is no configuration for those end users."

## Salesforce's ambitious plan to make Slackbot the one 'super agent' that controls all the others

Salesforce positions Slackbot as what Harris calls a "super agent" — a central hub that can eventually coordinate with other AI agents across an organization.

"Every corporation is going to have an employee super agent," Harris said. "Slackbot is essentially taking the magic of what Slack does. We think that Slackbot, and we're really excited about it, is going to be that."

The vision extends to third-party agents already launching in Slack. Last month, Anthropic released a preview of Claude Code for Slack, allowing developers to interact with Claude's coding capabilities directly in chat threads. OpenAI, Google, Vercel, and others have also built agents for the platform.

"Most of the net-new apps that are being deployed to Slack are agents," Seaman noted during the press conference. "This is proof of the promise of humans and agents coexisting and working together in Slack to solve problems."

Harris described a future where Slackbot becomes an [MCP (Model Context Protocol) client](https://modelcontextprotocol.io/docs/learn/client-concepts), able to leverage tools from across the software ecosystem — similar to how the developer tool Cursor works. "Slack can be an MCP client, and Slackbot will be the hub of that, leveraging all these tools out in the world, some of which will be these amazing agents," he said.

But Harris also cautioned against over-promising on multi-agent coordination. "I still think we're in the single agent world," he said. "FY26 is going to be the year where we started to see more coordination. But we're going to do it with customer success in mind, and not demonstrate and talk about, like, 'I've got 1,000 agents working together,' because I think that's unrealistic."

## Slackbot costs nothing extra, but Salesforce's data access fees could squeeze some customers

Slackbot is included at no additional cost for customers on [Business+](https://slack.com/pricing/businessplus) and [Enterprise+](https://slack.com/enterprise) plans. "There's no additional fees customers have to do," Gavin confirmed. "If they're on one of those plans, they're going to get Slackbot."

However, some enterprise customers may face other cost pressures related to Salesforce's broader data strategy. CIOs may see price increases for third-party applications that work with Salesforce data, as effects of higher charges for API access ripple through the software supply chain.

Fivetran CEO George Fraser has warned that Salesforce's shift in pricing policy for API access could have tangible consequences for enterprises relying on Salesforce as a system of record. "They might not be able to use Fivetran to replicate their data to Snowflake and instead have to use Salesforce Data Cloud. Or they might find that they are not able to interact with their data via ChatGPT, and instead have to use Agentforce," Fraser said in a [recent CIO report](https://www.cio.com/article/4108001/salesforce-is-tightening-control-of-its-data-ecosystem-and-cios-may-have-to-pay-the-price.html).

Salesforce has framed the pricing change as standard industry practice.

## What Slackbot can do today, what's coming in weeks, and what's still on the roadmap

The new Slackbot begins rolling out today and will reach all eligible customers by the end of February. Mobile availability will complete by March 3, Bauer confirmed during her interview with VentureBeat.

Some capabilities remain works in progress. Calendar reading and availability checking are available at launch, but the ability to actually book meetings is "coming a few weeks after," according to Seaman. Image generation is not currently supported, though Bauer said it's "something that we are looking at in the future."

When asked about integration with competing CRM systems like [HubSpot](https://www.hubspot.com/) and [Microsoft Dynamics](https://www.microsoft.com/en-us/dynamics-365), Salesforce representatives declined to provide specifics during the interview, though they acknowledged the question touched on key competitive differentiators.

## Salesforce is betting the future of work looks like a chat window—and it's not alone

The Slackbot launch is Salesforce's bet that the future of enterprise work is conversational — that employees will increasingly prefer to interact with AI through natural language rather than navigating traditional software interfaces.

Harris described Slack's product philosophy using principles like "don't make me think" and "be a great host." The goal, he said, is for Slackbot to surface information proactively rather than requiring users to hunt for it.

"One of the revelations for me is LLMs applied to unstructured information are incredible," Harris said. "And the amount of value you have if you're a Slack user, if your corporation uses Slack — the amount of value in Slack is unbelievable. Because you're talking about work, you're sharing documents, you're making decisions, but you can't as a human go through that and really get the same value that an LLM can do."

Looking ahead, Harris expects the interfaces themselves to evolve beyond pure conversation. "We're kind of saturating what we can do with purely conversational UIs," he said. "I think we'll start to see agents building an interface that best suits your intent, as opposed to trying to surface something within a conversational interface that matches your intent."

Microsoft, Google, and a growing roster of AI startups are placing similar bets — that the winning enterprise AI will be the one embedded in the tools workers already use, not another application to learn. The race to become that invisible layer of workplace intelligence is now fully underway.

For Salesforce, the stakes extend beyond a single product launch. After a [bruising year](https://www.investopedia.com/can-salesforce-stock-recover-here-s-what-wall-street-thinks-crm-earnings-11862399) on Wall Street and persistent questions about whether AI threatens its core business, the company is wagering that Slackbot can prove the opposite — that the tens of millions of people already chatting in Slack every day is not a vulnerability, but an unassailable advantage.

Haley Gault, the Salesforce account executive in Pittsburgh who stumbled upon the new Slackbot on a snowy morning, captured the shift in a single sentence: "I honestly can't imagine working for another company not having access to these types of tools. This is just how I work now."

That's precisely what Salesforce is counting on.
