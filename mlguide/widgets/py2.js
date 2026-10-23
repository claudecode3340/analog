/* py2 · k-nearest neighbours in 2-D: drag the new point, change k, watch the vote */
G.widget("py2-knn", function (body, args) {
  var train = args.train || [
    [1.0, 2.0, "blue"], [2.0, 1.0, "blue"], [2.5, 3.0, "blue"], [3.0, 1.5, "blue"], [4.0, 3.5, "blue"], [1.5, 4.5, "blue"],
    [6.0, 6.5, "orange"], [7.0, 5.0, "orange"], [5.5, 8.0, "orange"], [8.0, 7.0, "orange"], [6.5, 3.5, "orange"], [4.5, 6.0, "orange"]];
  var q = (args.query || [4, 4.5]).slice(), k = args.k || 3, regions = false;
  var COL = { blue: "var(--tool)", orange: "var(--math)" };
  var ctl = G.el("div"); ctl.style.cssText = "display:flex;flex-wrap:wrap;gap:6px 16px;align-items:center"; body.appendChild(ctl);
  var ks = G.slider(ctl, { label: "k", min: 1, max: 11, step: 2, value: k, onChange: function (v) { k = v; draw(); } });
  G.seg(ctl, [["off", "Just the vote"], ["on", "Colour the whole map"]], "off", function (v) { regions = v === "on"; draw(); });
  var grid = G.el("div"); grid.style.cssText = "display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));align-items:start;margin-top:6px"; body.appendChild(grid);
  var left = G.el("div"); grid.appendChild(left);
  var right = G.el("div"); grid.appendChild(right);
  var pl = G.plot(left, { w: 460, h: 440, x: [0, 10], y: [0, 10], xlabel: "x1", ylabel: "x2", pad: { l: 44, r: 14, t: 14, b: 44 }, label: "training points and the new point with its nearest neighbours" });
  var info = G.el("div", "readout"); right.appendChild(info);
  var tbl = G.el("div"); tbl.style.cssText = "font-size:14.5px;margin-top:8px"; right.appendChild(tbl);
  var drag = false;
  function dist(a, b) { return Math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])); }
  function vote(p, kk) {
    var ds = train.map(function (t, i) { return { i: i, d: dist(p, t), c: t[2] }; }).sort(function (a, b) { return a.d - b.d; });
    var near = ds.slice(0, kk), cnt = { blue: 0, orange: 0 };
    near.forEach(function (n) { cnt[n.c]++; });
    return { near: near, cnt: cnt, pred: cnt.blue > cnt.orange ? "blue" : "orange" };
  }
  function draw() {
    pl.clear();
    if (regions) {
      var n = 50, s = 10 / n, gr = G.svg("g", { style: "opacity:.17" }, pl.layer);
      for (var a = 0; a < n; a++) for (var b = 0; b < n; b++) {
        var v = vote([(a + 0.5) * s, (b + 0.5) * s], k);
        G.svg("rect", { x: pl.X(a * s), y: pl.Y((b + 1) * s), width: pl.X(s) - pl.X(0) + 0.6, height: pl.Y(0) - pl.Y(s) + 0.6, style: "fill:" + COL[v.pred] }, gr);
      }
    }
    var r = vote(q, k), rad = r.near[r.near.length - 1].d;
    G.svg("circle", { cx: pl.X(q[0]), cy: pl.Y(q[1]), r: pl.X(rad) - pl.X(0), style: "fill:none;stroke:var(--muted);stroke-width:1.2;stroke-dasharray:5 4" }, pl.layer);
    r.near.forEach(function (nb) { var t = train[nb.i]; pl.line([q, [t[0], t[1]]], { stroke: COL[nb.c], "stroke-width": 2, opacity: 0.8 }); });
    train.forEach(function (t, i) {
      var isN = r.near.some(function (nb) { return nb.i === i; });
      pl.dot(t[0], t[1], { r: isN ? 8 : 6.5, style: "fill:" + COL[t[2]] + ";stroke:var(--surface);stroke-width:2" + (isN ? "" : ";opacity:.75") });
    });
    var qd = pl.dot(q[0], q[1], { r: 11, style: "fill:var(--surface);stroke:" + COL[r.pred] + ";stroke-width:4;cursor:grab" });
    pl.text(q[0], q[1] - 0.16, "?", { "text-anchor": "middle", style: "fill:var(--ink);font-weight:700;font-size:13px" });
    qd.addEventListener("pointerdown", function (e) { drag = true; try { pl.svg.setPointerCapture(e.pointerId); } catch (x) {} e.preventDefault(); });
    info.innerHTML = "<div>new point<b>(" + G.fmt(q[0], 1) + ", " + G.fmt(q[1], 1) + ")</b></div><div>votes blue : orange<b>" + r.cnt.blue + " : " + r.cnt.orange + "</b></div><div>prediction<b style=\"color:" + COL[r.pred] + "\">" + r.pred + "</b></div>";
    tbl.innerHTML = '<div class="tw"><table class="t"><thead><tr><th>rank</th><th>neighbour</th><th>distance</th><th>class</th></tr></thead><tbody>' + r.near.map(function (nb, j) { var t = train[nb.i]; return "<tr><td class=\"n\">" + (j + 1) + "</td><td>(" + t[0] + ", " + t[1] + ")</td><td class=\"n\">" + nb.d.toFixed(3) + "</td><td style=\"color:" + COL[nb.c] + ";font-weight:700\">" + nb.c + "</td></tr>"; }).join("") + "</tbody></table></div>";
  }
  function move(e) {
    if (!drag) return;
    var rc = pl.svg.getBoundingClientRect(), px = (e.clientX - rc.left) / rc.width * pl.W, py = (e.clientY - rc.top) / rc.height * pl.H;
    var x = (px - pl.P.l) / (pl.W - pl.P.l - pl.P.r) * 10, y = (pl.H - pl.P.b - py) / (pl.H - pl.P.t - pl.P.b) * 10;
    q = [Math.max(0, Math.min(10, Math.round(x * 10) / 10)), Math.max(0, Math.min(10, Math.round(y * 10) / 10))]; draw();
  }
  pl.svg.style.touchAction = "none";
  pl.svg.addEventListener("pointermove", move);
  pl.svg.addEventListener("pointerup", function () { drag = false; });
  pl.svg.addEventListener("click", function (e) { if (e.target.tagName === "circle") return; drag = true; move(e); drag = false; });
  draw();
});
