// ABOUTME: Browser acceptance for the directory and the three difficult entry pages.
// ABOUTME: One project runs without JavaScript, so the reading path must not need it.

import { expect, test, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';

/** One organization record, as far as the entry header reads it. */
interface CatalogCompany {
  readonly id: string;
  readonly name: string;
  readonly logo: { readonly path: string } | null;
}

/** The committed catalog, so the spec follows the data. */
const CATALOG = JSON.parse(
  readFileSync(new URL('../../data/agents.json', import.meta.url), 'utf8'),
) as {
  approaches: ReadonlyArray<{ id: string; company_id: string; catalog_section: string; page_content: { questions: Record<string, { state: string }> } }>;
  companies: ReadonlyArray<CatalogCompany>;
  claims: ReadonlyArray<{ id: string; approach_id: string }>;
};
/** The number of implementations in the committed catalog. */
const TOTAL = CATALOG.approaches.length;
/** The organizations with a vendored logo, so their pages must show the image. */
const COMPANIES_WITH_LOGOS = CATALOG.companies.filter(
  (company): company is CatalogCompany & { logo: { readonly path: string } } =>
    company.logo !== null,
);
/** The organization behind one approach, so the mark follows the catalog. */
const companyOf = (approachId: string) => {
  const approach = CATALOG.approaches.find((candidate) => candidate.id === approachId);
  return CATALOG.companies.find((company) => company.id === approach?.company_id);
};

const ENTRIES = [
  {
    id: 'block-builderbot',
    heading: 'Builderbot',
    company: 'Block',
    /** The undefined meaning of an operation must stay beside the figure. */
    caveat: 'does not define an operation',
  },
  {
    id: 'uber-ureview',
    heading: 'uReview',
    company: 'Uber',
    caveat: 'conflicts and remains unresolved',
  },
  {
    id: 'plaid-internal-mcp-server',
    heading: 'Internal MCP server',
    company: 'Plaid',
    caveat: 'separate from internal MCP server adoption',
  },
] as const;

const PILOT_IDS = CATALOG.approaches.map((approach) => approach.id);
/** Records with workflow claims; other reviewed entries explain their absence. */
const WORKFLOW_REPORTED = new Set(
  (
    CATALOG.approaches as ReadonlyArray<{
      id: string;
      page_content?: { questions?: { workflow?: { state?: string } } };
    }>
  )
    .filter((approach) => approach.page_content?.questions?.workflow?.state === 'reported')
    .map((approach) => approach.id),
);

async function structuredData(page: Page): Promise<Record<string, unknown>> {
  const text = await page.locator('script[type="application/ld+json"]').innerText();
  return JSON.parse(text) as Record<string, unknown>;
}

test.describe('the directory', () => {
  test('links to every entry page in the initial HTML', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('h1')).toHaveText('How companies build internal AI agents');
    await expect(page.locator('#decisions a')).toHaveText([
      'When should an agent stop?',
      'Some steps do not need a model',
      'More comments can mean more work',
    ]);
    const cards = page.locator('article.entry[data-approach-id]');
    await expect(cards).toHaveCount(TOTAL);
    for (const entry of ENTRIES) {
      const card = page.locator(`article.entry#${entry.id}`);
      await expect(card).toHaveCount(1);
      await expect(card.locator(`a[href="/agents/${entry.id}"]`).first()).toHaveCount(1);
    }
  });

  test('reports a missing address as a real 404', async ({ page }) => {
    const response = await page.goto('/agents/not-a-real-entry');
    expect(response?.status()).toBe(404);
  });
});

