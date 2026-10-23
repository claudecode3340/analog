/* py1 · list indexing/slicing visualiser, and a "labels on boxes" assignment stepper */

/* ---------- 1. indexing and slicing ---------- */
G.widget("py1-slice", function (body, args) {
  var vals = args.values || [62, 75, 81, 70, 90, 55, 68];
  var name = args.name || "marks";
  var n = vals.length;
  var mode = args.mode || "slice";
  var st = { i: 2, start: 1, stop: 4, step: 1, s0: false, s1: false, s2: true };
  if (args.start != null) st.start = args.start; if (args.stop != null) st.stop = args.stop;

  var top = G.el("div"); top.style.cssText = "display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:6px"; body.appendChild(top);
  G.seg(top, [["index", "One item: " + name + "[i]"], ["slice", "A slice: " + name + "[start:stop:step]"]], mode, function (m) { mode = m; layout(); draw(); });
  var expr = G.el("div"); expr.style.cssText = "font:600 18px/1.4 var(--mono);margin:8px 0 2px;color:var(--ink);overflow-wrap:anywhere"; body.appendChild(expr);
  var narrow = (body.clientWidth || 700) < 520, W = narrow ? 400 : 720, H = 170, bw = Math.min(84, (W - 16) / n), x0 = (W - bw * n) / 2, by = 58, bh = 52;
  var svg = G.svg("svg", { viewBox: "0 0 " + W + " " + H, class: "wsvg", role: "img", "aria-label": "list boxes with positive and negative positions" }, body);
  var ctl = G.el("div"); ctl.style.cssText = "display:grid;gap:4px;grid-template-columns:repeat(auto-fit,minmax(min(100%,210px),1fr));margin-top:6px"; body.appendChild(ctl);
  var info = G.el("div", "readout"); body.appendChild(info);
  var note = G.el("p"); note.style.cssText = "font-size:15px;color:var(--ink2);margin:8px 0 0"; body.appendChild(note);

  function mk(label, key, emptyKey, min, max) {
    var box = G.el("div"); ctl.appendChild(box);
    var cb = null;
    G.slider(box, { label: label, min: min, max: max, step: 1, value: st[key], onChange: function (v) { st[key] = v; if (emptyKey) { st[emptyKey] = false; if (cb) cb.checked = false; } draw(); } });
    if (emptyKey) {
      var lab = G.el("label"); lab.style.cssText = "font-size:14px;color:var(--muted);display:flex;gap:6px;align-items:center;cursor:pointer";
      cb = document.createElement("input"); cb.type = "checkbox"; cb.checked = st[emptyKey];
      cb.onchange = function () { st[emptyKey] = cb.checked; draw(); };
      lab.appendChild(cb); lab.appendChild(document.createTextNode("leave it out (use the default)")); box.appendChild(lab);
    }
    return box;
  }
  var cI = mk("i", "i", null, -n - 1, n);
  var cA = mk("start", "start", "s0", -n, n);
  var cB = mk("stop", "stop", "s1", -n, n);
  var cC = mk("step", "step", "s2", -3, 3);
  function layout() { cI.style.display = mode === "index" ? "" : "none"; [cA, cB, cC].forEach(function (c) { c.style.display = mode === "slice" ? "" : "none"; }); }

  function sliceIdx() {
    var step = st.s2 ? 1 : st.step;
    if (step === 0) return { err: "ValueError: slice step cannot be zero" };
    var a, b;
    if (step > 0) {
      a = st.s0 ? 0 : st.start; b = st.s1 ? n : st.stop;
      if (a < 0) a += n; if (b < 0) b += n; a = Math.max(0, Math.min(n, a)); b = Math.max(0, Math.min(n, b));
    } else {
      a = st.s0 ? n - 1 : st.start; b = st.s1 ? -1 : st.stop;
      if (!st.s0 && a < 0) a += n; if (!st.s1 && b < 0) b += n;
      a = Math.max(-1, Math.min(n - 1, a)); if (!st.s1) b = Math.max(-1, Math.min(n - 1, b));
    }
    var out = [];
    for (var k = a; step > 0 ? k < b : k > b; k += step) out.push(k);
    return { idx: out, a: a, b: b, step: step };
  }
  function t(x, y, s, attrs) { var e = G.svg("text", Object.assign({ x: x, y: y, "text-anchor": "middle" }, attrs || {}), svg); e.textContent = s; return e; }
  function ord(k) { return k === 1 ? "1st" : k === 2 ? "2nd" : k === 3 ? "3rd" : k + "th"; }
  function draw() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var sel = [], res, txt, msg, r = null;
    if (mode === "index") {
      var i = st.i, j = i < 0 ? i + n : i;
      txt = name + "[" + i + "]";
      if (j < 0 || j >= n) { res = "IndexError: list index out of range"; msg = "A list of length " + n + " has positions 0 to " + (n - 1) + " (or −1 to −" + n + " counting from the end). Position " + i + " does not exist."; }
      else { sel = [j]; res = String(vals[j]); msg = i < 0 ? "Negative positions count from the end: " + i + " means position " + n + " + (" + i + ") = " + j + "." : "Position " + i + " is the " + ord(i + 1) + " box, because counting starts at 0."; }
    } else {
      r = sliceIdx();
      txt = name + "[" + (st.s0 ? "" : st.start) + ":" + (st.s1 ? "" : st.stop) + (st.s2 ? "" : ":" + st.step) + "]";
      if (r.err) { res = r.err; msg = "A step of 0 would never move, so Python refuses it."; }
      else {
        sel = r.idx; res = "[" + sel.map(function (k) { return vals[k]; }).join(", ") + "]";
        msg = r.step > 0 ? "Start at position " + r.a + ", take " + (r.step === 1 ? "every item" : "every " + ord(r.step) + " item") + ", and stop BEFORE position " + r.b + ". You get " + sel.length + " item" + (sel.length === 1 ? "" : "s") + "."
          : "A negative step walks backwards: start at position " + r.a + " and move left " + (-r.step) + " at a time until you pass " + (r.b < 0 ? "the left edge" : "position " + r.b) + ".";
        if (!sel.length) msg += " Nothing is between the fence posts, so the result is an empty list [] (not an error).";
      }
    }
    expr.innerHTML = txt + '  <span style="color:var(--muted)">→</span>  <span style="color:' + (/Error/.test(res) ? "var(--bad)" : "var(--accent)") + '">' + res + "</span>";
    vals.forEach(function (v, k) {
      var x = x0 + k * bw, on = sel.indexOf(k);
      G.svg("rect", { x: x + 3, y: by, width: bw - 6, height: bh, rx: 8, style: on >= 0 ? "fill:var(--accent-soft);stroke:var(--accent);stroke-width:2.5" : "fill:var(--surface);stroke:var(--line2);stroke-width:1.2" }, svg);
      t(x + bw / 2, by + 33, String(v), { style: "fill:var(--ink);font-size:" + (narrow ? 19 : 20) + "px;font-weight:" + (on >= 0 ? 700 : 400) });
      t(x + bw / 2, by - 12, String(k), { style: "fill:var(--tool);font:600 14px var(--mono)" });
      t(x + bw / 2, by + bh + 22, String(k - n), { style: "fill:var(--math);font:600 14px var(--mono)" });
      if (on >= 0 && sel.length > 1) {
        G.svg("circle", { cx: x + bw - 10, cy: by + 10, r: 9, style: "fill:var(--accent)" }, svg);
        t(x + bw - 10, by + 14, String(on + 1), { style: "fill:var(--surface);font-size:11px;font-weight:700" });
      }
    });
    if (r && !r.err && r.step > 0) {
      [[r.a, "start", "var(--good)"], [r.b, "stop", "var(--bad)"]].forEach(function (f, q) {
        var x = x0 + f[0] * bw;
        G.svg("line", { x1: x, x2: x, y1: by - 4, y2: by + bh + 4, style: "stroke:" + f[2] + ";stroke-width:3;" + (q ? "stroke-dasharray:5 3" : "") }, svg);
        t(x, H - 6, f[1] + " " + f[0], { style: "fill:" + f[2] + ";font-size:12.5px;font-weight:700" });
      });
    }
    info.innerHTML = "<div>len(" + name + ")<b>" + n + "</b></div><div>result<b style=\"font-size:15px\">" + res.replace(/</g, "&lt;") + "</b></div>";
    note.textContent = msg;
  }
  layout(); draw();
});

