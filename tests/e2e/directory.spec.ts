// ABOUTME: Browser acceptance for the directory: search, filters, history, and old links.
// ABOUTME: The no-javascript project proves that every entry link works without the script.

import { expect, test, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { PREVIEW_URL } from './preview';

const PREVIEW_HOST = new URL(PREVIEW_URL).host;
/** The committed catalog, so the spec follows the data. */
const CATALOG = JSON.parse(
  readFileSync(new URL('../../data/agents.json', import.meta.url), 'utf8'),
) as {
  approaches: ReadonlyArray<{ id: string; company_id: string; catalog_section: 'agents' | 'infrastructure' }>;
  companies: ReadonlyArray<{ id: string; logo: { readonly path: string } | null }>;
};
/** The number of implementations in the committed catalog. */
const TOTAL = CATALOG.approaches.filter((item) => item.catalog_section === 'agents').length;
const ALL_TOTAL = CATALOG.approaches.length;
/** The logo descriptor of each company, or null when only its monogram remains. */
const LOGO_BY_COMPANY = new Map(CATALOG.companies.map((company) => [company.id, company.logo]));
/** Cards whose companies show a monogram, and cards whose companies show a logo. */
const MONOGRAM_CARDS = CATALOG.approaches
  .filter((approach) => LOGO_BY_COMPANY.get(approach.company_id) === null)
  .slice(0, 3);
const LOGO_CARDS = CATALOG.approaches
  .filter((approach) => LOGO_BY_COMPANY.get(approach.company_id) !== null)
  .slice(0, 3);
const visibleCards = (page: Page) => page.locator('article.entry:visible');

test.describe('the directory without javascript', () => {
  test.skip(({ javaScriptEnabled }) => javaScriptEnabled !== false, 'This is the no-JS project.');

  test('names each card by its company and its name', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('#brex-disputes h3')).toHaveText('Brex · Dispute preparation agent');
    await expect(page.locator('#brex-disputes .entry-bookmark')).toHaveAttribute('aria-label', 'Bookmark Brex · Dispute preparation agent');
    await page.goto('/infrastructure');
    await expect(page.locator('#dropbox-nova h3')).toHaveText('Dropbox · Nova');
  });

  test('shows every entry link', async ({ page }) => {
    await page.goto('/');
    await expect(visibleCards(page)).toHaveCount(TOTAL);
    const links = page.locator('article.entry a[href^="/agents/"]');
    const targets = await links.evaluateAll((nodes) =>
      nodes.map((node) => (node as HTMLAnchorElement).getAttribute('href')),
    );
    expect(new Set(targets).size).toBe(ALL_TOTAL);
  });

  test('keeps the card of an old fragment link as its anchor', async ({ page }) => {
    await page.goto('/#block-builderbot');
    expect(new URL(page.url()).pathname).toBe('/');
    await expect(page.locator('article.entry#block-builderbot')).toBeVisible();
  });

  test('gives every card exactly one company logo mark', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('article.entry')).toHaveCount(ALL_TOTAL);
    await expect(page.locator('article.entry span.company-logo')).toHaveCount(ALL_TOTAL);
    await expect(page.locator('article.entry:has(span.company-logo[data-company-id])')).toHaveCount(
      ALL_TOTAL,
    );

    for (const approach of MONOGRAM_CARDS) {
      const mark = page.locator(`article.entry#${approach.id} span.company-logo`);
      await expect(mark).toHaveAttribute('data-company-id', approach.company_id);
      // The card's mark is rendered but hidden for now, so only its presence is checked.
      await expect(mark.locator('span.company-logo-monogram')).toHaveCount(1);
      await expect(mark.locator('img')).toHaveCount(0);
    }

    for (const approach of LOGO_CARDS) {
      const logo = LOGO_BY_COMPANY.get(approach.company_id)!;
      const mark = page.locator(`article.entry#${approach.id} span.company-logo`);
      await expect(mark).toHaveAttribute('data-company-id', approach.company_id);
      await expect(mark.locator('img')).toHaveAttribute('src', `/${logo.path}`);
      await expect(mark.locator('span.company-logo-monogram')).toHaveCount(0);
    }
  });
});

