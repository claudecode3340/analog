"""HTML helpers that reproduce the original guide's markup exactly (same classes), so new cards look native."""


def K(*keys, bare=False):
    """K('HOME', '>Statistics', '>1-Variable'): '>' marks a menu item; consecutive plain keys are pressed in a row.
    Menu steps get an arrow before them."""
    out = []
    for i, k in enumerate(keys):
        if k.startswith('>'):
            out.append('<span class="arrow">→</span>')
            out.append(f'<span class="k m">{k[1:]}</span>')
        else:
            out.append(f'<span class="k">{k}</span>')
    inner = ''.join(out)
    return inner if bare else f'<span class="keys">{inner}</span>'


def fmt(v):
    if isinstance(v, str): return v
    if abs(v - round(v)) < 1e-9: v = int(round(v))
    s = f'{v}' if isinstance(v, int) else f'{v:.4f}'.rstrip('0').rstrip('.')
    return s.replace('-', '−')


def M(rows, label=None, hl=None):
    """a matrix as the guide draws it; hl = {(i, j): 'h1'|'h2'|'h3'|'dim'|'b'} or a set of (i, j) (→ h1)"""
    n = len(rows[0])
    if hl and not isinstance(hl, dict): hl = {p: 'h1' for p in hl}
    cells = ''.join(f'<div class="{(hl or {}).get((i, j), "")}">{fmt(v)}</div>' for i, r in enumerate(rows) for j, v in enumerate(r))
    lab = f'<span class="lab">{label}</span>' if label else ''
    return f'<span class="mcol"><div class="mat" style="grid-template-columns:repeat({n},auto)">{cells}</div>{lab}</span>'


def MR(*mats):
    return '<div class="mrow">' + ''.join(mats) + '</div>'


def lcd(title, body):
    return f'<div class="mrow"><div class="lcd"><div class="top"><span>{title}</span><span>fx-991CW</span></div>{body}</div></div>'


def lcdmat(title, rows):
    n = len(rows[0])
    cells = ''.join(f'<div class="">{fmt(v)}</div>' for r in rows for v in r)
    return f'<div class="mrow"><div class="lcd"><div class="top"><span>{title}</span><span>fx-991CW</span></div><div class="mat" style="grid-template-columns:repeat({n},auto)">{cells}</div></div></div>'


def mmss(sec):
    return f'{sec // 60}:{sec % 60:02d}'


def card(cid, src, title, stmt, ans, *, kind='', steps=(), concept=None, formula=None, calc=None, fast=(), mis=(), secs=300, marks=None, extra_sol=''):
    """kind: '' past paper · 'tb' textbook · 'sl' slide example · 'dr' practice"""
    aim = int(round(secs * 0.83 / 15) * 15)
    cls = f'src {kind}'.strip()
    h = [f'<div class="prob" id="{cid}">',
         f'  <div class="prob-h"><span class="{cls}">{src}</span><h4>{title}</h4><button class="done-btn" type="button" data-id="{cid}" aria-pressed="false">Mark solved</button></div>',
         f'  <div class="timer" data-id="{cid}" data-total="{secs}" data-aim="{aim}"' + (f' data-marks="{marks}"' if marks else '') + '></div>',
         f'  <div class="stmt">{stmt}</div>']
    if calc:
        body = calc if calc.lstrip().startswith('<') else f'<p>{calc}</p>'
        h.append(f'  <details class="calc-hint" open><summary>fx-991CW makes this much faster — how to use it here</summary><div class="calcq">{body}</div></details>')
    h.append(f'  <details class="s s-ans"><summary>Final answer</summary><div><div class="ansline">{ans}</div></div></details>')
    sol = []
    if concept: sol.append(f'<div class="sol-row"><span class="tag">Concept</span><div>{concept}</div></div>')
    if formula: sol.append(f'<div class="sol-row"><span class="tag">Formula</span><div>{formula}</div></div>')
    if steps: sol.append(walk([('', x, None) for x in steps]))
    sol.append(extra_sol)
    sol.append(f'<div class="sol-row"><span class="tag a">Answer</span><div>{ans}</div></div>')
    h.append(f'  <details class="s s-sol"><summary>Full solution</summary><div>{"".join(sol)}</div></details>')
    fast = list(fast) + [f'Aim for {mmss(aim)} (allotment {mmss(secs)}). If you are stuck at double your share, write the formula with symbols and move on.']
    h.append('  <details class="s s-fast"><summary>Faster in the exam</summary><div><ul>' + ''.join(f'<li>{x}</li>' for x in fast) + '</ul></div></details>')
    if mis: h.append('  <details class="s s-mis"><summary>Common mistakes</summary><div><ul>' + ''.join(f'<li>{x}</li>' for x in mis) + '</ul></div></details>')
    h.append('</div>')
    return '\n'.join(h)


