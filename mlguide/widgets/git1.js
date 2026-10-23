/* git1 · working folder → staging area → commits → GitHub, with a live `git status` */
G.widget("git1-flow", function (body, args) {
  var S;
  function reset() {
    S = { files: { "README.md": { wd: 1, st: 0, cm: 0 }, "knn.py": { wd: 1, st: 0, cm: 0 } }, commits: [], pushed: 0, log: "" };
  }
  reset();
  var bar = G.el("div"); bar.style.cssText = "display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px"; body.appendChild(bar);
  var cols = G.el("div"); cols.style.cssText = "display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(min(100%,150px),1fr))"; body.appendChild(cols);
  var term = G.el("pre"); term.style.cssText = "background:#0f141b;color:#d7dde8;border-radius:10px;padding:10px 14px;font:13px/1.5 var(--mono);white-space:pre-wrap;margin:10px 0 0;min-height:120px;overflow-x:auto"; body.appendChild(term);
  var AREAS = [["wd", "1 · Working folder", "your files on disk", "var(--tool)"], ["st", "2 · Staging area", "what the next commit will contain", "var(--math)"], ["cm", "3 · Commits (local)", "save points in .git", "var(--isl)"], ["gh", "4 · GitHub", "the copy online", "var(--udl)"]];
  var boxes = {};
  AREAS.forEach(function (a) {
    var b = G.el("div"); b.style.cssText = "border:1.5px solid " + a[3] + ";border-radius:12px;padding:8px 10px;background:var(--surface);min-height:120px";
    b.innerHTML = '<div style="font-weight:700;color:' + a[3] + ';font-size:15px">' + a[1] + '</div><div style="font-size:12.5px;color:var(--muted);margin-bottom:6px">' + a[2] + "</div>";
    var inner = G.el("div"); b.appendChild(inner); boxes[a[0]] = inner; cols.appendChild(b);
  });
  function chip(txt, col, sub) { return '<div style="border:1px solid var(--line2);border-left:4px solid ' + col + ';border-radius:7px;padding:3px 8px;margin:4px 0;font:13px/1.4 var(--mono);background:var(--panel)">' + txt + (sub ? '<div style="font:11.5px var(--body);color:var(--muted)">' + sub + "</div>" : "") + "</div>"; }
  function status(f) {
    var x = S.files[f];
    if (!x.cm && !x.st) return "untracked";
    var out = [];
    if (x.st && x.st !== x.cm) out.push(x.cm ? "staged-mod" : "staged-new");
    if (x.wd !== (x.st || x.cm)) out.push("modified");
    return out.join(" ") || "clean";
  }
  function gitStatus() {
    var st = [], md = [], ut = [];
    Object.keys(S.files).forEach(function (f) {
      var x = S.files[f];
      if (!x.cm && !x.st) { ut.push(f); return; }
      if (x.st && x.st !== x.cm) st.push((x.cm ? "modified:   " : "new file:   ") + f);
      if (x.wd !== (x.st || x.cm)) md.push("modified:   " + f);
    });
    var t = "$ git status\nOn branch main\n";
    if (S.commits.length && S.pushed) t += S.commits.length > S.pushed ? "Your branch is ahead of 'origin/main' by " + (S.commits.length - S.pushed) + " commit" + (S.commits.length - S.pushed > 1 ? "s" : "") + ".\n  (use \"git push\" to publish your local commits)\n" : "Your branch is up to date with 'origin/main'.\n";
    if (!S.commits.length) t += "\nNo commits yet\n";
    if (st.length) t += "\nChanges to be committed:\n" + st.map(function (s) { return '        <span style="color:#7ee2a8">' + s + "</span>"; }).join("\n") + "\n";
    if (md.length) t += "\nChanges not staged for commit:\n  (use \"git add &lt;file&gt;...\" to update what will be committed)\n" + md.map(function (s) { return '        <span style="color:#ff7b72">' + s + "</span>"; }).join("\n") + "\n";
    if (ut.length) t += "\nUntracked files:\n  (use \"git add &lt;file&gt;...\" to include in what will be committed)\n" + ut.map(function (s) { return '        <span style="color:#ff7b72">' + s + "</span>"; }).join("\n") + "\n";
    if (!st.length && !md.length && !ut.length) t += "nothing to commit, working tree clean\n";
    return t;
  }
  function draw() {
    boxes.wd.innerHTML = Object.keys(S.files).map(function (f) {
      var s = status(f), sub = s === "untracked" ? "untracked (git ignores it until you add it)" : /modified/.test(s) ? "changed since last add/commit" : "saved in a commit";
      return chip(f + " <small>v" + S.files[f].wd + "</small>", /untracked|modified/.test(s) ? "var(--bad)" : "var(--good)", sub);
    }).join("");
    var stg = Object.keys(S.files).filter(function (f) { var x = S.files[f]; return x.st && x.st !== x.cm; });
    boxes.st.innerHTML = stg.length ? stg.map(function (f) { return chip(f + " <small>v" + S.files[f].st + "</small>", "var(--math)", "ready to commit"); }).join("") : '<div style="color:var(--faint);font-size:13px">(empty)</div>';
    boxes.cm.innerHTML = S.commits.length ? S.commits.slice().reverse().map(function (c, j) { var idx = S.commits.length - j; return chip(c.id + " " + c.msg, "var(--isl)", (idx <= S.pushed ? "pushed · " : "") + c.files); }).join("") : '<div style="color:var(--faint);font-size:13px">(no commits yet)</div>';
    boxes.gh.innerHTML = S.pushed ? S.commits.slice(0, S.pushed).reverse().map(function (c) { return chip(c.id + " " + c.msg, "var(--udl)"); }).join("") : '<div style="color:var(--faint);font-size:13px">(nothing pushed yet)</div>';
    term.innerHTML = (S.log ? S.log + "\n" : "") + gitStatus();
  }
  function hex(n) { var s = ""; var r = G.rng(n * 7919 + 13); for (var i = 0; i < 7; i++) s += "0123456789abcdef"[Math.floor(r() * 16)]; return s; }
  function edit(f) { if (!S.files[f]) S.files[f] = { wd: 1, st: 0, cm: 0 }; else S.files[f].wd++; S.log = "(you edited and saved " + f + " in VS Code)"; draw(); }
  function add(which) {
    var fs = which === "." ? Object.keys(S.files) : [which], did = [];
    fs.forEach(function (f) { var x = S.files[f]; if (x.wd !== (x.st || x.cm) || (!x.cm && !x.st)) { x.st = x.wd; did.push(f); } });
    S.log = "$ git add " + which + (did.length ? "" : "\n(nothing changed, so nothing new was staged)"); draw();
  }
  var msgs = ["Add README and KNN script", "Fix distance formula", "Add notes", "Tidy README", "Use odd k only", "Add tests"];
  function commit() {
    var stg = Object.keys(S.files).filter(function (f) { var x = S.files[f]; return x.st && x.st !== x.cm; });
    var m = msgs[S.commits.length % msgs.length];
    if (!stg.length) { S.log = '$ git commit -m "' + m + '"\nnothing added to commit (use "git add" first)'; draw(); return; }
    stg.forEach(function (f) { S.files[f].cm = S.files[f].st; });
    var id = hex(S.commits.length + 1);
    S.commits.push({ id: id, msg: m, files: stg.join(", ") });
    S.log = '$ git commit -m "' + m + '"\n[main ' + (S.commits.length === 1 ? "(root-commit) " : "") + id + "] " + m + "\n " + stg.length + " file" + (stg.length > 1 ? "s" : "") + " changed"; draw();
  }
  function push() {
    if (!S.commits.length) { S.log = "$ git push\nerror: src refspec main does not match any (make a commit first)"; draw(); return; }
    var n = S.commits.length - S.pushed;
    S.log = "$ git push\n" + (n ? "To https://github.com/you/ml-course.git\n   " + (S.pushed ? S.commits[S.pushed - 1].id : "*") + ".." + S.commits[S.commits.length - 1].id + "  main -> main" : "Everything up-to-date");
    S.pushed = S.commits.length; draw();
  }
  G.button(bar, "✎ Edit README.md", function () { edit("README.md"); });
  G.button(bar, "✎ Edit knn.py", function () { edit("knn.py"); });
  G.button(bar, "+ New notes.txt", function () { edit("notes.txt"); });
  G.button(bar, "git add README.md", function () { add("README.md"); }, "run");
  G.button(bar, "git add .", function () { add("."); }, "run");
  G.button(bar, "git commit -m …", commit, "run");
  G.button(bar, "git push", push, "run");
  G.button(bar, "Start again", function () { reset(); draw(); });
  draw();
});
