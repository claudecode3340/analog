/* ML Foundations guide · runtime
   Rail + progress + lesson map · theme · search · Python cells (Pyodide worker) · exercises ·
   predictions · quizzes · book problems · flashcards (FSRS-6) · widgets · glossary · notebooks. */
(function () {
  "use strict";
  var LS = "mlg1.";
  function ld(k, d) { try { var v = localStorage.getItem(LS + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } }
  function sv(k, v) { try { localStorage.setItem(LS + k, JSON.stringify(v)); } catch (e) {} }
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function jsonScript(id, d) { var s = document.getElementById(id); if (!s) return d; try { return JSON.parse(s.textContent); } catch (e) { return d; } }
  function today() { return Math.floor((Date.now() - new Date().getTimezoneOffset() * 60000) / 864e5); }

  /* ================= G: shared helpers for widgets ================= */
  var SVGNS = "http://www.w3.org/2000/svg";
  var G = window.G = {
    el: el, $: $, $$: $$, esc: esc, W: {},
    widget: function (name, fn) { G.W[name] = fn; },
    svg: function (tag, attrs, parent) { var e = document.createElementNS(SVGNS, tag); for (var k in attrs || {}) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; },
    rng: function (seed) { var a = (seed >>> 0) || 1; return function () { a = (a + 0x6D2B79F5) >>> 0; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; },
    randn: function (r) { var u = 1 - r(), v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); },
    css: function (v) { return getComputedStyle(document.documentElement).getPropertyValue(v).trim(); },
    tex: function (s, display) { try { return window.katex ? katex.renderToString(s, { displayMode: !!display, throwOnError: false }) : esc(s); } catch (e) { return esc(s); } },
    fmt: function (x, d) { if (!isFinite(x)) return String(x); d = d == null ? 3 : d; var v = Number(x.toFixed(d)); return (Object.is(v, -0) ? 0 : v).toString(); },
    slider: function (parent, o) {
      var w = el("label", "ctrl"); w.innerHTML = '<span>' + o.label + '</span>';
      var i = el("input"); i.type = "range"; i.min = o.min; i.max = o.max; i.step = o.step || 1; i.value = o.value;
      var out = el("output"); var f = o.fmt || function (v) { return v; };
      out.textContent = f(+i.value); w.appendChild(i); w.appendChild(out); parent.appendChild(w);
      i.addEventListener("input", function () { out.textContent = f(+i.value); o.onChange && o.onChange(+i.value); });
      return { input: i, get: function () { return +i.value; }, set: function (v) { i.value = v; out.textContent = f(+v); } };
    },
    seg: function (parent, opts, val, onChange) {
      var s = el("div", "seg"); opts.forEach(function (o) { var b = el("button", o[0] === val ? "on" : "", o[1]); b.type = "button"; b.onclick = function () { $$("button", s).forEach(function (x) { x.classList.remove("on"); }); b.classList.add("on"); onChange(o[0]); }; s.appendChild(b); }); parent.appendChild(s); return s;
    },
    button: function (parent, label, fn, cls) { var b = el("button", "cbtn " + (cls || ""), label); b.type = "button"; b.onclick = fn; parent.appendChild(b); return b; },
    /* plot: a simple 2-D axes in SVG. o = {w,h,x:[a,b],y:[a,b],xlabel,ylabel,xticks,yticks,pad} */
    plot: function (parent, o) {
      var W = o.w || 640, H = o.h || 380, P = o.pad || { l: 54, r: 16, t: 14, b: 44 };
      var s = G.svg("svg", { viewBox: "0 0 " + W + " " + H, class: "wsvg", role: "img", "aria-label": o.label || "chart" }, parent);
      var X = function (v) { return P.l + (v - o.x[0]) / (o.x[1] - o.x[0]) * (W - P.l - P.r); };
      var Y = function (v) { return H - P.b - (v - o.y[0]) / (o.y[1] - o.y[0]) * (H - P.t - P.b); };
      var ticks = function (a, b, n) { var st = Math.pow(10, Math.floor(Math.log10((b - a) / n))); var m = [1, 2, 5, 10].find(function (k) { return (b - a) / (st * k) <= n; }) * st; var r = []; for (var v = Math.ceil(a / m) * m; v <= b + 1e-9; v += m) r.push(+v.toFixed(10)); return r; };
      var g = G.svg("g", {}, s);
      (o.xticks || ticks(o.x[0], o.x[1], 7)).forEach(function (t) { G.svg("line", { x1: X(t), x2: X(t), y1: P.t, y2: H - P.b, class: "grid" }, g); var tx = G.svg("text", { x: X(t), y: H - P.b + 17, "text-anchor": "middle", class: "tick" }, g); tx.textContent = G.fmt(t, 3); });
      (o.yticks || ticks(o.y[0], o.y[1], 6)).forEach(function (t) { G.svg("line", { x1: P.l, x2: W - P.r, y1: Y(t), y2: Y(t), class: "grid" }, g); var tx = G.svg("text", { x: P.l - 8, y: Y(t) + 4, "text-anchor": "end", class: "tick" }, g); tx.textContent = G.fmt(t, 3); });
      G.svg("line", { x1: P.l, x2: W - P.r, y1: H - P.b, y2: H - P.b, class: "ax" }, g); G.svg("line", { x1: P.l, x2: P.l, y1: P.t, y2: H - P.b, class: "ax" }, g);
      if (o.xlabel) { var xl = G.svg("text", { x: (P.l + W - P.r) / 2, y: H - 6, "text-anchor": "middle", class: "albl" }, g); xl.textContent = o.xlabel; }
      if (o.ylabel) { var yl = G.svg("text", { x: 14, y: (P.t + H - P.b) / 2, "text-anchor": "middle", class: "albl", transform: "rotate(-90 14 " + (P.t + H - P.b) / 2 + ")" }, g); yl.textContent = o.ylabel; }
      var layer = G.svg("g", {}, s);
      return { svg: s, layer: layer, X: X, Y: Y, W: W, H: H, P: P,
        clear: function () { while (layer.firstChild) layer.removeChild(layer.firstChild); },
        line: function (pts, attrs) { var d = pts.map(function (p, i) { return (i ? "L" : "M") + X(p[0]).toFixed(1) + " " + Y(p[1]).toFixed(1); }).join(""); return G.svg("path", Object.assign({ d: d, fill: "none", stroke: "var(--accent)", "stroke-width": 2.2 }, attrs || {}), layer); },
        dot: function (x, y, attrs) { return G.svg("circle", Object.assign({ cx: X(x), cy: Y(y), r: 4, fill: "var(--accent)" }, attrs || {}), layer); },
        text: function (x, y, t, attrs) { var e = G.svg("text", Object.assign({ x: X(x), y: Y(y), class: "tick" }, attrs || {}), layer); e.textContent = t; return e; }
      };
    }
  };

  /* ================= state ================= */
  var S = {
    done: ld("done", {}), started: ld("started", {}), solved: ld("solved", {}), probs: ld("probs", {}),
    quiz: ld("quiz", {}), pred: ld("pred", {}), checks: ld("checks", {}), cards: ld("cards", {}), code: ld("code", {})
  };
  function save(k) { sv(k, S[k]); }
  var LESSONS = [];

  /* ================= theme ================= */
  var theme = ld("theme", null); if (theme) document.documentElement.setAttribute("data-theme", theme);
  function toggleTheme() {
    var dark = document.documentElement.getAttribute("data-theme") === "dark" || (!document.documentElement.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
    var nx = dark ? "light" : "dark"; document.documentElement.setAttribute("data-theme", nx); sv("theme", nx);
    document.dispatchEvent(new CustomEvent("guide:theme"));
  }

  /* ================= rail, progress, lesson map ================= */
  var KIND = { tool: "Python & tools", math: "Maths", isl: "ISLP", udl: "Prince · UDL", proj: "Project", start: "Start here", review: "Review" };
  function buildRail() {
    var toc = $("#toc"); toc.innerHTML = "";
    var mo = null, wk = null;
    LESSONS.forEach(function (L) {
      if (L.month !== mo) { mo = L.month; wk = null; var mh = el("div", "mh", '<span>' + L.monthName + '</span><em class="mc" data-m="' + mo + '"></em>'); toc.appendChild(mh); }
      if (L.week && L.week !== wk) { wk = L.week; toc.appendChild(el("div", "wh", "Week " + wk)); }
      var a = el("a", "k-" + L.kind, '<span class="d"></span><span>' + esc(L.short) + '</span>'); a.href = "#" + L.id; a.dataset.id = L.id; a.title = L.title; L.link = a;
      a.addEventListener("click", function () { document.body.classList.remove("railopen"); });
      toc.appendChild(a);
    });
    var lm = $("#lmap"); lm.innerHTML = "";
    var months = {}; LESSONS.forEach(function (L) { (months[L.month] = months[L.month] || []).push(L); });
    Object.keys(months).forEach(function (m) { var g = el("div", "mg"); months[m].forEach(function (L) { var i = el("i", "k-" + L.kind); i.title = L.title; L.cell = i; g.appendChild(i); }); lm.appendChild(g); });
    lm.title = "Every lesson as a square: faint = not started, half = started, full colour = done. Click to open the menu.";
    lm.onclick = function () { document.body.classList.toggle("railopen"); };
    renderProgress();
  }
  function lessonState(L) { return S.done[L.id] ? "dn" : (S.started[L.id] ? "st" : ""); }
  function renderProgress() {
    var learn = LESSONS.filter(function (L) { return L.kind !== "review"; });
    var n = learn.filter(function (L) { return S.done[L.id]; }).length;
    $("#rprog-n").textContent = n; $("#rprog-t").textContent = learn.length;
    $("#rprog-bar").style.width = (100 * n / Math.max(1, learn.length)).toFixed(1) + "%";
    LESSONS.forEach(function (L) {
      var st = lessonState(L);
      L.link.classList.toggle("done", st === "dn"); L.link.classList.toggle("started", st === "st");
      L.cell.className = "k-" + L.kind + (st ? " " + st : "") + (curId === L.id ? " cur" : "");
    });
    $$(".mc").forEach(function (e) { var m = e.dataset.m; var ls = learn.filter(function (L) { return String(L.month) === m; }); if (!ls.length) { e.textContent = ""; return; } e.textContent = ls.filter(function (L) { return S.done[L.id]; }).length + "/" + ls.length; });
    $$(".monthcards a").forEach(function (a) { var m = a.dataset.m; var ls = learn.filter(function (L) { return String(L.month) === m; }); var d = ls.filter(function (L) { return S.done[L.id]; }).length; var b = $("i", a); if (b) b.style.width = (100 * d / Math.max(1, ls.length)) + "%"; var c = $(".cnt", a); if (c) c.textContent = d + " of " + ls.length + " lessons done"; });
    $("#due-n").textContent = deckDue().length;
  }
  function markStarted(id) { if (!id || S.started[id]) return; S.started[id] = 1; save("started"); renderProgress(); }
  var curId = null;
  function scrollSpy() {
    // Works out the current lesson from the scroll position (robust to jumps and to content above growing).
    var secs = $$("section.lesson"), ticking = false;
    function setCur(id) {
      if (curId === id) return; curId = id;
      LESSONS.forEach(function (L) { L.link.classList.toggle("on", L.id === id); });
      var L = LESSONS.find(function (x) { return x.id === id; });
      $("#where-t").textContent = L ? L.title : ""; $("#where-k").textContent = L ? (L.monthName + (L.week ? " · Week " + L.week : "")) : "";
      if (L && L.link.scrollIntoViewIfNeeded) L.link.scrollIntoViewIfNeeded(false);
      renderProgress();
    }
    function check() {
      ticking = false; var y = innerHeight * 0.45, id = null;
      for (var i = 0; i < secs.length; i++) { var r = secs[i].getBoundingClientRect(); if (r.top <= y && r.bottom > y) { id = secs[i].id; break; } }
      if (id) setCur(id);
    }
    function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(check); } }
    addEventListener("scroll", onScroll, { passive: true }); addEventListener("resize", onScroll);
    if (window.ResizeObserver) new ResizeObserver(onScroll).observe(document.body);
    check();
  }

  /* ================= code editor (textarea + highlight overlay) ================= */
  var KW = /\b(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b/;
  var BI = /\b(print|len|range|enumerate|zip|sum|min|max|abs|round|sorted|list|dict|set|tuple|int|float|str|bool|type|isinstance|map|filter|any|all|open|input|super|reversed)\b/;
  function highlight(src) {
    var out = "", re = /(#[^\n]*)|("""[\s\S]*?"""|'''[\s\S]*?'''|f?"(?:\\.|[^"\\\n])*"|f?'(?:\\.|[^'\\\n])*')|(\b\d+\.?\d*(?:e[+-]?\d+)?\b)|([A-Za-z_]\w*)|([\s\S])/g, m;
    while ((m = re.exec(src))) {
      if (m[1]) out += '<span class="tk-com">' + esc(m[1]) + "</span>";
      else if (m[2]) out += '<span class="tk-str">' + esc(m[2]) + "</span>";
      else if (m[3]) out += '<span class="tk-num">' + m[3] + "</span>";
      else if (m[4]) { var w = m[4]; if (KW.test(w) && w.match(KW)[0] === w) out += '<span class="tk-kw">' + w + "</span>"; else if (BI.test(w) && w.match(BI)[0] === w) out += '<span class="tk-bi">' + w + "</span>"; else if (src.charAt(re.lastIndex) === "(") out += '<span class="tk-fn">' + w + "</span>"; else out += w; }
      else out += esc(m[5]);
    }
    return out + "\n";
  }
  function editor(parent, code, opts) {
    opts = opts || {};
    var wrap = el("div", "code" + (opts.readOnly ? " ro" : ""));
    var pre = el("pre", "hl"); var ta = el("textarea"); ta.spellcheck = false; ta.value = code; ta.setAttribute("autocapitalize", "off"); ta.setAttribute("autocomplete", "off");
    if (opts.readOnly) ta.readOnly = true;
    ta.setAttribute("aria-label", opts.label || "Python code");
    wrap.appendChild(pre); wrap.appendChild(ta); parent.appendChild(wrap);
    function sync() { pre.innerHTML = highlight(ta.value); ta.style.height = "auto"; ta.style.height = (ta.scrollHeight + 2) + "px"; pre.scrollLeft = ta.scrollLeft; }
    ta.addEventListener("input", function () { sync(); opts.onChange && opts.onChange(ta.value); });
    ta.addEventListener("scroll", function () { pre.scrollLeft = ta.scrollLeft; pre.scrollTop = ta.scrollTop; });
    ta.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && (e.shiftKey || e.ctrlKey || e.metaKey)) { e.preventDefault(); opts.onRun && opts.onRun(); return; }
      if (opts.readOnly) return;
      if (e.key === "Tab") { e.preventDefault(); var s = ta.selectionStart; ta.setRangeText("    ", s, ta.selectionEnd, "end"); sync(); opts.onChange && opts.onChange(ta.value); }
      else if (e.key === "Enter") {
        var s2 = ta.selectionStart, line = ta.value.slice(0, s2).split("\n").pop(), ind = (line.match(/^\s*/) || [""])[0];
        if (/:\s*$/.test(line)) ind += "    ";
        e.preventDefault(); ta.setRangeText("\n" + ind, s2, ta.selectionEnd, "end"); sync(); opts.onChange && opts.onChange(ta.value);
      }
    });
    requestAnimationFrame(sync); setTimeout(sync, 60);
    return { ta: ta, get: function () { return ta.value; }, set: function (v) { ta.value = v; sync(); } };
  }

  /* ================= Python worker ================= */
  var PY = { worker: null, ready: false, state: "idle", queue: {}, n: 0, timer: null };
  function pyStatus(s, msg) { var e = $("#pystat"); e.className = "pystat " + s; $("span", e).textContent = msg; PY.state = s; }
  function pyStart() {
    if (PY.worker) return;
    var src = $("#pyworker-src").textContent;
    PY.worker = new Worker(URL.createObjectURL(new Blob([src], { type: "text/javascript" })));
    PY.worker.onmessage = function (ev) {
      var m = ev.data;
      if (m.type === "status") { pyStatus(m.s, m.msg); if (m.s === "ready") PY.ready = true; }
      else if (m.type === "result") { clearTimeout(PY.timer); var cb = PY.queue[m.id]; delete PY.queue[m.id]; cb && cb(m.res); }
    };
    var files = jsonScript("pyfiles", {}), zips = jsonScript("pyzips", {});
    PY.worker.postMessage({ type: "init", prelude: $("#prelude-src").textContent, files: files, zips: zips });
  }
  function pyRun(code, ns, opts, cb) {
    pyStart(); var id = ++PY.n; PY.queue[id] = cb;
    PY.worker.postMessage({ type: "run", id: id, ns: ns, code: code, check: opts.check || null, expectError: opts.expectError || null });
    clearTimeout(PY.timer);
    PY.timer = setTimeout(function watchdog() {
      if (!PY.queue[id]) return;
      if (!PY.ready) { PY.timer = setTimeout(watchdog, 90000); return; }
      PY.worker.terminate(); PY.worker = null; PY.ready = false;
      var q = PY.queue; PY.queue = {};
      Object.keys(q).forEach(function (k) { q[k]({ status: "error", outputs: [], etype: "Timeout", error: "Stopped after 60 seconds.", friendly: "This cell ran for over a minute, so Python was restarted (usually an endless loop). Fix the code, then re-run the cells above this one, top to bottom, because the restart wiped their results." }); });
      pyStatus("idle", "Python restarted");
    }, PY.ready ? 60000 : 180000);
  }
  function renderOut(box, res, opts) {
    box.innerHTML = ""; opts = opts || {};
    if (opts.ref) box.appendChild(el("div", "tag", "Reference output · press Run to run it yourself"));
    if (res.status === "expected") box.appendChild(el("div", "expected", "<b>✓ This error is the point of this cell.</b> Nothing is broken. Read the last line of the message below."));
    (res.outputs || []).forEach(function (o) {
      if (o.t === "text") { var p = el("pre"); p.textContent = o.v; box.appendChild(p); }
      else if (o.t === "stderr") { var q = el("pre", "err"); q.textContent = o.v; box.appendChild(q); }
      else if (o.t === "html") { var d = el("div"); d.innerHTML = o.v; box.appendChild(d); }
      else if (o.t === "img") { var im = el("img"); im.src = (o.v.indexOf("data:") === 0 ? "" : "data:image/png;base64,") + o.v; im.alt = "plot output"; box.appendChild(im); }
    });
    if (res.status === "error" || res.status === "expected") {
      var pe = el("pre", res.status === "error" ? "err" : ""); pe.textContent = res.error; box.appendChild(pe);
      if (res.status === "error" && res.friendly) box.appendChild(el("div", "friendly", "<b>What this means:</b> " + esc(res.friendly)));
      if (res.status === "error" && res.etype === "NameError" && opts.runAbove) { var b = el("button", "cbtn", "Run all cells above, then this one"); b.onclick = opts.runAbove; box.appendChild(b); }
    }
  }
  var OUTS = {};
  function lessonOf(node) { var s = node.closest("section.lesson"); return s ? s.id : "main"; }

  function initCell(div) {
    var id = div.id, ns = lessonOf(div), mode = div.dataset.mode || "run";
    var src = $("pre.src", div); var orig = src.textContent.replace(/^\n/, "").replace(/\s+$/, "");
    var note = $(".pynote", div);
    div.classList.add(mode);
    var ph = el("div", "ph"); var lab = el("span", "lab", div.dataset.label || (mode === "setup" ? "Setup for this lesson · run me first" : mode === "local" ? "Run this on your Mac (Jupyter) · PyTorch" : "Python · edit and run"));
    ph.appendChild(lab);
    var codeHost = el("div"); src.replaceWith(codeHost);
    var ed = editor(codeHost, S.code[id] != null ? S.code[id] : orig, { onRun: run, onChange: function (v) { S.code[id] = v; save("code"); } });
    var out = el("div", "out");
    div.insertBefore(ph, div.firstChild);
    if (note) div.appendChild(note);
    div.insertBefore(out, note || null);
    var runB = null;
    if (mode !== "local") runB = G.button(ph, "▶ Run", run, "run");
    G.button(ph, "Copy", function () { try { navigator.clipboard.writeText(ed.get()); } catch (e) {} });
    G.button(ph, "Reset", function () { ed.set(orig); delete S.code[id]; save("code"); });
    if (OUTS[id]) renderOut(out, OUTS[id], { ref: true });
    function run(cb) {
      if (div.dataset.gated === "1") { var pr = div.previousElementSibling; pr && pr.scrollIntoView({ block: "center", behavior: "smooth" }); pr && pr.classList.add("nudge"); return; }
      if (mode === "local") return;
      markStarted(ns);
      if (runB) { runB.disabled = true; runB.textContent = "Running…"; }
      out.innerHTML = '<span class="tag">' + (PY.ready ? "Running…" : "Starting Python (first run takes ~15 s)…") + "</span>";
      pyRun(ed.get(), ns, { expectError: div.dataset.error || null }, function (res) {
        if (runB) { runB.disabled = false; runB.textContent = "▶ Run"; }
        renderOut(out, res, { runAbove: function () { runAbove(div); } });
        typeof cb === "function" && cb(res);
      });
    }
    div._run = run;
    if (runB) runB.title = "Run (Shift+Enter)";
  }
  function runAbove(div) {
    var sec = div.closest("section.lesson"); var cells = $$(".py", sec).filter(function (c) { return c.dataset.mode !== "local"; });
    var idx = cells.indexOf(div); var list = cells.slice(0, idx + 1);
    (function next(i) { if (i >= list.length) return; list[i]._run(function () { next(i + 1); }); })(0);
  }

  /* ================= predictions ================= */
  function initPredict(p) {
    var cell = p.nextElementSibling; var gate = cell && (cell.classList.contains("py") || cell.classList.contains("widget"));
    var pid = (cell && cell.id ? cell.id : "p") + "-pred";
    p.insertBefore(el("div", "pt", "Predict first"), p.firstChild);
    var why = $(".why", p); var correct = +p.dataset.correct;
    var opts = $$(".opts > li", p);
    var tries = 0;
    function unlock() { if (gate) { cell.dataset.gated = "0"; cell.classList.remove("locked"); } }
    if (gate) cell.dataset.gated = S.pred[pid] ? "0" : "1";
    opts.forEach(function (li, i) {
      var b = el("button", "opt", '<span class="l">' + "ABCDEF"[i] + "</span><span>" + li.innerHTML + "</span>"); b.type = "button"; li.innerHTML = ""; li.appendChild(b);
      b.onclick = function () {
        tries++;
        if (i + 1 === correct) { b.classList.add("right"); finish(tries === 1); }
        else { b.classList.add("wrong"); b.disabled = true; if (tries >= 2) { opts[correct - 1].firstChild.classList.add("right"); finish(false); } }
      };
    });
    function finish(first) { opts.forEach(function (li) { li.firstChild.disabled = true; }); why && why.classList.add("show"); S.pred[pid] = first ? 1 : 2; save("pred"); unlock(); }
    if (S.pred[pid]) { opts.forEach(function (li, i) { li.firstChild.disabled = true; if (i + 1 === correct) li.firstChild.classList.add("right"); }); why && why.classList.add("show"); }
    else if (gate) { var sk = el("button", "skip", "Skip the prediction"); sk.type = "button"; sk.onclick = function () { S.pred[pid] = 3; save("pred"); why && why.classList.add("show"); unlock(); sk.remove(); }; p.appendChild(sk); }
  }

  /* ================= exercises ================= */
  function initEx(div) {
    var id = div.id, ns = lessonOf(div);
    var task = $(".task", div), src = $("pre.src", div), check = $("pre.check", div), sol = $("pre.solution", div), exp = $(".explain", div);
    var hints = $$(".hint", div);
    var orig = src.textContent.replace(/^\n/, "").replace(/\s+$/, ""), solTxt = sol ? sol.textContent.replace(/^\n/, "").replace(/\s+$/, "") : "";
    var ph = el("div", "ph", '<span class="lab">Your turn · ' + esc(div.dataset.title || "write the code") + "</span>");
    div.insertBefore(ph, div.firstChild);
    var host = el("div"); src.replaceWith(host);
    var ed = editor(host, S.code[id] != null ? S.code[id] : orig, { onRun: doCheck, onChange: function (v) { S.code[id] = v; save("code"); } });
    var out = el("div", "out"); host.after(out);
    var bar = el("div", "ebar"); out.after(bar);
    hints.forEach(function (h, i) { h.insertAdjacentHTML("afterbegin", '<b class="hn">Hint ' + (i + 1) + "</b>"); bar.after(h); });
    var lastH = hints.length ? hints[hints.length - 1] : bar;
    var solw = el("div", "solwrap");
    if (sol) { solw.appendChild(el("div", "sl", "Solution")); var sh = el("div"); solw.appendChild(sh); editor(sh, solTxt, { readOnly: true, label: "solution" }); sol.remove(); if (exp) solw.appendChild(exp); }
    lastH.after(solw);
    var chk = G.button(bar, "✓ Check", doCheck, "check");
    var shown = 0, hb = null;
    if (hints.length) hb = G.button(bar, "Hint (" + hints.length + ")", function () { if (shown < hints.length) { hints[shown].classList.add("show"); shown++; } hb.textContent = shown < hints.length ? "Next hint (" + (hints.length - shown) + " left)" : "All hints shown"; if (shown >= hints.length) hb.disabled = true; });
    if (sol) G.button(bar, "Show solution", function () { solw.classList.toggle("show"); });
    G.button(bar, "Reset", function () { ed.set(orig); delete S.code[id]; save("code"); });
    var st = el("span", "status", S.solved[id] ? "✓ Solved" : "Not checked yet"); bar.appendChild(st);
    if (S.solved[id]) div.classList.add("solved");
    if (OUTS[id + ":starter"] && !S.code[id]) renderOut(out, OUTS[id + ":starter"], { ref: true });
    function doCheck() {
      markStarted(ns); chk.disabled = true; chk.textContent = "Checking…";
      out.innerHTML = '<span class="tag">' + (PY.ready ? "Running your code and the tests…" : "Starting Python (first run takes ~15 s)…") + "</span>";
      pyRun(ed.get(), ns, { check: check ? check.textContent : null }, function (res) {
        chk.disabled = false; chk.textContent = "✓ Check";
        renderOut(out, res, { runAbove: function () { runAbove(div); } });
        if (res.status === "ok") { out.insertBefore(el("div", "ok", "✓ All tests passed."), out.firstChild); S.solved[id] = 1; save("solved"); div.classList.add("solved"); st.textContent = "✓ Solved"; }
        else if (res.status === "fail") { var f = el("div", "friendly", "<b>Not yet:</b> " + esc(res.fail)); out.insertBefore(f, out.firstChild); st.textContent = "Not yet"; }
      });
    }
    div._run = doCheck;
  }

  /* ================= book problems (layered answers) ================= */
  function initProb(div) {
    var id = div.id;
    var h = el("div", "prh", '<span class="src">' + esc(div.dataset.src || "Exercise") + '</span><span class="tt">' + (div.dataset.title || "") + "</span>");
    var b = el("button", "done", S.probs[id] ? "✓ Solved" : "Mark solved"); b.type = "button"; h.appendChild(b);
    div.insertBefore(h, div.firstChild);
    if (S.probs[id]) div.classList.add("solved");
    b.onclick = function () { S.probs[id] = S.probs[id] ? 0 : 1; if (!S.probs[id]) delete S.probs[id]; save("probs"); div.classList.toggle("solved", !!S.probs[id]); b.textContent = S.probs[id] ? "✓ Solved" : "Mark solved"; markStarted(lessonOf(div)); };
    var ai = $(".ansin", div);
    if (ai) {
      var box = el("div", "ansbox", '<span>Your answer' + (ai.dataset.unit ? " (" + esc(ai.dataset.unit) + ")" : "") + ':</span>');
      var inp = el("input"); inp.inputMode = "decimal"; box.appendChild(inp);
      var cb = el("button", "cbtn", "Check"); box.appendChild(cb); var fb = el("span", "fb"); box.appendChild(fb);
      ai.replaceWith(box);
      cb.onclick = function () { var v = parseFloat(inp.value), a = parseFloat(ai.dataset.answer), tol = parseFloat(ai.dataset.tol || "0.01"); if (!isFinite(v)) { fb.className = "fb no"; fb.textContent = "Type a number."; return; } var ok = Math.abs(v - a) <= Math.max(tol * Math.abs(a), tol); fb.className = "fb " + (ok ? "ok" : "no"); fb.textContent = ok ? "✓ Correct. Now compare your working with the full solution." : "Not yet. Open the hint, or check each step."; };
    }
    $$("details", div).forEach(function (d) { d.addEventListener("toggle", function () { if (d.open) { markStarted(lessonOf(div)); renderMathIn(d); } }); });
  }

  /* ================= quizzes ================= */
  function initQuiz(qz) {
    var qs = $$(".q", qz); var lid = lessonOf(qz);
    var head = el("div", "qt", 'Test yourself<span class="sc"></span>'); qz.insertBefore(head, qz.firstChild);
    function score() { var a = 0, r = 0; qs.forEach(function (q) { var k = S.quiz[q.dataset.qid]; if (k) { a++; if (k === 1) r++; } }); $(".sc", head).textContent = a + " / " + qs.length + " answered · " + r + " right first time"; }
    qs.forEach(function (q, qi) {
      var qid = q.dataset.qid = lid + ":q" + qi;
      var type = q.dataset.type || "mcq", why = $(".why", q);
      if (type === "mcq") {
        var correct = +q.dataset.correct, opts = $$(".opts > li", q), tries = 0;
        opts.forEach(function (li, i) {
          var b = el("button", "opt", '<span class="l">' + "ABCDEF"[i] + "</span><span>" + li.innerHTML + "</span>"); b.type = "button"; li.innerHTML = ""; li.appendChild(b);
          b.onclick = function () { tries++; markStarted(lid); if (i + 1 === correct) { b.classList.add("right"); opts.forEach(function (x) { x.firstChild.disabled = true; }); why && why.classList.add("show"); if (!S.quiz[qid]) { S.quiz[qid] = tries === 1 ? 1 : 2; save("quiz"); } score(); } else { b.classList.add("wrong"); b.disabled = true; why && why.classList.add("show"); if (!S.quiz[qid]) { S.quiz[qid] = 2; save("quiz"); score(); } } };
        });
        if (S.quiz[qid]) { opts.forEach(function (li, i) { if (i + 1 === correct) li.firstChild.classList.add("right"); li.firstChild.disabled = true; }); why && why.classList.add("show"); }
      } else if (type === "num") {
        var row = el("div", "numrow"); var inp = el("input"); inp.inputMode = "decimal"; inp.placeholder = "your answer"; row.appendChild(inp);
        if (q.dataset.unit) row.appendChild(el("span", "", esc(q.dataset.unit)));
        var cbt = el("button", "cbtn", "Check"); row.appendChild(cbt); var shb = el("button", "cbtn", "Show"); row.appendChild(shb); var fb = el("span", "fb"); row.appendChild(fb);
        (why || null) ? q.insertBefore(row, why) : q.appendChild(row);
        var ans = parseFloat(q.dataset.answer), tol = parseFloat(q.dataset.tol || "0.01"), t2 = 0;
        cbt.onclick = function () { t2++; markStarted(lid); var v = parseFloat(inp.value); if (!isFinite(v)) { fb.className = "fb no"; fb.textContent = "Type a number."; return; } var ok = Math.abs(v - ans) <= Math.max(tol * Math.abs(ans), tol); fb.className = "fb " + (ok ? "ok" : "no"); fb.textContent = ok ? "✓ Right" : "Not yet, try again"; if (ok) { why && why.classList.add("show"); if (!S.quiz[qid]) { S.quiz[qid] = t2 === 1 ? 1 : 2; save("quiz"); score(); } } };
        shb.onclick = function () { fb.className = "fb"; fb.textContent = "Answer: " + q.dataset.answer + (q.dataset.unit ? " " + q.dataset.unit : ""); why && why.classList.add("show"); if (!S.quiz[qid]) { S.quiz[qid] = 2; save("quiz"); score(); } };
      } else {
        var model = $(".model", q); var mb = el("button", "cbtn", "Show a model answer"); mb.type = "button";
        model ? q.insertBefore(mb, model) : q.appendChild(mb);
        mb.onclick = function () { model && model.classList.toggle("show"); if (!S.quiz[qid]) { S.quiz[qid] = 1; save("quiz"); score(); } };
      }
    });
    score();
  }

  /* ================= flashcards deck (FSRS-6) ================= */
  var CARDS = [];
  function hash(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return (h >>> 0).toString(36); }
  function harvestCards() {
    $$(".cards").forEach(function (box) {
      var lid = lessonOf(box); var L = LESSONS.find(function (x) { return x.id === lid; });
      var fcs = $$(".fc", box);
      var pv = el("div", "cprev");
      fcs.forEach(function (fc) { var f = $(".f", fc), b = $(".b", fc); if (!f || !b) return; var id = lid + ":" + hash(f.textContent); CARDS.push({ id: id, f: f.innerHTML, b: b.innerHTML, lid: lid, lt: L ? L.short : "" }); pv.appendChild(el("div", "", f.innerHTML)); });
      var ct = el("div", "ct", "<span>Flashcards · " + fcs.length + " cards added to your review deck</span><span>say the answer before you flip</span>");
      box.insertBefore(ct, box.firstChild); box.appendChild(pv);
    });
  }
  function deckDue() { var t = today(); return CARDS.filter(function (c) { var s = S.cards[c.id]; return s && s.due <= t; }); }
  function deckNew() { return CARDS.filter(function (c) { return !S.cards[c.id] && (S.started[c.lid] || S.done[c.lid]); }); }
  function initDeck() {
    var host = $("#deck"); if (!host) return;
    var stats = el("div", "dstats"); host.appendChild(stats);
    var seg = el("div", "ctrls"); host.appendChild(seg);
    var mode = "due";
    G.seg(seg, [["due", "Due today"], ["new", "New (from lessons you started)"], ["all", "Cram all"]], mode, function (m) { mode = m; nextCard(); });
    var card = el("div", "dcard"); host.appendChild(card);
    var q = [], cur = null;
    function counts() { var t = today(); var due = deckDue().length, nw = deckNew().length, learned = Object.keys(S.cards).length; stats.innerHTML = "<div><b>" + due + "</b>due today</div><div><b>" + nw + "</b>new, ready</div><div><b>" + learned + "</b>cards in rotation</div><div><b>" + CARDS.length + "</b>cards in the guide</div>"; }
    function pool() { if (mode === "due") return deckDue(); if (mode === "new") return deckNew().slice(0, 20); return CARDS.slice(); }
    function nextCard() {
      counts(); if (!q.length) q = pool().sort(function () { return Math.random() - 0.5; });
      cur = q.shift();
      if (!cur) { card.innerHTML = '<div class="front">' + (mode === "due" ? "Nothing due right now. Start a lesson, or switch to New cards." : "No cards here yet. Cards appear once you start a lesson.") + "</div>"; return; }
      card.innerHTML = '<div class="from">' + esc(cur.lt) + '</div><div class="front">' + cur.f + '</div><div class="back" hidden>' + cur.b + '</div><div class="dbtns"><button class="show">Show answer (space)</button></div>';
      renderMathIn(card);
      $(".show", card).onclick = reveal;
    }
    function ivl(g) { var st = S.cards[cur.id]; var s = FSRS6.schedule(st ? { S: st.S, D: st.D, reps: st.reps, lapses: st.lapses, last: st.last } : null, g, today()); return s.due - today(); }
    function reveal() {
      $(".back", card).hidden = false;
      var b = $(".dbtns", card); b.innerHTML = "";
      [[1, "Again", "again"], [2, "Hard", "hard"], [3, "Good", "good"], [4, "Easy", "easy"]].forEach(function (r) {
        var d = ivl(r[0]); var x = el("button", r[2], r[1] + "<small>" + (d <= 1 ? "1 day" : d + " days") + "</small>"); x.onclick = function () { rate(r[0]); }; b.appendChild(x);
      });
    }
    function rate(g) {
      var st = S.cards[cur.id]; var s = FSRS6.schedule(st ? { S: st.S, D: st.D, reps: st.reps, lapses: st.lapses, last: st.last } : null, g, today());
      S.cards[cur.id] = s; save("cards"); if (g === 1) q.splice(Math.min(3, q.length), 0, cur);
      renderProgress(); nextCard();
    }
    document.addEventListener("keydown", function (e) {
      if (!host.closest("section").contains(document.activeElement) && !isVisible(host)) return;
      if (e.target.tagName === "TEXTAREA" || e.target.tagName === "INPUT") return;
      var sb = $(".show", card); if (e.key === " " && sb) { e.preventDefault(); reveal(); }
      else if (/^[1-4]$/.test(e.key) && !$(".show", card) && cur) { rate(+e.key); }
    });
    nextCard();
  }
  function isVisible(n) { var r = n.getBoundingClientRect(); return r.top < innerHeight && r.bottom > 0; }

  /* ================= month tests (one random question per lesson) ================= */
  function initTests() {
    $$(".mtest").forEach(function (box) {
      var m = box.dataset.month;
      function build() {
        box.innerHTML = "";
        var qz = el("div", "quiz"); var n = 0;
        $$('section.lesson[data-month="' + m + '"]').forEach(function (sec) {
          var pool = $$(".quiz .q", sec).filter(function (q) { return (q.dataset.type || "mcq") !== "open"; });
          if (!pool.length) return; var q = pool[Math.floor(Math.random() * pool.length)].cloneNode(true);
          $$(".opt", q).forEach(function (b) { var li = b.parentNode; li.innerHTML = b.lastChild.innerHTML; });
          $$(".numrow,.cbtn", q).forEach(function (x) { x.remove(); }); $$(".why", q).forEach(function (w) { w.classList.remove("show"); });
          var L = LESSONS.find(function (x) { return x.id === sec.id; });
          q.querySelector(".stem").insertAdjacentHTML("afterbegin", '<a class="chip" style="margin-right:8px" href="#' + sec.id + '">' + esc(L ? L.short : sec.id) + "</a> ");
          qz.appendChild(q); n++;
        });
        box.appendChild(qz); initQuiz(qz);
        var nb = el("button", "cbtn", "↻ New test"); nb.onclick = build; box.appendChild(nb);
      }
      build();
    });
  }

  /* ================= worked examples (step reveal) ================= */
  function initWorked(w) {
    var k = w.closest("section.lesson"); if (k && !w.style.getPropertyValue("--k")) {}
    $$(".steps > li", w).forEach(function (li) { if (!(li.children.length === 1 && li.firstElementChild.tagName === "DIV")) { var d = el("div"); while (li.firstChild) d.appendChild(li.firstChild); li.appendChild(d); } });
    if (w.dataset.reveal != null) {
      var steps = $$(".steps > li", w); if (steps.length < 2) return;
      var ol = $(".steps", w); ol.classList.add("reveal");
      steps.forEach(function (s, i) { if (i > 0) s.classList.add("later"); });
      var res = $(".result", w); if (res) res.hidden = true;
      var b = el("button", "revealbtn", "Show next step ↓"); b.type = "button"; ol.after(b);
      var k2 = 1; var all = el("button", "revealbtn", "Show all"); all.type = "button"; b.after(all);
      function step() { if (k2 < steps.length) { steps[k2].classList.remove("later"); renderMathIn(steps[k2]); k2++; } if (k2 >= steps.length) { b.remove(); all.remove(); if (res) res.hidden = false; } }
      b.onclick = step; all.onclick = function () { while (k2 < steps.length) step(); step(); };
    }
  }

  /* ================= misc components ================= */
  var CT = { key: "Key idea", intuition: "Intuition", analogy: "Analogy", pitfall: "Watch out", ece: "Your ECE background", book: "From the book", mac: "On your Mac", exam: "Interview angle" };
  function initCallout(c) { if ($(".ct", c)) return; var t = Object.keys(CT).find(function (k) { return c.classList.contains(k); }); if (t) c.insertBefore(el("div", "ct", CT[t]), c.firstChild); }
  function initChecklist(c) {
    if (!$(".ct", c)) c.insertBefore(el("div", "ct", "Can you do these? Tick when true"), c.firstChild);
    $$("input[type=checkbox]", c).forEach(function (inp, i) { var k = lessonOf(c) + ":c" + i; inp.checked = !!S.checks[k]; inp.onchange = function () { S.checks[k] = inp.checked ? 1 : 0; save("checks"); markStarted(lessonOf(c)); }; });
  }
  function initDone(d) {
    var lid = d.dataset.lesson; var inp = $("input", d); inp.checked = !!S.done[lid];
    inp.onchange = function () { if (inp.checked) S.done[lid] = 1; else delete S.done[lid]; save("done"); markStarted(lid); renderProgress(); };
    var nb = $(".nbbtn", d); if (nb) nb.onclick = function () { downloadNotebook(lid); };
  }
  function downloadNotebook(lid) {
    var all = jsonScript("notebooks", {}); var nb = all[lid]; if (!nb) return;
    var blob = new Blob([JSON.stringify(nb, null, 1)], { type: "application/x-ipynb+json" });
    var a = el("a"); a.href = URL.createObjectURL(blob); a.download = lid + ".ipynb"; document.body.appendChild(a); a.click(); a.remove();
  }
  window.downloadDataPack = function () {
    var z = jsonScript("datapack", null); if (!z) return;
    var s = atob(z.b64), u = new Uint8Array(s.length); for (var i = 0; i < s.length; i++) u[i] = s.charCodeAt(i);
    var a = el("a"); a.href = URL.createObjectURL(new Blob([u], { type: "application/zip" })); a.download = "ml-course-data.zip"; document.body.appendChild(a); a.click(); a.remove();
  };
  function initFigures() {
    document.addEventListener("click", function (e) {
      var im = e.target.closest(".fimg img"); if (!im) return;
      var lb = el("div", "lightbox"); var i2 = el("img"); i2.src = im.src; i2.alt = im.alt; lb.appendChild(i2); lb.onclick = function () { lb.remove(); }; document.body.appendChild(lb);
    });
  }
  var GLOSS = {};
  function initGlossary() {
    GLOSS = jsonScript("glossary", {});
    var tip = el("div", "gtip"); tip.hidden = true; document.body.appendChild(tip);
    document.addEventListener("mouseover", function (e) {
      var d = e.target.closest("dfn[data-g]"); if (!d) { tip.hidden = true; return; }
      var g = GLOSS[d.dataset.g]; if (!g) return;
      tip.innerHTML = "<b>" + esc(g.term) + "</b>" + g.def; tip.hidden = false; renderMathIn(tip);
      var r = d.getBoundingClientRect(); tip.style.left = Math.min(innerWidth - 360, Math.max(8, r.left)) + "px"; tip.style.top = (r.bottom + 8 + 200 > innerHeight ? r.top - tip.offsetHeight - 8 : r.bottom + 8) + "px";
    });
  }
  function renderMathIn(node) {
    if (!window.katex || !node) return;
    var walk = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, null), list = [], t;
    while ((t = walk.nextNode())) if (/\\\(|\\\[/.test(t.nodeValue) && !t.parentNode.closest("pre,code,textarea,.katex")) list.push(t);
    list.forEach(function (tn) {
      var s = tn.nodeValue, html = esc(s).replace(/\\\[([\s\S]+?)\\\]/g, function (m, x) { return G.tex(x.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">"), true); }).replace(/\\\(([\s\S]+?)\\\)/g, function (m, x) { return G.tex(x.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">"), false); });
      var sp = el("span"); sp.innerHTML = html; tn.replaceWith(sp);
    });
  }
  G.renderMath = renderMathIn;

  /* ================= search ================= */
  function initSearch() {
    var idx = [];
    LESSONS.forEach(function (L) { idx.push({ t: L.title, s: L.monthName + (L.week ? " · Week " + L.week : ""), h: "#" + L.id }); });
    $$("section.lesson h3[id], section.lesson h4[id]").forEach(function (h) { var sec = h.closest("section"); var L = LESSONS.find(function (x) { return x.id === sec.id; }); idx.push({ t: h.textContent.trim(), s: L ? L.title : "", h: "#" + h.id }); });
    Object.keys(GLOSS).forEach(function (k) { var g = GLOSS[k]; if (g.at) idx.push({ t: g.term, s: "Glossary", h: "#" + g.at }); });
    var ov = el("div", "search"); ov.hidden = true; ov.innerHTML = '<div class="box"><input placeholder="Search lessons, topics, terms… (Esc to close)" aria-label="Search"><div class="res"></div></div>'; document.body.appendChild(ov);
    var inp = $("input", ov), res = $(".res", ov), sel = 0;
    function show() { ov.hidden = false; inp.value = ""; draw(); inp.focus(); }
    function hide() { ov.hidden = true; }
    function draw() {
      var q = inp.value.trim().toLowerCase(); var hits = idx.filter(function (x) { return !q || x.t.toLowerCase().indexOf(q) >= 0 || x.s.toLowerCase().indexOf(q) >= 0; }).slice(0, 40);
      res.innerHTML = ""; hits.forEach(function (x, i) { var a = el("a", i === sel ? "sel" : "", esc(x.t) + "<small>" + esc(x.s) + "</small>"); a.href = x.h; a.onclick = hide; res.appendChild(a); });
    }
    inp.addEventListener("input", function () { sel = 0; draw(); });
    inp.addEventListener("keydown", function (e) { var as = $$("a", res); if (e.key === "ArrowDown") { sel = Math.min(as.length - 1, sel + 1); draw(); e.preventDefault(); } else if (e.key === "ArrowUp") { sel = Math.max(0, sel - 1); draw(); e.preventDefault(); } else if (e.key === "Enter" && as[sel]) { location.hash = as[sel].getAttribute("href"); hide(); } else if (e.key === "Escape") hide(); });
    ov.addEventListener("click", function (e) { if (e.target === ov) hide(); });
    $("#searchbtn").onclick = show;
    document.addEventListener("keydown", function (e) { if ((e.key === "k" && (e.ctrlKey || e.metaKey)) || (e.key === "/" && !/INPUT|TEXTAREA/.test(document.activeElement.tagName))) { e.preventDefault(); show(); } });
  }

  /* ================= widgets (lazy) ================= */
  function initWidgets() {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return; io.unobserve(e.target);
        var w = e.target, fn = G.W[w.dataset.w];
        var body = $(".wb", w);
        if (!fn) { body.innerHTML = '<p style="color:var(--bad)">Widget "' + esc(w.dataset.w) + '" is missing.</p>'; return; }
        try { fn(body, JSON.parse(w.dataset.args || "{}"), { root: w, lesson: lessonOf(w) }); } catch (err) { body.innerHTML = '<pre class="err">' + esc(err.stack || err) + "</pre>"; console.error(err); }
      });
    }, { rootMargin: "400px 0px" });
    $$(".widget").forEach(function (w) {
      var note = $(".wn", w);
      var wh = el("div", "wh", '<span class="tag">' + esc(w.dataset.tag || "Interactive") + "</span><b>" + esc(w.dataset.title || "") + "</b>");
      var wb = el("div", "wb");
      Array.prototype.slice.call(w.childNodes).forEach(function (n) { if (n !== note) wb.appendChild(n); });
      w.innerHTML = ""; w.appendChild(wh); w.appendChild(wb); if (note) w.appendChild(note);
      io.observe(w);
    });
  }

  /* ================= boot ================= */
  function boot() {
    var MN = jsonScript("months", {});
    OUTS = jsonScript("outputs", {});
    $$("section.lesson").forEach(function (s) {
      LESSONS.push({ id: s.id, kind: s.dataset.kind || "isl", month: s.dataset.month || "0", monthName: MN[s.dataset.month] || ("Month " + s.dataset.month), week: s.dataset.week || "", title: s.dataset.title || s.id, short: s.dataset.short || s.dataset.title || s.id });
    });
    buildRail();
    $("#themebtn").onclick = toggleTheme;
    $("#menubtn").onclick = function () { document.body.classList.toggle("railopen"); };
    $("#pystat").onclick = function () { pyStart(); };
    $$(".callout").forEach(initCallout);
    $$(".worked").forEach(initWorked);
    $$(".predict").forEach(initPredict);
    $$(".py").forEach(initCell);
    $$(".ex").forEach(initEx);
    $$(".prob").forEach(initProb);
    $$(".lesson .quiz").forEach(initQuiz);
    $$(".checklist").forEach(initChecklist);
    $$(".ldone").forEach(initDone);
    harvestCards();
    initGlossary(); initFigures(); initWidgets(); initSearch(); initDeck(); initTests();
    scrollSpy(); renderProgress();
    if (location.hash) { var t = document.getElementById(location.hash.slice(1)); if (t) setTimeout(function () { t.scrollIntoView(); }, 50); }
    document.dispatchEvent(new CustomEvent("guide:ready"));
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
