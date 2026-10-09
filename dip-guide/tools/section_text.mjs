import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage();
await p.goto('file://' + process.argv[2], { waitUntil: 'domcontentloaded' });
const r = await p.evaluate((id) => { document.querySelectorAll('details').forEach((d) => (d.open = true)); const s = document.getElementById(id); return s.innerText; }, process.argv[3]);
console.log(r);
await b.close();
