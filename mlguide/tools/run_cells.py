#!/usr/bin/env python
"""Run every Python cell and exercise of one or more lessons in real CPython, using the
SAME runtime (src/prelude.py) the browser uses. Produces build/outputs/<lesson>.json with the
reference outputs shown in the guide, and fails loudly if anything is wrong.

Usage (from anywhere):
  source /tmp/claude-0/-home-user-analog/f43a8c4b-e900-5b65-9888-7cda2c0d5ebc/scratchpad/mlenv/bin/activate
  python /home/user/analog/mlguide/tools/run_cells.py isl2-1 isl2-2      # some lessons
  python /home/user/analog/mlguide/tools/run_cells.py --all              # everything

Checks performed
  * .py cells (run/setup/local): must finish with status ok (or the declared data-error for expect-error cells)
  * .ex exercises: starter + check must NOT pass (unless data-starter-passes); solution + check MUST pass
  * every cell runs in the lesson's own namespace, top to bottom, exactly like the browser
"""
import sys, os, json, time, shutil, base64, io, signal, importlib.util, glob
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTD = os.path.join(ROOT, "build", "outputs")
WORK = os.path.join(ROOT, "build", "work")


def load_prelude():
    spec = importlib.util.spec_from_file_location("guide_rt", os.path.join(ROOT, "src", "prelude.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    sys.modules["guide_rt"] = m
    m.setup_pandas()
    return m


def to_webp(outs):
    try:
        from PIL import Image
    except Exception:
        return outs
    for o in outs:
        if o.get("t") == "img" and not o["v"].startswith("data:"):
            im = Image.open(io.BytesIO(base64.b64decode(o["v"]))).convert("RGB")
            b = io.BytesIO()
            im.save(b, "WEBP", quality=86, method=6)
            o["v"] = "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()
    return outs


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout()


def code_of(node):
    return node.get_text().replace("\r", "").strip("\n").rstrip()


def run_lesson(rt, lid, verbose=True):
    path = os.path.join(ROOT, "lessons", lid + ".html")
    if not os.path.exists(path):
        print(f"[{lid}] no file {path}")
        return False
    soup = BeautifulSoup(open(path, encoding="utf-8").read(), "lxml")
    rt.reset_ns(lid)
    outs, ok_all = {}, True
    items = soup.select(".py, .ex")
    t0 = time.time()
    for it in items:
        cid = it.get("id")
        if not cid:
            print(f"[{lid}] ERROR: a cell has no id: {str(it)[:120]}")
            ok_all = False
            continue
        signal.signal(signal.SIGALRM, _alarm)
        signal.alarm(int(it.get("data-timeout", "240")))
        try:
            if "py" in it.get("class", []):
                src = it.select_one("pre.src")
                if src is None:
                    print(f"[{lid}] ERROR {cid}: no pre.src"); ok_all = False; continue
                exp = it.get("data-error")
                res = json.loads(rt.run(code_of(src), lid, None, exp))
                good = res["status"] == ("expected" if exp else "ok")
                if not good:
                    ok_all = False
                    print(f"[{lid}] FAIL cell {cid}: status={res['status']} {res.get('etype','')}\n{res.get('error','')}\n{res.get('fail','')}")
                outs[cid] = {"status": res["status"], "outputs": to_webp(res["outputs"]),
                             **({"error": res["error"], "etype": res.get("etype"), "friendly": res.get("friendly", "")} if res.get("error") else {})}
            else:
                src, chk, sol = it.select_one("pre.src"), it.select_one("pre.check"), it.select_one("pre.solution")
                if not (src and chk and sol):
                    print(f"[{lid}] ERROR exercise {cid}: needs pre.src, pre.check and pre.solution"); ok_all = False; continue
                # starter must not pass (run in a throwaway copy of the namespace)
                snap = dict(rt._ns(lid))
                r0 = json.loads(rt.run(code_of(src), lid, code_of(chk)))
                rt._NS[lid] = snap
                if r0["status"] == "ok" and not it.has_attr("data-starter-passes"):
                    ok_all = False
                    print(f"[{lid}] FAIL exercise {cid}: the STARTER code already passes the checks (make the starter incomplete or the checks stricter)")
                r1 = json.loads(rt.run(code_of(sol), lid, code_of(chk)))
                if r1["status"] != "ok":
                    ok_all = False
                    print(f"[{lid}] FAIL exercise {cid}: the SOLUTION does not pass: {r1['status']} {r1.get('fail','')}\n{r1.get('error','')}")
                outs[cid + ":solution"] = {"status": r1["status"], "outputs": to_webp(r1["outputs"])}
        except Timeout:
            ok_all = False
            print(f"[{lid}] FAIL {cid}: timed out")
        finally:
            signal.alarm(0)
    os.makedirs(OUTD, exist_ok=True)
    json.dump(outs, open(os.path.join(OUTD, lid + ".json"), "w"))
    if verbose:
        print(f"[{lid}] {'OK' if ok_all else 'PROBLEMS'}: {len(items)} cells/exercises in {time.time()-t0:.1f}s")
    return ok_all


def prepare_work():
    os.makedirs(WORK, exist_ok=True)
    for f in glob.glob(os.path.join(ROOT, "data", "*")):
        if os.path.isfile(f):
            shutil.copy(f, WORK)
    os.chdir(WORK)


def main():
    args = sys.argv[1:]
    cur = json.load(open(os.path.join(ROOT, "curriculum.json")))
    ids = [L["id"] for L in cur["lessons"]] if (not args or args == ["--all"]) else args
    prepare_work()
    rt = load_prelude()
    bad = [lid for lid in ids if os.path.exists(os.path.join(ROOT, "lessons", lid + ".html")) and not run_lesson(rt, lid)]
    print("ALL GOOD" if not bad else "PROBLEMS IN: " + ", ".join(bad))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
