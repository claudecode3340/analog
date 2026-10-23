/* isl3-2 · multiple linear regression widgets. Uses ADV_* arrays and isl31Sums/isl31Grid from isl3-1.js (loaded first). */
/* least squares by the normal equations, Gaussian elimination with partial pivoting. X: array of rows (each row includes the leading 1). */
function isl32ols(X, y) {
  var p = X[0].length, A = [], i, j, k;
  for (i = 0; i < p; i++) { A.push(new Array(p + 1).fill(0)); }
  for (var r = 0; r < X.length; r++) for (i = 0; i < p; i++) { for (j = 0; j < p; j++) A[i][j] += X[r][i] * X[r][j]; A[i][p] += X[r][i] * y[r]; }
  for (i = 0; i < p; i++) {
    var m = i; for (k = i + 1; k < p; k++) if (Math.abs(A[k][i]) > Math.abs(A[m][i])) m = k;
    var t = A[i]; A[i] = A[m]; A[m] = t;
    for (k = i + 1; k < p; k++) { var f = A[k][i] / A[i][i]; for (j = i; j <= p; j++) A[k][j] -= f * A[i][j]; }
  }
  var b = new Array(p).fill(0);
  for (i = p - 1; i >= 0; i--) { var s = A[i][p]; for (j = i + 1; j < p; j++) s -= A[i][j] * b[j]; b[i] = s / A[i][i]; }
  return b;
}

/* ---------- isl3-2-plane: the least-squares plane for sales on TV and radio (Figures 3.4 and 3.5) ---------- */
G.widget("isl3-2-plane", function (body) {
  var n = ADV_TV.length, st = { az: 35, el: 20, model: "add" };
  var Xa = [], Xi = [];
  for (var i = 0; i < n; i++) { Xa.push([1, ADV_TV[i], ADV_RADIO[i]]); Xi.push([1, ADV_TV[i], ADV_RADIO[i], ADV_TV[i] * ADV_RADIO[i]]); }
  var ba = isl32ols(Xa, ADV_SALES), bi = isl32ols(Xi, ADV_SALES);
  function f(tv, ra) { return st.model === "add" ? ba[0] + ba[1] * tv + ba[2] * ra : bi[0] + bi[1] * tv + bi[2] * ra + bi[3] * tv * ra; }
  var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
  G.slider(ctr, { label: "turn (azimuth)", min: 0, max: 360, step: 1, value: st.az, fmt: function (v) { return v + "°"; }, onChange: function (v) { st.az = v; draw(); } });
  G.slider(ctr, { label: "tilt (elevation)", min: 0, max: 70, step: 1, value: st.el, fmt: function (v) { return v + "°"; }, onChange: function (v) { st.el = v; draw(); } });
  G.seg(ctr, [["add", "plane: TV + radio"], ["int", "surface: + TV×radio"]], "add", function (v) { st.model = v; draw(); });
  var ro = G.el("div", "readout"); body.appendChild(ro);
  var W = 640, H = 440, svg = G.svg("svg", { viewBox: "0 0 " + W + " " + H, class: "wsvg", role: "img", "aria-label": "3-D view of sales against TV and radio with the fitted surface" }, body);
  var layer = G.svg("g", {}, svg);
  function proj(tv, ra, s) {
    var u = tv / 300 - 0.5, v = ra / 50 - 0.5, w = s / 28 - 0.5, a = st.az * Math.PI / 180, e = st.el * Math.PI / 180;
    var xs = u * Math.cos(a) - v * Math.sin(a), d = u * Math.sin(a) + v * Math.cos(a);
    return [W / 2 + 330 * xs, H / 2 + 10 - 280 * (w * Math.cos(e) + d * Math.sin(e)), d];
  }
  function seg(p, q, attrs) { return G.svg("line", Object.assign({ x1: p[0], y1: p[1], x2: q[0], y2: q[1] }, attrs), layer); }
  function draw() {
    while (layer.firstChild) layer.removeChild(layer.firstChild);
    // floor box and axes
    var c = [[0, 0], [300, 0], [300, 50], [0, 50]];
    for (var k = 0; k < 4; k++) seg(proj(c[k][0], c[k][1], 0), proj(c[(k + 1) % 4][0], c[(k + 1) % 4][1], 0), { stroke: "var(--line2)", "stroke-width": 1 });
    seg(proj(0, 0, 0), proj(0, 0, 28), { stroke: "var(--line2)", "stroke-width": 1 });
    [["TV →", 300, 0, 0], ["radio →", 0, 50, 0], ["sales", 0, 0, 28]].forEach(function (L) { var p = proj(L[1], L[2], L[3]); var t = G.svg("text", { x: p[0] + 6, y: p[1] + 4, class: "albl" }, layer); t.textContent = L[0]; });
    // points below the surface first (drawn under it), then the surface mesh, then points above
    var below = [], above = [];
    for (var i = 0; i < n; i++) { var r = ADV_SALES[i] - f(ADV_TV[i], ADV_RADIO[i]); (r < 0 ? below : above).push(i); }
    function pts(list, col) { list.forEach(function (i) { var p = proj(ADV_TV[i], ADV_RADIO[i], ADV_SALES[i]), q = proj(ADV_TV[i], ADV_RADIO[i], f(ADV_TV[i], ADV_RADIO[i])); seg(p, q, { stroke: "var(--muted)", "stroke-width": 0.8, opacity: 0.7 }); G.svg("circle", { cx: p[0], cy: p[1], r: 2.8, fill: col }, layer); }); }
    pts(below, "var(--tool)");
    for (var g = 0; g <= 10; g++) {
      var a1 = [], a2 = [];
      for (var h = 0; h <= 20; h++) { a1.push(proj(30 * g, 2.5 * h, f(30 * g, 2.5 * h))); a2.push(proj(15 * h, 5 * g, f(15 * h, 5 * g))); }
      [a1, a2].forEach(function (A) { G.svg("path", { d: A.map(function (p, j) { return (j ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1); }).join(""), fill: "none", stroke: "var(--isl)", "stroke-width": 1, opacity: 0.55 }, layer); });
    }
    pts(above, "var(--bad)");
    var b = st.model === "add" ? ba : bi, R = 0, T = 0, m = ADV_SALES.reduce(function (s, v) { return s + v; }, 0) / n;
    for (i = 0; i < n; i++) { var e = ADV_SALES[i] - f(ADV_TV[i], ADV_RADIO[i]); R += e * e; T += (ADV_SALES[i] - m) * (ADV_SALES[i] - m); }
    ro.innerHTML = "<div>fitted model<b>" + (st.model === "add" ? "ŷ = " + b[0].toFixed(3) + " + " + b[1].toFixed(4) + "·TV + " + b[2].toFixed(4) + "·radio" : "ŷ = " + b[0].toFixed(2) + " + " + b[1].toFixed(4) + "·TV + " + b[2].toFixed(4) + "·radio + " + b[3].toFixed(5) + "·TV·radio") + "</b></div><div>RSS<b>" + G.fmt(R, 1) + "</b></div><div>R²<b>" + G.fmt(1 - R / T, 4) + "</b></div><div>points above / below<b>" + above.length + " red / " + below.length + " blue</b></div>";
  }
  draw();
});

