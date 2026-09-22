# Plan 015: Give every page its own link preview card

> Requested on 2026-09-21 as a plan after a design review of six card treatments and
> two rounds of exploration. The owner chose the directory card, inverted (G1 on the
> review page), and asked for implementation prep on the same day. Implementation is
> not authorized by this document; the STOP conditions below name what needs approval
> first.

## Status and baseline

- Priority P2; effort M. One branch, one pull request.
- Category: discovery and sharing. Supersedes Plan 014 Phase 5 item 1, which asked
  for the same output without a design.
- Planned on 2026-09-21 on `main` at `73bf5aa`.
- Baseline: every route sets `og:image` to the one file `public/og.png`, 1200 by 630,
  through `OG_IMAGE` in `src/lib/metadata.ts`. Titles, descriptions, and canonical
  URLs are already per page. Only the image is not.
- Design review: <https://claude.ai/artifact/TwGubVbUGwR2y421FgZUWV>. The chosen card
  is G1 in the "G explored" section; the "Rendered" section at the top shows three
  cards produced by the real renderer.
- Renderer spike, 2026-09-21, outside the repository: `satori` 0.33.4 and
  `@resvg/resvg-js` 2.6.2 render the G1 card from the static Areal instances and the
  vendored logos. Three cards in 2.5 s including the font load; one hundred renders in
  13.9 s, about 140 ms each; identical bytes for identical input; 48 to 57 KB per PNG.
  The catalog has about 95 routes, so the build cost is about 14 s, inside Plan 014's
  30 s budget.
- Fonts: the renderer needs static TTF files, because satori reads neither WOFF2 nor
  variable fonts. The licensed ABC Areal package (owner-supplied 2026-09-22) ships
  `ABCAreal-Regular.ttf` and `ABCAreal-Medium.ttf`, the two weights `DESIGN.md`
  allows. They sit at `src/og/fonts/`. On 2026-09-22 the owner decided to commit
  them to the public repository for now and to handle licence adherence, including
  the private-repository provisioning in step 2, as the next day's work. Converted or
  instanced files are not used anywhere: the Dinamo terms (§10) forbid converting or
  modifying the fonts.
- Licence, from `Dinamo Licensing Terms.pdf` v2.51 in the package. Read for this plan
  on 2026-09-22; the invoice's licence types decide, and only the owner has it:
  - Rendering PNG cards at build time is use of the desktop files to create digital
    documents for one brand (§9.2, desktop/print). The output is a raster; no font
    data reaches an end user (§10 "embed ... in a way end users can access them").
  - §9.4 (social media) covers "design assets for one brand to use on social media
    channels". A link preview is drawn by the platform from our page, not posted by
    us, but a strict reading could ask for it. A Company Size under 3 gets it free
    with desktop/print; otherwise it is a line on the invoice to check.
  - §10 forbids putting the fonts in public repositories. The repository
    `steel-experiments/internal-agents-map` is public. The TTFs therefore never enter
    git; see the build step below. The same clause touches `public/fonts/Areal.woff2`,
    committed in `1ee95c0`; that is outside this plan and recorded as a finding.
- Other agents edit this checkout. Stage explicit paths only; never `git add -A`.

## Why this matters

A company that shares its own entry page today gets a card that never names it. The
card is the first thing a reader sees in Slack, LinkedIn, or X, and it decides whether
the link is opened. A card that shows the system name and the organization mark makes
the entry worth resharing by the organization itself, which is the cheapest reach the
catalog can get. The organization card carries the count of documented systems, which
is the hook for the same share.

## The card

The homepage directory item at poster scale, on the site's own colours. One template
for entries; a panel-less variant for organizations and sections. 1200 by 630.

**Entry card (G1).**

- Ground Sand 3 `#F1F0EF`. Padding 72px top, 84px sides, 60px bottom. Two columns:
  text, then a 340px panel, 56px apart.