def h3(t): return f'<h3>{t}</h3>'
def note(t): return f'<div class="note">{t}</div>'
def rule(title, eq, idea, watch=None, remember=None):
    dl = f'<dt>Idea</dt><dd>{idea}</dd>' + (f'<dt>Watch out</dt><dd>{watch}</dd>' if watch else '') + (f'<dt>Remember</dt><dd class="hook">{remember}</dd>' if remember else '')
    return f'<div class="rule"><div class="rh">{title}</div>' + (f'<div class="eq">{eq}</div>' if eq else '') + f'<dl>{dl}</dl></div>'
def box(title, body): return f'<div class="box"><h4>{title}</h4>{body}</div>'
def grid2(*b): return '<div class="grid2">' + ''.join(b) + '</div>'
def table(head, rows):
    return '<div class="tw"><table class="t"><tr>' + ''.join(f'<th>{x}</th>' for x in head) + '</tr>' + ''.join('<tr>' + ''.join(f'<td class="l">{c}</td>' for c in r) + '</tr>' for r in rows) + '</table></div>'


# ───────────────────────── pictures: pixel grids as inline SVG ─────────────────────────
_GID = 0


def gsvg(vals, cls=None, path=None, cross=None, cell=46, idx=True, label=None, small=None, maxw=None, ring=None, links=None):
    """vals: 2-D list (numbers or strings). cls: {(i,j): class} with classes in, out, path, p, q, block, c1..c4, n4, nd, ctr, hl.
    path: [(i,j), ...] drawn as numbered arrows. cross: [((i,j),(k,l)), ...] forbidden moves drawn as red dashed lines with ×.
    small: {(i,j): 'text'} small corner labels. ring: [(i,j), ...] cells outlined in red (e.g. the corner pixel that blocks a diagonal)."""
    R, Cn = len(vals), len(vals[0]); cls = cls or {}; pad = 26 if idx else 4
    W, H = pad + Cn * cell + 4, pad + R * cell + 4
    X = lambda j: pad + j * cell + cell / 2
    Y = lambda i: pad + i * cell + cell / 2
    global _GID
    _GID += 1; mid = f'ah{_GID}'
    o = [f'<svg class="gsvg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"' + (f' style="max-width:{maxw}px"' if maxw else '') + '>']
    o.append(f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" class="g-arrowhead"/></marker></defs>')
    if idx:
        for j in range(Cn): o.append(f'<text x="{X(j)}" y="{pad - 9}" class="g-idx">{j}</text>')
        for i in range(R): o.append(f'<text x="{pad - 12}" y="{Y(i) + 5}" class="g-idx">{i}</text>')
    for i in range(R):
        for j in range(Cn):
            c = cls.get((i, j), '')
            o.append(f'<rect x="{pad + j * cell}" y="{pad + i * cell}" width="{cell}" height="{cell}" class="g-cell {"g-" + c if c else ""}"/>')
            v = vals[i][j]
            if v is not None and v != '':
                tc = 'g-val' + (' dk' if c and c != 'out' else ' mu' if c == 'out' else '')
                o.append(f'<text x="{X(j)}" y="{Y(i) + 6}" class="{tc}">{fmt(v) if not isinstance(v, str) else v}</text>')
            if small and (i, j) in small:
                o.append(f'<text x="{pad + j * cell + 5}" y="{pad + i * cell + 13}" class="g-small">{small[(i, j)]}</text>')
    for (i, j) in (ring or []):
        o.append(f'<rect x="{pad + j * cell + 3}" y="{pad + i * cell + 3}" width="{cell - 6}" height="{cell - 6}" rx="6" class="g-ring"/>')
    for (a, b) in (links or []):
        x0, y0, x1, y1 = X(a[1]), Y(a[0]), X(b[1]), Y(b[0])
        o.append(f'<line x1="{x0 + (x1 - x0) * .27:.1f}" y1="{y0 + (y1 - y0) * .27:.1f}" x2="{x1 - (x1 - x0) * .27:.1f}" y2="{y1 - (y1 - y0) * .27:.1f}" class="g-link"/>')
    if path:
        for k in range(1, len(path)):
            (i0, j0), (i1, j1) = path[k - 1], path[k]
            x0, y0, x1, y1 = X(j0), Y(i0), X(j1), Y(i1)
            sh = 0.30  # stop short of the centres so the numbers stay readable
            o.append(f'<line x1="{x0 + (x1 - x0) * sh:.1f}" y1="{y0 + (y1 - y0) * sh:.1f}" x2="{x1 - (x1 - x0) * sh:.1f}" y2="{y1 - (y1 - y0) * sh:.1f}" class="g-arrow" marker-end="url(#{mid})"/>')
        for k, (i, j) in enumerate(path):
            o.append(f'<circle cx="{pad + j * cell + cell - 10}" cy="{pad + i * cell + 10}" r="8" class="g-stepc"/><text x="{pad + j * cell + cell - 10}" y="{pad + i * cell + 14}" class="g-step">{k}</text>')
    for (a, b) in (cross or []):
        (i0, j0), (i1, j1) = a, b
        o.append(f'<line x1="{X(j0)}" y1="{Y(i0)}" x2="{X(j1)}" y2="{Y(i1)}" class="g-cross"/>')
        mx, my = (X(j0) + X(j1)) / 2, (Y(i0) + Y(i1)) / 2
        o.append(f'<circle cx="{mx}" cy="{my}" r="10" class="g-crossc"/><text x="{mx}" y="{my + 5}" class="g-crosst">×</text>')
    o.append('</svg>')
    svg = ''.join(o)
    return f'<figure class="gfig">{svg}' + (f'<figcaption>{label}</figcaption>' if label else '') + '</figure>'


def figs(*f):
    return '<div class="figrow">' + ''.join(f) + '</div>'


def lesson(title, what, body, use=None, tag=None):
    """a full-width teaching block: title, one-line plain meaning, body, and 'where you use it'"""
    t = f'<span class="ltag">{tag}</span>' if tag else ''
    u = f'<div class="use"><b>Where you use it:</b> {use}</div>' if use else ''
    return f'<div class="lesson"><h4>{t}<span>{title}</span></h4><p class="what">{what}</p>{body}{u}</div>'


def cl(keys, means='', screen=''):
    """one calculator line inside a walk step: the keys, what they mean, and (optionally) the screen"""
    return f'<div class="cline"><div class="ckeys">{keys}</div>' + (f'<div class="cmean">{means}</div>' if means else '') + '</div>' + (f'<div class="cscreen">{screen}</div>' if screen else '')


def walk(steps):
    """step-by-step solution: steps = [(title, text, figure_html_or_None, calculator_html_or_None)]"""
    out = ['<div class="walk">']
    for n, st in enumerate(steps, 1):
        st = tuple(st) + (None,) * (4 - len(st))
        title, text, fig, cal = st[:4]
        calbox = f'<div class="wcalc"><div class="wcl">On the fx-991CW</div>{cal}</div>' if cal else ''
        out.append(f'<div class="wstep"><div class="wn">{n}</div><div class="wt">' + (f'<div class="wh">{title}</div>' if title else '') + f'<div>{text}</div>{calbox}</div>' + (f'<div class="wf">{fig}</div>' if fig else '') + '</div>')
    out.append('</div>')
    return ''.join(out)


def extract_div(s, start):
    """return (begin, end) of the balanced <div ...> that starts at index start"""
    i, depth = start, 0
    tag = __import__('re').compile(r'<div\b|</div>')
    for m in tag.finditer(s, start):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return start, m.end()
    raise ValueError('unbalanced div')


def set_solution(card_html, new_inner):
    """replace the card's Full solution with new content"""
    i = card_html.find('<details class="s s-sol">')
    if i < 0: raise ValueError('no solution block')
    import re as _re
    depth, j = 0, -1
    for m in _re.finditer(r'<details\b|</details>', card_html[i:]):
        depth += 1 if m.group(0) != '</details>' else -1
        if depth == 0: j = i + m.end(); break
    if 'class="wcalc"' in new_inner:
        card_html = card_html.replace('<details class="calc-hint" open><summary>fx-991CW makes this much faster — how to use it here', '<details class="calc-hint"><summary>Calculator steps only (the same steps are inside the solution below, next to what each one means)', 1)
        k = card_html.find('<details class="s s-sol">'); j += k - i; i = k
    return card_html[:i] + f'<details class="s s-sol" open><summary>Full solution, step by step</summary><div>{new_inner}</div></details>' + card_html[j:]


import base64 as _b64, os as _os, math as _m
_ASSETS = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'dip-lesson', 'assets')


