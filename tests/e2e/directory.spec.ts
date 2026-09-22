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
    for (const path of ['/notes', '/']) {
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
    for (const group of ['catalog', 'infrastructure', 'notes', 'definitions']) {
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

    await page.locator('.nav-links a[href="/notes"]').click();
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
    const notes = page.locator('.nav-links a[href="/notes"]');
    await expect(notes).toHaveAttribute('aria-current', 'page');
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
