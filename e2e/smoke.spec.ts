/** Smoke test: every page loads, every lesson can be walked from "why" to "lock it in" without errors. */
import { expect, test } from '@playwright/test';

const LESSONS = ['u0-drops', 'u0-parallel', 'u1-mosfet', 'u2-pinchoff', 'u2-squarelaw', 'u3-recipe', 'u3-pmos-design', 'u4-gm', 'u4-ro', 'u5-cs'];

test.beforeEach(async ({ page }) => {
  page.on('pageerror', (e) => {
    throw e;
  });
});

for (const id of LESSONS) {
  test(`lesson ${id} walks through all 8 steps`, async ({ page }) => {
    const errors: string[] = [];
    page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(`#/learn/${id}`);
    for (let s = 0; s < 7; s++) {
      if (s === 2) await page.locator('.choice-card').first().click();
      await page.getByRole('button', { name: /^Next:/ }).click();
    }
    await expect(page.getByRole('heading', { name: 'Lock it in' })).toBeVisible();
    await expect(page.locator('.lockin')).toBeVisible();
    // Stepping back keeps the "Your turn" answers mounted.
    await page.getByRole('button', { name: 'Step 7: Your turn' }).click();
    await expect(page.locator('section.step-card:not([hidden]) .problem').first()).toBeVisible();
    await page.screenshot({ path: `test-results/shots/lesson-${id}-390.png`, fullPage: true });
    expect(errors).toEqual([]);
  });
}

for (const route of ['#/path', '#/learn', '#/labs', '#/labs/mosfet', '#/labs/dc', '#/practice', '#/review', '#/settings']) {
  test(`page ${route}`, async ({ page }) => {
    const errors: string[] = [];
    page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
    for (const width of [1280, 390]) {
      await page.setViewportSize({ width, height: 900 });
      await page.goto(route);
      await page.waitForTimeout(150);
      const scrollW = await page.evaluate(() => document.documentElement.scrollWidth);
      expect(scrollW, 'no horizontal page scroll').toBeLessThanOrEqual(width + 1);
      await page.screenshot({ path: `test-results/shots/page-${route.replace(/[#/]/g, '_')}-${width}.png`, fullPage: true });
    }
    expect(errors).toEqual([]);
  });
}

test('practice: a diagnosed mistake, then the right answer', async ({ page }) => {
  await page.goto('#/practice');
  await page.getByRole('button', { name: /WE1/ }).click();
  const input = page.getByLabel(/Drain current/);
  await input.fill('180u');
  await input.press('Enter');
  await expect(page.locator('.feedback.wrong').first()).toContainText('½');
  await input.fill('90 µA');
  await input.press('Enter');
  await expect(page.locator('.feedback.correct').first()).toBeVisible();
});

test('DC stepper reaches the fence check', async ({ page }) => {
  await page.goto('#/labs/dc');
  await page.getByRole('button', { name: 'Show all' }).click();
  await expect(page.locator('.fence-ok')).toBeVisible();
  await page.getByRole('button', { name: /Trap/ }).click();
  await page.getByRole('button', { name: 'Show all' }).click();
  await expect(page.locator('.fence-bad').first()).toBeVisible();
});
