> Archived source snapshot  
> Source ID: `stripe-minions-source-3`  
> Original URL: <https://news.ycombinator.com/item?id=47086557>  
> Final URL: <https://news.ycombinator.com/item?id=47086557>  
> Title: Minions – Stripe's Coding Agents Part 2 | Hacker News  
> Captured at: `2026-08-31T17:50:06Z`

---

[https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)

---

## Comments

> **testfrequency** · [2026-02-20](https://news.ycombinator.com/item?id=47087119)
> 
> How is this already #1 on the front page with 12 upvotes and 9 comments…
> 
> The article doesn’t reveal much. It feels like a fluff piece, and I can’t comprehend what the goal of sharing “we use AI agents” means for the dev community, with little to no examples to share. For a “dev” micro blog, this feels very lackluster. Maybe the Minion could have helped with the technical docs?
> 
> EDIT: *slightly adjusts tinfoil hat* minutes later it’s at #6
> 
> > **nylonstrung** · [2026-02-20](https://news.ycombinator.com/item?id=47087736)
> > 
> > It has all the trappings of NIH syndrome.
> > 
> > Reinventing the wheel without explaining why existing tools didn't work
> > 
> > Creating buzzwords ("blueprints" "devboxes") for concepts that are not novel and already have common terms
> > 
> > Yet they embrace MCP of all things as a transport layer- the one part of the common "agentic" stack that genuinely sucks and needs to be reinvented
> > 
> > > **menaerus** · [2026-02-20](https://news.ycombinator.com/item?id=47090861)
> > > 
> > > They mention "Why did we build it ourselves" in the part1 series: [https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-...](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)
> > > 
> > > However, it is also light on material. I would also like to hear more technical details, they're probably intentionally secretive about it.
> > > 
> > > But I do, however, understand that building an agent that is highly optimized for your own codebase/process is possible. In fact, I am pretty sure many companies do that but it's not yet in the ether.
> > > 
> > > Otherwise, one of the most interesting bits from the article was
> > > 
> > > \> Over 1,300 Stripe pull requests (up from 1,000 as of Part 1) merged each week are completely minion-produced, human-reviewed, but containing no human-written code.
> > > 
> > > > **tempest\_** · [2026-02-20](https://news.ycombinator.com/item?id=47090962)
> > > > 
> > > > "human reviewed"
> > > > 
> > > > "LGTM..."
> > > > 
> > > > I feel like code review is already hard and under done the 'velocity' here is only going to make that worse.
> > > > 
> > > > I am also curious how this works when the new crop of junior devs do not have the experience enough to review code but are not getting the experience from writing it.
> > > > 
> > > > Time will tell I guess.
> > > > 
> > > > > **menaerus** · [2026-02-20](https://news.ycombinator.com/item?id=47091129)
> > > > > 
> > > > > Agents can already do the review by themselves. I'd be surprised they review all of the code by hand. They probably can't mention it due to the regulatory of the field itself. But from what I have seen agentic review tools are already between 80th and 90th percentile. Out of randomly picked 10 engineers, it will provide more useful comments than most engineers.
> > > > > 
> > > > > > **tibbar** · [2026-02-20](https://news.ycombinator.com/item?id=47091592)
> > > > > > 
> > > > > > the problem with LLM code review is that it's good at checking local consistency and minor bugs, but it generally can't tell you if you are solving the wrong problem or if your approach is a bad one for non-technical reasons.
> > > > > > 
> > > > > > This is an enormous drawback and makes LLM code review more akin to a linter at the moment.
> > > > > > 
> > > > > > > **menaerus** · [2026-02-20](https://news.ycombinator.com/item?id=47091718)
> > > > > > > 
> > > > > > > I mean if the model can reason about making the changes on the large-scale repository then this implies it can also reason about the change somebody else did, no? I kinda agree and disagree with you at the same time, which is why I said most of the engineers but I believe we are heading towards the model being able to completely autonomously write and review its own changes.
> > > > > > > 
> > > > > > > > **tibbar** · [2026-02-20](https://news.ycombinator.com/item?id=47091849)
> > > > > > > > 
> > > > > > > > There's a good chance that in the long run LLMs can become good at this, but this would require them e.g. being plugged into the meetings and so on that led to a particular feature request. To be a good software engineer, you need all the inputs that software engineers get.
> > > > > > > > 
> > > > > > > > > **menaerus** · [2026-02-20](https://news.ycombinator.com/item?id=47092146)
> > > > > > > > > 
> > > > > > > > > If you read thoroughly through Stripe blog, you will see that they feed their model already with this or similar type of information. Being plugged into the meetings might just mean feed the model with the meeting minutes or let the model listen to the meeting and transcribe the meeting. It seems to me that both of them are possible even as of today.
> > 
> > > **\_\_float** · [2026-02-20](https://news.ycombinator.com/item?id=47089800)
> > > 
> > > What are the common terms for those? (I have heard "devbox" across multiple companies, and I'm not in the LLM world enough to know the other parts.)
> > > 
> > > **CuriouslyC** · [2026-02-20](https://news.ycombinator.com/item?id=47089363)
> > > 
> > > I was an early MCP hater, but one thing I will say about it is that it's useful as a common interface for secure centralization. I can control auth and policy centrally via a MCP gateway in a way that would be much harder if I had to stitch together API proxies, CLIs, etc to provide capabilities.
> > > 
> > > **croes** · [2026-02-20](https://news.ycombinator.com/item?id=47091375)
> > > 
> > > \>Reinventing the wheel without explaining why existing tools didn't work
> > > 
> > > Won‘t that be the nee normal with all those AI agents?
> > > 
> > > No frameworks, no libraries, just let AI create everything from scratch again
> > > 
> > > **throwaway-aws9** · [2026-02-20](https://news.ycombinator.com/item?id=47088920)
> > > 
> > > resume driven development
> 
> > **PunchyHamster** · [2026-02-20](https://news.ycombinator.com/item?id=47089086)
> > 
> > well, it's very important, now you know the financial code is handled by a bunch of barely supervised AI tools and can make decisions on whether to use product or not based on that
> > 
> > **netule** · [2026-02-20](https://news.ycombinator.com/item?id=47089007)
> > 
> > Stripe was launched through Y Combinator. It makes sense for their stuff to quickly bubble to the top of their news aggregator.
> > 
> > **BiteCode\_dev** · [2026-02-20](https://news.ycombinator.com/item?id=47087359)
> > 
> > Likely they have whitelisted domaine names that go straight to the home page. Would make sense to put all Y combinator ex and new startup sites.
> > 
> > Marketting is a major goal of HN after all.
> > 
> > > **dewey** · [2026-02-20](https://news.ycombinator.com/item?id=47088058)
> > > 
> > > Or the simpler explanation (which is probably closer to the truth): Stripe is a very popular company on HN as many people use them, their founders sometimes comment here and if they share their opinion on something people pay attention and upvote it.
> > > 
> > > > **nullstyle** · [2026-02-20](https://news.ycombinator.com/item?id=47088242)
> > > > 
> > > > Or the even simpler explanation, that whenever Stripe posts a blog post, they have nine or 10 employees waiting to upvote it the moment it goes live.
> > > > 
> > > > **BiteCode\_dev** · [2026-02-20](https://news.ycombinator.com/item?id=47091087)
> > > > 
> > > > Doesn't explain how you get to the frontpage with less than 20 upvotes magically.
> > > > 
> > > > > **steveklabnik** · [2026-02-20](https://news.ycombinator.com/item?id=47091207)
> > > > > 
> > > > > You only need about 4 upvotes in the first 20 minutes or so to get on the front page. It's the same for every story.
> > 
> > > **handfuloflight** · [2026-02-20](https://news.ycombinator.com/item?id=47087631)
> > > 
> > > your absolut lee r8

> **hibikir** · [2026-02-20](https://news.ycombinator.com/item?id=47089319)
> 
> Stripe had invested a lot in dev experience over the years precisely because of how "unique" some of the technology choices were: Mongo and originally normal Ruby for a system that mainly deals with money? Without a massive test suite, letting a normal dev make changes without a lot of rails is asking for a sea of incidents. If I recall correctly, the parallelization needed to run the unit tests for developers used to make the cost of continuous integration higher than the cost of the rest of the ec2 instances. Add the dev boxes, as trying to put a useful test environment in a laptop became unreasonable, and they already start with a pile of guardrails tooling that other companies never even needed. A hassle for years, but now a boon, as the guardrails help the LLMs.
> 
> It'd be nice to get an old school, stripey blog post, the kind that has a bit less fluff, and is mostly the data you'd all have put in the footnotes of the shipped email. Something that actually talks about the difficulties, instead of non-replicable generalities. After all, if one looks at the stock price, it's not as if competitors are being all that competitive lately, and I don't think it's mainly the details of the AI that make a difference. It'd also be nice to hear what goes one when not just babysitting minions, if there's actually anything else a dev is doing nowadays. AI adoption has changed the day to day experience within the industry, as most managers don't seem to know which way is up. So just explaining what days look like today might even sell as a recruiting initiative.

> **jimmydoe** · [2026-02-20](https://news.ycombinator.com/item?id=47087926)
> 
> This is a devops post. They just brag about the plumbing.
> 
> Dark secret of dark factory is high quality human input, which takes time and focus to draft up, otherwise human will end up multiple shot it, and read thru the transcript to tune the input.

> **gas9S9zw3P9c** · [2026-02-20](https://news.ycombinator.com/item?id=47086953)
> 
> Where is the detail? Examples? Something concrete? I don't think it is, but it does read like LLM generated content marketing. Lots of generic statements everyone knows. Yes, dev environments are helpful. Have been for 20 years. Yes, context and rules are important for agents. Surprise.
> 
> TLDR "look we use AI at Stripe too, come work here"
> 
> > **menaerus** · [2026-02-21](https://news.ycombinator.com/item?id=47098381)
> > 
> > Why would you go and work for a company that markets itself in the blog post that they just managed to automate a substantial part of the software engineering work?

> **3rodents** · [2026-02-20](https://news.ycombinator.com/item?id=47086907)
> 
> Are any companies doing this sharing the code being produced or some example Pull Requests? I am wondering if a lot of the human review is substantive or rubber stamping - as we see with long Pull Requests from humans. I know I would half-ass a review of a PR containing lots of robot code. I assume stripe has higher standards than me but would be nice to see some real world examples.
> 
> > **fnord123** · [2026-02-20](https://news.ycombinator.com/item?id=47086950)
> > 
> > On thing that troubles me is that code reviews are also an educational moment for seniors teaching juniors as well as an opportunity for people who know a system to point out otherwise undocumented constraints of the system. If people slack on reviews with the agent it means these other externalities suffer.
> > 
> > Are being handling this at all? Is it no longer needed because it gets rolled into AGENTS.md?
> > 
> > > **blitzar** · [2026-02-20](https://news.ycombinator.com/item?id=47086989)
> > > 
> > > I find working with Ai a lot like working with a junior employee... with the junior employee they learn and get better (skill level and at dealing with me) but with Ai the mentoring lessons reset once you type /clear
> > > 
> > > Skills are a positive development for task preferences, agents.md for high level context, but a lot of the time its just easier to do things the way your Ai wants.
> > > 
> > > **yunohn** · [2026-02-20](https://news.ycombinator.com/item?id=47088290)
> > > 
> > > \> educational moment for seniors teaching juniors
> > > 
> > > You see, this is no longer necessary - companies are firing all the non-seniors, are not hiring any juniors, and delegating everything to AI. This is the future apparently!

> **rmac** · [2026-02-20](https://news.ycombinator.com/item?id=47093680)
> 
> When the norm on HF daily papes is a pdf, a website, & a git, corp. thinkpieces like this are going to have to work a lot harder to get any meaningful engagement and onward corp word-of-mouth. like i now think stripe has fallen a but, where before they were tier...
> 
> this is the risk you run putting out subpar content in a world where the norms and appetites shift daily. slightly unfair? yes, as stripe has never been one to shine in the "corp infra open source" category tho; Which is crazy because it doesn't reflect the ridiculous talent they have internally.

> **tuhgdetzhh** · [2026-02-20](https://news.ycombinator.com/item?id=47093563)
> 
> \> Since MCP is a common language for all agents at Stripe, not just minions, we built a central internal MCP server called Toolshed, which hosts more than 400 MCP tools spanning internal systems and SaaS platforms we use at Stripe.
> 
> Are there ecisting open source solutions for such a toolshed?

> **rco8786** · [2026-02-20](https://news.ycombinator.com/item?id=47087114)
> 
> I'm sure there are lots of Stripe engineers that cruise the comments here. Anyone care to provide some color on how this is actually working? It's not a secret that agents can produce tons and tons of code on their own. But is this code being shipped? Maintained? Reviewed?
> 
> > **etothet** · [2026-02-20](https://news.ycombinator.com/item?id=47087644)
> > 
> > Part 1 is linked in this article and explains a bit: “Minions are Stripe’s homegrown coding agents. They’re fully unattended and built to one-shot tasks. Over a thousand pull requests merged each week at Stripe are completely minion-produced, and while they’re human-reviewed, they contain no human-written code.”
> > 
> > I could be wrong, but my educated guess is that, like many companies, they have many low hanging fruit tasks that would never make it into a sprint or even somewhat larger tasks that are straight forward to define and implement in isolation.
> > 
> > **dakolli** · [2026-02-20](https://news.ycombinator.com/item?id=47087236)
> > 
> > The few guys who they haven't laid off are too busy reviewing and being overworked, doing the work of 10 to scroll HN. Gotta get their boss another boat, AI is so awesome!
> > 
> > > **malfist** · [2026-02-20](https://news.ycombinator.com/item?id=47088079)
> > > 
> > > Stripe hasn't had a layoff in a good while. Stripe is hiring like mad and is planning on growing engineering significantly. Your comment isn't grounded in reality
> > > 
> > > > **snayan** · [2026-02-20](https://news.ycombinator.com/item?id=47089819)
> > > > 
> > > > Seems like they've been pretty successful with this method? Why do you think it's bullshit?
> > > > 
> > > > > **rileymichael** · [2026-02-20](https://news.ycombinator.com/item?id=47094423)
> > > > > 
> > > > > successful how? the only metric i see is # of pull requests which means nothing. hell, $dayJob has hundreds of PRs generated weekly from renovate, i18n integrations, etc. with no LLM in the mix!

> **eric\_khun** · [2026-02-20](https://news.ycombinator.com/item?id=47090730)
> 
> is there a way to visualize what your agents are doing? I'm adding a bunch of debug code to the claude agent sdk, but it's a bit overwhelming to read at some time , but I just want to see visually what how it does all the tools calling, what files it reads etc…
> 
> > **\_ink\_** · [2026-02-20](https://news.ycombinator.com/item?id=47090892)
> > 
> > In Part 1 of the post they show that their agent has some kind of UI.

> **nottorp** · [2026-02-20](https://news.ycombinator.com/item?id=47087336)
> 
> Hey can they ask their coding agents to support 3D secure, so I can pay with EU emitted credit cards on the few US sites I'm interested in?
> 
> > **lmz** · [2026-02-20](https://news.ycombinator.com/item?id=47088385)
> > 
> > That's for the Stripe customer to configure. Stripe itself has supported 3DS since ages ago.
> > 
> > Edit: also you'll find a pretty common sentiment among US website owners is that the new API that supports 3DS is overcomplicated and they want their 7 lines of code create-a-charge-with-a-token back. Screw the Europeans because they only care about US buyers anyway.
> > 
> > > **nottorp** · [2026-02-21](https://news.ycombinator.com/item?id=47102295)
> > > 
> > > Well it's not like I buy many physical goods from US companies (and amazon US is fine, even handles customs for me).
> > > 
> > > Keeping my subscriptions to Asimov's and Ars Technica is becoming a pain though because ... Stripe I guess. Ars staff even confirmed it.
> > > 
> > > A Revolut card works fine, local banks' cards deny the charge by default and if you're lucky they call you and ask if they should allow it.

> **prima-facie** · [2026-02-20](https://news.ycombinator.com/item?id=47090042)
> 
> What's the deal with \`Devboxes\`? is this a common thing? Sounds very clunky for regular (human-driven) development.
> 
> > **embedding-shape** · [2026-02-20](https://news.ycombinator.com/item?id=47090069)
> > 
> > Seems like a compliance thing? I too run my LLMs inside some sort of containment and does "manual" development inside the same environment, but wouldn't make sense to have that containment remotely, so I'm guessing that's because they need to have some sort of strict control over it?
> > 
> > > **kkl** · [2026-02-21](https://news.ycombinator.com/item?id=47097359)
> > > 
> > > While there are compliance/security benefits it is not the primary motivation.
> > > 
> > > If you have fairly complicated infrastructure it can be way more efficient to have a pool of ready to go beefy EC2 instances on a recent commit of your multi-GB git repo instead of having to run everything on a laptop.
> 
> > **chrchr** · [2026-02-20](https://news.ycombinator.com/item?id=47092593)
> > 
> > Amazon developers use similar devboxes. I think it is mostly so that developers can use a production-like Linux environment with integrated Amazon dev tooling. You're not required to use a devbox, but it can be easier and more convenient than running stuff on your laptop.
> > 
> > **steveklabnik** · [2026-02-20](https://news.ycombinator.com/item?id=47091232)
> > 
> > It's not uncommon. It's more common at large companies. For example, Google calls theirs "Clients in the Cloud".

> **hrgahb** · [2026-02-20](https://news.ycombinator.com/item?id=47091636)
> 
> Either one should drop Stripe due to vibe coding or this is just a marketing favor to other VC AI companies to boost AI in general.

> **vbs\_redlof** · [2026-02-20](https://news.ycombinator.com/item?id=47086921)
> 
> Good to see we're vibe coding critical financial infrastructure. Progress is being made.
> 
> Next up: let's vibe code a pacemaker.
> 
> > **trevorhinesley** · [2026-02-20](https://news.ycombinator.com/item?id=47087001)
> > 
> > The glass-half-full here is it’s an incredible signal that one of the largest financial gateways in the world is \_able\_ to do this with current capabilities.
> > 
> > Personally, this is exciting.
> > 
> > > **handfuloflight** · [2026-02-20](https://news.ycombinator.com/item?id=47087089)
> > > 
> > > They are enforcing rigor, on agents, the same way they would on humans. Do people think Stripe's engineering team would have been able to progress if each individual (human | machine) employee was not under harness and guardrail, and just wrote code willy nilly according to their whims? Vibe coding is whimsical, agentic engineering is re-applying what brought and brings rigor to software engineering in general, just to LLM outputs. Of course, it's not only that and there are novel problem spaces.
> > > 
> > > > **stareatgoats** · [2026-02-20](https://news.ycombinator.com/item?id=47088630)
> > > > 
> > > > Isn't there a rule against this - i.e. accusing commenters for using LLMs (the offensive language aside)? Implicitly there is \[0\], because I can't see how it adds to the conversation. So what if it sounds like an LLM? Soon you won't be able to tell the difference anyway, and all that will be left is some chance that you are correct. Comments should be judged their content merits, not on whether the commenter is native English speaker or not.
> > > > 
> > > > \[0\] > Be kind. Don't be snarky. Converse curiously; don't cross-examine. Edit out swipes. Comments should get more thoughtful and substantive, not less, as a topic gets more divisive. When disagreeing, please reply to the argument instead of calling names. "That is idiotic; 1 + 1 is 2, not 3" can be shortened to "1 + 1 is 2, not 3." Don't be curmudgeonly. Thoughtful criticism is fine, but please don't be rigidly or generically negative.
> > > > 
> > > > etc: [https://news.ycombinator.com/newsguidelines.html](https://news.ycombinator.com/newsguidelines.html)
> > > > 
> > > > > **handfuloflight** · [2026-02-20](https://news.ycombinator.com/item?id=47088932)
> > > > > 
> > > > > What can I say? I speak like my friends.
> > > 
> > > > **handfuloflight** · [2026-02-20](https://news.ycombinator.com/item?id=47087356)
> > > > 
> > > > You're absolutely wrong! @dang, I really did write each letter by hand!
> > > > 
> > > > Lt. Dang, ice cream!
> > 
> > > **kypro** · [2026-02-20](https://news.ycombinator.com/item?id=47087076)
> > > 
> > > Exactly, 1000 PRs per week probably equates to around ~100 engineers worth of output.
> > > 
> > > Hard to do an exact ROI, but they're probably saving something like $20,000,000+ / year from not having to hire engineers to do this work.
> > > 
> > > > **qudat** · [2026-02-20](https://news.ycombinator.com/item?id=47087324)
> > > > 
> > > > They still need someone to review and hopefully QA every PR. I doubt it’s saving much time except maybe the initial debug pass of building human context of the problem. The real benefit here is the ability for the human swe to quickly context switch between problems and domains.
> > > > 
> > > > But again: the agent can only move as fast as we can review code.
> > > > 
> > > > **echelon** · [2026-02-20](https://news.ycombinator.com/item?id=47088795)
> > > > 
> > > > And they're not the only company doing this.
> > > > 
> > > > Financial capital at scale will begin to run circles around labor capital.
> 
> > **ndr** · [2026-02-20](https://news.ycombinator.com/item?id=47087312)
> > 
> > Soon indeed. From today:
> > 
> > \> Cardiologist wins 3rd place at Anthropic's hackathon.
> > 
> > [https://x.com/trajektoriePL/status/2024774752116658539](https://x.com/trajektoriePL/status/2024774752116658539)
> > 
> > **jobs\_throwaway** · [2026-02-20](https://news.ycombinator.com/item?id=47089985)
> > 
> > It's all human-reviewed, not vibe coded
> > 
> > **handfuloflight** · [2026-02-20](https://news.ycombinator.com/item?id=47087057)
> > 
> > Vibe coders do not know what linting is.

> **\_ache\_** · [2026-02-20](https://news.ycombinator.com/item?id=47089190)
> 
> Why they is so many 404. Linked to mp3 ?! What was this feature ?