- Title: `<Company>'s <agent_name>`, the possessive the homepage uses for every item
  and `organization-view.ts` already builds. Areal 500, letter spacing -0.03em, line
  height 1.02. The possessive in muted `#82827C`, the name in ink `#21201C`. Size by
  the length of the whole string: 80px up to 12 characters, 72px up to 22, 64px
  beyond. The two parts are separate spans in a wrapping row, so when they do not fit
  one line the possessive takes the first line alone (see the Brex render).
- Lede: the directory card's own `excerpt` (the summary claim through `shorten` at
  `CARD_SUMMARY_LIMIT`). 32px, 400, muted, line height 1.38, letter spacing -0.01em,
  24px below the title. At most three lines; the layout leaves room for three.
- Tags, 30px below the lede: the same row `AgentCard.astro` renders, the approach
  type label first, then the domain labels. 28px, 400, 12px by 20px padding, 28px
  radius, 16px apart. First tag blue-3 `#E6F4FE` on blue-9 `#0090FF`; the rest white
  on `#63635E`. At most four tags; the row does not wrap.
- Footer, pinned to the bottom of the text column: `internal-agents.com`, 26px, 500,
  ink. Nothing else.
- Panel: white, 32px corners, full height of the content box, contents centred. The
  organization logo from `public/logos/`, aspect kept: a square or tall mark at 120px
  high with the company name under it (32px, 500, 26px gap); a wordmark (registry
  flag) at 64px high and no name. A raster logo is never drawn above its own pixel
  height.
- Infrastructure entries use the same card; their first tag reads `Platform` or
  whatever `approachTypeLabel` says.

**Organization card (G5 layout).**

- Same ground and padding, no panel. The logo at the top left: 64px high for a mark,
  56px for a wordmark, with the company name beside a mark only.
- Title: the company name, 80px, 500, ink, 30px below the logo.
- Lede: the count sentence the organization page derives, 32px, muted.
- Tags: the system names, one white tag each, 28px, wrapping to as many rows as
  needed; the footer sits below the last row. Brex at five is the current maximum
  and fits two rows.
- Footer: `internal-agents.com/organizations/<id>`.

**Section and guide cards** (infrastructure, definitions, methodology, notes index,
each note): the G5 layout with no logo. A 14px blue-9 dot then the eyebrow in 26px
muted uppercase (`INFRASTRUCTURE`, `DEFINITIONS`, `NOTES`, `NOTE`), the page title at
72px, the page description as the lede, the footer. Notes add their publication date
to the eyebrow line. The homepage keeps `public/og.png` in this plan; redrawing it on
the same rules is a one-line follow-up once the cards are live.

**Type and glyphs.** ABC Areal Regular and Medium from the licensed package, 400 and
500 only. ABC Areal carries the middot, the
arrow, and the dash, but not the command glyph (U+2318); any text outside Latin
punctuation is checked against the font's cmap first, or satori falls back to
another face without warning.

**Reference element tree.** The spike's card function, which the executor turns into
`src/og/card.ts`:

```js
h('div', { display: 'flex', width: 1200, height: 630, background: SAND3, padding: '72px 84px 60px', fontFamily: 'Areal', color: INK }, [
  h('div', { display: 'flex', flexDirection: 'column', flex: 1, marginRight: 56 }, [
    h('div', { display: 'flex', flexWrap: 'wrap', fontSize: size, fontWeight: 500, letterSpacing: '-0.03em', lineHeight: 1.02 }, [
      h('span', { color: MUTED, marginRight: '0.22em' }, `${company}'s`), h('span', {}, name) ]),
    h('div', { fontSize: 32, lineHeight: 1.38, color: MUTED, marginTop: 24, letterSpacing: '-0.01em' }, excerpt),
    h('div', { display: 'flex', marginTop: 30 }, tags.map(tag)),
    h('div', { marginTop: 'auto', fontSize: 26, fontWeight: 500 }, 'internal-agents.com') ]),
  h('div', { display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: 340, background: '#fff', borderRadius: 32 }, [
    h('img', { width, height }, undefined, { src: logoDataUri }), ...(wordmark ? [] : [h('div', { fontSize: 32, fontWeight: 500, marginTop: 26 }, company)]) ]) ])
