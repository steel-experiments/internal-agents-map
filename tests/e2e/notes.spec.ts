// ABOUTME: Browser acceptance for the notes index, one note, and the two guides.
// ABOUTME: One project runs without JavaScript, so every reading path must work there.

import { expect, test, type Page } from '@playwright/test';

const NOTE_SLUGS = [
  'stop-a-run',
  'review-noise',
  'split-the-work',
  'work-can-continue',
  'load-tools',
  'steps-without-a-model',
  'test-on-your-work',
];

async function structuredData(page: Page): Promise<Record<string, unknown>> {
  const text = await page.locator('script[type="application/ld+json"]').innerText();
  return JSON.parse(text) as Record<string, unknown>;
}

/** HTML typography curls quotation marks; the export keeps the author's Markdown. */
function comparableProse(text: string): string {
  return text.replace(/\*\*/g, '').replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, ' ').trim();
}

/** Every fragment link on the page must reach an element of that page. */
async function assertFragmentsResolve(page: Page): Promise<void> {
  const fragments = await page
    .locator('a[href^="#"]')
    .evaluateAll((nodes) =>
      nodes.map((node) => (node as HTMLAnchorElement).getAttribute('href') ?? ''),
    );
  for (const fragment of fragments) {
    await expect(page.locator(fragment)).toHaveCount(1);
  }
}

test.describe('the notes index', () => {
  test('links to every note in the initial HTML', async ({ page }) => {
    const response = await page.goto('/notes');
    expect(response?.status()).toBe(200);
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('h1')).toHaveText('Notes');
    await expect(page).toHaveTitle('Notes · Internal Agents Map');
    await expect(page.locator('article.note-preview')).toHaveCount(NOTE_SLUGS.length);
    for (const slug of NOTE_SLUGS) {
      await expect(page.locator(`a[href="/notes/${slug}"]`).first()).toBeVisible();
    }
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute(
      'href',
      'https://internal-agents.com/notes',
    );
    await expect(page.locator('meta[name="description"]')).toHaveAttribute('content', /.{40,}/);
  });
});

test.describe('one note', () => {
  test('reads as a complete document with its diagram and sources', async ({ page }) => {
    const response = await page.goto('/notes/stop-a-run');
    expect(response?.status()).toBe(200);
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('h1')).toHaveText('When should an agent stop?');
    await expect(page).toHaveTitle('When should an agent stop? · Notes · Internal Agents Map');
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute(
      'href',
      'https://internal-agents.com/notes/stop-a-run',
    );
    await expect(page.locator('meta[property="og:type"]')).toHaveAttribute('content', 'article');
    await expect(page.locator('meta[name="robots"]')).toHaveCount(0);

    await expect(page.locator('figure.note-diagram')).toHaveCount(1);
    await expect(page.locator('.note-branches')).toContainText('Checks fail; budget remains');
    await expect(page.locator('.note-branches')).toContainText('Budget exhausted');
    await expect(page.locator('figure figcaption')).toContainText('proposed control flow');

    await expect(page.locator('#source-stripe')).toBeVisible();
    await expect(page.locator('.note-sources ol > li')).toHaveCount(3);
    await assertFragmentsResolve(page);
  });

  test('sends its catalog links to the entry pages', async ({ page }) => {
    await page.goto('/notes/stop-a-run');
    for (const id of ['stripe-minions', 'dropbox-nova', 'doordash-code-review']) {
      await expect(page.locator(`main a[href="/agents/${id}"]`)).toHaveCount(1);
    }
    await expect(page.locator('a[href*="index.html"]')).toHaveCount(0);
  });

  test('describes itself as an article for search engines', async ({ page }) => {
    await page.goto('/notes/stop-a-run');
    const graph = (await structuredData(page))['@graph'] as Array<Record<string, unknown>>;
    const article = graph.find((node) => node['@type'] === 'Article');
    expect(article?.url).toBe('https://internal-agents.com/notes/stop-a-run');
    expect(article?.headline).toBe('When should an agent stop?');
    expect(article?.datePublished).toBe('2026-09-11');
    expect(article?.dateModified).toBe('2026-09-16');
    expect(graph.map((node) => node['@type'])).toContain('BreadcrumbList');
  });

  test('offers a way back and a way on', async ({ page }) => {
    await page.goto('/notes/stop-a-run');
    await expect(page.locator('.note-next a[href="/notes"]')).toBeVisible();
    await page.locator('.note-next a[href="/notes/review-noise"]').click();
    await expect(page.locator('h1')).toHaveText('More comments can mean more work');
  });
});

