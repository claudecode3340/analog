#!/usr/bin/env python
"""Assemble the single-file guide.

  python /home/user/analog/mlguide/tools/build.py            # full build -> dist/ML_Foundations_M1-3.html
  python /home/user/analog/mlguide/tools/build.py --check    # validate lessons only (no output)
  python /home/user/analog/mlguide/tools/build.py --only isl2-1,isl2-2   # build a preview with just these lessons

Validation (fails the build): duplicate ids, missing figures, broken #links, a .predict not followed by a
.py/.widget, exercises missing parts, quizzes without answers, unknown widgets, maths errors (KaTeX).
"""
import sys, os, json, re, base64, glob, io, zipfile, subprocess, html as H
from bs4 import BeautifulSoup, NavigableString

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, LES, FIGS, DATA, WID = (os.path.join(ROOT, d) for d in ("src", "lessons", "figs", "data", "widgets"))
KATEX = os.path.join(ROOT, "tools", "node_modules", "katex", "dist")
ERR = []


def err(msg):
    ERR.append(msg)


def rd(p):
    return open(p, encoding="utf-8").read()


def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()


def katex_css():
    css = rd(os.path.join(KATEX, "katex.min.css"))
    def rep(m):
        f = m.group(1)
        if not f.endswith(".woff2"):
            return "url()"
        return "url(data:font/woff2;base64," + b64(os.path.join(KATEX, f)) + ")"
    css = re.sub(r"url\((fonts/[^)]+)\)", rep, css)
    css = re.sub(r",\s*url\(\)\s*format\(\"woff\"\)", "", css)
    css = re.sub(r",\s*url\(\)\s*format\(\"truetype\"\)", "", css)
    return css


KIND_LABEL = {"tool": "Python & tools", "math": "Maths", "isl": "ISLP", "udl": "Prince · UDL", "proj": "Project", "start": "Start here", "review": "Review"}


