/* m-calc · secant to tangent, squared vs absolute loss, gradient descent on contours, backprop graph */
(function () {
  function toData(pl, e, xr, yr) {
    var r = pl.svg.getBoundingClientRect();
    var px = (e.clientX - r.left) / r.width * pl.W, py = (e.clientY - r.top) / r.height * pl.H;
    return [xr[0] + (px - pl.P.l) / (pl.W - pl.P.l - pl.P.r) * (xr[1] - xr[0]), yr[0] + (pl.H - pl.P.b - py) / (pl.H - pl.P.t - pl.P.b) * (yr[1] - yr[0])];
  }
  var clipN = 0;
  function clip(pl) {
    var id = "mcclip" + (++clipN), defs = G.svg("defs", {}, pl.svg), cp = G.svg("clipPath", { id: id }, defs);
    G.svg("rect", { x: pl.P.l, y: pl.P.t, width: pl.W - pl.P.l - pl.P.r, height: pl.H - pl.P.t - pl.P.b }, cp);
    pl.layer.setAttribute("clip-path", "url(#" + id + ")");
  }
  function arrow(pl, x0, y0, x1, y1, col, w) {
    var X0 = pl.X(x0), Y0 = pl.Y(y0), X1 = pl.X(x1), Y1 = pl.Y(y1), L = Math.hypot(X1 - X0, Y1 - Y0);
    if (L < 2) return;
    var ux = (X1 - X0) / L, uy = (Y1 - Y0) / L, h = Math.min(12, L * 0.45);
    G.svg("line", { x1: X0, y1: Y0, x2: X1 - ux * h * 0.8, y2: Y1 - uy * h * 0.8, stroke: col, "stroke-width": w || 3, "stroke-linecap": "round" }, pl.layer);
    var p = [[X1, Y1], [X1 - ux * h - uy * h * 0.5, Y1 - uy * h + ux * h * 0.5], [X1 - ux * h + uy * h * 0.5, Y1 - uy * h - ux * h * 0.5]];
    G.svg("polygon", { points: p.map(function (q) { return q[0].toFixed(1) + "," + q[1].toFixed(1); }).join(" "), fill: col }, pl.layer);
  }

  /* ---------- 1. secant to tangent ---------- */
  G.widget("m-calc-secant", function (body) {
    var F = {
      sq: { name: "x²", f: function (x) { return x * x; }, d: function (x) { return 2 * x; }, xr: [-1, 4], yr: [-1, 16], a: 3 },
      cub: { name: "x³ − 3x", f: function (x) { return x * x * x - 3 * x; }, d: function (x) { return 3 * x * x - 3; }, xr: [-2.5, 2.5], yr: [-6, 6], a: 0.5 },
      exp: { name: "eˣ", f: Math.exp, d: Math.exp, xr: [-2, 2.5], yr: [-1, 12], a: 1 },
      sin: { name: "sin x", f: Math.sin, d: Math.cos, xr: [-3.2, 3.2], yr: [-1.6, 1.6], a: 0.5 }
    };
    var cur = "sq", a = F.sq.a, h = 1, pl;
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    G.seg(ctr, [["sq", "x²"], ["cub", "x³ − 3x"], ["exp", "eˣ"], ["sin", "sin x"]], cur, function (v) { cur = v; a = F[v].a; sa.input.min = F[v].xr[0] + 0.3; sa.input.max = F[v].xr[1] - 0.3; sa.set(a); build(); draw(); });
    var sa = G.slider(ctr, { label: "point a", min: -0.7, max: 3.7, step: 0.05, value: a, fmt: function (v) { return G.fmt(v, 2); }, onChange: function (v) { a = v; draw(); } });
    var sh = G.slider(ctr, { label: "step h", min: 0, max: 100, step: 1, value: 66, fmt: function (v) { return G.fmt(hOf(v), 3); }, onChange: function (v) { h = hOf(v); draw(); } });
    function hOf(v) { return Math.pow(10, -2 + 2.3 * v / 100); }
    h = hOf(66);
    var info = G.el("div", "readout"); body.appendChild(info);
    var host = G.el("div", ""); body.appendChild(host);
    function build() { host.innerHTML = ""; var o = F[cur]; pl = G.plot(host, { w: 680, h: 330, x: o.xr, y: o.yr, xlabel: "x", ylabel: "f(x)", label: "curve with a secant and tangent line" }); clip(pl); }
    function draw() {
      var o = F[cur]; pl.clear();
      var pts = []; for (var k = 0; k <= 200; k++) { var x = o.xr[0] + (o.xr[1] - o.xr[0]) * k / 200; pts.push([x, o.f(x)]); }
      pl.line(pts, { stroke: "var(--ink2)", "stroke-width": 2.4 });
      var fa = o.f(a), fb = o.f(a + h), s = (fb - fa) / h, t = o.d(a);
      pl.line([[o.xr[0], fa + t * (o.xr[0] - a)], [o.xr[1], fa + t * (o.xr[1] - a)]], { stroke: "var(--udl)", "stroke-width": 2, "stroke-dasharray": "7 5" });
      pl.line([[o.xr[0], fa + s * (o.xr[0] - a)], [o.xr[1], fa + s * (o.xr[1] - a)]], { stroke: "var(--math)", "stroke-width": 2.6 });
      pl.line([[a, fa], [a + h, fa], [a + h, fb]], { stroke: "var(--muted)", "stroke-width": 1.2, "stroke-dasharray": "3 3" });
      pl.dot(a, fa, { r: 6, fill: "var(--ink)" }); pl.dot(a + h, fb, { r: 6, fill: "var(--math)" });
      info.innerHTML = "<div>f(a)<b>" + G.fmt(fa, 4) + "</b></div><div>f(a + h)<b>" + G.fmt(fb, 4) + "</b></div><div>secant slope (orange) = rise ÷ run<b>" + G.fmt(s, 4) + "</b></div><div>true derivative f′(a) (dashed)<b>" + G.fmt(t, 4) + "</b></div><div>difference<b>" + G.fmt(s - t, 4) + "</b></div>";
    }
    build(); draw();
  });

  /* ---------- 2. squared versus absolute loss ---------- */
  G.widget("m-calc-meanmed", function (body, args) {
    var xs = (args.x || [1, 2, 6]).slice(), XR = [0, 12], drag = -1;
    var info = G.el("div", "readout"); body.appendChild(info);
    var strip = G.plot(body, { w: 680, h: 96, x: XR, y: [0, 1], yticks: [], xlabel: "the data (drag the dots)", pad: { l: 54, r: 16, t: 8, b: 40 }, label: "data points on a line" });
    var p1 = G.plot(body, { w: 680, h: 200, x: XR, y: [0, 120], ylabel: "Σ(xᵢ − c)²", pad: { l: 54, r: 16, t: 10, b: 26 }, label: "squared loss as a function of c" });
    var p2 = G.plot(body, { w: 680, h: 200, x: XR, y: [0, 24], ylabel: "Σ|xᵢ − c|", xlabel: "summary value c", pad: { l: 54, r: 16, t: 10, b: 40 }, label: "absolute loss as a function of c" });
    clip(p1); clip(p2);
    function draw() {
      var n = xs.length, mean = xs.reduce(function (s, v) { return s + v; }, 0) / n, srt = xs.slice().sort(function (u, v) { return u - v; }), med = srt[(n - 1) / 2];
      var sq = function (c) { return xs.reduce(function (s, v) { return s + (v - c) * (v - c); }, 0); }, ab = function (c) { return xs.reduce(function (s, v) { return s + Math.abs(v - c); }, 0); };
      [strip, p1, p2].forEach(function (p) { p.clear(); });
      var a1 = [], a2 = []; for (var k = 0; k <= 240; k++) { var c = XR[0] + (XR[1] - XR[0]) * k / 240; a1.push([c, sq(c)]); a2.push([c, ab(c)]); }
      p1.line(a1, { stroke: "var(--tool)", "stroke-width": 2.6 }); p2.line(a2, { stroke: "var(--good)", "stroke-width": 2.6 });
      p1.line([[mean, 0], [mean, 120]], { stroke: "var(--tool)", "stroke-dasharray": "5 4", "stroke-width": 1.5 }); p1.dot(mean, sq(mean), { r: 6, fill: "var(--tool)" });
      p1.text(Math.min(mean + 0.15, 9.2), 105, "minimum at the mean, c = " + G.fmt(mean, 2), { fill: "var(--tool)", "font-weight": 700, "font-size": 13 });
      p2.line([[med, 0], [med, 24]], { stroke: "var(--good)", "stroke-dasharray": "5 4", "stroke-width": 1.5 }); p2.dot(med, ab(med), { r: 6, fill: "var(--good)" });
      p2.text(Math.min(med + 0.15, 9), 21, "minimum at the median, c = " + G.fmt(med, 2), { fill: "var(--good)", "font-weight": 700, "font-size": 13 });
      strip.line([[mean, 0.05], [mean, 0.95]], { stroke: "var(--tool)", "stroke-dasharray": "5 4", "stroke-width": 2 });
      strip.line([[med, 0.05], [med, 0.95]], { stroke: "var(--good)", "stroke-dasharray": "2 3", "stroke-width": 2 });
      xs.forEach(function (v, i) {
        var d = strip.dot(v, 0.5, { r: 10, fill: "var(--math)", stroke: "var(--surface)", "stroke-width": 3, style: "cursor:grab" });
        d.addEventListener("pointerdown", function (e) { drag = i; strip.svg.setPointerCapture(e.pointerId); e.preventDefault(); });
      });
      info.innerHTML = "<div>data<b>" + xs.map(function (v) { return G.fmt(v, 1); }).join(", ") + "</b></div><div>mean<b style='color:var(--tool)'>" + G.fmt(mean, 3) + "</b></div><div>median<b style='color:var(--good)'>" + G.fmt(med, 3) + "</b></div><div>Σ(xᵢ − mean)²<b>" + G.fmt(sq(mean), 3) + "</b></div><div>Σ|xᵢ − median|<b>" + G.fmt(ab(med), 3) + "</b></div>";
    }
    strip.svg.addEventListener("pointermove", function (e) { if (drag < 0) return; var q = toData(strip, e, XR, [0, 1]); xs[drag] = Math.max(0, Math.min(12, Math.round(q[0] * 10) / 10)); draw(); });
    strip.svg.addEventListener("pointerup", function () { drag = -1; });
    draw();
  });

  /* ---------- 3. gradient and gradient descent on the least-squares bowl ---------- */
  G.widget("m-calc-gd", function (body) {
    // L(b0,b1) = sum (y - b0 - b1 x)^2 for (1,2),(2,3),(3,5) = Lmin + d^T A d,  A = X^T X
    var A = [[3, 6], [6, 14]], bs = [1 / 3, 1.5], Lmin = 1 / 6;
    var XR = [-3, 4], YR = [-0.5, 3.5];
    function L(b) { var d0 = b[0] - bs[0], d1 = b[1] - bs[1]; return Lmin + A[0][0] * d0 * d0 + 2 * A[0][1] * d0 * d1 + A[1][1] * d1 * d1; }
    function grad(b) { var d0 = b[0] - bs[0], d1 = b[1] - bs[1]; return [2 * (A[0][0] * d0 + A[0][1] * d1), 2 * (A[0][1] * d0 + A[1][1] * d1)]; }
    var tr = 17, dt = 3 * 14 - 36, l1 = tr / 2 + Math.sqrt(tr * tr / 4 - dt), l2 = tr / 2 - Math.sqrt(tr * tr / 4 - dt);
    var v1 = [A[0][1], l1 - A[0][0]], n1 = Math.hypot(v1[0], v1[1]); v1 = [v1[0] / n1, v1[1] / n1]; var v2 = [-v1[1], v1[0]];
    var start = [2.5, 0.2], b = start.slice(), path = [b.slice()], alpha = 0.02, drag = false;
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    G.slider(ctr, { label: "learning rate α", min: 0.002, max: 0.07, step: 0.002, value: alpha, fmt: function (v) { return G.fmt(v, 3); }, onChange: function (v) { alpha = v; } });
    function step() { var g = grad(b); b = [b[0] - alpha * g[0], b[1] - alpha * g[1]]; if (Math.abs(b[0]) + Math.abs(b[1]) > 1e6) b = [NaN, NaN]; path.push(b.slice()); }
    G.button(ctr, "Step", function () { step(); draw(); });
    G.button(ctr, "Run 50", function () { for (var k = 0; k < 50; k++) step(); draw(); });
    G.button(ctr, "Reset", function () { b = start.slice(); path = [b.slice()]; draw(); });
    var info = G.el("div", "readout"); body.appendChild(info);
    var W = 680, PW = W - 54 - 16, PH = PW * (YR[1] - YR[0]) / (XR[1] - XR[0]);
    var pl = G.plot(body, { w: W, h: Math.round(PH + 14 + 44), x: XR, y: YR, xlabel: "β₀ (intercept)", ylabel: "β₁ (slope)", label: "contours of the least-squares loss with gradient arrows" });
    clip(pl);
    function draw() {
      pl.clear();
      [0.25, 1, 2.5, 5, 10, 20, 40, 80].forEach(function (c) {
        var pts = []; for (var k = 0; k <= 120; k++) { var t = k / 120 * 2 * Math.PI, r1 = Math.sqrt(c / l1) * Math.cos(t), r2 = Math.sqrt(c / l2) * Math.sin(t); pts.push([bs[0] + r1 * v1[0] + r2 * v2[0], bs[1] + r1 * v1[1] + r2 * v2[1]]); }
        pl.line(pts, { stroke: "var(--udl)", "stroke-width": 1.1, opacity: 0.55 });
      });
      pl.dot(bs[0], bs[1], { r: 5, fill: "var(--good)" }); pl.text(bs[0] + 0.08, bs[1] - 0.17, "minimum (1/3, 1.5)", { fill: "var(--good)", "font-size": 12 });
      var good = path.filter(function (p) { return isFinite(p[0]); });
      if (good.length > 1) { pl.line(good, { stroke: "var(--math)", "stroke-width": 1.6 }); good.forEach(function (p) { pl.dot(p[0], p[1], { r: 2.6, fill: "var(--math)" }); }); }
      if (isFinite(b[0])) {
        var g = grad(b), gn = Math.hypot(g[0], g[1]) || 1, s = 0.7 / gn;
        arrow(pl, b[0], b[1], b[0] + g[0] * s, b[1] + g[1] * s, "var(--bad)", 3);
        arrow(pl, b[0], b[1], b[0] - g[0] * s, b[1] - g[1] * s, "var(--good)", 3);
        var h = pl.dot(b[0], b[1], { r: 9, fill: "var(--ink)", stroke: "var(--surface)", "stroke-width": 3, style: "cursor:grab" });
        h.addEventListener("pointerdown", function (e) { drag = true; pl.svg.setPointerCapture(e.pointerId); e.preventDefault(); });
        info.innerHTML = "<div>step<b>" + (path.length - 1) + "</b></div><div>(β₀, β₁)<b>(" + G.fmt(b[0], 3) + ", " + G.fmt(b[1], 3) + ")</b></div><div>loss L<b>" + G.fmt(L(b), 4) + "</b></div><div>gradient ∇L (red, uphill)<b>(" + G.fmt(g[0], 2) + ", " + G.fmt(g[1], 2) + ")</b></div><div>−∇L (green) = descent direction<b>‖∇L‖ = " + G.fmt(gn, 2) + "</b></div>";
      } else info.innerHTML = "<div>diverged<b style='color:var(--bad)'>the steps grew without limit: lower α and press Reset</b></div>";
    }
    pl.svg.addEventListener("pointermove", function (e) { if (!drag) return; var q = toData(pl, e, XR, YR); b = [Math.max(XR[0], Math.min(XR[1], q[0])), Math.max(YR[0], Math.min(YR[1], q[1]))]; start = b.slice(); path = [b.slice()]; draw(); });
    pl.svg.addEventListener("pointerup", function () { drag = false; });
    draw();
  });

  /* ---------- 4. forward values, backward derivatives ---------- */
  G.widget("m-calc-graph", function (body) {
    var v = { x: 2, w: 0.5, b: -0.5, y: 1 };
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    [["x", "input x", -3, 3], ["w", "weight w", -3, 3], ["b", "bias b", -3, 3], ["y", "target y", 0, 1]].forEach(function (s) {
      G.slider(ctr, { label: s[1], min: s[2], max: s[3], step: 0.05, value: v[s[0]], fmt: function (q) { return G.fmt(q, 2); }, onChange: function (q) { v[s[0]] = q; draw(); } });
    });
    var row = G.el("div", ""); row.style.cssText = "display:flex;flex-wrap:wrap;gap:8px;align-items:stretch;justify-content:center;margin-top:12px"; body.appendChild(row);
    function card(title, val, gr, local) {
      var c = G.el("div", ""); c.style.cssText = "flex:1 1 118px;max-width:170px;border:1px solid var(--line2);border-radius:12px;padding:8px 10px;background:var(--surface);text-align:center";
      c.innerHTML = "<div style='font-size:15px'>" + G.tex(title) + "</div><div style='font:700 18px var(--mono);margin:4px 0'>" + G.fmt(val, 4) + "</div><div style='font:600 13px var(--mono);color:var(--udl)'>" + G.tex("\\partial L/\\partial\\," + title.split("=")[0]) + " = " + G.fmt(gr, 4) + "</div>" + (local ? "<div style='font-size:12px;color:var(--muted);margin-top:4px'>local: " + local + "</div>" : "");
      return c;
    }
    function draw() {
      var z = v.w * v.x + v.b, a = 1 / (1 + Math.exp(-z)), d = a - v.y, L = d * d;
      var gL = 1, gd = 2 * d, ga = gd, gz = ga * a * (1 - a), gw = gz * v.x, gb = gz;
      row.innerHTML = "";
      var inputs = G.el("div", ""); inputs.style.cssText = "display:flex;flex-direction:column;gap:6px;flex:1 1 118px;max-width:170px";
      [["w", v.w, gw, "∂z/∂w = x = " + G.fmt(v.x, 2)], ["b", v.b, gb, "∂z/∂b = 1"]].forEach(function (q) {
        var c = G.el("div", ""); c.style.cssText = "border:1px solid var(--line2);border-radius:12px;padding:6px 10px;background:var(--panel);text-align:center";
        c.innerHTML = "<div>" + G.tex(q[0]) + " = <b style='font-family:var(--mono)'>" + G.fmt(q[1], 2) + "</b></div><div style='font:600 13px var(--mono);color:var(--udl)'>" + G.tex("\\partial L/\\partial " + q[0]) + " = " + G.fmt(q[2], 4) + "</div><div style='font-size:12px;color:var(--muted)'>" + q[3] + "</div>";
        inputs.appendChild(c);
      });
      row.appendChild(inputs);
      var arr = function () { var s = G.el("div", "", "→"); s.style.cssText = "align-self:center;font-size:22px;color:var(--muted)"; return s; };
      row.appendChild(arr()); row.appendChild(card("z=wx+b", z, gz, "∂a/∂z = a(1−a) = " + G.fmt(a * (1 - a), 4)));
      row.appendChild(arr()); row.appendChild(card("a=\\sigma(z)", a, ga, "∂d/∂a = 1"));
      row.appendChild(arr()); row.appendChild(card("d=a-y", d, gd, "∂L/∂d = 2d"));
      row.appendChild(arr()); row.appendChild(card("L=d^2", L, gL, ""));
    }
    draw();
  });
})();
