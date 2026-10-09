import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: +process.argv[3] || 1440, height: 900 } });
await p.goto('file://' + process.argv[2], { waitUntil: 'load' }); await p.waitForTimeout(6000);
const r = await p.evaluate(() => { const W = document.documentElement.clientWidth; const out = []; document.querySelectorAll('main *').forEach((e) => { const rc = e.getBoundingClientRect(); if (rc.right > W + 2 && rc.width > 0) { const sec = e.closest('section')?.id; out.push(sec + ' ' + e.tagName + '.' + (e.className?.baseVal ?? e.className) + ' ' + Math.round(rc.right - W)); } }); return [...new Set(out)].slice(0, 25); });
console.log(r.join('\n')); await b.close();
