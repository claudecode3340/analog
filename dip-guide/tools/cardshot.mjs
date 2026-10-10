import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, colorScheme: 'dark' });
await p.goto('file://' + process.argv[2], { waitUntil: 'load' }); await p.waitForTimeout(5000);
for (const id of process.argv.slice(3)) {
  const el = await p.$('#' + id); if (!el) { console.log('missing', id); continue; }
  await el.screenshot({ path: '/tmp/claude-0/card_' + id + '.png' });
}
await b.close();
