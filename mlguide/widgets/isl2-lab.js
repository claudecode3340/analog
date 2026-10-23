/* isl2-lab · slice a string; which entries does an index pick */
(function () {
  function box(parent, html) { var d = G.el("div", "", html); d.style.cssText = "display:flex;flex-wrap:wrap;gap:4px;margin:10px 0 6px;justify-content:center"; parent.appendChild(d); return d; }
  function cell(t, on, sub) {
    var c = G.el("div", "", "<div style='font:600 18px var(--mono)'>" + (t === " " ? "␣" : t) + "</div><div style='font:11px var(--mono);color:var(--muted)'>" + sub + "</div>");
    c.style.cssText = "min-width:30px;padding:6px 4px;text-align:center;border-radius:8px;border:1px solid var(--line);" + (on ? "background:var(--accent);color:#fff;border-color:var(--accent)" : "background:var(--panel)");
    if (on) c.lastChild.style.color = "#fff";
    return c;
  }
  G.widget("isl2-lab-slice", function (body) {
    var s = "hello world", st = { a: 3, b: 6, c: 1 };
    var ctl = G.el("div", "ctrls"); body.appendChild(ctl);
    G.slider(ctl, { label: "start", min: 0, max: 11, value: 3, onChange: function (v) { st.a = v; draw(); } });
    G.slider(ctl, { label: "stop", min: 0, max: 11, value: 6, onChange: function (v) { st.b = v; draw(); } });
    G.slider(ctl, { label: "step", min: 1, max: 4, value: 1, onChange: function (v) { st.c = v; draw(); } });
    var row = box(body, ""), info = G.el("div", "readout"); body.appendChild(info);
    function draw() {
      row.innerHTML = ""; var out = "";
      for (var i = 0; i < s.length; i++) { var on = i >= st.a && i < st.b && (i - st.a) % st.c === 0; if (on) out += s[i]; row.appendChild(cell(s[i], on, i)); }
      var code = '"hello world"[' + st.a + ":" + st.b + (st.c > 1 ? ":" + st.c : "") + "]";
      info.innerHTML = "<div>code<b>" + code + "</b></div><div>result<b>'" + out.replace(/ /g, "␣") + "'</b></div><div>length<b>" + out.length + "</b></div>";
    }
    draw();
  });

  G.widget("isl2-lab-index", function (body) {
    var A = []; for (var i = 0; i < 16; i++) A.push(i);
    function pairs(rs, cs) { return rs.map(function (r, k) { return [r, cs[k]]; }); }
    function mesh(rs, cs) { var o = []; rs.forEach(function (r) { cs.forEach(function (c) { o.push([r, c]); }); }); return o; }
    var EX = [
      ["A[1, 2]", [[1, 2]], "6", "one entry: row 1, column 2"],
      ["A[[1, 3]]", mesh([1, 3], [0, 1, 2, 3]), "[[4, 5, 6, 7], [12, 13, 14, 15]]", "a list of rows"],
      ["A[:, [0, 2]]", mesh([0, 1, 2, 3], [0, 2]), "[[0, 2], [4, 6], [8, 10], [12, 14]]", "all rows, columns 0 and 2"],
      ["A[[1, 3], [0, 2]]", pairs([1, 3], [0, 2]), "[4, 14]", "two lists are PAIRED: (1,0) and (3,2), a 1-D result"],
      ["A[np.ix_([1, 3], [0, 2])]", mesh([1, 3], [0, 2]), "[[4, 6], [12, 14]]", "np.ix_ makes every row × every column"],
      ["A[1:4:2, 0:3:2]", mesh([1, 3], [0, 2]), "[[4, 6], [12, 14]]", "two slices always give a block"],
      ["A[np.ix_([1, 3], [0, 2, 3])]", mesh([1, 3], [0, 2, 3]), "[[4, 6, 7], [12, 14, 15]]", "rows 1, 3 × columns 0, 2, 3"],
      ["A[keep_rows]", mesh([1, 3], [0, 1, 2, 3]), "[[4, 5, 6, 7], [12, 13, 14, 15]]", "Boolean mask [F, T, F, T] keeps rows 1 and 3"]
    ];
    var st = 3, ctl = G.el("div", ""); ctl.style.cssText = "display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px"; body.appendChild(ctl);
    var btns = EX.map(function (e, k) { return G.button(ctl, e[0], function () { st = k; draw(); }); });
    var grid = G.el("div", ""); grid.style.cssText = "display:grid;grid-template-columns:repeat(4,52px);gap:5px;justify-content:center;margin:8px auto"; body.appendChild(grid);
    var info = G.el("div", "readout"); body.appendChild(info);
    function draw() {
      btns.forEach(function (b, k) { b.style.outline = k === st ? "2px solid var(--accent)" : ""; });
      grid.innerHTML = ""; var sel = EX[st][1];
      A.forEach(function (v) {
        var r = Math.floor(v / 4), c = v % 4, k = -1; sel.forEach(function (p, j) { if (p[0] === r && p[1] === c) k = j; });
        var d = G.el("div", "", String(v)); d.style.cssText = "height:44px;display:flex;align-items:center;justify-content:center;border-radius:8px;font:600 16px var(--mono);border:1px solid var(--line);" + (k >= 0 ? "background:var(--accent);color:#fff" : "background:var(--panel);color:var(--muted)");
        grid.appendChild(d);
      });
      info.innerHTML = "<div>expression<b>" + EX[st][0] + "</b></div><div>result<b>" + EX[st][2] + "</b></div><div>why<b style='font-size:14px'>" + EX[st][3] + "</b></div>";
    }
    draw();
  });
})();
