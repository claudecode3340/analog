import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from draw import *
from model import idn, vout_of
import numpy as np
from matplotlib.patches import Polygon

OUT = 'figs'
os.makedirs(OUT, exist_ok=True)


def vtc(VDD, vtn, vtp, kn, kp, n=1200, lam=1e-4):
    vin = np.linspace(0, VDD, n)
    return vin, np.array([vout_of(v, VDD, vtn, vtp, kn, kp, lam) for v in vin])


def plotfig(w, h, **kw):
    fig, ax = plt.subplots(figsize=(w, h), **kw)
    return fig, ax


# ------------------------------------------------------------------ PART 0
def f_symbols():
    fig, ax = canvas(-1.0, 17.0, -2.1, 2.0)
    for x, kind, c, name, l1, l2 in [(0.9, 'n', N, 'NMOS', r'HIGH:  $V_{GS} > V_{T0,n}$  $(>0)$', 'current flows D → S'),
                                      (9.9, 'p', P, 'PMOS', r'LOW:  $V_{GS} < V_{T0,p}$  $(<0)$', 'current flows S → D')]:
        m = mos(ax, x, 0, kind, c)
        txt(ax, m['g'][0] - 0.15, 0, 'G', c, 12, ha='right', weight='bold')
        top, bot = ('D', 'S') if kind == 'n' else ('S', 'D')
        txt(ax, m['d'][0] if kind == 'n' else m['s'][0], 1.15, top, c, 12, weight='bold')
        txt(ax, m['s'][0] if kind == 'n' else m['d'][0], -1.2, bot, c, 12, weight='bold')
        arrow(ax, (x + 0.85, 0.75), (x + 0.85, -0.75), c, ms=12)
        txt(ax, x + 1.0, 0, r'$I_D$' if kind == 'n' else r'$|I_D|$', c, 13, ha='left')
        txt(ax, x + 0.2, -1.85, name, c, 12, weight='bold')
        txt(ax, x + 2.4, 0.6, 'ON when the gate is', INK, 10.5, ha='left')
        txt(ax, x + 2.4, 0.0, l1, c, 11, ha='left')
        txt(ax, x + 2.4, -0.6, l2, MUT, 10, ha='left')
    save(fig, 'f_symbols')


def f_ivcurves():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 3.1), gridspec_kw={'wspace': 0.42, 'width_ratios': [1.25, 1]})
    vds = np.linspace(0, 5, 400)
    shades = ['#93c5fd', '#60a5fa', '#3b82f6', '#1d4ed8']
    for vgs, c in zip([2, 3, 4, 5], shades):
        ov = vgs - 1
        i = np.where(vds < ov, 2 * ov * vds - vds ** 2, ov ** 2) / 2
        a1.plot(vds, i, color=c, lw=2)
        a1.text(5.08, ov ** 2 / 2, f'{vgs} V', color=c, fontsize=9.5, va='center')
    x = np.linspace(0, 4, 100)
    a1.plot(x, x ** 2 / 2, color=R, ls='--', lw=1.4)
    a1.text(0.2, 7.6, 'LINEAR\n(resistor-like)', fontsize=9, color=INK, weight='semibold')
    a1.text(3.0, 1.0, 'SATURATION\n(current-source-like)', fontsize=9, color=INK, weight='semibold')
    a1.text(4.95, 5.4, 'edge of sat.:\n' + r'$V_{DS}=V_{GS}-V_{T0}$', color=R, fontsize=9, ha='right')
    a1.text(5.08, 9.0, r'$V_{GS}$', fontsize=9.5, color=N)
    a1.set_xlabel(r'$V_{DS}$ (V)'); a1.set_ylabel(r'$I_D$  (units of $k_n$ V$^2$)')
    a1.set_xlim(0, 5); a1.set_ylim(0, 8.6); a1.set_title('NMOS output curves', loc='left')
    v = np.linspace(-5, 5, 400)
    a2.plot(v, np.where(v > 1, (v - 1) ** 2 / 2, 0), color=N, lw=2.2)
    a2.plot(v, np.where(v < -1, (v + 1) ** 2 / 2, 0), color=P, lw=2.2)
    a2.axvline(0, color='#d1d5db', lw=0.8)
    a2.text(4.6, 7.4, 'NMOS ON\n' + r'$V_{GS}>V_{T0,n}$', color=N, fontsize=9.5, ha='right')
    a2.text(-4.0, 7.4, 'PMOS ON\n' + r'$V_{GS}<V_{T0,p}$', color=P, fontsize=9.5)
    a2.set_xlabel(r'$V_{GS}$ (V)'); a2.set_ylabel(r'$|I_D|$ (saturation)'); a2.set_xticks([-4, -2, 0, 2, 4])
    a2.set_ylim(0, 8.6); a2.set_title('Turn-on: mirror images', loc='left')
    save(fig, 'f_ivcurves')


def f_vtc_crit():
    VDD = 5
    vin = np.linspace(0, VDD, 2000); w = 0.38
    vo = VDD / (1 + np.exp((vin - 2.5) / w))
    g = np.gradient(vo, vin); idx = np.where(g <= -1)[0]
    vil, vih, vth = vin[idx[0]], vin[idx[-1]], 2.5
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 3.5), gridspec_kw={'width_ratios': [1.6, 1], 'wspace': 0.22})
    a1.plot(vin, vo, color=INK, lw=2.4)
    a1.plot([0, VDD], [0, VDD], color='#c7cbd1', ls='--', lw=1)
    for x0, c in [(vil, R), (vih, R)]:
        y0 = np.interp(x0, vin, vo)
        a1.plot([x0 - 0.6, x0 + 0.6], [y0 + 0.6, y0 - 0.6], color=c, lw=1.4)
        a1.plot(x0, y0, 'o', color=c, ms=6, zorder=5)
        a1.plot([x0, x0], [0, y0], color=c, ls=':', lw=1)
    a1.plot(vth, vth, 'o', color=PU, ms=6, zorder=5)
    a1.plot([vth, vth], [0, vth], color=PU, ls=':', lw=1)
    a1.text(vil + 0.3, 4.75, 'slope = −1', color=R, fontsize=9.5)
    a1.text(vih + 0.3, 0.9, 'slope = −1', color=R, fontsize=9.5)
    a1.text(vth + 0.15, vth + 0.15, r'$V_{in}=V_{out}$', color=PU, fontsize=9.5)
    a1.text(0.15, 3.3, 'output = logic 1', color=MUT, fontsize=9.5)
    a1.text(3.45, 1.75, 'output = logic 0', color=MUT, fontsize=9.5)
    a1.set_xticks([0, vil, vth, vih, VDD]); a1.set_xticklabels(['0', r'$V_{IL}$', r'$V_{th}$', r'$V_{IH}$', r'$V_{DD}$'])
    a1.set_yticks([0, VDD]); a1.set_yticklabels([r'$V_{OL}$', r'$V_{OH}$'])
    a1.set_xlabel(r'$V_{in}$'); a1.set_ylabel(r'$V_{out}$')
    a1.set_xlim(0, VDD); a1.set_ylim(-0.1, 5.3); a1.grid(False)
    a1.set_title('The VTC and its five numbers', loc='left')
    # noise margins
    a2.axis('off'); a2.set_xlim(0, 10); a2.set_ylim(-0.6, 11.4)
    VOH, VOL, VIH, VIL = 9.4, 0.6, 6.3, 4.0
    a2.add_patch(Rectangle((0.8, VOL), 1.6, VOH - VOL, fc='white', ec=INK, lw=1.2))
    a2.text(1.6, 10.3, 'driver\noutput', ha='center', va='center', fontsize=9.5)
    a2.add_patch(Rectangle((6.6, VIH), 1.6, VOH - VIH, fc='#bfdbfe', ec='none'))
    a2.add_patch(Rectangle((6.6, VIL), 1.6, VIH - VIL, fc='#e5e7eb', ec='none'))
    a2.add_patch(Rectangle((6.6, VOL), 1.6, VIL - VOL, fc='#fed7aa', ec='none'))
    a2.text(7.4, 10.3, 'receiver\ninput', ha='center', va='center', fontsize=9.5)
    a2.text(7.4, (VIH + VOH) / 2, 'reads 1', ha='center', va='center', fontsize=9, color='#1e3a8a', rotation=90)
    a2.text(7.4, (VIL + VIH) / 2, '?', ha='center', va='center', fontsize=11, color=MUT)
    a2.text(7.4, (VOL + VIL) / 2, 'reads 0', ha='center', va='center', fontsize=9, color='#7c2d12', rotation=90)
    for yv in [VOH, VOL, VIH, VIL]:
        a2.plot([2.4, 6.6], [yv, yv], color='#d1d5db', ls='--', lw=0.9)
    a2.text(0.6, VOH, r'$V_{OH}$', ha='right', va='center', fontsize=11)
    a2.text(0.6, VOL, r'$V_{OL}$', ha='right', va='center', fontsize=11)
    a2.text(8.4, VIH, r'$V_{IH}$', ha='left', va='center', fontsize=11)
    a2.text(8.4, VIL, r'$V_{IL}$', ha='left', va='center', fontsize=11)
    a2.annotate('', (4.5, VIH), (4.5, VOH), arrowprops=dict(arrowstyle='<|-|>', color=N, lw=1.3))
    a2.text(4.7, (VIH + VOH) / 2, r'$NM_H$', color=N, fontsize=11.5, va='center')
    a2.annotate('', (4.5, VOL), (4.5, VIL), arrowprops=dict(arrowstyle='<|-|>', color=P, lw=1.3))
    a2.text(4.7, (VOL + VIL) / 2, r'$NM_L$', color=P, fontsize=11.5, va='center')
    a2.set_title('Noise margins', loc='left', pad=4)
    save(fig, 'f_vtc_crit')