def lesson_html(L, cur, manifest, widgets, outputs_ids):
    path = os.path.join(LES, L["id"] + ".html")
    if not os.path.exists(path):
        return None
    soup = BeautifulSoup(rd(path), "html.parser")
    sec = soup.find("section")
    if sec is None or sec.get("id") != L["id"]:
        err(f"{L['id']}: file must contain one <section class=\"lesson\" id=\"{L['id']}\">")
        return None
    sec["class"] = list(set((sec.get("class") or []) + ["lesson", "k-" + L["kind"]]))
    for k in ("month", "week", "kind", "title", "short"):
        sec["data-" + k] = str(L[k])
    # ---- header
    head = soup.new_tag("div", attrs={"class": "lhead"})
    kick = soup.new_tag("div", attrs={"class": "kick"})
    c = soup.new_tag("span", attrs={"class": "chip kind"}); c.string = KIND_LABEL[L["kind"]]; kick.append(c)
    if L["week"]:
        c = soup.new_tag("span", attrs={"class": "chip"}); c.string = f"Month {L['month']} · Week {L['week']}"; kick.append(c)
    if sec.get("data-book"):
        c = soup.new_tag("span", attrs={"class": "chip book"}); c.string = sec["data-book"]; kick.append(c)
    c = soup.new_tag("span", attrs={"class": "chip time"}); c.string = f"about {L['mins'] // 60} h {L['mins'] % 60:02d} min" if L["mins"] >= 60 else f"about {L['mins']} min"; kick.append(c)
    head.append(kick)
    h2 = soup.new_tag("h2", attrs={"class": "lt"}); h2.string = L["title"]; head.append(h2)
    lede = sec.find(class_="lede", recursive=False)
    if lede:
        lede.extract(); head.append(lede)
    else:
        err(f"{L['id']}: missing <p class=\"lede\"> (2–3 sentences: why this lesson matters)")
    sec.insert(0, head)
    # ---- figures
    for f in sec.select("figure.book"):
        fid = f.get("data-fig")
        m = manifest.get(fid)
        if not m:
            err(f"{L['id']}: figure {fid} not found in figs/ (ids look like islp-2.9 or udl-3.3)")
            continue
        img_path = os.path.join(FIGS, fid + ".webp")
        holder = soup.new_tag("div", attrs={"class": "fimg"})
        img = soup.new_tag("img", attrs={"src": "data:image/webp;base64," + b64(img_path), "alt": m.get("caption", "")[:300], "loading": "lazy", "width": str(m.get("w", "")), "height": str(m.get("h", ""))})
        holder.append(img)
        f.insert(0, holder)
        cap = f.find("figcaption")
        if cap is None:
            cap = soup.new_tag("figcaption"); f.append(cap)
        book = "ISLP" if fid.startswith("islp") else "Prince"
        tag = soup.new_tag("span", attrs={"class": "ftag"}); tag.string = f"From the book · {book} Figure {fid.split('-',1)[1]}"
        cap.insert(0, tag)
        if not f.has_attr("data-nobookcap") and m.get("caption"):
            d = soup.new_tag("details"); s = soup.new_tag("summary"); s.string = "The book's own caption"; d.append(s)
            p = soup.new_tag("div"); p.string = m["caption"]; d.append(p); cap.append(d)
        f["class"] = list(set((f.get("class") or []) + ["k-" + ("isl" if book == "ISLP" else "udl")]))
    # ---- component checks
    for p in sec.select(".predict"):
        nx = p.find_next_sibling()
        if nx is None or not ({"py", "widget"} & set(nx.get("class", []))):
            err(f"{L['id']}: a .predict must be immediately followed by a .py cell or .widget")
        if not p.get("data-correct") or not p.select(".opts > li"):
            err(f"{L['id']}: .predict needs data-correct and <ol class=\"opts\"><li>…")
    for x in sec.select(".ex"):
        if not (x.select_one("pre.src") and x.select_one("pre.check") and x.select_one("pre.solution") and x.select_one(".task")):
            err(f"{L['id']}: exercise {x.get('id')} needs .task, pre.src, pre.check, pre.solution")
        if x.get("id") and x["id"] + ":solution" not in outputs_ids:
            err(f"{L['id']}: exercise {x.get('id')} has not been verified (run tools/run_cells.py {L['id']})")
    for c in sec.select(".py"):
        if c.get("id") and c["id"] not in outputs_ids:
            err(f"{L['id']}: cell {c.get('id')} has no reference output (run tools/run_cells.py {L['id']})")
    for q in sec.select(".quiz .q"):
        t = q.get("data-type", "mcq")
        if t == "mcq" and not (q.get("data-correct") and q.select(".opts > li") and q.select_one(".why")):
            err(f"{L['id']}: mcq needs data-correct, .opts and .why: {q.get_text()[:80]}")
        if t == "num" and not q.get("data-answer"):
            err(f"{L['id']}: numeric question needs data-answer: {q.get_text()[:80]}")
    for w in sec.select(".widget"):
        if w.get("data-w") not in widgets:
            err(f"{L['id']}: unknown widget '{w.get('data-w')}' (register it with G.widget('{w.get('data-w')}', fn) in widgets/*.js)")
    # ---- done bar
    idx = [x["id"] for x in cur["lessons"]].index(L["id"])
    nxt = cur["lessons"][idx + 1] if idx + 1 < len(cur["lessons"]) else None
    done = BeautifulSoup(
        f'<div class="ldone" data-lesson="{L["id"]}"><label><input type="checkbox"> I can do this lesson without help</label>'
        + ('<button class="nbbtn" type="button">⬇ Download as a Jupyter notebook</button>' if sec.select(".py, .ex") else "")
        + (f'<span class="nx">Next: <a href="#{nxt["id"]}">{H.escape(nxt["short"])}</a></span>' if nxt else "") + "</div>", "html.parser")
    sec.append(done)
    return sec


def text_md(node):
    t = node.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", t)


