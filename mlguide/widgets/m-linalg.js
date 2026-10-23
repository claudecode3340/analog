/* m-linalg · dot product, click-a-cell matrix product, 2x2 transform, least squares */
(function () {
  function toData(pl, e, x0, x1, y0, y1) {
    var r = pl.svg.getBoundingClientRect();
    var px = (e.clientX - r.left) / r.width * pl.W, py = (e.clientY - r.top) / r.height * pl.H;
    return [x0 + (px - pl.P.l) / (pl.W - pl.P.l - pl.P.r) * (x1 - x0), y0 + (pl.H - pl.P.b - py) / (pl.H - pl.P.t - pl.P.b) * (y1 - y0)];
  }
  function arrow(pl, x0, y0, x1, y1, col, w, dash) {
    var X0 = pl.X(x0), Y0 = pl.Y(y0), X1 = pl.X(x1), Y1 = pl.Y(y1), L = Math.hypot(X1 - X0, Y1 - Y0);
    if (L < 1) return;
    var ux = (X1 - X0) / L, uy = (Y1 - Y0) / L, h = Math.min(13, L * 0.45);
    G.svg("line", { x1: X0, y1: Y0, x2: X1 - ux * h * 0.8, y2: Y1 - uy * h * 0.8, stroke: col, "stroke-width": w || 3, "stroke-dasharray": dash || "", "stroke-linecap": "round" }, pl.layer);
    var p = [[X1, Y1], [X1 - ux * h - uy * h * 0.5, Y1 - uy * h + ux * h * 0.5], [X1 - ux * h + uy * h * 0.5, Y1 - uy * h - ux * h * 0.5]];
    G.svg("polygon", { points: p.map(function (q) { return q[0].toFixed(1) + "," + q[1].toFixed(1); }).join(" "), fill: col }, pl.layer);
  }
  function wrapSvg(body) { var d = G.el("div", ""); d.style.cssText = "max-width:520px;margin:6px auto 0"; body.appendChild(d); return d; }
  var clipN = 0;
  function clip(pl) {
    var id = "mlclip" + (++clipN), defs = G.svg("defs", {}, pl.svg), cp = G.svg("clipPath", { id: id }, defs);
    G.svg("rect", { x: pl.P.l, y: pl.P.t, width: pl.W - pl.P.l - pl.P.r, height: pl.H - pl.P.t - pl.P.b }, cp);
    pl.layer.setAttribute("clip-path", "url(#" + id + ")");
  }

  /* ---------- 1. dot product, angle, projection ---------- */
  G.widget("m-linalg-dot", function (body) {
    var a = [3, 1], b = [1, 2], drag = null, R = 4;
    var info = G.el("div", "readout"); body.appendChild(info);
    var eq = G.el("div", ""); eq.style.cssText = "margin:10px 0 2px;overflow-x:auto;text-align:center;font-size:16px"; body.appendChild(eq);
    var host = wrapSvg(body);
    var pl = G.plot(host, { w: 500, h: 500, x: [-R, R], y: [-R, R], pad: { l: 34, r: 12, t: 12, b: 30 }, label: "two draggable vectors with their projection" });
    function draw() {
      pl.clear();
      pl.line([[-R, 0], [R, 0]], { stroke: "var(--line2)", "stroke-width": 1.4 }); pl.line([[0, -R], [0, R]], { stroke: "var(--line2)", "stroke-width": 1.4 });
      var d = a[0] * b[0] + a[1] * b[1], na = Math.hypot(a[0], a[1]), nb = Math.hypot(b[0], b[1]);
      arrow(pl, 0, 0, a[0], a[1], "var(--math)", 3.4); arrow(pl, 0, 0, b[0], b[1], "var(--tool)", 3.4);
      if (na > 0) {
        var c = d / (na * na), p = [c * a[0], c * a[1]];
        pl.line([[b[0], b[1]], p], { stroke: "var(--muted)", "stroke-width": 1.5, "stroke-dasharray": "3 4" });
        arrow(pl, 0, 0, p[0], p[1], "var(--udl)", 5, "8 5");
      }
      [[a, "a", "var(--math)"], [b, "b", "var(--tool)"]].forEach(function (v) {
        var h = pl.dot(v[0][0], v[0][1], { r: 11, fill: v[2], opacity: 0.25, style: "cursor:grab" });
        h.addEventListener("pointerdown", function (e) { drag = v[0]; pl.svg.setPointerCapture(e.pointerId); e.preventDefault(); });
        pl.text(v[0][0] + 0.18, v[0][1] + 0.22, v[1] + " = (" + v[0][0] + ", " + v[0][1] + ")", { fill: v[2], "font-weight": 700, "font-size": 14 });
      });
      var cos = na && nb ? d / (na * nb) : NaN, ang = Math.acos(Math.max(-1, Math.min(1, cos))) * 180 / Math.PI;
      var kind = Math.abs(d) < 1e-9 ? "orthogonal (90°)" : d > 0 ? "less than 90°: same general direction" : "more than 90°: opposite-ish";
      info.innerHTML = "<div>a·b<b>" + G.fmt(d, 2) + "</b></div><div>‖a‖<b>" + G.fmt(na, 3) + "</b></div><div>‖b‖<b>" + G.fmt(nb, 3) + "</b></div><div>cos θ<b>" + G.fmt(cos, 4) + "</b></div><div>θ<b>" + G.fmt(ang, 1) + "°</b></div><div>angle is<b style='font-size:14px'>" + kind + "</b></div>";
      eq.innerHTML = G.tex("\\mathbf a^{\\mathsf T}\\mathbf b=(" + a[0] + ")(" + b[0] + ")+(" + a[1] + ")(" + b[1] + ")=" + G.fmt(a[0] * b[0], 2) + (a[1] * b[1] < 0 ? "" : "+") + G.fmt(a[1] * b[1], 2) + "=\\mathbf{" + G.fmt(d, 2) + "}", true) +
        "<div style='font-size:13px;color:var(--muted)'>dashed violet arrow: projection of b onto a, \\(\\frac{\\mathbf a^{\\mathsf T}\\mathbf b}{\\mathbf a^{\\mathsf T}\\mathbf a}\\mathbf a\\) = " + G.fmt(na ? d / (na * na) : 0, 3) + " × a</div>";
      G.renderMath && G.renderMath(eq);
    }
    pl.svg.addEventListener("pointermove", function (e) {
      if (!drag) return; var q = toData(pl, e, -R, R, -R, R);
      drag[0] = Math.max(-3.5, Math.min(3.5, Math.round(q[0] * 2) / 2)); drag[1] = Math.max(-3.5, Math.min(3.5, Math.round(q[1] * 2) / 2));
      if (drag[0] === 0 && drag[1] === 0) drag[0] = 0.5; draw();
    });
    pl.svg.addEventListener("pointerup", function () { drag = null; });
    draw();
  });

  /* ---------- 2. click a cell of the product ---------- */
  G.widget("m-linalg-matmul", function (body) {
    var EX = {
      sq: { A: [[1, 2], [3, 4]], B: [[5, 6], [7, 8]] },
      rect: { A: [[1, 0, 2], [-1, 3, 1]], B: [[3, 1], [2, 1], [1, 0]] }
    };
    var cur = "sq", si = 0, sj = 0;
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    G.seg(ctr, [["sq", "2×2 times 2×2 (ISLP)"], ["rect", "2×3 times 3×2"]], cur, function (v) { cur = v; si = 0; sj = 0; draw(); });
    var row = G.el("div", "mrow"); row.style.justifyContent = "center"; body.appendChild(row);
    var eq = G.el("div", ""); eq.style.cssText = "text-align:center;overflow-x:auto;font-size:16px"; body.appendChild(eq);
    function grid(M, cls, lab, click) {
      var w = G.el("span", ""), g = G.el("span", "mgrid"); g.style.gridTemplateColumns = "repeat(" + M[0].length + ",auto)";
      M.forEach(function (r, i) { r.forEach(function (v, j) {
        var c = G.el("span", cls(i, j), String(v));
        if (click) { c.style.cursor = "pointer"; c.title = "row " + (i + 1) + ", column " + (j + 1); c.onclick = function () { si = i; sj = j; draw(); }; }
        g.appendChild(c); }); });
      w.appendChild(g); w.appendChild(G.el("span", "lab", lab)); return w;
    }
    function draw() {
      var A = EX[cur].A, B = EX[cur].B, m = A.length, n = B.length, p = B[0].length;
      var C = A.map(function (r) { return B[0].map(function (_, j) { return r.reduce(function (s, v, k) { return s + v * B[k][j]; }, 0); }); });
      row.innerHTML = "";
      row.appendChild(grid(A, function (i) { return i === si ? "h1" : ""; }, "A (" + m + "×" + n + ")"));
      row.appendChild(G.el("span", "op", "×"));
      row.appendChild(grid(B, function (i, j) { return j === sj ? "h2" : ""; }, "B (" + n + "×" + p + ")"));
      row.appendChild(G.el("span", "op", "="));
      row.appendChild(grid(C, function (i, j) { return i === si && j === sj ? "h4" : ""; }, "AB (" + m + "×" + p + ") · click a cell", true));
      var terms = A[si].map(function (v, k) { return "(" + v + ")(" + B[k][sj] + ")"; }).join("+");
      var prods = A[si].map(function (v, k) { return v * B[k][sj]; });
      eq.innerHTML = G.tex("\\begin{aligned}(\\mathbf{AB})_{" + (si + 1) + (sj + 1) + "}&=\\textstyle\\sum_{k=1}^{" + n + "}a_{" + (si + 1) + "k}\\,b_{k" + (sj + 1) + "}\\\\&=" + terms + "\\\\&=" + prods.join("+").replace(/\+-/g, "-") + "=\\mathbf{" + C[si][sj] + "}\\end{aligned}", true);
    }
    draw();
  });

  /* ---------- 3. a 2x2 matrix moving the plane ---------- */
  G.widget("m-linalg-transform", function (body, args) {
    var M = (args.m || [2, 1, 1, 2]).slice(), R = 4.5;
    var presets = [["sym", "[[2,1],[1,2]]", [2, 1, 1, 2]], ["id", "identity", [1, 0, 0, 1]], ["rot", "rotate 30°", [0.87, -0.5, 0.5, 0.87]], ["shear", "shear", [1, 1, 0, 1]], ["refl", "mirror", [1, 0, 0, -1]], ["sing", "singular", [1, 2, 0.5, 1]], ["prince", "Prince Fig. 23.3", [2, -1, 3.1, 1.5]]];
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    var sl = [];
    G.seg(ctr, presets.map(function (p) { return [p[0], p[1]]; }), "sym", function (v) { presets.forEach(function (p) { if (p[0] === v) M = p[2].slice(); }); sl.forEach(function (s, k) { s.set(M[k]); }); draw(); });
    var ctr2 = G.el("div", "ctrls"); body.appendChild(ctr2);
    ["a (top-left)", "b (top-right)", "c (bottom-left)", "d (bottom-right)"].forEach(function (lab, k) {
      sl.push(G.slider(ctr2, { label: lab, min: -3, max: 3, step: 0.1, value: M[k], fmt: function (v) { return G.fmt(v, 2); }, onChange: function (v) { M[k] = v; draw(); } }));
    });
    var info = G.el("div", "readout"); body.appendChild(info);
    var host = wrapSvg(body);
    var pl = G.plot(host, { w: 500, h: 500, x: [-R, R], y: [-R, R], pad: { l: 34, r: 12, t: 12, b: 30 }, label: "grid transformed by a 2 by 2 matrix" });
    clip(pl);
    function T(x, y) { return [M[0] * x + M[1] * y, M[2] * x + M[3] * y]; }
    function draw() {
      pl.clear();
      for (var k = -6; k <= 6; k++) {
        var l1 = [], l2 = [];
        for (var t = -6; t <= 6; t += 0.5) { l1.push(T(k, t)); l2.push(T(t, k)); }
        pl.line(l1, { stroke: "var(--accent)", "stroke-width": k === 0 ? 1.6 : 0.8, opacity: 0.35 });
        pl.line(l2, { stroke: "var(--accent)", "stroke-width": k === 0 ? 1.6 : 0.8, opacity: 0.35 });
      }
      var circ = [], circ0 = [];
      for (var s = 0; s <= 64; s++) { var th = s / 64 * 2 * Math.PI; circ.push(T(Math.cos(th), Math.sin(th))); circ0.push([Math.cos(th), Math.sin(th)]); }
      pl.line(circ0, { stroke: "var(--muted)", "stroke-width": 1.2, "stroke-dasharray": "3 4" });
      pl.line(circ, { stroke: "var(--ink2)", "stroke-width": 1.6, "stroke-dasharray": "6 4" });
      var sq = [T(0, 0), T(1, 0), T(1, 1), T(0, 1)];
      G.svg("polygon", { points: [[0, 0], [1, 0], [1, 1], [0, 1]].map(function (q) { return pl.X(q[0]) + "," + pl.Y(q[1]); }).join(" "), fill: "none", stroke: "var(--muted)", "stroke-dasharray": "4 3" }, pl.layer);
      G.svg("polygon", { points: sq.map(function (q) { return pl.X(q[0]) + "," + pl.Y(q[1]); }).join(" "), fill: "var(--good)", opacity: 0.22, stroke: "var(--good)" }, pl.layer);
      var tr = M[0] + M[3], det = M[0] * M[3] - M[1] * M[2], disc = tr * tr / 4 - det, ev = "";
      if (disc >= -1e-12) {
        var r = Math.sqrt(Math.max(0, disc)), ls = [tr / 2 + r, tr / 2 - r];
        ls.forEach(function (lam, k) {
          var v = Math.abs(M[1]) > 1e-9 ? [M[1], lam - M[0]] : Math.abs(M[2]) > 1e-9 ? [lam - M[3], M[2]] : (k === 0 ? (M[0] >= M[3] ? [1, 0] : [0, 1]) : (M[0] >= M[3] ? [0, 1] : [1, 0]));
          var nv = Math.hypot(v[0], v[1]) || 1; v = [v[0] / nv, v[1] / nv];
          pl.line([[-6 * v[0], -6 * v[1]], [6 * v[0], 6 * v[1]]], { stroke: "var(--udl)", "stroke-width": 1.6, "stroke-dasharray": "8 6" });
        });
        ev = G.fmt(ls[0], 3) + " and " + G.fmt(ls[1], 3);
      } else ev = "complex: " + G.fmt(tr / 2, 3) + " ± " + G.fmt(Math.sqrt(-disc), 3) + "i (no real eigenvector)";
      arrow(pl, 0, 0, M[0], M[2], "var(--math)", 3.4); arrow(pl, 0, 0, M[1], M[3], "var(--tool)", 3.4);
      pl.text(M[0] + 0.15, M[2] - 0.3, "column 1 = A(1,0)", { fill: "var(--math)", "font-weight": 700, "font-size": 13 });
      pl.text(M[1] + 0.15, M[3] + 0.2, "column 2 = A(0,1)", { fill: "var(--tool)", "font-weight": 700, "font-size": 13 });
      info.innerHTML = "<div>A<b style='font-size:14px'>" + G.tex("\\begin{pmatrix}" + G.fmt(M[0], 2) + "&" + G.fmt(M[1], 2) + "\\\\" + G.fmt(M[2], 2) + "&" + G.fmt(M[3], 2) + "\\end{pmatrix}") + "</b></div><div>det A = ad − bc (area factor)<b>" + G.fmt(det, 3) + "</b></div><div>eigenvalues (dashed violet lines = eigenvectors)<b>" + ev + "</b></div>";
    }
    draw();
  });

  /* ---------- 4. least squares: residuals and the normal equations ---------- */
  G.widget("m-linalg-lsq", function (body) {
    var P = [[1, 2], [2, 3], [3, 5]], b0 = 1, b1 = 1, drag = -1;
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    var s0 = G.slider(ctr, { label: "intercept β₀", min: -2, max: 4, step: 0.01, value: b0, fmt: function (v) { return G.fmt(v, 2); }, onChange: function (v) { b0 = v; draw(); } });
    var s1 = G.slider(ctr, { label: "slope β₁", min: -1, max: 3, step: 0.01, value: b1, fmt: function (v) { return G.fmt(v, 2); }, onChange: function (v) { b1 = v; draw(); } });
    G.button(ctr, "Solve the normal equations", function () {
      var n = P.length, sx = 0, sy = 0, sxx = 0, sxy = 0;
      P.forEach(function (p) { sx += p[0]; sy += p[1]; sxx += p[0] * p[0]; sxy += p[0] * p[1]; });
      var det = n * sxx - sx * sx; b0 = (sxx * sy - sx * sxy) / det; b1 = (n * sxy - sx * sy) / det;
      s0.set(Math.round(b0 * 100) / 100); s1.set(Math.round(b1 * 100) / 100); draw();
    });
    var info = G.el("div", "readout"); body.appendChild(info);
    var pl = G.plot(body, { w: 680, h: 330, x: [0, 4], y: [0, 7], xlabel: "x", ylabel: "y", label: "three points, a line and its residuals" });
    function draw() {
      pl.clear();
      pl.line([[0, b0], [4, b0 + 4 * b1]], { stroke: "var(--accent)", "stroke-width": 2.6 });
      var rss = 0, se = 0, sxe = 0, es = [];
      P.forEach(function (p, i) {
        var yh = b0 + b1 * p[0], e = p[1] - yh; es.push(G.fmt(e, 3)); rss += e * e; se += e; sxe += p[0] * e;
        pl.line([[p[0], p[1]], [p[0], yh]], { stroke: "var(--bad)", "stroke-width": 3 });
        var c = pl.dot(p[0], p[1], { r: 8, fill: "var(--tool)", stroke: "var(--surface)", "stroke-width": 2.5, style: "cursor:ns-resize" });
        c.addEventListener("pointerdown", function (ev) { drag = i; pl.svg.setPointerCapture(ev.pointerId); ev.preventDefault(); });
      });
      info.innerHTML = "<div>residuals e = y − ŷ<b>(" + es.join(", ") + ")</b></div><div>RSS = ‖e‖²<b>" + G.fmt(rss, 4) + "</b></div><div>1ᵀe = Σ eᵢ<b>" + G.fmt(se, 4) + "</b></div><div>xᵀe = Σ xᵢeᵢ<b>" + G.fmt(sxe, 4) + "</b></div><div>points<b style='font-size:13px'>" + P.map(function (p) { return "(" + p[0] + ", " + G.fmt(p[1], 1) + ")"; }).join(" ") + "</b></div>";
    }
    pl.svg.addEventListener("pointermove", function (e) {
      if (drag < 0) return; var q = toData(pl, e, 0, 4, 0, 7);
      P[drag][1] = Math.max(0.2, Math.min(6.8, Math.round(q[1] * 10) / 10)); draw();
    });
    pl.svg.addEventListener("pointerup", function () { drag = -1; });
    draw();
  });
})();