# ------------------------------------------------------------------ PART 1
def f_inverter():
    fig, ax = canvas(-6.6, 13.2, -3.2, 3.4)
    inverter(ax, 1.0, 0, gds=True, currents=True, out_len=2.0, mdx=1.75)
    card(ax, -6.5, 3.1, [r'PMOS:  $V_{GS,p}=V_{in}-V_{DD}$', r'           $V_{DS,p}=V_{out}-V_{DD}$'],
         P, 10.5, w=4.0, fc='#fff7ed', edge='#fed7aa')
    card(ax, -6.5, -1.5, [r'NMOS:  $V_{GS,n}=V_{in}$', r'           $V_{DS,n}=V_{out}$'],
         N, 10.5, w=4.0, fc='#eff6ff', edge='#bfdbfe')
    # switch model
    x = 9.4
    vdd(ax, x, 2.9)
    wire(ax, [(x, 2.9), (x, 2.5)], P)
    switch(ax, x, 2.5, 1.2, closed=False, c=P)
    res(ax, x, 1.3, 1.3, P)
    dot(ax, x, 0)
    wire(ax, [(x, 0), (x + 1.2, 0)]); term(ax, x + 1.2, 0); txt(ax, x + 1.45, 0, r'$V_{out}$', INK, 12, ha='left')
    res(ax, x, 0, 1.3, N)
    switch(ax, x, -1.3, 1.2, closed=True, c=N)
    wire(ax, [(x, -2.5), (x, -2.6)], N); gnd(ax, x, -2.6)
    txt(ax, x - 0.5, 1.9, 'PMOS switch\nON when $V_{in}$ LOW', P, 9.5, ha='right')
    txt(ax, x - 0.5, -1.9, 'NMOS switch\nON when $V_{in}$ HIGH', N, 9.5, ha='right')
    txt(ax, x - 0.5, 0.65, r'$R_{on,p}$', P, 10, ha='right')
    txt(ax, x - 0.5, -0.65, r'$R_{on,n}$', N, 10, ha='right')
    txt(ax, 5.0, 0.35, '≈', MUT, 22)
    save(fig, 'f_inverter')


def f_story():
    """Five panels A-E: off = open switch, linear = resistor, saturated = current source."""
    VDD = 5
    vin, vo = vtc(VDD, 1, -1, 1, 1)
    pts = [('A', 0.5), ('B', 1.9), ('C', 2.5), ('D', 3.1), ('E', 4.5)]
    states = {'A': ('lin', 'off'), 'B': ('lin', 'sat'), 'C': ('sat', 'sat'), 'D': ('sat', 'lin'), 'E': ('off', 'lin')}
    fig, ax = canvas(-0.6, 20.0, -4.7, 3.6)
    for i, (k, v) in enumerate(pts):
        x = 0.9 + i * 4.0
        ax.add_patch(FancyBboxPatch((x - 0.95, -4.55), 3.5, 8.0, boxstyle='round,pad=0,rounding_size=0.25',
                                    fc='#f9fafb', ec='#e5e7eb', lw=1))
        txt(ax, x + 0.8, 3.0, k, INK, 15, weight='bold')
        xc = x + 0.4
        vdd(ax, xc, 2.25, None)
        sp, sn = states[k]
        def el(state, ytop, c):
            if state == 'off':
                return switch(ax, xc, ytop, 1.8, closed=False, c=c)
            if state == 'lin':
                return res(ax, xc, ytop, 1.8, c)
            return isrc(ax, xc, ytop, 1.8, c)
        el(sp, 2.25, P)
        dot(ax, xc, 0.45)
        wire(ax, [(xc, 0.45), (xc + 0.9, 0.45)])
        term(ax, xc + 0.9, 0.45)
        el(sn, 0.45, N)
        gnd(ax, xc, -1.35)
        vout = np.interp(v, vin, vo)
        names = {'off': 'off', 'lin': 'linear', 'sat': 'sat.'}
        txt(ax, xc - 0.55, 1.35, names[sp], P, 9, ha='right')
        txt(ax, xc - 0.55, -0.45, names[sn], N, 9, ha='right')
        txt(ax, x + 0.8, -2.45, rf'$V_{{in}}\approx{v:g}$ V', INK, 10)
        out = {'A': r'$V_{out}=V_{DD}$', 'B': r'$V_{out}$ near $V_{DD}$', 'C': 'falls steeply',
               'D': r'$V_{out}$ near 0', 'E': r'$V_{out}=0$'}[k]
        txt(ax, x + 0.8, -3.1, out, MUT, 9.5)
        cur = {'A': 'no current', 'B': 'small current', 'C': 'peak current', 'D': 'small current', 'E': 'no current'}[k]
        txt(ax, x + 0.8, -3.7, cur, MUT, 9.5)
    txt(ax, 9.4, -4.25 + 0.0, '', INK)
    save(fig, 'f_story')


def f_map():
    VDD, vtn, vtp = 5, 1, -1
    vin, vo = vtc(VDD, vtn, vtp, 1, 1, 1500)
    fig, ax = plotfig(6.6, 4.6)
    x = np.linspace(0, VDD, 300)
    ax.fill_between(x, np.maximum(x - vtn, 0), VDD, where=x >= vtn, color=N, alpha=0.08, lw=0)
    ax.fill_between(x, 0, np.minimum(x - vtp, VDD), where=x <= VDD + vtp, color=P, alpha=0.08, lw=0)
    ax.plot(x, x - vtn, color=N, lw=1.8)
    ax.plot(x, x - vtp, color=P, lw=1.8)
    ax.axvline(vtn, color=N, ls=':', lw=1); ax.axvline(VDD + vtp, color=P, ls=':', lw=1)
    ax.plot(vin, vo, color=INK, lw=2.8, zorder=5)
    for k, v in [('A', 0.5), ('B', 1.9), ('C', 2.5), ('D', 3.1), ('E', 4.5)]:
        y = np.interp(v, vin, vo) if k != 'C' else 2.5
        ax.plot(v, y, 'o', color='white', mec=INK, mew=1.8, ms=8, zorder=6)
        ax.text(v + 0.12, y + 0.18, k, fontsize=12, weight='bold', zorder=7)
    ax.text(0.12, 3.15, 'PMOS saturated\nBELOW the orange line\n' + r'$V_{out}=V_{in}-V_{T0,p}$', color=P, fontsize=9.5, bbox=dict(fc='white', ec='none', alpha=0.9, pad=2), zorder=8)
    ax.text(4.95, 0.75, 'NMOS saturated\nABOVE the blue line\n' + r'$V_{out}=V_{in}-V_{T0,n}$', color=N, fontsize=9.5, ha='right', bbox=dict(fc='white', ec='none', alpha=0.9, pad=2), zorder=8)
    ax.text(1.55, 1.85, 'both\nsat.', color=PU, fontsize=9.5, ha='left', weight='semibold')
    ax.set_xticks([0, vtn, 2.5, VDD + vtp, VDD]); ax.set_xticklabels(['0', r'$V_{T0,n}$', r'$V_{th}$', r'$V_{DD}+V_{T0,p}$', r'$V_{DD}$'])
    ax.set_yticks([0, -vtp, VDD - vtn, VDD]); ax.set_yticklabels(['0', r'$|V_{T0,p}|$', r'$V_{DD}-V_{T0,n}$', r'$V_{DD}$'])
    ax.set_xlim(0, VDD); ax.set_ylim(0, VDD + 0.05); ax.grid(False)
    ax.set_xlabel(r'$V_{in}$'); ax.set_ylabel(r'$V_{out}$')
    save(fig, 'f_map')