def notebook(sec):
    cells = [{"cell_type": "markdown", "metadata": {}, "source": [f"# {sec['data-title']}\n\nFrom *ML Foundations · Months 1–3*. Put this notebook in your `~/ml-course` folder (next to the data files), "
                                                                  "open it in VS Code or JupyterLab and run the cells top to bottom with Shift+Enter."]}]
    for it in sec.select(".py, .ex"):
        if "py" in it.get("class", []):
            note = it.select_one(".pynote")
            if note:
                cells.append({"cell_type": "markdown", "metadata": {}, "source": [text_md(note)]})
            cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": [it.select_one("pre.src").get_text().strip("\n")]})
        else:
            cells.append({"cell_type": "markdown", "metadata": {}, "source": ["## Your turn: " + it.get("data-title", "exercise") + "\n\n" + text_md(it.select_one(".task"))]})
            cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": [it.select_one("pre.src").get_text().strip("\n")]})
            cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": ["# Run this cell to check your answer. If nothing is printed except 'All tests passed', you're done.\n" + it.select_one("pre.check").get_text().strip("\n") + "\nprint('All tests passed')"]})
    return {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}


def review_sections(cur, soup_all):
    sheet = ['<section class="lesson" id="review-sheet"><p class="lede">Every boxed formula from every lesson, in order, with a one-line meaning. Click a lesson name to jump back to where it is taught.</p>']
    for sec in soup_all:
        blocks = sec.select(".mathblock[data-sheet]")
        if not blocks:
            continue
        sheet.append(f'<h3>{H.escape(sec["data-title"])} <a href="#{sec["id"]}" style="font-size:14px">open lesson ↗</a></h3>')
        for b in blocks:
            bb = BeautifulSoup(str(b), "html.parser").find()
            bb["data-sheet-copy"] = "1"
            for t in bb.select("[id]"):
                del t["id"]
            sheet.append(str(bb))
    sheet.append('<h3 id="glossary-h">Glossary</h3><div id="gloss-list"></div></section>')
    deck = '<section class="lesson" id="review-deck"><p class="lede">Every flashcard from every lesson you have started lands here, scheduled with FSRS-6 (the same memory model as your COMSYS drill). Ten minutes a day keeps everything you learned this month alive.</p><div class="deck" id="deck"></div></section>'
    tests = ['<section class="lesson" id="review-tests"><p class="lede">One random question from every lesson of the month. A miss links back to the lesson that teaches it. Press “New test” for a fresh draw.</p>']
    for m in ("1", "2", "3"):
        tests.append(f'<h3>{H.escape(cur["months"][m])}</h3><div class="mtest" data-month="{m}"></div>')
    tests.append("</section>")
    return {"review-deck": deck, "review-tests": "".join(tests), "review-sheet": "".join(sheet)}


