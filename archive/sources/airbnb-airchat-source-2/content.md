> Archived source snapshot  
> Source ID: `airbnb-airchat-source-2`  
> Original URL: <https://getdx.com/podcast/beyond-the-cli-agentic-ai-for-async-workloads-and-non-developers/>  
> Final URL: <https://getdx.com/podcast/beyond-the-cli-agentic-ai-for-async-workloads-and-non-developers/>  
> Title: Beyond the CLI: Agentic AI for async workloads and non-developers  
> Captured at: `2026-08-31T17:38:48Z`

---

In this session from DX Annual, Christopher Sanson, Product Lead, AI Developer Experience, and Madison Capps, Engineering Manager, Infrastructure at Airbnb, challenge some of the most common assumptions about AI. Is AI primarily about replacing humans? Do organizations need mandates to drive adoption? And are the productivity gains really as small as some studies suggest? Using examples from Airbnb's own AI journey, they share how the company achieved widespread adoption of agentic AI through AirChat, community enablement, and internal tooling rather than top-down mandates. They also discuss the impact AI is having on developer productivity, how non-developers are increasingly using coding tools, and how teams are rethinking product development in an AI-first world. Finally, Madison takes a deeper look at the infrastructure powering Airbnb’s AI strategy, including AirChat CLI, the AirChat SDK, and AirChat Remote, along with the company’s vision for asynchronous agent workflows and the next generation of AI-powered development.

## Show notes

### AI adoption at scale

- **Successful AI adoption does not require mandates.** Airbnb achieved 97% weekly usage and 90% daily usage of agentic AI tools among engineers without tying adoption to performance reviews or quotas. Christopher argued that the best adoption comes when developers choose to use AI because it genuinely helps them work faster and better.
- **Treat internal AI tools like products, not internal infrastructure.** Airbnb built a recognizable brand around AirChat, invested in onboarding and workshops, created internal marketing materials, and focused heavily on user experience. That product mindset helped turn AirChat into a company-wide platform rather than just another engineering tool.
- **Community-driven learning scales better than centralized training.** AI champions, train-the-trainer programs, hackathons, workshops, and active peer-to-peer learning channels allowed knowledge to spread organically across the company. Over time, the AI community became larger and more active than the team managing the platform itself.

### Productivity gains are accelerating

- **Developers are spending more time actively coding.** Christopher challenged the idea that engineers only spend a small percentage of their time writing code. As coding becomes faster and easier with agentic AI, developers can spend more of their week building software rather than working around implementation bottlenecks.
- **The most active AI users see the largest productivity gains.** Airbnb found that developers who spent four or more hours per day working with agentic AI dramatically increased their output. The relationship between AI usage and productivity became stronger as engineers learned how to incorporate agents into their daily workflows.
- **PR throughput increased by 65% after the introduction of agentic AI.** Airbnb’s data suggests that productivity gains extend well beyond the single-digit improvements often cited in industry studies. Developers who heavily embraced agentic AI moved from industry-average output to some of the highest throughput levels measured internally.
- **AI-authored code is becoming mainstream.** Roughly 59% of Airbnb’s code is now primarily authored by AI, and more than half of developers report that AI generates the majority of the code they work with. Christopher argued that this shift is happening far faster than most organizations realize.

### AI is spreading beyond engineering

- **The addressable market for AI is much larger than developers alone.** Airbnb initially expected adoption to level off around its engineering population. Instead, usage continued growing as product managers, designers, finance teams, and operations teams began integrating agentic AI into their work.
- **People will learn new workflows when the value is obvious.** Some non-engineering teams adopted VS Code and terminal-based tools simply because they provided the best access to agentic AI capabilities. Rather than resisting technical tools, employees were willing to learn them in exchange for meaningful productivity gains.
- **Domain experts are increasingly building their own AI-powered solutions.** Airbnb’s internal platforms allow teams to create specialized applications tailored to their own workflows. This shifts more problem-solving into the hands of the people closest to the business problem.

### Rethinking how work gets done

- **Many existing processes were designed around expensive software development.** Product reviews, lengthy requirements documents, and sequential handoffs evolved in a world where implementation was slow and costly. AI changes those economics and creates opportunities to redesign workflows from first principles.
- **AI enables faster movement from ideas to prototypes.** Rather than spending weeks refining specifications before building anything, teams can generate multiple prototypes quickly, test ideas earlier, and iterate before committing significant resources.
- **Smaller teams can collaborate earlier and move faster.** Airbnb sees opportunities to reduce handoffs between product managers, designers, and engineers by bringing teams together earlier in the process and using AI to accelerate exploration and execution.

### Building for asynchronous AI

- **Current agentic AI tooling still creates friction.** Managing multiple sessions, handling long-running tasks, maintaining context, and switching between workflows remain cumbersome despite major advances in model capabilities.
- **The next frontier is asynchronous agent workflows.** Rather than interacting with a single agent in real time, developers are increasingly orchestrating multiple agents working in parallel, often across long-running tasks that continue without constant supervision.
- **Airbnb is investing in infrastructure, not just models.** AirChat CLI, migration tooling, the AirChat SDK, and AirChat Remote were all built around the belief that future gains will come from workflow orchestration, platform capabilities, and developer experience as much as from improvements in foundation models.

