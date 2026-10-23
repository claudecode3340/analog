/* isl3-3 · potential problems and KNN widgets. Uses isl31Sums, isl31Grid (isl3-1.js) and isl32ols (isl3-2.js). */
function isl33fitInfo(X, y) {
  var b = isl32ols(X, y), n = y.length, p = X[0].length, fit = [], res = [], rss = 0, m = 0, tss = 0, i, j;
  for (i = 0; i < n; i++) { var f = 0; for (j = 0; j < p; j++) f += X[i][j] * b[j]; fit.push(f); res.push(y[i] - f); rss += (y[i] - f) * (y[i] - f); m += y[i] / n; }
  for (i = 0; i < n; i++) tss += (y[i] - m) * (y[i] - m);
  return { b: b, fit: fit, res: res, rss: rss, r2: 1 - rss / tss, rse: Math.sqrt(rss / (n - p)) };
}
/* a simple running-mean smoother of residuals against fitted values (like the book's red line) */
function isl33smooth(xs, ys, k) {
  var idx = xs.map(function (v, i) { return i; }).sort(function (a, b) { return xs[a] - xs[b]; }), out = [];
  for (var t = 0; t < idx.length; t += Math.max(1, Math.floor(idx.length / 40))) {
    var lo = Math.max(0, t - k), hi = Math.min(idx.length, t + k + 1), s = 0;
    for (var u = lo; u < hi; u++) s += ys[idx[u]];
    out.push([xs[idx[t]], s / (hi - lo)]);
  }
  return out;
}

