// ABOUTME: Collection browsing and infrastructure profiles remain usable without JavaScript.
import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';
const catalog = JSON.parse(readFileSync(new URL('../../data/agents.json', import.meta.url), 'utf8'));
const count = (section: string) => catalog.approaches.filter((item: any) => item.catalog_section === section).length;
for (const [path, section] of [['/', 'agents'], ['/infrastructure', 'infrastructure']]) {
  test(`${path} initially lists only ${section}, with a visible cross-collection link`, async ({ page }) => {
    await page.goto(path!);
    await expect(page.locator('article.entry:visible')).toHaveCount(count(section!));
    await expect(page.locator(`article.entry[data-collection="${section === 'agents' ? 'infrastructure' : 'agents'}"]:visible`)).toHaveCount(0);
    const menu = page.locator('.nav-toggle');
    if (await menu.isVisible()) await menu.click();
    await expect(page.locator('.sidebar a[href="/infrastructure"]')).toBeVisible();
    await expect(page.locator('.sidebar a[href="/"]')).toBeVisible();
  });
}
test('legacy platform and mixed-type queries switch to grouped All with OR semantics and history', async ({ page, javaScriptEnabled }) => {
  test.skip(javaScriptEnabled === false, 'URL filtering needs JavaScript; canonical indexes do not.');
  await page.goto('/?type=platform&type=agent');
  await expect(page.locator('[data-collection-group="infrastructure"]')).toBeVisible();
  await expect(page.locator('[data-collection-group="agents"]')).toBeVisible();
  await expect(page.locator('article.entry:visible')).toHaveCount(catalog.approaches.filter((item: any) => ['platform', 'agent'].includes(item.approach_type)).length);
  await page.locator('#q').fill('spectre');
  await expect(page.locator('article.entry:visible')).toHaveCount(1);
  await expect(page).toHaveURL(/collection=all/);
  await page.goBack();
  await expect(page.locator('#q')).toHaveValue('');
  await expect(page.locator('#directory-heading')).toHaveText('Agents and the infrastructure they run on.');
  await expect(page.locator('[data-collection-group="infrastructure"]')).toBeVisible();
  await expect(page.locator('[data-collection-group="agents"]')).toBeVisible();
});
test('local search stays scoped and All URLs search across collections', async ({ page, javaScriptEnabled }) => {
  test.skip(javaScriptEnabled === false);
  await page.goto('/?q=spectre');
  await expect(page.locator('article.entry[data-approach-id="harvey-spectre"]')).toBeHidden();
  await page.goto('/?collection=all&q=spectre');
  await expect(page.locator('article.entry[data-approach-id="harvey-spectre"]')).toBeVisible();
  await expect(page.locator('#q')).toHaveValue('spectre');
});
test('infrastructure has architecture first, stable claims, no agent attention levels, and Markdown parity', async ({ page, request }) => {
  await page.goto('/agents/harvey-spectre');
  const headings = await page.locator('.entry-section > h2').allTextContents();
  expect(headings.indexOf('Capabilities and architecture')).toBeLessThan(headings.indexOf('Documented uses'));
  await expect(page.locator('.entry-header')).not.toContainText('Human involvement');
  await expect(page.locator('#human-involvement')).not.toContainText('Level ');
  await expect(page.locator('.notice')).toHaveCount(0);
  for (const item of catalog.claims.filter((item: any) => item.approach_id === 'harvey-spectre')) {
    await expect(page.locator(`#claim-${item.id}`)).toHaveCount(1);
  }
  const text = await (await request.get('/agents/harvey-spectre.md')).text();
  expect(text).toContain('## Capabilities and architecture');
  expect(text).not.toContain('- Autonomy:');
  expect((await request.get('/infrastructure.md')).status()).toBe(200);
});
