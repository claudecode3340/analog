// Smoke test: node tools/smoke.js dist/preview.html
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async()=>{const f=process.argv[2]; const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1440,height:900}});
const errs=[]; p.on('pageerror',e=>errs.push('PAGEERR '+e.message)); p.on('console',m=>{if(m.type()==='error')errs.push('CONSOLE '+m.text())});
await p.goto('file://'+require('path').resolve(f)); await p.waitForTimeout(1200);
await p.screenshot({path:'build/shots/top.png'});
// run first cell
const cell=await p.$('.py'); await (await cell.$('.cbtn.run')).click();
await p.waitForFunction(()=>{const o=document.querySelector('.py .out');return o&&!/Running|Starting/.test(o.textContent)},null,{timeout:240000});
console.log('cell1 out:',(await p.$eval('.py .out',e=>e.textContent)).slice(0,200));
// ISLP inside the browser
await p.evaluate(()=>{const ta=document.querySelector('.py textarea');ta.value="from ISLP import load_data\nimport statsmodels.api as sm\nAuto=load_data('Auto')\nprint(Auto.shape)\nAuto.head(3)";ta.dispatchEvent(new Event('input'))});
await (await cell.$('.cbtn.run')).click();
await p.waitForFunction(()=>{const o=document.querySelector('.py .out');return o&&!/Running/.test(o.textContent)&&o.textContent.length>5},null,{timeout:240000});
console.log('ISLP out:',(await p.$eval('.py .out',e=>e.textContent)).slice(0,300));
// exercise with solution
const ex=await p.$('div.ex'); await p.evaluate(()=>{const ta=document.querySelector('div.ex textarea');ta.value="def double(x):\n    return x*2";ta.dispatchEvent(new Event('input'))});
await (await ex.$('.cbtn.check')).click(); await p.waitForFunction(()=>/passed|Not yet|Error/.test(document.querySelector('div.ex .out').textContent),null,{timeout:120000});
console.log('exercise:',(await p.$eval('div.ex .out',e=>e.textContent)).slice(0,120));
await ex.scrollIntoViewIfNeeded(); await p.screenshot({path:'build/shots/ex.png'});
const w=await p.$('.worked'); await w.scrollIntoViewIfNeeded(); await p.screenshot({path:'build/shots/worked.png'});
console.log('errors',JSON.stringify(errs)); await b.close();})();
