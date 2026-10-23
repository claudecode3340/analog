/* np2 · NumPy II widgets: broadcasting visualiser, matrix-vector stepper, distance matrix */
(function () {
  function mgrid(R, C, cell) {
    var s = '<span class="mgrid" style="grid-template-columns:repeat(' + C + ',auto)">';
    for (var i = 0; i < R; i++) for (var j = 0; j < C; j++) s += cell(i, j);
    return s + "</span>";
  }
  function shp(s) { return "(" + s.join(", ") + (s.length === 1 ? "," : "") + ")"; }

  G.widget("np2-broadcast", function (body) {
    var As = { "3,4": [3, 4], "3,1": [3, 1], "1,4": [1, 4], "4": [4], "2,3": [2, 3] };
    var Bs = { "s": [], "4": [4], "3": [3], "1,4": [1, 4], "3,1": [3, 1], "2,1": [2, 1] };
    var a = "3,4", b = "4";
    var c1 = G.el("div", "ctrls"); body.appendChild(c1);
    c1.appendChild(G.el("span", "", "<b style='font-size:13px;color:var(--muted)'>A</b>"));
    G.seg(c1, Object.keys(As).map(function (k) { return [k, shp(As[k])]; }), a, function (v) { a = v; draw(); });
    var c2 = G.el("div", "ctrls"); body.appendChild(c2);
    c2.appendChild(G.el("span", "", "<b style='font-size:13px;color:var(--muted)'>B</b>"));
    G.seg(c2, Object.keys(Bs).map(function (k) { return [k, k === "s" ? "scalar" : shp(Bs[k])]; }), b, function (v) { b = v; draw(); });
    var expr = G.el("div"); expr.style.cssText = "font:700 16px var(--mono);margin:4px 0 8px;color:var(--tool)"; body.appendChild(expr);
    var rules = G.el("div"); body.appendChild(rules);
    var pics = G.el("div", "mrow"); body.appendChild(pics);
    var msg = G.el("p"); msg.style.cssText = "font-size:14.5px;line-height:1.55;margin:8px 0 0"; body.appendChild(msg);
    function draw() {
      var sa = As[a], sb = Bs[b];
      expr.textContent = "np.arange(" + sa.reduce(function (p, q) { return p * q; }, 1) + ").reshape" + shp(sa) + "  +  " + (sb.length ? "B" + shp(sb) : "100");
      var pa = sa.slice(), pb = sb.slice();
      while (pa.length < 2) pa.unshift(1); while (pb.length < 2) pb.unshift(1);
      var ok = true, out = [], why = [];
      for (var k = 0; k < 2; k++) {
        var x = pa[k], y = pb[k];
        if (x === y) { out.push(x); why.push("equal"); }
        else if (x === 1) { out.push(y); why.push("A stretches 1 → " + y); }
        else if (y === 1) { out.push(x); why.push("B stretches 1 → " + x); }
        else { ok = false; out.push("✗"); why.push(x + " vs " + y + ": mismatch"); }
      }
      var padA = sa.length < 2 ? ' <span style="color:var(--faint)">(padded on the left)</span>' : "";
      var padB = sb.length < 2 ? ' <span style="color:var(--faint)">(padded on the left)</span>' : "";
      var td = 'style="font-family:var(--mono);text-align:center;padding:6px 10px"';
      rules.innerHTML = '<div class="tw" style="margin:6px 0"><table class="t"><thead><tr><th></th><th>axis 0</th><th>axis 1</th><th></th></tr></thead><tbody>' +
        "<tr><td>A " + shp(sa) + "</td><td " + td + ">" + pa[0] + "</td><td " + td + ">" + pa[1] + "</td><td>" + padA + "</td></tr>" +
        "<tr><td>B " + (sb.length ? shp(sb) : "scalar ()") + "</td><td " + td + ">" + pb[0] + "</td><td " + td + ">" + pb[1] + "</td><td>" + padB + "</td></tr>" +
        "<tr><td><b>check</b></td>" + why.map(function (w) { var bad = /mismatch/.test(w); return '<td style="text-align:center;font-size:13px;color:var(' + (bad ? "--bad" : "--good") + ');font-weight:600">' + (bad ? "✗ " : "✓ ") + w + "</td>"; }).join("") + "<td></td></tr>" +
        "<tr><td><b>result</b></td><td " + td + "><b>" + out[0] + "</b></td><td " + td + "><b>" + out[1] + "</b></td><td></td></tr></tbody></table></div>";
      if (!ok) {
        pics.innerHTML = "";
        var bad = why.findIndex(function (w) { return /mismatch/.test(w); });
        msg.innerHTML = '<b style="color:var(--bad)">ValueError: operands could not be broadcast together with shapes ' + shp(sa).replace(/ /g, "") + " " + (sb.length ? shp(sb).replace(/ /g, "") : "()") + ".</b> On axis " + bad + " the sizes are " + pa[bad] + " and " + pb[bad] + ": they are not equal and neither is 1, so NumPy cannot stretch one to fit the other." +
          (b === "3" && a === "3,4" ? " You meant one number per <i>row</i>: make B a column with <code>v[:, None]</code>, shape (3, 1)." : "");
        return;
      }
      var R = out[0], C = out[1];
      var vA = function (i, j) { return (pa[0] === 1 ? 0 : i) * pa[1] + (pa[1] === 1 ? 0 : j); };
      var vB = function (i, j) { return sb.length ? 10 * ((pb[0] === 1 ? 0 : i) * pb[1] + (pb[1] === 1 ? 0 : j) + 1) : 100; };
      function stretched(p, val, cls) {
        return mgrid(R, C, function (i, j) {
          var virt = (p[0] === 1 && i > 0) || (p[1] === 1 && j > 0);
          return '<span class="' + cls + '" style="' + (virt ? "opacity:.42;outline:1.5px dashed var(--line2);outline-offset:-3px" : "") + '">' + val(i, j) + "</span>";
        });
      }
      pics.innerHTML = '<span>' + stretched(pa, vA, "h1") + '<span class="lab">A stretched to (' + R + ", " + C + ')</span></span><span class="op">+</span><span>' +
        stretched(pb, vB, "h2") + '<span class="lab">B stretched to (' + R + ", " + C + ')</span></span><span class="op">=</span><span>' +
        mgrid(R, C, function (i, j) { return "<span>" + (vA(i, j) + vB(i, j)) + "</span>"; }) + '<span class="lab">result ' + shp(sa.length === 1 && sb.length <= 1 ? [C] : [R, C]) + "</span></span>";
      msg.innerHTML = "Faded, dashed cells are <b>virtual copies</b>: NumPy reuses the same number without copying memory. " +
        (sa.length === 1 && sb.length <= 1 ? "Both inputs are 1-D, so the result is 1-D too (drawn as one row)." : "Result shape <b>(" + R + ", " + C + ")</b>.");
    }
    draw();
  });

  G.widget("np2-matvec", function (body) {
    var A = [[2, 1], [1, 3], [0, 4]], x = [1, 2], step = 0;
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    var s0 = G.slider(ctr, { label: "x₀", min: -3, max: 3, step: 1, value: 1, onChange: function (v) { x[0] = v; draw(); } });
    var s1 = G.slider(ctr, { label: "x₁", min: -3, max: 3, step: 1, value: 2, onChange: function (v) { x[1] = v; draw(); } });
    var bt = G.el("div", "ctrls"); body.appendChild(bt);
    G.button(bt, "Next row →", function () { step = Math.min(3, step + 1); draw(); });
    G.button(bt, "Show all", function () { step = 3; draw(); });
    G.button(bt, "Reset", function () { step = 0; draw(); });
    var pic = G.el("div", "mrow"); body.appendChild(pic);
    var calc = G.el("div"); calc.style.cssText = "font:600 16px var(--mono);margin:8px 0;min-height:1.5em;color:var(--ink)"; body.appendChild(calc);
    function draw() {
      var cur = step >= 1 && step <= 3 ? step - 1 : -1;
      var y = A.map(function (r) { return r[0] * x[0] + r[1] * x[1]; });
      pic.innerHTML = '<span>' + mgrid(3, 2, function (i, j) { return '<span class="' + (i === cur ? "h1" : "") + '">' + A[i][j] + "</span>"; }) + '<span class="lab">A (3 × 2)</span></span><span class="op">@</span><span>' +
        mgrid(2, 1, function (i) { return '<span class="' + (cur >= 0 ? "h2" : "") + '">' + x[i] + "</span>"; }) + '<span class="lab">x (2)</span></span><span class="op">=</span><span>' +
        mgrid(3, 1, function (i) { return '<span class="' + (i === cur ? "h4" : "") + '">' + (i < step ? y[i] : "?") + "</span>"; }) + '<span class="lab">A @ x (3)</span></span>';
      if (cur < 0) calc.innerHTML = step === 0 ? '<span style="color:var(--muted);font-weight:500;font-family:var(--body)">Press “Next row” to compute the first entry.</span>' : "";
      else {
        var r = A[cur];
        calc.innerHTML = "row " + cur + ": " + r[0] + "·" + (x[0] < 0 ? "(" + x[0] + ")" : x[0]) + " + " + r[1] + "·" + (x[1] < 0 ? "(" + x[1] + ")" : x[1]) + " = " + r[0] * x[0] + " + " + r[1] * x[1] + " = <b style='color:var(--good)'>" + y[cur] + "</b>";
      }
      if (step === 3) calc.innerHTML += '<div style="font:500 14px var(--body);color:var(--muted);margin-top:4px">All three rows done: A @ x = [' + y.join(", ") + "]. Each entry is one dot product.</div>";
    }
    draw();
  });

  G.widget("np2-dist", function (body) {
    var r = G.rng(7), train = [], test = [[2, 7.5], [5.5, 3], [8.5, 8]];
    for (var i = 0; i < 6; i++) train.push([1 + r() * 8, 1 + r() * 8]);
    var pl = G.plot(body, { w: 520, h: 360, x: [0, 10], y: [0, 10], xlabel: "feature 1", ylabel: "feature 2", label: "training points (blue) and draggable test points (red)" });
    var tbl = G.el("div", "tw"); tbl.style.margin = "10px 0 0"; body.appendChild(tbl);
    var drag = -1;
    function dist(p, q) { return Math.hypot(p[0] - q[0], p[1] - q[1]); }
    function draw() {
      pl.clear();
      var D = test.map(function (t) { return train.map(function (q) { return dist(t, q); }); });
      var nn = D.map(function (row) { var m = 0; row.forEach(function (v, j) { if (v < row[m]) m = j; }); return m; });
      test.forEach(function (t, i) { pl.line([t, train[nn[i]]], { stroke: "var(--bad)", "stroke-width": 2, "stroke-dasharray": "5 4" }); });
      train.forEach(function (q, j) {
        pl.dot(q[0], q[1], { r: 8, fill: "var(--tool)", stroke: "var(--surface)", "stroke-width": 2 });
        pl.text(q[0], q[1], String(j), { "text-anchor": "middle", dy: "4", fill: "#fff", "font-size": "10", "font-weight": "700", style: "pointer-events:none" });
      });
      test.forEach(function (t, i) {
        var c = pl.dot(t[0], t[1], { r: 11, fill: "var(--bad)", stroke: "var(--surface)", "stroke-width": 3, style: "cursor:grab" });
        c.addEventListener("pointerdown", function (e) { drag = i; e.preventDefault(); try { pl.svg.setPointerCapture(e.pointerId); } catch (er) {} });
        pl.text(t[0], t[1], String(i), { "text-anchor": "middle", dy: "4", fill: "#fff", "font-size": "11", "font-weight": "700", style: "pointer-events:none" });
      });
      var h = '<table class="t"><thead><tr><th>D[i, j]</th>' + train.map(function (_, j) { return "<th>j=" + j + "</th>"; }).join("") + "<th>argmin</th></tr></thead><tbody>";
      D.forEach(function (row, i) {
        h += '<tr><td style="font-family:var(--mono);color:var(--bad);font-weight:700">test ' + i + "</td>" + row.map(function (v, j) { return '<td class="n" style="' + (j === nn[i] ? "background:var(--hl1);font-weight:700" : "") + '">' + v.toFixed(2) + "</td>"; }).join("") + '<td class="n"><b>' + nn[i] + "</b></td></tr>";
      });
      tbl.innerHTML = h + "</tbody></table>";
    }
    function move(e) {
      if (drag < 0) return;
      var b = pl.svg.getBoundingClientRect(), px = (e.clientX - b.left) / b.width * pl.W, py = (e.clientY - b.top) / b.height * pl.H;
      var vx = (px - pl.P.l) / (pl.W - pl.P.l - pl.P.r) * 10, vy = (pl.H - pl.P.b - py) / (pl.H - pl.P.t - pl.P.b) * 10;
      test[drag] = [Math.max(0, Math.min(10, vx)), Math.max(0, Math.min(10, vy))]; draw();
    }
    pl.svg.style.touchAction = "none";
    pl.svg.addEventListener("pointermove", move);
    window.addEventListener("pointerup", function () { drag = -1; });
    draw();
  });
})();
