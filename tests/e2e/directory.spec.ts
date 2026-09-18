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
/** A work filter value, and the label the search box suggests for it. */
const WORK = { value: 'security', label: 'Security' };
const INVOCATION = { value: 'background', label: 'Background' };
/** A supervision value, the label of its chip, and the level a person can type to reach it. */
const SUPERVISION = { value: 'exception-only', label: 'Exception-only (level 5)', typed: 'level 5' };
/** A search term. The cards whose text carries it are counted from the page. */
const SEARCH = { term: 'uber' };

const visibleCards = (page: Page) => page.locator('article.entry:visible');
/** The chips of the selected facet terms, in selection order. */
const chips = (page: Page) => page.locator('#chips .chip');
const chip = (page: Page, key: string, value: string) =>
  page.locator(`#chips .chip[data-key="${key}"][data-id="${value}"]`);
const suggestion = (page: Page, key: string, value: string) =>
  page.locator(`#suggestions [role="option"][data-key="${key}"][data-id="${value}"]`);
/** How many cards carry the work value, hidden or not. */
const workCount = (page: Page) => page.locator(`article.entry[data-collection="agents"][data-work~="${WORK.value}"]`).count();
/** How many cards carry the search term in their searchable text, hidden or not. */
const searchCount = (page: Page) =>
  page.locator(`article.entry[data-collection="agents"][data-search*="${SEARCH.term}"]`).count();