def f_regions():
    VDD = 5
    vin, vo = vtc(VDD, 1, -1, 1, 1, 1500)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.8, 5.4), sharex=True, gridspec_kw={'hspace': 0.12, 'height_ratios': [1.25, 1]})
    cols = []
    for v in vin:
        cols.append(MUT if v < 1 or v > 4 else (N if v < 2.499 else (P if v > 2.501 else PU)))
    for seg, c in [((0, 1), MUT), ((1, 2.5), N), ((2.5, 4), P), ((4, 5), MUT)]:
        m = (vin >= seg[0]) & (vin <= seg[1])
        a1.plot(vin[m], vo[m], color=c, lw=2.8)
    a1.plot([2.5, 2.5], [1.5, 3.5], color=PU, lw=2.8)
    for b in [1, 2.5, 4]:
        a1.axvline(b, color='#e5e7eb', lw=1); a2.axvline(b, color='#e5e7eb', lw=1)
    lab = [(0.5, 'A', 'n: OFF\np: linear', MUT), (1.75, 'B', 'n: sat.\np: linear', N),
           (3.25, 'D', 'n: linear\np: sat.', P), (4.5, 'E', 'n: linear\np: OFF', MUT)]
    for x, k, s, c in lab + [(2.5, 'C', '', PU)]:
        a1.text(x, 5.55, k, ha='center', fontsize=13, weight='bold', color=c)
    a1.text(0.5, 2.2, 'n: OFF\np: linear', ha='center', fontsize=9.5, color=MUT)
    a1.text(1.75, 1.2, 'n: sat.\np: linear', ha='center', fontsize=9.5, color=N)
    a1.text(3.25, 1.6, 'n: linear\np: sat.', ha='center', fontsize=9.5, color=P)
    a1.text(4.5, 2.2, 'n: linear\np: OFF', ha='center', fontsize=9.5, color=MUT)
    a1.annotate('C: both saturated\n(vertical drop, λ = 0)', (2.5, 2.9), (2.75, 4.05), fontsize=9.5, color=PU,
                arrowprops=dict(arrowstyle='-', color=PU, lw=1))
    a1.set_ylim(-0.2, 6.1); a1.set_ylabel(r'$V_{out}$ (V)'); a1.set_yticks([0, 1, 2, 3, 4, 5])
    i = np.array([idn(v, o, 1, 1) for v, o in zip(vin, vo)]) * 100
    for seg, c in [((0, 1), MUT), ((1, 2.5), N), ((2.5, 4), P), ((4, 5), MUT)]:
        m = (vin >= seg[0]) & (vin <= seg[1])
        a2.plot(vin[m], i[m], color=c, lw=2.6)
    a2.annotate(f'peak at $V_{{th}}$', (2.5, i.max()), (3.2, i.max() * 0.95), fontsize=9.5,
                arrowprops=dict(arrowstyle='-', color=INK, lw=0.8))
    a2.text(0.5, 25, 'zero static\ncurrent', ha='center', fontsize=9.5, color=MUT)
    a2.text(4.5, 25, 'zero static\ncurrent', ha='center', fontsize=9.5, color=MUT)
    a2.set_ylabel(r'$I_{D,n}=|I_{D,p}|$ (µA)'); a2.set_xlabel(r'$V_{in}$ (V)')
    a2.set_ylim(-5, 130); a2.set_xlim(0, 5)
    a2.text(0.02, 0.97, r'$V_{DD}=5$ V, $V_T=\pm1$ V, $k_n=k_p=100$ µA/V²', transform=a2.transAxes, fontsize=8.5, color=MUT, va='top')
    save(fig, 'f_regions')


def f_slope():
    VDD = 5
    vin, vo = vtc(VDD, 1, -1, 200, 100, 2000)
    fig, ax = plotfig(5.6, 3.6)
    ax.plot(vin, vo, color=INK, lw=2.4)
    for x0, lab, dx in [(1.795, r'$V_{IL}=1.795$ V', -1.55), (2.536, r'$V_{IH}=2.536$ V', 0.2)]:
        y0 = np.interp(x0, vin, vo)
        xs = np.array([x0 - 0.7, x0 + 0.7])
        ax.plot(xs, y0 - (xs - x0), color=R, lw=1.5)
        ax.plot(x0, y0, 'o', color=R, ms=7, zorder=5)
        ax.plot([x0, x0], [0, y0], color=R, ls=':', lw=1)
        ax.text(*((0.2, 3.9) if dx < 0 else (2.75, 0.9)), lab, color=R, fontsize=10.5)
    ax.text(3.0, 4.0, 'tangent lines of slope −1', color=R, fontsize=9.5)
    ax.set_xlim(0, 5); ax.set_ylim(-0.1, 5.3)
    ax.set_xlabel(r'$V_{in}$ (V)'); ax.set_ylabel(r'$V_{out}$ (V)')
    ax.text(3.0, 3.4, r'$k_R=2$, $V_{DD}=5$ V, $V_T=\pm1$ V', fontsize=9.5, color=MUT)
    save(fig, 'f_slope')


# ------------------------------------------------------------------ PART 2
def f_kr():
    VDD = 5
    fig, ax = plotfig(5.0, 3.6)
    cs = ['#c2410c', '#fb923c', INK, '#60a5fa', '#1d4ed8']
    for kR, c in zip([0.25, 0.5, 1, 2, 4], cs):
        vin, vo = vtc(VDD, 1, -1, kR, 1, 800)
        vth = (1 + (1 / np.sqrt(kR)) * 4) / (1 + 1 / np.sqrt(kR))
        ax.plot(vin, vo, color=c, lw=2.1, label=rf'$k_R={kR:g}$  →  $V_{{th}}={vth:.2f}$ V')
        ax.plot(vth, vth, 'o', color=c, ms=6, zorder=5, mec='white', mew=1)
    ax.plot([0, 5], [0, 5], color='#c7cbd1', ls='--', lw=1)
    ax.annotate('', (1.75, 0.8), (3.0, 0.8), arrowprops=dict(arrowstyle='-|>', color=N, lw=1.5))
    ax.text(0.15, 0.75, 'stronger NMOS\n→ $V_{th}$ moves LEFT', color=N, fontsize=9.5, va='center')
    ax.legend(loc='center left', fontsize=9.5, bbox_to_anchor=(1.01, 0.55))
    ax.set_xlim(0, 5); ax.set_ylim(-0.1, 5.3)
    ax.set_xlabel(r'$V_{in}$ (V)'); ax.set_ylabel(r'$V_{out}$ (V)')
    save(fig, 'f_kr')


def f_sym():
    VDD, VT = 2.5, 0.6
    vin, vo = vtc(VDD, VT, -VT, 1, 1, 1500)
    vil, vih = 1.0875, 1.4125
    fig, ax = plotfig(5.6, 3.7)
    ax.plot(vin, vo, color=INK, lw=2.4)
    ax.plot([0, VDD], [0, VDD], color='#c7cbd1', ls='--', lw=1)
    for x0, c in [(vil, R), (vih, R)]:
        y0 = np.interp(x0, vin, vo)
        ax.plot(x0, y0, 'o', color=c, ms=6, zorder=5); ax.plot([x0, x0], [0, y0], color=c, ls=':', lw=1)
    ax.plot(1.25, 1.25, 'o', color=PU, ms=6, zorder=5)
    ax.annotate('', (0, 0.25), (vil, 0.25), arrowprops=dict(arrowstyle='<|-|>', color=P, lw=1.2))
    ax.text(vil / 2, 0.35, r'$NM_L=1.0875$ V', color=P, ha='center', fontsize=9.5)
    ax.annotate('', (vih, 2.25), (VDD, 2.25), arrowprops=dict(arrowstyle='<|-|>', color=N, lw=1.2))
    ax.text((vih + VDD) / 2, 2.35, r'$NM_H=1.0875$ V', color=N, ha='center', fontsize=9.5)
    ax.text(vil - 0.05, 1.9, r'$V_{IL}$', color=R, ha='right', fontsize=10.5)
    ax.text(vih + 0.05, 0.55, r'$V_{IH}$', color=R, fontsize=10.5)
    ax.text(1.32, 1.2, r'$V_{th}=V_{DD}/2$', color=PU, fontsize=10)
    ax.set_xlim(0, VDD); ax.set_ylim(-0.05, 2.6)
    ax.set_xlabel(r'$V_{in}$ (V)'); ax.set_ylabel(r'$V_{out}$ (V)')
    save(fig, 'f_sym')


