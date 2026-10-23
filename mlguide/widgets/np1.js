/* np1 · NumPy I widgets: slicing explorer, axis reductions, reshape/transpose */
(function () {
  /* Python slice semantics for one axis of length n: returns {idx:[...], keep:bool, text} or throws */
  function parseSpec(s, n) {
    s = (s || "").trim();
    if (s === "") s = ":";
    if (s.indexOf(":") < 0) {
      if (!/^-?\d+$/.test(s)) throw new Error("'" + s + "' is not an integer or a slice");
      var k = parseInt(s, 10), kk = k < 0 ? k + n : k;
      if (kk < 0 || kk >= n) throw new Error("IndexError: index " + k + " is out of bounds for axis with size " + n);
      return { idx: [kk], keep: false, text: String(k) };
    }
    var parts = s.split(":");
    if (parts.length > 3) throw new Error("A slice has at most two colons: start:stop:step");
    var num = function (t) { t = (t || "").trim(); if (t === "") return null; if (!/^-?\d+$/.test(t)) throw new Error("'" + t + "' is not an integer"); return parseInt(t, 10); };
    var a = num(parts[0]), b = num(parts[1]), st = parts.length > 2 ? num(parts[2]) : null;
    if (st === 0) throw new Error("ValueError: slice step cannot be zero");
    var step = st == null ? 1 : st;
    function norm(v, isStop) {
      if (v == null) return step > 0 ? (isStop ? n : 0) : (isStop ? -1 : n - 1);
      if (v < 0) { v += n; if (v < 0) v = step < 0 ? -1 : 0; }
      else if (v >= n) v = step < 0 ? n - 1 : n;
      return v;
    }
    var i0 = norm(a, false), i1 = norm(b, true), out = [];
    if (step > 0) for (var i = i0; i < i1; i += step) out.push(i);
    else for (var j = i0; j > i1; j += step) out.push(j);
    return { idx: out, keep: true, text: s.replace(/\s+/g, "") };
  }

  G.widget("np1-slicer", function (body) {
    var R = 5, C = 6;
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    function box(label, val) {
      var w = G.el("label", "ctrl", "<span>" + label + "</span>");
      var i = G.el("input"); i.type = "text"; i.value = val; i.spellcheck = false; i.setAttribute("autocapitalize", "off");
      i.style.cssText = "width:7em;font:600 15px var(--mono);padding:5px 8px;border:1px solid var(--line2);border-radius:8px;background:var(--surface);color:var(--ink)";
      w.appendChild(i); ctr.appendChild(w); i.addEventListener("input", draw); return i;
    }
    var rIn = box("rows", "1:4"), cIn = box("columns", "::2");
    var pre = G.el("div", "ctrls"); pre.style.gap = "6px"; body.appendChild(pre);
    [["1", ":"], [":", "2"], ["0:2", "1:3"], ["1:4:2", "0:3:2"], ["::-1", ":"], ["::4", "::5"], ["-1", "::-1"]].forEach(function (p) {
      var b = G.button(pre, "A[" + p[0] + ", " + p[1] + "]", function () { rIn.value = p[0]; cIn.value = p[1]; draw(); });
      b.style.fontFamily = "var(--mono)";
    });
    var expr = G.el("div"); expr.style.cssText = "font:700 18px var(--mono);margin:6px 0 10px;color:var(--tool)"; body.appendChild(expr);
    var wrap = G.el("div"); wrap.style.cssText = "display:flex;flex-wrap:wrap;gap:18px;align-items:flex-start"; body.appendChild(wrap);
    var gridBox = G.el("div"); wrap.appendChild(gridBox);
    var resBox = G.el("div"); resBox.style.cssText = "flex:1;min-width:220px"; wrap.appendChild(resBox);
    var cells = [];
    var g = G.el("div"); g.style.cssText = "display:inline-grid;grid-template-columns:repeat(" + (C + 1) + ",auto);gap:3px;user-select:none;touch-action:none";
    gridBox.appendChild(g);
    var hs = "display:grid;place-items:center;font:600 11px var(--mono);color:var(--faint);min-width:18px;min-height:18px";
    g.appendChild(G.el("span", "", "")).style.cssText = hs;
    for (var j = 0; j < C; j++) { var h = G.el("span", "", String(j)); h.style.cssText = hs; g.appendChild(h); }
    var drag = null;
    for (var i = 0; i < R; i++) {
      var hh = G.el("span", "", String(i)); hh.style.cssText = hs; g.appendChild(hh); cells.push([]);
      for (var k = 0; k < C; k++) {
        var c = G.el("span", "", String(i * C + k));
        c.style.cssText = "display:grid;place-items:center;width:42px;height:36px;border-radius:6px;font:500 14px var(--mono);background:var(--panel);cursor:pointer;transition:background .12s";
        (function (ii, kk) {
          c.addEventListener("pointerdown", function (e) { e.preventDefault(); drag = [ii, kk]; set(ii, kk); });
          c.addEventListener("pointerenter", function () { if (drag) set(ii, kk); });
        })(i, k);
        g.appendChild(c); cells[i].push(c);
      }
    }
    document.addEventListener("pointerup", function () { drag = null; });
    function set(i, k) {
      var r0 = Math.min(drag[0], i), r1 = Math.max(drag[0], i), c0 = Math.min(drag[1], k), c1 = Math.max(drag[1], k);
      rIn.value = r0 + ":" + (r1 + 1); cIn.value = c0 + ":" + (c1 + 1); draw();
    }
    function pad(v) { v = String(v); return " ".repeat(Math.max(0, 2 - v.length)) + v; }
    function fmtArr(rs, cs, rk, ck) {
      if (!rk && !ck) return "np.int64(" + (rs[0] * C + cs[0]) + ")";
      if (rk && ck) {
        var rows = rs.map(function (r) { return "[" + cs.map(function (c) { return pad(r * C + c); }).join(", ") + "]"; });
        return "array([" + rows.join(",\n       ") + "])";
      }
      var flat = rk ? rs.map(function (r) { return r * C + cs[0]; }) : cs.map(function (c) { return rs[0] * C + c; });
      return "array([" + flat.map(pad).join(", ") + "])";
    }
    function draw() {
      var rs, cs;
      cells.forEach(function (row) { row.forEach(function (c) { c.style.background = "var(--panel)"; c.style.boxShadow = ""; c.style.fontWeight = "500"; }); });
      try { rs = parseSpec(rIn.value, R); cs = parseSpec(cIn.value, C); }
      catch (e) { expr.textContent = "A[" + rIn.value + ", " + cIn.value + "]"; resBox.innerHTML = '<div style="color:var(--bad);font-weight:600;font-size:14px">' + G.esc(e.message) + "</div>"; return; }
      expr.textContent = "A[" + rs.text + ", " + cs.text + "]";
      var first = true;
      rs.idx.forEach(function (r) { cs.idx.forEach(function (c) { var el = cells[r][c]; el.style.background = "var(--hl1)"; el.style.fontWeight = "700"; if (first) { el.style.boxShadow = "inset 0 0 0 2px var(--warn)"; first = false; } }); });
      var shape = [];
      if (rs.keep) shape.push(rs.idx.length); if (cs.keep) shape.push(cs.idx.length);
      var shp = "(" + shape.join(", ") + (shape.length === 1 ? "," : "") + ")";
      var empty = rs.idx.length === 0 || cs.idx.length === 0;
      resBox.innerHTML = '<div class="readout"><div>rows<b>' + (rs.idx.join(", ") || "none") + '</b></div><div>columns<b>' + (cs.idx.join(", ") || "none") + '</b></div><div>result shape<b>' + (shape.length ? shp : "()") + "</b></div></div>" +
        '<pre style="font:13.5px/1.5 var(--mono);background:var(--panel);color:var(--ink);padding:8px 10px;border-radius:8px;margin:8px 0;white-space:pre;overflow-x:auto">' + (empty ? "array([], shape=" + shp + ", dtype=int64)" : fmtArr(rs.idx, cs.idx, rs.keep, cs.keep)) + "</pre>" +
        '<div style="font-size:13.5px;color:var(--muted);line-height:1.5">The outlined cell is the first element of the result. ' + (!rs.keep && !cs.keep ? "Two integers pick a single element." : (!rs.keep || !cs.keep) ? "An integer index removed one axis, so the result is 1-D." : "Two slices keep both axes, so the result is 2-D.") + "</div>";
    }
    draw();
  });

  G.widget("np1-axis", function (body) {
    var B = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]];
    var op = "sum", ax = "0";
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    G.seg(ctr, [["sum", "sum"], ["mean", "mean"], ["max", "max"], ["argmax", "argmax"]], op, function (v) { op = v; draw(); });
    G.seg(ctr, [["none", "no axis"], ["0", "axis=0"], ["1", "axis=1"]], ax, function (v) { ax = v; draw(); });
    var expr = G.el("div"); expr.style.cssText = "font:700 17px var(--mono);margin:4px 0 6px;color:var(--tool)"; body.appendChild(expr);
    var row = G.el("div", "mrow"); body.appendChild(row);
    var note = G.el("p"); note.style.cssText = "font-size:14px;color:var(--muted);margin:6px 0 0;line-height:1.5"; body.appendChild(note);
    var cols = ["h1", "h2", "h3", "h4"], rowc = ["h1", "h2", "h4"];
    function red(v) {
      if (op === "sum") return v.reduce(function (a, b) { return a + b; }, 0);
      if (op === "mean") return v.reduce(function (a, b) { return a + b; }, 0) / v.length;
      if (op === "max") return Math.max.apply(null, v);
      var m = 0; v.forEach(function (x, i) { if (x > v[m]) m = i; }); return m;
    }
    function grid(vals, clsOf, ncol) {
      var s = '<span class="mgrid" style="grid-template-columns:repeat(' + ncol + ',auto)">';
      vals.forEach(function (v, i) { var c = clsOf(i); s += "<span" + (c ? ' class="' + c + '"' : "") + ">" + G.fmt(v, 2) + "</span>"; });
      return s + "</span>";
    }
    function draw() {
      var flat = [].concat.apply([], B), res, cls, rcls, ncol;
      expr.textContent = "B." + op + "(" + (ax === "none" ? "" : "axis=" + ax) + ")";
      if (ax === "none") { res = [red(flat)]; cls = function () { return "h1"; }; rcls = cls; ncol = 1; }
      else if (ax === "0") { res = [0, 1, 2, 3].map(function (j) { return red(B.map(function (r) { return r[j]; })); }); cls = function (i) { return cols[i % 4]; }; rcls = function (i) { return cols[i]; }; ncol = 4; }
      else { res = B.map(red); cls = function (i) { return rowc[Math.floor(i / 4)]; }; rcls = function (i) { return rowc[i]; }; ncol = 1; }
      var shape = ax === "none" ? "a single number" : "shape (" + res.length + ",)";
      row.innerHTML = '<span>' + grid(flat, cls, 4) + '<span class="lab">B, shape (3, 4)</span></span><span class="op">→</span><span>' +
        grid(res, rcls, ncol) + '<span class="lab">' + shape + "</span></span>";
      var t = ax === "none" ? "No axis: all 12 numbers are combined into one." :
        ax === "0" ? "axis=0: go <b>down</b> the rows. Axis 0 (length 3) disappears, leaving one answer per column: 4 answers." :
        "axis=1: go <b>across</b> the columns. Axis 1 (length 4) disappears, leaving one answer per row: 3 answers (NumPy returns them as a 1-D array; they are drawn as a column here so you can see which row each came from).";
      if (op === "argmax") t += ax === "0" ? " argmax gives the <i>row number</i> where each column is largest." : ax === "1" ? " argmax gives the <i>column number</i> where each row is largest." : " Without an axis, argmax counts positions in the flattened array, row by row: 11 is the last cell.";
      note.innerHTML = t;
    }
    draw();
  });

  G.widget("np1-reshape", function (body) {
    var shapes = [[1, 12], [2, 6], [3, 4], [4, 3], [6, 2], [12, 1]], cur = [3, 4], tr = false;
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    G.seg(ctr, shapes.map(function (s) { return [s.join("x"), s[0] + "×" + s[1]]; }), "3x4", function (v) { cur = v.split("x").map(Number); draw(); });
    G.seg(ctr, [["n", "as is"], ["t", ".T"]], "n", function (v) { tr = v === "t"; draw(); });
    var expr = G.el("div"); expr.style.cssText = "font:700 16px var(--mono);margin:4px 0 8px;color:var(--tool)"; body.appendChild(expr);
    var holder = G.el("div"); holder.style.cssText = "overflow-x:auto"; body.appendChild(holder);
    var info = G.el("div", "readout"); body.appendChild(info);
    function draw() {
      var r = cur[0], c = cur[1], R = tr ? c : r, Cc = tr ? r : c;
      expr.textContent = "np.arange(12).reshape(" + r + ", " + c + ")" + (tr ? ".T" : "");
      var s = '<span class="mgrid" style="grid-template-columns:repeat(' + Cc + ',auto)">';
      for (var i = 0; i < R; i++) for (var j = 0; j < Cc; j++) {
        var v = tr ? j * c + i : i * c + j, p = Math.round(12 + v / 11 * 70);
        s += '<span style="background:color-mix(in srgb,var(--tool) ' + p + '%,var(--panel));' + (p > 50 ? "color:#fff" : "") + '">' + v + "</span>";
      }
      holder.innerHTML = s + "</span>";
      var firstRow = []; for (var q = 0; q < Cc; q++) firstRow.push(tr ? q * c : q);
      info.innerHTML = "<div>shape<b>(" + R + ", " + Cc + ")</b></div><div>first row<b>" + firstRow.join(" ") + "</b></div><div>element [i, j] holds<b>" + (tr ? "j*" + c + " + i" : "i*" + c + " + j") + "</b></div>";
    }
    draw();
  });
})();
