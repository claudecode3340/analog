/* isl2-2 · flexibility vs train/test MSE; bias–variance; KNN by hand; KNN decision boundary */
(function () {
  function cap(html) { var d = G.el("div", "wcap", html || ""); d.style.cssText = "font-size:13.5px;line-height:1.5;color:var(--ink2);margin:4px 4px 10px"; return d; }
  function solve(A, b) {
    var n = b.length, M = A.map(function (r, i) { return r.slice().concat([b[i]]); });
    for (var c = 0; c < n; c++) {
      var p = c; for (var r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
      var t = M[c]; M[c] = M[p]; M[p] = t;
      for (r = c + 1; r < n; r++) { var f = M[r][c] / M[c][c]; for (var k = c; k <= n; k++) M[r][k] -= f * M[c][k]; }
    }
    var x = new Array(n);
    for (var i = n - 1; i >= 0; i--) { var s = M[i][n]; for (var j = i + 1; j < n; j++) s -= M[i][j] * x[j]; x[i] = s / M[i][i]; }
    return x;
  }
  function legendre(u, d) { var P = [1, u]; for (var k = 1; k < d; k++) P.push(((2 * k + 1) * u * P[k] - k * P[k - 1]) / (k + 1)); return P.slice(0, d + 1); }
  function polyfit(xs, ys, d) {
    var m = d + 1, A = [], b = [], i;
    for (i = 0; i < m; i++) { A.push(new Array(m).fill(0)); b.push(0); }
    for (var n = 0; n < xs.length; n++) { var P = legendre((xs[n] - 50) / 50, d); for (i = 0; i < m; i++) { b[i] += P[i] * ys[n]; for (var j = 0; j < m; j++) A[i][j] += P[i] * P[j]; } }
    for (i = 0; i < m; i++) A[i][i] += 1e-9;
    var coef = solve(A, b);
    return function (x) { var P = legendre((x - 50) / 50, d), s = 0; for (var i = 0; i < m; i++) s += coef[i] * P[i]; return s; };
  }
  var TRUTH = {
    curvy: { f: function (x) { var s = Math.sin(Math.PI * x / 130); return 4 + 5.5 * s * s; }, y: [0, 13], name: "curvy (Fig 2.9)" },
    linear: { f: function (x) { return 2.5 + 0.1 * x + 0.2 * Math.sin(x / 15); }, y: [0, 15], name: "nearly linear (Fig 2.10)" },
    wiggly: { f: function (x) { return 12 + 13 * Math.exp(-x / 12) - 22 * Math.pow(x / 100, 6) + 2 * Math.exp(-Math.pow((x - 50) / 12, 2)); }, y: [-14, 30], name: "very non-linear (Fig 2.11)" }
  };
  // mulberry32: better-mixed than an LCG, so consecutive normal draws are independent
  function RNG(seed) { var a = (seed * 2654435761) >>> 0; return function () { a = (a + 0x6D2B79F5) >>> 0; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  function sim(f, n, rng) { var xs = [], ys = []; for (var i = 0; i < n; i++) { var x = 100 * rng(); xs.push(x); ys.push(f(x) + G.randn(rng)); } return [xs, ys]; }
  function mse(f, xs, ys) { var s = 0; for (var i = 0; i < xs.length; i++) { var e = ys[i] - f(xs[i]); s += e * e; } return s / xs.length; }

  /* ---------- flexibility: training vs test MSE ---------- */
  G.widget("isl2-2-flex", function (body, args) {
    var st = { t: "curvy", d: 4, draw: 0 }, seed = args.seed || 7;
    var ctl = G.el("div", "ctrls"); body.appendChild(ctl);
    G.seg(ctl, [["curvy", "curvy f"], ["linear", "nearly linear f"], ["wiggly", "very non-linear f"]], st.t, function (v) { st.t = v; data(); draw(); });
    G.slider(ctl, { label: "degree", min: 1, max: 15, step: 1, value: st.d, fmt: function (v) { return v + " (" + (v + 1) + " params)"; }, onChange: function (v) { st.d = v; draw(); } });
    G.button(ctl, "new training set", function () { st.draw++; data(); draw(); });
    var p1 = G.plot(body, { w: 680, h: 290, x: [0, 100], y: [0, 13], xlabel: "X", ylabel: "Y", label: "data, true f and the fitted polynomial" });
    var cap1 = cap(); body.appendChild(cap1);
    var p2 = G.plot(body, { w: 680, h: 250, x: [1, 16], y: [0, 4], xlabel: "flexibility (parameters = degree + 1)", ylabel: "MSE", label: "training and test MSE against flexibility" });
    body.appendChild(cap("<span style='color:var(--muted)'><b>grey</b></span>: training MSE · <span style='color:var(--bad)'><b>red</b></span>: test MSE · dashed: Var(ε) = 1, the floor · values above 4 are cut off"));
    var info = G.el("div", "readout"); body.appendChild(info);
    var D = {};
    function data() {
      var T = TRUTH[st.t], rng = RNG(seed + 101 * st.draw + (st.t === "linear" ? 7 : st.t === "wiggly" ? 13 : 0));
      D.tr = sim(T.f, 50, rng); D.te = sim(T.f, 1500, rng); D.tr_m = []; D.te_m = []; D.fits = [];
      for (var d = 1; d <= 15; d++) { var fh = polyfit(D.tr[0], D.tr[1], d); D.fits.push(fh); D.tr_m.push(mse(fh, D.tr[0], D.tr[1])); D.te_m.push(mse(fh, D.te[0], D.te[1])); }
    }
    function draw() {
      var T = TRUTH[st.t], lo = T.y[0], hi = T.y[1];
      var Y1 = function (v) { return (v - lo) / (hi - lo) * 13; };
      p1.clear();
      D.tr[0].forEach(function (x, i) { p1.dot(x, Y1(D.tr[1][i]), { r: 3.6, fill: "none", stroke: "var(--ink)", "stroke-width": 1.2 }); });
      var c1 = [], c2 = [], fh = D.fits[st.d - 1];
      for (var x = 0; x <= 100; x += 0.5) { c1.push([x, Y1(T.f(x))]); c2.push([x, Math.max(-0.5, Math.min(13.5, Y1(fh(x))))]); }
      p1.line(c1, { stroke: "var(--ink)", "stroke-width": 2.4 });
      p1.line(c2, { stroke: "var(--accent)", "stroke-width": 2.4 });
      cap1.innerHTML = "<b>" + T.name + "</b> · <b>black</b>: true f · <span style='color:var(--accent)'><b>blue</b></span>: the degree-" + st.d + " fit · circles: the 50 training points";
      p2.clear();
      var cap = 4, clip = function (v) { return Math.min(cap, v); };
      p2.line([[1, 1], [16, 1]], { stroke: "var(--ink)", "stroke-dasharray": "5 5", "stroke-width": 1.4 });
      p2.line(D.tr_m.map(function (v, i) { return [i + 2, clip(v)]; }), { stroke: "var(--muted)", "stroke-width": 2.4 });
      p2.line(D.te_m.map(function (v, i) { return [i + 2, clip(v)]; }), { stroke: "var(--bad)", "stroke-width": 2.6 });
      p2.dot(st.d + 1, clip(D.tr_m[st.d - 1]), { r: 6, fill: "var(--muted)" });
      p2.dot(st.d + 1, clip(D.te_m[st.d - 1]), { r: 6, fill: "var(--bad)" });
      var best = D.te_m.indexOf(Math.min.apply(null, D.te_m)) + 1;
      info.innerHTML = "<div>degree<b>" + st.d + "</b></div><div>training MSE<b>" + G.fmt(D.tr_m[st.d - 1], 3) + "</b></div><div>test MSE<b>" + G.fmt(D.te_m[st.d - 1], 3) + "</b></div><div>best degree for this training set<b>" + best + "</b></div>";
    }
    data(); draw();
  });

  /* ---------- bias–variance with 40 training sets ---------- */
  G.widget("isl2-2-bv", function (body, args) {
    var f = TRUTH.curvy.f, rng = RNG(args.seed || 5), sets = [], i;
    for (i = 0; i < 40; i++) sets.push(sim(f, 50, rng));
    var grid = []; for (var x = 5; x <= 95; x += 2.5) grid.push(x);
    var st = { d: 1 };
    var ctl = G.el("div", "ctrls"); body.appendChild(ctl);
    G.slider(ctl, { label: "degree", min: 1, max: 12, step: 1, value: 1, onChange: function (v) { st.d = v; draw(); } });
    var pl = G.plot(body, { w: 680, h: 300, x: [0, 100], y: [0, 13], xlabel: "X", ylabel: "f̂(X)", label: "forty fitted curves, their average and the truth" });
    body.appendChild(cap("<span style='color:var(--accent)'><b>faint blue</b></span>: 40 fits, one per training set · <span style='color:var(--math)'><b>orange</b></span>: their average · <b>black</b>: true f"));
    var bar = G.plot(body, { w: 680, h: 120, x: [0, 3.5], y: [0, 1], yticks: [], xlabel: "contribution to the expected test MSE", pad: { l: 20, r: 20, t: 10, b: 40 }, label: "stacked bar of bias squared, variance and irreducible error" });
    body.appendChild(cap("<span style='color:var(--isl)'><b>green</b></span>: bias² · <span style='color:var(--bad)'><b>red</b></span>: variance · <b>grey</b>: Var(ε) · total length = expected test MSE"));
    var info = G.el("div", "readout"); body.appendChild(info);
    function draw() {
      pl.clear(); bar.clear();
      var fits = sets.map(function (s) { return polyfit(s[0], s[1], st.d); });
      var xs = []; for (var x = 0; x <= 100; x += 1) xs.push(x);
      fits.forEach(function (fh) { pl.line(xs.map(function (x) { return [x, Math.max(-1, Math.min(14, fh(x)))]; }), { stroke: "var(--accent)", "stroke-width": 1, opacity: 0.28 }); });
      var avg = xs.map(function (x) { var s = 0; fits.forEach(function (fh) { s += fh(x); }); return [x, Math.max(-1, Math.min(14, s / fits.length))]; });
      pl.line(xs.map(function (x) { return [x, f(x)]; }), { stroke: "var(--ink)", "stroke-width": 2.6 });
      pl.line(avg, { stroke: "var(--math)", "stroke-width": 3 });
      var b2 = 0, v = 0;
      grid.forEach(function (x) { var p = fits.map(function (fh) { return fh(x); }), m = p.reduce(function (a, c) { return a + c; }, 0) / p.length; b2 += (m - f(x)) * (m - f(x)); v += p.reduce(function (a, c) { return a + (c - m) * (c - m); }, 0) / p.length; });
      b2 /= grid.length; v /= grid.length;
      var parts = [[b2, "var(--isl)", "bias²"], [v, "var(--bad)", "variance"], [1, "var(--muted)", "Var(ε)"]], at = 0;
      parts.forEach(function (p) {
        var w = Math.min(p[0], 3.5 - at); if (w <= 0) return;
        G.svg("rect", { x: bar.X(at), y: bar.Y(0.85), width: Math.max(0, bar.X(at + w) - bar.X(at)), height: bar.Y(0.15) - bar.Y(0.85), fill: p[1], opacity: 0.85 }, bar.layer);
        at += w;
      });
      info.innerHTML = "<div>bias² (avg over x)<b>" + G.fmt(b2, 3) + "</b></div><div>variance<b>" + G.fmt(v, 3) + "</b></div><div>Var(ε)<b>1</b></div><div>expected test MSE<b>" + G.fmt(b2 + v + 1, 3) + "</b></div>";
    }
    draw();
  });

  /* ---------- KNN by hand: drag the cross ---------- */
  var PTS = [[1, 7, 0, "B1"], [4, 5, 0, "B2"], [1, 4, 0, "B3"], [3, 1, 0, "B4"], [8, 9, 0, "B5"], [9, 7, 0, "B6"], [3, 8, 1, "O1"], [5, 9, 1, "O2"], [7, 8, 1, "O3"], [8, 4, 1, "O4"], [6, 3, 1, "O5"], [7, 2, 1, "O6"]];
  var COL = ["var(--accent)", "var(--math)"], NAME = ["blue", "orange"];
  G.widget("isl2-2-knn3", function (body) {
    var st = { K: 1, x: 3, y: 7 }, drag = false;
    var ctl = G.el("div", "ctrls"); body.appendChild(ctl);
    G.seg(ctl, [[1, "K = 1"], [3, "K = 3"], [5, "K = 5"], [7, "K = 7"]], 1, function (v) { st.K = v; draw(); });
    var pl = G.plot(body, { w: 560, h: 500, x: [0, 10], y: [0, 10], xlabel: "X₁", ylabel: "X₂", label: "twelve training points and a draggable test point" });
    var info = G.el("div", "readout"); body.appendChild(info);
    function draw() {
      pl.clear();
      var ds = PTS.map(function (p, i) { return [Math.hypot(p[0] - st.x, p[1] - st.y), i]; }).sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; });
      var r = ds[st.K - 1][0], nb = ds.slice(0, st.K).map(function (d) { return d[1]; });
      G.svg("ellipse", { cx: pl.X(st.x), cy: pl.Y(st.y), rx: Math.abs(pl.X(r) - pl.X(0)), ry: Math.abs(pl.Y(0) - pl.Y(r)), fill: "var(--good)", "fill-opacity": 0.14, stroke: "var(--good)", "stroke-width": 1.5 }, pl.layer);
      PTS.forEach(function (p, i) {
        pl.dot(p[0], p[1], { r: 8, fill: COL[p[2]], stroke: nb.indexOf(i) >= 0 ? "var(--ink)" : "var(--surface)", "stroke-width": nb.indexOf(i) >= 0 ? 3 : 2 });
        pl.text(p[0] + 0.25, p[1] + 0.3, p[3], { fill: "var(--muted)" });
      });
      var c = G.svg("g", { style: "cursor:grab" }, pl.layer), X = pl.X(st.x), Y = pl.Y(st.y);
      G.svg("circle", { cx: X, cy: Y, r: 16, fill: "transparent" }, c);
      G.svg("path", { d: "M" + (X - 8) + " " + (Y - 8) + "L" + (X + 8) + " " + (Y + 8) + "M" + (X + 8) + " " + (Y - 8) + "L" + (X - 8) + " " + (Y + 8), stroke: "var(--ink)", "stroke-width": 3.5 }, c);
      c.addEventListener("pointerdown", function (e) { drag = true; pl.svg.setPointerCapture(e.pointerId); e.preventDefault(); });
      var nO = nb.filter(function (i) { return PTS[i][2] === 1; }).length, nB = st.K - nO;
      var pred = nO > nB ? "orange" : nB > nO ? "blue" : "tie";
      info.innerHTML = "<div>test point<b>(" + G.fmt(st.x, 1) + ", " + G.fmt(st.y, 1) + ")</b></div><div>neighbours<b>" + nb.map(function (i) { return PTS[i][3]; }).join(", ") + "</b></div><div>Pr(blue) · Pr(orange)<b>" + nB + "/" + st.K + " · " + nO + "/" + st.K + "</b></div><div>prediction<b>" + pred + "</b></div>";
    }
    function at(e) { var b = pl.svg.getBoundingClientRect(), px = (e.clientX - b.left) / b.width * pl.W, py = (e.clientY - b.top) / b.height * pl.H; return [(px - pl.P.l) / (pl.W - pl.P.l - pl.P.r) * 10, (pl.H - pl.P.b - py) / (pl.H - pl.P.t - pl.P.b) * 10]; }
    pl.svg.addEventListener("pointermove", function (e) { if (!drag) return; var q = at(e); st.x = Math.max(0, Math.min(10, Math.round(q[0] * 10) / 10)); st.y = Math.max(0, Math.min(10, Math.round(q[1] * 10) / 10)); draw(); });
    pl.svg.addEventListener("pointerup", function () { drag = false; });
    pl.svg.style.touchAction = "none";
    draw();
  });

  /* ---------- KNN decision boundary on simulated mixture data ---------- */
  G.widget("isl2-2-knn", function (body, args) {
    var rng = RNG(args.seed || 11), s5 = Math.sqrt(0.2), i, j, k;
    var C = [[], []];
    for (i = 0; i < 10; i++) { C[0].push([1 + G.randn(rng), G.randn(rng)]); C[1].push([G.randn(rng), 1 + G.randn(rng)]); }
    function sample(n) { var P = []; for (var i = 0; i < n; i++) { var c = i < n / 2 ? 0 : 1, m = C[c][Math.floor(rng() * 10)]; P.push([m[0] + s5 * G.randn(rng), m[1] + s5 * G.randn(rng), c]); } return P; }
    function pO(x, y) { var a = 0, b = 0; for (var i = 0; i < 10; i++) { a += Math.exp(-(Math.pow(x - C[1][i][0], 2) + Math.pow(y - C[1][i][1], 2)) / 0.4); b += Math.exp(-(Math.pow(x - C[0][i][0], 2) + Math.pow(y - C[0][i][1], 2)) / 0.4); } return a / (a + b); }
    var TR = sample(200), TE = sample(2000), KMAX = 100;
    function cum(x, y) { var d = TR.map(function (p, i) { return [(p[0] - x) * (p[0] - x) + (p[1] - y) * (p[1] - y), i]; }); d.sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; }); var c = new Int16Array(KMAX + 1); for (var k = 1; k <= KMAX; k++) c[k] = c[k - 1] + TR[d[k - 1][1]][2]; return [c, TR[d[0][1]][2]]; }
    function predict(cc, K) { var o = cc[0][K]; return 2 * o > K ? 1 : 2 * o < K ? 0 : cc[1]; }
    var X0 = -2.6, X1 = 3.6, Y0 = -2.4, Y1 = 3.4, NG = 46, gx = [], gy = [], GC = [], GB = [];
    for (j = 0; j < NG; j++) for (i = 0; i < NG; i++) { var x = X0 + (i + 0.5) * (X1 - X0) / NG, y = Y0 + (j + 0.5) * (Y1 - Y0) / NG; gx.push(x); gy.push(y); GC.push(cum(x, y)); GB.push(pO(x, y)); }
    var TRC = TR.map(function (p) { return cum(p[0], p[1]); }), TEC = TE.map(function (p) { return cum(p[0], p[1]); });
    var bayes = TE.reduce(function (s, p) { var q = pO(p[0], p[1]); return s + 1 - Math.max(q, 1 - q); }, 0) / TE.length;
    var errTr = [0], errTe = [0];
    for (k = 1; k <= KMAX; k++) {
      errTr.push(TR.reduce(function (s, p, i) { return s + (predict(TRC[i], k) !== p[2] ? 1 : 0); }, 0) / TR.length);
      errTe.push(TE.reduce(function (s, p, i) { return s + (predict(TEC[i], k) !== p[2] ? 1 : 0); }, 0) / TE.length);
    }
    var st = { K: 1 };
    var ctl = G.el("div", "ctrls"); body.appendChild(ctl);
    G.slider(ctl, { label: "K", min: 1, max: 100, step: 1, value: 1, onChange: function (v) { st.K = v; draw(); } });
    var pl = G.plot(body, { w: 600, h: 560, x: [X0, X1], y: [Y0, Y1], xlabel: "X₁", ylabel: "X₂", label: "KNN decision regions, training points and the Bayes boundary" });
    var ch = G.plot(body, { w: 600, h: 230, x: [-2, 0], y: [0, 0.35], xticks: [], xlabel: "K (log scale; more flexible to the right)", ylabel: "error", pad: { l: 58, r: 16, t: 14, b: 44 }, label: "training and test error rate against 1/K" });
    body.appendChild(cap("<span style='color:var(--isl)'>■</span> training error &nbsp; <span style='color:var(--math)'>■</span> test error &nbsp; - - Bayes error rate &nbsp; · &nbsp; background: KNN prediction, <span style='color:var(--udl)'>purple dots</span>: Bayes boundary"));
    var info = G.el("div", "readout"); body.appendChild(info);
    var cw = (pl.X(X1) - pl.X(X0)) / NG, chh = (pl.Y(Y0) - pl.Y(Y1)) / NG;
    // static: Bayes boundary dots, error curves
    var lx = function (K) { return -Math.log10(K); };
    function draw() {
      pl.clear(); ch.clear();
      for (var n = 0; n < gx.length; n++) { var c = predict(GC[n], st.K); G.svg("rect", { x: pl.X(gx[n]) - cw / 2, y: pl.Y(gy[n]) - chh / 2, width: cw + 0.5, height: chh + 0.5, fill: COL[c], opacity: 0.16 }, pl.layer); }
      for (j = 0; j < NG; j++) for (i = 0; i < NG; i++) {
        var a = j * NG + i;
        if (i < NG - 1 && (GB[a] > 0.5) !== (GB[a + 1] > 0.5)) pl.dot((gx[a] + gx[a + 1]) / 2, gy[a], { r: 2.2, fill: "var(--udl)" });
        if (j < NG - 1 && (GB[a] > 0.5) !== (GB[a + NG] > 0.5)) pl.dot(gx[a], (gy[a] + gy[a + NG]) / 2, { r: 2.2, fill: "var(--udl)" });
      }
      TR.forEach(function (p) { if (p[0] < X0 || p[0] > X1 || p[1] < Y0 || p[1] > Y1) return; pl.dot(p[0], p[1], { r: 3.4, fill: "none", stroke: COL[p[2]], "stroke-width": 1.8 }); });
      [100, 50, 20, 10, 5, 2, 1].forEach(function (K) { ch.text(lx(K), -0.025, String(K), { "text-anchor": "middle" }); });
      ch.line([[-2, bayes], [0, bayes]], { stroke: "var(--ink)", "stroke-dasharray": "6 5", "stroke-width": 1.4 });
      var tr = [], te = []; for (var K = 1; K <= KMAX; K++) { tr.push([lx(K), errTr[K]]); te.push([lx(K), errTe[K]]); }
      ch.line(tr, { stroke: "var(--isl)", "stroke-width": 2 }); ch.line(te, { stroke: "var(--math)", "stroke-width": 2.2 });
      ch.dot(lx(st.K), errTr[st.K], { r: 5, fill: "var(--isl)" }); ch.dot(lx(st.K), errTe[st.K], { r: 5, fill: "var(--math)" });
      info.innerHTML = "<div>K<b>" + st.K + "</b></div><div>training error<b>" + G.fmt(errTr[st.K], 3) + "</b></div><div>test error (2,000 points)<b>" + G.fmt(errTe[st.K], 3) + "</b></div><div>Bayes error rate<b>" + G.fmt(bayes, 3) + "</b></div>";
    }
    draw();
  });
})();