def f_layout():
    fig, ax = canvas(0, 15, 0, 10.2, scale=0.42)
    gray = '#9ca3af'
    # rails
    ax.add_patch(Rectangle((0.5, 9.0), 8.5, 0.7, fc='#d1d5db', ec='none'))
    ax.add_patch(Rectangle((0.5, 0.5), 8.5, 0.7, fc='#d1d5db', ec='none'))
    # nwell
    ax.add_patch(Rectangle((1.0, 5.6), 7.2, 3.1, fc='#dcfce7', ec=G, lw=1.4, ls='--'))
    # p+ active (wide)
    ax.add_patch(Rectangle((2.0, 6.0), 5.0, 2.3, fc='#fed7aa', ec=P, lw=1.6))
    # n+ active (narrow)
    ax.add_patch(Rectangle((2.0, 2.0), 5.0, 1.0, fc='#bfdbfe', ec=N, lw=1.6))
    # metal straps: source contacts to rails, drain strap
    ax.add_patch(Rectangle((2.4, 6.3), 0.9, 3.0, fc=gray, ec='none', alpha=0.75))
    ax.add_patch(Rectangle((2.4, 0.9), 0.9, 2.0, fc=gray, ec='none', alpha=0.75))
    ax.add_patch(Rectangle((5.7, 2.2), 0.9, 5.9, fc=gray, ec='none', alpha=0.75))
    # poly gate
    ax.add_patch(Rectangle((4.2, 1.5), 0.55, 7.3, fc=R, ec='none', alpha=0.8))
    ax.add_patch(Rectangle((1.2, 4.3), 3.55, 0.6, fc=R, ec='none', alpha=0.8))
    # contacts
    for (cx, cy) in [(2.55, 7.4), (2.55, 6.6), (5.85, 7.4), (5.85, 6.6), (2.55, 2.25), (5.85, 2.25)]:
        ax.add_patch(Rectangle((cx, cy), 0.6, 0.5, fc='white', ec=INK, lw=1, hatch='////'))
    txt(ax, 0.9, 4.6, r'$V_{in}$', INK, 12, ha='right')
    notes = [(9.35, 'VDD rail (metal)', 9.35), (8.2, 'n-well (tied to VDD)', 8.2), (7.2, 'p+ active  =  PMOS (wide)', 7.15),
             (5.0, 'poly gate  =  shared input', 6.0), (4.6, 'metal: both drains → Vout', 4.6),
             (2.5, 'n+ active  =  NMOS (narrow)', 2.5), (0.85, 'GND rail (metal)', 0.85)]
    targets = [(8.9, 9.35), (8.2, 8.2), (7.0, 7.15), (4.75, 6.0), (6.6, 4.6), (7.0, 2.5), (8.9, 0.85)]
    for (y, s, ty), (tx, tyy) in zip(notes, targets):
        ax.plot([tx, 9.6], [tyy, ty], color=MUT, lw=0.7)
        txt(ax, 9.75, ty, s, INK, 10, ha='left')
    save(fig, 'f_layout')


def f_gain():
    VDD = 3.0
    kn = 134.3e-6 * 20; kR = 0.765625; kp = kn / kR
    lam_n, lam_p = 0.1, 0.2
    vin = np.linspace(0, VDD, 3000)

    def vo_l(v):
        f = lambda o: idn(v, o, kn, 0.7, lam_n) - idn(VDD - v, VDD - o, kp, 0.8, lam_p)
        lo, hi = 0.0, VDD
        for _ in range(80):
            m = (lo + hi) / 2
            if f(m) > 0: hi = m
            else: lo = m
        return (lo + hi) / 2
    vo = np.array([vo_l(v) for v in vin])
    g = np.gradient(vo, vin)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 2.9), gridspec_kw={'wspace': 0.32})
    a1.plot(vin, vo, color=INK, lw=2.2)
    a1.plot([0, 3], [0, 3], color='#c7cbd1', ls='--', lw=1)
    a1.set_xlabel(r'$V_{in}$ (V)'); a1.set_ylabel(r'$V_{out}$ (V)'); a1.set_title('VTC with λ ≠ 0: steep, not vertical', loc='left', fontsize=10.5)
    a2.plot(vin, -g, color=PU, lw=2.2)
    a2.set_xlabel(r'$V_{in}$ (V)'); a2.set_ylabel(r'$|A_v| = |dV_{out}/dV_{in}|$')
    a2.set_title('Small-signal gain peaks at $V_{th}$', loc='left', fontsize=10.5)
    a2.axvline(1.5, color='#d1d5db', lw=1, ls='--')
    a2.text(1.6, 12, 'large gain only\nnear $V_{th}=1.5$ V\n(finite because λ ≠ 0)', fontsize=9.5, color=PU)
    a2.set_xlim(0.8, 2.2); a2.set_ylim(0, 26)
    save(fig, 'f_gain')


def f_smallsignal():
    fig, ax = canvas(-3.6, 13.2, -3.1, 3.3)
    inverter(ax, 1.0, 0, vout=r'$v_{out}$', vin=r'$v_{in}$')
    txt(ax, 5.0, 0.3, '⇒', MUT, 20)
    x0 = 7.0
    wire(ax, [(x0, 1.4), (11.6, 1.4)])
    isrc(ax, x0, 1.4, 2.8, PU, None)
    res(ax, 9.5, 1.4, 2.8, INK, r'$r_{O1}\,\|\,r_{O2}$', 11)
    wire(ax, [(x0, -1.4), (9.5, -1.4)])
    gnd(ax, 8.25, -1.4)
    dot(ax, 9.5, 1.4); term(ax, 11.6, 1.4); txt(ax, 11.85, 1.4, r'$v_{out}$', INK, 12, ha='left')
    txt(ax, x0, 2.1, r'$(g_{m1}+g_{m2})\,v_{in}$', PU, 11)
    save(fig, 'f_smallsignal')


# ------------------------------------------------------------------ PART 3
def f_caps():
    fig, ax = canvas(-3.6, 17.5, -3.6, 4.4)
    io = inverter(ax, 1.0, 0, out_len=0.01, vout=None, vdd_label=None)
    txt(ax, 1.45, 2.35, r'$V_{DD}$', INK, 11, ha='left')
    # load node bus
    wire(ax, [(1.0, 0), (12.2, 0)])
    # Cgd caps (bridging gate and drain): draw dashed from gate bus to output
    gx = io['gx']
    # gate-drain overlap caps bridge INPUT and OUTPUT: draw them as one bridge above the inverter
    wire(ax, [(gx - 0.5, 0), (gx - 0.5, 3.3), (0.0, 3.3)], PU, ls='--', lw=1.4)
    dot(ax, gx - 0.5, 0, PU, 0.07)
    wire(ax, [(0.0, 3.05), (0.0, 3.55)], PU, lw=2.4); wire(ax, [(0.18, 3.05), (0.18, 3.55)], PU, lw=2.4)
    wire(ax, [(0.18, 3.3), (2.2, 3.3), (2.2, 0)], PU, ls='--', lw=1.4)
    dot(ax, 2.2, 0, PU, 0.07)
    txt(ax, 0.09, 3.95, r'$C_{gd,p}+C_{gd,n}$  (gate–drain overlap: input ↔ output)', PU, 10.5, ha='left')
    def gcap(x, c, lab, tied):
        dot(ax, x, 0)
        yb = cap(ax, x, 0, c, lab, 10.5, lead=0.55, ldx=0.4)
        if tied == 'gnd':
            gnd(ax, x, yb)
        else:
            wire(ax, [(x, yb), (x, yb - 0.25)], c)
            txt(ax, x, yb - 0.55, tied, c, 9.5)
    # Cdb,p goes to VDD (n-well): draw upward
    x = 3.6
    dot(ax, x, 0)
    wire(ax, [(x, 0), (x, 0.55)], G)
    wire(ax, [(x - 0.32, 0.55), (x + 0.32, 0.55)], G, lw=2.4); wire(ax, [(x - 0.32, 0.71), (x + 0.32, 0.71)], G, lw=2.4)
    wire(ax, [(x, 0.71), (x, 1.5)], G); vdd(ax, x, 1.5, r'$V_{DD}$', G, 10)
    txt(ax, x + 0.42, 0.95, r'$C_{db,p}$', G, 10.5, ha='left')
    gcap(3.6, G, r'$C_{db,n}$', 'gnd')
    gcap(5.9, AMB, r'$C_{int}$ (wire)', 'gnd')
    gcap(8.6, R, r'$C_g$', 'gnd')
    txt(ax, 9.9, -2.75, 'next stage', R, 10)
    # next inverter (small) gate
    inverter(ax, 14.0, 0, labels=False, vin=None, vout=None, in_len=0.01, out_len=0.9)
    wire(ax, [(12.2, 0), (12.8, 0)])
    txt(ax, 1.25, -0.35, r'$V_{out}$', INK, 11, ha='left', weight='bold')
    save(fig, 'f_caps')


