import { chromium } from 'playwright';
const f = process.argv[2];
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const out = {};
for (const [name, vp] of [['desk', { width: 1440, height: 900 }], ['phone', { width: 390, height: 844 }]]) {
  const p = await b.newPage({ viewport: vp });
  const errs = []; p.on('pageerror', (e) => errs.push(String(e))); p.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + f, { waitUntil: 'load', timeout: 60000 });
  await p.waitForTimeout(6000);
  const r = await p.evaluate(() => {
    const ids = [...document.querySelectorAll('[id]')].map((e) => e.id); const dup = ids.filter((x, i) => ids.indexOf(x) !== i);
    const links = [...document.querySelectorAll('a[href^="#"]')].map((a) => a.getAttribute('href').slice(1)).filter((h) => h && !document.getElementById(h));
    return { mathjax: !!window.MathJax?.startup?.document, merr: document.querySelectorAll('mjx-merror, .mjx-merror, [data-mjx-error]').length, rawTeX: [...document.querySelectorAll('.prob')].filter((c) => /\\\(|\\\[/.test(c.innerText)).map((c) => c.id).slice(0, 20), dup: [...new Set(dup)].slice(0, 20), badLinks: [...new Set(links)], overflow: document.documentElement.scrollWidth - window.innerWidth, cards: document.querySelectorAll('.prob').length };
  });
  out[name] = { ...r, errs: errs.slice(0, 5) };
  for (const id of process.argv.slice(3)) { const el = await p.$('#' + id); if (el) { await el.evaluate((e) => e.querySelectorAll('details').forEach((d) => (d.open = true))); await el.screenshot({ path: `/tmp/claude-0/shot_${name}_${id}.png` }).catch((e) => console.log('shot fail', id, e.message)); } }
  await p.close();
}
console.log(JSON.stringify(out, null, 1));
await b.close();
