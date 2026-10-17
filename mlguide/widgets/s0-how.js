/* s0-how · drag the dots, watch the mean (reference example of the widget pattern) */
G.widget("s0-mean-drag", function (body, args) {
  var xs = (args.values || [62, 75, 81, 70]).slice();
  var info = G.el("div", "readout"); body.appendChild(info);
  var pl = G.plot(body, { w: 680, h: 230, x: [40, 100], y: [0, 1], yticks: [], xlabel: "mark", pad: { l: 20, r: 20, t: 20, b: 44 }, label: "marks on a number line with their mean" });
  var drag = -1;
  function draw() {
    pl.clear();
    var m = xs.reduce(function (a, b) { return a + b; }, 0) / xs.length;
    pl.line([[m, 0.05], [m, 0.95]], { stroke: "var(--udl)", "stroke-dasharray": "6 5", "stroke-width": 2 });
    pl.text(m, 0.97, "mean " + G.fmt(m, 2), { "text-anchor": "middle", fill: "var(--udl)", "font-weight": 700 });
    xs.forEach(function (x, i) {
      var c = pl.dot(x, 0.45, { r: 11, fill: "var(--accent)", stroke: "var(--surface)", "stroke-width": 3, style: "cursor:grab" });
      c.addEventListener("pointerdown", function (e) { drag = i; c.setPointerCapture(e.pointerId); });
      pl.text(x, 0.22, String(Math.round(x)), { "text-anchor": "middle" });
    });
    info.innerHTML = "<div>sum<b>" + G.fmt(xs.reduce(function (a, b) { return a + b; }, 0), 1) + "</b></div><div>n<b>" + xs.length + "</b></div><div>mean = sum ÷ n<b>" + G.fmt(m, 2) + "</b></div>";
  }
  pl.svg.addEventListener("pointermove", function (e) {
    if (drag < 0) return;
    var r = pl.svg.getBoundingClientRect(), px = (e.clientX - r.left) / r.width * pl.W;
    var v = 40 + (px - pl.P.l) / (pl.W - pl.P.l - pl.P.r) * 60; xs[drag] = Math.max(40, Math.min(100, Math.round(v))); draw();
  });
  pl.svg.addEventListener("pointerup", function () { drag = -1; });
  draw();
});