def f_overlap():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.8, 3.1), gridspec_kw={'width_ratios': [1.3, 1], 'wspace': 0.25})
    a = a1; a.set_xlim(0, 10); a.set_ylim(0, 6); a.set_aspect('equal'); a.axis('off')
    a.add_patch(Rectangle((0.3, 0.6), 9.4, 2.4, fc='#f3f4f6', ec='#9ca3af'))
    a.text(9.4, 0.9, 'p-substrate', ha='right', fontsize=9, color=MUT)
    a.add_patch(Rectangle((0.8, 2.1), 3.0, 0.9, fc='#bfdbfe', ec=N))
    a.add_patch(Rectangle((6.2, 2.1), 3.0, 0.9, fc='#bfdbfe', ec=N))
    a.text(2.3, 2.55, 'n⁺ source', ha='center', fontsize=9); a.text(7.7, 2.55, 'n⁺ drain', ha='center', fontsize=9)
    a.add_patch(Rectangle((3.3, 3.1), 3.4, 0.25, fc='#fde68a', ec='none'))
    a.add_patch(Rectangle((3.3, 3.35), 3.4, 0.9, fc='#fca5a5', ec=R))
    a.text(5, 3.8, 'gate', ha='center', fontsize=9.5, weight='semibold')
    for x0 in [3.3, 6.2]:
        a.add_patch(Rectangle((x0, 2.1), 0.5, 1.0, fc='none', ec=PU, hatch='////', lw=0))
    a.annotate('', (3.3, 4.7), (3.8, 4.7), arrowprops=dict(arrowstyle='<|-|>', color=PU, lw=1))
    a.text(3.55, 5.0, r'$L_D$', color=PU, ha='center', fontsize=10.5)
    a.annotate('', (6.2, 4.7), (6.7, 4.7), arrowprops=dict(arrowstyle='<|-|>', color=PU, lw=1))
    a.text(6.45, 5.0, r'$L_D$', color=PU, ha='center', fontsize=10.5)
    a.annotate('', (3.8, 1.8), (6.2, 1.8), arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1))
    a.text(3.6, 1.2, r'$L_{eff}=L_{drawn}-2L_D$', ha='center', fontsize=9.5)
    a.text(5, 5.6, r'overlap: $C_{gd}=C_{gs}=C_{ox}WL_D$', ha='center', fontsize=10.5, color=PU)
    # C-V
    b = a2
    v = np.array([0, 0.7, 0.7, 2.0, 2.0, 3.0])
    b.plot([0, 1, 1, 2.2, 2.2, 3.2], [0.15, 0.15, 0.82, 0.82, 0.55, 0.55], color=N, lw=2.1, label=r'$C_{GS}$')
    b.plot([0, 2.2, 2.2, 3.2], [0.15, 0.15, 0.55, 0.55], color=P, lw=2.1, label=r'$C_{GD}$')
    b.set_xticks([1, 2.2]); b.set_xticklabels([r'$V_{TH}$', r'$V_D+V_{TH}$'])
    b.set_yticks([0.15, 0.55, 0.82]); b.set_yticklabels([r'$WC_{ov}$', r'$\frac{1}{2}WLC_{ox}$', r'$\frac{2}{3}WLC_{ox}$'], fontsize=9)
    b.text(0.25, 0.3, 'off', fontsize=9, color=MUT); b.text(1.25, 0.9, 'saturation', fontsize=9, color=MUT); b.text(2.35, 0.65, 'triode', fontsize=9, color=MUT)
    b.set_xlabel(r'$V_{GS}$ (fixed $V_D$)'); b.legend(loc='upper left', fontsize=9.5, bbox_to_anchor=(0, 0.88))
    b.set_ylim(0, 1.05); b.set_title('After Razavi Fig. 2.34 (overlap terms\nadded on)', loc='left', fontsize=9.5)
    save(fig, 'f_overlap')


def f_lumped():
    fig, ax = canvas(-4.2, 18.4, -3.6, 3.4)
    for k, x0 in [('fall', 1.0), ('rise', 12.0)]:
        on = N if k == 'fall' else P
        inverter(ax, x0, 0, vout=r'$V_{out}$', out_len=2.6, labels=False,
                 vin=r'$V_{in}$: 0 → $V_{DD}$' if k == 'fall' else r'$V_{in}$: $V_{DD}$ → 0',
                 cn=N if k == 'fall' else '#c4c8cf', cp=P if k == 'rise' else '#c4c8cf', lsize=11)
        xc = x0 + 1.6
        dot(ax, xc, 0)
        yb = cap(ax, xc, 0, INK, r'$C_{load}$', 11, lead=0.6)
        gnd(ax, xc, yb)
        if k == 'fall':
            wire(ax, [(xc - 0.3, -0.3), (x0 + 0.3, -0.3)], N, lw=2.4, z=9)
            arrow(ax, (x0 + 0.3, -0.3), (x0 + 0.3, -2.0), N, lw=2.4, ms=14, z=9)
            txt(ax, x0 + 1.4, 1.3, 'PMOS OFF', '#9ca3af', 10, ha='left')
            txt(ax, x0 + 0.8, -2.95, 'NMOS discharges $C_{load}$ → output falls  ($\\tau_{PHL}$)', N, 10.5)
        else:
            arrow(ax, (x0 + 0.3, 2.0), (x0 + 0.3, 0.3), P, lw=2.4, ms=14, z=9)
            wire(ax, [(x0 + 0.3, 0.3), (xc - 0.3, 0.3)], P, lw=2.4, z=9)
            arrow(ax, (xc - 0.6, 0.3), (xc - 0.15, 0.3), P, lw=2.4, ms=14, z=9)
            txt(ax, x0 + 2.25, -1.7, 'NMOS OFF', '#9ca3af', 10, ha='left')
            txt(ax, x0 + 0.8, -2.95, 'PMOS charges $C_{load}$ → output rises  ($\\tau_{PLH}$)', P, 10.5)
    save(fig, 'f_lumped')


def f_waves():
    t = np.linspace(0, 10, 2000)
    vin = np.where(t < 1, 0, np.where(t < 1.15, (t - 1) / 0.15, np.where(t < 6, 1, np.where(t < 6.15, 1 - (t - 6) / 0.15, 0))))
    vout = np.ones_like(t)
    m1 = (t >= 1.07) & (t < 6.07); vout[m1] = np.exp(-(t[m1] - 1.07) / 0.9)
    m2 = t >= 6.07; vout[m2] = 1 - (1 - np.exp(-5 / 0.9)) * np.exp(-(t[m2] - 6.07) / 1.5)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.8, 4.4), sharex=True, gridspec_kw={'hspace': 0.15, 'height_ratios': [1, 1.6]})
    a1.plot(t, vin, color=INK, lw=2); a1.set_ylabel(r'$V_{in}$'); a1.set_yticks([0, 0.5, 1]); a1.set_yticklabels([r'$V_{OL}$', r'$V_{50\%}$', r'$V_{OH}$'])
    a1.axhline(0.5, color='#d1d5db', ls='--', lw=0.9)
    a2.plot(t, vout, color=N, lw=2.3); a2.set_ylabel(r'$V_{out}$')
    for y in [0.1, 0.5, 0.9]:
        a2.axhline(y, color='#d1d5db', ls='--', lw=0.9)
    a2.set_yticks([0, 0.1, 0.5, 0.9, 1]); a2.set_yticklabels([r'$V_{OL}$', '10%', r'$V_{50\%}$', '90%', r'$V_{OH}$'])
    t1, t3 = 1.075, 6.075
    t2 = 1.07 + 0.9 * np.log(2); t4 = 6.07 + 1.5 * np.log(2 * (1 - np.exp(-5 / 0.9)))
    for x in [t1, t2, t3, t4]:
        a1.axvline(x, color='#9ca3af', ls=':', lw=0.9); a2.axvline(x, color='#9ca3af', ls=':', lw=0.9)
    a2.annotate('', (t1, 0.5), (t2, 0.5), arrowprops=dict(arrowstyle='<|-|>', color=PU, lw=1.3))
    a2.text(t2 + 0.15, 0.56, r'$\tau_{PHL}=t_2-t_1$', color=PU, fontsize=10.5)
    a2.annotate('', (t3, 0.5), (t4, 0.5), arrowprops=dict(arrowstyle='<|-|>', color=PU, lw=1.3))
    a2.text(t4 + 0.15, 0.42, r'$\tau_{PLH}=t_4-t_3$', color=PU, fontsize=10.5)
    tf0 = 1.07 + 0.9 * np.log(1 / 0.9); tf1 = 1.07 + 0.9 * np.log(1 / 0.1)
    a2.annotate('', (tf0, 0.22), (tf1, 0.22), arrowprops=dict(arrowstyle='<|-|>', color=P, lw=1.2))
    a2.text(tf1 + 0.1, 0.22, r'$t_{fall}$ (90%→10%)', color=P, fontsize=10, va='center')
    k = 1 - np.exp(-5 / 0.9)
    tr0 = 6.07 + 1.5 * np.log(k / 0.9); tr1 = 6.07 + 1.5 * np.log(k / 0.1)
    a2.annotate('', (tr0, 0.78), (tr1, 0.78), arrowprops=dict(arrowstyle='<|-|>', color=G, lw=1.2))
    a2.text(tr0 - 0.1, 0.78, r'$t_{rise}$ (10%→90%)', color=G, fontsize=10, va='center', ha='right')
    a2.set_xticks([t1, t2, t3, t4]); a2.set_xticklabels([r'$t_1$', r'$t_2$', r'$t_3$', r'$t_4$'])
    a2.set_xlabel('time'); a2.set_xlim(0, 10)
    for a in (a1, a2):
        a.grid(False)
    save(fig, 'f_waves')


