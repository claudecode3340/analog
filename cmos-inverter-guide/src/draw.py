"""Tiny schematic-drawing kit on top of matplotlib (consistent look for every circuit)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle, FancyBboxPatch
import numpy as np

N = '#2563eb'      # NMOS blue
P = '#ea580c'      # PMOS orange
PU = '#7c3aed'     # purple accent
G = '#059669'      # green
R = '#dc2626'      # red
INK = '#1f2937'
MUT = '#6b7280'
LIGHT = '#e5e7eb'
AMB = '#b45309'

plt.rcParams.update({
    'font.family': 'Inter', 'font.size': 11, 'mathtext.fontset': 'cm',
    'svg.fonttype': 'path', 'axes.edgecolor': '#9ca3af', 'axes.labelcolor': INK,
    'xtick.color': '#4b5563', 'ytick.color': '#4b5563', 'axes.linewidth': 0.9,
    'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True,
    'grid.color': '#eef0f3', 'grid.linewidth': 0.8, 'axes.axisbelow': True,
    'legend.frameon': False, 'axes.titlesize': 11.5, 'axes.titleweight': 'semibold',
    'axes.titlecolor': INK, 'axes.labelsize': 11.5,
})

LW = 1.7
S = 0.40  # inches per schematic unit


def canvas(x0, x1, y0, y1, scale=S):
    fig = plt.figure(figsize=((x1 - x0) * scale, (y1 - y0) * scale))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
    ax.set_aspect('equal'); ax.axis('off')
    return fig, ax


def save(fig, name, out='figs'):
    fig.savefig(f'{out}/{name}.svg', bbox_inches='tight', pad_inches=0.04, transparent=True)
    import os
    if os.environ.get('PREVIEW'):
        os.makedirs('prev', exist_ok=True)
        fig.savefig(f'prev/{name}.png', bbox_inches='tight', pad_inches=0.04, dpi=90, facecolor='white')
    plt.close(fig)


def wire(ax, pts, c=INK, lw=LW, ls='-', z=2):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=c, lw=lw, ls=ls, solid_capstyle='round', solid_joinstyle='round', zorder=z)


def dot(ax, x, y, c=INK, r=0.075):
    ax.add_patch(Circle((x, y), r, color=c, zorder=5))


def term(ax, x, y, c=INK, r=0.1):
    ax.add_patch(Circle((x, y), r, facecolor='white', edgecolor=c, lw=LW, zorder=6))


def txt(ax, x, y, s, c=INK, size=11, ha='center', va='center', **kw):
    ax.text(x, y, s, color=c, fontsize=size, ha=ha, va=va, zorder=8, **kw)


def vdd(ax, x, y, label=r'$V_{DD}$', c=INK, size=12):
    wire(ax, [(x - 0.32, y), (x + 0.32, y)], c, lw=2.2)
    if label:
        txt(ax, x, y + 0.32, label, c, size)


def gnd(ax, x, y, c=INK):
    wire(ax, [(x, y), (x, y - 0.18)], c)
    for i, w in enumerate([0.34, 0.22, 0.10]):
        wire(ax, [(x - w, y - 0.18 - i * 0.11), (x + w, y - 0.18 - i * 0.11)], c, lw=1.6)


def mos(ax, x, y, kind='n', c=None, label=None, lsize=12, label_dx=0.62):
    """Vertical MOSFET, gate on the left. (x, y) = channel centre.
    Returns dict of terminal points g, d, s (drain/source at x+0.45, y±0.9)."""
    c = c or (N if kind == 'n' else P)
    wire(ax, [(x, y - 0.42), (x, y + 0.42)], c, lw=2.4)
    wire(ax, [(x - 0.2, y - 0.32), (x - 0.2, y + 0.32)], c, lw=2.4)
    if kind == 'p':
        ax.add_patch(Circle((x - 0.29, y), 0.09, facecolor='white', edgecolor=c, lw=LW, zorder=6))
        wire(ax, [(x - 0.38, y), (x - 0.75, y)], c)
    else:
        wire(ax, [(x - 0.2, y), (x - 0.75, y)], c)
    top = [(x, y + 0.3), (x + 0.45, y + 0.3), (x + 0.45, y + 0.9)]
    bot = [(x, y - 0.3), (x + 0.45, y - 0.3), (x + 0.45, y - 0.9)]
    wire(ax, top, c); wire(ax, bot, c)
    if kind == 'n':
        ax.add_patch(FancyArrowPatch((x + 0.06, y - 0.3), (x + 0.4, y - 0.3), arrowstyle='-|>',
                                     mutation_scale=15, color=c, lw=0, zorder=6))
        d, s = (x + 0.45, y + 0.9), (x + 0.45, y - 0.9)
    else:
        ax.add_patch(FancyArrowPatch((x + 0.42, y + 0.3), (x + 0.06, y + 0.3), arrowstyle='-|>',
                                     mutation_scale=15, color=c, lw=0, zorder=6))
        d, s = (x + 0.45, y - 0.9), (x + 0.45, y + 0.9)
    if label:
        txt(ax, x + label_dx, y, label, c, lsize, ha='left')
    return {'g': (x - 0.75, y), 'd': d, 's': s}


def cap(ax, x, ytop, c=INK, label=None, lsize=11, lead=0.45, ldx=0.38, w=0.32):
    y1 = ytop - lead
    wire(ax, [(x, ytop), (x, y1)], c)
    wire(ax, [(x - w, y1), (x + w, y1)], c, lw=2.4)
    wire(ax, [(x - w, y1 - 0.16), (x + w, y1 - 0.16)], c, lw=2.4)
    wire(ax, [(x, y1 - 0.16), (x, y1 - 0.16 - lead)], c)
    if label:
        txt(ax, x + ldx, y1 - 0.08, label, c, lsize, ha='left')
    return y1 - 0.16 - lead


def res(ax, x, ytop, length=1.4, c=INK, label=None, lsize=11, ldx=0.35):
    lead = (length - 0.9) / 2
    pts = [(x, ytop), (x, ytop - lead)]
    n = 6
    for i in range(n):
        pts.append((x + (0.18 if i % 2 == 0 else -0.18), ytop - lead - (i + 0.5) * 0.9 / n))
    pts += [(x, ytop - lead - 0.9), (x, ytop - length)]
    wire(ax, pts, c)
    if label:
        txt(ax, x + ldx, ytop - length / 2, label, c, lsize, ha='left')
    return ytop - length


def isrc(ax, x, ytop, length=1.4, c=INK, label=None, lsize=11, up=False, ldx=0.42):
    cy = ytop - length / 2
    wire(ax, [(x, ytop), (x, cy + 0.32)], c)
    wire(ax, [(x, cy - 0.32), (x, ytop - length)], c)
    ax.add_patch(Circle((x, cy), 0.32, facecolor='white', edgecolor=c, lw=LW, zorder=4))
    a, b = (cy + 0.2, cy - 0.2) if not up else (cy - 0.2, cy + 0.2)
    ax.add_patch(FancyArrowPatch((x, a), (x, b), arrowstyle='-|>', mutation_scale=10, color=c, lw=1.4, zorder=6))
    if label:
        txt(ax, x + ldx, cy, label, c, lsize, ha='left')
    return ytop - length


def switch(ax, x, ytop, length=1.4, closed=True, c=INK, label=None, lsize=11, ldx=0.35):
    a = ytop - 0.4; b = ytop - length + 0.4
    wire(ax, [(x, ytop), (x, a)], c); wire(ax, [(x, b), (x, ytop - length)], c)
    dot(ax, x, a, c, 0.06); dot(ax, x, b, c, 0.06)
    if closed:
        wire(ax, [(x, b), (x + 0.06, a)], c, lw=2)
    else:
        wire(ax, [(x, b), (x + 0.35, a + 0.05)], c, lw=2)
    if label:
        txt(ax, x + ldx, (a + b) / 2, label, c, lsize, ha='left')
    return ytop - length


def arrow(ax, p0, p1, c=INK, lw=1.4, ms=11, style='-|>', z=7, **kw):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, color=c, lw=lw, zorder=z, **kw))


def darrow(ax, p0, p1, c=INK, lw=1.2, ms=9):
    arrow(ax, p0, p1, c, lw, ms, style='<|-|>')


def card(ax, x, y, lines, c=INK, size=10.5, dy=0.42, pad=0.25, w=None, edge='#d1d5db', fc='#f9fafb'):
    """Parameter card: a rounded box with one line per entry, top-left at (x, y)."""
    h = dy * len(lines) + pad * 1.4
    w = w or max(len(l) for l in lines) * 0.13 + 0.6
    ax.add_patch(FancyBboxPatch((x, y - h), w, h, boxstyle='round,pad=0.02,rounding_size=0.15',
                                fc=fc, ec=edge, lw=1.0, zorder=1))
    for i, l in enumerate(lines):
        txt(ax, x + pad, y - pad - dy * (i + 0.5), l, c, size, ha='left')
    return w, h


def inverter(ax, x, y, cn=N, cp=P, labels=True, vin=r'$V_{in}$', vout=r'$V_{out}$', vdd_label=r'$V_{DD}$',
             out_len=1.3, in_len=0.9, lsize=12, gds=False, currents=False, mdx=0.62):
    """Standard CMOS inverter. (x, y) = output node. Returns key points."""
    mp = mos(ax, x - 0.45, y + 1.3, 'p', cp, r'$M_2$' if labels else None, lsize, mdx)
    mn = mos(ax, x - 0.45, y - 1.3, 'n', cn, r'$M_1$' if labels else None, lsize, mdx)
    wire(ax, [mp['d'], (x, y), mn['d']], INK)
    vdd(ax, x, y + 2.2, vdd_label)
    wire(ax, [mp['s'], (x, y + 2.2)], cp)
    gnd(ax, x, y - 2.2)
    wire(ax, [mn['s'], (x, y - 2.2)], cn)
    gx = x - 1.2 - 0.0
    wire(ax, [mp['g'], (gx, y + 1.3), (gx, y - 1.3), mn['g']])
    dot(ax, gx, y)
    wire(ax, [(gx - in_len, y), (gx, y)])
    term(ax, gx - in_len, y)
    if vin:
        txt(ax, gx - in_len - 0.2, y, vin, INK, lsize, ha='right')
    dot(ax, x, y)
    wire(ax, [(x, y), (x + out_len, y)])
    term(ax, x + out_len, y)
    if vout:
        txt(ax, x + out_len + 0.2, y, vout, INK, lsize, ha='left')
    if gds:
        for m, c, k in [(mp, cp, 'p'), (mn, cn, 'n')]:
            txt(ax, m['g'][0] + 0.05, m['g'][1] + 0.28, 'G', c, 9, weight='bold')
            txt(ax, x - 0.24, y + (-0.6 if k == 'n' else 0.6), 'D', c, 9, weight='bold')
            txt(ax, x - 0.24, y + (-1.85 if k == 'n' else 1.85), 'S', c, 9, weight='bold')
    if currents:
        arrow(ax, (x + 0.35, y + 1.85), (x + 0.35, y + 0.7), cp, lw=1.6, ms=13)
        txt(ax, x + 0.5, y + 1.5, r'$i_{D,p}$', cp, 11, ha='left')
        arrow(ax, (x + 0.35, y - 0.7), (x + 0.35, y - 1.85), cn, lw=1.6, ms=13)
        txt(ax, x + 0.5, y - 1.1, r'$i_{D,n}$', cn, 11, ha='left')
    return {'in': (gx - in_len, y), 'out': (x + out_len, y), 'gx': gx, 'mp': mp, 'mn': mn}
