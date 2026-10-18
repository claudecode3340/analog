/* s0-setup · a pretend Terminal for practising pwd, ls, cd and mkdir safely */
G.widget("s0-setup-term", function (body, args) {
  var HOME = "/Users/you";
  function dir(kids) { return { d: 1, k: kids || {} }; }
  function file() { return { d: 0 }; }
  var root = dir({
    Applications: dir({ "Visual Studio Code.app": dir({}), "Utilities": dir({ "Terminal.app": dir({}) }) }),
    Users: dir({ you: dir({
      ".zshrc": file(),
      Desktop: dir({ "photo.png": file() }),
      Documents: dir({ "notes.txt": file(), "resume.pdf": file() }),
      Downloads: dir({ "ml-course-data.zip": file(), "VSCode-darwin-universal.zip": file() }),
      Music: dir({}), Pictures: dir({})
    }) })
  });
  var cwd = HOME, hist = [], hpos = 0;
  var tasks = [
    ["pwd", "Ask where you are: <code>pwd</code>"],
    ["ls", "List what is here: <code>ls</code>"],
    ["cdDocs", "Go into Documents: <code>cd Documents</code>"],
    ["back", "Go back up one level: <code>cd ..</code>"],
    ["mk", "Make the course folder: <code>mkdir ml-course</code>"],
    ["cdml", "Go into it: <code>cd ml-course</code>"],
    ["home", "Jump home from anywhere: <code>cd ~</code> (or just <code>cd</code>)"]
  ];
  var done = {};

  var wrap = G.el("div"); wrap.style.cssText = "display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));align-items:start";
  body.appendChild(wrap);
  var term = G.el("div"); term.style.cssText = "background:#0f141b;color:#d7dde8;border-radius:12px;padding:10px 12px 12px;font:13.5px/1.55 var(--mono);min-height:280px;max-height:380px;overflow:auto;border:1px solid var(--line2);cursor:text";
  var bar = G.el("div", "", '<span style="display:inline-block;width:11px;height:11px;border-radius:50%;background:#ff5f57;margin-right:6px"></span><span style="display:inline-block;width:11px;height:11px;border-radius:50%;background:#febc2e;margin-right:6px"></span><span style="display:inline-block;width:11px;height:11px;border-radius:50%;background:#28c840;margin-right:10px"></span><span style="color:#8a93a3;font-size:12px">you — zsh (practice)</span>');
  bar.style.cssText = "margin:0 0 8px;white-space:nowrap";
  term.appendChild(bar);
  var log = G.el("div"); log.style.cssText = "white-space:pre-wrap;word-break:break-word";
  term.appendChild(log);
  var line = G.el("div"); line.style.cssText = "display:flex;gap:6px;align-items:baseline";
  var pr = G.el("span"); pr.style.cssText = "color:#7ee2a8;white-space:nowrap";
  var inp = document.createElement("input");
  inp.setAttribute("aria-label", "Type a command and press Return");
  inp.setAttribute("autocapitalize", "off"); inp.setAttribute("autocomplete", "off"); inp.setAttribute("spellcheck", "false");
  inp.style.cssText = "flex:1;min-width:40px;background:transparent;border:0;outline:0;color:#fff;font:inherit;padding:0";
  line.appendChild(pr); line.appendChild(inp); term.appendChild(line);
  wrap.appendChild(term);
  term.addEventListener("click", function () { inp.focus(); });

  var side = G.el("div"); wrap.appendChild(side);
  var tl = G.el("div"); tl.style.cssText = "font-size:15px;line-height:1.5";
  side.appendChild(G.el("div", "", "<b>Your missions</b> (they tick themselves):"));
  side.appendChild(tl);
  var info = G.el("div", "readout"); side.appendChild(info);
  var bb = G.el("div"); bb.style.cssText = "display:flex;flex-wrap:wrap;gap:6px;margin-top:8px"; side.appendChild(bb);
  ["pwd", "ls", "cd Documents", "cd ..", "mkdir ml-course", "cd ml-course", "cd ~", "ls -a"].forEach(function (c) {
    G.button(bb, c, function () { inp.value = c; submit(); });
  });
  G.button(bb, "Start again", function () { reset(); });

  function short(p) { return p === HOME ? "~" : (p === "/" ? "/" : p.split("/").pop()); }
  function prompt() { return "you@MacBook-Air " + short(cwd) + " %"; }
  function norm(p) {
    if (p === "~" || p.indexOf("~/") === 0) p = HOME + p.slice(1);
    var abs = p.charAt(0) === "/" ? p : cwd + "/" + p;
    var out = [];
    abs.split("/").forEach(function (s) { if (!s || s === ".") return; if (s === "..") out.pop(); else out.push(s); });
    return "/" + out.join("/");
  }
  function lookup(p) { // case-insensitive like a default Mac disk; returns {node, path}
    var parts = p.split("/").filter(Boolean), n = root, real = [];
    for (var i = 0; i < parts.length; i++) {
      if (!n.d) return null;
      var key = Object.keys(n.k).find(function (k) { return k.toLowerCase() === parts[i].toLowerCase(); });
      if (!key) return null; n = n.k[key]; real.push(key);
    }
    return { node: n, path: "/" + real.join("/") };
  }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;"); }
  function out(html) { var d = G.el("div", "", html); log.appendChild(d); }
  function tick(k) { if (!done[k]) { done[k] = 1; drawTasks(); } }
  function drawTasks() {
    tl.innerHTML = tasks.map(function (t) { var ok = !!done[t[0]]; return '<div style="margin:3px 0;color:' + (ok ? "var(--good)" : "var(--ink2)") + '">' + (ok ? "&#10003; " : "&#9675; ") + t[1] + "</div>"; }).join("");
    var n = Object.keys(done).length;
    info.innerHTML = "<div>you are in<b style=\"font-size:15px\">" + esc(cwd) + "</b></div><div>missions done<b>" + n + " / " + tasks.length + "</b></div>";
  }
  function run(cmd) {
    var parts = cmd.trim().split(/\s+/), c = parts[0], a = parts.slice(1);
    if (!c) return;
    if (c === "pwd") { out(esc(cwd)); tick("pwd"); return; }
    if (c === "ls") {
      var all = a.indexOf("-a") >= 0 || a.indexOf("-la") >= 0 || a.indexOf("-al") >= 0;
      var target = a.filter(function (x) { return x.charAt(0) !== "-"; })[0];
      var L = lookup(target ? norm(target) : cwd);
      if (!L) { out("ls: " + esc(target) + ": No such file or directory"); return; }
      if (!L.node.d) { out(esc(target)); return; }
      var names = Object.keys(L.node.k).filter(function (k) { return all || k.charAt(0) !== "."; }).sort(function (x, y) { return x.toLowerCase() < y.toLowerCase() ? -1 : 1; });
      if (all) names = [".", ".."].concat(names);
      out(names.length ? names.map(function (k) { var isd = k === "." || k === ".." || (L.node.k[k] && L.node.k[k].d); return '<span style="color:' + (isd ? "#79b8ff" : "#d7dde8") + '">' + esc(k) + "</span>"; }).join("    ") : '<span style="color:#8a93a3">(nothing here yet: an empty folder prints nothing)</span>');
      if (cwd === HOME || target) tick("ls");
      return;
    }
    if (c === "cd") {
      var t = a[0] || "~";
      if (a.length > 1) { out("cd: string not in pwd: " + esc(a[0]) + '\n<span style="color:#e6b450">(Hint: a folder name with a space needs quotes, e.g. cd "My Folder")</span>'); return; }
      var L2 = lookup(norm(t));
      if (!L2) { out("cd: no such file or directory: " + esc(t) + '\n<span style="color:#e6b450">(Hint: type ls to see the exact names that exist here.)</span>'); return; }
      if (!L2.node.d) { out("cd: not a directory: " + esc(t)); return; }
      var from = cwd; cwd = L2.path;
      if (cwd === HOME + "/Documents") tick("cdDocs");
      if (t === ".." && from === HOME + "/Documents" && cwd === HOME) tick("back");
      if (/\/ml-course$/i.test(cwd)) tick("cdml");
      if (cwd === HOME && (t === "~" || !a[0]) && from !== HOME) tick("home");
      return;
    }
    if (c === "mkdir") {
      var names2 = a.filter(function (x) { return x.charAt(0) !== "-"; });
      if (!names2.length) { out("usage: mkdir [-p] directory_name ..."); return; }
      names2.forEach(function (nm) {
        var full = norm(nm), parent = full.slice(0, full.lastIndexOf("/")) || "/", base = full.split("/").pop();
        var P = lookup(parent);
        if (!P || !P.node.d) { out("mkdir: " + esc(parent) + ": No such file or directory"); return; }
        if (lookup(full)) { out("mkdir: " + esc(nm) + ": File exists"); return; }
        P.node.k[base] = dir({});
        if (/^ml-course$/i.test(base)) tick("mk");
      });
      return;
    }
    if (c === "clear") { log.innerHTML = ""; return; }
    if (c === "whoami") { out("you"); return; }
    if (c === "echo") { out(esc(a.join(" "))); return; }
    if (c === "open") { out('<span style="color:#8a93a3">(On your Mac, open . opens this folder in a Finder window.)</span>'); return; }
    if (c === "help") { out("This practice Terminal understands: pwd, ls, ls -a, cd, mkdir, clear, whoami, echo, open ."); return; }
    if (c === "%" || c === "$") { out('<span style="color:#e6b450">Don\'t type the % sign: it is part of the prompt, not the command.</span>'); return; }
    out("zsh: command not found: " + esc(c) + (/^[A-Z]/.test(c) ? '\n<span style="color:#e6b450">(Type commands in lower case, exactly as shown.)</span>' : ""));
  }
  function submit() {
    var cmd = inp.value; inp.value = "";
    out('<span style="color:#7ee2a8">' + esc(prompt()) + "</span> " + esc(cmd));
    if (cmd.trim()) { hist.push(cmd); hpos = hist.length; }
    run(cmd); pr.textContent = prompt(); drawTasks();
    term.scrollTop = term.scrollHeight;
  }
  inp.addEventListener("keydown", function (e) {
    if (e.key === "Enter") { e.preventDefault(); submit(); }
    else if (e.key === "ArrowUp") { if (hpos > 0) { hpos--; inp.value = hist[hpos]; } e.preventDefault(); }
    else if (e.key === "ArrowDown") { if (hpos < hist.length - 1) { hpos++; inp.value = hist[hpos]; } else { hpos = hist.length; inp.value = ""; } e.preventDefault(); }
  });
  function reset() {
    cwd = HOME; done = {}; log.innerHTML = ""; hist = []; hpos = 0;
    var me = lookup(HOME).node; Object.keys(me.k).forEach(function (k) { if (/^ml-course$/i.test(k)) delete me.k[k]; });
    out('<span style="color:#8a93a3">Last login: Sat Oct 17 09:12:04 on ttys000\nThis is a practice Terminal inside the page. Nothing you type here touches your Mac.</span>');
    pr.textContent = prompt(); drawTasks();
  }
  reset();
});
