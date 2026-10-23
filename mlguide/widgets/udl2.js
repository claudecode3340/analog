/* udl2 · Prince Chapter 2 widgets */
(function () {
  var X = [0.03, 0.19, 0.34, 0.46, 0.78, 0.81, 1.08, 1.18, 1.39, 1.60, 1.65, 1.90];
  var Yd = [0.67, 0.85, 1.05, 1.00, 1.40, 1.50, 1.30, 1.54, 1.55, 1.68, 1.73, 1.60];
  var BEST = [0.82595, 0.52223];
  function loss(a, b) { var s = 0; for (var i = 0; i < X.length; i++) { var r = a + b * X[i] - Yd[i]; s += r * r; } return s; }
  function grad(a, b) { var g0 = 0, g1 = 0; for (var i = 0; i < X.length; i++) { var r = a + b * X[i] - Yd[i]; g0 += 2 * r; g1 += 2 * X[i] * r; } return [g0, g1]; }
  var uid = 0;
  function clip(pl) {
    var id = "udl2clip" + (uid++);
    var cp = G.svg("clipPath", { id: id }, pl.svg);
    G.svg("rect", { x: pl.P.l, y: pl.P.t, width: pl.W - pl.P.l - pl.P.r, height: pl.H - pl.P.t - pl.P.b }, cp);
    pl.layer.setAttribute("clip-path", "url(#" + id + ")");
    return "url(#" + id + ")";
  }

  G.widget("udl2-fit", function (body) {
    var st = { a: 0.4, b: 0.2, path: [] };
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    var f2 = function (v) { return v.toFixed(2); };
    var sa = G.slider(ctr, { label: "φ₀ intercept", min: 0, max: 2, step: 0.01, value: st.a, fmt: f2, onChange: function (v) { st.a = v; st.path = []; draw(); } });
    var sb = G.slider(ctr, { label: "φ₁ slope", min: -1, max: 1, step: 0.01, value: st.b, fmt: f2, onChange: function (v) { st.b = v; st.path = []; draw(); } });
    var ctr2 = G.el("div", "ctrls"); body.appendChild(ctr2);
    G.seg(ctr2, [["b", "line (b)"], ["c", "line (c)"], ["d", "line (d)"]], "b", function (k) {
      var p = { b: [0.4, 0.2], c: [1.6, -0.8], d: [0.82, 0.52] }[k]; set(p[0], p[1]); st.path = []; draw();
    });
    G.button(ctr2, "Step downhill", function () {
      if (!st.path.length) st.path.push([st.a, st.b]);
      var g = grad(st.a, st.b); set(st.a - 0.02 * g[0], st.b - 0.02 * g[1]); st.path.push([st.a, st.b]); draw();
    });
    G.button(ctr2, "Jump to best", function () { set(BEST[0], BEST[1]); st.path = []; draw(); });
    var info = G.el("div", "readout"); body.appendChild(info);
    var grid = G.el("div"); grid.style.cssText = "display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px;margin-top:12px"; body.appendChild(grid);
    var h1 = G.el("div"), h2 = G.el("div"); grid.appendChild(h1); grid.appendChild(h2);
    var pd = G.plot(h1, { w: 400, h: 360, x: [0, 2], y: [0, 2], xlabel: "input x", ylabel: "output y", label: "data, line and residuals" });
    var pl = G.plot(h2, { w: 400, h: 360, x: [0, 2], y: [-1, 1], xlabel: "intercept φ₀", ylabel: "slope φ₁", label: "loss surface heat map" });
    clip(pd); var cpl = clip(pl);
    // static heat map, drawn once beneath the moving layer
    var heat = G.svg("g", { "clip-path": cpl, "shape-rendering": "crispEdges" }, pl.svg); pl.svg.insertBefore(heat, pl.layer);
    var N = 40, lmin = Math.log(0.2), lmax = Math.log(Math.max(loss(0, -1), loss(2, 1)));
    var cw = (pl.W - pl.P.l - pl.P.r) / N, ch = (pl.H - pl.P.t - pl.P.b) / N;
    for (var i = 0; i < N; i++) for (var j = 0; j < N; j++) {
      var a = (i + 0.5) / N * 2, b = -1 + (j + 0.5) / N * 2;
      var t = (Math.log(loss(a, b)) - lmin) / (lmax - lmin);
      G.svg("rect", { x: pl.X(i / N * 2), y: pl.Y(-1 + (j + 1) / N * 2), width: cw, height: ch, fill: "var(--udl)", "fill-opacity": (0.05 + 0.8 * Math.max(0, Math.min(1, t))).toFixed(3) }, heat);
    }
    // contours: the loss is quadratic, so its contours are ellipses around the minimum
    var I = X.length, Sx = 0, Sxx = 0; X.forEach(function (v) { Sx += v; Sxx += v * v; });
    var l11 = Math.sqrt(I), l21 = Sx / l11, l22 = Math.sqrt(Sxx - l21 * l21), Lmin = loss(BEST[0], BEST[1]);
    [0.4, 1, 2, 4, 8, 16].forEach(function (c) {
      var k = Math.sqrt(c - Lmin), pts = [];
      for (var q = 0; q <= 120; q++) {
        var th = q / 120 * 2 * Math.PI, u0 = Math.cos(th), u1 = Math.sin(th);
        pts.push([BEST[0] + k * (u0 / l11 - l21 * u1 / (l11 * l22)), BEST[1] + k * u1 / l22]);
      }
      var d = pts.map(function (p, n) { return (n ? "L" : "M") + pl.X(p[0]).toFixed(1) + " " + pl.Y(p[1]).toFixed(1); }).join("");
      G.svg("path", { d: d, "shape-rendering": "geometricPrecision", fill: "none", stroke: "var(--surface)", "stroke-width": 1.2, "stroke-opacity": 0.85 }, heat);
    });

    function set(a, b) { st.a = Math.max(0, Math.min(2, a)); st.b = Math.max(-1, Math.min(1, b)); sa.set(+st.a.toFixed(2)); sb.set(+st.b.toFixed(2)); }
    function draw() {
      pd.clear(); pl.clear();
      for (var i = 0; i < X.length; i++) {
        pd.line([[X[i], Yd[i]], [X[i], st.a + st.b * X[i]]], { stroke: "var(--bad)", "stroke-width": 2, "stroke-dasharray": "4 3" });
      }
      pd.line([[0, st.a], [2, st.a + 2 * st.b]], { stroke: "var(--udl)", "stroke-width": 3 });
      for (i = 0; i < X.length; i++) pd.dot(X[i], Yd[i], { r: 6, fill: "var(--math)", stroke: "var(--surface)", "stroke-width": 1.5 });
      if (st.path.length > 1) pl.line(st.path, { stroke: "var(--ink)", "stroke-width": 1.8 });
      st.path.forEach(function (p) { pl.dot(p[0], p[1], { r: 3, fill: "var(--ink)" }); });
      pl.dot(BEST[0], BEST[1], { r: 6, fill: "none", stroke: "var(--good)", "stroke-width": 2.5 });
      pl.dot(st.a, st.b, { r: 8, fill: "var(--accent)", stroke: "var(--surface)", "stroke-width": 2.5 });
      var g = grad(st.a, st.b), L = loss(st.a, st.b);
      info.innerHTML = "<div>φ = (φ₀, φ₁)<b>(" + st.a.toFixed(2) + ", " + st.b.toFixed(2) + ")</b></div><div>loss L[φ]<b>" + L.toFixed(3) + "</b></div><div>∂L/∂φ₀<b>" + g[0].toFixed(2) + "</b></div><div>∂L/∂φ₁<b>" + g[1].toFixed(2) + "</b></div><div>steps taken<b>" + Math.max(0, st.path.length - 1) + "</b></div>";
    }
    var dragging = false;
    function pick(e) {
      var r = pl.svg.getBoundingClientRect(), px = (e.clientX - r.left) / r.width * pl.W, py = (e.clientY - r.top) / r.height * pl.H;
      set((px - pl.P.l) / (pl.W - pl.P.l - pl.P.r) * 2, -1 + (pl.H - pl.P.b - py) / (pl.H - pl.P.t - pl.P.b) * 2); st.path = []; draw();
    }
    pl.svg.style.touchAction = "none"; pl.svg.style.cursor = "crosshair";
    pl.svg.addEventListener("pointerdown", function (e) { dragging = true; pl.svg.setPointerCapture(e.pointerId); pick(e); });
    pl.svg.addEventListener("pointermove", function (e) { if (dragging) pick(e); });
    pl.svg.addEventListener("pointerup", function () { dragging = false; });
    draw();
  });

  /* Under- and overfitting: fit polynomials of growing degree to 8 of the 12 points, test on 4 */
  G.widget("udl2-capacity", function (body) {
    var test = [2, 5, 8, 10], tr = [], te = [];
    for (var i = 0; i < 12; i++) (test.indexOf(i) >= 0 ? te : tr).push(i);
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    var deg = 1;
    G.slider(ctr, { label: "polynomial degree", min: 0, max: 7, step: 1, value: 1, onChange: function (v) { deg = v; draw(); } });
    var info = G.el("div", "readout"); body.appendChild(info);
    var pl = G.plot(body, { w: 680, h: 330, x: [0, 2], y: [0, 2.5], xlabel: "input x", ylabel: "output y", label: "polynomial fits" });
    clip(pl);
    // least squares polynomial fit on centred x via normal equations (small, well-conditioned enough)
    function fit(d) {
      var n = d + 1, A = [], bv = [];
      for (var r = 0; r < n; r++) { A.push(new Array(n).fill(0)); bv.push(0); }
      tr.forEach(function (k) { var u = X[k] - 1, p = []; for (var q = 0; q < n; q++) p.push(Math.pow(u, q)); for (var r = 0; r < n; r++) { bv[r] += p[r] * Yd[k]; for (var c = 0; c < n; c++) A[r][c] += p[r] * p[c]; } });
      for (var c = 0; c < n; c++) { var piv = c; for (r = c + 1; r < n; r++) if (Math.abs(A[r][c]) > Math.abs(A[piv][c])) piv = r;
        var tmp = A[c]; A[c] = A[piv]; A[piv] = tmp; var tb = bv[c]; bv[c] = bv[piv]; bv[piv] = tb;
        for (r = 0; r < n; r++) if (r !== c) { var m = A[r][c] / A[c][c]; for (var cc = c; cc < n; cc++) A[r][cc] -= m * A[c][cc]; bv[r] -= m * bv[c]; } }
      return bv.map(function (v, k) { return v / A[k][k]; });
    }
    function ev(w, xx) { var u = xx - 1, s = 0; for (var q = w.length - 1; q >= 0; q--) s = s * u + w[q]; return s; }
    function draw() {
      pl.clear(); var w = fit(deg), pts = [];
      for (var k = 0; k <= 300; k++) { var xx = k / 150; pts.push([xx, Math.max(-5, Math.min(8, ev(w, xx)))]); }
      pl.line(pts, { stroke: "var(--udl)", "stroke-width": 3 });
      var Ltr = 0, Lte = 0;
      tr.forEach(function (k) { var r = ev(w, X[k]) - Yd[k]; Ltr += r * r; pl.dot(X[k], Yd[k], { r: 6, fill: "var(--math)", stroke: "var(--surface)", "stroke-width": 1.5 }); });
      te.forEach(function (k) { var r = ev(w, X[k]) - Yd[k]; Lte += r * r; pl.line([[X[k], Yd[k]], [X[k], Math.max(-5, Math.min(8, ev(w, X[k])))]], { stroke: "var(--bad)", "stroke-width": 2, "stroke-dasharray": "4 3" });
        G.svg("rect", { x: pl.X(X[k]) - 6, y: pl.Y(Yd[k]) - 6, width: 12, height: 12, fill: "var(--isl)", stroke: "var(--surface)", "stroke-width": 1.5 }, pl.layer); });
      info.innerHTML = "<div>parameters<b>" + (deg + 1) + "</b></div><div>training loss (8 circles)<b>" + Ltr.toFixed(4) + "</b></div><div>test loss (4 squares)<b>" + Lte.toFixed(4) + "</b></div><div>verdict<b>" + (deg === 0 ? "underfits" : deg >= 5 ? "overfits" : "about right") + "</b></div>";
    }
    draw();
  });
})();