test.describe('the directory with javascript', () => {
  test.skip(({ javaScriptEnabled }) => javaScriptEnabled === false, 'These cases need the script.');

  test('shows the whole catalog under a bar that opens the palette', async ({ page }) => {
    await page.goto('/');
    await expect(visibleCards(page)).toHaveCount(TOTAL);
    const bar = page.locator('.search-launcher');
    await expect(bar).toBeVisible();
    // It reads as a field and answers as a door: no field of its own to type in.
    await expect(bar.locator('input')).toHaveCount(0);
    await bar.click();
    await expect(page.locator('#palette')).toBeVisible();
  });

  for (const shortcut of ['Meta+k', 'Control+k']) {
    test(`${shortcut} opens the palette and types into it`, async ({ page }) => {
      await page.goto('/');
      await expect(page.locator('#palette')).toBeHidden();
      await page.keyboard.press(shortcut);
      await expect(page.locator('#palette')).toBeVisible();
      await expect(page.locator('#palette-input')).toBeFocused();
      await page.keyboard.type('notion');
      await expect(page.locator('#palette-input')).toHaveValue('notion');
      // The letter reaches the field rather than closing what it opened.
      await page.keyboard.press('k');
      await expect(page.locator('#palette-input')).toHaveValue('notionk');
      await page.keyboard.press('Escape');
      await expect(page.locator('#palette')).toBeHidden();
      // A close leaves its animation's fill behind; the next open must clear it.
      await page.keyboard.press(shortcut);
      await expect(page.locator('#palette')).toBeVisible();
      await expect
        .poll(
          () => page.evaluate(() => getComputedStyle(document.getElementById('palette')!).opacity),
          { timeout: 2000 },
        )
        .toBe('1');
    });
  }

  test('reopens the palette on a clean box after a close', async ({ page }) => {
    await page.goto('/');
    await page.keyboard.press('Meta+k');
    await expect(page.locator('#palette')).toBeVisible();
    await page.keyboard.press('Escape');
    await expect(page.locator('#palette')).toBeHidden();
    await page.keyboard.press('Meta+k');
    await expect(page.locator('#palette')).toBeVisible();
    // The close fades the blocks, so nothing it leaves can outlast it on the box.
    expect(await page.evaluate(() => document.getElementById('palette')!.style.opacity)).toBe('');
  });

  test('search launchers and shortcuts survive client navigation', async ({ page }) => {
    await page.goto('/definitions');
    // A document replacement would erase this marker and mask the regression.
    await page.evaluate(() => { Object.assign(window, { navigationMarker: true }); });
    for (const path of ['/lessons', '/']) {
      const menu = page.locator('.nav-toggle');
      if (await menu.isVisible()) await menu.click();
      await page.locator(`.nav-links a[href="${path}"]`).first().click();
      await expect(page).toHaveURL(new RegExp(`${path}$`));
      expect(await page.evaluate(() => 'navigationMarker' in window)).toBe(true);
      await page.locator('.search-launcher').click();
      await expect(page.locator('#palette')).toBeVisible();
      await page.keyboard.press('Escape');
      await expect(page.locator('#palette')).toBeHidden();
      await page.keyboard.press('Control+k');
      await expect(page.locator('#palette-input')).toBeFocused();
      await page.keyboard.press('Escape');
      await expect(page.locator('#palette')).toBeHidden();
    }
    await page.locator('.search-launcher').click();
    await expect(page.locator('#palette')).toBeVisible();
  });

  test('reinitializing a page keeps one contents rail and a working palette', async ({ page }) => {
    await page.goto('/definitions');
    const links = page.locator('#contents a');
    await expect(links).not.toHaveCount(0);
    const count = await links.count();
    await page.evaluate(() => {
      document.dispatchEvent(new Event('astro:page-load'));
      document.dispatchEvent(new Event('astro:page-load'));
    });
    await expect(page.locator('#contents .contents-title')).toHaveCount(1);
    await expect(links).toHaveCount(count);
    await page.locator('[data-palette-open]').click();
    const filters = page.locator('.palette-filter-open');
    if (await filters.isVisible()) await filters.click();
    await page.locator('.palette-pill').first().click();
    await expect(page.locator('.palette-menu').first()).toBeVisible();
  });

  test('global search launcher opens the palette after repeated closes', async ({ page }) => {
    await page.goto('/?work=security');
    for (const target of ['#search-shortcut', '#search-shortcut', '#search-shortcut']) {
      await page.locator(target).first().click();
      await expect(page.locator('#palette-input')).toBeFocused();
      await page.keyboard.press('Escape');
      await expect(page.locator('#palette')).toBeHidden();
    }
  });

  test('the palette opens from the bar and reaches every kind of page', async ({ page }) => {
    await page.goto('/');
    await page.locator('.search-launcher').click();
    await expect(page.locator('#palette')).toBeVisible();
    for (const group of ['catalog', 'infrastructure', 'lessons', 'definitions']) {
      await expect(page.locator(`.palette-group[data-group="${group}"]`)).toBeVisible();
    }
    await page.locator('#palette-input').fill('stripe');
    await expect(page.locator('.palette-group[data-group="definitions"]')).toBeHidden();
    await expect(page.locator('.palette-item:not([hidden])').first()).toContainText('Stripe');
  });

  test.describe('old fragment links', () => {
    test('sends an entry fragment to the entry page', async ({ page }) => {
      await page.goto('/#block-builderbot');
      await expect(page).toHaveURL(/\/agents\/block-builderbot$/);
      await expect(page.locator('h1')).toHaveText('Builderbot');
    });

    test('sends a claim fragment to the claim on its entry page', async ({ page }) => {
      await page.goto('/#claim-uber-ureview--headline-metric');
      await expect(page).toHaveURL(
        /\/agents\/uber-ureview#claim-uber-ureview--headline-metric$/,
      );
      await expect(page.locator('#claim-uber-ureview--headline-metric')).toBeVisible();
    });

    test('sends a source fragment to the source on its entry page', async ({ page }) => {
      await page.goto('/#source-plaid-internal-mcp-server-source-1');
      await expect(page).toHaveURL(
        /\/agents\/plaid-internal-mcp-server#source-plaid-internal-mcp-server-source-1$/,
      );
      await expect(page.locator('#source-plaid-internal-mcp-server-source-1')).toBeVisible();
    });

    test('replaces the directory in the history, so back leaves the site entry', async ({ page }) => {
      await page.goto('/');
      await page.goto('/#block-builderbot');
      await expect(page).toHaveURL(/\/agents\/block-builderbot$/);
      await page.goBack();
      expect(new URL(page.url()).pathname).toBe('/');
    });

    for (const fragment of ['#catalog', '#main', '#not-a-real-entry', '#claim-nobody--field']) {
      test(`keeps ${fragment} on the directory`, async ({ page }) => {
        await page.goto(`/${fragment}`);
        expect(new URL(page.url()).pathname).toBe('/');
        await expect(visibleCards(page)).toHaveCount(TOTAL);
      });
    }

    for (const fragment of [
      '#//evil.example.com',
      '#https://evil.example.com',
      '#block-builderbot/../../evil',
      '#%2e%2e%2fevil',
    ]) {
      test(`refuses to redirect on ${fragment}`, async ({ page }) => {
        await page.goto(`/${fragment}`);
        expect(new URL(page.url()).host).toBe(PREVIEW_HOST);
        expect(new URL(page.url()).pathname).toBe('/');
      });
    }
  });

});

