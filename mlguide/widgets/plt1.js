/* plt1 · matplotlib widgets: format-string builder, histogram bins */
(function () {
  G.widget("plt1-style", function (body) {
    var st = { c: "r", m: "o", l: "--", lw: 2, ms: 7 };
    var COL = { b: ["var(--tool)", "blue"], r: ["var(--bad)", "red"], g: ["var(--good)", "green"], k: ["var(--ink)", "black"] };
    var c1 = G.el("div", "ctrls"); body.appendChild(c1);
    G.seg(c1, [["b", "b blue"], ["r", "r red"], ["g", "g green"], ["k", "k black"]], st.c, function (v) { st.c = v; draw(); });
    var c2 = G.el("div", "ctrls"); body.appendChild(c2);
    G.seg(c2, [["", "no marker"], ["o", "o"], ["s", "s"], ["^", "^"], ["+", "+"], ["x", "x"]], st.m, function (v) { st.m = v; draw(); });
    G.seg(c2, [["-", "-"], ["--", "--"], [":", ":"], ["-.", "-."], ["", "no line"]], st.l, function (v) { st.l = v; draw(); });
    var c3 = G.el("div", "ctrls"); body.appendChild(c3);
    G.slider(c3, { label: "linewidth", min: 0.5, max: 5, step: 0.5, value: st.lw, onChange: function (v) { st.lw = v; draw(); } });
    G.slider(c3, { label: "markersize", min: 3, max: 14, step: 1, value: st.ms, onChange: function (v) { st.ms = v; draw(); } });
    var code = G.el("pre"); code.style.cssText = "font:600 14px/1.6 var(--mono);background:var(--panel);color:var(--ink);padding:10px 12px;border-radius:10px;margin:4px 0 8px;white-space:pre-wrap;word-break:break-word"; body.appendChild(code);
    var pl = G.plot(body, { w: 400, h: 220, x: [0, 1], y: [-1.3, 1.3], xlabel: "x", ylabel: "sin(2π·2x)", pad: { l: 50, r: 14, t: 12, b: 40 }, label: "preview of the styled line" });
    var note = G.el("p"); note.style.cssText = "font-size:14px;color:var(--muted);margin:6px 0 0"; body.appendChild(note);
    function marker(x, y, col) {
      var X = pl.X(x), Y = pl.Y(y), r = st.ms / 2 + 1, L = pl.layer;
      if (st.m === "o") G.svg("circle", { cx: X, cy: Y, r: r, fill: col }, L);
      else if (st.m === "s") G.svg("rect", { x: X - r, y: Y - r, width: 2 * r, height: 2 * r, fill: col }, L);
      else if (st.m === "^") G.svg("path", { d: "M" + X + " " + (Y - r * 1.2) + "L" + (X + r * 1.1) + " " + (Y + r * 0.8) + "L" + (X - r * 1.1) + " " + (Y + r * 0.8) + "Z", fill: col }, L);
      else if (st.m === "+") G.svg("path", { d: "M" + (X - r) + " " + Y + "H" + (X + r) + "M" + X + " " + (Y - r) + "V" + (Y + r), stroke: col, "stroke-width": 2 }, L);
      else if (st.m === "x") G.svg("path", { d: "M" + (X - r) + " " + (Y - r) + "L" + (X + r) + " " + (Y + r) + "M" + (X + r) + " " + (Y - r) + "L" + (X - r) + " " + (Y + r), stroke: col, "stroke-width": 2 }, L);
    }
    function draw() {
      pl.clear();
      var col = COL[st.c][0], pts = [];
      for (var i = 0; i <= 16; i++) { var x = i / 16; pts.push([x, Math.sin(2 * Math.PI * 2 * x)]); }
      var dash = { "-": "", "--": "10 6", ":": "2 5", "-.": "10 5 2 5" }[st.l];
      if (st.l) pl.line(pts, { stroke: col, "stroke-width": st.lw * 1.4, "stroke-dasharray": dash, "stroke-linecap": st.l === ":" ? "round" : "butt" });
      if (st.m) pts.forEach(function (p) { marker(p[0], p[1], col); });
      var fmt = st.c + st.m + st.l;
      var kw = ["color='" + COL[st.c][1] + "'"];
      if (st.m) kw.push("marker='" + st.m + "'", "markersize=" + st.ms);
      kw.push("linestyle='" + (st.l || "none") + "'");
      if (st.l) kw.push("linewidth=" + st.lw);
      code.textContent = "ax.plot(x, y, '" + fmt + "'" + (st.l ? ", linewidth=" + st.lw : "") + (st.m ? ", markersize=" + st.ms : "") + ")\n# the same with keywords only:\nax.plot(x, y, " + kw.join(", ") + ")";
      note.innerHTML = !st.l && !st.m ? "<b style='color:var(--bad)'>No marker and no line: nothing is drawn.</b>" : !st.l ? "Markers only: this is a scatter plot, like ISLP's <code>ax.plot(x, y, 'o')</code>." : !st.m ? "A plain line: right for a function or a time series." : "Line and markers: shows both the trend and the actual samples.";
    }
    draw();
  });

  G.widget("plt1-bins", function (body, args) {
    var v = args.mpg || [], lo = 8, hi = 48, bins = 12;
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    var sl = G.slider(ctr, { label: "bins", min: 2, max: 80, step: 1, value: bins, onChange: function (b) { bins = b; draw(); } });
    G.seg(ctr, [[3, "3"], [12, "12"], [25, "25"], [80, "80"]], 12, function (b) { bins = +b; sl.set(b); draw(); });
    var codeL = G.el("div"); codeL.style.cssText = "font:700 15px var(--mono);color:var(--tool);margin:2px 0 6px"; body.appendChild(codeL);
    var pl = null, holder = G.el("div"); body.appendChild(holder);
    var info = G.el("div", "readout"); body.appendChild(info);
    var mn = Math.min.apply(null, v), mx = Math.max.apply(null, v);
    function draw() {
      var w = (mx - mn) / bins, counts = new Array(bins).fill(0);
      v.forEach(function (x) { var k = Math.min(bins - 1, Math.floor((x - mn) / w)); counts[k]++; });
      var top = Math.max.apply(null, counts);
      holder.innerHTML = "";
      pl = G.plot(holder, { w: 400, h: 260, x: [lo, hi], y: [0, top * 1.08], xlabel: "mpg (miles per gallon)", ylabel: "number of cars", pad: { l: 54, r: 14, t: 12, b: 42 }, label: "histogram of Auto mpg" });
      counts.forEach(function (c, k) {
        var x0 = pl.X(mn + k * w), x1 = pl.X(mn + (k + 1) * w);
        G.svg("rect", { x: x0 + 0.5, y: pl.Y(c), width: Math.max(0.5, x1 - x0 - 1), height: pl.Y(0) - pl.Y(c), fill: "var(--tool)", opacity: 0.85 }, pl.layer);
      });
      codeL.textContent = "ax.hist(Auto['mpg'], bins=" + bins + ")";
      info.innerHTML = "<div>cars<b>" + v.length + "</b></div><div>bin width<b>" + G.fmt(w, 2) + " mpg</b></div><div>tallest bar<b>" + top + "</b></div><div>empty bins<b>" + counts.filter(function (c) { return c === 0; }).length + "</b></div>";
    }
    draw();
  });
})();
