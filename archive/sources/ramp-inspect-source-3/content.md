> Archived source snapshot  
> Source ID: `ramp-inspect-source-3`  
> Original URL: <https://news.ycombinator.com/item?id=48042123>  
> Final URL: <https://news.ycombinator.com/item?id=48042123>  
> Title: Show HN: I built an open source background agent inspired by Ramp Inspect | Hacker News  
> Captured at: `2026-08-31T17:46:39Z`

---

[https://github.com/jvaill/Kill-The-Backlog](https://github.com/jvaill/Kill-The-Backlog)

I’ve been quietly building an open source background agent inspired by Ramp’s Inspect.

Basically, you can self-host it, point it to a GH repo, and prompt agents to do work on your behalf in the cloud.

The idea is to tighten the prompt -> preview -> deploy loop. Next steps will be to add preview environments and trigger changes from sources other than the web ui, like slack or your favorite project management tool.

All while making sure you can continue to self-host it and bring your own API keys.

---

## Comments

> **debarshri** · [2026-05-06](https://news.ycombinator.com/item?id=48043082)
> 
> why does it need e2b? Why cant you just use docker.
> 
> > **jvaill** · [2026-05-07](https://news.ycombinator.com/item?id=48053530)
> > 
> > I think eventually it'll support many different runtimes. I started with e2b because it has stronger security guarantees, especially useful if this ends up being multi-tenant.