def img(key, w=220, label=None):
    data = _b64.b64encode(open(_os.path.join(_ASSETS, key + '.webp'), 'rb').read()).decode()
    return f'<figure class="gfig"><img src="data:image/webp;base64,{data}" width="{w}" style="border-radius:8px;display:block" alt="{label or key}">' + (f'<figcaption>{label}</figcaption>' if label else '') + '</figure>'


F_SHAPE = [(0, 0), (0, 1.6), (0.5, 1.6), (0.5, 0.5), (1.1, 0.5), (1.1, 1.2), (1.6, 1.2), (1.6, 0.5), (2.6, 0.5), (2.6, 0)]


def affine_svg(A, label=None, span=(-3.2, 3.6), size=230, before=True):
    """draw the letter F before (grey) and after (orange) the 3×3 affine A; x = row (down), y = column (right)"""
    lo, hi = span; sc = size / (hi - lo)
    P = lambda x, y: ((y - lo) * sc, (x - lo) * sc)  # screen (X right = y, Y down = x)
    def poly(pts, cls):
        return '<polygon points="' + ' '.join(f'{P(x, y)[0]:.1f},{P(x, y)[1]:.1f}' for x, y in pts) + f'" class="{cls}"/>'
    new = [(A[0][0] * x + A[0][1] * y + A[0][2], A[1][0] * x + A[1][1] * y + A[1][2]) for x, y in F_SHAPE]
    ox, oy = P(0, 0)
    o = [f'<svg class="gsvg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">',
         f'<rect x="0" y="0" width="{size}" height="{size}" class="a-bg"/>']
    for k in range(int(_m.ceil(lo)), int(hi) + 1):
        X, Y = P(k, k)
        o.append(f'<line x1="{X:.1f}" y1="0" x2="{X:.1f}" y2="{size}" class="a-grid"/><line x1="0" y1="{Y:.1f}" x2="{size}" y2="{Y:.1f}" class="a-grid"/>')
    o.append(f'<line x1="{ox}" y1="{oy}" x2="{size - 4}" y2="{oy}" class="a-axis"/><line x1="{ox}" y1="{oy}" x2="{ox}" y2="{size - 4}" class="a-axis"/>')
    o.append(f'<text x="{size - 6}" y="{oy - 6}" class="a-lab" text-anchor="end">y →</text><text x="{ox + 6}" y="{size - 8}" class="a-lab">x ↓</text><circle cx="{ox}" cy="{oy}" r="3.5" class="a-o"/>')
    if before: o.append(poly(F_SHAPE, 'a-before'))
    o.append(poly(new, 'a-after'))
    o.append('</svg>')
    return f'<figure class="gfig">{"".join(o)}' + (f'<figcaption>{label}</figcaption>' if label else '') + '</figure>'
