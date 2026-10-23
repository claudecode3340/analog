/* isl3-1 · simple linear regression widgets. Advertising data (ISLP) embedded: TV and radio budgets, sales. Also used by isl3-2.js. */
var ADV_TV=[230.1,44.5,17.2,151.5,180.8,8.7,57.5,120.2,8.6,199.8,66.1,214.7,23.8,97.5,204.1,195.4,67.8,281.4,69.2,147.3,218.4,237.4,13.2,228.3,62.3,262.9,142.9,240.1,248.8,70.6,292.9,112.9,97.2,265.6,95.7,290.7,266.9,74.7,43.1,228,202.5,177,293.6,206.9,25.1,175.1,89.7,239.9,227.2,66.9,199.8,100.4,216.4,182.6,262.7,198.9,7.3,136.2,210.8,210.7,53.5,261.3,239.3,102.7,131.1,69,31.5,139.3,237.4,216.8,199.1,109.8,26.8,129.4,213.4,16.9,27.5,120.5,5.4,116,76.4,239.8,75.3,68.4,213.5,193.2,76.3,110.7,88.3,109.8,134.3,28.6,217.7,250.9,107.4,163.3,197.6,184.9,289.7,135.2,222.4,296.4,280.2,187.9,238.2,137.9,25,90.4,13.1,255.4,225.8,241.7,175.7,209.6,78.2,75.1,139.2,76.4,125.7,19.4,141.3,18.8,224,123.1,229.5,87.2,7.8,80.2,220.3,59.6,0.7,265.2,8.4,219.8,36.9,48.3,25.6,273.7,43,184.9,73.4,193.7,220.5,104.6,96.2,140.3,240.1,243.2,38,44.7,280.7,121,197.6,171.3,187.8,4.1,93.9,149.8,11.7,131.7,172.5,85.7,188.4,163.5,117.2,234.5,17.9,206.8,215.4,284.3,50,164.5,19.6,168.4,222.4,276.9,248.4,170.2,276.7,165.6,156.6,218.5,56.2,287.6,253.8,205,139.5,191.1,286,18.7,39.5,75.5,17.2,166.8,149.7,38.2,94.2,177,283.6,232.1];
var ADV_RADIO=[37.8,39.3,45.9,41.3,10.8,48.9,32.8,19.6,2.1,2.6,5.8,24,35.1,7.6,32.9,47.7,36.6,39.6,20.5,23.9,27.7,5.1,15.9,16.9,12.6,3.5,29.3,16.7,27.1,16,28.3,17.4,1.5,20,1.4,4.1,43.8,49.4,26.7,37.7,22.3,33.4,27.7,8.4,25.7,22.5,9.9,41.5,15.8,11.7,3.1,9.6,41.7,46.2,28.8,49.4,28.1,19.2,49.6,29.5,2,42.7,15.5,29.6,42.8,9.3,24.6,14.5,27.5,43.9,30.6,14.3,33,5.7,24.6,43.7,1.6,28.5,29.9,7.7,26.7,4.1,20.3,44.5,43,18.4,27.5,40.6,25.5,47.8,4.9,1.5,33.5,36.5,14,31.6,3.5,21,42.3,41.7,4.3,36.3,10.1,17.2,34.3,46.4,11,0.3,0.4,26.9,8.2,38,15.4,20.6,46.8,35,14.3,0.8,36.9,16,26.8,21.7,2.4,34.6,32.3,11.8,38.9,0,49,12,39.6,2.9,27.2,33.5,38.6,47,39,28.9,25.9,43.9,17,35.4,33.2,5.7,14.8,1.9,7.3,49,40.3,25.8,13.9,8.4,23.3,39.7,21.1,11.6,43.5,1.3,36.9,18.4,18.1,35.8,18.1,36.8,14.7,3.4,37.6,5.2,23.6,10.6,11.6,20.9,20.1,7.1,3.4,48.9,30.2,7.8,2.3,10,2.6,5.4,5.7,43,21.3,45.1,2.1,28.7,13.9,12.1,41.1,10.8,4.1,42,35.6,3.7,4.9,9.3,42,8.6];
var ADV_NEWS=[69.2,45.1,69.3,58.5,58.4,75,23.5,11.6,1,21.2,24.2,4,65.9,7.2,46,52.9,114,55.8,18.3,19.1,53.4,23.5,49.6,26.2,18.3,19.5,12.6,22.9,22.9,40.8,43.2,38.6,30,0.3,7.4,8.5,5,45.7,35.1,32,31.6,38.7,1.8,26.4,43.3,31.5,35.7,18.5,49.9,36.8,34.6,3.6,39.6,58.7,15.9,60,41.4,16.6,37.7,9.3,21.4,54.7,27.3,8.4,28.9,0.9,2.2,10.2,11,27.2,38.7,31.7,19.3,31.3,13.1,89.4,20.7,14.2,9.4,23.1,22.3,36.9,32.5,35.6,33.8,65.7,16,63.2,73.4,51.4,9.3,33,59,72.3,10.9,52.9,5.9,22,51.2,45.9,49.8,100.9,21.4,17.9,5.3,59,29.7,23.2,25.6,5.5,56.5,23.2,2.4,10.7,34.5,52.7,25.6,14.8,79.2,22.3,46.2,50.4,15.6,12.4,74.2,25.9,50.6,9.2,3.2,43.1,8.7,43,2.1,45.1,65.6,8.5,9.3,59.7,20.5,1.7,12.9,75.6,37.9,34.4,38.9,9,8.7,44.3,11.9,20.6,37,48.7,14.2,37.7,9.5,5.7,50.5,24.3,45.2,34.6,30.7,49.3,25.6,7.4,5.4,84.8,21.6,19.4,57.6,6.4,18.4,47.4,17,12.8,13.1,41.8,20.3,35.2,23.7,17.6,8.3,27.4,29.7,71.8,30,19.6,26.6,18.2,3.7,23.4,5.8,6,31.6,3.6,6,13.8,8.1,6.4,66.2,8.7];
var ADV_SALES=[22.1,10.4,9.3,18.5,12.9,7.2,11.8,13.2,4.8,10.6,8.6,17.4,9.2,9.7,19,22.4,12.5,24.4,11.3,14.6,18,12.5,5.6,15.5,9.7,12,15,15.9,18.9,10.5,21.4,11.9,9.6,17.4,9.5,12.8,25.4,14.7,10.1,21.5,16.6,17.1,20.7,12.9,8.5,14.9,10.6,23.2,14.8,9.7,11.4,10.7,22.6,21.2,20.2,23.7,5.5,13.2,23.8,18.4,8.1,24.2,15.7,14,18,9.3,9.5,13.4,18.9,22.3,18.3,12.4,8.8,11,17,8.7,6.9,14.2,5.3,11,11.8,12.3,11.3,13.6,21.7,15.2,12,16,12.9,16.7,11.2,7.3,19.4,22.2,11.5,16.9,11.7,15.5,25.4,17.2,11.7,23.8,14.8,14.7,20.7,19.2,7.2,8.7,5.3,19.8,13.4,21.8,14.1,15.9,14.6,12.6,12.2,9.4,15.9,6.6,15.5,7,11.6,15.2,19.7,10.6,6.6,8.8,24.7,9.7,1.6,12.7,5.7,19.6,10.8,11.6,9.5,20.8,9.6,20.7,10.9,19.2,20.1,10.4,11.4,10.3,13.2,25.4,10.9,10.1,16.1,11.6,16.6,19,15.6,3.2,15.3,10.1,7.3,12.9,14.4,13.3,14.9,18,11.9,11.9,8,12.2,17.1,15,8.4,14.5,7.6,11.7,11.5,27,20.2,11.7,11.8,12.6,10.5,12.2,8.7,26.2,17.6,22.6,10.3,17.3,15.9,6.7,10.8,9.9,5.9,19.6,17.3,7.6,9.7,12.8,25.5,13.4];
/* shared small helpers (also used by isl3-2.js / isl3-3.js, which load after this file) */
function isl31Grid(body) { var d = G.el("div"); d.style.cssText = "display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:10px;align-items:start"; body.appendChild(d); return d; }
function isl31Sums(x, y) {
  var n = x.length, Sx = 0, Sy = 0, Sxx = 0, Sxy = 0, Syy = 0;
  for (var i = 0; i < n; i++) { Sx += x[i]; Sy += y[i]; Sxx += x[i] * x[i]; Sxy += x[i] * y[i]; Syy += y[i] * y[i]; }
  var xb = Sx / n, yb = Sy / n, cxx = Sxx - n * xb * xb, cxy = Sxy - n * xb * yb;
  var b1 = cxy / cxx, b0 = yb - b1 * xb;
  return { n: n, Sx: Sx, Sy: Sy, Sxx: Sxx, Sxy: Sxy, Syy: Syy, xb: xb, yb: yb, cxx: cxx, cxy: cxy, b0: b0, b1: b1 };
}