### Preparing for an AI-first future

- **Organizations should build for where developer workflows are heading.** Madison described Airbnb’s approach as continuously forecasting how engineers are likely to work in the near future and investing in the infrastructure required to support those workflows before they become mainstream.
- **AI-first architecture will become increasingly important.** As throughput rises and more work is delegated to agents, teams will need stronger guardrails, scalable platforms, and systems designed specifically to support AI-assisted development.
- **The biggest bottlenecks are shifting away from code generation.** As AI reduces implementation costs, constraints move elsewhere in the system. Coordination, validation, infrastructure, and workflow management are becoming the new challenges organizations must solve.

## Timestamps

([00:00](https://www.youtube.com/watch?v=lL9-yATNAo0)) Intro

([01:37](https://www.youtube.com/watch?v=lL9-yATNAo0&t=97s)) Myth #1: AI is about replacing humans

([03:22](https://www.youtube.com/watch?v=lL9-yATNAo0&t=202s)) Myth #2: You need mandates to drive AI adoption

([05:21](https://www.youtube.com/watch?v=lL9-yATNAo0&t=321s)) AirChat, agentic AI, and Airbnb’s adoption strategy

([08:07](https://www.youtube.com/watch?v=lL9-yATNAo0&t=487s)) Myth #3: AI has little impact on productivity

([09:33](https://www.youtube.com/watch?v=lL9-yATNAo0&t=573s)) Airbnb’s increase in coding time and PR throughput

([14:20](https://www.youtube.com/watch?v=lL9-yATNAo0&t=860s)) Myth #4: AI coding tools are just for coders

([15:39](https://www.youtube.com/watch?v=lL9-yATNAo0&t=939s)) How non-developers are using coding tools

([17:24](https://www.youtube.com/watch?v=lL9-yATNAo0&t=1044s)) Rethinking product development in an AI-first world

([20:30](https://www.youtube.com/watch?v=lL9-yATNAo0&t=1230s)) Myth #5: Vibe coding isn’t coding

([22:16](https://www.youtube.com/watch?v=lL9-yATNAo0&t=1336s)) Unsolved problems in agentic AI tooling and how Airbnb is addressing them

([26:30](https://www.youtube.com/watch?v=lL9-yATNAo0&t=1590s)) Airbnb’s overall AI philosophy in practice

([29:15](https://www.youtube.com/watch?v=lL9-yATNAo0&t=1755s)) Using agentic AI to accelerate code migrations

([30:18](https://www.youtube.com/watch?v=lL9-yATNAo0&t=1818s)) AirChat SDK: How Airbnb enables teams to build AI-powered applications

([33:17](https://www.youtube.com/watch?v=lL9-yATNAo0&t=1997s)) AirChat Remote and asynchronous agent workflows

([36:07](https://www.youtube.com/watch?v=lL9-yATNAo0&t=2167s)) Predictions for what’s next

Listen to this episode on:

- [Spotify](https://open.spotify.com/episode/1YS3gOoRwnZBFM10ElhybO)
- [Apple Podcasts](https://podcasts.apple.com/us/podcast/beyond-the-cli-agentic-ai-for-async-workloads-and/id1619140476?i=1000773730152)
- [YouTube](https://youtu.be/lL9-yATNAo0)
- [Overcast](https://overcast.fm/itunes1619140476/)

## Transcript

Christopher Sanson:

Hello, everybody.

Madison Capps:

Afternoon.

Christopher Sanson:

All right. Nice to meet everybody. My name’s Christopher. This is Madison. I’m going to kick us off, talk a little bit about what we’ve been doing with AI at Airbnb, and then Madison is going to come on and actually talk about what’s actually been happening from an engineering perspective. All right. So we’re going to talk a little bit about what we’re doing with non-developers and sort of the next wave of what’s next along with some agsynchronous AI stuff. But I don’t know, the vibe, it’s kind of been doom and gloom so far. I don’t know. This morning was like, you read the news and it’s like, “AI is taking our jobs,” and then, “AI actually isn’t making us that more productive.” And by the way, those are complete opposite sentiments. So I don’t know which one is true, but I don’t know, “It costs too much and we need mandates for people to adopt it,” and things like that.

And I read these headlines and stuff like that. And I think what we’re seeing inside of Airbnb is kind of the opposite. We’re seeing it unlock new levels of productivity. These are the most wildly successful tools we’ve ever rolled out before. So I wanted to take a minute to talk a little bit about what we’re seeing and I’d say Airbnb and actually share some numbers with you. And I want to do it by going through a couple of myths that you do see in the news a lot that I think have kind of been true, but I think this is all going to change very, very fast 'cause especially since December, January, probably like a lot of you, a lot of the old metrics have just completely changed. So I kind of want to walk through a little bit of that with y’all today. And the first myth I want to really tackle is that AI, the value of AI is all about replacing humans.

Actually, I loved what Jennifer was talking about this morning around setting the tone and the culture around AI tools feeds into everything else that’s happening in terms of adoption, in terms of utilization. And again, I don’t know about you guys. I’ve been on developer platform for a long time and our CFO was never asking us what we were doing. You know what I mean? Finance did not care about PR throughput, but now all of a sudden they’re sort of, “Hey, what’s going on with AI productivity?” We’re like, “Why are you asking us this?” But people can kind of check that vibe. I think the way I like to think about is Steve Job has this great quote about the computer. Some of you probably know, he called it, “A bicycle for the mind.” A lot of people probably know that quote. There’s actually … I don’t know if you know the full story though behind it.

There was a little more to it. He actually talked about it in the context of a study. There was a scientific study that looked at the efficiency of motion, of locomotion. How much energy did animals take to move one kilometer versus humans? And what they found was that animals were way more efficient. Humans were like dead last. The condor uses way less energy to travel one kilometer than a person. I don’t know why they had to do a study. I could have just told them that. I don’t know why they need to figure that out, but they did it. And then what happened is that somebody said, “Okay, that makes sense, but what if we put a human on a bicycle and did that same comparison?” And a human on a bike blew the animals away. It went from last to first, and that was his context.

He said, “Computers are like a bicycle for the mine.” And I love it. And I think we’re seeing that all over again. We like to call it sort of like if that’s a bicycle, AI is kind of like a motorcycle for the mind. We’re seeing people achieve levels of sort of creativity unlock and productivity that really wasn’t possible before. The second myth is around, I think, mandates to drive AI adoption. So you probably all read Pragmatic Engineer, you read the DX blogs, you know who they are about measuring token usage and performance reviews. And I think it was really encouraging that most of the folks this morning have said, “We don’t really do that, but it definitely seems like it’s pretty prevalent.” And we haven’t done any mandates inside of Airbnb. It’s all been organic adoption. And I’m excited to say a lot of people have said that adoption seems pretty high.

We actually, we wanted to share some numbers. 97% of active engineers inside of Airbnb are using Agentic AI on a weekly basis so far, 90% daily. And this is like agentic AI. So it’s not just chat, it’s nothing like that. It’s Claude Code, it’s Codex, they’re using Agentic AI. It’s almost totally ubiquitous. And this adoption has been like nothing I’ve ever seen. It’s really happened just, I mean, these tools came out a year ago. So really we’ve gone from basically 0% to 97% adoption in less than a year. And I want to sort of-

Christopher Sanson:

… Adoption in less than a year. And I want to share a little bit about what we did to encourage this. I think I was at the Netflix talk earlier. It was very similar. We saw a similar playbook to what you guys have been doing. But the first thing we did was, you ask a product guy, I’m going to say it was all about the product. We launched an internal product called AirChat and we built a brand around it and we treated it like a product. And AirChat was our… It’s like our internal AI harness before that was a term. And it makes AI work really, really well inside of Airbnb right out of the box. So we handle authentication as permissioning. We load default MCPs, integrates, it knows how to operate inside of Airbnb. We created t-shirts, we ran workshops, and this became a rallying call internally. Everyone knows AirChat. It makes it easy to share and talk about. And it really helped the word of mouth and positivity around it.

The other part is that we’ve been doing this for a while. So we’ve been on this AI journey for three years now. So like many of you, we rolled out some of the initial enterprise vendor solutions, like the auto complete stuff. We were pretty quickly realizing that that wasn’t going to get us where we wanted to go. We didn’t have access to the latest models. It didn’t work across all the IDEs that we use. So that’s when we first launched AirChat as a series of IDE plugins in JetBrains and Xcode, backed it up by the latest models, got the ball rolling. And then like many of you, we did things like helping assist and speed up AI migrations. We launched agentic AI pretty early last year when that first started rolling out. And so basically we’ve had this long runway of people… People have talked about before, but you get on the learning curve. We’ve had a lot of time for people to adopt, to learn, to embrace these tools. And we’ve been pretty lucky to be early at each new wave.

The other thing is that we made it work really, really well inside of Airbnb. So we really spent a lot of time building out our plugin ecosystem and marketplace. This is an internal browser that I built myself. I vibe coded it in three days using AirChat. I haven’t been an active coder in 10 years. And in the old days, I would have had to write a PRD and get this on the engineering roadmap, but it would take three months, and I did it in three days. But you can see, we blurred out, but essentially this connects to everything that we use internally. And this is all community managed. And so it’s a combination of… There’s some managed centralized tasks by different organizations, but then there’s a lot of experimentation. There’s a lot of skills, a lot of instruction markdown files that people are using. And we really encourage that as well as we all learn.

The last piece that I think has been even the most critical to all of this has been the peer-to-peer learning and the community enablement. So I went back and looked up the very beginning of our AI for dev productivity channel, and we launched it about three years ago, asking about some slides for a deck around how we’re using AI in August of 2023. So God knows what was in that deck. But nowadays, we never asked everybody to join this. It wasn’t ordered or anything like that. And it’s essentially basically every developer inside of Airbnb. I think it’s one of, if not the most active Slack channel. It’s outgrown the AI team itself. People are contributing and sharing knowledge. And this is just one example. We’ve done a lot of events like hackathons and learnings. We also have an AI champions program. We did a train the trainers program where we taught AI champions to run their own workshops. And this has really helped us get to that 97%.

All right, myth number two, very topical. AI has minimal impact on productivity. So I’m going to share some numbers. You saw the news. Justin, I think you published this a month ago, you heard it this morning. Productivity gains are around 10%, 7%, 8%. And the main argument that you hear around this, which I guess makes sense is that, well, engineers don’t actually spend that much time coding. You see various estimates from like 25%, 20%. I think the number this morning from Microsoft was 14%. It’s data. I’m not going to argue with the data, but I think this is about to change in a big way. Saying engineers only code 20% of the time, it’s like saying golfers only hit the ball 20% of the time. They’re walking the course. What are they doing? They’re not always hitting the ball, but it’s the whole point.

I think what a lot of what a golfer will do is they pick their club, they line up the hole, they check the wind, they line everything up. And why do they do that? They do that because they have to get it right. You know what I mean? It’s a high stakes motion. So I think all these meetings, coding is kind of similar. We have all these meetings, we have all these reviews, we have all these docs. And I think a lot of it is about getting the code right. You know what I mean? Because it’s expensive to change. It’s an expensive, time-consuming operation. But that was how it used to be, right? Coding now is cheap and fast and easy. And what we’re seeing is that time spent coding is going way, way, way up. I think you need to lean into this. If you’re still in meetings all day and you’re still having people code 15% of the time, you’re leaving a ton of productivity gains on the table.

So this is a metric that we track internally that looks at how many hours per week they have an active agentic AI session. And this number has been going up and up and up, and this is much higher than 20%. And this is the median developer. If you look at the top 10% developers, they have an active agentic AI session running more than there are hours in the week. Because coding used to be about hands-on keyboard time. It used to take a long time to get into the flow. It was hard to do small bite size changes. All of that has changed. You can be in a meeting and actually be coding in the background because your agent is using it.

So I think what we’re seeing is that people are actually spending more and more time producing code. So what has that meant for PR throughput? The big number, the hot topic. Our PR throughput inside of Airbnb is 65% higher than it was before we introduced agentic AI. So this is a lot more than the seven or 10% that you may see. And this is using true throughput, which is the DX metric that takes PR complexity into account. And if you look at the growth, it started growing a little bit last year. And so we were also in that 10 to 20% number, but starting at the beginning of this year, this has really, really gone just through the roof. And if you look at this, this is I guess what someone who knows more than me would call like a longitudinal study, I guess. But these same developers had industry average output a year and a half ago, and now they’re closer to the top band.

And we actually, we went a step further. We drilled into this a little bit to see, “Okay, this is going up. Is this actually being driven by AI?” And if you break it down… So many people are using AI inside of Airbnb that daily usage wasn’t granular enough. So we asked people how many hours per day they’re using agentic AI. And we broke it down to one to four, four to six, six and more. And what we found is that the sweet spot seems to be around four hours a day. People that were using agentic AI for four hours or more per day have seen PR output more than double from before AI.

And the four-hour day people also are seeing growth, but not nearly to the same degree. And again, if you look at the more than four hour people, these groups were identical two years ago. It’s not that these were more prolific developers before either. These basically had the same output and the only thing that’s changed is how much they’re using AI. And again, this has really just exploded. And again, to put context on this, at least in our group in DX, the industry P90 is around here. It’s around 2.7 true throughput PRs. So you can see these developers went from industry average output to off the charts. I don’t know, 1%, top 0.1%, pretty much just from agentic AI usage.

Another way we look at this is AI authored code, another great DX study. So again, this was also another DX number that they published. For the industry average is around 27%, I think, as of Q1 for AI authored code. Inside of Airbnb, we’re double this. So we’re closer to 59% today. So more than half of code inside of Airbnb today is primarily authored by AI. And they tell us that they do these custom benchmark groups. There’s 20 peer companies. This is, I guess, a bit of an outlier where we’re at the top of this group.

Lastly, time savings. So in terms of time savings, developers say they save around six hours a week due to AI coding tools, basically. Again, this is also number one, and frankly, this is under counting it because the question was, we broke the question. The top option was eight hours or more per week, and that was the number one response. So over a third of developers told us they were saving at least a day a week because of AI, which was the biggest group. So we don’t actually really know what the upper bound is.

And I think my prediction is that at the next one of these events, these numbers will look quaint for everybody in this room. I think a lot of you are already seeing this, but the tools are getting so much better. People are getting so much better at using them. I think that every estimate we have made on terms of AI usage or AI growth has been wrong. We’ve undercounted. And this doesn’t really seem to be changing. New models are coming, new harnesses are coming, new capabilities are coming, people are getting better at this stuff. I think that this is going to come and come very, very fast for a lot of us.

All right. So I’m 20 slides in. I haven’t even gotten to the topic of the talk. I apologize. So I want to talk about the other one is AI coding tools are just for coders. They’re called Cloud Code. It’s called Codex, right? It’s for coders. I think anyone who has played around with these tools realizes that they’re much, much more capable of that. So something really funny happened that we weren’t expecting. We thought our addressable market for these tools was our developers. So we have around 2,000 or so developers inside of Airbnb. And as our AI tool usage went up and up, we’re like, “Okay, we’re going to get to about the size of our active developers, that’s our TAM, and then it’s going to flatten out.” And it didn’t. It just kept going. So as of now, we have about double the amount of users of agentic AI tools as we do active developers, and we were not really expecting this.

So what happened? Well, turns out a lot of folks had the chance to go home over Christmas break, finally have a chance to play around with these models and said, “Oh, snap, these got really good. When did that happen?” The last time I tried this, didn’t know how many Rs were in strawberry or whatever that whole thing was." And everyone was like, “Wow, this got really, really good.” So everyone came back to work essentially just demanding to use them in their own day-to-day work. And the way they’re using them is for everything. And what really surprised us was that they’re actually doing this in the terminal. So they just started using the terminal. Our finance team, the director of product and finance put together a 30-page onboarding guide to VS Code. So he has onboarded the whole ops and finance team to VS Code where he has AirChat running in the sidebar. He has a file browser with markdown files. This was not in our PRD for AirChat with like, “The finance team will learn to use VS Code.” That was-

Christopher Sanson:

For AirChat with the finance team will learn to use VS Code. That was not happening, but that’s what they’re doing. And they’re using it for everything. They’re using it for prototyping, for data research as a personal assistant. They’re building all sorts of really cool tools. And we did one thing that turned out to be really powerful that Madison will talk about is we built an SDK around this stuff.

So we built an SDK for AirChat so that anyone internally can build their own AI powered applications. And people are going really deep on this and building things we never would’ve thought of before. So just some examples like Pascal is an internal product planning tool that the product managers and designers use to go from idea to concept brief that does a ton of market research, looks at our roadmap, pulls in business objectives and puts it all together.

We have a prototyping tool for designers so they can rapidly vibe code prototypes to have higher fidelity concepts. I mentioned the operation folks in VS Code. The other one that’s been really popular is data analysis. So the data platform team built this whole data query tool with guardrails that queries business data. These have been really, really popular.

I think what’s really kind of most exciting, I think a little bit about this and the opportunity is stepping back a little bit. If you look at every technology, every new technology, the first phase is just applying the new technology to the old way of working. You know what I mean? This is sometimes called the horseless carriage effect, because the very first automobiles were basically just carriages without the horse.

It was called horseless carriages. The first movies were like people just pointed cameras at stage place. And in tech, the internet came out. The first websites, they were just like paper brochures. It was like the front page of a newspaper. Remember when mobile devices came out, the first websites were full HTML websites and you had to scroll in and hit the dropdown menu, and it took a while for people to figure out the newsfeed and scrolling.

And I think that’s what’s really exciting about this is we’re hoping to speed run that part a little bit. We kind of want to rush ahead. We look ahead, it’s a bit of a fog. It’s like wheels on luggage. It’s sort of obvious after the fact, but how did that take so long? So we’re starting to rethink from first principles on the product side of like, how do we do what we used to do in an AI first way? And so I think they were talking about prototyping earlier, and this is like a big one for us as well.

In the old way of working, despite all of our lip service to agile, like iterative development, it tends to be kind of waterfally. A product manager writes a long requirement stock, hands it off to a designer who creates mocks, who hands it off to an edge to create a prototype. They go back to the designer, the dentist are like, “Oh, well, now that I see it live, that’s not quite what I want.” And the product person was like, “Well, that’s not really what I was envisioning.” And it kind of takes forever.

In an AI first world, we’re kind of flipping this on the head in a couple ways. One is same thing, no more long requirement docs. Let’s just create a shorter concept brief that gets the key elements in place and go right to prototyping. Prototyping looks a lot more similar to what eventually you’re going to launch. It’s higher fidelity. Let’s just start there. Again, let’s go crazy. We don’t have to build one prototype. We can build five prototypes. We can build 10. It’s cheap. It’s really easy.

The other thing is to be way more collaborative earlier on. So instead of this sort of like PM is responsible for this designer and we really want to create smaller pods, like smaller teams moving faster is sort of our mantra and collaborating early on. And then of course, number three, using AI. Leveraging AI to create the concept brief, create the prototype. And even going further, things like, we talk to these teams and that they often say, well, the hard part actually isn’t creating these assets sometimes.

It’s just keeping everything coordinated because you create the prototype, you learn something, you update that, but the doc doesn’t get updated. And then when you go to review, nothing is in order. We can use AI for that too. We can have AI project coordinator, create a Jira ticket, create everything in sync. So this is kind of early days, but we’re seeing a lot of real promise here and it’s like something that I think is going to help transform. Again, I think they talked about the north star of idea to value.

We have sort of a similar concept. As coding becomes less of a bottleneck, it’s going to be these other steps in the pipeline that become more and more critical. So last one, maybe the most controversial, I don’t know. Vibe coding gets sort of a bad rap. Vibe coding, it’s not coding, it’s AI slop, yada-yada. Yeah, no, vibe coding is the future of coding. This is how engineers are coding nowadays. So I mentioned AI authored code.

So same group of people inside of every 28% of developers said that AI primarily authors 80 to 100% of their code already today, which is a pretty big number. But the speed at which this has happened is kind of mind-blowing. So this was our last DX survey in October. 3% of people said that AI authored 80 to 100% of their code, and you can see the green, but this totally flipped. Six months later, it’s 28%. Six months ago, more than half of people said AI authored zero to 20% of their code.

Now that number is 11%. More than half of people now say AI authors more than 60% of their code. And again, these are the worst the tools will ever be. This is only accelerating. We’re just at the beginning of this. Andrej Karpathy sort of famously summed this up earlier on. He was like, “This is the biggest change in programming and it happened in a matter of weeks.” And I think if this hasn’t happened already in your organization, it’s coming very, very quickly and soon. And I think there’s a lot of concern right now about AI adoption, AI productivity.

Yeah, that is a concern, but skip a step because I think you’re going to have a lot of problems very soon about overwhelming code review. You’re going to have a lot of other problems on the other parts of your system because I think this is coming no matter what you do. The other part of this is code quality, right? So we’re all concerned about that. We’re moving faster, but is it coming at the sacrifice of quality? And so far that hasn’t really showed up for us.

Our change confidence in Code Maintainability scores are basically flat. Our change failure rate has actually gone down over this time. Code Maintainability is actually improved as a sentiment. I think largely because we’ve invested a lot in migrations and tech debt, so I think our code base is healthier. So this is something we’re watching closely, but so far we haven’t seen this kind of concern or trade off around quality, but we’re also actively working to maintain that as well.

I think what’s really happening is that if anything, we’re not actually fully unlocking the potential of this because of the tooling. The tooling is actually holding us back. It’s not even the quality of the models or the harnesses at this point, but there’s some real challenges around the tooling itself to kind of unlock this next phase. So we talk about this as well as asynchronous AI. So we started with chat where you ask a question, get an answer.

We’re in kind of the agentic phase now where you ask an agent to do something for you. But we’re moving very, very quickly to this world of async AI where you’re managing multiple agents and we’re already sort of seeing it with power users, but there are a few kind of key gaps I think right now in the tool chain. One is that it’s still really, really hard to manage multiple sessions. If you’re in the terminal, you have a couple tabs open, it’s kind of a nightmare.

You don’t really know when you need to jump back in or it needs your attention. There’s still not a great user experience about this. It’s also really hard to run sessions remotely still. There’s some been recent feature launches, but I think this is largely unsolved. You don’t want to have everything tied to your laptop. You want to shut it down, you want to go to bed, you want to get on a plane, you want to pick it up from your phone.

You really want to be able to run these things remotely with all the right permissions and security in place. And then lastly, chat I think is underrated as a UX. It’s been pretty good, but it isn’t always the best. You run an agentic session, you have things running in parallel, you jump back in and you’re like, “Okay, what was going on? What was I talking about?” A lot of times the operations and engineers do are pretty standard.

It’s like rebase and merge this branch. Open a PR based on these comments with these fixes and submit a fix. This doesn’t need to be a chat. You can just have a button. So we’re working on something internally called AirChat Remote, which is sort of our next generation version of AirChat that addresses a lot of these questions. So right out of the gate, workloads run on something internally called Airdev Workspaces, and Madison will give you the real scoop on all this stuff.

So that runs off of the laptops. There’s a whole UI built around managing multiple sessions in parallel. So you can very quickly and easily see each session, what the status is, what kind of tools are running, which ones need attention, so you can kind of jump in and out. And then lastly is that we do have these dynamically created shortcuts. So if we have a pretty good idea of what you need to do next to keep this thing moving, we’re just going to expose that as a button.

All of these are backed by full agentic sessions you can jump in and out of, but the idea here is that we’re really sort of leaning into what’s really possible. And this is live. So this is an EAP internally. We have like 50 users and I don’t want to scare people, but the PR throughput for these folks is like 3X higher again. So I think the wave is coming and it feels sometimes like we’re behind, but I don’t think we’re going to feel that way for very long.

So just to close up, I want to sort of think about this as AI truths, right? AI is all about augmenting humans and unlocking creative potential that I think is pretty unprecedented. The one word we hear the most is fun. People are having more fun than they’ve ever had before. You can get to high adoption just through organic means, right? And honestly, that’s what you want. You want people voting with your feet.

You want missionaries, not mercenaries. We’re starting to see really significant impact on productivity from not just engineers, but non-engineers as well. And more and more, I think this is going to look like a step removed from the code itself where you’re managing async teams dynamically. And I’ll hand it off to Madison who’s going to go talk more about that.

Madison Capps:

Thanks, Christopher. All right. So how did we … Sorry, too long not talking. Okay. How did we get here? I won’t have time to dive really deeply into too much of the technical detail, but I do want to go over some of the goals, some of the requirements we set for ourselves, as well as a little bit of the architecture. So you’ll get a high level sense.

I do want to start with our overall philosophy though. One thing that we’ve focused on this entire time is not starting from a particular tool that we want to bring in. It’s more trying to predict how developers are going to work in the future, in some near point in the future, as far as we can predict out, seeing what we can reuse, seeing what we have to invest in ourselves to build, and then as the ecosystem changes, we do this exercise over again.

We set a new North Star vision that we’re heading towards and we continue to do that. This has left us with a few ways of working that seem like they might be in opposition a little bit, but that tension actually helps us balance for short-term and long-term development at the same time. We are trying to be about four to six months ahead of what you can get from the industry out of the box. And so if we can build something that will provide value in that time with a reasonable lift, we go ahead and do it.

That does mean that we have to be open to swapping out pieces with external solutions as they come along. And so we try to build the fundamentals in a very modular way so we can do this. That means we don’t always have the fanciest or shiniest things immediately when they’re available, but that does also mean that we’re trying to minimize churn on a paved path.

So what we build, we make sure it’s good, it’s solid, and we tell people, “This is the way that you should do things.” And we don’t change that on them too often. That doesn’t mean that we don’t like innovation though. So we really try to embrace community, innovation and developers and teams unblocking themselves, seeing the ways that people actually go about-

Madison Capps:

… teams unblocking themselves. Seeing the ways that people actually go about unblocking themselves is a very helpful signal for us in figuring out what our paved path should actually look like. And so often these innovators or first requesters become our really close partners and actually developing the paved path moving forward based on some of these things they tried for themselves. So unless there’s a security implication or a cost implication, we try to let people feel free to experiment. Christopher’s already talked about this evolution, but I do want to zoom in to when we started to bring agentic AI to Airbnb because that’s the point in time when AirChat went from being an IDE plugin into really being more of an ecosystem. So one of our goals after we did a bunch of third party evaluations was really to find a way to provide unified capabilities across all our surfaces.

Our developers really didn’t want to give up their IDEs. They loved it. We wanted to meet them where they were at. So we introduced something that we called AirChat CLI. This is a light abstraction wrapper around coding agents and passes all of the APIs through a single unified gateway. So we get cost control. We can see usage metrics in a very standardized way. But more than that, it allowed us to call into it from our various IDEs, as well as provide this new CLI option for people to do coding.

One of the things that, as Christopher already mentioned, people really like to do with agentic AI when it first came out was look at migrations. Migrations are very toilsome. For small or relatively simple migrations, this was pretty straightforward. You could just use a coding agent, handle it all yourself. But when you start getting into more large or complex migrations, we found that a structured approach actually worked a lot better in order to help manage the unpredictability of AI. So we developed a framework that allowed people to use a sequence of steps on each target where you would validate, transform, validate again, and do that in a loop until that particular step passed. Now this has worked really well. We have dozens of migrations that have happened. We save on average between a few months or up to even seven years per migration. So it’s about a 5X speed up, which is great.

However, and as Christopher mentioned, people want to be able to close their laptops, walk away. They don’t want to babysit this. We didn’t really have a great solution for them at this time. We’ll come back to that. All right. Moving on, we’ve gotten into what we’re calling the AirChat SDK. The goal, as we quickly saw, as individuals became comfortable with agentic AI for their own use cases was, how do I empower other people to be able to operate better in my domain of expertise? And so people really wanted to build tools that they could share with other developers to help them work faster or better in their particular domains.

You can enable sharing of MCPs or skills or plugins, et cetera, but they wanted more than that. They actually wanted the ability to create their own customized UIs on top of this that would live in a web interface. So we introduced the SDK. A couple technical requirements for this. We really wanted a language agnostic protocol for communication and data modeling so people could use this in whatever language they were comfortable. We wanted bidirectional communication also so that we could have this true back and forth conversation with the agent, even from the web application.

And we really wanted people to be able to configure prompts, tools, hooks, anything that people needed to customize for the particular application is something that should be able to happen through the client.

Datako, as I already showed, this is one of our data applications that people have built has high hundreds of daily active users, which is fantastic. It’s quickly becoming one of the primary ways to actually look at data. You don’t have to know what tables you’re looking for. You don’t have to know where the data lives. It’s probably the most successful application so far that’s been built on top of our AirChat SDK, but we have about 40 of these projects that are now stood up internally. It’s pretty fantastic because we’ve taken the time that it takes to build one of these from a day or two down to about two to four hours. So a lot of teams are starting to feel really empowered to create things that actually fit their individual needs.

All right. This takes us to today. When we start talking about paralyzed and async AI. So we have a bunch of goals now. People have gotten very comfortable using agentic AI and they have new needs. We have people that are doing parallelization on their own. They’re opening multiple terminals or trying to set up get work trees. It’s really cumbersome for them and they never know which ones actually need their attention at any given moment. People are also coming up with all of these various use cases for where they might actually call agentic workflows. They’re things like triggering from an on call support channel in order to have some agentic triaging happening and actually fixing things, fixing things on PRs when they fail, or really just starting workflows from Slack and then being able to check on it later. So there’s lots of interfaces people would like.

There’s also a desire to have these long-running non-local environments that persist context, particularly referring back to the migration case. This is one of the main goals that we are hoping to solve. People can run these things, they can walk away, they can come back, they haven’t lost their place. Which takes us to this grand goal of trying to truly offload work from developers. What things can we run asynchronously in the background and autonomously? Turns out that actually solving all three of those previous goals is needed for solving this as well. So as Christopher mentioned, we’re really leaning into the AirChat remote idea. This is really just a starting point, WebUI. The idea of this is supposed to be that you can see everything. And for some nomenclature, we’re calling parallelized sessions, sessions. And we’re calling asynchronous workflows tasks, but you can manage both of them through the same WebUI.

But the magic is really probably in the architecture. So we’ve designed this so that it connects to and sits on top of all of the previous pieces of the AirChat ecosystem, which is why I ran you through all of those. We hope that one day there’s going to be more vendor solutions that we can kind of slot into pieces here so we’re not having to maintain this forever. But in the short term, this really provides us a powerful way to be able to support multiple agents, to be able to have it not run on people’s laptops directly and to do parallelized synchronous workloads as well as the asynchronous ones.

AirChat API is the central coordination point of all of this. It’s where all of the client interactions come from. You can do WebUI, you can do Slack, you can do from the SDK apps, which is going to be pretty fantastic. It handles the authentication, the lifecycle management, and it streams events back to the clients. It takes us to our worker pool. Our worker pool is built on top of something called the AirDev platform. So we have infrastructure for developers at Airbnb to allow them to spin up their own customized workspaces or cloud IDEs in a way that is remote. They’re pre-configured for fast development on our major monitor repos. So out of the box, they work very nicely. So our strategy today is to re-leverage these cloud environments, not only for paralyzed coding agents because they’re really easy to configure and stand up, but also for async agentic flows because they do provide sandboxing.

So even though each workplace has access to our \[inaudible 00:42:53\] tool chain, build dependencies, source control, everything an agent might need to be successful, they are network isolated from production services and user data. Last but not least, we’ve got the agent, Damon, runs one per worker. It’s really responsible for configuring the agent tool loop of a task on a workspace and starting its execution. It wraps agent runtimes behind ACP. For interactive sessions, we go back through the remote API so we can really stream the responses back to clients without needing Damon connections directly. Christopher mentioned this is still an Alpha. We’re still doing a lot of additions to this. I think right now, as I’m speaking, someone is adding in the ability to run these things on a schedule so that UI should exist by the time I get back to the office, which is pretty phenomenal because somebody put up a design for it this morning.

So we can build faster than we can align, I think sometimes. We also want to build a migration platform in here to make it easier to use our migration framework directly, since we know this is one of sort of the primary points that people will be able to find value from it, as well as handle more non-deterministic migrations. So big picture, what’s next? Magic eightball would probably say, response fuzzy, ask again later. This is due to us projecting our vision out into the future. We’re about at the point where we need to do that exercise again, but we do have a few predictions. We think that AI first architecture is going to become increasingly important. We do think that there’s going to be increasing importance also on guardrails as code goes through. Throughput is going to accelerate. The more we can do in automatedly checking that this is great, is going to help us reduce bottlenecks.

And we also think that there’s an increasing importance in scale and resilience of the surrounding infrastructure. I think as someone mentioned earlier this morning, the more goes into the front of the pipe, the more needs to come out the back of the pipe, the whole pipe needs to expand to accommodate that. So as for specifics, we’re still figuring that out. If you’re working on something similar, if you have a vision of what’s next, we’d love to chat with you, but that is it for us.

Justin Reock:

Thanks, Chuck. Thank you very much. Unfortunately, I know I said we’d have time for Q&A, but that was so much good content. We filled up our time and I want to make sure that we’re having enough time for Interstitial, but thank you both so much. I would encourage you. There were some great questions there in the chat, so I really would encourage you to go find Christopher and Madison, ask them yourself.

Christopher Sanson:

Sure. Happy to.

Justin Reock:

Thank you so much. That was great.

Madison Capps:

Thank you folks.