/* ---------- isl3-3-resid: residual-plot diagnostics for six situations ---------- */
G.widget("isl3-3-resid", function (body) {
  var st = { sc: "curve", fix: false };
  var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
  var segEl = G.seg(ctr, [["ok", "healthy"], ["curve", "non-linear"], ["funnel", "funnel"], ["corr", "correlated errors"], ["outlier", "outlier"], ["lev", "high leverage"]], st.sc, function (v) { st.sc = v; st.fix = false; fx.textContent = fixLabel(); draw(); });
  segEl.style.flexWrap = "wrap"; segEl.style.maxWidth = "100%";
  var fx = G.button(ctr, "", function () { st.fix = !st.fix; fx.textContent = fixLabel(); draw(); });
  function fixLabel() { var L = { ok: "nothing to fix", curve: "add x² term", funnel: "use log(y)", corr: "(needs time-series methods)", outlier: "remove the outlier", lev: "remove the point" }[st.sc]; return (st.fix ? "undo: " : "fix: ") + L; }
  fx.textContent = fixLabel();
  var ro = G.el("div", "readout"); body.appendChild(ro);
  var grid = isl31Grid(body), a = G.el("div"), c = G.el("div"); grid.appendChild(a); grid.appendChild(c);
  var A = G.el("div"), C = G.el("div"); a.appendChild(A); c.appendChild(C);
  function data() {
    var rng = G.rng(11), n = 100, x = [], y = [], i, prev = 0;
    for (i = 0; i < n; i++) {
      var xi = st.sc === "corr" ? i / (n - 1) * 4 - 2 : -2 + 4 * rng(), e = G.randn(rng), yi;
      if (st.sc === "curve") yi = 1 + 1.2 * xi + 1.1 * xi * xi + 0.8 * e;
      else if (st.sc === "funnel") yi = Math.exp(1.6 + 0.45 * xi + 0.22 * e);
      else if (st.sc === "corr") { prev = 0.9 * prev + Math.sqrt(1 - 0.81) * e; yi = 2 + xi + 0.8 * prev; }
      else yi = 2 + 1.5 * xi + 0.7 * e;
      x.push(xi); y.push(yi);
    }
    if (st.sc === "outlier") { x.push(0.3); y.push(2 + 1.5 * 0.3 + 6); }
    if (st.sc === "lev") { x.push(6); y.push(2 + 1.5 * 6 - 6); }
    if (st.fix && (st.sc === "outlier" || st.sc === "lev")) { x.pop(); y.pop(); }
    return { x: x, y: y };
  }
  function draw() {
    var d = data(), x = d.x, y = d.y, n = x.length, logy = st.fix && st.sc === "funnel", sq = st.fix && st.sc === "curve";
    var yy = y.map(function (v) { return logy ? Math.log(v) : v; });
    var X = x.map(function (v) { return sq ? [1, v, v * v] : [1, v]; });
    var F = isl33fitInfo(X, yy);
    var xmin = Math.min.apply(null, x), xmax = Math.max.apply(null, x), ymin = Math.min.apply(null, yy), ymax = Math.max.apply(null, yy);
    A.innerHTML = ""; C.innerHTML = "";
    var padY = (ymax - ymin) * 0.08 + 0.1;
    var pl = G.plot(A, { w: 460, h: 320, x: [Math.floor(xmin), Math.ceil(xmax)], y: [ymin - padY, ymax + padY], xlabel: "x", ylabel: logy ? "log(y)" : "y", label: "data and fitted model" });
    for (var i = 0; i < n; i++) pl.dot(x[i], yy[i], { r: 2.8, fill: (st.sc === "outlier" || st.sc === "lev") && !st.fix && i === n - 1 ? "var(--bad)" : "var(--ink2)", opacity: 0.75 });
    var curve = []; for (var k = 0; k <= 60; k++) { var xv = xmin + (xmax - xmin) * k / 60; curve.push([xv, F.b[0] + F.b[1] * xv + (sq ? F.b[2] * xv * xv : 0)]); }
    pl.line(curve, { stroke: "var(--accent)", "stroke-width": 2.4 });
    var hx = st.sc === "corr", xs = hx ? x.map(function (v, i) { return i + 1; }) : F.fit;
    var rmax = Math.max.apply(null, F.res.map(Math.abs)) * 1.1;
    var lo = Math.min.apply(null, xs), hi = Math.max.apply(null, xs);
    var pr = G.plot(C, { w: 460, h: 320, x: [lo - (hi - lo) * 0.03, hi + (hi - lo) * 0.03], y: [-rmax, rmax], xlabel: hx ? "observation order (time)" : "fitted value ŷ", ylabel: "residual", label: "residual plot" });
    pr.line([[lo, 0], [hi, 0]], { stroke: "var(--muted)", "stroke-dasharray": "4 4", "stroke-width": 1.2 });
    if (hx) pr.line(xs.map(function (v, i) { return [v, F.res[i]]; }), { stroke: "var(--isl)", "stroke-width": 1.2 });
    for (i = 0; i < n; i++) pr.dot(xs[i], F.res[i], { r: 2.6, fill: (st.sc === "outlier" || st.sc === "lev") && !st.fix && i === n - 1 ? "var(--bad)" : "var(--ink2)", opacity: 0.75 });
    if (!hx) pr.line(isl33smooth(xs, F.res, 10), { stroke: "var(--bad)", "stroke-width": 2 });
    // leverage and studentized residual of the last point
    var Sx = isl31Sums(x, yy), hl = 1 / n + (x[n - 1] - Sx.xb) * (x[n - 1] - Sx.xb) / Sx.cxx;
    var verdict = { ok: "no pattern: assumptions look fine", curve: "U-shape: the straight line misses a curve", funnel: "spread grows with ŷ: heteroscedasticity", corr: "neighbours have similar residuals: tracking", outlier: "one residual far from the rest", lev: "one point far out in x, pulling the line" }[st.sc];
    if (st.fix) verdict = { ok: verdict, curve: "pattern gone after adding x²", funnel: "spread roughly constant after log(y)", corr: "a transformation cannot remove time correlation", outlier: "outlier removed: RSE drops", lev: "point removed: the line swings back" }[st.sc];
    ro.innerHTML = "<div>what the residual plot says<b>" + verdict + "</b></div><div>R²<b>" + G.fmt(F.r2, 3) + "</b></div><div>RSE<b>" + G.fmt(F.rse, 3) + "</b></div><div>slope b₁<b>" + G.fmt(F.b[1], 3) + "</b></div>" + ((st.sc === "lev" || st.sc === "outlier") && !st.fix ? "<div>leverage of red point (avg " + G.fmt(2 / n, 3) + ")<b>" + G.fmt(hl, 3) + "</b></div>" : "");
  }
  draw();
});

