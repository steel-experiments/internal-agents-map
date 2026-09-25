// ABOUTME: Company pages preserve the shared design and connect existing catalog records.
import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';
const catalog = JSON.parse(readFileSync(new URL('../../data/agents.json', import.meta.url), 'utf8'));
for (const id of ['airbnb', 'harvey', 'stripe', 'databricks', 'y-combinator']) {
  test(`${id} publishes accurate groups, metadata and crawlable links`, async ({ page, request }) => {
    await page.goto(`/organizations/${id}`);
    const members = catalog.approaches.filter((entry: any) => entry.company_id === id);
    await expect(page.locator('article.entry')).toHaveCount(members.length);
    for (const entry of members) await expect(page.locator(`article.entry[data-approach-id="${entry.id}"] h3 a`)).toHaveAttribute('href', `/agents/${entry.id}`);
    for (const section of ['agents', 'infrastructure']) {
      await expect(page.locator(`#${section}-title`)).toHaveCount(members.some((entry: any) => entry.catalog_section === section) ? 1 : 0);
    }
    const website = new URL((await page.locator('.organization-website').getAttribute('href'))!);
    expect(website.searchParams.get('utm_source')).toBe('internal-agents.com');
    expect(website.searchParams.get('utm_campaign')).toBe('organization-profile');
    await expect(page.locator('.sidebar')).not.toContainText('Organizations');
    await expect(page.locator('.sidebar [aria-current="page"]')).toHaveCount(0);
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', `https://internal-agents.com/organizations/${id}`);
    await expect(page.locator('link[rel="alternate"][type="text/markdown"]')).toHaveAttribute('href', `https://internal-agents.com/organizations/${id}.md`);
    const markdown = await (await request.get(`/organizations/${id}.md`)).text();
    for (const entry of members) expect(markdown).toContain(`/agents/${entry.id}`);
    const sitemap = await (await request.get('/sitemap.xml')).text();
    expect(sitemap.split(`<loc>https://internal-agents.com/organizations/${id}</loc>`)).toHaveLength(2);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
    if (id === 'harvey') {
      await expect(page.locator('#connections')).toContainText('Related implementation');
      await expect(page.locator('#connections')).not.toContainText('Built on');
    }
  });
}
test('Company links support record to company to another record navigation', async ({ page }) => {
  await page.goto('/agents/airbnb-datako');
  await page.locator('.entry-facts a[href="/organizations/airbnb"]').click();
  await expect(page).toHaveURL(/\/organizations\/airbnb$/);
  await page.locator('#airbnb-pascal h3 a').click();
  await expect(page).toHaveURL(/\/agents\/airbnb-pascal$/);
});
test('unknown company is 404', async ({ request }) => {
  expect((await request.get('/organizations/not-a-company')).status()).toBe(404);
});
test('organization search remains the shared palette', async ({ page, javaScriptEnabled }) => {
  test.skip(javaScriptEnabled === false, 'The shared palette requires JavaScript.');
  await page.goto('/organizations/airbnb');
  await expect(page.locator('.search-launcher')).toHaveCount(1);
  for (let i = 0; i < 2; i++) {
    await page.keyboard.press('ControlOrMeta+k');
    await expect(page.getByRole('dialog')).toBeVisible();
    await page.keyboard.press('Escape');
    await expect(page.getByRole('dialog')).not.toBeVisible();
  }
});
