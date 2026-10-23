/* isl2-1 · reducible vs irreducible error; parametric vs flexible fits on Income1 */
(function () {
  function solve(A, b) { // Gaussian elimination with partial pivoting
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
  function polyfit(xs, ys, d, c, h) {
    var m = d + 1, A = [], b = [], i, j;
    for (i = 0; i < m; i++) { A.push(new Array(m).fill(0)); b.push(0); }
    xs.forEach(function (x, n) { var P = legendre((x - c) / h, d); for (var i = 0; i < m; i++) { b[i] += P[i] * ys[n]; for (var j = 0; j < m; j++) A[i][j] += P[i] * P[j]; } });
    for (i = 0; i < m; i++) A[i][i] += 1e-9;
    var coef = solve(A, b);
    return function (x) { var P = legendre((x - c) / h, d), s = 0; for (var i = 0; i < m; i++) s += coef[i] * P[i]; return s; };
  }
  function knnfit(xs, ys, K) {
    return function (x) {
      var o = xs.map(function (v, i) { return [Math.abs(v - x), i]; }).sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; });
      var s = 0; for (var k = 0; k < K; k++) s += ys[o[k][1]]; return s / K;
    };
  }

  /* ---------- reducible vs irreducible ---------- */
  G.widget("isl2-1-noise", function (body, args) {
    var rng = G.rng(args.seed || 3);
    var f = function (x) { return 20 + 60 / (1 + Math.exp(-(x - 16) / 1.4)); };
    var xs = [], zt = [], zs = [], i;
    for (i = 0; i < 30; i++) { xs.push(10 + 12 * i / 29); zt.push(G.randn(rng)); }
    for (i = 0; i < 200; i++) zs.push(G.randn(rng));
    var st = { sigma: 6, x0: 13, kind: "line" };
    var ctl = G.el("div", "ctrls"); body.appendChild(ctl);
    G.seg(ctl, [["line", "f̂ = straight line"], ["true", "f̂ = the true f"], ["flat", "f̂ = flat (mean)"]], st.kind, function (v) { st.kind = v; draw(); });
    G.slider(ctl, { label: "noise σ", min: 1, max: 15, step: 0.5, value: st.sigma, fmt: function (v) { return v.toFixed(1); }, onChange: function (v) { st.sigma = v; draw(); } });
    G.slider(ctl, { label: "x₀", min: 10, max: 22, step: 0.5, value: st.x0, fmt: function (v) { return v.toFixed(1); }, onChange: function (v) { st.x0 = v; draw(); } });
    var pl = G.plot(body, { w: 680, h: 360, x: [9.5, 22.5], y: [-5, 105], xlabel: "years of education", ylabel: "income", label: "true f, fitted f-hat and the spread of Y at x0" });
    var info = G.el("div", "readout"); body.appendChild(info);
    function draw() {
      pl.clear();
      var ys = xs.map(function (x, i) { return f(x) + st.sigma * zt[i]; });
      var fh;
      if (st.kind === "true") fh = f;
      else if (st.kind === "flat") { var m = ys.reduce(function (a, b) { return a + b; }, 0) / ys.length; fh = function () { return m; }; }
      else fh = polyfit(xs, ys, 1, 16, 6);
      var cur = [], cur2 = []; for (var x = 9.5; x <= 22.5; x += 0.1) { cur.push([x, f(x)]); cur2.push([x, fh(x)]); }
      xs.forEach(function (x, i) { pl.dot(x, ys[i], { r: 3.2, fill: "var(--muted)", opacity: 0.55 }); });
      pl.line(cur, { stroke: "var(--accent)", "stroke-width": 2.6 });
      pl.line(cur2, { stroke: "var(--math)", "stroke-width": 2.4, "stroke-dasharray": st.kind === "true" ? "7 5" : "none" });
      var fx = f(st.x0), fhx = fh(st.x0), se = 0;
      zs.forEach(function (z, k) { var Y = fx + st.sigma * z; se += (Y - fhx) * (Y - fhx); pl.dot(st.x0 + ((k % 9) - 4) * 0.035, Y, { r: 2, fill: "var(--isl)", opacity: 0.4 }); });
      se /= zs.length;
      pl.line([[st.x0, fx], [st.x0, fhx]], { stroke: "var(--bad)", "stroke-width": 4 });
      pl.dot(st.x0, fx, { r: 5, fill: "var(--accent)" }); pl.dot(st.x0, fhx, { r: 5, fill: "var(--math)" });
      pl.text(9.8, 99, "blue: true f · orange: f̂ · green: 200 possible Y at x₀ · red bar: f − f̂", { fill: "var(--muted)" });
      var red = (fx - fhx) * (fx - fhx), irr = st.sigma * st.sigma;
      info.innerHTML = "<div>f(x₀)<b>" + G.fmt(fx, 2) + "</b></div><div>f̂(x₀)<b>" + G.fmt(fhx, 2) + "</b></div><div>reducible [f−f̂]²<b>" + G.fmt(red, 2) + "</b></div><div>irreducible σ²<b>" + G.fmt(irr, 2) + "</b></div><div>total (formula)<b>" + G.fmt(red + irr, 2) + "</b></div><div>avg (Y−Ŷ)² over the 200 dots<b>" + G.fmt(se, 2) + "</b></div>";
    }
    draw();
  });

  /* ---------- parametric vs flexible on Income1 ---------- */
  var INC = [[10.0, 26.66], [10.4, 27.31], [10.84, 22.13], [11.24, 21.17], [11.65, 15.19], [12.09, 26.4], [12.49, 17.44], [12.89, 25.51], [13.29, 36.88], [13.73, 39.67], [14.13, 34.4], [14.54, 41.5], [14.98, 44.98], [15.38, 47.04], [15.78, 48.25], [16.22, 57.03], [16.62, 51.49], [17.02, 61.34], [17.46, 57.58], [17.87, 68.55], [18.27, 64.31], [18.71, 68.96], [19.11, 74.61], [19.51, 71.87], [19.91, 76.1], [20.35, 75.78], [20.76, 72.49], [21.16, 77.36], [21.6, 72.12], [22.0, 80.26]];
  G.widget("isl2-1-flex", function (body) {
    var xs = INC.map(function (p) { return p[0]; }), ys = INC.map(function (p) { return p[1]; });
    var KS = [29, 20, 15, 12, 10, 8, 6, 5, 4, 3, 2, 1];
    var st = { m: "poly", lev: 1 };
    var ctl = G.el("div", "ctrls"); body.appendChild(ctl);
    G.seg(ctl, [["poly", "Polynomial (parametric)"], ["knn", "K-nearest average (non-parametric)"]], st.m, function (v) { st.m = v; draw(); });
    G.slider(ctl, { label: "flexibility", min: 1, max: 12, step: 1, value: 1, fmt: function (v) { return String(v); }, onChange: function (v) { st.lev = v; draw(); } });
    var pl = G.plot(body, { w: 680, h: 340, x: [9.6, 22.4], y: [5, 95], xlabel: "years of education", ylabel: "income", label: "Income data with a fitted curve and residuals" });
    var info = G.el("div", "readout"); body.appendChild(info);
    function fitter(X, Y) { return st.m === "poly" ? polyfit(X, Y, st.lev, 16, 6) : knnfit(X, Y, Math.min(KS[st.lev - 1], X.length)); }
    function draw() {
      pl.clear();
      var fh = fitter(xs, ys), tr = 0, loo = 0;
      xs.forEach(function (x, i) { var e = ys[i] - fh(x); tr += e * e; pl.line([[x, ys[i]], [x, fh(x)]], { stroke: "var(--bad)", "stroke-width": 1.6, opacity: 0.8 }); });
      for (var i = 0; i < xs.length; i++) {
        var X2 = xs.filter(function (_, j) { return j !== i; }), Y2 = ys.filter(function (_, j) { return j !== i; });
        var e = ys[i] - fitter(X2, Y2)(xs[i]); loo += e * e;
      }
      tr /= xs.length; loo /= xs.length;
      var cur = []; for (var x = 9.7; x <= 22.3; x += 0.04) cur.push([x, Math.max(-20, Math.min(130, fh(x)))]);
      pl.line(cur, { stroke: "var(--math)", "stroke-width": 2.6 });
      xs.forEach(function (x, i) { pl.dot(x, ys[i], { r: 4.2, fill: "var(--accent)" }); });
      var what = st.m === "poly" ? "degree " + st.lev + " polynomial · " + (st.lev + 1) + " parameters" : "average of the K = " + KS[st.lev - 1] + " nearest people";
      info.innerHTML = "<div>model<b>" + what + "</b></div><div>training MSE (red)<b>" + G.fmt(tr, 1) + "</b></div><div>hidden-person MSE<b>" + G.fmt(loo, 1) + "</b></div>";
    }
    draw();
  });
})();
