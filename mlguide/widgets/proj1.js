/* proj1 · gradient descent on the TV-only loss bowl, and polynomial overfitting */
(function () {
  var TV = [230.1,44.5,17.2,151.5,180.8,8.7,57.5,120.2,8.6,199.8,66.1,214.7,23.8,97.5,204.1,195.4,67.8,281.4,69.2,147.3,218.4,237.4,13.2,228.3,62.3,262.9,142.9,240.1,248.8,70.6,292.9,112.9,97.2,265.6,95.7,290.7,266.9,74.7,43.1,228,202.5,177,293.6,206.9,25.1,175.1,89.7,239.9,227.2,66.9,199.8,100.4,216.4,182.6,262.7,198.9,7.3,136.2,210.8,210.7,53.5,261.3,239.3,102.7,131.1,69,31.5,139.3,237.4,216.8,199.1,109.8,26.8,129.4,213.4,16.9,27.5,120.5,5.4,116,76.4,239.8,75.3,68.4,213.5,193.2,76.3,110.7,88.3,109.8,134.3,28.6,217.7,250.9,107.4,163.3,197.6,184.9,289.7,135.2,222.4,296.4,280.2,187.9,238.2,137.9,25,90.4,13.1,255.4,225.8,241.7,175.7,209.6,78.2,75.1,139.2,76.4,125.7,19.4,141.3,18.8,224,123.1,229.5,87.2,7.8,80.2,220.3,59.6,0.7,265.2,8.4,219.8,36.9,48.3,25.6,273.7,43,184.9,73.4,193.7,220.5,104.6,96.2,140.3,240.1,243.2,38,44.7,280.7,121,197.6,171.3,187.8,4.1,93.9,149.8,11.7,131.7,172.5,85.7,188.4,163.5,117.2,234.5,17.9,206.8,215.4,284.3,50,164.5,19.6,168.4,222.4,276.9,248.4,170.2,276.7,165.6,156.6,218.5,56.2,287.6,253.8,205,139.5,191.1,286,18.7,39.5,75.5,17.2,166.8,149.7,38.2,94.2,177,283.6,232.1];
  var SALES = [22.1,10.4,9.3,18.5,12.9,7.2,11.8,13.2,4.8,10.6,8.6,17.4,9.2,9.7,19,22.4,12.5,24.4,11.3,14.6,18,12.5,5.6,15.5,9.7,12,15,15.9,18.9,10.5,21.4,11.9,9.6,17.4,9.5,12.8,25.4,14.7,10.1,21.5,16.6,17.1,20.7,12.9,8.5,14.9,10.6,23.2,14.8,9.7,11.4,10.7,22.6,21.2,20.2,23.7,5.5,13.2,23.8,18.4,8.1,24.2,15.7,14,18,9.3,9.5,13.4,18.9,22.3,18.3,12.4,8.8,11,17,8.7,6.9,14.2,5.3,11,11.8,12.3,11.3,13.6,21.7,15.2,12,16,12.9,16.7,11.2,7.3,19.4,22.2,11.5,16.9,11.7,15.5,25.4,17.2,11.7,23.8,14.8,14.7,20.7,19.2,7.2,8.7,5.3,19.8,13.4,21.8,14.1,15.9,14.6,12.6,12.2,9.4,15.9,6.6,15.5,7,11.6,15.2,19.7,10.6,6.6,8.8,24.7,9.7,1.6,12.7,5.7,19.6,10.8,11.6,9.5,20.8,9.6,20.7,10.9,19.2,20.1,10.4,11.4,10.3,13.2,25.4,10.9,10.1,16.1,11.6,16.6,19,15.6,3.2,15.3,10.1,7.3,12.9,14.4,13.3,14.9,18,11.9,11.9,8,12.2,17.1,15,8.4,14.5,7.6,11.7,11.5,27,20.2,11.7,11.8,12.6,10.5,12.2,8.7,26.2,17.6,22.6,10.3,17.3,15.9,6.7,10.8,9.9,5.9,19.6,17.3,7.6,9.7,12.8,25.5,13.4];
  var N = TV.length;
  function mean(a) { var s = 0; for (var i = 0; i < a.length; i++) s += a[i]; return s / a.length; }
  function sd(a, m) { var s = 0; for (var i = 0; i < a.length; i++) s += (a[i] - m) * (a[i] - m); return Math.sqrt(s / a.length); }
  var uid = 0;
  function clip(pl) {
    var id = "proj1-clip-" + (++uid);
    var defs = G.svg("defs", {}, pl.svg), cp = G.svg("clipPath", { id: id }, defs);
    G.svg("rect", { x: pl.P.l, y: pl.P.t, width: pl.W - pl.P.l - pl.P.r, height: pl.H - pl.P.t - pl.P.b }, cp);
    pl.layer.setAttribute("clip-path", "url(#" + id + ")");
  }
  function twoUp(body) {
    var host = G.el("div"); host.style.cssText = "display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:12px;margin-top:10px"; body.appendChild(host);
    var a = G.el("div"), b = G.el("div"); host.appendChild(a); host.appendChild(b); return [a, b];
  }

  G.widget("proj1-gd", function (body) {
    var mTV = mean(TV), sTV = sd(TV, mTV), my = mean(SALES);
    var mode = "raw", logLr = Math.log10(3e-5), steps = 1000, anim = null;
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    G.seg(ctr, [["raw", "raw TV"], ["z", "standardised TV"]], mode, function (v) { mode = v; logLr = v === "raw" ? Math.log10(3e-5) : -1; lrS.set(logLr); steps = v === "raw" ? 1000 : 30; stS.set(steps); draw(); });
    var lrS = G.slider(ctr, { label: "step size η", min: -6, max: 0.2, step: 0.05, value: logLr, fmt: function (v) { return Math.pow(10, v).toExponential(1); }, onChange: function (v) { logLr = v; draw(); } });
    var stS = G.slider(ctr, { label: "steps", min: 1, max: 2000, step: 1, value: 1000, onChange: function (v) { steps = v; draw(); } });
    G.button(ctr, "Run ▶", function () {
      if (anim) clearInterval(anim); var t = 1;
      anim = setInterval(function () { t = Math.min(2000, Math.ceil(t * 1.12 + 1)); steps = t; stS.set(t); draw(); if (t >= 2000) { clearInterval(anim); anim = null; } }, 60);
    });
    var info = G.el("div", "readout"); body.appendChild(info);
    var hs = twoUp(body);
    function stats() {
      var x = TV.map(function (v) { return mode === "raw" ? v : (v - mTV) / sTV; });
      var a12 = mean(x), a22 = mean(x.map(function (v) { return v * v; }));
      var c2 = mean(x.map(function (v, i) { return v * SALES[i]; })), yy = mean(SALES.map(function (v) { return v * v; }));
      var det = a22 - a12 * a12;
      return { a11: 1, a12: a12, a22: a22, c1: my, c2: c2, yy: yy, b0: (a22 * my - a12 * c2) / det, b1: (c2 - a12 * my) / det };
    }
    function loss(S, b0, b1) { return S.yy - 2 * (b0 * S.c1 + b1 * S.c2) + S.a11 * b0 * b0 + 2 * S.a12 * b0 * b1 + S.a22 * b1 * b1; }
    function draw() {
      var S = stats(), lr = Math.pow(10, logLr), Lst = loss(S, S.b0, S.b1);
      var R = mode === "raw" ? { x: [-1, 9], y: [-0.01, 0.1] } : { x: [-2, 16], y: [-3, 8.5] };
      hs[0].innerHTML = ""; hs[1].innerHTML = "";
      var pl = G.plot(hs[0], { w: 520, h: 340, x: R.x, y: R.y, xlabel: "β₀ (intercept)", ylabel: mode === "raw" ? "β₁ (per $1k of TV)" : "β₁ (per SD of TV)", pad: { l: 64, r: 16, t: 14, b: 44 }, label: "loss contours with the gradient descent path" });
      clip(pl);
      var tr = S.a11 + S.a22, dt = S.a11 * S.a22 - S.a12 * S.a12, disc = Math.sqrt(Math.max(0, tr * tr / 4 - dt));
      var l1 = tr / 2 + disc, l2 = tr / 2 - disc, v1 = Math.abs(S.a12) < 1e-12 ? (S.a11 >= S.a22 ? [1, 0] : [0, 1]) : [S.a12, l1 - S.a11], nv = Math.hypot(v1[0], v1[1]); v1 = [v1[0] / nv, v1[1] / nv]; var v2 = [-v1[1], v1[0]];
      [0.5, 2, 8, 30, 100, 300].forEach(function (c) {
        var pts = []; for (var k = 0; k <= 200; k++) { var th = k / 200 * 2 * Math.PI, u = Math.sqrt(c / l1) * Math.cos(th), w = Math.sqrt(c / l2) * Math.sin(th); pts.push([S.b0 + u * v1[0] + w * v2[0], S.b1 + u * v1[1] + w * v2[1]]); }
        pl.line(pts, { stroke: "var(--line2)", "stroke-width": 1.2 });
      });
      var b = [0, 0], path = [b.slice()], Ls = [loss(S, 0, 0)], div = false;
      for (var t = 0; t < steps; t++) {
        var g0 = 2 * (S.a11 * b[0] + S.a12 * b[1] - S.c1), g1 = 2 * (S.a12 * b[0] + S.a22 * b[1] - S.c2);
        b = [b[0] - lr * g0, b[1] - lr * g1]; var L = loss(S, b[0], b[1]);
        if (!isFinite(L) || L > 1e8) { div = true; break; }
        path.push(b.slice()); Ls.push(L);
      }
      var cl = function (p) { return [Math.max(R.x[0] - 50, Math.min(R.x[1] + 50, p[0])), Math.max(R.y[0] - 50, Math.min(R.y[1] + 50, p[1]))]; };
      pl.line(path.map(cl), { stroke: "var(--proj)", "stroke-width": 2 });
      path.forEach(function (p, i) { if (i < 40 || i === path.length - 1) { var q = cl(p); pl.dot(q[0], q[1], { r: i === path.length - 1 ? 5.5 : 2.4, fill: i === path.length - 1 ? "var(--bad)" : "var(--proj)" }); } });
      pl.dot(S.b0, S.b1, { r: 7, fill: "none", stroke: "var(--ink)", "stroke-width": 2 });
      pl.text(S.b0, S.b1, "minimum", { fill: "var(--ink)", "font-weight": 700, dy: -12, "text-anchor": "middle" });
      pl.text(0, 0, "start", { fill: "var(--muted)", dy: 16, dx: 4 });
      var X2 = Math.max(10, steps);
      var p2 = G.plot(hs[1], { w: 520, h: 340, x: [0, X2], y: [0.5, 2.6], xlabel: "step", ylabel: "log₁₀ training MSE", label: "loss curve" });
      clip(p2);
      p2.line([[0, Math.log10(Lst)], [X2, Math.log10(Lst)]], { stroke: "var(--ink)", "stroke-dasharray": "5 4", "stroke-width": 1.2 });
      p2.text(X2 * 0.98, Math.log10(Lst), "best possible: " + G.fmt(Lst, 2), { dy: 18, fill: "var(--muted)", "text-anchor": "end" });
      p2.line(Ls.map(function (L, i) { return [i, Math.log10(Math.max(L, 1e-3))]; }), { stroke: "var(--proj)" });
      var last = Ls[Ls.length - 1], bL = path[path.length - 1], d1 = mode === "raw" ? 4 : 3;
      info.innerHTML = "<div>stable if η &lt;<b>" + (1 / l1).toExponential(2) + "</b></div><div>condition number<b>" + G.fmt(l1 / l2, 1) + "</b></div><div>loss now<b>" + (div ? "diverged!" : G.fmt(last, 3)) + "</b></div><div>β₀, β₁ now<b>" + (div ? "—" : G.fmt(bL[0], 3) + ", " + G.fmt(bL[1], d1)) + "</b></div><div>target β₀, β₁<b>" + G.fmt(S.b0, 3) + ", " + G.fmt(S.b1, d1) + "</b></div>";
    }
    draw();
  });

  G.widget("proj1-poly", function (body) {
    var deg = 3, seed = 3;
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    G.slider(ctr, { label: "degree", min: 1, max: 10, step: 1, value: deg, onChange: function (v) { deg = v; draw(); } });
    G.button(ctr, "New training sample", function () { seed++; draw(); });
    var info = G.el("div", "readout"); body.appendChild(info);
    var hs = twoUp(body);
    function lsq(V, y) { // least squares by modified Gram–Schmidt QR (never forms V^T V)
      var n = V.length, p = V[0].length, Q = V.map(function (r) { return r.slice(); }), Rm = [], i, j, k;
      for (j = 0; j < p; j++) Rm.push(new Array(p).fill(0));
      for (j = 0; j < p; j++) {
        var nr = 0; for (i = 0; i < n; i++) nr += Q[i][j] * Q[i][j]; nr = Math.sqrt(nr); Rm[j][j] = nr; for (i = 0; i < n; i++) Q[i][j] /= nr;
        for (k = j + 1; k < p; k++) { var d = 0; for (i = 0; i < n; i++) d += Q[i][j] * Q[i][k]; Rm[j][k] = d; for (i = 0; i < n; i++) Q[i][k] -= d * Q[i][j]; }
      }
      var qy = []; for (j = 0; j < p; j++) { var s = 0; for (i = 0; i < n; i++) s += Q[i][j] * y[i]; qy.push(s); }
      var b = new Array(p).fill(0); for (j = p - 1; j >= 0; j--) { var t = qy[j]; for (k = j + 1; k < p; k++) t -= Rm[j][k] * b[k]; b[j] = t / Rm[j][j]; }
      return b;
    }
    function row(z, d) { var r = [], v = 1; for (var k = 0; k <= d; k++) { r.push(v); v *= z; } return r; }
    function pred(b, z) { var s = 0, v = 1; for (var k = 0; k < b.length; k++) { s += b[k] * v; v *= z; } return s; }
    function draw() {
      var r = G.rng(seed * 7919 + 11), idx = [], i; for (i = 0; i < N; i++) idx.push(i);
      for (i = N - 1; i > 0; i--) { var j = Math.floor(r() * (i + 1)), t = idx[i]; idx[i] = idx[j]; idx[j] = t; }
      var tr = idx.slice(0, 20), te = idx.slice(20);
      var xt = tr.map(function (i) { return TV[i]; }), m = mean(xt), s = sd(xt, m);
      var curves = [], errs = [];
      for (var d = 1; d <= 10; d++) {
        var b = lsq(tr.map(function (i) { return row((TV[i] - m) / s, d); }), tr.map(function (i) { return SALES[i]; }));
        var e = function (set) { var q = 0; set.forEach(function (i) { var u = SALES[i] - pred(b, (TV[i] - m) / s); q += u * u; }); return q / set.length; };
        curves.push(b); errs.push([e(tr), e(te)]);
      }
      hs[0].innerHTML = ""; hs[1].innerHTML = "";
      var pl = G.plot(hs[0], { w: 520, h: 340, x: [0, 300], y: [0, 30], xlabel: "TV budget ($1000s)", ylabel: "sales (1000 units)", label: "polynomial fit to 20 training markets" });
      clip(pl);
      te.forEach(function (i) { pl.dot(TV[i], SALES[i], { r: 2.6, fill: "var(--muted)", opacity: 0.35 }); });
      tr.forEach(function (i) { pl.dot(TV[i], SALES[i], { r: 5, fill: "var(--proj)", stroke: "var(--surface)", "stroke-width": 1.5 }); });
      var bb = curves[deg - 1], pts = []; for (var x = 0; x <= 300; x += 1) pts.push([x, Math.max(-20, Math.min(50, pred(bb, (x - m) / s)))]);
      pl.line(pts, { stroke: "var(--bad)", "stroke-width": 2.4 });
      var lg = errs.map(function (e) { return [Math.log10(e[0]), Math.log10(e[1])]; });
      var p2 = G.plot(hs[1], { w: 520, h: 340, x: [0.5, 10.5], y: [0, 4], xlabel: "polynomial degree", ylabel: "log₁₀ MSE", xticks: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], label: "training and test error for every degree" });
      clip(p2);
      G.svg("rect", { x: p2.X(deg - 0.5), y: p2.P.t, width: p2.X(1) - p2.X(0), height: p2.H - p2.P.t - p2.P.b, fill: "var(--panel)" }, p2.layer);
      p2.line(lg.map(function (v, i) { return [i + 1, v[0]]; }), { stroke: "var(--proj)" });
      p2.line(lg.map(function (v, i) { return [i + 1, Math.min(v[1], 4.2)]; }), { stroke: "var(--bad)" });
      lg.forEach(function (v, i) { p2.dot(i + 1, v[0], { fill: "var(--proj)" }); p2.dot(i + 1, Math.min(v[1], 4.2), { fill: "var(--bad)" }); });
      p2.text(1.15, lg[0][0], "training", { dy: 18, fill: "var(--proj)", "font-weight": 700 });
      p2.text(1.15, lg[0][1], "test", { dy: -10, fill: "var(--bad)", "font-weight": 700 });
      info.innerHTML = "<div>coefficients<b>" + (deg + 1) + "</b></div><div>training MSE (20 markets)<b>" + G.fmt(errs[deg - 1][0], 2) + "</b></div><div>test MSE (180 markets)<b>" + G.fmt(errs[deg - 1][1], 1) + "</b></div>";
    }
    draw();
  });
})();
