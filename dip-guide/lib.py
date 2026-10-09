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
    if steps: sol.append('<ol class="steps">' + ''.join(f'<li>{x}</li>' for x in steps) + '</ol>')
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
