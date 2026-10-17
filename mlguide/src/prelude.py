# Shared Python runtime for the guide. The SAME file runs in the browser (Pyodide worker)
# and in the build harness (CPython), so the reference outputs shown in the guide are
# produced by exactly the code path the learner's "Run" button uses.
import sys, io, ast, base64, traceback, json, os, warnings

os.environ.setdefault("MPLBACKEND", "Agg")
_NS = {}
_MPL_READY = [False]

FRIENDLY = {
    "NameError": "Python doesn't know this name yet. Either it is misspelt, or it was created in a cell "
                 "above that you haven't run. Run the cells above this one (top to bottom), then run this one again.",
    "SyntaxError": "Python could not read this line. Look at the caret ^ below: a missing bracket, quote, colon (:) "
                   "or comma is the usual cause.",
    "IndentationError": "The spaces at the start of a line are wrong. Lines inside a for, if or def must be indented "
                        "by the same amount (4 spaces).",
    "TypeError": "An operation got the wrong kind of value, e.g. adding a number to a string, or calling a function "
                 "with the wrong number of inputs. Read the last line of the message: it names the two types.",
    "ValueError": "The type was right but the value was not acceptable, e.g. int('abc'), or arrays whose shapes "
                  "don't fit together.",
    "IndexError": "You asked for a position that doesn't exist. Python counts from 0, so a list of length 3 has "
                  "positions 0, 1, 2.",
    "KeyError": "That key (column name or dictionary key) doesn't exist. Check the spelling and capital letters; "
                "print the keys or df.columns to see what exists.",
    "AttributeError": "This object has no method or attribute with that name. Check the spelling, and check what "
                      "type the object is with type(x).",
    "ZeroDivisionError": "You divided by zero somewhere.",
    "ModuleNotFoundError": "That library isn't available here. In the browser you have numpy, pandas, matplotlib, "
                           "scikit-learn, statsmodels and ISLP. PyTorch cells run on your Mac (see the setup lesson).",
    "ImportError": "The import failed. Check the spelling of the module and of the name you import from it.",
    "AssertionError": "A check failed.",
}


def _ns(name):
    d = _NS.get(name)
    if d is None:
        d = {"__name__": "__main__", "__builtins__": __builtins__}
        _NS[name] = d
    return d


def reset_ns(name):
    _NS.pop(name, None)


def _mpl_setup():
    if _MPL_READY[0]:
        return
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        plt.rcParams.update({
            "figure.figsize": (6.4, 4.0), "figure.dpi": 110, "savefig.dpi": 110,
            "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
            "grid.alpha": 0.25, "axes.titleweight": "bold", "font.size": 10.5,
            "axes.prop_cycle": matplotlib.cycler(color=["#3B4AD0", "#C0392F", "#1C7650", "#B0520C",
                                                        "#6A3DC4", "#0B7782", "#9A6200", "#5F6573"]),
        })
        plt.show = lambda *a, **k: None
        _MPL_READY[0] = True
    except Exception:
        pass


def _figs():
    out = []
    if "matplotlib.pyplot" not in sys.modules:
        return out
    import matplotlib.pyplot as plt
    for num in plt.get_fignums():
        fig = plt.figure(num)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", facecolor="white")
        out.append({"t": "img", "v": base64.b64encode(buf.getvalue()).decode()})
    plt.close("all")
    return out


def _show(val):
    if val is None:
        return None
    try:
        h = getattr(val, "_repr_html_", None)
        if callable(h) and type(val).__module__.startswith("pandas"):
            html = h()
            if html:
                return {"t": "html", "v": html}
    except Exception:
        pass
    try:
        return {"t": "text", "v": repr(val)}
    except Exception as e:
        return {"t": "text", "v": "<unprintable: %s>" % e}


def _fmt_exc(e, filename):
    et = type(e).__name__
    tb = traceback.extract_tb(e.__traceback__)
    lines = []
    for fr in tb:
        if fr.filename == filename:
            lines.append("  line %d: %s" % (fr.lineno, (fr.line or "").strip()))
    msg = "".join(traceback.format_exception_only(type(e), e)).rstrip()
    text = ("\n".join(lines) + "\n" if lines else "") + msg
    friendly = ""
    for cls in type(e).__mro__:
        if cls.__name__ in FRIENDLY:
            friendly = FRIENDLY[cls.__name__]
            break
    return et, text, friendly


def run(code, ns_name="main", check=None, expect_error=None):
    """Run a cell. Returns a JSON string: {status, outputs:[...], error?, friendly?, fail?}."""
    ns = _ns(ns_name)
    if "matplotlib" in code or "plt." in code or "pandas" in code:
        _mpl_setup()
    out, err = io.StringIO(), io.StringIO()
    old = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = out, err
    res = {"status": "ok", "outputs": []}
    val = None
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            tree = ast.parse(code, "<cell>", "exec")
            last = None
            if tree.body and isinstance(tree.body[-1], ast.Expr) and not code.rstrip().endswith(";"):
                last = ast.Expression(tree.body.pop().value)
            exec(compile(tree, "<cell>", "exec"), ns)
            if last is not None:
                val = eval(compile(last, "<cell>", "eval"), ns)
            if check:
                try:
                    exec(compile(check, "<check>", "exec"), ns)
                except AssertionError as ae:
                    res["status"] = "fail"
                    res["fail"] = str(ae) or "One of the checks did not pass."
    except BaseException as e:  # noqa
        et, text, friendly = _fmt_exc(e, "<cell>")
        if isinstance(e, SyntaxError):
            text = "".join(traceback.format_exception_only(type(e), e)).rstrip()
        if expect_error and et == expect_error:
            res["status"] = "expected"
        else:
            res["status"] = "error"
        res["error"] = text
        res["etype"] = et
        res["friendly"] = friendly
    finally:
        sys.stdout, sys.stderr = old
    s = out.getvalue()
    if s:
        res["outputs"].append({"t": "text", "v": s})
    e2 = err.getvalue()
    if e2.strip():
        res["outputs"].append({"t": "stderr", "v": e2})
    res["outputs"].extend(_figs())
    if res["status"] in ("ok", "fail"):
        sv = _show(val)
        if sv:
            res["outputs"].append(sv)
    return json.dumps(res)


def setup_pandas():
    try:
        import pandas as pd
        pd.set_option("display.max_rows", 20)
        pd.set_option("display.max_columns", 14)
        pd.set_option("display.width", 120)
    except Exception:
        pass