def main():
    args = sys.argv[1:]
    check_only = "--check" in args
    only = None
    cur = json.load(open(os.path.join(ROOT, "curriculum.json")))
    release = None
    if "--only" in args:
        only = set(args[args.index("--only") + 1].split(","))
    if "--months" in args:  # a release of months 1..N: lessons of those months, review sections, links to later months shown as "coming soon"
        release = int(args[args.index("--months") + 1])
        only = {L["id"] for L in cur["lessons"] if L["kind"] != "review" and L["month"].isdigit() and int(L["month"]) <= release}
    manifest = {}
    mp = os.path.join(FIGS, "manifest.json")
    if os.path.exists(mp):
        for m in json.load(open(mp)):
            manifest[m["id"]] = m
    wsrc = "".join(rd(f) + "\n" for f in sorted(glob.glob(os.path.join(WID, "*.js"))))
    widgets = set(re.findall(r"G\.widget\(\s*['\"]([\w-]+)['\"]", wsrc))
    outputs = {}
    for f in glob.glob(os.path.join(ROOT, "build", "outputs", "*.json")):
        outputs.update(json.load(open(f)))
    secs, nbs, missing = [], {}, []
    for L in cur["lessons"]:
        if L["kind"] == "review" or (only and L["id"] not in only and L["id"] != "s0-how"):
            continue
        s = lesson_html(L, cur, manifest, widgets, outputs)
        if s is None:
            missing.append(L["id"]); continue
        secs.append(s)
        if s.select(".py, .ex"):
            nbs[L["id"]] = notebook(s)
    # ids & links
    ids = {}
    for s in secs:
        for t in s.select("[id]"):
            if t["id"] in ids:
                err(f"duplicate id '{t['id']}' in {s['id']} and {ids[t['id']]}")
            ids[t["id"]] = s["id"]
    rev = review_sections(cur, secs)
    rev_ids = {"review-deck", "review-tests", "review-sheet", "glossary-h"}
    for s in secs:
        for a in s.select('a[href^="#"]'):
            h = a["href"][1:]
            later = next((L for L in cur["lessons"] if L["id"] == h), None)
            if h and h not in ids and h not in rev_ids and not (only and later):
                err(f"{s['id']}: link to #{h} goes nowhere")
            elif release and h and h not in ids and h not in rev_ids and later:
                sp = s.new_tag("span", attrs={"class": "later", "title": f"Coming in Month {later['month']}"})
                sp.string = a.get_text()
                a.replace_with(sp)
    # glossary
    gloss = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "glossary", "*.json"))):
        for k, v in json.load(open(f)).items():
            gloss[k] = v
    if missing:
        print("lessons not written yet:", ", ".join(missing))
    if ERR:
        print("\n".join("ERROR " + e for e in ERR))
        print(f"{len(ERR)} problem(s)")
        if check_only or not only or release:
            sys.exit(1)
    if check_only:
        print("check ok"); return
    # ---- data for the browser
    pyfiles = {}
    for f in sorted(glob.glob(os.path.join(DATA, "*"))):
        if os.path.isfile(f) and not f.endswith(".zip"):
            pyfiles[os.path.basename(f)] = b64(f)
    pyzips = {}
    for f in sorted(glob.glob(os.path.join(DATA, "*.zip"))):
        pyzips[os.path.basename(f)[:-4]] = b64(f)
    dp = io.BytesIO()
    with zipfile.ZipFile(dp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(glob.glob(os.path.join(DATA, "*"))):
            if os.path.isfile(f) and not f.endswith(".zip"):
                z.write(f, "ml-course/" + os.path.basename(f))
        for lid, nb in nbs.items():
            z.writestr(f"ml-course/notebooks/{lid}.ipynb", json.dumps(nb, indent=1))
    datapack = {"b64": base64.b64encode(dp.getvalue()).decode()}
    used_outs = {k: v for k, v in outputs.items() if k.split(":")[0] in ids}
    for k in list(used_outs):
        if k.endswith(":solution"):
            del used_outs[k]
    order = [L["id"] for L in cur["lessons"]]
    body = []
    for L in cur["lessons"]:
        if L["kind"] == "review":
            if only and not release:
                continue
            body.append(rev[L["id"]].replace('class="lesson"', f'class="lesson k-review" data-month="R" data-week="" data-kind="review" data-title="{H.escape(L["title"])}" data-short="{H.escape(L["short"])}"', 1))
        else:
            s = next((x for x in secs if x["id"] == L["id"]), None)
            if s is not None:
                body.append(str(s))
    def mcard(m):
        first = next((L["id"] for L in cur["lessons"] if L["month"] == m), "")
        if first not in ids:
            return f'<div class="soon" data-m="{m}"><h4>{H.escape(cur["months"][m])}</h4><p class="cnt">Coming soon</p></div>'
        return f'<a href="#{first}" data-m="{m}"><h4>{H.escape(cur["months"][m])}</h4><p class="cnt"></p><div class="mbar"><i></i></div></a>'
    months_cards = "".join(mcard(m) for m in ("1", "2", "3"))
    hero = f'''<header class="hero"><div class="kick"><span class="chip kind k-start">Your ML / DL / CV path · part 1</span><span class="chip">ISLP · Prince UDL · Python · NumPy · PyTorch</span></div>
<h1>Learn machine learning <em>from zero</em>,<br>one worked example at a time.</h1>
<p>Twelve weeks. You start by typing your first line of Python and finish by training a neural network you wrote yourself, in NumPy and then in PyTorch. Every idea is built from the ground up, shown with real numbers, drawn, run, and practised until it sticks.</p>
<div class="monthcards">{months_cards}</div></header>'''
    rail = '''<aside class="rail" aria-label="Contents">
<div class="brand"><i>∂</i><div>ML Foundations<small>Months 1–3 · from zero</small></div></div>
<div class="rprog"><div class="bar"><i id="rprog-bar"></i></div><span><b id="rprog-n">0</b> of <b id="rprog-t">0</b> lessons done</span></div>
<div class="rbtns"><a class="rbtn" href="#review-deck">Flashcards <span class="n" id="due-n">0</span></a><a class="rbtn" href="#s0-setup">Mac setup</a></div>
<div class="legend"><span class="k-tool"><i></i>Python &amp; tools</span><span class="k-math"><i></i>Maths</span><span class="k-isl"><i></i>ISLP</span><span class="k-udl"><i></i>Prince</span><span class="k-proj"><i></i>Project</span></div>
<nav class="toc" id="toc"></nav></aside>'''
    top = '''<header class="topbar"><button class="tbtn menu-btn" id="menubtn" aria-label="Open contents">☰</button><div class="where"><b id="where-t">ML Foundations</b><span id="where-k"></span></div>
<button class="lmap" id="lmap" type="button" aria-label="Lesson map"></button><button class="pystat" id="pystat" type="button" title="Start Python now" style="border:0;background:transparent;cursor:pointer"><i></i><span>Python: starts on first Run</span></button>
<button class="tbtn" id="searchbtn" type="button">Search <kbd>⌘K</kbd></button><button class="tbtn" id="themebtn" type="button" aria-label="Light or dark">◐</button></header>'''
    def js_json(id_, obj):
        return f'<script type="application/json" id="{id_}">' + json.dumps(obj, separators=(",", ":")).replace("</", "<\\/") + "</script>"
    css = rd(os.path.join(SRC, "fonts.css")) + katex_css() + rd(os.path.join(SRC, "style.css"))
    content = hero + "\n".join(body)
    page = ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>ML Foundations · Months 1–3</title><style>{css}</style></head><body><div class=\"app\">{rail}<div class=\"main\">{top}<main class=\"content\">{content}</main></div></div>"
            + js_json("months", cur["months"]) + js_json("outputs", used_outs) + js_json("glossary", gloss) + js_json("notebooks", nbs)
            + js_json("pyfiles", pyfiles) + js_json("pyzips", pyzips) + js_json("datapack", datapack)
            + '<script type="text/plain" id="pyworker-src">' + rd(os.path.join(SRC, "pyworker.js")).replace("</", "<\\/") + "</script>"
            + '<script type="text/plain" id="prelude-src">' + rd(os.path.join(SRC, "prelude.py")) + "</script>"
            + "<script>" + rd(os.path.join(KATEX, "katex.min.js")) + "</script>"
            + "<script>" + rd(os.path.join(SRC, "fsrs6.js")) + "</script>"
            + "<script>" + rd(os.path.join(SRC, "runtime.js")) + "\n" + wsrc + "\n" + glossary_js() + "</script></body></html>")
    os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
    tag = ("-" + "+".join(sorted(only))[:80]) if only else ""
    if release:
        tag = f"-M1-{release}" if release > 1 else "-M1"
    raw = os.path.join(ROOT, "build", f"raw{tag}.html")
    open(raw, "w", encoding="utf-8").write(page)
    out = os.path.join(ROOT, "dist", "ML_Foundations_M1-3.html" if not only else (f"ML_Foundations{tag}.html" if release else f"preview{tag}.html"))
    r = subprocess.run(["node", os.path.join(ROOT, "tools", "katex_render.js"), raw, out], capture_output=True, text=True)
    print(r.stdout.strip(), r.stderr.strip()[:6000])
    if r.returncode != 0:
        sys.exit(2)
    print(f"wrote {out} ({os.path.getsize(out)/1e6:.1f} MB), {len(secs)} lessons")


def glossary_js():
    # Fill the glossary list in the review sheet from the glossary JSON.
    return """document.addEventListener('guide:ready',function(){var g=document.getElementById('gloss-list');if(!g)return;var d=JSON.parse(document.getElementById('glossary').textContent||'{}');
var ks=Object.keys(d).sort(function(a,b){return d[a].term.localeCompare(d[b].term)});g.className='symbols';g.innerHTML='<div class="row h"><span>Term</span><span>Meaning</span><span>Taught in</span></div>'+ks.map(function(k){var x=d[k];return '<div class="row"><span class="s" style="font-size:16px;font-weight:700">'+G.esc(x.term)+'</span><span>'+x.def+'</span><span class="eg">'+(x.at?'<a href="#'+x.at+'">open ↗</a>':'')+'</span></div>'}).join('');G.renderMath(g);});"""


if __name__ == "__main__":
    main()