/* ---------- isl3-3-leverage: drag one point; see leverage, studentized residual and the fit move ---------- */
G.widget("isl3-3-leverage", function (body) {
  var rng = G.rng(5), x = [], y = [], i;
  for (i = 0; i < 30; i++) { var xi = G.randn(rng) * 0.9; x.push(xi); y.push(1 + 2 * xi + 0.6 * G.randn(rng)); }
  var P = { x: 4, y: 3 }, drag = false;
  var ro = G.el("div", "readout"); body.appendChild(ro);
  var pl = G.plot(body, { w: 680, h: 360, x: [-3, 5], y: [-6, 14], xlabel: "X", ylabel: "Y", label: "drag the red point" });
  function fit(xx, yy) { var S = isl31Sums(xx, yy); return S; }
  function draw() {
    pl.clear();
    var xa = x.concat([P.x]), ya = y.concat([P.y]), n = xa.length, Sa = fit(xa, ya), So = fit(x, y);
    var e = ya.map(function (v, i) { return v - Sa.b0 - Sa.b1 * xa[i]; }), rss = e.reduce(function (s, v) { return s + v * v; }, 0);
    var h = 1 / n + (P.x - Sa.xb) * (P.x - Sa.xb) / Sa.cxx, ei = e[n - 1];
    var s2 = (rss - ei * ei / (1 - h)) / (n - 3), stud = ei / Math.sqrt(s2 * (1 - h));
    pl.line([[-3, So.b0 - 3 * So.b1], [5, So.b0 + 5 * So.b1]], { stroke: "var(--tool)", "stroke-width": 2.2, "stroke-dasharray": "7 5" });
    pl.line([[-3, Sa.b0 - 3 * Sa.b1], [5, Sa.b0 + 5 * Sa.b1]], { stroke: "var(--bad)", "stroke-width": 2.4 });
    for (var i = 0; i < x.length; i++) pl.dot(x[i], y[i], { r: 3.2, fill: "none", stroke: "var(--ink2)", "stroke-width": 1.4 });
    var c = pl.dot(P.x, P.y, { r: 9, fill: "var(--bad)", stroke: "var(--surface)", "stroke-width": 3, style: "cursor:grab" });
    c.addEventListener("pointerdown", function (ev) { drag = true; c.setPointerCapture(ev.pointerId); });
    ro.innerHTML = "<div>leverage hᵢ of red point<b>" + G.fmt(h, 3) + "</b></div><div>average leverage (p+1)/n<b>" + G.fmt(2 / n, 3) + "</b></div><div>studentized residual<b>" + G.fmt(stud, 2) + "</b></div><div>slope with / without it<b>" + G.fmt(Sa.b1, 2) + " / " + G.fmt(So.b1, 2) + "</b></div>";
  }
  pl.svg.addEventListener("pointermove", function (ev) {
    if (!drag) return;
    var r = pl.svg.getBoundingClientRect(), px = (ev.clientX - r.left) / r.width * pl.W, py = (ev.clientY - r.top) / r.height * pl.H;
    P.x = Math.max(-3, Math.min(5, -3 + (px - pl.P.l) / (pl.W - pl.P.l - pl.P.r) * 8));
    P.y = Math.max(-6, Math.min(14, -6 + (pl.H - pl.P.b - py) / (pl.H - pl.P.t - pl.P.b) * 20)); draw();
  });
  pl.svg.addEventListener("pointerup", function () { drag = false; });
  var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
  G.button(ctr, "Outlier, low leverage", function () { P = { x: 0.2, y: 8 }; draw(); });
  G.button(ctr, "High leverage, on the line", function () { P = { x: 4.5, y: 10 }; draw(); });
  G.button(ctr, "High leverage AND outlier", function () { P = { x: 4, y: 3 }; draw(); });
  draw();
});

