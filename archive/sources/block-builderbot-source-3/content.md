> Archived source snapshot  
> Source ID: `block-builderbot-source-3`  
> Original URL: <https://github.com/block/builderbot>  
> Final URL: <https://github.com/block/builderbot>  
> Title: GitHub - block/builderbot: Incubating experimental AI projects to operate millions of lines of code · GitHub  
> Captured at: `2026-08-31T17:40:09Z`

---

## Builderbot Monorepo

This repository contains Builderbot apps, shared UI packages, and Rust crates.

## Quick Start

```
# from repo root
source ./bin/activate-hermit
just setup
```

`just setup` runs `lefthook install` and `pnpm install`.

Then run an app:

```
just dev          # start Staged
just dev differ   # start Differ
```

## App Installation

For end-user installs:

- Staged (macOS): `curl -fsSL https://raw.githubusercontent.com/block/builderbot/main/apps/staged/install.sh | bash`
- Differ: no standalone installer yet; run from source with `just dev differ` or build with `just app differ build`

## Command Guide

The root `justfile` supports both styles:

```
just dev differ     # verb-first (recommended for humans)
just app differ dev # explicit delegation form
```

Useful commands:

```
just apps         # list app names
just setup        # first-time setup (hooks + JS deps)
just dev          # run Staged app
just dev differ   # run Differ app
just staged       # alias for \`just app staged dev\`
just differ       # alias for \`just app differ dev\`
just check        # full non-modifying checks
just ci           # alias of \`just check\`
just fmt          # format repo
just lint         # lint repo
just test         # run Rust workspace tests
```

## Repo Layout

- `apps/staged`: main desktop app.
- `apps/differ`: standalone diff app.
- `packages/diff-viewer`: shared Svelte diff viewer package.
- `crates/`: shared Rust crates.
- `scripts/`: helper scripts used by app tooling.

## App-Level Commands

Each app has its own `justfile` for app-specific workflows:

- `apps/staged/justfile`
- `apps/differ/justfile`

Use root delegation to run any app recipe:

```
just app staged ci
just app differ build
```

## Troubleshooting

- `just: command not found`
	- Run `source ./bin/activate-hermit` in your shell.
- Frontend waiting on dev server / port issues
	- Check listeners: `lsof -nP -iTCP:<port> -sTCP:LISTEN`
- `node_modules` appears at repo root
	- Expected for this `pnpm` workspace monorepo; app `node_modules` entries are symlinked into the root store.

## More Docs

- Staged app docs: `apps/staged/README.md`
