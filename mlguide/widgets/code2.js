/* code2 · step through the hash-map and two-pointer patterns */
(function () {
  function framesPair(a, t) {
    var F = [], L = 0, R = a.length - 1;
    F.push({ a: a, p: { L: L, R: R }, msg: "Start: L at the smallest item, R at the largest. Target " + t + "." });
    while (L < R) {
      var s = a[L] + a[R];
      if (s === t) { F.push({ a: a, p: { L: L, R: R }, hl: [L, R], good: true, msg: a[L] + " + " + a[R] + " = " + s + " = target. Found the pair at indices (" + L + ", " + R + ")." }); return F; }
      if (s < t) { F.push({ a: a, p: { L: L, R: R }, hl: [L, R], msg: a[L] + " + " + a[R] + " = " + s + " < " + t + ": too small. Only a bigger left item can help, so L moves right." }); L++; }
      else { F.push({ a: a, p: { L: L, R: R }, hl: [L, R], msg: a[L] + " + " + a[R] + " = " + s + " > " + t + ": too big. Only a smaller right item can help, so R moves left." }); R--; }
      F.push({ a: a, p: { L: L, R: R }, msg: "Now L = " + L + ", R = " + R + "." });
    }
    F.push({ a: a, p: { L: L, R: R }, bad: true, msg: "L and R met: no pair adds up to " + t + "." });
    return F;
  }
  function framesZeros(a0) {
    var a = a0.slice(), F = [], w = 0;
    F.push({ a: a.slice(), p: { w: 0, r: 0 }, msg: "w (write) marks where the next non-zero goes; r (read) visits every item." });
    for (var r = 0; r < a.length; r++) {
      if (a[r] !== 0) {
        var msg = "a[" + r + "] = " + a[r] + " is not zero: swap a[w=" + w + "] and a[r=" + r + "], then w moves right.";
        var t = a[w]; a[w] = a[r]; a[r] = t;
        F.push({ a: a.slice(), p: { w: w, r: r }, hl: [w, r], msg: msg }); w++;
      } else F.push({ a: a.slice(), p: { w: w, r: r }, hl: [r], msg: "a[" + r + "] = 0: skip it. w stays at " + w + "." });
    }
    F.push({ a: a.slice(), p: { w: w }, good: true, msg: "Done. The non-zeros kept their order; zeros fill positions " + w + " onwards." });
    return F;
  }
  function pairs(d, order) { return order.map(function (k) { return [k, d[k]]; }); }
  function framesTwoSum(a, t) {
    var F = [], d = {}, order = [];
    F.push({ a: a, p: {}, d: [], msg: "Empty dict: it will map value → index for everything seen so far. Target " + t + "." });
    for (var i = 0; i < a.length; i++) {
      var need = t - a[i];
      if (need in d) { F.push({ a: a, p: { i: i }, hl: [d[need], i], d: pairs(d, order), good: true, msg: "a[" + i + "] = " + a[i] + ", need " + t + " − " + a[i] + " = " + need + ". " + need + " is in the dict at index " + d[need] + ": answer (" + d[need] + ", " + i + ")." }); return F; }
      F.push({ a: a, p: { i: i }, hl: [i], d: pairs(d, order), msg: "a[" + i + "] = " + a[i] + ", need " + t + " − " + a[i] + " = " + need + ". Not in the dict, so store " + a[i] + " → " + i + "." });
      d[a[i]] = i; order.push(a[i]);
    }
    F.push({ a: a, p: {}, d: pairs(d, order), bad: true, msg: "No pair found." });
    return F;
  }
  function framesCount(s) {
    var F = [], d = {}, order = [], a = s.split("");
    F.push({ a: a, p: {}, d: [], msg: "Empty dict. For each character: counts[ch] = counts.get(ch, 0) + 1." });
    for (var i = 0; i < a.length; i++) {
      var old = d[a[i]] || 0; if (!old) order.push(a[i]); d[a[i]] = old + 1;
      F.push({ a: a, p: { i: i }, hl: [i], d: pairs(d, order), msg: "'" + a[i] + "': get gives " + old + ", so store " + (old + 1) + "." });
    }
    F.push({ a: a, p: {}, d: pairs(d, order), good: true, msg: "One pass, one dict update per character: O(n)." });
    return F;
  }
  G.widget("code2-pointers", function (body, args) {
    var modes = {
      count: function () { return framesCount("banana"); },
      twosum: function () { return framesTwoSum([3, 8, 4, 6, 1], 10); },
      pair: function () { return framesPair([1, 3, 4, 6, 8, 11], 10); },
      zeros: function () { return framesZeros([0, 1, 0, 3, 12, 0, 5]); }
    };
    var mode = args.mode || "pair", F = modes[mode](), k = 0;
    var ctr = G.el("div", "ctrls"); body.appendChild(ctr);
    G.seg(ctr, [["count", "count letters"], ["twosum", "two-sum (dict)"], ["pair", "pair sum"], ["zeros", "move zeros"]], mode, function (v) { mode = v; F = modes[v](); k = 0; draw(); });
    var btns = G.el("div", "ctrls"); body.appendChild(btns);
    G.button(btns, "◀ Back", function () { if (k > 0) { k--; draw(); } });
    G.button(btns, "Next ▶", function () { if (k < F.length - 1) { k++; draw(); } });
    G.button(btns, "Reset", function () { k = 0; draw(); });
    var svgBox = G.el("div"); body.appendChild(svgBox);
    var msg = G.el("p"); msg.style.cssText = "min-height:3.2em;margin:10px 0;font-size:15px;line-height:1.55"; body.appendChild(msg);
    var info = G.el("div", "readout"); body.appendChild(info);
    function draw() {
      var f = F[k], n = f.a.length, cw = 64, W = Math.max(n * cw + 40, 300), H = 150;
      svgBox.innerHTML = "";
      var s = G.svg("svg", { viewBox: "0 0 " + W + " " + H, class: "wsvg", role: "img", "aria-label": "list with pointers" }, svgBox);
      s.style.maxWidth = Math.round(W * 1.1) + "px";
      for (var i = 0; i < n; i++) {
        var x = 20 + i * cw, on = f.hl && f.hl.indexOf(i) >= 0, col = f.good ? "var(--good)" : "var(--accent)";
        G.svg("rect", { x: x + 3, y: 30, width: cw - 6, height: 48, rx: 8, fill: on ? col : "var(--panel)", "fill-opacity": on ? 0.22 : 1, stroke: on ? col : "var(--line)", "stroke-width": 2 }, s);
        var t = G.svg("text", { x: x + cw / 2, y: 61, "text-anchor": "middle", style: "font:600 20px var(--mono);fill:var(--ink)" }, s); t.textContent = f.a[i];
        var ix = G.svg("text", { x: x + cw / 2, y: 22, "text-anchor": "middle", class: "tick" }, s); ix.textContent = i;
      }
      var cols = { L: "var(--accent)", R: "var(--bad)", w: "var(--good)", r: "var(--accent)", i: "var(--accent)" };
      var used = {};
      Object.keys(f.p).forEach(function (name) {
        var i = f.p[name]; if (i == null) return;
        var row = used[i] || 0; used[i] = row + 1;
        var x = 20 + Math.min(i, n) * cw + cw / 2, y = 96 + row * 26;
        G.svg("path", { d: "M" + x + " " + (y - 10) + "l-7 10h14z", fill: cols[name] }, s);
        var tt = G.svg("text", { x: x, y: y + 15, "text-anchor": "middle", style: "font:700 15px var(--mono);fill:" + cols[name] }, s); tt.textContent = name + "=" + i;
      });
      msg.innerHTML = "<b>Step " + k + " of " + (F.length - 1) + ".</b> " + G.esc(f.msg);
      msg.style.color = f.bad ? "var(--bad)" : "";
      if (f.d) {
        info.innerHTML = "<div>dict<b>{" + f.d.map(function (q) { return (typeof q[0] === "string" ? "'" + q[0] + "'" : q[0]) + ": " + q[1]; }).join(", ") + "}</b></div>";
      } else info.innerHTML = "";
    }
    draw();
  });
})();