/* ---------- isl3-2-confound: the newspaper paradox as a slider ---------- */
G.widget("isl3-2-confound", function (body) {
  var st = { rho: 0.35, seed: 3 };
  var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
  G.slider(ctr, { label: "correlation of newspaper with radio", min: 0, max: 0.95, step: 0.05, value: st.rho, fmt: function (v) { return (+v).toFixed(2); }, onChange: function (v) { st.rho = v; draw(); } });
  G.button(ctr, "New random markets", function () { st.seed++; draw(); });
  var ro = G.el("div", "readout"); body.appendChild(ro);
  var pl = G.plot(body, { w: 680, h: 320, x: [0, 60], y: [0, 30], xlabel: "newspaper budget (simulated)", ylabel: "sales", label: "sales against newspaper with simple and multiple regression slopes" });
  function draw() {
    var rng = G.rng(st.seed), n = 400, ra = [], nw = [], sa = [], X = [], i;
    for (i = 0; i < n; i++) {
      var z1 = G.randn(rng), z2 = G.randn(rng);
      var r = 25 + 14.5 * z1, w = Math.abs(25 + 10 * (st.rho * z1 + Math.sqrt(1 - st.rho * st.rho) * z2));
      ra.push(r); nw.push(w); sa.push(9 + 0.2 * r + 0 * w + 1.5 * G.randn(rng)); X.push([1, r, w]);
    }
    var S = isl31Sums(nw, sa), bm = isl32ols(X, sa), C = isl31Sums(ra, nw);
    var corr = C.cxy / Math.sqrt(C.cxx * (C.Syy - n * C.yb * C.yb));
    pl.clear();
    for (i = 0; i < n; i++) pl.dot(nw[i], sa[i], { r: 2.6, fill: "var(--ink2)", opacity: 0.6 });
    pl.line([[0, S.b0], [60, S.b0 + 60 * S.b1]], { stroke: "var(--bad)", "stroke-width": 2.6 });
    pl.line([[0, S.yb - S.xb * bm[2]], [60, S.yb + (60 - S.xb) * bm[2]]], { stroke: "var(--accent)", "stroke-width": 2.6, "stroke-dasharray": "7 5" });
    ro.innerHTML = "<div>true effect of newspaper<b>0</b></div><div>actual correlation(radio, newspaper)<b>" + G.fmt(corr, 2) + "</b></div><div>simple regression slope (red)<b>" + G.fmt(S.b1, 4) + "</b></div><div>multiple regression slope, radio held fixed (blue dashed)<b>" + G.fmt(bm[2], 4) + "</b></div>";
  }
  draw();
});

