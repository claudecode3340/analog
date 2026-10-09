"""Helpers for Chapter 3 walkthroughs: equalisation tables, bar charts, filter windows (all computed with numpy)."""
import json, os
import numpy as np
from lib import *

ANS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dip-lesson', 'num', 'answers.json')))
r4 = lambda v: fmt(round(float(v), 4))
half_up = lambda v: int(np.floor(v + 0.5))


def eq_table(nk, L=None, MN=None, show_p=False):
    L = L or len(nk); MN = MN or sum(nk)
    run = np.cumsum(nk); s = (L - 1) * run / MN
    head = ['r<sub>k</sub>', 'n<sub>k</sub> (pixels at r<sub>k</sub>)'] + (['p<sub>r</sub> = n<sub>k</sub>/MN'] if show_p else []) + ['running total', f's = {L - 1} × running ÷ {MN}', 'rounded s']
    rows = [[k, nk[k]] + ([r4(nk[k] / MN)] if show_p else []) + [int(run[k]), r4(s[k]), f'<b>{half_up(s[k])}</b>'] for k in range(L)]
    return table(head, rows), [half_up(v) for v in s]


def moved_hist(nk, sr, L=None):
    L = L or len(nk); h = [0] * L
    for k, v in enumerate(nk): h[sr[k]] += v
    return h


def bars(counts, label=None, w=300, h=120, hl=None):
    n = len(counts); mx = max(counts) or 1; bw = (w - 20) / n
    o = [f'<svg class="gsvg" viewBox="0 0 {w} {h + 28}" width="{w}" height="{h + 28}"><rect x="0" y="0" width="{w}" height="{h + 28}" class="a-bg"/>']
    for k, c in enumerate(counts):
        bh = (h - 22) * c / mx; x = 10 + k * bw
        o.append(f'<rect x="{x + 2:.1f}" y="{h - bh:.1f}" width="{bw - 4:.1f}" height="{bh:.1f}" rx="2" class="{"b-hl" if hl and k in hl else "b-bar"}"/>')
        if c: o.append(f'<text x="{x + bw / 2:.1f}" y="{h - bh - 4:.1f}" class="a-lab" text-anchor="middle">{fmt(c)}</text>')
        o.append(f'<text x="{x + bw / 2:.1f}" y="{h + 16}" class="a-lab" text-anchor="middle">{k}</text>')
    o.append('</svg>')
    return f'<figure class="gfig">{"".join(o)}' + (f'<figcaption>{label}</figcaption>' if label else '') + '</figure>'


def pad(f, a, mode):
    return np.pad(np.asarray(f, float), a, {'zero': 'constant', 'replicate': 'edge', 'mirror': 'symmetric'}[mode])


def window_fig(f, x, y, w, mode='zero', conv=False, scale=1, label_kernel='kernel', note=None):
    """three pictures: padded image with the 3×3 window, the kernel (rotated if convolution), and the products; plus the sum"""
    f = np.asarray(f, float); w = np.asarray(w, float); a = w.shape[0] // 2
    fp = pad(f, a, mode); wk = np.rot90(w, 2) if conv else w
    win = fp[x:x + 2 * a + 1, y:y + 2 * a + 1]
    prod = win * wk
    m, n = f.shape
    cls = {}
    for i in range(m + 2 * a):
        for j in range(n + 2 * a):
            inside = a <= i < m + a and a <= j < n + a
            cls[(i, j)] = 'out' if not inside else ''
            if x <= i < x + 2 * a + 1 and y <= j < y + 2 * a + 1: cls[(i, j)] = 'hl' if inside else 'block'
    total = prod.sum() * scale
    R = lambda A: [[fmt(round(float(v), 4)) for v in r] for r in A]
    cw = lambda A: max(36, 9 * max(len(str(v)) for r in A for v in r) + 16)
    fpv, wkv, prv = R(fp), R(wk), R(prod)
    fig = figs(gsvg(fpv, cls, cell=cw(fpv), idx=False, label=f'{mode}-padded image; yellow/red = the window around ({x}, {y}) (red = padding)'),
               gsvg(wkv, {(i, j): 'n4' for i in range(2 * a + 1) for j in range(2 * a + 1)}, cell=cw(wkv), idx=False, label=label_kernel + (' rotated 180°' if conv else '')),
               gsvg(prv, {(i, j): 'n8' for i in range(2 * a + 1) for j in range(2 * a + 1)}, cell=cw(prv), idx=False, label='window × kernel, entry by entry'))
    return fig, total