/* ---------- isl3-3-knn: KNN regression vs linear regression as non-linearity and dimension grow ---------- */
G.widget("isl3-3-knn", function (body) {
  var st = { a: 0, p: 1, K: 9 };
  var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
  G.slider(ctr, { label: "non-linearity of f", min: 0, max: 1, step: 0.1, value: st.a, fmt: function (v) { return (+v).toFixed(1); }, onChange: function (v) { st.a = v; draw(); } });
  G.slider(ctr, { label: "K (neighbours)", min: 1, max: 10, step: 1, value: st.K, onChange: function (v) { st.K = v; draw(); } });
  var ctr2 = G.el("div", "ctrls"); body.appendChild(ctr2);
  G.seg(ctr2, [[1, "p = 1"], [2, "p = 2"], [4, "p = 4"], [10, "p = 10"], [20, "p = 20"]], 1, function (v) { st.p = v; draw(); });
  var ro = G.el("div", "readout"); body.appendChild(ro);
  var grid = isl31Grid(body), A = G.el("div"), B = G.el("div"); grid.appendChild(A); grid.appendChild(B);
  function f(x) { return 2 + 1.2 * x + st.a * 1.3 * Math.sin(3.2 * x); }
  function sample(rng, n) { var X = [], y = []; for (var i = 0; i < n; i++) { var r = []; for (var j = 0; j < st.p; j++) r.push(-1 + 2 * rng()); X.push(r); y.push(f(r[0]) + 0.3 * G.randn(rng)); } return { X: X, y: y }; }
  function knn(tr, x0, K) {
    var d = tr.X.map(function (r, i) { var s = 0; for (var j = 0; j < r.length; j++) s += (r[j] - x0[j]) * (r[j] - x0[j]); return [s, i]; });
    d.sort(function (a, b) { return a[0] - b[0]; }); var m = 0; for (var k = 0; k < K; k++) m += tr.y[d[k][1]]; return m / K;
  }
  function draw() {
    var rng = G.rng(21), tr = sample(rng, 50), te = sample(rng, 300);
    var b = isl32ols(tr.X.map(function (r) { return [1].concat(r); }), tr.y);
    function lr(x0) { var s = b[0]; for (var j = 0; j < x0.length; j++) s += b[j + 1] * x0[j]; return s; }
    var lrMSE = 0; te.X.forEach(function (r, i) { var e = te.y[i] - lr(r); lrMSE += e * e / te.y.length; });
    var mse = []; for (var K = 1; K <= 10; K++) { var s = 0; te.X.forEach(function (r, i) { var e = te.y[i] - knn(tr, r, K); s += e * e / te.y.length; }); mse.push(s); }
    A.innerHTML = ""; B.innerHTML = "";
    var pl = G.plot(A, { w: 460, h: 320, x: [-1, 1], y: [-0.5, 5], xlabel: "x₁ (the only predictor that matters)", ylabel: "y", label: "training data, true f, KNN and linear fits" });
    var tc = []; for (var k = 0; k <= 80; k++) { var xv = -1 + 2 * k / 80; tc.push([xv, f(xv)]); }
    tr.X.forEach(function (r, i) { pl.dot(r[0], tr.y[i], { r: 3, fill: "var(--warn)" }); });
    pl.line(tc, { stroke: "var(--ink)", "stroke-width": 2.2 });
    if (st.p === 1) {
      var kc = []; for (k = 0; k <= 200; k++) { var xv2 = -1 + 2 * k / 200; kc.push([xv2, knn(tr, [xv2], st.K)]); }
      pl.line(kc, { stroke: "var(--tool)", "stroke-width": 2 });
      pl.line([[-1, b[0] - b[1]], [1, b[0] + b[1]]], { stroke: "var(--accent)", "stroke-width": 2, "stroke-dasharray": "7 5" });
    } else {
      te.X.slice(0, 120).forEach(function (r) { pl.dot(r[0], knn(tr, r, st.K), { r: 2.2, fill: "var(--tool)", opacity: 0.8 }); });
    }
    var ymax = Math.max(0.2, Math.max.apply(null, mse.concat([lrMSE])) * 1.1);
    var pm = G.plot(B, { w: 460, h: 320, x: [-1.05, 0.05], y: [0, ymax], xticks: [-1, Math.log10(0.2), Math.log10(0.5), 0], xlabel: "1/K (log scale): flexible →", ylabel: "test MSE", label: "test MSE of KNN against 1/K, with linear regression" });
    // relabel the log ticks
    Array.prototype.forEach.call(pm.svg.querySelectorAll("text.tick[text-anchor=middle]"), function (t) { var v = { "-1": "0.1", "-0.699": "0.2", "-0.301": "0.5", "0": "1" }[t.textContent]; if (v) t.textContent = v; });
    pm.line([[-1.05, lrMSE], [0.05, lrMSE]], { stroke: "var(--ink)", "stroke-width": 1.6, "stroke-dasharray": "6 5" });
    pm.line(mse.map(function (m, i) { return [Math.log10(1 / (i + 1)), m]; }), { stroke: "var(--good)", "stroke-width": 2.2 });
    mse.forEach(function (m, i) { pm.dot(Math.log10(1 / (i + 1)), m, { r: i + 1 === st.K ? 6 : 3, fill: "var(--good)" }); });
    var best = Math.min.apply(null, mse);
    ro.innerHTML = "<div>linear regression test MSE<b>" + G.fmt(lrMSE, 3) + "</b></div><div>KNN test MSE at K = " + st.K + "<b>" + G.fmt(mse[st.K - 1], 3) + "</b></div><div>best KNN (K = " + (mse.indexOf(best) + 1) + ")<b>" + G.fmt(best, 3) + "</b></div><div>winner<b>" + (best < lrMSE ? "KNN" : "linear regression") + "</b></div>";
  }
  draw();
});