/* The chrome around the page: the menu a phone opens, the dot a column carries,
   and the sheet the filters become. Each is wired per page, for every width. */
test.describe('the site chrome', () => {
  test.skip(({ javaScriptEnabled }) => javaScriptEnabled === false, 'These cases need the script.');

  test('leaves the sidebar alone when Escape closes something else', async ({ page }, testInfo) => {
    test.skip(testInfo.project.name !== 'desktop', 'The sidebar is a column only on a wide screen.');
    await page.goto('/');
    // The menu answers Escape at every width, and the element it moves is the sidebar.
    const sampling = page.evaluate(
      () =>
        new Promise<number>((resolve) => {
          const sidebar = document.querySelector('.sidebar')!;
          let lowest = 1;
          const until = performance.now() + 500;
          const tick = (): void => {
            lowest = Math.min(lowest, Number(getComputedStyle(sidebar).opacity));
            if (performance.now() < until) requestAnimationFrame(tick);
            else resolve(lowest);
          };
          requestAnimationFrame(tick);
        }),
    );
    await page.keyboard.press('Escape');
    expect(await sampling).toBe(1);
  });

  test('takes the dot off one page before it brings it back on the next', async ({
    page,
  }, testInfo) => {
    test.skip(testInfo.project.name !== 'desktop', 'The dot stands beside a column only.');
    await page.goto('/');
    // The change captures the dot it leaves apart from the dot it arrives with,
    // so each has its own timing to read. Sharing a name would pair them into
    // one, and the page would carry both dots at once for the whole change.
    await page.evaluate(() => {
      const timings: Record<string, { start: number; end: number }> = {};
      (window as unknown as { timings: typeof timings }).timings = timings;
      document.addEventListener('astro:after-swap', () => {
        // The animations begin once the change is captured, a frame or two later.
        const until = performance.now() + 600;
        const tick = (): void => {
          for (const animation of document.getAnimations()) {
            const effect = animation.effect;
            const pseudo = effect instanceof KeyframeEffect ? effect.pseudoElement : null;
            if (!effect || !pseudo?.includes('nav-dot')) continue;
            const timing = effect.getComputedTiming();
            const start = Number(timing.delay ?? 0);
            timings[pseudo] = { start, end: start + Number(timing.activeDuration ?? 0) };
          }
          if (performance.now() < until) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      });
    });

    await page.locator('.nav-links a[href="/lessons"]').click();
    await expect
      .poll(() =>
        page.evaluate(
          () => Object.keys((window as unknown as { timings: Record<string, unknown> }).timings).length,
        ),
      )
      .toBe(2);

    const timings = await page.evaluate(
      () =>
        (window as unknown as { timings: Record<string, { start: number; end: number }> }).timings,
    );
    const leaving = timings['::view-transition-old(nav-dot-out)'];
    const arriving = timings['::view-transition-new(nav-dot-in)'];
    expect(leaving).toBeDefined();
    expect(arriving).toBeDefined();
    // The one that leaves is gone before the one that arrives begins.
    expect(arriving!.start).toBeGreaterThanOrEqual(leaving!.end);

    // And it comes back beside the page now open, not the page it left.
    const lessons = page.locator('.nav-links a[href="/lessons"]');
    await expect(lessons).toHaveAttribute('aria-current', 'page');
    await expect
      .poll(() =>
        page.evaluate(() => {
          const dot = document.querySelector<HTMLElement>('.nav-dot')!;
          const current = document.querySelector<HTMLElement>('.nav-links a[aria-current="page"]')!;
          return dot.style.top === `${current.offsetTop + current.offsetHeight / 2}px`;
        }),
      )
      .toBe(true);
  });

  test('carries the dot to its link when a narrow window is widened', async ({ page }, testInfo) => {
    test.skip(testInfo.project.name !== 'desktop', 'One project is enough, and it can resize.');
    // A narrow screen hides the column, so the dot is placed against a laid-out one.
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto('/');
    await page.setViewportSize({ width: 1280, height: 900 });
    await expect
      .poll(() =>
        page.evaluate(() => {
          const dot = document.querySelector<HTMLElement>('.nav-dot')!;
          const current = document.querySelector<HTMLElement>('.nav-links a[aria-current="page"]')!;
          return dot.style.top === `${current.offsetTop + current.offsetHeight / 2}px`;
        }),
      )
      .toBe(true);
  });

  test('drops the filter sheet’s staged choices when the palette closes', async ({ page }, testInfo) => {
    test.skip(testInfo.project.name !== 'mobile', 'The filters are a sheet only on a phone.');
    const openPalette = async (): Promise<void> => {
      await page.locator('[data-palette-open], .search-box').first().click();
      await expect(page.locator('#palette')).toBeVisible();
    };
    await page.goto('/');
    await openPalette();
    await page.locator('.palette-filter-open').click();
    const facet = page.locator('.palette-facet').nth(1);
    await facet.locator('.palette-pill').click();
    await facet.locator('.palette-option').first().click();
    await expect(facet.locator('.palette-pill')).toHaveClass(/is-on/);

    // Tapping the scrim is neither Apply nor Go back, so the choice never landed.
    const panel = (await page.locator('.palette-panel').boundingBox())!;
    await page.mouse.click(panel.x + panel.width / 2, Math.max(4, panel.y - 8));
    await expect(page.locator('#palette')).toBeHidden();
    await openPalette();
    await expect(facet.locator('.palette-pill')).not.toHaveClass(/is-on/);
  });
  test('the filter button says whether the sheet is open', async ({ page }, testInfo) => {
    test.skip(testInfo.project.name !== 'mobile', 'The filters are a sheet only on a phone.');
    await page.goto('/');
    await page.locator('[data-palette-open], .search-box').first().click();
    await expect(page.locator('#palette')).toBeVisible();
    const button = page.locator('.palette-filter-open');
    await expect(button).toHaveAttribute('aria-expanded', 'false');
    await button.click();
    await expect(button).toHaveAttribute('aria-expanded', 'true');
    await page.locator('.palette-back').click();
    await expect(button).toHaveAttribute('aria-expanded', 'false');
  });

  test('the sheet takes what it stands over out of reach', async ({ page }, testInfo) => {
    test.skip(testInfo.project.name !== 'mobile', 'The filters are a sheet only on a phone.');
    await page.goto('/');
    await page.locator('[data-palette-open], .search-box').first().click();
    await expect(page.locator('#palette')).toBeVisible();
    const head = page.locator('.palette-search');
    await page.locator('.palette-filter-open').click();
    expect(await head.evaluate((el) => el.hasAttribute('inert'))).toBe(true);
    // The field the sheet covers cannot be reached behind it, by tab or by script.
    const reached = await page.evaluate(() => {
      document.getElementById('palette-input')!.focus();
      return document.activeElement?.id ?? '';
    });
    expect(reached).not.toBe('palette-input');
    await page.locator('.palette-back').click();
    expect(await head.evaluate((el) => el.hasAttribute('inert'))).toBe(false);
  });
});

test.describe('the directory order', () => {
  /** The card identifiers in the order the agents grid shows them. */
  const cardOrder = (page: Page) =>
    page.locator('[data-collection-group="agents"] article.entry').evaluateAll((nodes) =>
      nodes.map((node) => ({
        id: node.id,
        documented: node.getAttribute('data-well-documented') === 'true',
        featured: node.getAttribute('data-featured') === 'true',
        rank: Number(node.getAttribute('data-alphabetical-rank')),
      })),
    );

  test('shows the well-documented cards first, each with its badge', async ({ page }) => {
    await page.goto('/');
    const cards = await cardOrder(page);
    const firstPlain = cards.findIndex((card) => !card.documented);
    expect(firstPlain).toBeGreaterThan(0);
    expect(cards.slice(firstPlain).every((card) => !card.documented)).toBe(true);
    await expect(page.locator(`article.entry#${cards[0]!.id} .tag-documented`)).toHaveText('In depth');
    await expect(page.locator('article.entry .tag-documented')).toHaveCount(
      cards.filter((card) => card.documented).length + (await page.locator('[data-collection-group="infrastructure"] article.entry[data-well-documented="true"]').count()),
    );
    await expect(page.locator(`article.entry#${cards[firstPlain]!.id} .tag-documented`)).toHaveCount(0);
  });

  test('names the type only on a card that is not a plain agent', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('article.entry#stripe-minions .tag-type')).toHaveCount(0);
    await expect(page.locator('article.entry#figma-security-agent .tag-type')).toHaveText('Agent family');
    // Without its type tag, a plain agent's first tag is a work domain, which keeps the plain style.
    const first = page.locator('article.entry#stripe-minions .tags > .tag').first();
    const family = page.locator('article.entry#figma-security-agent .tag-type');
    const color = (node: typeof first) => node.evaluate((element) => getComputedStyle(element).backgroundColor);
    expect(await color(first)).not.toBe(await color(family));
  });

  test('marks the work domain of a problem page on each of its cards', async ({ page }) => {
    await page.goto('/problems/code-review-load');
    const cards = page.locator('article.entry');
    expect(await cards.count()).toBeGreaterThan(0);
    // Every card on the page carries the problem's domain, and only that tag is marked.
    await expect(page.locator('article.entry .tag-match')).toHaveCount(await cards.count());
    await expect(page.locator('article.entry .tag-match').first()).toHaveText('Code review');
    const marked = page.locator('article.entry .tag-match').first();
    const plain = page.locator('article.entry .tags > .tag:not(.tag-match):not(.tag-type):not(.tag-documented)').first();
    const color = (node: typeof marked) => node.evaluate((element) => getComputedStyle(element).backgroundColor);
    expect(await color(marked)).not.toBe(await color(plain));
    await page.goto('/');
    await expect(page.locator('article.entry .tag-match')).toHaveCount(0);
  });

  test('shows the featured cards before all others', async ({ page }) => {
    await page.goto('/');
    const cards = await cardOrder(page);
    const featured = cards.filter((card) => card.featured).length;
    expect(featured).toBeGreaterThan(0);
    expect(cards.slice(0, featured).every((card) => card.featured)).toBe(true);
  });

  test('opens A–Z from the URL, and the default order without it', async ({ page, javaScriptEnabled }) => {
    test.skip(javaScriptEnabled === false, 'The sort needs the script.');
    await page.goto('/?sort=az');
    const ranks = (await cardOrder(page)).map((card) => card.rank);
    expect(ranks).toEqual([...ranks].sort((a, b) => a - b));
    await page.goto('/');
    expect((await cardOrder(page))[0]!.documented).toBe(true);
  });

  test('shows no sort control on the page', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('#catalog [data-sort-option]')).toHaveCount(0);
  });

  test('puts a bookmarked card first, keeps it after a reload, and lets it go', async ({ page, javaScriptEnabled }) => {
    test.skip(javaScriptEnabled === false, 'The bookmark corner needs the script.');
    await page.goto('/');
    const last = (await cardOrder(page)).at(-1)!;
    const corner = page.locator(`article.entry#${last.id} [data-bookmark]`);
    await expect(corner).toHaveAttribute('aria-pressed', 'false');
    await corner.click();
    await expect(page).toHaveURL(/\/$/);
    await expect(corner).toHaveAttribute('aria-pressed', 'true');
    expect((await cardOrder(page))[0]!.id).toBe(last.id);
    await page.reload();
    expect((await cardOrder(page))[0]!.id).toBe(last.id);
    await page.goto('/?sort=az');
    expect((await cardOrder(page))[0]!.id).toBe(last.id);
    await page.locator(`article.entry#${last.id} [data-bookmark]`).click();
    await expect(page.locator(`article.entry#${last.id} [data-bookmark]`)).toHaveAttribute('aria-pressed', 'false');
    expect((await cardOrder(page))[0]!.id).not.toBe(last.id);
  });

  test('keeps an open pill menu above the results while the palette opens', async ({ page, javaScriptEnabled, isMobile }) => {
    test.skip(javaScriptEnabled === false, 'The palette needs the script.');
    test.skip(isMobile, 'On a phone the pills are in the filter sheet, above the results.');
    await page.goto('/');
    await page.locator('.search-launcher').click();
    await page.locator('[data-palette-sort] .palette-pill').click();
    // The opening animation gives each row a transform; hold them in that state.
    const covered = await page.evaluate(() => {
      for (const selector of ['.palette-filters', '.palette-results']) {
        const row = document.querySelector<HTMLElement>(selector)!;
        row.getAnimations().forEach((animation) => animation.cancel());
        row.style.transform = 'translateY(1px)';
      }
      const option = document.querySelector<HTMLElement>('[data-palette-sort] [data-sort-option="az"]')!;
      const box = option.getBoundingClientRect();
      const top = document.elementFromPoint(box.left + box.width / 2, box.top + box.height / 2);
      return option.contains(top) ? null : top?.outerHTML.slice(0, 80);
    });
    expect(covered).toBeNull();
  });

  test('sorts the palette from its sort pill, and the directory with it', async ({ page, javaScriptEnabled }) => {
    test.skip(javaScriptEnabled === false, 'The palette needs the script.');
    await page.goto('/');
    await page.locator('.search-launcher').click();
    const sort = page.locator('[data-palette-sort]');
    const firstItem = page.locator('.palette-group[data-group="catalog"] li:has(.palette-item:visible)').first();
    await expect(firstItem).toHaveAttribute('data-well-documented', 'true');
    // On a phone the pills are behind the filter sheet.
    const sheet = page.locator('.palette-filter-open');
    if (await sheet.isVisible()) await sheet.click();
    await sort.locator('.palette-pill').click();
    await sort.locator('[data-sort-option="az"]').click();
    await expect(sort.locator('[data-sort-option="az"]')).toHaveAttribute('aria-pressed', 'true');
    const ranks = () =>
      page.locator('.palette-group[data-group="catalog"] li').evaluateAll((nodes) =>
        nodes.map((node) => Number(node.getAttribute('data-alphabetical-rank'))),
      );
    await expect.poll(async () => {
      const list = await ranks();
      return list.every((rank, index) => index === 0 || list[index - 1]! < rank);
    }).toBe(true);
    await expect(firstItem).toHaveAttribute('data-alphabetical-rank', String(Math.min(...(await ranks()))));
    await expect(page).toHaveURL(/\?sort=az$/);
    await page.keyboard.press('Escape');
    const cards = (await cardOrder(page)).map((card) => card.rank);
    expect(cards).toEqual([...cards].sort((a, b) => a - b));
  });
});

