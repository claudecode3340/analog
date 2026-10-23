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
      if (isEx) {
        const sb = await p.$(`#${id} button:has-text("Show solution")`); if (sb) await sb.click();
        await p.waitForTimeout(150);
        const cb = await p.$(`#${id} .cbtn.check`); await cb.click();
      } else {
        const rb = await p.$(`#${id} .cbtn.run`); await rb.click();
      }
      try {
        await p.waitForFunction(([id, isEx]) => { const c = document.getElementById(id); const o = c.querySelector('.out'); if (!o) return false; const t = o.textContent;
          if (/Running|Starting|Loading|Installing/.test(t) && !/Stopped after/.test(t)) return false;
          return isEx ? /All tests passed|Not yet|Error|Traceback|Stopped/.test(t) || !!o.querySelector('pre.err') : (o.children.length > 0 && !o.querySelector('.spin')); }, [id, isEx], { timeout: 300000, polling: 300 });
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