test.describe('the directory without javascript', () => {
  test.skip(({ javaScriptEnabled }) => javaScriptEnabled !== false, 'This is the no-JS project.');

  test('shows every entry link and hides the filter form', async ({ page }) => {
    await page.goto('/');
    await expect(visibleCards(page)).toHaveCount(TOTAL);
    const links = page.locator('article.entry a[href^="/agents/"]');
    const targets = await links.evaluateAll((nodes) =>
      nodes.map((node) => (node as HTMLAnchorElement).getAttribute('href')),
    );
    expect(new Set(targets).size).toBe(ALL_TOTAL);
    await expect(page.locator('#filters')).toBeHidden();
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

  test('shows the filter form and the whole catalog first', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('#filters')).toBeVisible();
    await expect(visibleCards(page)).toHaveCount(TOTAL);
    await expect(page.locator('#results')).toHaveText(`${TOTAL} items`);
    await expect(page.locator('#empty')).toBeHidden();
  });

  for (const shortcut of ['Meta+k', 'Control+k']) {
    test(`${shortcut} opens the palette and types into it`, async ({ page }) => {
      await page.goto('/?q=github');
      await expect(page.locator('#filters')).toBeVisible();
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

  test('search launchers and shortcuts survive client navigation', async ({ page }) => {
    await page.goto('/definitions');
    // A document replacement would erase this marker and mask the regression.
    await page.evaluate(() => { Object.assign(window, { navigationMarker: true }); });
    for (const path of ['/notes', '/']) {
      const menu = page.locator('.nav-toggle');
      if (await menu.isVisible()) await menu.click();
      await page.locator(`a[href="${path}"]`).first().click();
      await expect(page).toHaveURL(new RegExp(`${path}$`));
      expect(await page.evaluate(() => 'navigationMarker' in window)).toBe(true);
      await page.locator(path === '/' ? '#search-shortcut' : 'button[data-palette-open]').click();
      await expect(page.locator('#palette')).toBeVisible();
      await page.keyboard.press('Escape');
      await expect(page.locator('#palette')).toBeHidden();
      await page.keyboard.press('Control+k');
      await expect(page.locator('#palette-input')).toBeFocused();
      await page.keyboard.press('Escape');
      await expect(page.locator('#palette')).toBeHidden();
    }
    await page.locator('#search-shortcut').click();
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

  test('the palette opens from the search box and reaches every kind of page', async ({ page }) => {
    await page.goto('/');
    await page.locator('#search-shortcut').click();
    await expect(page.locator('#palette')).toBeVisible();
    for (const group of ['catalog', 'infrastructure', 'notes', 'definitions']) {
      await expect(page.locator(`.palette-group[data-group="${group}"]`)).toBeVisible();
    }
    await page.locator('#palette-input').fill('stripe');
    await expect(page.locator('.palette-group[data-group="definitions"]')).toBeHidden();
    await expect(page.locator('.palette-item:not([hidden])').first()).toContainText('Stripe');
  });

  test('searches the cards and records the search in the URL', async ({ page }) => {
    await page.goto('/');
    await page.fill('#q', SEARCH.term);
    await expect(visibleCards(page)).toHaveCount(await searchCount(page));
    await expect(page.locator('#results')).toHaveText(`${await searchCount(page)} items`);
    await expect(page).toHaveURL(new RegExp(`\\?q=${SEARCH.term}$`));
    await expect(page.locator('article.entry#uber-ureview')).toBeVisible();
  });

  test('turns a suggested work area into a chip and records it in the URL', async ({ page }) => {
    await page.goto('/');
    await page.fill('#q', 'secu');
    await expect(page.locator('#q')).toHaveAttribute('aria-expanded', 'true');
    await expect(suggestion(page, 'work', WORK.value)).toHaveText(`Work domain${WORK.label}`);
    await suggestion(page, 'work', WORK.value).click();

    await expect(chip(page, 'work', WORK.value)).toContainText(WORK.label);
    await expect(page.locator('#q')).toHaveValue('');
    await expect(page.locator('#suggestions')).toBeHidden();
    await expect(visibleCards(page)).toHaveCount(await workCount(page));
    await expect(page).toHaveURL(new RegExp(`\\?work=${WORK.value}$`));
  });

  test('turns an exact facet word into a chip on Enter', async ({ page }) => {
    await page.goto('/');
    await page.fill('#q', WORK.label);
    await page.keyboard.press('Enter');
    await expect(chip(page, 'work', WORK.value)).toBeVisible();
    await expect(page.locator('#q')).toHaveValue('');
    await expect(page).toHaveURL(new RegExp(`\\?work=${WORK.value}$`));
  });

  test('reaches a supervision level by its number', async ({ page }) => {
    await page.goto('/');
    await page.fill('#q', SUPERVISION.typed);
    await page.keyboard.press('Enter');
    await expect(chip(page, 'supervision', SUPERVISION.value)).toContainText(SUPERVISION.label);
    await expect(page).toHaveURL(new RegExp(`\\?supervision=${SUPERVISION.value}$`));
    await expect(visibleCards(page)).toHaveCount(
      await page.locator(`article.entry[data-supervision~="${SUPERVISION.value}"]`).count(),
    );
  });

  test('keeps other words as free text that must all match', async ({ page }) => {
    await page.goto('/');
    await page.fill('#q', 'internal coding');
    await page.keyboard.press('Enter');
    await expect(chips(page)).toHaveCount(0);
    await expect(page.locator('#q')).toHaveValue('internal coding');
    await expect(page).toHaveURL(/\?q=internal(\+|%20)coding$/);
    // Cards collapse before they are hidden, so let the list settle first.
    await expect(visibleCards(page)).not.toHaveCount(TOTAL);
    const count = await visibleCards(page).count();
    expect(count).toBeGreaterThan(0);
    expect(count).toBeLessThan(TOTAL);
    for (const text of await visibleCards(page).evaluateAll((nodes) =>
      nodes.map((node) => (node as HTMLElement).dataset.search ?? ''),
    )) {
      expect(text).toContain('coding');
      expect(text).toContain('internal');
    }
  });

  test('combines two values of one facet with OR', async ({ page }) => {
    await page.goto('/');
    await page.fill('#q', 'security');
    await page.keyboard.press('Enter');
    await page.fill('#q', 'coding');
    await page.keyboard.press('Enter');
    await expect(chips(page)).toHaveCount(2);
    await expect(page).toHaveURL(/\?work=security&work=coding$/);
    const either = await page
      .locator('article.entry[data-collection="agents"][data-work~="security"], article.entry[data-collection="agents"][data-work~="coding"]')
      .count();
    await expect(visibleCards(page)).toHaveCount(either);
  });

  test('filters structural type and invocation independently', async ({ page }) => {
    await page.goto(`/?type=agent&invocation=${INVOCATION.value}`);
    await expect(chip(page, 'type', 'agent')).toContainText('Agent');
    await expect(chip(page, 'invocation', INVOCATION.value)).toContainText(INVOCATION.label);
    const matching = await page
      .locator('article.entry[data-type~="agent"][data-invocation~="background"]')
      .count();
    await expect(visibleCards(page)).toHaveCount(matching);
  });

  test('combines repeated invocation values with OR', async ({ page }) => {
    await page.goto('/?invocation=background&invocation=scheduled');
    await expect(chips(page)).toHaveCount(2);
    const either = await page
      .locator('article.entry[data-invocation~="background"], article.entry[data-invocation~="scheduled"]')
      .count();
    await expect(visibleCards(page)).toHaveCount(either);
  });

  test('migrates the old task-agent type to agent', async ({ page }) => {
    await page.goto('/?type=task-agent');
    await expect(chip(page, 'type', 'agent')).toContainText('Agent');
    await expect(visibleCards(page)).toHaveCount(
      await page.locator('article.entry[data-type~="agent"]').count(),
    );
  });

  test('explains the old background-agent type and preserves other filters', async ({ page }) => {
    await page.goto(`/?type=background-agent&work=${WORK.value}`);
    await expect(page.locator('#legacy-filter-notice')).toBeVisible();
    await expect(page.locator('#legacy-filter-notice')).toContainText('Background invocation');
    await expect(chip(page, 'work', WORK.value)).toBeVisible();
    await expect(visibleCards(page)).toHaveCount(await workCount(page));
  });

  test('restores the state of a shared filtered address', async ({ page }) => {
    await page.goto(`/?work=${WORK.value}`);
    await expect(chip(page, 'work', WORK.value)).toBeVisible();
    await expect(visibleCards(page)).toHaveCount(await workCount(page));
  });

  test('ignores a filter value that the catalog does not use', async ({ page }) => {
    await page.goto('/?work=not-a-real-value');
    await expect(chips(page)).toHaveCount(0);
    await expect(visibleCards(page)).toHaveCount(TOTAL);
  });

  test('keeps the homepage canonical while a filter is applied', async ({ page }) => {
    await page.goto(`/?q=${SEARCH.term}&work=${WORK.value}`);
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute(
      'href',
      'https://internal-agents.com/',
    );
  });

  test('walks back and forward through the filter history', async ({ page }) => {
    await page.goto('/');
    await page.fill('#q', WORK.label);
    await page.keyboard.press('Enter');
    await expect(page).toHaveURL(new RegExp(`work=${WORK.value}`));
    await page.fill('#q', SUPERVISION.typed);
    await page.keyboard.press('Enter');
    await expect(visibleCards(page)).toHaveCount(
      await page
        .locator(
          `article.entry[data-collection="agents"][data-work~="${WORK.value}"][data-supervision~="${SUPERVISION.value}"]`,
        )
        .count(),
    );

    await page.goBack();
    await expect(chip(page, 'supervision', SUPERVISION.value)).toHaveCount(0);
    await expect(visibleCards(page)).toHaveCount(await workCount(page));

    await page.goBack();
    await expect(chips(page)).toHaveCount(0);
    await expect(visibleCards(page)).toHaveCount(TOTAL);

    await page.goForward();
    await expect(chip(page, 'work', WORK.value)).toBeVisible();
    await expect(visibleCards(page)).toHaveCount(await workCount(page));
  });

  test('removes a chip from its button and from Backspace', async ({ page }) => {
    await page.goto(`/?work=${WORK.value}&supervision=${SUPERVISION.value}`);
    await expect(chips(page)).toHaveCount(2);
    await chip(page, 'work', WORK.value).getByRole('button').click();
    await expect(chips(page)).toHaveCount(1);
    await expect(page).toHaveURL(new RegExp(`\\?supervision=${SUPERVISION.value}$`));

    await page.locator('#q').focus();
    await page.keyboard.press('Backspace');
    await expect(chips(page)).toHaveCount(0);
    await expect(page).toHaveURL(/\/$/);
    await expect(visibleCards(page)).toHaveCount(TOTAL);
  });

  test('explains an empty result and resets the search', async ({ page }) => {
    await page.goto(`/?work=${WORK.value}`);
    await page.fill('#q', 'nothing matches this text');
    await expect(visibleCards(page)).toHaveCount(0);
    await expect(page.locator('#empty')).toBeVisible();

    await page.locator('#empty button').click();
    await expect(visibleCards(page)).toHaveCount(TOTAL);
    await expect(page.locator('#empty')).toBeHidden();
    await expect(page.locator('#q')).toHaveValue('');
    await expect(chips(page)).toHaveCount(0);
    await expect(page).toHaveURL(/\/(\?.*)?$/);
    expect(new URL(page.url()).searchParams.get('q')).toBeNull();
    expect(new URL(page.url()).searchParams.get('work')).toBeNull();
  });

  test('works from the keyboard alone', async ({ page }) => {
    await page.goto('/');
    await page.locator('#q').focus();
    await page.keyboard.type(SEARCH.term);
    await page.keyboard.press('Enter');
    await expect(visibleCards(page)).toHaveCount(await searchCount(page));
    await expect(page).toHaveURL(new RegExp(`\\?q=${SEARCH.term}$`));

    await page.fill('#q', 'secu');
    await page.keyboard.press('ArrowDown');
    await expect(suggestion(page, 'work', WORK.value)).toHaveAttribute('aria-selected', 'true');
    await expect(page.locator('#q')).toHaveAttribute('aria-activedescendant', /suggestion-/);
    await page.keyboard.press('Enter');
    await expect(chip(page, 'work', WORK.value)).toBeVisible();
    await expect(page).toHaveURL(new RegExp(`\\?work=${WORK.value}$`));

    // Security is a chip now, so it leaves the list. Another prefix opens it again.
    await page.fill('#q', 'cod');
    await expect(page.locator('#suggestions')).toBeVisible();
    await page.keyboard.press('Escape');
    await expect(page.locator('#suggestions')).toBeHidden();
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

  test('captures the filtered and the empty directory', async ({ page }, testInfo) => {
    await page.goto(`/?work=${WORK.value}`);
    await page.screenshot({
      path: testInfo.outputPath('directory-filtered.png'),
      fullPage: true,
    });
    await page.fill('#q', 'nothing matches this text');
    await expect(page.locator('#empty')).toBeVisible();
    await page.screenshot({
      path: testInfo.outputPath('directory-empty.png'),
      fullPage: true,
    });
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
});