test.describe('the problem entry points', () => {
  const PROBLEM_PATHS = [
    '/problems/code-review-load',
    '/problems/security-alerts',
    '/problems/company-data',
    '/problems/operations',
    '/infrastructure',
  ];

  test('the homepage links to every problem under the hero', async ({ page }) => {
    await page.goto('/');
    const links = page.locator('header.intro .problem-links a');
    await expect(links).toHaveCount(PROBLEM_PATHS.length);
    expect(await links.evaluateAll((nodes) => nodes.map((node) => node.getAttribute('href')))).toEqual(PROBLEM_PATHS);
    await expect(page.locator('.problem-links h2')).toHaveText('Start with a problem');
  });

  test('the infrastructure page shows no problem links', async ({ page }) => {
    await page.goto('/infrastructure');
    await expect(page.locator('.problem-links')).toHaveCount(0);
  });

  for (const path of PROBLEM_PATHS.slice(0, -1)) {
    test(`${path} lists its records with the detailed ones first`, async ({ page }) => {
      await page.goto(path);
      await expect(page.locator('h1')).not.toBeEmpty();
      const cards = page.locator('#agents article.entry');
      expect(await cards.count()).toBeGreaterThan(0);
      const flags = await cards.evaluateAll((nodes) => nodes.map((node) => node.getAttribute('data-well-documented') === 'true'));
      const firstPlain = flags.indexOf(false);
      if (firstPlain >= 0) expect(flags.slice(firstPlain).every((flag) => !flag)).toBe(true);
      const href = await cards.first().locator('h3 a').getAttribute('href');
      expect(href).toMatch(/^\/agents\//);
    });
  }
});