```

Satori needs `display: flex` on every element with more than one child, has no
`grid` and no `text-wrap: balance`, and takes images as data URIs.

## Product contract

- Every canonical HTML page carries an `og:image` that resolves to a file in `dist/`,
  1200 by 630, PNG, under 300KB, with `og:image:width`, `og:image:height`, and an alt
  text derived from the same fields as the card (`<Company>'s <agent_name>: <excerpt>`).
- Image paths: `og/agents/<id>.png`, `og/organizations/<id>.png`, `og/<section>.png`.
  The `og:image` URL carries `?v=<hash>` where the hash covers the record's
  `last_reviewed_at`, the logo file hash from the registry, and a template version
  constant, so LinkedIn and Slack drop their cached card when the card changes.
- The build stays deterministic: the same inputs write the same bytes, so the
  publication check can compare two builds.
- No new runtime. The site stays static; the images are files.
- The design of the pages does not change. `DESIGN.md` is untouched.

## Scope

In: the renderer, its fonts, the three card kinds, the layout prop, the delivery and
unit checks, and the Plan 014 pulse config update so the audit tests the new tags.

Out: a share block or badge on entry pages (a separate plan if wanted), any change to
the logo registry's assets, dark cards, and the outreach list from Plan 014 Phase 5.

## Implementation steps

1. **Dependencies.** Add `satori` and `@resvg/resvg-js` as dev dependencies, pinned.
   Record the versions and the measured build time in the pull request.
2. **Font provisioning (deferred by the owner on 2026-09-22 to the licence
   follow-up; the first release commits the files).** The two TTFs live outside the
   public repository. Store them
   in the private sibling repository `steel-experiments/internal-agents-map-private`
   under `fonts/`, and let the build fetch them: a small `scripts/fetch-og-fonts.mjs`
   reads `OG_FONTS_TOKEN` (a fine-grained GitHub token with read access to that one
   repository, set in Vercel) and downloads both files to `src/og/fonts/` when they
   are absent. Locally the files are already there. When the token is missing and the
   files are absent, the renderer throws and the build fails; it never falls back to
   another face. The Vercel build command gains `node scripts/fetch-og-fonts.mjs &&`
   before `npm run build`.
3. **Registry flag.** Add an optional `wordmark: true` to a company's logo entry in
   `data/companies.yaml` where the logo spells the name (Brex, StrongDM, Uber, and any
   other the executor finds by looking at each file). Surface it on `CompanyLogo` in
   `src/lib/companies.ts`; it selects the panel fit and hides the name. The site's own
   `CompanyLogo.astro` ignores it.
4. **Renderer module.** `src/lib/og.ts` (pure) derives the card input of an entry, an
   organization, or a section from the directory card, the company view, and the page
   headings, plus the image path, the version hash, and the alt text.
   `src/lib/section-cards.ts` holds the section and note inputs the pages and the
   endpoints share. `src/og/render.ts` builds the satori element tree, loads
   `ABCAreal-Regular.ttf` and `ABCAreal-Medium.ttf` once, runs satori then resvg
   (`fitTo` width 1200), and returns PNG bytes. Logos are read from `public/logos/`
   and passed as data URIs with their registry width and height.
5. **Endpoints.** `src/pages/og/agents/[id].png.ts`, `src/pages/og/organizations/
   [id].png.ts`, and one static endpoint per section card, each with `getStaticPaths`
   from the catalog and returning the PNG bytes with `image/png`.
6. **Layout.** `SiteLayout` takes an optional `ogImage: { path, alt, version }` and
   falls back to `OG_IMAGE`. Entry, organization, section, guide, and note pages pass
   theirs. A helper in `src/lib/metadata.ts` builds the versioned URL and the alt text.