/* ---------- isl3-1-rss: drag a line, see residuals, RSS and the RSS contour map ---------- */
G.widget("isl3-1-rss", function (body) {
  var x = ADV_TV, y = ADV_SALES, S = isl31Sums(x, y);
  function rss(b0, b1) { return S.Syy - 2 * b0 * S.Sy - 2 * b1 * S.Sxy + S.n * b0 * b0 + 2 * b0 * b1 * S.Sx + b1 * b1 * S.Sxx; }
  var minR = rss(S.b0, S.b1);
  var st = { b0: 5.5, b1: 0.06 };
  var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
  var s0 = G.slider(ctr, { label: "intercept β₀", min: 4, max: 10, step: 0.01, value: st.b0, fmt: function (v) { return v.toFixed(2); }, onChange: function (v) { st.b0 = v; draw(); } });
  var s1 = G.slider(ctr, { label: "slope β₁", min: 0.025, max: 0.07, step: 0.0005, value: st.b1, fmt: function (v) { return v.toFixed(4); }, onChange: function (v) { st.b1 = v; draw(); } });
  G.button(ctr, "Jump to least squares", function () { st.b0 = S.b0; st.b1 = S.b1; s0.set(st.b0.toFixed(2)); s1.set(st.b1.toFixed(4)); draw(); });
  var ro = G.el("div", "readout"); body.appendChild(ro);
  var grid = isl31Grid(body);
  var left = G.el("div"), right = G.el("div"); grid.appendChild(left); grid.appendChild(right);
  var pl = G.plot(left, { w: 460, h: 340, x: [0, 300], y: [0, 28], xlabel: "TV budget (thousand $)", ylabel: "sales (thousand units)", label: "Advertising data with your line and residuals" });
  var B0 = [4, 10], B1 = [0.025, 0.07];
  var pc = G.plot(right, { w: 460, h: 340, x: B0, y: B1, xlabel: "β₀ (intercept)", ylabel: "β₁ (slope)", pad: { l: 64, r: 14, t: 14, b: 44 }, label: "contours of RSS over intercept and slope" });
  var levels = [2.11, 2.15, 2.2, 2.3, 2.5, 3, 4, 6];
  var cl = G.svg("g", {}); pc.svg.insertBefore(cl, pc.layer);
  levels.forEach(function (L) {
    var pts = [];
    for (var k = 0; k <= 180; k++) {
      var th = 2 * Math.PI * k / 180, u0 = Math.cos(th), u1 = Math.sin(th) * 0.01;
      var q = S.n * u0 * u0 + 2 * S.Sx * u0 * u1 + S.Sxx * u1 * u1;
      var r = Math.sqrt(Math.max(0, (L * 1000 - minR) / q));
      pts.push([S.b0 + r * u0, S.b1 + r * u1]);
    }
    var d = pts.map(function (p, i) { return (i ? "L" : "M") + pc.X(Math.max(B0[0], Math.min(B0[1], p[0]))).toFixed(1) + " " + pc.Y(Math.max(B1[0], Math.min(B1[1], p[1]))).toFixed(1); }).join("");
    G.svg("path", { d: d, fill: "none", stroke: "var(--isl)", "stroke-width": 1.2, opacity: 0.75 }, cl);
    var top = pts.reduce(function (a, b) { return b[1] > a[1] ? b : a; });
    if (top[1] < B1[1] && top[0] > B0[0] && top[0] < B0[1]) { var t = G.svg("text", { x: pc.X(top[0]), y: pc.Y(top[1]) - 3, "text-anchor": "middle", class: "tick", fill: "var(--isl)" }, cl); t.textContent = L; }
  });
  pc.svg.style.cursor = "crosshair";
  pc.svg.addEventListener("pointerdown", function (e) {
    var r = pc.svg.getBoundingClientRect(), px = (e.clientX - r.left) / r.width * pc.W, py = (e.clientY - r.top) / r.height * pc.H;
    var b0 = B0[0] + (px - pc.P.l) / (pc.W - pc.P.l - pc.P.r) * (B0[1] - B0[0]);
    var b1 = B1[0] + (pc.H - pc.P.b - py) / (pc.H - pc.P.t - pc.P.b) * (B1[1] - B1[0]);
    if (b0 < B0[0] || b0 > B0[1] || b1 < B1[0] || b1 > B1[1]) return;
    st.b0 = b0; st.b1 = b1; s0.set(b0.toFixed(2)); s1.set(b1.toFixed(4)); draw();
  });
  function draw() {
    pl.clear(); pc.clear();
    for (var i = 0; i < x.length; i++) pl.line([[x[i], y[i]], [x[i], st.b0 + st.b1 * x[i]]], { stroke: "var(--bad)", "stroke-width": 1, opacity: 0.55 });
    for (i = 0; i < x.length; i++) pl.dot(x[i], y[i], { r: 2.6, fill: "var(--ink2)" });
    pl.line([[0, st.b0], [300, st.b0 + 300 * st.b1]], { stroke: "var(--accent)", "stroke-width": 2.6 });
    pc.dot(S.b0, S.b1, { r: 5, fill: "var(--bad)" });
    pc.text(S.b0 + 0.1, S.b1 - 0.003, "least squares", { fill: "var(--bad)" });
    pc.dot(st.b0, st.b1, { r: 6, fill: "var(--accent)", stroke: "var(--surface)", "stroke-width": 2 });
    var R = rss(st.b0, st.b1);
    ro.innerHTML = "<div>your line<b>ŷ = " + st.b0.toFixed(2) + " + " + st.b1.toFixed(4) + "x</b></div><div>your RSS<b>" + G.fmt(R, 1) + "</b></div><div>RSS ÷ 1000 (book's contour units)<b>" + G.fmt(R / 1000, 3) + "</b></div><div>smallest possible RSS<b>" + G.fmt(minR, 1) + "</b></div><div>extra RSS you are paying<b>" + G.fmt(R - minR, 1) + "</b></div>";
  }
  draw();
});