def filt(f, w, mode='zero', conv=False):
    f = np.asarray(f, float); w = np.asarray(w, float); a = w.shape[0] // 2
    fp = pad(f, a, mode); wk = np.rot90(w, 2) if conv else w
    m, n = f.shape
    return np.array([[(fp[i:i + 2 * a + 1, j:j + 2 * a + 1] * wk).sum() for j in range(n)] for i in range(m)])


def tcurve(f, label=None, pts=None, size=190, L=256):
    """plot s = T(r) on 0..L-1 (input → right, output ↑), with the dashed 45° identity"""
    p = 18; W = size; S = (W - 2 * p) / (L - 1)
    X = lambda r: p + r * S; Y = lambda s: W - p - s * S
    path = ' '.join(f'{X(r):.1f},{Y(min(max(f(r), 0), L - 1)):.1f}' for r in np.linspace(0, L - 1, 120))
    o = [f'<svg class="gsvg" viewBox="0 0 {W} {W}" width="{W}" height="{W}"><rect x="0" y="0" width="{W}" height="{W}" class="a-bg"/>',
         f'<line x1="{X(0)}" y1="{Y(0)}" x2="{X(L - 1)}" y2="{Y(L - 1)}" class="a-grid" stroke-dasharray="4 4"/>',
         f'<line x1="{X(0)}" y1="{Y(0)}" x2="{X(L - 1)}" y2="{Y(0)}" class="a-axis"/><line x1="{X(0)}" y1="{Y(0)}" x2="{X(0)}" y2="{Y(L - 1)}" class="a-axis"/>',
         f'<polyline points="{path}" fill="none" stroke="#c2410c" stroke-width="3"/>',
         f'<text x="{W - p}" y="{W - 4}" class="a-lab" text-anchor="end">input r →</text><text x="{p + 4}" y="{p - 4}" class="a-lab">output s ↑</text>']
    for (r, s, t) in (pts or []):
        o.append(f'<circle cx="{X(r):.1f}" cy="{Y(s):.1f}" r="4.5" fill="#c2410c"/><text x="{X(r) + 7:.1f}" y="{Y(s) + 4:.1f}" class="a-lab">{t}</text>')
    o.append('</svg>')
    return f'<figure class="gfig">{"".join(o)}' + (f'<figcaption>{label}</figcaption>' if label else '') + '</figure>'


def hist_fig(key, label=None, w=240, h=90, bins=32):
    from PIL import Image
    a = np.asarray(Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dip-lesson', 'assets', key + '.webp')).convert('L')).astype(int)
    c = np.bincount(a.ravel() * bins // 256, minlength=bins); mx = c.max(); bw = (w - 10) / bins
    o = [f'<svg class="gsvg" viewBox="0 0 {w} {h + 18}" width="{w}" height="{h + 18}"><rect x="0" y="0" width="{w}" height="{h + 18}" class="a-bg"/>']
    for k, v in enumerate(c):
        bh = (h - 6) * v / mx
        o.append(f'<rect x="{5 + k * bw:.1f}" y="{h - bh:.1f}" width="{bw - 1:.1f}" height="{bh:.1f}" class="b-bar"/>')
    o.append(f'<text x="5" y="{h + 14}" class="a-lab">0</text><text x="{w - 5}" y="{h + 14}" class="a-lab" text-anchor="end">255</text></svg>')
    return f'<figure class="gfig">{"".join(o)}' + (f'<figcaption>{label}</figcaption>' if label else '') + '</figure>'


def photo_with_hist(key, label, w=200):
    return f'<div style="display:flex;flex-direction:column;gap:6px;align-items:center">{img(key, w)}{hist_fig(key, label, w=w)}</div>'