def f_avg():
    VDD = 3.3; kn = 200e-6; vt = 0.6
    vo = np.linspace(0, VDD, 400)
    i = np.array([idn(VDD, v, kn, vt) for v in vo]) * 1e6
    fig, ax = plotfig(6.2, 3.3)
    ax.plot(vo, i, color=N, lw=2.4)
    m = vo >= 1.65
    ax.fill_between(vo[m], 0, i[m], color=N, alpha=0.08)
    ax.plot([1.65, 3.3], [673.9, 673.9], color=P, ls='--', lw=1.8)
    ax.text(0.1, 770, r'$I_{avg}=\frac{729+619}{2}=674$ µA  (dashed line)', color=P, fontsize=10.5)
    ax.plot([1.65, 3.3], [618.75, 729], 'o', color=INK, ms=6, zorder=5)
    ax.text(1.72, 545, '619 µA (linear)', ha='left', fontsize=9.5)
    ax.text(3.25, 770, '729 µA (sat.)', ha='right', fontsize=9.5)
    ax.axvline(2.7, color='#d1d5db', ls='--', lw=1)
    ax.text(2.65, 80, 'linear', ha='right', fontsize=9, color=MUT); ax.text(2.75, 80, 'sat.', fontsize=9, color=MUT)
    ax.set_xlabel(r'$V_{out}$ (V)       ← time runs this way during the fall')
    ax.set_ylabel(r'$i_{D,n}$ (µA)'); ax.set_xlim(0, 3.4); ax.set_ylim(0, 860)
    save(fig, 'f_avg')


def f_exact():
    VDD, C, kn, vt = 3.3, 0.3e-12, 200e-6, 0.6
    dt = 1e-13; v = VDD; ts = [0]; vs = [v]; t = 0
    while t < 2.2e-9:
        i = idn(VDD, v, kn, vt); v -= i / C * dt; t += dt; ts.append(t); vs.append(v)
    ts = np.array(ts) * 1e12; vs = np.array(vs)
    t1p = 2 * C * vt / (kn * (VDD - vt) ** 2) * 1e12
    t2 = 703.0
    fig, ax = plotfig(6.6, 3.4)
    ax.axvspan(0, t1p, color=N, alpha=0.07); ax.axvspan(t1p, t2, color=G, alpha=0.07)
    ax.plot(ts, vs, color=N, lw=2.4)
    s = 673.9e-6 / C * 1e-12
    ax.plot([0, 1.65 / s], [3.3, 1.65], color=P, ls='--', lw=1.6)
    for y, l in [(3.3, r'$V_{OH}=3.3$'), (2.7, r'$V_{OH}-V_{T0,n}=2.7$'), (1.65, r'$V_{50\%}=1.65$')]:
        ax.axhline(y, color='#e5e7eb', lw=0.9, ls='--')
    ax.set_yticks([0, 1.65, 2.7, 3.3]); ax.set_yticklabels(['0', r'$V_{50\%}=1.65$', r'$V_{OH}-V_{T0,n}=2.7$', r'$V_{OH}=3.3$'], fontsize=9)
    ax.set_xticks([0, t1p, t2, 1400, 2100]); ax.set_xticklabels(['0', f"$t_1'$\n{t1p:.0f} ps", '$t_2$\n703 ps', '1400', '2100'], fontsize=9)
    ax.text(t1p / 2, 0.45, 'NMOS\nsat.', ha='center', fontsize=9, color=N)
    ax.text((t1p + t2) / 2, 0.45, 'NMOS\nlinear', ha='center', fontsize=9, color=G)
    ax.text(900, 2.75, 'dashed: average-current method\n(straight line, slope $-I_{avg}/C_{load}$)', fontsize=9, color=P)
    ax.set_xlim(0, 2200); ax.set_ylim(0, 3.5); ax.grid(False)
    ax.set_xlabel('time after the input step (ps)'); ax.set_ylabel(r'$V_{out}$ (V)')
    save(fig, 'f_exact')


def f_sizing():
    # model: Cload = Cfix + c*(1+beta) (self + next-stage loading); tau_PHL ~ Cload/kn ; tau_PLH ~ Cload/(kp), kp = kn*beta/2.5
    beta = np.linspace(0.6, 5, 300)
    Cfix, c = 0.0, 8.0
    Cl = Cfix + c * (1 + beta)
    phl = 5 * Cl
    plh = 5 * Cl / (beta / 2.5)
    tp = (phl + plh) / 2
    fig, ax = plotfig(5.8, 3.3)
    ax.plot(beta, phl, color=N, lw=2.2, label=r'$\tau_{PHL}$ (NMOS pulls down)')
    ax.plot(beta, plh, color=P, lw=2.2, label=r'$\tau_{PLH}$ (PMOS pulls up)')
    ax.plot(beta, tp, color=INK, lw=2.2, label=r'$\tau_P$ (average)')
    b_eq = 2.5; ax.plot(b_eq, 5 * (Cfix + c * (1 + b_eq)), 'o', color=PU, ms=7, zorder=5)
    ib = np.argmin(tp); ax.plot(beta[ib], tp[ib], 'o', color=INK, ms=7, zorder=5)
    ax.annotate(r'equal edges at $\beta=\mu_n/\mu_p\approx2.5$', (b_eq, 5 * (Cfix + c * (1 + b_eq))), (3.0, 60),
                fontsize=9.5, color=PU, arrowprops=dict(arrowstyle='-', color=PU, lw=0.8))
    ax.annotate(rf'min. average at $\beta=\sqrt{{\mu_n/\mu_p}}\approx{beta[ib]:.1f}$', (beta[ib], tp[ib]), (0.6, 25),
                fontsize=9.5, color=INK, arrowprops=dict(arrowstyle='-', color=INK, lw=0.8))
    ax.set_ylim(0, 380); ax.set_xlim(0.5, 5)
    ax.set_xlabel(r'$\beta=(W/L)_p\,/\,(W/L)_n$'); ax.set_ylabel('delay (ps, model)')
    ax.legend(loc='upper right', fontsize=9)
    save(fig, 'f_sizing')


def mini_inv(ax, x, y, s=1.0, c=INK):
    tri = Polygon([(x, y + 0.55 * s), (x, y - 0.55 * s), (x + 0.95 * s, y)], closed=True, fc='white', ec=c, lw=LW, zorder=4)
    ax.add_patch(tri)
    ax.add_patch(Circle((x + 1.05 * s, y), 0.1 * s, fc='white', ec=c, lw=LW, zorder=5))
    return (x, y), (x + 1.15 * s, y)


def f_ring():
    fig, ax = canvas(-0.6, 14.4, -1.9, 1.3)
    xs = [0.6 + i * 2.7 for i in range(5)]
    outs = []
    for i, x in enumerate(xs):
        a, b = mini_inv(ax, x, 0)
        if i > 0:
            wire(ax, [outs[-1], a])
        outs.append(b)
        txt(ax, x + 0.4, 0.85, f'{i + 1}', MUT, 10)
    for o in outs[:-1]:
        wire(ax, [o, (o[0] + 0.5, 0)])
    end = outs[-1]
    wire(ax, [end, (end[0] + 0.5, 0), (end[0] + 0.5, -1.2), (-0.1, -1.2), (-0.1, 0), (0.6, 0)])
    arrow(ax, (7.5, -1.2), (6.5, -1.2), INK, ms=13)
    txt(ax, 7.0, -1.65, r'$N=5$ (odd) inverters in a loop:  one period $T=2N\tau_P$', INK, 11)
    save(fig, 'f_ring')


