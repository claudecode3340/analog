/* code1 · how operation counts grow: O(1), O(log n), O(n), O(n log n), O(n^2) */
G.widget("code1-bigo", function (body, args) {
  var N = args.nmax || 64;
  var fam = [
    { k: "O(1)", f: function () { return 1; }, c: "var(--good)" },
    { k: "O(log n)", f: function (n) { return Math.max(1, Math.log2(n)); }, c: "var(--isl)" },
    { k: "O(n)", f: function (n) { return n; }, c: "var(--accent)" },
    { k: "O(n log n)", f: function (n) { return n * Math.max(1, Math.log2(n)); }, c: "var(--warn)" },
    { k: "O(n²)", f: function (n) { return n * n; }, c: "var(--bad)" }
  ];
  var mode = args.mode || "zoom", n = args.n || 16;
  var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
  G.seg(ctr, [["full", "y up to n²"], ["zoom", "zoom in (y ≤ 400)"], ["log", "log scale"]], mode, function (v) { mode = v; build(); });
  var sl = G.slider(ctr, { label: "n", min: 1, max: N, step: 1, value: n, onChange: function (v) { n = v; draw(); } });
  var holder = G.el("div"); body.appendChild(holder);
  var info = G.el("div", "readout"); body.appendChild(info);
  var note = G.el("p"); note.style.cssText = "font-size:14px;color:var(--muted);margin:8px 0 0"; body.appendChild(note);
  var pl;
  function yv(v) { return mode === "log" ? Math.log10(v) : v; }
  function build() {
    holder.innerHTML = "";
    var ymax = mode === "full" ? N * N : mode === "zoom" ? 400 : Math.log10(N * N) + 0.1;
    pl = G.plot(holder, { w: 680, h: 330, x: [1, N], y: [0, ymax], xlabel: "input size n", ylabel: mode === "log" ? "steps (log scale)" : "steps",
      yticks: mode === "log" ? [] : null, pad: { l: 62, r: 92, t: 14, b: 44 }, label: "operation counts of five complexity classes against n" });
    if (mode === "log") {
      for (var e = 0; e <= Math.floor(ymax); e++) {
        G.svg("line", { x1: pl.P.l, x2: pl.W - pl.P.r, y1: pl.Y(e), y2: pl.Y(e), class: "grid" }, pl.svg);
        var t = G.svg("text", { x: pl.P.l - 8, y: pl.Y(e) + 4, "text-anchor": "end", class: "tick" }, pl.svg); t.textContent = String(Math.pow(10, e));
      }
    }
    draw();
  }
  function draw() {
    pl.clear();
    var ymax = mode === "full" ? N * N : mode === "zoom" ? 400 : Math.log10(N * N) + 0.1;
    pl.line([[n, 0], [n, ymax]], { stroke: "var(--muted)", "stroke-dasharray": "5 5", "stroke-width": 1.5 });
    var labs = [];
    fam.forEach(function (F) {
      var pts = [], last = null;
      for (var x = 1; x <= N; x += 0.25) {
        var v = F.f(x);
        if (v > ymax && mode !== "log") { pts.push([x, ymax]); last = [x, ymax]; break; }
        pts.push([x, yv(v)]); last = [x, yv(v)];
      }
      pl.line(pts, { stroke: F.c, "stroke-width": 2.6 });
      labs.push({ x: pl.X(Math.min(last[0], N)), y: pl.Y(last[1]), F: F });
      var vn = F.f(n);
      if (mode === "log" || vn <= ymax) pl.dot(n, yv(vn), { r: 5, fill: F.c, stroke: "var(--surface)", "stroke-width": 2 });
    });
    labs.sort(function (a, b) { return b.y - a.y; });
    for (var i = 1; i < labs.length; i++) if (labs[i - 1].y - labs[i].y < 15 && Math.abs(labs[i - 1].x - labs[i].x) < 60) labs[i].y = labs[i - 1].y - 15;
    labs.forEach(function (L) { var t = G.svg("text", { x: L.x + 6, y: L.y + 4, class: "tick", fill: L.F.c, "font-weight": 700 }, pl.layer); t.textContent = L.F.k; t.style.fill = L.F.c; });
    info.innerHTML = fam.map(function (F) { return "<div>" + F.k + "<b>" + G.fmt(F.f(n), 1) + "</b></div>"; }).join("");
    var d = n * n / (n * Math.max(1, Math.log2(n)));
    note.innerHTML = "At n = " + n + ", an O(n²) method takes <b>" + G.fmt(n * n / Math.max(1, n), 1) + "×</b> the steps of an O(n) one, and <b>" + G.fmt(d, 1) + "×</b> the steps of an O(n log n) one. Double n and watch which numbers double and which quadruple.";
  }
  build();
});
