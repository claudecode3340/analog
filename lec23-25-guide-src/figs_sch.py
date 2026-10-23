"""Schematic figures."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sym import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figs')
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.family': 'Inter', 'mathtext.fontset': 'stixsans', 'svg.fonttype': 'path'})


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + '.svg'), bbox_inches='tight', pad_inches=0.04, transparent=True)
    fig.savefig(os.path.join(OUT, name + '.png'), bbox_inches='tight', pad_inches=0.04, dpi=110, facecolor='white')
    plt.close(fig)


def inverter_core(ax, x0=0, y0=0, labels=True, vin=True, nlab='$M_1$ NMOS', plab='$M_2$ PMOS', sep=0.8):
    """returns out point, gate join point."""
    P = mos(ax, x0, y0 + sep, 'p', ORANGE, plab if labels else None)
    N = mos(ax, x0, y0 - sep, 'n', BLUE, nlab if labels else None)
    vdd(ax, P['top'])
    gnd(ax, N['bot'])
    wire(ax, [P['bot'], N['top']])
    out = (P['x'], y0)
    dot(ax, out)
    gx = P['g'][0]
    wire(ax, [P['g'], (gx, y0), N['g']])
    dot(ax, (gx, y0))
    if vin:
        wire(ax, [(gx, y0), (gx - 0.5, y0)])
        term(ax, (gx - 0.5, y0), '$V_{in}$', 'left')
    return out, (gx, y0), P, N


def fig_inverter():
    fig, ax = plt.subplots(figsize=(6.8, 2.9))
    out, g, P, N = inverter_core(ax, 0, 0)
    wire(ax, [out, (out[0] + 0.9, 0)])
    term(ax, (out[0] + 0.9, 0), '$V_{out}$', 'right')
    # terminal voltages annotations
    text(ax, (-3.0, 1.3), 'PMOS:', ORANGE, 10, ha='left', weight='bold')
    text(ax, (-3.0, 1.05), '$V_{GS,p}=V_{in}-V_{DD}$', ORANGE, 10.5, ha='left')
    text(ax, (-3.0, 0.78), '$V_{DS,p}=V_{out}-V_{DD}$', ORANGE, 10.5, ha='left')
    text(ax, (-3.0, -0.75), 'NMOS:', BLUE, 10, ha='left', weight='bold')
    text(ax, (-3.0, -1.0), '$V_{GS,n}=V_{in}$', BLUE, 10.5, ha='left')
    text(ax, (-3.0, -1.27), '$V_{DS,n}=V_{out}$', BLUE, 10.5, ha='left')
    # switch model on right
    xs = 4.0
    vdd(ax, (xs, 1.55))
    switch(ax, (xs, 1.55), (xs, 0.25), closed=False, c=ORANGE)
    res(ax, (xs, 0.25), (xs, 0.0), ORANGE, n=4, amp=0.06)
    dot(ax, (xs, 0))
    res(ax, (xs, 0.0), (xs, -0.25), BLUE, n=4, amp=0.06)
    switch(ax, (xs, -0.25), (xs, -1.55), closed=True, c=BLUE)
    gnd(ax, (xs, -1.55))
    wire(ax, [(xs, 0), (xs + 0.7, 0)])
    term(ax, (xs + 0.7, 0), '$V_{out}$', 'right')
    text(ax, (xs + 0.45, 0.95), 'PMOS: switch + $R_{on,p}$\nON when $V_{in}$ low', ORANGE, 9, ha='left')
    text(ax, (xs + 0.45, -0.95), 'NMOS: switch + $R_{on,n}$\nON when $V_{in}$ high', BLUE, 9, ha='left')
    text(ax, (xs + 0.6, -2.15), 'the lecture\'s "non-ideal switches"', MUTED, 9, ha='center', style='italic')
    setup(ax, (-3.1, 6.6), (-2.3, 2.1))
    save(fig, 'sch_inverter')


def fig_load():
    fig, ax = plt.subplots(figsize=(4.0, 2.9))
    out, g, P, N = inverter_core(ax, 0, 0, nlab='', plab='')
    wire(ax, [out, (out[0] + 1.6, 0)])
    term(ax, (out[0] + 1.6, 0), '$V_{out}$', 'right')
    cx = out[0] + 1.0
    dot(ax, (cx, 0))
    wire(ax, [(cx, 0), (cx, -0.5)])
    cap(ax, (cx, -0.57), label='$C_{load}$')
    wire(ax, [(cx, -0.64), (cx, -1.1)])
    gnd(ax, (cx, -1.1))
    arrow(ax, (out[0] + 0.15, 0.75), (out[0] + 0.15, 0.25), ORANGE)
    text(ax, (out[0] + 0.25, 0.55), '$i_{D,p}$', ORANGE, 11, ha='left')
    arrow(ax, (out[0] + 0.15, -0.25), (out[0] + 0.15, -0.75), BLUE)
    text(ax, (out[0] + 0.25, -0.45), '$i_{D,n}$', BLUE, 11, ha='left')
    arrow(ax, (out[0] + 0.35, 0.12), (out[0] + 0.85, 0.12), AQUA)
    text(ax, (out[0] + 0.6, 0.3), '$i_C$', AQUA, 11)
    text(ax, (cx - 0.6, -2.05), '$i_C = i_{D,p}-i_{D,n} = C_{load}\\,\\dfrac{dV_{out}}{dt}$', INK, 11)
    setup(ax, (-1.6, 3.2), (-2.3, 1.75))
    save(fig, 'sch_load')


def fig_caps():
    """Lec 25: driving inverter + its parasitics + interconnect + next stage."""
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    out, g, P, N = inverter_core(ax, 0, 0, nlab='', plab='', sep=1.1)
    gx = g[0]
    cv = VIOLET
    for yy, lab in [(0.3, '$C_{gd,p}$'), (-0.3, '$C_{gd,n}$')]:
        dot(ax, (gx, yy), cv, 0.035); dot(ax, (out[0], yy), cv, 0.035)
        wire(ax, [(gx, yy), (-0.25, yy)], cv, ls='--')
        cap(ax, (-0.18, yy), 'h', cv, w=0.11, gap=0.04)
        wire(ax, [(-0.11, yy), (out[0], yy)], cv, ls='--')
        text(ax, (-0.18, yy + (0.27 if yy > 0 else -0.27)), lab, cv, 9.5)
    text(ax, (-1.7, -2.45), '$C_{gs,p}$, $C_{gs,n}$ hang on the input\nnode (or are shorted): not on $V_{out}$', MUTED, 8.5, ha='left')
    # drain-bulk caps on output
    dx = out[0] + 0.55
    wire(ax, [out, (out[0] + 3.0, 0)])
    dot(ax, (dx, 0))
    wire(ax, [(dx, 0), (dx, 0.45)], AQUA, ls='--')
    cap(ax, (dx, 0.52), 'v', AQUA, w=0.13, gap=0.04)
    wire(ax, [(dx, 0.56), (dx, 0.95)], AQUA, ls='--')
    wire(ax, [(dx - 0.12, 0.95), (dx + 0.12, 0.95)], AQUA, lw=2.2)
    text(ax, (dx, 1.13), '$V_{DD}$ (n-well)', AQUA, 8.5)
    text(ax, (dx + 0.17, 0.52), '$C_{db,p}$', AQUA, 10, ha='left')
    wire(ax, [(dx, 0), (dx, -0.45)], AQUA, ls='--')
    cap(ax, (dx, -0.52), 'v', AQUA, w=0.13, gap=0.04)
    wire(ax, [(dx, -0.56), (dx, -0.9)], AQUA, ls='--')
    gnd(ax, (dx, -0.9), AQUA)
    text(ax, (dx + 0.17, -0.52), '$C_{db,n}$', AQUA, 10, ha='left')
    # interconnect
    ix = out[0] + 1.5
    dot(ax, (ix, 0))
    wire(ax, [(ix, 0), (ix, -0.45)], YELLOW, ls='--')
    cap(ax, (ix, -0.52), 'v', YELLOW, w=0.13, gap=0.04)
    wire(ax, [(ix, -0.56), (ix, -0.9)], YELLOW, ls='--')
    gnd(ax, (ix, -0.9), YELLOW)
    text(ax, (ix + 0.17, -0.52), '$C_{int}$', '#9a6a00', 10, ha='left')
    text(ax, (ix, 0.3), 'wire', '#9a6a00', 8.5)
    # next stage
    nx = out[0] + 3.0 + 0.85
    out2, g2, P2, N2 = inverter_core(ax, nx, 0, labels=False, vin=False, sep=1.1)
    wire(ax, [(out[0] + 3.0, 0), g2])
    wire(ax, [out2, (out2[0] + 0.4, 0)])
    term(ax, (out2[0] + 0.4, 0), None)
    # Cg of next stage
    cgx = out[0] + 2.6
    dot(ax, (cgx, 0))
    wire(ax, [(cgx, 0), (cgx, -0.45)], RED, ls='--')
    cap(ax, (cgx, -0.52), 'v', RED, w=0.13, gap=0.04)
    wire(ax, [(cgx, -0.56), (cgx, -0.9)], RED, ls='--')
    gnd(ax, (cgx, -0.9), RED)
    text(ax, (cgx + 0.17, -0.52), '$C_g$', RED, 10, ha='left')
    text(ax, (nx + 1.0, -2.45), 'next stage:  $C_g = C_{ox}(WL)_n + C_{ox}(WL)_p$', RED, 9)
    text(ax, (out[0] + 0.08, -0.2), '$V_{out}$', INK, 10.5, ha='left')
    setup(ax, (-1.75, 6.6), (-2.75, 2.2))
    save(fig, 'sch_caps')


def fig_ring():
    fig, ax = plt.subplots(figsize=(6.0, 1.5))
    xs = [0, 2.0, 4.0]
    names = ['X', 'Y', 'Z']
    for i, x in enumerate(xs):
        tri = Polygon([(x, 0.45), (x, -0.45), (x + 0.8, 0)], closed=True, fc='white', ec=INK, lw=LW, zorder=3)
        ax.add_patch(tri)
        ax.add_patch(Circle((x + 0.87, 0), 0.07, fc='white', ec=INK, lw=LW, zorder=3))
        wire(ax, [(x + 0.94, 0), (x + 2.0 if i < 2 else x + 1.4, 0)])
        nx = x + 1.35
        dot(ax, (nx, 0))
        text(ax, (nx, 0.25), names[i], INK, 11)
    wire(ax, [(5.4, 0), (5.4, -0.8), (-0.5, -0.8), (-0.5, 0), (0, 0)])
    setup(ax, (-0.8, 6.0), (-1.0, 0.6))
    save(fig, 'sch_ring')


def fig_razavi211():
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.4))
    # (a) source follower charging C1 (drain at VDD, gate stepped 0->3)
    ax = axs[0]
    M = mos(ax, 0, 0.3, 'n', BLUE, '$M_1$')
    vdd(ax, M['top'])
    wire(ax, [M['bot'], (0.3, -0.5)])
    dot(ax, (0.3, -0.5))
    wire(ax, [(0.3, -0.5), (0.9, -0.5)])
    term(ax, (0.9, -0.5), '$V_X$', 'right')
    wire(ax, [(0.3, -0.5), (0.3, -0.75)])
    cap(ax, (0.3, -0.82), label='$C_1$ (1 V)')
    wire(ax, [(0.3, -0.89), (0.3, -1.15)])
    gnd(ax, (0.3, -1.15))
    wire(ax, [M['g'], (-0.9, 0.3)])
    term(ax, (-0.9, 0.3), '$V_{in}$: 0→3 V', 'left', fs=10)
    text(ax, (0, -1.75), '(a)', MUTED, 10)
    setup(ax, (-2.6, 1.6), (-1.9, 1.4))
    # (b) NMOS discharging C1 (drain = VX)
    ax = axs[1]
    M = mos(ax, 0, 0.0, 'n', BLUE, '$M_1$')
    gnd(ax, M['bot'])
    wire(ax, [M['top'], (0.3, 0.75), (1.1, 0.75)])
    dot(ax, (1.1, 0.75))
    wire(ax, [(1.1, 0.75), (1.6, 0.75)])
    term(ax, (1.6, 0.75), '$V_X$', 'right')
    wire(ax, [(1.1, 0.75), (1.1, 0.07)])
    cap(ax, (1.1, 0.0), label='$C_1$ (1 V)')
    wire(ax, [(1.1, -0.07), (1.1, -0.55)])
    gnd(ax, (1.1, -0.55))
    wire(ax, [M['g'], (-0.9, 0)])
    term(ax, (-0.9, 0), '$V_{in}$: 0→3 V', 'left', fs=10)
    text(ax, (0.3, -1.75), '(b)', MUTED, 10)
    setup(ax, (-2.6, 2.3), (-1.9, 1.4))
    save(fig, 'sch_razavi211')


def fig_amp():
    """inverter biased at trip point as an amplifier: small-signal parallel model."""
    fig, ax = plt.subplots(figsize=(6.0, 2.3))
    out, g, P, N = inverter_core(ax, 0, 0, nlab='$M_1$', plab='$M_2$')
    wire(ax, [out, (out[0] + 0.7, 0)])
    term(ax, (out[0] + 0.7, 0), '$v_{out}$', 'right')
    # small signal model
    x = 4.0
    ax.add_patch(Circle((x, 0), 0.28, fc='white', ec=INK, lw=LW, zorder=3))
    arrow(ax, (x, -0.17), (x, 0.17), INK, ms=10)
    wire(ax, [(x, 0.28), (x, 0.9), (x + 1.2, 0.9), (x + 1.2, 0.6)])
    res(ax, (x + 1.2, 0.6), (x + 1.2, -0.6))
    wire(ax, [(x + 1.2, -0.6), (x + 1.2, -0.9), (x, -0.9), (x, -0.28)])
    gnd(ax, (x + 0.6, -0.9))
    dot(ax, (x + 0.6, -0.9))
    wire(ax, [(x + 1.2, 0.9), (x + 1.8, 0.9)])
    term(ax, (x + 1.8, 0.9), '$v_{out}$', 'right')
    text(ax, (x - 0.38, 0.5), '$(g_{m1}+g_{m2})\\,v_{in}$', INK, 10, ha='right')
    text(ax, (x + 1.35, 0), '$r_{O1}\\parallel r_{O2}$', INK, 10, ha='left')
    setup(ax, (-1.4, 7.4), (-1.7, 1.7))
    save(fig, 'sch_amp')


if __name__ == '__main__':
    fig_inverter(); fig_load(); fig_caps(); fig_ring(); fig_razavi211(); fig_amp()