test.describe('every note as a document', () => {
  for (const slug of NOTE_SLUGS) {
    test(`${slug} preserves its sources and structured content in the export`, async ({ page, request }) => {
      await page.goto(`/notes/${slug}`);
      await assertFragmentsResolve(page);
      const response = await request.get(`/notes/${slug}.md`);
      expect(response.status()).toBe(200);
      const markdown = comparableProse(await response.text());
      const article = page.locator('.note-detail > article');
      // Compare what is present, without requiring every article to use a diagram or quotation.
      const blocks = await article.locator('h1, h2, figure, th, td').allInnerTexts();
      for (const block of blocks) {
        expect(markdown).toContain(comparableProse(block));
      }
      const sources = await article.locator('.note-sources ol a').evaluateAll((links) =>
        links.map((link) => (link as HTMLAnchorElement).href),
      );
      for (const source of sources) expect(markdown).toContain(source);
      expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(
        (page.viewportSize()?.width ?? 0) + 1,
      );
    });
  }
});

test.describe('the entry page', () => {
  test('lists the notes that examine the implementation', async ({ page }) => {
    await page.goto('/agents/stripe-minions');
    const related = page.locator('#related');
    await expect(related.locator('a[href="/notes/stop-a-run"]')).toHaveCount(1);
    await expect(related.locator('a[href="/notes/steps-without-a-model"]')).toHaveCount(1);
  });
});

test.describe('the Definitions guide', () => {
  test('shows the chart with links to the entry pages and their claims', async ({ page }) => {
    const response = await page.goto('/definitions');
    expect(response?.status()).toBe(200);
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('h1')).toHaveText('What makes an agent internal?');
    await expect(page).toHaveTitle('What makes an agent internal? · Internal Agents Map');
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute(
      'href',
      'https://internal-agents.com/definitions',
    );

    const markers = page.locator('.quadrant-cell li[data-chart-approach-id]');
    expect(await markers.count()).toBeGreaterThan(0);
    await expect(
      page.locator('.quadrant-cell a[href="/agents/stripe-minions"]'),
    ).toHaveCount(1);
    await expect(
      page.locator(
        '.placement-notes a[href="/agents/stripe-minions#claim-stripe-minions--summary"]',
      ),
    ).toHaveCount(1);
    await expect(page.locator('a[href*="index.html"]')).toHaveCount(0);
  });

  test('keeps the diagrams in the initial HTML', async ({ page }) => {
    await page.goto('/definitions');
    await expect(page.locator('.scope-figure svg')).toHaveCount(2);
    await expect(page.locator('.place-panel')).toHaveCount(4);
    await expect(page.locator('.workflow-figure')).toHaveCount(1);
    await assertFragmentsResolve(page);
  });

  test('explains scoped supervision and separates type from invocation', async ({ page }) => {
    await page.goto('/definitions#supervision');
    await expect(page.locator('#supervision')).toBeVisible();
    // Boundaries, structural types, and invocation modes each state their own table.
    await expect(page.locator('#supervision .classification-table')).toHaveCount(3);
    await expect(page.locator('#supervision table').first().locator('tbody tr')).toHaveCount(5);
    await expect(page.locator('#supervision')).toContainText('Continuous steering');
    await expect(page.locator('#supervision')).toContainText('Exception-only');
    await expect(page.locator('#supervision')).toContainText('Approach types');
    await expect(page.locator('#supervision')).toContainText('Work modes');
  });
});

test.describe('the Methodology guide', () => {
  test('reads as a complete document', async ({ page }) => {
    const response = await page.goto('/methodology');
    expect(response?.status()).toBe(200);
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('h1')).toHaveText('Methodology');
    await expect(page).toHaveTitle('Methodology · Internal Agents Map');
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute(
      'href',
      'https://internal-agents.com/methodology',
    );
    await expect(page.locator('a[href="/definitions"]')).not.toHaveCount(0);
    await expect(page.locator('a[href="/notes"]')).not.toHaveCount(0);
    await expect(page.locator('main section')).toHaveCount(8);
  });
});