7. **Checks.** `scripts/check_site.py` adds the image paths to the expected output
   set, parses each page's `og:image`, and fails when the target file is missing, not
   1200 by 630, or over 300KB. `tests/web/` gains a test that every catalog entry and
   organization has a card input and that the title size steps match the name lengths
   above. `scripts/site-publication.ts` needs no change if the endpoints register as
   routes; if the manifest gains `og/` routes, exclude them there as `robots.txt` and
   the exports are.
8. **Pulse config.** Add the `og:image` per-page rule to `.claude/skills/seo/
   config.json` so `tech-audit.mjs` reports a page that fell back to the default card.
9. **Release.** Build, run the card validators for X and LinkedIn on one entry, one
   organization, and the infrastructure page, and attach the three screenshots to the
   pull request.

## Commands

```sh
npm run build
uv run --locked python scripts/check_site.py --root dist
npm run test:unit
node .claude/skills/seo/scripts/tech-audit.mjs
npm run verify
```

## Done criteria

1. Every route in the manifest except the homepage carries its own `og:image`, and
   the delivery check proves each file exists at 1200 by 630.
2. Two consecutive builds write identical PNG bytes for the same inputs.
3. The renderer adds no more than 30 seconds to `npm run build`.
4. One entry card, one organization card, and the infrastructure card pass the X and
   LinkedIn validators with the correct image.
5. `npm run verify` is green.
6. The licence follow-up is scheduled: the fonts leave the public repository.

## STOP conditions

- **Font licence.** Before the pull request is opened, the owner confirms from the
  Dinamo invoice that the licence held covers desktop/print for Steel's Company Size,
  and decides whether the social media line is needed for link previews. If the
  invoice does not cover it, stop; do not swap the face and do not render with a
  converted file.
- **Public repository.** Waived by the owner on 2026-09-22 for the first release; the
  licence follow-up moves the TTFs out of the public repository.
- **Dependency.** Two dev dependencies are added: `satori` 0.33.4 and
  `@resvg/resvg-js` 2.6.2 (a native binary per platform; confirm the Vercel build
  image is covered, it is for linux-x64-gnu). The spike measured about 140 ms per
  card and about 14 s for the catalog; report the number from the real build in the
  pull request, as Plan 014 requires.
- Stop if a summary cannot fit two lines at 32px and the record has no workflow scope
  line; report which records.

## Completion record

Execution authorized by the owner on 2026-09-22, built the same day on the branch
`plan-015-og-cards`, and merged to `main` through pull request #11 on the owner's
instruction.

- Built: `src/lib/og.ts`, `src/lib/section-cards.ts`, `src/og/render.ts`, the four
  endpoints under `src/pages/og/`, the `ogImage` prop on both layouts, and the card
  on every entry, organization, section, guide, and note page. 102 cards per build.
- Checks: `scripts/check_site.py` requires a card per route at 1200 by 630 under
  300 KB and a valid `og:image` on every page (four new fixture cases);
  `tests/web/og.test.ts` covers the derivations, the URLs, and one real render;
  `tests/test_publication.py` and `tests/e2e/entry-pages.spec.ts` expect the per-page
  card; the SEO pulse reports a page that shares the default card
  (`og_image_default`, edited in the main checkout where the skill lives).
- Measured: `npm run build` 15.4 s in total with the cards, about 140 ms per card;
  identical bytes on repeated renders; 48 to 57 KB per PNG.
- `npm run verify` green on 2026-09-22 (174 unit tests, 208 Python tests, 489
  browser checks in the entry spec after its expectation moved to the per-page card).
- Deviations from the plan as written: the wordmark rule is derived from the logo's
  aspect ratio instead of a registry flag; the card excerpt is 120 characters, not the
  directory's 200; the fonts are committed for now by the owner's decision.
- Open: the licence follow-up (private-repository provisioning, the invoice check, and
  `public/fonts/Areal.woff2` in the public repository), the X and LinkedIn validator
  pass after deployment, and a redraw of the home card on the same rules.