/* ---------- 2. names are labels on value boxes ---------- */
G.widget("py1-boxes", function (body, args) {
  var S = {
    numbers: {
      code: ["x = 5", "y = x", "x = x + 1", "print(x, y)"],
      steps: [
        { line: -1, names: {}, objs: {}, say: "Nothing exists yet. Press Next line to run the first line." },
        { line: 0, names: { x: "a" }, objs: { a: "5" }, say: "Python first makes the value 5 (a box), then ties the label x to it. Read '=' as 'gets', not 'equals': x gets 5." },
        { line: 1, names: { x: "a", y: "a" }, objs: { a: "5" }, say: "y = x does NOT copy anything. It ties a second label, y, to the same box. Both names now lead to 5." },
        { line: 2, names: { x: "b", y: "a" }, objs: { a: "5", b: "6" }, say: "The right side is worked out first: x + 1 is 5 + 1 = 6, a new box. Then the label x is moved onto 6. Nobody moved y." },
        { line: 3, names: { x: "b", y: "a" }, objs: { a: "5", b: "6" }, say: "Changing x never changes y: numbers can't be changed in place, so Python makes a new box instead.", out: "6 5" }
      ]
    },
    lists: {
      code: ["a = [62, 75]", "b = a", "b.append(81)", "print(a)", "c = a.copy()", "c.append(70)", "print(a, c)"],
      steps: [
        { line: -1, names: {}, objs: {}, say: "Lists behave differently from numbers, and this surprises everyone once. Press Next line." },
        { line: 0, names: { a: "p" }, objs: { p: "[62, 75]" }, say: "A list box is made, and the label a is tied to it." },
        { line: 1, names: { a: "p", b: "p" }, objs: { p: "[62, 75]" }, say: "As before, b = a ties a second label to the SAME list. There is still only one list." },
        { line: 2, names: { a: "p", b: "p" }, objs: { p: "[62, 75, 81]" }, say: "append changes the list box itself (lists can be changed in place). Both labels lead to this one box..." },
        { line: 3, names: { a: "p", b: "p" }, objs: { p: "[62, 75, 81]" }, say: "...so printing a shows 81 too, even though we only 'touched' b.", out: "[62, 75, 81]" },
        { line: 4, names: { a: "p", b: "p", c: "q" }, objs: { p: "[62, 75, 81]", q: "[62, 75, 81]" }, say: "a.copy() builds a NEW box with the same contents. The label c goes on the new box." },
        { line: 5, names: { a: "p", b: "p", c: "q" }, objs: { p: "[62, 75, 81]", q: "[62, 75, 81, 70]" }, say: "Appending to c changes only the copy." },
        { line: 6, names: { a: "p", b: "p", c: "q" }, objs: { p: "[62, 75, 81]", q: "[62, 75, 81, 70]" }, say: "Two different lists. Rule: = never copies; use .copy() when you want a separate list.", out: "[62, 75, 81] [62, 75, 81, 70]" }
      ]
    },
    total: {
      code: ["marks = [62, 75, 81]", "total = 0", "for m in marks:", "    total = total + m", "mean = total / len(marks)"],
      steps: [
        { line: -1, names: {}, objs: {}, say: "A running total, the most common pattern in ML code (sums of errors, of losses...). Press Next line." },
        { line: 0, names: { marks: "L" }, objs: { L: "[62, 75, 81]" }, say: "The list of marks gets the label marks." },
        { line: 1, names: { marks: "L", total: "z" }, objs: { L: "[62, 75, 81]", z: "0" }, say: "total starts at 0: nothing has been added yet." },
        { line: 2, names: { marks: "L", total: "z", m: "a" }, objs: { L: "[62, 75, 81]", z: "0", a: "62" }, say: "First trip round the loop: the label m goes on the first mark, 62." },
        { line: 3, names: { marks: "L", total: "b", m: "a" }, objs: { L: "[62, 75, 81]", b: "62", a: "62" }, say: "Right side first: total + m = 0 + 62 = 62. Then total moves to 62." },
        { line: 2, names: { marks: "L", total: "b", m: "c" }, objs: { L: "[62, 75, 81]", b: "62", c: "75" }, say: "Second trip: m moves to 75." },
        { line: 3, names: { marks: "L", total: "d", m: "c" }, objs: { L: "[62, 75, 81]", d: "137", c: "75" }, say: "total + m = 62 + 75 = 137. total moves to 137." },
        { line: 2, names: { marks: "L", total: "d", m: "e" }, objs: { L: "[62, 75, 81]", d: "137", e: "81" }, say: "Third and last trip: m moves to 81." },
        { line: 3, names: { marks: "L", total: "f", m: "e" }, objs: { L: "[62, 75, 81]", f: "218", e: "81" }, say: "total + m = 137 + 81 = 218. The list is used up, so the loop ends." },
        { line: 4, names: { marks: "L", total: "f", m: "e", mean: "g" }, objs: { L: "[62, 75, 81]", f: "218", e: "81", g: "72.666..." }, say: "218 / 3 = 72.666... Notice m still exists after the loop, labelling the last mark." }
      ]
    }
  };
  var which = args.start || "numbers", k = 0;
  var top = G.el("div"); top.style.cssText = "display:flex;flex-wrap:wrap;gap:8px;align-items:center"; body.appendChild(top);
  G.seg(top, [["numbers", "Numbers"], ["lists", "Lists (the surprise)"], ["total", "A running total"]], which, function (v) { which = v; k = 0; draw(); });
  var grid = G.el("div"); grid.style.cssText = "display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));margin-top:10px;align-items:start"; body.appendChild(grid);
  var codeBox = G.el("div"); codeBox.style.cssText = "background:var(--code-bg);border:1px solid var(--line);border-radius:10px;padding:8px 0;font:14px/1.7 var(--mono);color:var(--code-ink);overflow-x:auto"; grid.appendChild(codeBox);
  var pic = G.el("div"); grid.appendChild(pic);
  var say = G.el("p"); say.style.cssText = "margin:10px 0 4px;font-size:15.5px;color:var(--ink2);min-height:3em"; body.appendChild(say);
  var outp = G.el("div"); outp.style.cssText = "font:14px var(--mono);color:var(--muted)"; body.appendChild(outp);
  var bb = G.el("div"); bb.style.cssText = "display:flex;gap:8px;margin-top:8px;flex-wrap:wrap"; body.appendChild(bb);
  G.button(bb, "◀ Back", function () { if (k > 0) { k--; draw(); } });
  var nb = G.button(bb, "Next line ▶", function () { if (k < S[which].steps.length - 1) { k++; draw(); } }, "run");
  G.button(bb, "Restart", function () { k = 0; draw(); });
  function draw() {
    var sc = S[which], s = sc.steps[k];
    codeBox.innerHTML = sc.code.map(function (c, i) { var on = i === s.line; return '<div style="padding:0 14px;white-space:pre;' + (on ? "background:var(--hl1);font-weight:700" : "") + '">' + (on ? "▶ " : "  ") + c.replace(/</g, "&lt;") + "</div>"; }).join("");
    say.textContent = "Step " + k + " of " + (sc.steps.length - 1) + ". " + s.say;
    outp.innerHTML = s.out ? "printed: <b style=\"color:var(--ink)\">" + s.out + "</b>" : "";
    nb.disabled = k >= sc.steps.length - 1;
    pic.innerHTML = "";
    var names = Object.keys(s.names), objs = Object.keys(s.objs);
    var rowH = 50, H = Math.max(2, Math.max(names.length, objs.length)) * rowH + 40, W = 400;
    var svg = G.svg("svg", { viewBox: "0 0 " + W + " " + H, class: "wsvg", role: "img", "aria-label": "names on the left pointing to values on the right" }, pic);
    var lab = function (x, y, txt, st) { var e = G.svg("text", { x: x, y: y, style: st }, svg); e.textContent = txt; return e; };
    lab(20, 18, "names (labels)", "fill:var(--muted);font-size:12.5px;font-weight:700");
    lab(200, 18, "values (boxes)", "fill:var(--muted);font-size:12.5px;font-weight:700");
    var oy = {};
    objs.forEach(function (o, i) {
      var y = 34 + i * rowH, txt = s.objs[o], w = Math.max(54, 10 * txt.length + 24);
      oy[o] = y + 18;
      G.svg("rect", { x: 200, y: y, width: Math.min(w, 196), height: 36, rx: 7, style: "fill:var(--surface);stroke:var(--isl);stroke-width:2" }, svg);
      lab(210, y + 24, txt, "fill:var(--ink);font:600 15px var(--mono)");
    });
    names.forEach(function (nm, i) {
      var y = 34 + i * rowH, ty = oy[s.names[nm]];
      G.svg("rect", { x: 14, y: y + 4, width: 78, height: 28, rx: 14, style: "fill:var(--tool-soft);stroke:var(--tool);stroke-width:1.5" }, svg);
      lab(53, y + 23, nm, "fill:var(--tool);font:700 14px var(--mono);text-anchor:middle");
      G.svg("path", { d: "M92 " + (y + 18) + " C140 " + (y + 18) + " 150 " + ty + " 196 " + ty, style: "fill:none;stroke:var(--tool);stroke-width:1.8" }, svg);
      G.svg("circle", { cx: 196, cy: ty, r: 3.5, style: "fill:var(--tool)" }, svg);
    });
    if (!names.length) lab(20, 60, "(empty)", "fill:var(--faint);font-size:14px");
  }
  draw();
});
