import { chromium } from '../tools/node_modules/playwright-core/index.mjs';
import fs from 'fs';
const dir = process.cwd();
const hdr = fs.readFileSync(dir + '/figs/hdr.svg').toString('base64');
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome', args: ['--no-sandbox'] });
const page = await browser.newPage();
await page.goto('file://' + dir + '/guide.html', { waitUntil: 'networkidle' });
await page.waitForFunction(() => window.__done === true);
await page.evaluate(() => document.fonts.ready);
const headerTemplate = `<div style="width:100%;padding:0 10mm;margin-top:4mm;box-sizing:border-box;">
  <div style="border:1px solid #e2e0da;border-radius:2mm;padding:1.2mm 2mm;background:#fafaf8;">
  <img src="data:image/svg+xml;base64,${hdr}" style="width:100%;display:block"></div></div>`;
const footerTemplate = `<div style="width:100%;font-family:Inter,sans-serif;font-size:7.5pt;color:#8a8984;padding:0 17mm;display:flex;justify-content:space-between">
  <span>Analog Lab · Lectures 23–25 · CMOS inverter</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`;
await page.pdf({ path: dir + '/out.pdf', format: 'A4', printBackground: true, displayHeaderFooter: true, headerTemplate, footerTemplate, preferCSSPageSize: true });
await browser.close();