/* ---------- isl3-1-sampling: population line vs many least-squares lines (Figure 3.3) ---------- */
G.widget("isl3-1-sampling", function (body) {
  var st = { n: 100, sd: 3, seed: 7 }, rng = G.rng(st.seed), lines = [], slopes = [], cur = null;
  var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
  G.slider(ctr, { label: "n points", min: 10, max: 400, step: 10, value: st.n, onChange: function (v) { st.n = v; reset(); } });
  G.slider(ctr, { label: "noise σ", min: 0.5, max: 8, step: 0.5, value: st.sd, onChange: function (v) { st.sd = v; reset(); } });
  G.button(ctr, "Draw a new data set", function () { one(); draw(); });
  G.button(ctr, "Draw 200 data sets", function () { for (var k = 0; k < 200; k++) one(); draw(); });
  var ro = G.el("div", "readout"); body.appendChild(ro);
  var grid = isl31Grid(body);
  var a = G.el("div"), b = G.el("div"); grid.appendChild(a); grid.appendChild(b);
  var pl = G.plot(a, { w: 460, h: 340, x: [-2, 2], y: [-12, 14], xlabel: "X", ylabel: "Y", label: "data, true line and least-squares lines" });
  var ph = G.plot(b, { w: 460, h: 340, x: [1.5, 4.5], y: [0, 1], yticks: [], xlabel: "slope estimate β̂₁ from each data set", pad: { l: 20, r: 14, t: 14, b: 44 }, label: "histogram of slope estimates" });
  function one() {
    var x = [], y = [];
    for (var i = 0; i < st.n; i++) { var xi = -2 + 4 * rng(); x.push(xi); y.push(2 + 3 * xi + st.sd * G.randn(rng)); }
    var S = isl31Sums(x, y); cur = { x: x, y: y, S: S }; lines.push([S.b0, S.b1]); slopes.push(S.b1);
  }
  function reset() { rng = G.rng(st.seed); lines = []; slopes = []; for (var k = 0; k < 10; k++) one(); draw(); }
  function draw() {
    pl.clear(); ph.clear();
    for (var i = 0; i < cur.x.length; i++) pl.dot(cur.x[i], cur.y[i], { r: 2.8, fill: "none", stroke: "var(--ink2)" });
    lines.slice(-12, -1).forEach(function (l) { pl.line([[-2, l[0] - 2 * l[1]], [2, l[0] + 2 * l[1]]], { stroke: "var(--tool)", "stroke-width": 1.2, opacity: 0.5 }); });
    pl.line([[-2, -4], [2, 8]], { stroke: "var(--bad)", "stroke-width": 2.4 });
    var c = lines[lines.length - 1]; pl.line([[-2, c[0] - 2 * c[1]], [2, c[0] + 2 * c[1]]], { stroke: "var(--accent)", "stroke-width": 2.4 });
    var nb = 30, lo = 1.5, hi = 4.5, w = (hi - lo) / nb, cnt = new Array(nb).fill(0);
    slopes.forEach(function (s) { var k = Math.floor((s - lo) / w); if (k >= 0 && k < nb) cnt[k]++; });
    var mx = Math.max.apply(null, cnt) || 1;
    cnt.forEach(function (c, k) { if (!c) return; G.svg("rect", { x: ph.X(lo + k * w) + 1, y: ph.Y(0.92 * c / mx), width: Math.max(1, ph.X(lo + w) - ph.X(lo) - 2), height: ph.Y(0) - ph.Y(0.92 * c / mx), fill: "var(--tool)", opacity: 0.75 }, ph.layer); });
    ph.line([[3, 0], [3, 1]], { stroke: "var(--bad)", "stroke-width": 2, "stroke-dasharray": "5 4" });
    ph.text(3.04, 0.95, "true β₁ = 3", { fill: "var(--bad)" });
    var m = slopes.reduce(function (p, q) { return p + q; }, 0) / slopes.length;
    var sd = Math.sqrt(slopes.reduce(function (p, q) { return p + (q - m) * (q - m); }, 0) / Math.max(1, slopes.length - 1));
    var se = st.sd / Math.sqrt(cur.S.cxx);
    ro.innerHTML = "<div>data sets drawn<b>" + slopes.length + "</b></div><div>latest β̂₀, β̂₁<b>" + G.fmt(c[0], 2) + ", " + G.fmt(c[1], 3) + "</b></div><div>average of all β̂₁<b>" + G.fmt(m, 3) + "</b></div><div>spread (sd) of the β̂₁ values<b>" + G.fmt(sd, 3) + "</b></div><div>formula SE(β̂₁) = σ/√Σ(xᵢ−x̄)²<b>" + G.fmt(se, 3) + "</b></div>";
  }
  reset();
});

