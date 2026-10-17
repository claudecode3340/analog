// Visual check of one lesson in a built preview.
//   node tools/shot.js dist/preview-<ids>.html <lessonId> [outdir]
// Writes <outdir>/<lessonId>-NN.png (1440px wide, light theme, 1000px tall slices of the lesson),
// <lessonId>-dark.png and <lessonId>-phone.png; prints JS errors and horizontal-overflow problems.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const [, , file, lid, outd0] = process.argv; const outd = outd0 || path.join(__dirname, '..', 'build', 'shots');
  fs.mkdirSync(outd, { recursive: true });
  const b = await chromium.launch(); const errs = [];
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  p.on('pageerror', e => errs.push('PAGEERROR ' + e.message)); p.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE ' + m.text()); });
  await p.goto('file://' + path.resolve(file)); await p.waitForTimeout(800);
  // open all widgets/figures by scrolling through
  const box = await p.evaluate(id => { const s = document.getElementById(id); if (!s) return null; const r = s.getBoundingClientRect(); return { top: r.top + scrollY, h: r.height }; }, lid);
  if (!box) { console.log('lesson not found'); process.exit(1); }
  for (let y = box.top; y < box.top + box.h; y += 700) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(120); }
  let i = 0;
  for (let y = box.top; y < box.top + box.h; y += 1000) {
    await p.evaluate(y => scrollTo(0, y - 64), y); await p.waitForTimeout(250);
    await p.screenshot({ path: path.join(outd, `${lid}-${String(++i).padStart(2, '0')}.png`) });
  }
  await p.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark'));
  await p.evaluate(y => scrollTo(0, y + 900), box.top); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(outd, `${lid}-dark.png`) });
  await p.setViewportSize({ width: 390, height: 860 }); await p.evaluate(() => document.documentElement.setAttribute('data-theme', 'light'));
  await p.waitForTimeout(300);
  const over = await p.evaluate(id => { const s = document.getElementById(id); const bad = []; s.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (r.right > innerWidth + 1 && !e.closest('.katex,.katex-display,.tw,.code,.out,pre,.mrow,.steps>li>div,svg')) bad.push(e.tagName + '.' + e.className + ' ' + Math.round(r.right)); }); return { doc: document.documentElement.scrollWidth, bad: bad.slice(0, 12) }; }, lid);
  await p.evaluate(y => scrollTo(0, y), box.top); await p.waitForTimeout(200);
  await p.screenshot({ path: path.join(outd, `${lid}-phone.png`) });
  console.log(`${i} light slices written to ${outd}`);
  console.log('phone width check: document scrollWidth =', over.doc, '(must be 390)', over.bad.length ? 'overflowing: ' + over.bad.join(' | ') : 'no overflowing elements');
  console.log('errors:', errs.length ? errs.join('\n') : 'none');
  await b.close();
})();
