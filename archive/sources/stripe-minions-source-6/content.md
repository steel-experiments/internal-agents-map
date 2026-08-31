> Archived source snapshot  
> Source ID: `stripe-minions-source-6`  
> Original URL: <https://news.ycombinator.com/item?id=47087114>  
> Final URL: <https://news.ycombinator.com/item?id=47087114>  
> Title: I'm sure there are lots of Stripe engineers that cruise the comments here. Anyon... | Hacker News  
> Captured at: `2026-08-31T17:50:32Z`

---

**rco8786** · 2026-02-20

I'm sure there are lots of Stripe engineers that cruise the comments here. Anyone care to provide some color on how this is actually working? It's not a secret that agents can produce tons and tons of code on their own. But is this code being shipped? Maintained? Reviewed?

---

## Comments

> **etothet** · [2026-02-20](https://news.ycombinator.com/item?id=47087644)
> 
> Part 1 is linked in this article and explains a bit: “Minions are Stripe’s homegrown coding agents. They’re fully unattended and built to one-shot tasks. Over a thousand pull requests merged each week at Stripe are completely minion-produced, and while they’re human-reviewed, they contain no human-written code.”
> 
> I could be wrong, but my educated guess is that, like many companies, they have many low hanging fruit tasks that would never make it into a sprint or even somewhat larger tasks that are straight forward to define and implement in isolation.

> **dakolli** · [2026-02-20](https://news.ycombinator.com/item?id=47087236)
> 
> The few guys who they haven't laid off are too busy reviewing and being overworked, doing the work of 10 to scroll HN. Gotta get their boss another boat, AI is so awesome!
> 
> > **malfist** · [2026-02-20](https://news.ycombinator.com/item?id=47088079)
> > 
> > Stripe hasn't had a layoff in a good while. Stripe is hiring like mad and is planning on growing engineering significantly. Your comment isn't grounded in reality
> > 
> > > **snayan** · [2026-02-20](https://news.ycombinator.com/item?id=47089819)
> > > 
> > > Seems like they've been pretty successful with this method? Why do you think it's bullshit?
> > > 
> > > > **rileymichael** · [2026-02-20](https://news.ycombinator.com/item?id=47094423)
> > > > 
> > > > successful how? the only metric i see is # of pull requests which means nothing. hell, $dayJob has hundreds of PRs generated weekly from renovate, i18n integrations, etc. with no LLM in the mix!