def f_razavi253():
    fig, ax = canvas(-3.4, 15.0, -3.6, 2.9)
    # (a) source follower charging C1
    m = mos(ax, 0.8, 0.6, 'n', N, r'$M_1$')
    wire(ax, [m['d'], (1.25, 2.0)]); vdd(ax, 1.25, 2.0, r'$V_{DD}=3$ V', INK, 11)
    wire(ax, [m['g'], (-1.0, 0.6)]); term(ax, -1.0, 0.6); txt(ax, -1.2, 0.6, r'$V_{in}$: 0→3 V', INK, 10.5, ha='right')
    wire(ax, [m['s'], (1.25, -0.8)]); dot(ax, 1.25, -0.8)
    wire(ax, [(1.25, -0.8), (2.4, -0.8)]); term(ax, 2.4, -0.8); txt(ax, 2.6, -0.8, r'$V_X$', INK, 12, ha='left')
    yb = cap(ax, 1.25, -0.8, INK, r'$C_1$ (starts at 1 V)', 10, lead=0.5)
    gnd(ax, 1.25, yb)
    txt(ax, 0.6, -3.35, '(a) Q3.5: source follower', MUT, 10.5)
    # (b) common source discharging C1
    x = 9.6
    m = mos(ax, x, -0.6, 'n', N, r'$M_1$')
    wire(ax, [m['s'], (x + 0.45, -1.8)]); gnd(ax, x + 0.45, -1.8)
    wire(ax, [m['g'], (x - 1.8, -0.6)]); term(ax, x - 1.8, -0.6); txt(ax, x - 2.0, -0.6, r'$V_{in}$: 0→3 V', INK, 10.5, ha='right')
    wire(ax, [m['d'], (x + 0.45, 1.4), (x + 1.9, 1.4)]); dot(ax, x + 0.45, 1.4)
    dot(ax, x + 1.9, 1.4)
    wire(ax, [(x + 1.9, 1.4), (x + 3.0, 1.4)]); term(ax, x + 3.0, 1.4); txt(ax, x + 3.2, 1.4, r'$V_X$', INK, 12, ha='left')
    yb = cap(ax, x + 1.9, 1.4, INK, r'$C_1$ (1 V)', 10, lead=1.0)
    gnd(ax, x + 1.9, yb)
    txt(ax, x + 0.5, -3.35, '(b) Q3.4: discharge to ground', MUT, 10.5)
    save(fig, 'f_razavi253')


def f_razavi_ans():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 2.6), gridspec_kw={'wspace': 0.3})
    tau = np.linspace(0, 10, 300)
    # (a) dV/dt' = (2.3 - V)^2 /2 with t' = t kn/C -> 1/(2.3-V) = 1/1.3 + t'/2
    Va = 2.3 - 1 / (1 / 1.3 + tau / 2)
    a1.plot(tau, Va, color=N, lw=2.2)
    a1.axhline(2.3, color=R, ls='--', lw=1); a1.text(0.3, 2.36, r'$V_{in}-V_{TH}=2.3$ V (approached, never reached)', fontsize=8.5, color=R)
    a1.set_title('(a) source follower: saturated, slows down', loc='left', fontsize=10)
    a1.set_xlabel(r'$t\,/\,(C_1/k_n)$'); a1.set_ylabel(r'$V_X$ (V)'); a1.set_ylim(0.9, 2.55)
    tb = np.linspace(0, 3, 300)
    # linear discharge: V = 2Vov V0 e^{-2Vov t'} ... solve: ln(V0(2a-V)/(V(2a-V0))) = a t', a=2.3
    a = 2.3; V0 = 1.0
    E = np.exp(a * tb * 2 / 2)  # t = C/(kn a) ln(...) -> ln(...) = a t'
    K = E * V0 / (2 * a - V0)
    Vb = 2 * a * K / (1 + K)
    Vb = 2 * a / (1 + (2 * a - V0) / V0 * np.exp(a * tb))
    a2.plot(tb, Vb, color=N, lw=2.2)
    a2.set_title('(b) discharge: triode, almost exponential', loc='left', fontsize=10)
    a2.set_xlabel(r'$t\,/\,(C_1/k_n)$'); a2.set_ylabel(r'$V_X$ (V)')
    save(fig, 'f_razavi_ans')


# ------------------------------------------------------------------ QUESTION FIGURES
def q_inv(name, lines, cload=None, vin=r'$V_{in}$', vout=r'$V_{out}$', w=5.6, card_x=5.3):
    fig, ax = canvas(-3.0, card_x + w + 0.3, -3.0, 3.2)
    inverter(ax, 0.9, 0, vin=vin, vout=vout, out_len=2.9 if cload else 1.3, lsize=11.5, mdx=0.62)
    if cload:
        dot(ax, 2.5, 0)
        yb = cap(ax, 2.5, 0, INK, cload, 10.5, lead=0.55)
        gnd(ax, 2.5, yb)
    card(ax, card_x, 2.3, lines, INK, 10.5, dy=0.62, w=w)
    save(fig, name)


def q_nmos_bias():
    fig, ax = canvas(-3.2, 15.4, -2.6, 2.8)
    m = mos(ax, 0.6, 0, 'n', N, None)
    wire(ax, [m['g'], (-1.2, 0)]); term(ax, -1.2, 0); txt(ax, -1.4, 0, r'$V_{GS}=1.5$ V', N, 11, ha='right')
    wire(ax, [m['d'], (1.05, 1.4)]); term(ax, 1.05, 1.4); txt(ax, 1.3, 1.4, r'$V_{DS}=0.5$ V', N, 11, ha='left')
    gnd(ax, *m['s'])
    txt(ax, 0.6, -2.1, 'Q0.1', MUT, 10)
    x = 9.4
    io = inverter(ax, x, 0, vin=r'$V_{in}=1.0$ V', vout=r'$V_{out}=2.9$ V', vdd_label=r'$V_{DD}=3.3$ V', lsize=11, labels=False)
    txt(ax, x + 0.3, 1.3, '← which region?', P, 10, ha='left')
    txt(ax, x + 1.4, -2.1, 'Q0.2', MUT, 10)
    save(fig, 'q_p0')


def q_razavi21():
    fig, ax = canvas(-3.0, 12.2, -2.4, 2.6)
    m = mos(ax, 0.6, 0, 'n', N, r'$50/0.5$', 10.5)
    wire(ax, [m['g'], (-1.2, 0)]); term(ax, -1.2, 0); txt(ax, -1.4, 0, r'$1.5$ V', INK, 11, ha='right')
    wire(ax, [m['d'], (1.05, 1.5)]); vdd(ax, 1.05, 1.5, r'$3$ V', INK, 11)
    gnd(ax, *m['s'])
    arrow(ax, (2.6, 0.9), (2.6, -0.9), N); txt(ax, 2.8, 0, r'$I_{D}$ = ?', N, 11, ha='left')
    x = 8.0
    m = mos(ax, x, 0, 'p', P, r'$50/0.5$', 10.5)
    wire(ax, [m['s'], (x + 0.45, 1.5)]); vdd(ax, x + 0.45, 1.5, r'$3$ V', INK, 11)
    wire(ax, [m['g'], (x - 1.2, 0)]); term(ax, x - 1.2, 0); txt(ax, x - 1.4, 0, r'$1.5$ V', INK, 11, ha='right')
    gnd(ax, *m['d'])
    arrow(ax, (x + 2.0, 0.9), (x + 2.0, -0.9), P); txt(ax, x + 2.2, 0, r'$|I_{D}|$ = ?', P, 11, ha='left')
    save(fig, 'q_razavi21')


def q_levels():
    fig, ax = plt.subplots(figsize=(4.6, 2.5))
    ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(-0.3, 3.8)
    for x0, lab, pairs in [(1.0, 'driver', [(3.3, r'$V_{OH}=3.3$'), (0.2, r'$V_{OL}=0.2$')]),
                           (6.0, 'receiver', [(1.9, r'$V_{IH}=1.9$'), (1.2, r'$V_{IL}=1.2$')])]:
        ax.add_patch(Rectangle((x0, 0), 1.2, 3.3, fc='#f9fafb', ec='#d1d5db'))
        ax.text(x0 + 0.6, 3.6, lab, ha='center', fontsize=10)
        for y, s in pairs:
            ax.plot([x0, x0 + 1.2], [y, y], color=N if 'driver' == lab else P, lw=2)
            ax.text(x0 + 1.4, y, s + ' V', va='center', fontsize=10.5)
    save(fig, 'q_levels')


def q_testpoints():
    VDD = 3.3
    vin, vo = vtc(VDD, 0.6, -0.7, 200, 80, 1200)
    fig, ax = plotfig(4.6, 3.0)
    ax.plot(vin, vo, color=INK, lw=2.2)
    pts = [(0.4, 3.3), (1.0, 3.170), (2.0, 0.052), (3.0, 0.0)]
    for x, y in pts:
        ax.plot(x, y, 'o', color=PU, ms=7, zorder=5, mec='white', mew=1)
        ax.text(x + 0.07, y + 0.18, f'({x:g}, {y:g})', fontsize=9, color=PU)
    ax.set_xlabel(r'$V_{in}$ (V)'); ax.set_ylabel(r'$V_{out}$ (V)'); ax.set_ylim(-0.15, 3.7); ax.set_xlim(0, 3.5)
    save(fig, 'q_testpoints')


