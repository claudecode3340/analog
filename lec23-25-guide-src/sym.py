"""Tiny schematic-symbol library on matplotlib axes (data units ~ 1 = one device height)."""
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle

INK = '#1d1d1b'
MUTED = '#6b6a66'
BLUE, ORANGE, AQUA, VIOLET, RED, YELLOW, GREEN, MAGENTA = (
    '#2a78d6', '#eb6834', '#1baf7a', '#6250d6', '#e34948', '#eda100', '#008300', '#e87ba4')
LW = 1.5


def wire(ax, pts, c=INK, lw=LW, ls='-', z=2):
    pts = np.array(pts, float)
    ax.plot(pts[:, 0], pts[:, 1], color=c, lw=lw, ls=ls, solid_capstyle='round', zorder=z)


def dot(ax, p, c=INK, r=0.045):
    ax.add_patch(Circle(p, r, color=c, zorder=5))


def term(ax, p, label=None, side='left', c=INK, fs=11):
    ax.add_patch(Circle(p, 0.05, fc='white', ec=c, lw=LW, zorder=6))
    if label:
        dx = {'left': -0.12, 'right': 0.12, 'top': 0, 'bottom': 0}[side]
        dy = {'left': 0, 'right': 0, 'top': 0.15, 'bottom': -0.17}[side]
        ha = {'left': 'right', 'right': 'left', 'top': 'center', 'bottom': 'center'}[side]
        ax.text(p[0] + dx, p[1] + dy, label, ha=ha, va='center', fontsize=fs, color=c)


def text(ax, p, s, c=INK, fs=10.5, ha='center', va='center', **kw):
    ax.text(p[0], p[1], s, color=c, fontsize=fs, ha=ha, va=va, **kw)


def gnd(ax, p, c=INK):
    x, y = p
    wire(ax, [(x, y), (x, y - 0.15)], c)
    for i, w in enumerate([0.2, 0.13, 0.06]):
        wire(ax, [(x - w, y - 0.15 - i * 0.06), (x + w, y - 0.15 - i * 0.06)], c)


def vdd(ax, p, label='$V_{DD}$', c=INK):
    x, y = p
    wire(ax, [(x, y), (x, y + 0.15)], c)
    wire(ax, [(x - 0.18, y + 0.15), (x + 0.18, y + 0.15)], c, lw=LW + 0.6)
    ax.text(x, y + 0.22, label, ha='center', va='bottom', fontsize=11, color=c)


def mos(ax, x, y, kind='n', c=INK, label=None, lab_side='right', bulk=True, lead=0.35):
    """MOSFET with vertical channel at x, centred at y, gate on the left.
    NMOS: drain on top, source at bottom. PMOS: source on top, drain at bottom.
    Returns dict of terminal points: g, top, bot (end of leads)."""
    h = 0.32
    # channel (three segments look = enhancement); draw solid for clarity
    wire(ax, [(x, y - h), (x, y + h)], c, lw=LW + 1.0)
    # gate plate
    gx = x - 0.13
    wire(ax, [(gx, y - h * 0.85), (gx, y + h * 0.85)], c, lw=LW + 0.4)
    if kind == 'p':
        ax.add_patch(Circle((gx - 0.07, y), 0.065, fc='white', ec=c, lw=LW, zorder=4))
        gstart = gx - 0.135
    else:
        gstart = gx
    g = (gx - 0.55, y)
    wire(ax, [(gstart, y), g], c)
    # stubs
    wire(ax, [(x, y + h * 0.8), (x + 0.3, y + h * 0.8), (x + 0.3, y + h * 0.8 + lead)], c)
    wire(ax, [(x, y - h * 0.8), (x + 0.3, y - h * 0.8), (x + 0.3, y - h * 0.8 - lead)], c)
    top = (x + 0.3, y + h * 0.8 + lead)
    bot = (x + 0.3, y - h * 0.8 - lead)
    # source arrow
    if kind == 'n':
        sy = y - h * 0.8
        ax.add_patch(FancyArrowPatch((x + 0.05, sy), (x + 0.27, sy), arrowstyle='-|>', mutation_scale=11, color=c, lw=0, zorder=5))
    else:
        sy = y + h * 0.8
        ax.add_patch(FancyArrowPatch((x + 0.27, sy), (x + 0.04, sy), arrowstyle='-|>', mutation_scale=11, color=c, lw=0, zorder=5))
    if label:
        if lab_side == 'right':
            ax.text(x + 0.42, y, label, fontsize=10.5, color=c, ha='left', va='center')
        else:
            ax.text(x - 0.55, y + 0.3, label, fontsize=10.5, color=c, ha='right', va='center')
    return dict(g=g, top=top, bot=bot, x=x + 0.3)


def cap(ax, p, orient='v', c=INK, label=None, lab_side='right', w=0.22, gap=0.07, ls='-', fs=10.5, lead=0.0):
    x, y = p
    if orient == 'v':
        wire(ax, [(x - w, y + gap), (x + w, y + gap)], c, lw=LW + 0.6, ls=ls)
        wire(ax, [(x - w, y - gap), (x + w, y - gap)], c, lw=LW + 0.6, ls=ls)
        if lead:
            wire(ax, [(x, y + gap), (x, y + gap + lead)], c, ls=ls)
            wire(ax, [(x, y - gap), (x, y - gap - lead)], c, ls=ls)
        if label:
            dx = w + 0.08 if lab_side == 'right' else -(w + 0.08)
            ax.text(x + dx, y, label, fontsize=fs, color=c, ha='left' if lab_side == 'right' else 'right', va='center')
    else:
        wire(ax, [(x - gap, y - w), (x - gap, y + w)], c, lw=LW + 0.6, ls=ls)
        wire(ax, [(x + gap, y - w), (x + gap, y + w)], c, lw=LW + 0.6, ls=ls)
        if lead:
            wire(ax, [(x - gap, y), (x - gap - lead, y)], c, ls=ls)
            wire(ax, [(x + gap, y), (x + gap + lead, y)], c, ls=ls)
        if label:
            dy = w + 0.12 if lab_side == 'top' else -(w + 0.14)
            ax.text(x, y + dy, label, fontsize=fs, color=c, ha='center', va='center')


def res(ax, p0, p1, c=INK, n=6, amp=0.09):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0
    L = np.hypot(*d)
    u = d / L
    nrm = np.array([-u[1], u[0]])
    a, b = 0.2 * L, 0.8 * L
    pts = [p0, p0 + u * a]
    for i in range(n):
        t = a + (b - a) * (i + 0.5) / n
        pts.append(p0 + u * t + nrm * amp * (1 if i % 2 == 0 else -1))
    pts += [p0 + u * b, p1]
    wire(ax, pts, c)


def switch(ax, p_top, p_bot, closed=False, c=INK):
    x, yt = p_top
    _, yb = p_bot
    a = yt - 0.25 * (yt - yb)
    bpt = yb + 0.25 * (yt - yb)
    wire(ax, [(x, yt), (x, a)], c)
    wire(ax, [(x, yb), (x, bpt)], c)
    dot(ax, (x, a), c, 0.04)
    dot(ax, (x, bpt), c, 0.04)
    if closed:
        wire(ax, [(x, bpt), (x + 0.05, a)], c)
    else:
        wire(ax, [(x, bpt), (x + 0.3, a - 0.05)], c)


def arrow(ax, p0, p1, c=INK, lw=1.4, ms=12, style='-|>', ls='-'):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, color=c, lw=lw, ls=ls, zorder=6,
                                 shrinkA=0, shrinkB=0))


def setup(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.axis('off')
