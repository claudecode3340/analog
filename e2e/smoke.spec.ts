/** Smoke test: every page loads, every lesson can be walked from "why" to "lock it in" without errors. */
import { expect, test } from '@playwright/test';

const LESSONS = ['u0-drops', 'u0-parallel', 'u1-mosfet', 'u2-pinchoff', 'u2-squarelaw', 'u3-recipe', 'u3-pmos-design', 'u4-gm', 'u4-ro', 'u5-cs', 'u6-rules', 'u6-mirror', 'u7-loads', 'u7-degen', 'u8-follower', 'u8-cg', 'u9-cascode', 'u9-telescopic', 'u10-steering', 'u10-half', 'u10-cmrange', 'u11-ota', 'u11-ota-range', 'u12-poles', 'u12-settling', 'l1-gain', 'l1-speed', 'l1-other', 'l2-onestage', 'l2-buffer', 'l3-design', 'l3-scaling', 'l4-folding', 'l4-gain', 'l5-twostage', 'l6-boost', 'l7-cmfb', 'l8-cmfb', 'l8-replica', 'l9-slew', 'l10-psrr', 'l10-noise', 'l11-barkhausen', 'l11-multipole', 'l12-margins', 'l12-ringing', 'l13-dominant', 'l13-miller', 'l14-twostage', 'l14-rz', 'd15-statics', 'd16-loads', 'd17-cmos', 'd18-switching', 'd19-delaycalc', 'd20-gates', 'd21-cmoslogic', 'd22-euler', 'd23-rc', 'd24-linear', 'd25-path', 'd26-power', 'd27-staticdesign', 'd28-ratioed', 'd29-dynamic', 'd30-pass', 'd31-sequencing', 'd32-maxmin', 'd33-skew', 'd34-latches', 'd35-fulladder', 'd36-adders', 'd37-multiplier', 'd38-sram'];

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

for (const route of ['#/path', '#/learn', '#/labs', '#/labs/mosfet', '#/labs/dc', '#/labs/impedance', '#/labs/cs', '#/labs/cascode', '#/labs/diffpair', '#/labs/ota', '#/labs/feedback', '#/labs/headroom', '#/labs/folded', '#/labs/stability', '#/labs/inverter', '#/labs/effort', '#/practice', '#/review', '#/exam', '#/settings']) {
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
  await page.locator('summary', { hasText: 'Questions from our chat' }).click();
  await page.getByRole('button', { name: /WE1/ }).click();
  const input = page.getByLabel(/Drain current/);
  await input.fill('180u');
  await input.press('Enter');
  await expect(page.locator('.feedback.wrong').first()).toContainText('½');
  await input.fill('90 µA');
  await input.press('Enter');
  await expect(page.locator('.feedback.correct').first()).toBeVisible();
});

test('exam mode: start a paper, hand in, get marked', async ({ page }) => {
  await page.goto('#/exam');
  await page.getByRole('button', { name: /Quiz style/ }).click();
  await expect(page.locator('.exam-q')).toHaveCount(3);
  await page.getByRole('button', { name: 'Hand in' }).click();
  await expect(page.getByText(/Score \d+\/\d+/)).toBeVisible();
  await expect(page.locator('.exam-solution').first()).toBeVisible();
});

test('DC stepper reaches the fence check', async ({ page }) => {
  await page.goto('#/labs/dc');
  await page.getByRole('button', { name: 'Show all' }).click();
  await expect(page.locator('.fence-ok')).toBeVisible();
  await page.getByRole('button', { name: /Trap/ }).click();
  await page.getByRole('button', { name: 'Show all' }).click();
  await expect(page.locator('.fence-bad').first()).toBeVisible();
});
