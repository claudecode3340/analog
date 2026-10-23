/* Pyodide worker: runs learner code off the main thread so the page never freezes.
   Messages in : {type:'init', prelude, files:{path:base64}, zips:{dir:base64}}
                 {type:'run', id, ns, code, check, expectError}
                 {type:'reset', ns}
   Messages out: {type:'status', s, msg} · {type:'result', id, res} */
var PYO = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/";
var py = null, ready = null;
function post(m) { self.postMessage(m); }
function b64bytes(b) { var s = atob(b), a = new Uint8Array(s.length); for (var i = 0; i < s.length; i++) a[i] = s.charCodeAt(i); return a; }
async function init(m) {
  post({ type: "status", s: "loading", msg: "Downloading Python (first time ~15 s)…" });
  importScripts(PYO + "pyodide.js");
  py = await loadPyodide({ indexURL: PYO });
  post({ type: "status", s: "loading", msg: "Loading numpy and pandas…" });
  await py.loadPackage(["numpy", "pandas", "matplotlib"]);
  var FS = py.FS, home = "/home/pyodide";
  Object.keys(m.files || {}).forEach(function (p) {
    var parts = p.split("/"); var d = home;
    for (var i = 0; i < parts.length - 1; i++) { d += "/" + parts[i]; try { FS.mkdir(d); } catch (e) {} }
    FS.writeFile(home + "/" + p, b64bytes(m.files[p]));
  });
  var zips = m.zips || {};
  for (var k in zips) {
    FS.writeFile("/tmp/" + k + ".zip", b64bytes(zips[k]));
    py.runPython("import zipfile,sys; zipfile.ZipFile('/tmp/" + k + ".zip').extractall('/home/pyodide/_lib'); sys.path.insert(0,'/home/pyodide/_lib')");
  }
  FS.writeFile("/home/pyodide/_lib_prelude.py", m.prelude);
  py.runPython("import sys,os; sys.path.insert(0,'/home/pyodide'); os.chdir('/home/pyodide'); import importlib.util as u; s=u.spec_from_file_location('guide_rt','/home/pyodide/_lib_prelude.py'); guide_rt=u.module_from_spec(s); s.loader.exec_module(guide_rt); sys.modules['guide_rt']=guide_rt; guide_rt.setup_pandas()");
  post({ type: "status", s: "ready", msg: "Python ready" });
}
async function run(m) {
  try {
    await ready;
    post({ type: "status", s: "busy", msg: "Running…" });
    try { await py.loadPackagesFromImports(m.code + "\n" + (m.check || "")); } catch (e) {}
    var src = (m.code || "") + "\n" + (m.check || "");
    if (/\bstatsmodels\b|\bISLP\b|\bsummarize\b|read_html/.test(src)) { try { await py.loadPackage(["statsmodels", "scikit-learn", "scipy", "lxml"]); } catch (e) {} }
    py.globals.set("_c", m.code); py.globals.set("_k", m.check || null); py.globals.set("_n", m.ns || "main"); py.globals.set("_x", m.expectError || null);
    var r = py.runPython("import guide_rt; guide_rt.run(_c, _n, _k, _x)");
    post({ type: "result", id: m.id, res: JSON.parse(r) });
  } catch (e) {
    post({ type: "result", id: m.id, res: { status: "error", outputs: [], error: String(e && e.message || e), etype: "InternalError", friendly: "Something went wrong inside the Python runtime. Reload the page and try again." } });
  }
  post({ type: "status", s: "ready", msg: "Python ready" });
}
self.onmessage = function (ev) {
  var m = ev.data;
  if (m.type === "init") { ready = init(m).catch(function (e) { post({ type: "status", s: "failed", msg: "Python could not load (are you offline?). The reference outputs below are still shown. " + e }); throw e; }); }
  else if (m.type === "run") run(m);
  else if (m.type === "reset") ready.then(function () { py.runPython("import guide_rt; guide_rt.reset_ns(" + JSON.stringify(m.ns) + ")"); });
};