def q_cmos_vs_r():
    fig, ax = canvas(-3.0, 15.5, -3.0, 3.2)
    inverter(ax, 0.9, 0, labels=False)
    txt(ax, 0.9, -2.85, 'CMOS', INK, 10.5, weight='semibold')
    x = 11.0
    vdd(ax, x, 2.2)
    res(ax, x, 2.2, 2.2, INK, r'$R_L$', 11)
    dot(ax, x, 0)
    m = mos(ax, x - 0.45, -1.3, 'n', N, None)
    wire(ax, [m['s'], (x, -2.2)]); gnd(ax, x, -2.2)
    wire(ax, [m['g'], (x - 2.4, -1.3), (x - 2.4, 0)]); term(ax, x - 2.4, 0); txt(ax, x - 2.6, 0, r'$V_{in}$', INK, 11.5, ha='right')
    wire(ax, [(x, 0), (x + 1.3, 0)]); term(ax, x + 1.3, 0); txt(ax, x + 1.5, 0, r'$V_{out}$', INK, 11.5, ha='left')
    txt(ax, x, -2.85, 'resistive load', INK, 10.5, weight='semibold')
    save(fig, 'q_cmos_vs_r')


def q_pseudo():
    fig, ax = canvas(-3.0, 11.4, -3.0, 3.3)
    x = 0.9
    mp = mos(ax, x - 0.45, 1.3, 'p', P, r'$M_2$')
    mn = mos(ax, x - 0.45, -1.3, 'n', N, r'$M_1$')
    wire(ax, [mp['d'], (x, 0), mn['d']])
    vdd(ax, x, 2.2, r'$V_{DD}=3.3$ V', INK, 11); wire(ax, [mp['s'], (x, 2.2)], P)
    gnd(ax, x, -2.2); wire(ax, [mn['s'], (x, -2.2)], N)
    wire(ax, [mp['g'], (-1.0, 1.3), (-1.0, 0.75)], P); gnd(ax, -1.0, 0.75, P)
    wire(ax, [mn['g'], (-1.6, -1.3)]); term(ax, -1.6, -1.3); txt(ax, -1.8, -1.3, r'$V_{in}$', INK, 11.5, ha='right')
    dot(ax, x, 0); wire(ax, [(x, 0), (x + 1.3, 0)]); term(ax, x + 1.3, 0); txt(ax, x + 1.5, 0, r'$V_{out}$', INK, 11.5, ha='left')
    txt(ax, -1.0, 1.75, 'gate\ngrounded', P, 9)
    card(ax, 5.0, 2.3, [r'$k_n=200$ µA/V²,  $V_{T0,n}=0.6$ V', r'$k_p=80$ µA/V²,  $V_{T0,p}=-0.7$ V', r'Find $V_{OL}$ and the power', r'drawn when $V_{in}=V_{DD}$'], INK, 10.5, dy=0.62, w=6.2)
    save(fig, 'q_pseudo')


def q_chain(name, top, bot):
    fig, ax = canvas(-3.0, 16.6, -3.0, 3.2)
    inverter(ax, 0.9, 0, labels=False, vout=None, out_len=1.5)
    txt(ax, 1.4, 1.3, top, P, 10.5, ha='left')
    txt(ax, 1.4, -1.3, bot, N, 10.5, ha='left')
    wire(ax, [(2.4, 0), (4.6, 0)])
    txt(ax, 3.3, 0.35, r'$V_{out}$', INK, 11)
    inverter(ax, 7.6, 0, labels=False, vin=None, vout=None, in_len=0.6, out_len=0.9)
    txt(ax, 8.1, 1.3, 'identical', MUT, 10, ha='left'); txt(ax, 8.1, -1.3, 'next stage', MUT, 10, ha='left')
    save(fig, name)


def q_power():
    fig, ax = canvas(-4.6, 12.8, -3.0, 3.2)
    inverter(ax, 0.9, 0, labels=False, vin=None, out_len=1.6, vdd_label=r'$V_{DD}=3$ V')
    dot(ax, 2.0, 0); yb = cap(ax, 2.0, 0, INK, r'$C_{load}=50$ fF', 10.5, lead=0.55); gnd(ax, 2.0, yb)
    # clock waveform on input
    xs = [-4.4, -3.9, -3.9, -3.2, -3.2, -2.5, -2.5, -2.1]
    ys = [-0.3, -0.3, 0.3, 0.3, -0.3, -0.3, 0.3, 0.3]
    wire(ax, list(zip(xs, [y + 0.0 for y in ys])), PU)
    txt(ax, -3.2, 0.75, r'$f=1$ GHz', PU, 10.5)
    card(ax, 6.2, 2.0, [r'One full $0\to1\to0$ cycle', r'per clock period', r'Find $P_{dyn}$'], INK, 10.5, dy=0.62, w=4.6)
    save(fig, 'q_power')


if __name__ == '__main__':
    fns = [f_symbols, f_ivcurves, f_vtc_crit, f_inverter, f_story, f_map, f_regions, f_slope, f_kr, f_sym, f_layout,
           f_gain, f_smallsignal, f_caps, f_overlap, f_lumped, f_waves, f_avg, f_exact, f_sizing, f_ring,
           f_razavi253, f_razavi_ans, q_nmos_bias, q_razavi21, q_levels, q_testpoints, q_cmos_vs_r, q_pseudo, q_power]
    only = sys.argv[1:]
    for f in fns:
        if not only or f.__name__ in only:
            f()
    if not only or 'qinv' in only:
        q_inv('q_11', [r'$V_{DD}=3.3$ V', r'$V_{T0,n}=0.6$ V,  $V_{T0,p}=-0.7$ V', r'$k_n=200$ µA/V²,  $k_p=80$ µA/V²', r'Find $V_{OH},V_{OL},V_{IL},V_{IH}$, NMs'])
        q_inv('q_21', [r'$V_{DD}=3.3$ V', r'NMOS: $0.6$ V, $60$ µA/V², $W/L=8$', r'PMOS: $-0.7$ V, $25$ µA/V², $W/L=12$', r'Find $V_{th}$ and both NMs'], w=6.3)
        q_inv('q_22', [r'$V_{DD}=2.5$ V,  $V_{Tn}=-V_{Tp}=0.6$ V', r"$k'_n=3k'_p=120$ µA/V²", 'sized for equal rise & fall', r'Find $NM_L$, $NM_H$'], w=6.0)
        q_inv('q_23', [r'$V_{DD}=3.3$ V', r'$V_{T0,n}=0.6$ V,  $V_{T0,p}=-0.7$ V', r'$\mu_n/\mu_p=580/230$, same $t_{ox}$', r'Want $V_{th}=V_{DD}/2$:  $\beta$ = ?'])
        q_inv('q_24', [r'$V_{DD}=5$ V,  $V_T=\pm1$ V', r'symmetric design, then', r'redesigned with $k_R=4$', r'New $V_{th}$? Margins?'], w=5.0)
        q_inv('q_26', [r'Razavi Table 2.1 devices, $V_{DD}=3$ V', r'$V_{THN}=0.7$, $|V_{THP}|=0.8$ V', r'$\lambda_n=0.1$, $\lambda_p=0.2$ V$^{-1}$', r'$(W/L)_n=10/0.5$, want $V_{th}=1.5$ V'], w=6.4)
        q_inv('q_27', [r'Razavi Table 2.1 devices, $V_{DD}=3$ V', r'$\mu_nC_{ox}=134.3$, $\mu_pC_{ox}=38.4$ µA/V²', r'$(W/L)_n=(W/L)_p=10/0.5$', r'Find $V_{th}$'], w=6.6)
        q_inv('q_33', [r'Worked example 25.2 inverter', r'$V_{DD}=3.3$ V, $k_n=200$, $k_p=80$ µA/V²', r'$C_{load}=0.3$ pF (fixed)', r'Scale $(W/L)_p$ so $\tau_{PLH}=\tau_{PHL}$'], cload=r'$C_{load}$', w=6.6, card_x=7.2)
        q_inv('q_cap', [r'$V_{DD}=2.5$ V,  $V_{T0,n}=0.5$, $V_{T0,p}=-0.5$ V', r'$k_n=300$ µA/V²,  $k_p=150$ µA/V²', r'$C_{load}=50$ fF'], cload=r'$C_{load}$', w=7.0, card_x=7.2)
    if not only or 'chain' in only:
        q_chain('q_31', r'$W_p=2.5$ µm', r'$W_n=1$ µm')
        q_chain('q_37', r'$(W/L)_p=10/0.5$', r'$(W/L)_n=5/0.5$')