for (const entry of ENTRIES) {
  test.describe(entry.id, () => {
    test('reads as a complete document', async ({ page }) => {
      const response = await page.goto(`/agents/${entry.id}`);
      expect(response?.status()).toBe(200);

      await expect(page.locator('h1')).toHaveCount(1);
      await expect(page.locator('h1')).toHaveText(entry.heading);
      await expect(page).toHaveTitle(new RegExp(`${entry.heading} at ${entry.company}`));

      const canonical = page.locator('link[rel="canonical"]');
      await expect(canonical).toHaveAttribute('href', `https://internal-agents.com/agents/${entry.id}`);
      await expect(page.locator('meta[name="description"]')).toHaveAttribute('content', /.{40,}/);
      // Every entry draws its own preview card; the query carries the hash of its content.
      await expect(page.locator('meta[property="og:image"]')).toHaveAttribute(
        'content',
        new RegExp(`^https://internal-agents\\.com/og/agents/${entry.id}\\.png\\?v=[0-9a-f]{8}$`),
      );
      await expect(page.locator('meta[name="robots"]')).toHaveCount(0);

      await expect(page.locator('#sources')).toBeVisible();
      await expect(page.locator('.page-back-end')).toBeVisible();
      if (entry.id !== 'plaid-internal-mcp-server') {
      await expect(
        page.locator('#human-involvement a[href="/definitions#supervision"]'),
      ).toHaveText('supervision definitions');
      }
      await expect(page.locator('a[href="/"]:visible').first()).toBeVisible();
    });

    test('keeps the material qualification beside its statement', async ({ page }) => {
      await page.goto(`/agents/${entry.id}`);
      await expect(page.getByText(entry.caveat).first()).toBeVisible();
    });

    test('keeps claim and source anchors', async ({ page }) => {
      await page.goto(`/agents/${entry.id}`);
      const claims = page.locator('[data-claim-id]');
      expect(await claims.count()).toBeGreaterThan(0);
      for (const id of await claims.evaluateAll((nodes) => nodes.map((node) => node.id))) {
        expect(id).toMatch(/^claim-/);
      }
      const sources = page.locator('ol.sources > li[data-source-id]');
      expect(await sources.count()).toBeGreaterThan(0);
      for (const id of await sources.evaluateAll((nodes) => nodes.map((node) => node.id))) {
        expect(id).toMatch(/^source-/);
      }
    });

    test('describes itself for search engines', async ({ page }) => {
      await page.goto(`/agents/${entry.id}`);
      const data = await structuredData(page);
      const graph = data['@graph'] as Array<Record<string, unknown>>;
      const types = graph.map((node) => node['@type']);
      expect(types).toContain('WebPage');
      expect(types).toContain('BreadcrumbList');
      expect(types).toContain('Organization');
      const webPage = graph.find((node) => node['@type'] === 'WebPage');
      expect(webPage?.url).toBe(`https://internal-agents.com/agents/${entry.id}`);
    });

    test('shows the sources as links to their publishers', async ({ page }) => {
      await page.goto(`/agents/${entry.id}`);
      const links = page.locator('ol.sources a.source-url');
      expect(await links.count()).toBeGreaterThan(0);
      for (const href of await links.evaluateAll((nodes) =>
        nodes.map((node) => (node as HTMLAnchorElement).href),
      )) {
        expect(href).toMatch(/^https:\/\//);
      }
    });
  });
}

test.describe('narrow entry pages', () => {
  test.use({ viewport: { width: 375, height: 812 } });

  for (const id of ['doordash-flux', 'posthog-stamphog', 'salesforce-slackbot', 'sentry-junior']) {
    test(`keeps ${id} within the viewport, including its research details`, async ({ page }) => {
      const response = await page.goto(`/agents/${id}`);
      expect(response?.status()).toBe(200);
      await page.evaluate(async () => {
        await document.fonts.ready;
      });

      const expectNoHorizontalOverflow = async () => {
        const contentWidth = await page.evaluate(() => document.documentElement.scrollWidth);
        expect(contentWidth).toBeLessThanOrEqual(page.viewportSize()!.width);
      };

      await expectNoHorizontalOverflow();
      await page.locator('details.claim-details > summary').filter({ hasText: 'Research details for every claim' }).click();
      await expect(page.locator('.ledger')).toBeVisible();
      await expectNoHorizontalOverflow();
    });
  }
});

test.describe('reported results', () => {
  test('renders reviewed observations with the statements of other kinds', async ({ page }) => {
    await page.goto('/agents/ramp-inspect');
    const results = page.locator('#results');
    const observations = results.getByRole('heading', { name: 'Reported observations' });
    await expect(observations).toBeVisible();
    const opinion = results.locator('.claim', { hasText: 'limited only by model-provider' });
    await expect(opinion).toHaveCount(1);
  });
});

test.describe('page-content pilot', () => {
  for (const [id, note] of [
    ['plaid-ai-annotator', 'The capture names no run.'],
    ['zup-codegen', 'no trigger-to-output sequence is described.'],
  ]) {
    test(`${id} explains its unreported workflow in HTML and Markdown`, async ({ page, request }) => {
      await page.goto(`/agents/${id}`);
      const workflow = page.locator('#how-it-works');
      await expect(workflow).toBeVisible();
      await expect(workflow).toContainText('Not reported');
      await expect(workflow).toContainText(note);
      await expect(workflow.locator('.claim')).toHaveCount(0);
      const markdown = await (await request.get(`/agents/${id}.md`)).text();
      const section = markdown.split('## How it works')[1]?.split('## Where people stay involved')[0];
      expect(section).toContain('Not reported');
      expect(section).toContain(note);
    });
  }

  test('keeps reported implementation notes beside their claims', async ({ page, request }) => {
    await page.goto('/agents/linear-agent');
    const note = 'Codex is named for internal pull-request review; the captures say only frontier language models elsewhere.';
    await expect(page.locator('#implementation .architecture-note', { hasText: note })).toBeVisible();
    expect(await (await request.get('/agents/linear-agent.md')).text()).toContain(note);
  });

  test('says why an architecture field is unreported, as the Markdown export does', async ({ page, request }) => {
    await page.goto('/agents/airbnb-airchat');
    const note = 'The captures describe internal context through MCP servers and configuration files, not a separate knowledge store.';
    await expect(page.locator('#implementation .is-unreported', { hasText: note })).toBeVisible();
    expect(await (await request.get('/agents/airbnb-airchat.md')).text()).toContain(note);
  });

  test('keeps Sentry code-size exclusions in the canonical observation', async ({ page, request }) => {
    await page.goto('/agents/sentry-junior');
    await expect(page.locator('#results')).toContainText('excluding tests, evals, docs, and lockfiles');
    const markdown = await (await request.get('/agents/sentry-junior.md')).text();
    expect(markdown.split('## Reported observations')[1]?.split('## Lessons')[0])
      .toContain('excluding tests, evals, docs, and lockfiles');
  });

  for (const id of PILOT_IDS) {
    test(`${id} exposes the reviewed reading order and exports`, async ({ page, request }) => {
      await page.goto(`/agents/${id}`);
      const record = CATALOG.approaches.find((item) => item.id === id)!;
      const questionBySection: Record<string, string> = { '#how-it-works': 'workflow', '#validation': 'validation', '#results': 'observations', '#lessons': 'lessons' };
      // A section that would only say nothing was reported is not rendered at all,
      // so validation and lessons appear where the evidence gives them something.
      const stateOf = (selector: string): string | undefined =>
        questionBySection[selector]
          ? record.page_content.questions[questionBySection[selector]!]?.state
          : undefined;
      const selectors = ['#purpose', '#how-it-works', '#human-involvement', '#implementation', '#validation', '#results', '#lessons', '#sources'].filter(
        (selector) =>
          !(record.catalog_section === 'infrastructure' && stateOf(selector) === 'not-applicable') &&
          !(['#validation', '#lessons'].includes(selector) && stateOf(selector) !== 'reported' && stateOf(selector) !== 'mixed'),
      );
      for (const selector of selectors) {
        await expect(page.locator(selector), selector).toBeVisible();
      }
      if (WORKFLOW_REPORTED.has(id)) {
        await expect(page.locator('#how-it-works .claim-label').first()).not.toBeEmpty();
      }
      await expect(page.locator('#purpose a[href="#sources"]')).toBeVisible();
      const ids = await page.locator('[data-claim-id]').evaluateAll((nodes) => nodes.map((node) => node.id));
      expect(new Set(ids).size).toBe(ids.length);
      expect([...ids].sort()).toEqual(CATALOG.claims.filter((claim) => claim.approach_id === id).map((claim) => `claim-${claim.id}`).sort());
      expect((await request.get(`/agents/${id}.md`)).status()).toBe(200);
    });
  }

  test('keeps lessons separate from YC’s reviewed empty observations state', async ({ page }) => {
    await page.goto('/agents/ycombinator-agent-infra');
    await expect(page.locator('#results')).toContainText('Not reported');
    await expect(page.locator('#results .claim')).toHaveCount(0);
    await expect(page.locator('#lessons .claim')).toHaveCount(2);
  });

  test('shows one reading-flow representation of Notion’s aliased count', async ({ page }) => {
    await page.goto('/agents/notion-custom-agents');
    await expect(page.locator('#results .claim', { hasText: 'More than 3,000 internal Custom Agents' })).toHaveCount(1);
    await page.locator('details.claim-details > summary').filter({ hasText: 'Research details for every claim' }).click();
    await expect(page.getByText('Duplicate representation of').first()).toBeVisible();
  });

  /*
   * One capture per record, rather than every record in one case. The list is
   * the whole catalog, so a single case grew with it until its captures no
   * longer fit the time a case is given; and a record that runs off the side
   * now names itself instead of stopping the run at whichever came first.
   */
  for (const id of PILOT_IDS) {
    test(`captures ${id} for desktop and mobile review`, async ({ page }, testInfo) => {
      test.skip(testInfo.project.name === 'no-javascript', 'Desktop and mobile captures cover visual review.');
      await page.goto(`/agents/${id}`);
      await page.evaluate(async () => document.fonts.ready);
      expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(page.viewportSize()!.width);
      // At the phone's device scale the long records exceed the height that Chromium can capture, so the capture uses CSS pixels.
      await page.screenshot({
        path: testInfo.outputPath(`pilot-${testInfo.project.name}-${id}.png`),
        fullPage: true,
        scale: 'css',
      });
    });
  }
});

test.describe('lesson attribution', () => {
  test('shows reported opinions and catalog interpretations without field labels', async ({ page }) => {
    await page.goto('/agents/strongdm-software-factory');
    await expect(
      page.locator('#claim-strongdm-software-factory--lessons-learned-2 .claim-attribution'),
    ).toHaveText('Reported opinion:');

    await page.goto('/agents/coinbase-forge-mux');
    await expect(
      page.locator('#claim-coinbase-forge-mux--lessons-learned-2 .claim-attribution'),
    ).toHaveText('Catalog interpretation:');
  });
});

test.describe('supporting systems', () => {
  test('show the reviewed workflow section and keep the invocation fact', async ({ page }) => {
    await page.goto('/agents/plaid-internal-mcp-server');
    await expect(page.locator('#how-it-works')).toBeVisible();
    await expect(page.locator('#how-it-works .claim-label').first()).not.toBeEmpty();
    const facts = page.locator('.entry-facts');
    await expect(facts).not.toContainText('Invocation');
    await expect(page.locator('#how-it-works h2')).toHaveText('Documented uses');
    await expect(facts.locator('div').filter({ has: page.locator('dt', { hasText: 'Approach type' }) }).locator('dd')).toHaveText('Component');
  });

  test('do not deny the workflow of a platform that reports one', async ({ page }) => {
    await page.goto('/agents/workos-project-horizon');
    await expect(page.locator('#how-it-works')).toBeVisible();
    await expect(page.locator('.entry-facts div').filter({ has: page.locator('dt', { hasText: 'Approach type' }) }).locator('dd')).toHaveText('Agent');
    await expect(page.getByText('no execution workflow')).toHaveCount(0);
  });

  test('keep the workflow section where the sources report a workflow', async ({ page }) => {
    await page.goto('/agents/block-builderbot');
    await expect(page.locator('#how-it-works')).toBeVisible();
    expect(await page.locator('#how-it-works .claim').count()).toBeGreaterThan(0);
  });
});

test.describe('page previews', () => {
  test('captures the directory and the three entries', async ({ page }, testInfo) => {
    test.skip(testInfo.project.name === 'no-javascript', 'One capture per layout is enough.');
    for (const path of ['/', ...ENTRIES.map((entry) => `/agents/${entry.id}`)]) {
      await page.goto(path);
      const name = path === '/' ? 'directory' : path.slice('/agents/'.length);
      await page.screenshot({
        path: testInfo.outputPath(`${name}.png`),
        fullPage: true,
        scale: 'css',
      });
    }
  });
});

test.describe('company marks', () => {
  test('leads the entry header with the company logo before the heading', async ({ page }) => {
    for (const entry of ENTRIES) {
      await page.goto(`/agents/${entry.id}`);
      const company = companyOf(entry.id);
      const mark = page.locator(
        `header.entry-header > span.company-logo[data-company-id="${company?.id ?? ''}"]`,
      );
      await expect(mark).toHaveCount(1);
      await expect(page.locator('header.entry-header > span.company-logo ~ h1')).toHaveCount(1);

      if (company?.logo) {
        await expect(mark.locator('img')).toHaveAttribute('src', `/${company.logo.path}`);
      } else {
        await expect(mark.locator('span.company-logo-monogram')).toBeVisible();
        await expect(mark.locator('img')).toHaveCount(0);
      }
    }
  });

  for (const company of COMPANIES_WITH_LOGOS) {
    test(`shows the logo image of ${company.name} on an entry page`, async ({ page }) => {
      const approach = CATALOG.approaches.find(
        (candidate) => candidate.company_id === company.id,
      );
      test.skip(!approach, 'A company without an approach has no entry page.');
      await page.goto(`/agents/${approach!.id}`);
      const mark = page.locator(
        `header.entry-header span.company-logo[data-company-id="${company.id}"]`,
      );
      await expect(mark.locator('img')).toHaveAttribute('src', `/${company.logo.path}`);
    });
  }
});