/* ---------- isl3-1-tdist: t-statistic, t-distribution and the p-value ---------- */
function isl31lgamma(z) { var g = 7, c = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]; if (z < 0.5) return Math.log(Math.PI / Math.sin(Math.PI * z)) - isl31lgamma(1 - z); z -= 1; var x = c[0]; for (var i = 1; i < g + 2; i++) x += c[i] / (z + i); var t = z + g + 0.5; return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x); }
function isl31betacf(a, b, x) { var qab = a + b, qap = a + 1, qam = a - 1, c = 1, d = 1 - qab * x / qap; if (Math.abs(d) < 1e-300) d = 1e-300; d = 1 / d; var h = d; for (var m = 1; m <= 300; m++) { var m2 = 2 * m, aa = m * (b - m) * x / ((qam + m2) * (a + m2)); d = 1 + aa * d; if (Math.abs(d) < 1e-300) d = 1e-300; c = 1 + aa / c; if (Math.abs(c) < 1e-300) c = 1e-300; d = 1 / d; h *= d * c; aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2)); d = 1 + aa * d; if (Math.abs(d) < 1e-300) d = 1e-300; c = 1 + aa / c; if (Math.abs(c) < 1e-300) c = 1e-300; d = 1 / d; var del = d * c; h *= del; if (Math.abs(del - 1) < 1e-14) break; } return h; }
function isl31ibeta(a, b, x) { if (x <= 0) return 0; if (x >= 1) return 1; var bt = Math.exp(isl31lgamma(a + b) - isl31lgamma(a) - isl31lgamma(b) + a * Math.log(x) + b * Math.log(1 - x)); return x < (a + 1) / (a + b + 2) ? bt * isl31betacf(a, b, x) / a : 1 - bt * isl31betacf(b, a, 1 - x) / b; }
function isl31pval(t, df) { return isl31ibeta(df / 2, 0.5, df / (df + t * t)); }
G.widget("isl3-1-tdist", function (body, args) {
  var st = { t: args.t || 2.12, df: args.df || 3 };
  var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
  G.slider(ctr, { label: "your t-statistic", min: 0, max: 6, step: 0.01, value: st.t, fmt: function (v) { return (+v).toFixed(2); }, onChange: function (v) { st.t = v; draw(); } });
  G.seg(ctr, [[3, "df = 3 (n = 5)"], [10, "df = 10"], [30, "df = 30"], [198, "df = 198 (n = 200)"]], st.df, function (v) { st.df = v; draw(); });
  var ro = G.el("div", "readout"); body.appendChild(ro);
  var pl = G.plot(body, { w: 680, h: 300, x: [-6, 6], y: [0, 0.42], xlabel: "value of t if H₀ were true (β₁ = 0)", ylabel: "density", label: "t distribution with shaded p-value" });
  function pdf(t, df) { return Math.exp(isl31lgamma((df + 1) / 2) - isl31lgamma(df / 2) - 0.5 * Math.log(df * Math.PI) - (df + 1) / 2 * Math.log(1 + t * t / df)); }
  function crit(df) { var lo = 0, hi = 20; for (var k = 0; k < 80; k++) { var m = (lo + hi) / 2; if (isl31pval(m, df) > 0.05) lo = m; else hi = m; } return (lo + hi) / 2; }
  function draw() {
    pl.clear(); var df = st.df, t = Math.abs(st.t), pts = [], k, v;
    [-1, 1].forEach(function (sgn) {
      var a = sgn > 0 ? t : -6, b = sgn > 0 ? 6 : -t; if (b <= a) return; var poly = [[a, 0]];
      for (k = 0; k <= 60; k++) { v = a + (b - a) * k / 60; poly.push([v, pdf(v, df)]); } poly.push([b, 0]);
      var d = poly.map(function (p, i) { return (i ? "L" : "M") + pl.X(p[0]).toFixed(1) + " " + pl.Y(p[1]).toFixed(1); }).join("") + "Z";
      G.svg("path", { d: d, fill: "var(--bad)", opacity: 0.35 }, pl.layer);
    });
    for (k = 0; k <= 240; k++) { v = -6 + 12 * k / 240; pts.push([v, Math.exp(-v * v / 2) / Math.sqrt(2 * Math.PI)]); }
    pl.line(pts, { stroke: "var(--muted)", "stroke-width": 1.4, "stroke-dasharray": "5 4" });
    pts = []; for (k = 0; k <= 240; k++) { v = -6 + 12 * k / 240; pts.push([v, pdf(v, df)]); }
    pl.line(pts, { stroke: "var(--accent)", "stroke-width": 2.4 });
    var c = crit(df);
    [-c, c].forEach(function (z) { pl.line([[z, 0], [z, 0.4]], { stroke: "var(--warn)", "stroke-width": 1.4, "stroke-dasharray": "3 3" }); });
    pl.text(c + 0.1, 0.38, "±" + c.toFixed(3) + " (5% cut-off)", { fill: "var(--warn)" });
    pl.line([[t, 0], [t, pdf(t, df) + 0.03]], { stroke: "var(--bad)", "stroke-width": 2 });
    var p = isl31pval(t, df);
    ro.innerHTML = "<div>t<b>" + t.toFixed(2) + "</b></div><div>degrees of freedom n − 2<b>" + df + "</b></div><div>p-value = red area (both tails)<b>" + (p < 1e-4 ? p.toExponential(2) : p.toFixed(4)) + "</b></div><div>decision at 5%<b>" + (p < 0.05 ? "reject H₀" : "cannot reject H₀") + "</b></div>";
  }
  draw();
});
