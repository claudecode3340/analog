/* s0-maths · sigma-notation expander and formula anatomy */
G.widget("s0-maths-sigma", function (body, args) {
  var x = (args.x || [2, 5, 3, 6]).slice(), n = x.length;
  var mean = x.reduce(function (a, b) { return a + b; }, 0) / n;
  var terms = {
    xi: { tex: "x_i", f: function (i) { return x[i - 1]; }, show: function (i) { return String(x[i - 1]); } },
    xi2: { tex: "x_i^2", f: function (i) { return x[i - 1] * x[i - 1]; }, show: function (i) { return x[i - 1] < 0 ? "(" + x[i - 1] + ")^2" : x[i - 1] + "^2"; } },
    ixi: { tex: "i\\,x_i", f: function (i) { return i * x[i - 1]; }, show: function (i) { return i + "\\cdot " + x[i - 1]; } },
    dev: { tex: "(x_i-\\bar x)^2", f: function (i) { return Math.pow(x[i - 1] - mean, 2); }, show: function (i) { return "(" + x[i - 1] + "-" + G.fmt(mean, 2) + ")^2"; } },
    c: { tex: "7", f: function () { return 7; }, show: function () { return "7"; } }
  };
  var cur = "xi", lo = 1, hi = n;
  var data = G.el("div", "readout"); body.appendChild(data);
  data.innerHTML = x.map(function (v, k) { return "<div>x<sub>" + (k + 1) + "</sub><b>" + v + "</b></div>"; }).join("") + "<div>x̄ (mean of all " + n + ")<b>" + G.fmt(mean, 2) + "</b></div>";
  var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
  G.seg(ctr, [["xi", "x_i"], ["xi2", "x_i²"], ["ixi", "i·x_i"], ["dev", "(x_i − x̄)²"], ["c", "7"]], cur, function (v) { cur = v; draw(); });
  var s1 = G.slider(ctr, { label: "start i =", min: 1, max: n, value: 1, onChange: function (v) { lo = v; if (hi < lo) { hi = lo; s2.set(hi); } draw(); } });
  var s2 = G.slider(ctr, { label: "stop at", min: 1, max: n, value: n, onChange: function (v) { hi = v; if (lo > hi) { lo = hi; s1.set(lo); } draw(); } });
  var out = G.el("div", ""); out.style.cssText = "margin:10px 0;overflow-x:auto;font-size:17px"; body.appendChild(out);
  var svgHost = G.el("div", ""); body.appendChild(svgHost);
  function draw() {
    var t = terms[cur], vals = [], parts = [], shown = [];
    for (var i = lo; i <= hi; i++) { vals.push(t.f(i)); parts.push(t.show(i)); shown.push(G.fmt(t.f(i), 2)); }
    var tot = vals.reduce(function (a, b) { return a + b; }, 0);
    out.innerHTML = G.tex("\\sum_{i=" + lo + "}^{" + hi + "}" + t.tex + "=" + parts.join("+") + "=" + shown.join("+") + "=\\mathbf{" + G.fmt(tot, 3) + "}", true);
    svgHost.innerHTML = "";
    var all = []; for (var k = 1; k <= n; k++) all.push(t.f(k));
    var mx = Math.max.apply(null, all.concat([1])), mn = Math.min.apply(null, all.concat([0]));
    var pl = G.plot(svgHost, { w: 680, h: 220, x: [0.4, n + 0.6], y: [mn, mx * 1.18], xticks: x.map(function (v, k) { return k + 1; }), xlabel: "index i", ylabel: "term", label: "bar for each term of the sum" });
    for (var j = 1; j <= n; j++) {
      var on = j >= lo && j <= hi, v = t.f(j);
      var y0 = pl.Y(Math.max(0, v)), y1 = pl.Y(Math.min(0, v));
      G.svg("rect", { x: pl.X(j) - 26, y: y0, width: 52, height: Math.max(1, y1 - y0), rx: 4, fill: on ? "var(--math)" : "var(--line)", opacity: on ? 0.85 : 0.6 }, pl.layer);
      pl.text(j, Math.max(0, v) + (mx - mn) * 0.06, G.fmt(v, 2), { "text-anchor": "middle", fill: on ? "var(--ink)" : "var(--muted)" });
    }
  }
  draw();
});

