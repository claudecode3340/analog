/* pd1 · pandas widget: .loc versus .iloc selector */
(function () {
  G.widget("pd1-lociloc", function (body) {
    var names = ["chevrolet chevelle malibu", "buick skylark 320", "plymouth satellite", "amc rebel sst", "ford torino", "ford galaxie 500"];
    var cols = ["mpg", "cylinders", "horsepower", "weight", "year"];
    var data = [[18, 8, 130, 3504, 70], [15, 8, 165, 3693, 70], [18, 8, 150, 3436, 70], [16, 8, 150, 3433, 70], [17, 8, 140, 3449, 70], [15, 8, 198, 4341, 70]];
    var selR = [1, 2, 3], selC = [0, 1, 2], mask = null;
    var bt = G.el("div", "ctrls"); bt.style.gap = "6px"; body.appendChild(bt);
    G.button(bt, "rows 1–3, mpg…horsepower", function () { selR = [1, 2, 3]; selC = [0, 1, 2]; mask = null; draw(); });
    G.button(bt, "ISLP: amc rebel sst, ford torino", function () { selR = [3, 4]; selC = [0, 2]; mask = null; draw(); });
    G.button(bt, "filter: mpg > 16", function () { mask = "mpg > 16"; selR = data.map(function (r, i) { return r[0] > 16 ? i : -1; }).filter(function (i) { return i >= 0; }); selC = [0, 3]; draw(); });
    G.button(bt, "clear", function () { selR = []; selC = []; mask = null; draw(); });
    var holder = G.el("div"); holder.style.cssText = "overflow-x:auto;margin:6px 0"; body.appendChild(holder);
    var code = G.el("pre"); code.style.cssText = "font:600 13.5px/1.65 var(--mono);background:var(--panel);color:var(--ink);padding:10px 12px;border-radius:10px;margin:8px 0;white-space:pre-wrap;word-break:break-word"; body.appendChild(code);
    var note = G.el("p"); note.style.cssText = "font-size:14px;color:var(--muted);margin:4px 0 0;line-height:1.5"; body.appendChild(note);
    function toggle(arr, v) { var i = arr.indexOf(v); if (i >= 0) arr.splice(i, 1); else { arr.push(v); arr.sort(function (a, b) { return a - b; }); } }
    function contiguous(a) { for (var i = 1; i < a.length; i++) if (a[i] !== a[i - 1] + 1) return false; return a.length > 1; }
    function q(s) { return '"' + s + '"'; }
    function draw() {
      var th = "padding:6px 9px;font:600 12px var(--mono);cursor:pointer;user-select:none;border-bottom:1px solid var(--line2);white-space:nowrap";
      var h = '<table style="border-collapse:separate;border-spacing:2px;font:13.5px var(--mono)"><thead><tr><th style="' + th + ';text-align:left;cursor:default;color:var(--faint)">pos · name (index)</th>';
      cols.forEach(function (c, j) { var on = selC.indexOf(j) >= 0; h += '<th data-c="' + j + '" style="' + th + ';text-align:right;' + (on ? "background:var(--hl2);border-radius:6px;" : "") + '">' + c + '<div style="font-weight:400;color:var(--faint);font-size:10.5px">' + j + "</div></th>"; });
      h += "</tr></thead><tbody>";
      data.forEach(function (r, i) {
        var on = selR.indexOf(i) >= 0;
        h += '<tr><td data-r="' + i + '" style="padding:5px 9px;cursor:pointer;user-select:none;white-space:nowrap;border-radius:6px;font-family:var(--body);font-size:13.5px;' + (on ? "background:var(--hl2);font-weight:600" : "") + '"><span style="color:var(--faint);font-family:var(--mono);font-size:11px">' + i + "</span> " + names[i] + "</td>";
        r.forEach(function (v, j) { var hit = on && selC.indexOf(j) >= 0; h += '<td style="padding:5px 9px;text-align:right;border-radius:6px;' + (hit ? "background:var(--hl1);font-weight:700" : "") + '">' + v + "</td>"; });
        h += "</tr>";
      });
      holder.innerHTML = h + "</tbody></table>";
      G.$$("[data-r]", holder).forEach(function (el) { el.onclick = function () { mask = null; toggle(selR, +el.dataset.r); draw(); }; });
      G.$$("[data-c]", holder).forEach(function (el) { el.onclick = function () { toggle(selC, +el.dataset.c); draw(); }; });
      if (!selR.length || !selC.length) { code.textContent = "# click row names and column names to select them"; note.textContent = ""; return; }
      var rL, rI, cL, cI;
      if (mask) { rL = 'df["mpg"] > 16'; rI = "(df['mpg'] > 16).to_numpy()"; }
      else if (contiguous(selR)) { rL = q(names[selR[0]]) + ":" + q(names[selR[selR.length - 1]]); rI = selR[0] + ":" + (selR[selR.length - 1] + 1); }
      else if (selR.length === 1) { rL = "[" + q(names[selR[0]]) + "]"; rI = "[" + selR[0] + "]"; }
      else { rL = "[" + selR.map(function (i) { return q(names[i]); }).join(", ") + "]"; rI = "[" + selR.join(", ") + "]"; }
      if (contiguous(selC)) { cL = q(cols[selC[0]]) + ":" + q(cols[selC[selC.length - 1]]); cI = selC[0] + ":" + (selC[selC.length - 1] + 1); }
      else { cL = "[" + selC.map(function (j) { return q(cols[j]); }).join(", ") + "]"; cI = "[" + selC.join(", ") + "]"; }
      code.textContent = "df.loc[" + rL + ", " + cL + "]\ndf.iloc[" + rI + ", " + cI + "]\n# result shape: (" + selR.length + ", " + selC.length + ")";
      var t = [];
      if (mask) t.push("A boolean condition works directly in <code>.loc</code>. <code>.iloc</code> needs plain True/False values, hence <code>.to_numpy()</code>; in practice you use <code>.loc</code> for conditions.");
      if (!mask && contiguous(selR)) t.push("Rows: the <code>.loc</code> slice ends <b>at</b> " + q(names[selR[selR.length - 1]]) + " (included); the <code>.iloc</code> slice stops <b>before</b> position " + (selR[selR.length - 1] + 1) + ".");
      if (contiguous(selC)) t.push("Columns: the same rule, <code>" + q(cols[selC[selC.length - 1]]) + "</code> is included in <code>.loc</code>, while <code>.iloc</code> stops before position " + (selC[selC.length - 1] + 1) + ".");
      if (!t.length) t.push("Lists pick exactly the labels or positions you name, in that order.");
      note.innerHTML = t.join(" ");
    }
    draw();
  });
})();
