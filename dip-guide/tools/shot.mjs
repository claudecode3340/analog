import { chromium } from 'playwright';
const [f, ...ids] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, colorScheme: 'dark' });
const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
await p.goto('file://' + f, { waitUntil: 'load', timeout: 60000 });
await p.waitForTimeout(7000);
await p.addStyleTag({ content: '.topbar{position:static!important}' });
for (const id of ids) {
  const el = await p.$('#' + id);
  if (!el) { console.log('missing', id); continue; }
  const h = await el.evaluate((e) => e.getBoundingClientRect().height);
  await el.screenshot({ path: `/tmp/claude-0/s_${id}.png` });
  console.log(id, Math.round(h));
}
const sb = await p.evaluate(() => [...document.querySelectorAll('mjx-container,.eq')].filter((e) => e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflowX !== 'visible').length);
console.log('scrollable formulas:', sb, 'errors:', errs.slice(0, 3));
await b.close();