G.widget("s0-maths-anatomy", function (body) {
  var F = {
    rss: { name: "ISLP's RSS", parts: [
      ["\\mathrm{RSS}", "R-S-S, the residual sum of squares: one number saying how badly a line fits. This is what is computed (step 1 of the strategy)."],
      ["=", "“equals”."],
      ["\\sum_{i=1}^{n}", "“the sum for i from 1 to n”: repeat what follows once for each observation i = 1, 2, …, n and add the results."],
      ["\\big(y_i", "y-sub-i: the true response of observation i. Data, fixed."],
      ["-\\hat\\beta_0-\\hat\\beta_1x_i", "minus the prediction, beta-nought-hat plus beta-one-hat times x-i: the height of the fitted line at x-i."],
      ["\\big)^2", "squared: so negative and positive gaps both count, and big gaps count a lot."]],
      calc: "Points (1,2), (2,3), (3,5) with beta0-hat = 1, beta1-hat = 1: residuals 0, 0, 1, so RSS = 0 + 0 + 1 = 1" },
    loss: { name: "Prince's loss", parts: [
      ["L[\\boldsymbol\\phi]", "“L of phi”: the loss, a function of the parameters phi. Square brackets are Prince's way of writing function inputs."],
      ["=", "“equals”."],
      ["\\sum_{i=1}^{I}", "sum over the I training examples (Prince writes I where ISLP writes n)."],
      ["\\big(\\mathrm{f}[x_i,\\boldsymbol\\phi]", "the model's prediction for input x-i using parameters phi."],
      ["-y_i\\big)^2", "minus the true output, squared. The order (prediction − truth) does not matter once squared."]],
      calc: "Same points, phi = (1, 1): predictions 2, 3, 4; gaps 0, 0, −1, so L = 0 + 0 + 1 = 1" },
    logit: { name: "ISLP's logistic p(X)", parts: [
      ["p(X)", "“p of X”: short for Pr(Y = 1 | X), the probability of the ‘yes’ class given the input X."],
      ["=", "“equals”."],
      ["e^{\\beta_0+\\beta_1X}", "e to the power (beta-nought plus beta-one X): always positive. The linear part beta-nought + beta-one X can be any number."],
      ["\\div\\big(1+e^{\\beta_0+\\beta_1X}\\big)", "divided by one plus the same thing: this squashes the result into (0, 1), so it is a valid probability."]],
      calc: "Default data, beta0-hat = −10.6513, beta1-hat = 0.0055, X = 2000: inside = 0.3487, e^0.3487 = 1.4172, so p = 1.4172 / 2.4172 = 0.586" }
  };
  var cur = "rss";
  var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
  G.seg(ctr, [["rss", F.rss.name], ["loss", F.loss.name], ["logit", F.logit.name]], cur, function (v) { cur = v; draw(); });
  var row = G.el("div", ""); row.style.cssText = "display:flex;flex-wrap:wrap;gap:6px;align-items:center;justify-content:center;margin:14px 0;font-size:19px"; body.appendChild(row);
  var say = G.el("div", ""); say.style.cssText = "min-height:64px;padding:10px 14px;border-radius:10px;background:var(--panel);font-size:15px"; body.appendChild(say);
  var calc = G.el("div", ""); calc.style.cssText = "margin-top:10px;font-size:14px;color:var(--muted)"; body.appendChild(calc);
  var cols = ["var(--hl1)", "var(--hl2)", "var(--hl3)", "var(--hl4)"];
  function draw() {
    row.innerHTML = ""; var f = F[cur];
    f.parts.forEach(function (p, k) {
      var b = G.el("button", "", G.tex(p[0], false)); b.type = "button";
      b.style.cssText = "border:1px solid var(--line2);border-radius:8px;padding:6px 8px;cursor:pointer;color:var(--ink);background:" + (p[0] === "=" ? "transparent" : cols[k % 4]);
      b.onclick = function () { say.innerHTML = "<b>" + G.tex(p[0], false) + "</b> — " + p[1]; Array.prototype.forEach.call(row.children, function (c) { c.style.outline = ""; }); b.style.outline = "2px solid var(--accent)"; };
      row.appendChild(b);
    });
    say.innerHTML = "Click a piece of the formula above.";
    calc.innerHTML = "<b>With numbers:</b> " + f.calc;
  }
  draw();
});
