import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage();
await p.goto('file://' + process.argv[2], { waitUntil: 'domcontentloaded' });
await p.waitForTimeout(500);
const r = await p.evaluate(() => {
  document.querySelectorAll('details').forEach((d) => (d.open = true));
  return [...document.querySelectorAll('.prob')].map((c) => {
    const q = c.querySelector('.stmt'); const a = c.querySelector('.s-ans'); const sol = c.querySelector('.s-sol');
    return `##### ${c.id} | ${c.querySelector('.src')?.innerText} | ${c.querySelector('h4')?.innerText}\nQ: ${q ? q.innerText : '?'}\nA: ${a ? a.innerText.replace(/^Final answer\s*/, '') : '?'}\n`;
  }).join('\n');
});
console.log(r);
await b.close();