/* ---------- isl3-2-intervals: confidence vs prediction intervals along the TV line ---------- */
G.widget("isl3-2-intervals", function (body) {
  var S = isl31Sums(ADV_TV, ADV_SALES), n = S.n, b0 = S.b0, b1 = S.b1, rss = 0, i;
  for (i = 0; i < n; i++) { var e = ADV_SALES[i] - b0 - b1 * ADV_TV[i]; rss += e * e; }
  var rse = Math.sqrt(rss / (n - 2)), tq = 1.972017, st = { x0: 100 };
  var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
  G.slider(ctr, { label: "TV budget x₀", min: 0, max: 300, step: 1, value: st.x0, onChange: function (v) { st.x0 = v; draw(); } });
  var ro = G.el("div", "readout"); body.appendChild(ro);
  var pl = G.plot(body, { w: 680, h: 340, x: [0, 300], y: [0, 28], xlabel: "TV budget (thousand $)", ylabel: "sales", label: "confidence and prediction bands for sales on TV" });
  function sem(x) { return rse * Math.sqrt(1 / n + (x - S.xb) * (x - S.xb) / S.cxx); }
  function sep(x) { return rse * Math.sqrt(1 + 1 / n + (x - S.xb) * (x - S.xb) / S.cxx); }
  function band(fn, col, op) {
    var up = [], lo = [];
    for (var x = 0; x <= 300; x += 5) { var m = b0 + b1 * x; up.push([x, m + tq * fn(x)]); lo.push([x, m - tq * fn(x)]); }
    var pts = up.concat(lo.reverse());
    G.svg("path", { d: pts.map(function (p, j) { return (j ? "L" : "M") + pl.X(p[0]).toFixed(1) + " " + pl.Y(Math.max(0, Math.min(28, p[1]))).toFixed(1); }).join("") + "Z", fill: col, opacity: op }, pl.layer);
  }
  function draw() {
    pl.clear();
    band(sep, "var(--tool)", 0.18); band(sem, "var(--accent)", 0.45);
    for (i = 0; i < n; i++) pl.dot(ADV_TV[i], ADV_SALES[i], { r: 2.3, fill: "var(--ink2)", opacity: 0.6 });
    pl.line([[0, b0], [300, b0 + 300 * b1]], { stroke: "var(--accent)", "stroke-width": 2 });
    var x = st.x0, m = b0 + b1 * x;
    pl.line([[x, m - tq * sep(x)], [x, m + tq * sep(x)]], { stroke: "var(--tool)", "stroke-width": 5, opacity: 0.6 });
    pl.line([[x, m - tq * sem(x)], [x, m + tq * sem(x)]], { stroke: "var(--bad)", "stroke-width": 5 });
    pl.dot(x, m, { r: 5, fill: "var(--bad)", stroke: "var(--surface)", "stroke-width": 2 });
    ro.innerHTML = "<div>prediction ŷ₀<b>" + G.fmt(m, 3) + "</b></div><div>95% confidence interval (average sales)<b>[" + G.fmt(m - tq * sem(x), 2) + ", " + G.fmt(m + tq * sem(x), 2) + "]</b></div><div>95% prediction interval (one market)<b>[" + G.fmt(m - tq * sep(x), 2) + ", " + G.fmt(m + tq * sep(x), 2) + "]</b></div>";
  }
  draw();
});
