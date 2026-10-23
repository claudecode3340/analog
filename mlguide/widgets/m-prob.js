/* m-prob · normal area, Bayes with 1,000 people, coin likelihood, central limit theorem */
(function () {
  function erf(x) { var s = x < 0 ? -1 : 1; x = Math.abs(x); var t = 1 / (1 + 0.3275911 * x); var y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x); return s * y; }
  function Phi(z) { return 0.5 * (1 + erf(z / Math.SQRT2)); }
  function npdf(x, m, s) { return Math.exp(-(x - m) * (x - m) / (2 * s * s)) / Math.sqrt(2 * Math.PI * s * s); }
  var clipN = 0;
  function clip(pl) {
    var id = "mpclip" + (++clipN), defs = G.svg("defs", {}, pl.svg), cp = G.svg("clipPath", { id: id }, defs);
    G.svg("rect", { x: pl.P.l, y: pl.P.t - 2, width: pl.W - pl.P.l - pl.P.r, height: pl.H - pl.P.t - pl.P.b + 2 }, cp);
    pl.layer.setAttribute("clip-path", "url(#" + id + ")");
  }
  function area(pl, pts, y0, attrs) {
    var d = "M" + pl.X(pts[0][0]) + " " + pl.Y(y0) + pts.map(function (p) { return "L" + pl.X(p[0]).toFixed(1) + " " + pl.Y(p[1]).toFixed(1); }).join("") + "L" + pl.X(pts[pts.length - 1][0]) + " " + pl.Y(y0) + "Z";
    return G.svg("path", Object.assign({ d: d }, attrs), pl.layer);
  }

  /* ---------- 1. normal curve with shaded probability ---------- */
  G.widget("m-prob-normal", function (body) {
    var mu = 0, sg = 1, a = -1, b = 1;
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    var f2 = function (v) { return G.fmt(v, 2); };
    G.slider(ctr, { label: "mean μ", min: -3, max: 3, step: 0.05, value: mu, fmt: f2, onChange: function (v) { mu = v; draw(); } });
    G.slider(ctr, { label: "sd σ", min: 0.3, max: 3, step: 0.05, value: sg, fmt: f2, onChange: function (v) { sg = v; draw(); } });
    var sa = G.slider(ctr, { label: "from a", min: -6, max: 6, step: 0.01, value: a, fmt: f2, onChange: function (v) { a = v; if (a > b) { b = a; sb.set(b); } draw(); } });
    var sb = G.slider(ctr, { label: "to b", min: -6, max: 6, step: 0.01, value: b, fmt: f2, onChange: function (v) { b = v; if (b < a) { a = b; sa.set(a); } draw(); } });
    var info = G.el("div", "readout"); body.appendChild(info);
    var host = G.el("div", ""); body.appendChild(host);
    function draw() {
      host.innerHTML = "";
      var peak = npdf(mu, mu, sg), ymax = Math.max(0.45, peak * 1.12);
      var pl = G.plot(host, { w: 680, h: 300, x: [-6, 6], y: [0, ymax], xlabel: "x", ylabel: "density p(x)", label: "normal density with a shaded interval" });
      var pts = [], sh = [];
      for (var k = 0; k <= 300; k++) { var x = -6 + 12 * k / 300; pts.push([x, npdf(x, mu, sg)]); if (x >= a && x <= b) sh.push([x, npdf(x, mu, sg)]); }
      if (b > a) { sh.unshift([a, npdf(a, mu, sg)]); sh.push([b, npdf(b, mu, sg)]); area(pl, sh, 0, { fill: "var(--isl)", opacity: 0.3 }); }
      pl.line(pts, { stroke: "var(--isl)", "stroke-width": 2.6 });
      pl.line([[mu, 0], [mu, peak]], { stroke: "var(--muted)", "stroke-dasharray": "4 4", "stroke-width": 1.2 });
      [[mu - sg, "μ−σ"], [mu + sg, "μ+σ"]].forEach(function (q) { if (q[0] > -6 && q[0] < 6) { pl.line([[q[0], 0], [q[0], npdf(q[0], mu, sg)]], { stroke: "var(--muted)", "stroke-dasharray": "2 4" }); } });
      var P = Phi((b - mu) / sg) - Phi((a - mu) / sg);
      info.innerHTML = "<div>shaded area = P(a ≤ X ≤ b)<b>" + G.fmt(P, 4) + "</b></div><div>z-values (x − μ)/σ<b>" + G.fmt((a - mu) / sg, 2) + " to " + G.fmt((b - mu) / sg, 2) + "</b></div><div>peak height 1/√(2πσ²)<b>" + G.fmt(peak, 3) + "</b></div>";
    }
    draw();
  });

  /* ---------- 2. Bayes' rule with 1,000 people ---------- */
  G.widget("m-prob-bayes", function (body) {
    var prev = 0.01, sens = 0.9, spec = 0.91;
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    var pc = function (v) { return G.fmt(100 * v, 1) + "%"; };
    G.slider(ctr, { label: "prevalence", min: 0.001, max: 0.5, step: 0.001, value: prev, fmt: pc, onChange: function (v) { prev = v; draw(); } });
    G.slider(ctr, { label: "sensitivity", min: 0.5, max: 1, step: 0.005, value: sens, fmt: pc, onChange: function (v) { sens = v; draw(); } });
    G.slider(ctr, { label: "specificity", min: 0.5, max: 0.999, step: 0.001, value: spec, fmt: pc, onChange: function (v) { spec = v; draw(); } });
    var info = G.el("div", "readout"); body.appendChild(info);
    var host = G.el("div", ""); host.style.cssText = "max-width:640px;margin:10px auto 0"; body.appendChild(host);
    var svg = G.svg("svg", { viewBox: "0 0 640 400", class: "wsvg", role: "img", "aria-label": "1000 people coloured by disease and test result" }, host);
    var leg = G.el("div", ""); leg.style.cssText = "display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:center;font-size:13.5px;color:var(--muted);margin-top:8px"; body.appendChild(leg);
    function sw(st) { return "<span style='display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-1px;margin-right:5px;" + st + "'></span>"; }
    leg.innerHTML = [["background:var(--bad)", "sick, test positive"], ["border:2px solid var(--bad)", "sick, missed by the test"], ["background:var(--warn)", "healthy, false alarm"], ["background:var(--line)", "healthy, test negative"]].map(function (q) { return "<span style='white-space:nowrap'>" + sw(q[0]) + q[1] + "</span>"; }).join("");
    function draw() {
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      var sick = Math.round(1000 * prev), tp = Math.round(sick * sens), fn = sick - tp, fp = Math.round((1000 - sick) * (1 - spec));
      for (var i = 0; i < 1000; i++) {
        var c = i % 40, r = Math.floor(i / 40), x = c * 16 + 2, y = r * 16 + 2, at = { x: x, y: y, width: 12, height: 12, rx: 3 };
        if (i < tp) at.fill = "var(--bad)";
        else if (i < tp + fn) { at.fill = "none"; at.stroke = "var(--bad)"; at["stroke-width"] = 2; at.x += 1; at.y += 1; at.width = 10; at.height = 10; }
        else if (i < tp + fn + fp) at.fill = "var(--warn)";
        else at.fill = "var(--line)";
        G.svg("rect", at, svg);
      }
      var post = sens * prev / (sens * prev + (1 - spec) * (1 - prev));
      info.innerHTML = "<div>sick (of 1,000)<b>" + sick + "</b></div><div>true positives<b style='color:var(--bad)'>" + tp + "</b></div><div>false positives<b style='color:var(--warn)'>" + fp + "</b></div><div>P(sick | positive) from counts<b>" + tp + " / " + (tp + fp) + " = " + G.fmt(tp + fp ? tp / (tp + fp) : 0, 3) + "</b></div><div>exact, Bayes' rule<b>" + G.fmt(post, 4) + "</b></div>";
    }
    draw();
  });

  /* ---------- 3. likelihood of a coin's bias ---------- */
  G.widget("m-prob-lik", function (body, args) {
    var n = args.n || 10, k = args.k || 7, p = 0.5;
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    var sk;
    G.slider(ctr, { label: "flips n", min: 1, max: 200, step: 1, value: n, onChange: function (v) { var r = k / n; n = v; k = Math.round(r * n); sk.input.max = n; sk.set(k); draw(); } });
    sk = G.slider(ctr, { label: "heads k", min: 0, max: n, step: 1, value: k, onChange: function (v) { k = v; draw(); } });
    G.slider(ctr, { label: "try p", min: 0.01, max: 0.99, step: 0.01, value: p, fmt: function (v) { return G.fmt(v, 2); }, onChange: function (v) { p = v; draw(); } });
    var info = G.el("div", "readout"); body.appendChild(info);
    var host = G.el("div", ""); body.appendChild(host);
    function ll(q) { return (k ? k * Math.log(q) : 0) + (n - k ? (n - k) * Math.log(1 - q) : 0); }
    function draw() {
      host.innerHTML = "";
      var ph = Math.min(0.99, Math.max(0.01, k / n)), lmax = ll(ph);
      var p1 = G.plot(host, { w: 680, h: 190, x: [0, 1], y: [0, 1.1], ylabel: "L(p) ÷ L(p̂)", pad: { l: 54, r: 16, t: 10, b: 26 }, label: "likelihood scaled to peak 1" });
      var p2 = G.plot(host, { w: 680, h: 220, x: [0, 1], y: [lmax - 25, lmax + 3], ylabel: "log L(p)", xlabel: "p (probability of heads)", pad: { l: 54, r: 16, t: 10, b: 40 }, label: "log-likelihood with tangent" });
      clip(p1); clip(p2);
      var a1 = [], a2 = [];
      for (var i = 1; i < 400; i++) { var q = i / 400; a1.push([q, Math.exp(ll(q) - lmax)]); a2.push([q, ll(q)]); }
      area(p1, a1, 0, { fill: "var(--udl)", opacity: 0.15 }); p1.line(a1, { stroke: "var(--udl)", "stroke-width": 2.4 }); p2.line(a2, { stroke: "var(--udl)", "stroke-width": 2.4 });
      [p1, p2].forEach(function (pl, j) { pl.line([[ph, j ? lmax - 25 : 0], [ph, j ? lmax + 3 : 1.1]], { stroke: "var(--good)", "stroke-dasharray": "5 4", "stroke-width": 1.5 }); });
      var slope = (k ? k / p : 0) - (n - k ? (n - k) / (1 - p) : 0), y0 = ll(p);
      p2.line([[p - 0.15, y0 - 0.15 * slope], [p + 0.15, y0 + 0.15 * slope]], { stroke: "var(--math)", "stroke-width": 2.4 });
      p1.dot(p, Math.exp(y0 - lmax), { r: 6, fill: "var(--math)" }); p2.dot(p, y0, { r: 6, fill: "var(--math)" });
      info.innerHTML = "<div>MLE p̂ = k/n (green)<b>" + G.fmt(k / n, 3) + "</b></div><div>L(p) = pᵏ(1−p)ⁿ⁻ᵏ at your p<b>" + Math.exp(y0).toExponential(3) + "</b></div><div>log L(p)<b>" + G.fmt(y0, 3) + "</b></div><div>slope k/p − (n−k)/(1−p)<b>" + G.fmt(slope, 2) + "</b></div>";
    }
    draw();
  });

  /* ---------- 4. central limit theorem ---------- */
  G.widget("m-prob-clt", function (body, args) {
    var D = {
      unif: { name: "uniform(0,1)", mu: 0.5, sd: Math.sqrt(1 / 12), draw: function (r) { return r(); }, lo: 0, hi: 1, disc: false, pdf: function (x) { return x >= 0 && x <= 1 ? 1 : 0; } },
      expo: { name: "exponential", mu: 1, sd: 1, draw: function (r) { return -Math.log(1 - r()); }, lo: 0, hi: 6, disc: false, pdf: function (x) { return x >= 0 ? Math.exp(-x) : 0; } },
      die: { name: "die", mu: 3.5, sd: Math.sqrt(35 / 12), draw: function (r) { return 1 + Math.floor(6 * r()); }, lo: 1, hi: 6, disc: true, vals: [[1, 1 / 6], [2, 1 / 6], [3, 1 / 6], [4, 1 / 6], [5, 1 / 6], [6, 1 / 6]] },
      coin: { name: "coin, P(1) = 0.1", mu: 0.1, sd: 0.3, draw: function (r) { return r() < 0.1 ? 1 : 0; }, lo: 0, hi: 1, disc: true, vals: [[0, 0.9], [1, 0.1]] }
    };
    var cur = "expo", n = 1, N = 3000;
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    G.seg(ctr, [["unif", "uniform"], ["expo", "exponential"], ["die", "die"], ["coin", "skewed coin"]], cur, function (v) { cur = v; draw(); });
    G.slider(ctr, { label: "sample size n", min: 1, max: 50, step: 1, value: n, onChange: function (v) { n = v; draw(); } });
    var info = G.el("div", "readout"); body.appendChild(info);
    var host = G.el("div", ""); body.appendChild(host);
    function draw() {
      host.innerHTML = "";
      var d = D[cur], rng = G.rng((args.seed || 7) * 1000 + n), means = [];
      for (var s = 0; s < N; s++) { var t = 0; for (var j = 0; j < n; j++) t += d.draw(rng); means.push(t / n); }
      var se = d.sd / Math.sqrt(n), lo = Math.max(d.lo, d.mu - 4.2 * se), hi = Math.min(d.hi, d.mu + 4.2 * se);
      if (cur === "expo" && n === 1) { lo = 0; hi = 6; }
      var bins = [], w;
      if (d.disc) { w = 1 / n; var c0 = Math.ceil((lo - 1e-9) * n) / n; for (var c = c0; c <= hi + 1e-9; c += w) bins.push([c - w / 2, c + w / 2, 0]); }
      else { var B = 40; w = (hi - lo) / B; for (var q = 0; q < B; q++) bins.push([lo + q * w, lo + (q + 1) * w, 0]); }
      means.forEach(function (m) { for (var q = 0; q < bins.length; q++) if (m >= bins[q][0] - 1e-9 && m < bins[q][1] - 1e-9) { bins[q][2]++; break; } });
      var dens = bins.map(function (bn) { return bn[2] / (N * w); }), ymax = Math.max(Math.max.apply(null, dens), npdf(d.mu, d.mu, se)) * 1.12;
      var xl = d.disc ? lo - w / 2 : lo, xh = d.disc ? hi + w / 2 : hi;
      var pl = G.plot(host, { w: 680, h: 300, x: [xl, xh], y: [0, ymax], xlabel: "sample mean of n draws", ylabel: "density", label: "histogram of sample means with normal curve" });
      clip(pl);
      bins.forEach(function (bn, q) { if (!dens[q]) return; G.svg("rect", { x: pl.X(bn[0]) + 0.5, y: pl.Y(dens[q]), width: Math.max(1, pl.X(bn[1]) - pl.X(bn[0]) - 1), height: pl.Y(0) - pl.Y(dens[q]), fill: "var(--tool)", opacity: 0.55 }, pl.layer); });
      var cv = []; for (var k = 0; k <= 200; k++) { var x = xl + (xh - xl) * k / 200; cv.push([x, npdf(x, d.mu, se)]); }
      pl.line(cv, { stroke: "var(--math)", "stroke-width": 2.6 });
      var m = means.reduce(function (a, b) { return a + b; }, 0) / N, sdv = Math.sqrt(means.reduce(function (a, b) { return a + (b - m) * (b - m); }, 0) / (N - 1));
      // inset: the starting distribution
      var ins = G.svg("g", { transform: "translate(" + (pl.W - 190) + ",18)" }, pl.layer);
      G.svg("rect", { x: 0, y: 0, width: 170, height: 70, rx: 8, fill: "var(--surface)", stroke: "var(--line2)" }, ins);
      var tx = G.svg("text", { x: 8, y: 14, class: "tick" }, ins); tx.textContent = "start: " + d.name;
      if (d.disc) { var mx = Math.max.apply(null, d.vals.map(function (v) { return v[1]; })); d.vals.forEach(function (v, i) { var bx = 12 + i * (146 / d.vals.length), bh = 40 * v[1] / mx; G.svg("rect", { x: bx, y: 62 - bh, width: 146 / d.vals.length - 4, height: bh, fill: "var(--muted)" }, ins); }); }
      else { var pp = []; for (var u = 0; u <= 60; u++) { var xx = d.lo + (d.hi - d.lo) * u / 60; pp.push((12 + 146 * u / 60).toFixed(1) + "," + (62 - 40 * d.pdf(xx)).toFixed(1)); } G.svg("polyline", { points: pp.join(" "), fill: "none", stroke: "var(--muted)", "stroke-width": 2 }, ins); }
      info.innerHTML = "<div>n<b>" + n + "</b></div><div>mean of the 3,000 sample means<b>" + G.fmt(m, 3) + "</b></div><div>CLT: μ<b>" + G.fmt(d.mu, 3) + "</b></div><div>sd of the sample means<b>" + G.fmt(sdv, 3) + "</b></div><div>CLT: σ/√n<b>" + G.fmt(se, 3) + "</b></div>";
    }
    draw();
  });
})();
