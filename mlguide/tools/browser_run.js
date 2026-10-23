// Runs every cell (and every exercise's solution) of the given lessons in the REAL browser (Pyodide),
// top to bottom, and reports any cell whose result differs from the harness's expectation.
//   node tools/browser_run.js dist/preview-<ids>.html <lid> [<lid> ...]
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const path = require('path');
(async () => {
  const [, , file, ...lids] = process.argv;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.resolve(file), { timeout: 180000 }); await p.waitForTimeout(1500);
  let bad = 0;
  for (const lid of lids) {
    const ids = await p.evaluate(lid => [...document.querySelectorAll('#' + CSS.escape(lid) + ' .py, #' + CSS.escape(lid) + ' div.ex')].filter(e => e.dataset.mode !== 'local').map(e => e.id), lid);
    let n = 0; const t0 = Date.now();
    for (const id of ids) {
      const isEx = await p.evaluate(id => document.getElementById(id).classList.contains('ex'), id);
      await p.evaluate(id => { const c = document.getElementById(id); c.scrollIntoView(); const o = c.querySelector('.out'); if (o) o.dataset.prev = '1'; }, id);
      const btn = isEx ? '.cbtn.check' : '.cbtn.run';
      if (isEx) await p.evaluate(id => { const c = document.getElementById(id); const tas = c.querySelectorAll('textarea'); const sol = c.querySelector('.solwrap textarea'); tas[0].value = sol.value; tas[0].dispatchEvent(new Event('input')); }, id);
      await p.evaluate(([id, btn]) => { const c = document.getElementById(id); c.dataset.gated = '0'; c.querySelector(btn).click(); }, [id, btn]);
      try {
        await p.waitForFunction(([id, btn]) => { const b = document.querySelector('#' + id + ' ' + btn); return b && !b.disabled; }, [id, btn], { timeout: 300000, polling: 300 });
      } catch (e) { console.log(`[${lid}] TIMEOUT ${id}`); bad++; continue; }
      await p.waitForTimeout(100);
      const r = await p.evaluate(([id, isEx]) => { const c = document.getElementById(id); const o = c.querySelector('.out'); const err = o.querySelector('pre.err');
        if (isEx) return /All tests passed/.test(o.textContent) ? null : o.textContent.slice(0, 400);
        if (c.dataset.error) return /This error is the point/.test(o.textContent) ? null : 'expected error not shown: ' + o.textContent.slice(0, 300);
        return err ? err.textContent.slice(0, 400) : null; }, [id, isEx]);
      n++; if (r) { bad++; console.log(`[${lid}] PROBLEM ${id}: ${r}`); }
    }
    console.log(`[${lid}] ran ${n}/${ids.length} in browser in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  console.log(bad ? `BROWSER PROBLEMS: ${bad}` : 'BROWSER ALL GOOD', errs.length ? 'page errors: ' + errs.join(' | ') : '');
  await b.close();
})();
