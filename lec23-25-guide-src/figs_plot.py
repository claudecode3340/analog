"""Plots: every curve is computed from inv.py (square law, lambda = 0)."""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch, Circle
import inv
from sym import INK, MUTED, BLUE, ORANGE, AQUA, VIOLET, RED, YELLOW, GREEN, MAGENTA, mos, wire, arrow, text, dot, vdd, gnd

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figs')
GRID = '#e4e3df'
plt.rcParams.update({
    'font.family': 'Inter', 'font.size': 9.5, 'mathtext.fontset': 'stixsans', 'svg.fonttype': 'path',
    'axes.edgecolor': '#8a8984', 'axes.linewidth': 0.8, 'axes.labelcolor': INK, 'xtick.color': '#52514e',
    'ytick.color': '#52514e', 'axes.spines.top': False, 'axes.spines.right': False, 'lines.linewidth': 2.0,
    'axes.labelsize': 10.5, 'legend.frameon': False,
})


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + '.svg'), bbox_inches='tight', pad_inches=0.04, transparent=True)
    fig.savefig(os.path.join(OUT, name + '.png'), bbox_inches='tight', pad_inches=0.04, dpi=110, facecolor='white')
    plt.close(fig)


G = dict(vdd=5.0, kn=100e-6, kp=100e-6, vtn=1.0, vtp=-1.0)   # lecture-style generic inverter (kR = 1)


def vtc(p, n=1201):
    v = np.linspace(0, p['vdd'], n)
    return v, np.array([inv.vout_of(x, p) for x in v])


def ann(ax, xy, xytext, s, c=INK, fs=9.5, **kw):
    ax.annotate(s, xy=xy, xytext=xytext, fontsize=fs, color=c,
                arrowprops=dict(arrowstyle='-', color=c, lw=0.8, shrinkA=1, shrinkB=2), **kw)


# ---------------------------------------------------------------- prerequisites
def fig_idvds():
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.8))
    ax = axs[0]
    kn, vt = 1.0, 1.0
    vds = np.linspace(0, 5, 400)
    for vgs, c in [(2, '#9cc0ec'), (3, '#5f9ee3'), (4, BLUE), (5, '#174f94')]:
        ov = vgs - vt
        i = np.where(vds < ov, kn / 2 * (2 * ov * vds - vds ** 2), kn / 2 * ov ** 2)
        ax.plot(vds, i, color=c, lw=1.8)
        ax.text(5.05, kn / 2 * ov ** 2, f'$V_{{GS}}={vgs}$ V', va='center', fontsize=8.5, color=INK)
    x = np.linspace(0, 4, 100)
    ax.plot(x, kn / 2 * x ** 2, color=RED, lw=1.2, ls='--')
    ax.text(0.7, 5.6, 'edge of saturation\n$V_{DS}=V_{GS}-V_{Tn}$', color=RED, fontsize=8.5)
    ax.text(0.15, 7.7, 'LINEAR\n(triode)', fontsize=8.5, color=MUTED, weight='bold')
    ax.text(3.2, 1.0, 'SATURATION', fontsize=8.5, color=MUTED, weight='bold')
    ax.set_xlabel('$V_{DS}$ (V)'); ax.set_ylabel('$I_D$ (units of $k_n$·V²)')
    ax.set_xlim(0, 5); ax.set_ylim(0, 8.6)
    ax = axs[1]
    vgs = np.linspace(0, 5, 300)
    ax.plot(vgs, np.where(vgs > vt, 0.5 * (vgs - vt) ** 2, 0), color=BLUE, label='NMOS: $I_D$ vs $V_{GS}$')
    ax.plot(-vgs, np.where(vgs > vt, 0.5 * (vgs - vt) ** 2, 0), color=ORANGE, label='PMOS: $|I_D|$ vs $V_{GS}$')
    ax.axvline(0, color=GRID, lw=0.8)
    ax.text(0.2, 3.4, 'NMOS on for\n$V_{GS}>V_{Tn}>0$', color=BLUE, fontsize=8.5)
    ax.text(-2.4, 6.9, 'PMOS on for\n$V_{GS}<V_{Tp}<0$', color=ORANGE, fontsize=8.5)
    ax.set_xlabel('$V_{GS}$ (V)'); ax.set_ylabel('$|I_D|$ (sat.)')
    ax.set_xlim(-5, 5); ax.set_ylim(0, 8.6)
    fig.tight_layout(w_pad=2)
    save(fig, 'p_idvds')


def fig_vtc_generic():
    p = dict(vdd=5.0, kn=100e-6, kp=100e-6, vtn=1.0, vtp=-1.0)
    s = inv.summary(p)
    v, o = vtc(p)
    fig, ax = plt.subplots(figsize=(4.6, 3.6))
    ax.plot([0, 5], [0, 5], color=GRID, lw=1, ls='--')
    ax.text(4.05, 4.4, '$V_{out}=V_{in}$', color=MUTED, fontsize=8.5, rotation=38)
    ax.plot(v, o, color=INK, lw=2.2)
    # tangents of slope -1
    for x0, y0 in [(s['vil'], s['vout_il']), (s['vih'], s['vout_ih'])]:
        xx = np.array([x0 - 0.55, x0 + 0.55])
        ax.plot(xx, y0 - (xx - x0), color=RED, lw=1.4)
        ax.plot(x0, y0, 'o', ms=5, color=RED, zorder=5)
        ax.plot([x0, x0], [0, y0], color=RED, lw=0.8, ls=':')
    ax.plot(s['vth'], s['vth'], 'o', ms=5.5, color=VIOLET, zorder=5)
    ax.plot([s['vth']] * 2, [0, s['vth']], color=VIOLET, lw=0.8, ls=':')
    ax.text(s['vil'] - 0.45, s['vout_il'] + 0.25, 'slope $-1$', color=RED, fontsize=8.5)
    ax.text(s['vih'] + 0.25, s['vout_ih'] + 0.55, 'slope $-1$', color=RED, fontsize=8.5)
    ax.set_xticks([0, s['vil'], s['vth'], s['vih'], 5])
    ax.set_xticklabels(['0', '$V_{IL}$', '$V_{th}$', '$V_{IH}$', '$V_{DD}$'])
    ax.set_yticks([0, 5]); ax.set_yticklabels(['$V_{OL}=0$', '$V_{OH}=V_{DD}$'])
    ax.set_xlabel('$V_{in}$'); ax.set_ylabel('$V_{out}$')
    ax.set_xlim(0, 5.05); ax.set_ylim(-0.05, 5.3)
    ax.text(s['vth'] + 0.12, s['vth'] + 0.1, '$V_{in}=V_{out}$', color=VIOLET, fontsize=8.5)
    ax.text(0.2, 4.0, 'logic 1 out', color=MUTED, fontsize=8.5)
    ax.text(3.7, 0.4, 'logic 0 out', color=MUTED, fontsize=8.5)
    save(fig, 'p_vtc_generic')


def fig_nm_bars():
    p = dict(vdd=5.0, kn=100e-6, kp=100e-6, vtn=1.0, vtp=-1.0)
    s = inv.summary(p)
    fig, ax = plt.subplots(figsize=(3.2, 3.6))
    ax.axis('off')
    vdd_ = 5
    # output side (left) and input side (right)
    def bar(x, lo, hi, c, lab, lab_c=None):
        ax.add_patch(Rectangle((x, lo), 0.5, hi - lo, color=c, alpha=0.85, lw=0))
        ax.text(x + 0.25, (lo + hi) / 2, lab, ha='center', va='center', fontsize=8.2, color='white' if lab_c is None else lab_c, rotation=90)
    bar(0, 5 - 0.05, 5, INK, '')
    bar(0, 0, 0.05, INK, '')
    ax.add_patch(Rectangle((0, 0), 0.5, 5, fill=False, ec=MUTED, lw=0.8))
    ax.text(0.25, 5.35, 'driver\noutput', ha='center', fontsize=8.5, color=INK)
    ax.add_patch(Rectangle((2.2, 0), 0.5, 5, fill=False, ec=MUTED, lw=0.8))
    bar(2.2, s['vih'], 5, '#5f9ee3', 'reads as 1')
    bar(2.2, 0, s['vil'], '#ec8f69', 'reads as 0')
    ax.add_patch(Rectangle((2.2, s['vil']), 0.5, s['vih'] - s['vil'], color='#d0cfca', lw=0))
    ax.text(2.45, (s['vil'] + s['vih']) / 2, '?', ha='center', va='center', fontsize=9, color=INK)
    ax.text(2.45, 5.35, 'receiver\ninput', ha='center', fontsize=8.5, color=INK)
    for y, lab in [(5, '$V_{OH}$'), (0, '$V_{OL}$')]:
        ax.text(-0.1, y, lab, ha='right', va='center', fontsize=9)
    for y, lab in [(s['vih'], '$V_{IH}$'), (s['vil'], '$V_{IL}$')]:
        ax.text(2.8, y, lab, ha='left', va='center', fontsize=9)
        ax.plot([0.5, 2.2], [y, y], color=GRID, lw=0.8, ls='--')
    ax.add_patch(FancyArrowPatch((1.35, 5), (1.35, s['vih']), arrowstyle='<->', mutation_scale=9, color=BLUE, lw=1.2))
    ax.text(1.42, (5 + s['vih']) / 2, '$NM_H$', color=BLUE, fontsize=9, va='center')
    ax.add_patch(FancyArrowPatch((1.35, 0), (1.35, s['vil']), arrowstyle='<->', mutation_scale=9, color=ORANGE, lw=1.2))
    ax.text(1.42, s['vil'] / 2, '$NM_L$', color=ORANGE, fontsize=9, va='center')
    ax.plot([0.5, 2.2], [5, 5], color=GRID, lw=0.8, ls='--'); ax.plot([0.5, 2.2], [0, 0], color=GRID, lw=0.8, ls='--')
    ax.set_xlim(-0.8, 3.5); ax.set_ylim(-0.3, 6.0)
    save(fig, 'p_nm_bars')


def fig_partials():
    """partial fractions picture for the integral in Lec 25: 1/(V(a-V)) splits."""
    pass


# ---------------------------------------------------------------- Lecture 23
def fig_regionmap():
    p = dict(vdd=5.0, kn=100e-6, kp=100e-6, vtn=1.0, vtp=-1.0)
    s = inv.summary(p)
    v, o = vtc(p)
    V = 5
    fig, ax = plt.subplots(figsize=(6.6, 4.9))
    # NMOS saturated: Vin >= VTn and Vout >= Vin - VTn  (above line 1)
    ax.add_patch(Polygon([(1, 0), (1, V), (V, V), (V, V - 1)], closed=True, fc=BLUE, alpha=0.10, lw=0))
    ax.add_patch(Polygon([(1, 0), (1, V), (V, V), (V, V - 1)], closed=True, fill=False, hatch='||', ec=BLUE, alpha=0.25, lw=0))
    # PMOS saturated: Vin <= VDD + VTp and Vout <= Vin - VTp (below line 2)
    ax.add_patch(Polygon([(0, 0), (0, 1), (4, V), (4, 0)], closed=True, fc=ORANGE, alpha=0.10, lw=0))
    ax.add_patch(Polygon([(0, 0), (0, 1), (4, V), (4, 0)], closed=True, fill=False, hatch='--', ec=ORANGE, alpha=0.25, lw=0))
    x = np.linspace(0, V, 10)
    ax.plot(x, x - 1, color=BLUE, lw=1.4)
    ax.plot(x, x + 1, color=ORANGE, lw=1.4)
    ax.axvline(1, color=BLUE, lw=0.9, ls=':')
    ax.axvline(4, color=ORANGE, lw=0.9, ls=':')
    ax.plot(v, o, color=INK, lw=2.6, zorder=4)
    ax.text(4.08, 2.55, '$V_{out}=V_{in}-V_{T0,n}$\nNMOS sat. above', color=BLUE, fontsize=8.6, bbox=dict(fc='white', ec='none', pad=1.5))
    ax.text(0.12, 2.35, '$V_{out}=V_{in}-V_{T0,p}$\nPMOS sat. below', color=ORANGE, fontsize=8.6, bbox=dict(fc='white', ec='none', pad=1.5))
    # points
    pts = {'A': (0.5, 5.0), 'B': (s['vil'], s['vout_il']), 'C': (s['vth'], s['vth']),
           'D': (s['vih'], s['vout_ih']), 'E': (4.5, 0.0)}
    off = {'A': (0.0, 0.22), 'B': (0.1, 0.18), 'C': (0.16, 0.05), 'D': (0.15, 0.12), 'E': (0.0, 0.22)}
    for k, (a, b) in pts.items():
        ax.plot(a, b, 'o', ms=6.5, color=INK, mec='white', mew=1.2, zorder=6)
        ax.text(a + off[k][0], b + off[k][1], k, fontsize=11, weight='bold', color=INK, zorder=7)
    ax.set_xticks([0, 1, s['vil'], s['vth'], s['vih'], 4, 5])
    ax.set_xticklabels(['0', '$V_{T0,n}$', '$V_{IL}$', '$V_{th}$', '$V_{IH}$', '$V_{DD}+V_{T0,p}$', '$V_{DD}$'], fontsize=8.5)
    ax.set_yticks([0, 1, 4, 5]); ax.set_yticklabels(['0', '$|V_{T0,p}|$', '$V_{DD}-V_{T0,n}$', '$V_{DD}$'], fontsize=8.5)
    ax.set_xlim(0, V); ax.set_ylim(0, V + 0.02)
    ax.set_xlabel('$V_{in}$'); ax.set_ylabel('$V_{out}$')
    save(fig, 'p_regionmap')


def fig_vtc_current():
    p = dict(vdd=5.0, kn=100e-6, kp=100e-6, vtn=1.0, vtp=-1.0)
    s = inv.summary(p)
    v, o = vtc(p, 2001)
    i = np.array([inv.idn(a, b, p['kn'], p['vtn']) for a, b in zip(v, o)])
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.8, 5.0), sharex=True, gridspec_kw=dict(height_ratios=[1.6, 1], hspace=0.12))
    bounds = [0, 1, s['vil'], s['vth'] - 0.0001, s['vth'] + 0.0001, s['vih'], 4, 5]
    segs = [(0, 1, 'A', '#8a8984'), (1, s['vth'], 'B', BLUE), (s['vth'], s['vth'], 'C', VIOLET),
            (s['vth'], 4, 'D', ORANGE), (4, 5, 'E', '#8a8984')]
    reg = [(0, 1, 'A', 'n: off\np: lin'), (1, s['vth'] - 0.01, 'B', 'n: sat\np: lin'), (s['vth'] - 0.01, s['vth'] + 0.01, 'C', ''),
           (s['vth'] + 0.01, 4, 'D', 'n: lin\np: sat'), (4, 5, 'E', 'n: lin\np: off')]
    cols = {'A': '#8a8984', 'B': BLUE, 'C': VIOLET, 'D': ORANGE, 'E': '#8a8984'}
    for a, b, k, lab in reg:
        m = (v >= a) & (v <= b)
        ax1.plot(v[m], o[m], color=cols[k], lw=2.6)
        if lab:
            ax1.text((a + b) / 2, 5.45, k, ha='center', fontsize=10.5, weight='bold', color=cols[k])
            ax1.text((a + b) / 2 + (0.0 if k not in 'B' else -0.05), (2.25 if k in 'AE' else (4.2 if k == 'D' else 0.9)), lab, ha='center', fontsize=7.8, color=cols[k])
        ax2.plot(v[m], i[m] * 1e6, color=cols[k], lw=2.2)
    ax1.plot(s['vth'], s['vth'], 'o', color=VIOLET, ms=6)
    ax1.annotate('C: both saturated\n(vertical in this\n$\\lambda=0$ model)', xy=(s['vth'], s['vth']), xytext=(3.25, 2.4), fontsize=7.8, color=VIOLET,
                 arrowprops=dict(arrowstyle='-', color=VIOLET, lw=0.8))
    for x in [1, s['vth'], 4]:
        ax1.axvline(x, color=GRID, lw=0.8, zorder=0); ax2.axvline(x, color=GRID, lw=0.8, zorder=0)
    ax1.set_ylabel('$V_{out}$ (V)'); ax1.set_ylim(-0.1, 5.9)
    ax2.set_ylabel('$I_{D,n}=I_{D,p}$ (µA)')
    ax2.set_xlabel('$V_{in}$ (V)')
    peak = p['kn'] / 2 * (s['vth'] - 1) ** 2 * 1e6
    ax2.annotate(f'peak at $V_{{th}}$ = {peak:.0f} µA', xy=(s['vth'], peak), xytext=(3.2, peak * 0.85),
                 fontsize=8.2, color=INK, arrowprops=dict(arrowstyle='-', color=INK, lw=0.8))
    ax2.text(0.1, peak * 0.2, 'zero static\ncurrent', fontsize=8, color=MUTED)
    ax2.text(4.1, peak * 0.2, 'zero static\ncurrent', fontsize=8, color=MUTED)
    ax2.set_xlim(0, 5)
    save(fig, 'p_vtc_current')


def fig_slope():
    p = dict(vdd=5.0, kn=100e-6, kp=100e-6, vtn=1.0, vtp=-1.0)
    s = inv.summary(p)
    v, o = vtc(p, 4001)
    g = np.gradient(o, v)
    g = np.clip(g, -12, 1)
    fig, ax = plt.subplots(figsize=(4.4, 2.5))
    ax.plot(v, g, color=INK, lw=1.8)
    ax.axhline(-1, color=RED, lw=1.1, ls='--')
    ax.text(0.1, -1.9, '$dV_{out}/dV_{in}=-1$', color=RED, fontsize=8.5)
    for x in [s['vil'], s['vih']]:
        ax.plot(x, -1, 'o', color=RED, ms=5)
    ax.fill_between(v, g, -1, where=(g < -1), color=RED, alpha=0.08)
    ax.text(s['vth'], -6, '$|$gain$|>1$:\nnoise grows\n(forbidden zone)', ha='center', fontsize=8, color=RED)
    ax.text(0.15, -4.0, '$|$gain$|<1$:\nnoise shrinks', fontsize=8, color=MUTED)
    ax.set_xticks([0, s['vil'], s['vth'], s['vih'], 5]); ax.set_xticklabels(['0', '$V_{IL}$', '$V_{th}$', '$V_{IH}$', '$V_{DD}$'])
    ax.set_ylim(-12.5, 0.8); ax.set_xlim(0, 5)
    ax.set_ylabel('slope $dV_{out}/dV_{in}$'); ax.set_xlabel('$V_{in}$')
    save(fig, 'p_slope')


def fig_loadline():
    p = dict(vdd=5.0, kn=100e-6, kp=100e-6, vtn=1.0, vtp=-1.0)
    vo = np.linspace(0, 5, 400)
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    vins = [1.5, 2.0, 2.5, 3.0, 3.5]
    shades_b = ['#a9c8ef', '#79a9e8', BLUE, '#1f5fae', '#143f75']
    shades_o = ['#7a2f10', '#a8431b', ORANGE, '#f19267', '#f5b898']
    for k, vi in enumerate(vins):
        In = np.array([inv.idn(vi, x, p['kn'], p['vtn']) for x in vo]) * 1e6
        Ip = np.array([inv.idp(vi, x, p['kp'], p['vtp'], 5) for x in vo]) * 1e6
        ax.plot(vo, In, color=shades_b[k], lw=1.6)
        ax.plot(vo, Ip, color=shades_o[k], lw=1.6, ls='-')
        x = inv.vout_of(vi, p)
        y = inv.idn(vi, x, p['kn'], p['vtn']) * 1e6
        ax.plot(x, y, 'o', color=INK, ms=5.5, mec='white', mew=1, zorder=5)
        ax.text(x + (0.08 if vi != 2.5 else 0.1), y + 8, f'$V_{{in}}$={vi}', fontsize=7.8, color=INK)
    ax.text(4.2, 330, 'NMOS $I_{D,n}(V_{out})$\nrises with $V_{in}$', color=BLUE, fontsize=8.5)
    ax.text(0.05, 360, 'PMOS $I_{D,p}(V_{out})$\nfalls with $V_{in}$', color=ORANGE, fontsize=8.5)
    ax.set_xlabel('$V_{out}$ (V)'); ax.set_ylabel('current (µA)')
    ax.set_ylim(0, 420); ax.set_xlim(0, 5)
    ax.set_title('Each dot (equal currents) is one point of the VTC', fontsize=9, loc='left', color=MUTED)
    save(fig, 'p_loadline')


# ---------------------------------------------------------------- Lecture 24
def fig_kr_family():
    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    krs = [0.25, 0.5, 1, 2, 4]
    cols = [ORANGE, '#f19267', INK, '#5f9ee3', BLUE]
    for kr, c in zip(krs, cols):
        p = dict(vdd=5.0, kn=100e-6 * kr, kp=100e-6, vtn=1.0, vtp=-1.0)
        v, o = vtc(p)
        ax.plot(v, o, color=c, lw=2.0 if kr == 1 else 1.6)
        t = inv.vth(p)
        ax.plot(t, t, 'o', color=c, ms=4.5)
        ax.plot([], [], color=c, lw=2, label=f'$k_R$ = {kr:g}')
    ax.legend(loc='upper right', fontsize=8.5, handlelength=1.6, bbox_to_anchor=(1.0, 0.98))
    ax.plot([0, 5], [0, 5], color=GRID, lw=0.9, ls='--')
    ax.annotate('', xy=(1.75, 1.2), xytext=(3.25, 1.2), arrowprops=dict(arrowstyle='-|>', color=BLUE, lw=1.2))
    ax.text(0.15, 1.6, 'stronger NMOS\n→ $V_{th}$ moves left', color=BLUE, fontsize=8.5)
    ax.set_xlabel('$V_{in}$ (V)'); ax.set_ylabel('$V_{out}$ (V)')
    ax.set_xlim(0, 6.6); ax.set_ylim(0, 5.1); ax.set_xticks([0,1,2,3,4,5])
    save(fig, 'p_kr_family')


def fig_vth_kr():
    fig, ax = plt.subplots(figsize=(4.0, 3.0))
    kr = np.logspace(-2, 2, 300)
    for vdd_, c in [(5.0, INK), (3.3, BLUE)]:
        p = dict(vdd=vdd_, kp=1, vtn=0.7 if vdd_ == 3.3 else 1.0, vtp=-0.7 if vdd_ == 3.3 else -1.0)
        th = [inv.vth({**p, 'kn': k}) for k in kr]
        ax.semilogx(kr, th, color=c)
        ax.axhline(p['vtn'], color=c, lw=0.6, ls=':')
        ax.axhline(vdd_ + p['vtp'], color=c, lw=0.6, ls=':')
        ax.text(0.011, vdd_ / 2 + 0.12, f'$V_{{DD}}$={vdd_} V', color=c, fontsize=8)
    ax.axvline(1, color=GRID, lw=0.9)
    ax.text(1.1, 0.4, '$k_R=1$', fontsize=8, color=MUTED)
    ax.text(12, 3.6, '$V_{th}\\to V_{T0,n}$\nas $k_R\\to\\infty$', fontsize=8, color=MUTED)
    ax.text(0.012, 4.55, '$V_{th}\\to V_{DD}+V_{T0,p}$ as $k_R\\to 0$', fontsize=8, color=MUTED)
    ax.set_xlabel('$k_R=k_n/k_p$ (log scale)'); ax.set_ylabel('$V_{th}$ (V)')
    ax.set_ylim(0, 5)
    save(fig, 'p_vth_kr')


def fig_sym():
    p = dict(vdd=2.5, kn=120e-6, kp=120e-6, vtn=0.6, vtp=-0.6)
    s = inv.summary(p)
    v, o = vtc(p)
    fig, ax = plt.subplots(figsize=(4.8, 3.6))
    ax.plot(v, o, color=INK, lw=2.2)
    ax.plot([0, 2.5], [0, 2.5], color=GRID, lw=0.9, ls='--')
    ax.plot(1.25, 1.25, 'o', color=VIOLET, ms=6)
    for x0, y0 in [(s['vil'], s['vout_il']), (s['vih'], s['vout_ih'])]:
        ax.plot(x0, y0, 'o', color=RED, ms=5)
        ax.plot([x0, x0], [0, y0], color=RED, lw=0.8, ls=':')
    ax.annotate('', xy=(0, 0.25), xytext=(s['vil'], 0.25), arrowprops=dict(arrowstyle='<->', color=ORANGE, lw=1.1))
    ax.text(s['vil'] / 2, 0.36, f"$NM_L$ = {s['nml']:.4f} V", ha='center', fontsize=8.2, color=ORANGE)
    ax.annotate('', xy=(s['vih'], 2.25), xytext=(2.5, 2.25), arrowprops=dict(arrowstyle='<->', color=BLUE, lw=1.1))
    ax.text((s['vih'] + 2.5) / 2, 2.33, f"$NM_H$ = {s['nmh']:.4f}", ha='center', fontsize=8.2, color=BLUE)
    ax.text(1.32, 1.17, '$V_{th}=V_{DD}/2$', fontsize=8.2, color=VIOLET)
    ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0, 2.5])
    ax.text(s['vil'] - 0.05, s['vout_il'] - 0.25, '$V_{IL}$ = 1.0875', ha='right', fontsize=8.2, color=RED)
    ax.text(s['vih'] + 0.06, s['vout_ih'] + 0.12, '$V_{IH}$ = 1.4125', ha='left', fontsize=8.2, color=RED)
    ax.set_xlabel('$V_{in}$ (V)'); ax.set_ylabel('$V_{out}$ (V)')
    ax.set_xlim(0, 2.5); ax.set_ylim(0, 2.6)
    save(fig, 'p_sym')


def fig_layout():
    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    ax.set_aspect('equal'); ax.axis('off')
    NW, PD, ND, POLY, M1, CT = '#d9efe2', '#f6c5ae', '#b9d3f3', '#e34948', '#a3a29d', '#1d1d1b'
    ax.add_patch(Rectangle((0.8, 5.2), 5.4, 3.8, fc=NW, ec=AQUA, lw=1.2, ls='--'))
    ax.add_patch(Rectangle((1.6, 5.8), 3.6, 2.6, fc=PD, ec=ORANGE, lw=1.2))
    ax.add_patch(Rectangle((1.6, 1.4), 3.6, 1.0, fc=ND, ec=BLUE, lw=1.2))
    ax.add_patch(Rectangle((3.15, 0.9), 0.5, 8.0, fc=POLY, ec=POLY, alpha=0.85))
    ax.add_patch(Rectangle((1.2, 3.7), 2.45, 0.55, fc=POLY, ec=POLY, alpha=0.85))
    ax.add_patch(Rectangle((0.4, 9.4), 7.0, 0.7, fc=M1, ec=M1, alpha=0.7))
    ax.add_patch(Rectangle((0.4, -0.3), 7.0, 0.7, fc=M1, ec=M1, alpha=0.7))
    ax.add_patch(Rectangle((1.9, 6.1), 0.8, 3.6, fc=M1, ec=M1, alpha=0.7))
    ax.add_patch(Rectangle((1.9, 0.1), 0.8, 2.0, fc=M1, ec=M1, alpha=0.7))
    ax.add_patch(Rectangle((4.1, 1.7), 0.8, 6.4, fc=M1, ec=M1, alpha=0.7))
    ax.add_patch(Rectangle((4.1, 4.5), 3.3, 0.7, fc=M1, ec=M1, alpha=0.7))
    for (x, y) in [(2.1, 6.4), (2.1, 7.5), (4.3, 6.4), (4.3, 7.5), (2.1, 1.7), (4.3, 1.7)]:
        ax.add_patch(Rectangle((x, y), 0.4, 0.4, fc='white', ec=CT, lw=1, hatch='////'))
    ax.text(0.95, 3.97, '$V_{in}$', fontsize=11, va='center', ha='right')
    # labels on the right with leaders
    L = [((7.5, 9.75), '$V_{DD}$ rail (metal)', None), ((7.5, 4.85), '$V_{out}$ (metal joins both drains)', None),
         ((7.5, 0.05), 'GND rail (metal)', None),
         ((7.5, 8.3), 'n-well (tied to $V_{DD}$)', (6.2, 8.3)), ((7.5, 7.2), 'p$^+$ active: PMOS, wide ($W_p$)', (5.2, 7.2)),
         ((7.5, 6.1), 'poly gate (shared input)', (3.65, 6.0)), ((7.5, 1.9), 'n$^+$ active: NMOS ($W_n$)', (5.2, 1.9)),
         ((7.5, 3.0), 'contact (hatched)', (4.7, 1.9))]
    for (x, y), s, tgt in L:
        ax.text(x + 0.1, y, s, fontsize=8.8, va='center')
        if tgt:
            ax.plot([tgt[0], x], [tgt[1], y], color=MUTED, lw=0.6)
    ax.set_xlim(0, 13.5); ax.set_ylim(-0.6, 10.4)
    save(fig, 'p_layout')


def fig_xsec():
    fig, ax = plt.subplots(figsize=(6.6, 2.4))
    ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 12, 3, fc='#eceae4', ec=MUTED, lw=0.8))
    ax.text(0.2, 0.3, 'p-substrate (GND)', fontsize=8.5, color=MUTED)
    ax.add_patch(Rectangle((6.3, 1.0), 5.2, 2.0, fc='#cfe8d9', ec=AQUA, lw=0.8))
    ax.text(10.0, 1.2, 'n-well ($V_{DD}$)', fontsize=8.5, color='#11734f')
    for x, lab in [(1.0, 'S'), (3.6, 'D')]:
        ax.add_patch(Rectangle((x, 2.3), 1.4, 0.7, fc='#b9d3f3', ec=BLUE, lw=0.8))
        ax.text(x + 0.7, 2.6, 'n$^+$', fontsize=8, ha='center', color='#174f94')
    for x in [7.0, 9.6]:
        ax.add_patch(Rectangle((x, 2.3), 1.4, 0.7, fc='#f6c5ae', ec=ORANGE, lw=0.8))
        ax.text(x + 0.7, 2.6, 'p$^+$', fontsize=8, ha='center', color='#a8431b')
    for x0, x1 in [(2.25, 3.75), (8.25, 9.75)]:
        ax.add_patch(Rectangle((x0, 3.0), x1 - x0, 0.12, fc='#d0cfca', ec=MUTED, lw=0.6))
        ax.add_patch(Rectangle((x0, 3.12), x1 - x0, 0.45, fc=RED, alpha=0.8, lw=0))
    ax.text(3.0, 3.85, 'NMOS', ha='center', fontsize=9, color=BLUE, weight='bold')
    ax.text(9.0, 3.85, 'PMOS', ha='center', fontsize=9, color=ORANGE, weight='bold')
    ax.text(6.0, 4.4, '$V_{in}$ on both gates;  both drains (inner) → $V_{out}$', ha='center', fontsize=8.5)
    ax.set_xlim(-0.2, 12.2); ax.set_ylim(-0.2, 4.7)
    save(fig, 'p_xsec')


# ---------------------------------------------------------------- Lecture 25
def fig_overlap():
    fig, ax = plt.subplots(figsize=(6.0, 2.6))
    ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 10, 3, fc='#eceae4', ec=MUTED, lw=0.8))
    ax.add_patch(Rectangle((1.0, 2.0), 3.0, 1.0, fc='#b9d3f3', ec=BLUE, lw=0.9))
    ax.add_patch(Rectangle((6.0, 2.0), 3.0, 1.0, fc='#b9d3f3', ec=BLUE, lw=0.9))
    ax.text(2.5, 2.45, 'n$^+$ source', ha='center', fontsize=8.5, color='#174f94')
    ax.text(7.5, 2.45, 'n$^+$ drain', ha='center', fontsize=8.5, color='#174f94')
    ax.add_patch(Rectangle((3.4, 3.0), 3.2, 0.15, fc='#d0cfca', ec=MUTED, lw=0.6))
    ax.add_patch(Rectangle((3.4, 3.15), 3.2, 0.6, fc=RED, alpha=0.8, lw=0))
    ax.text(5.0, 3.42, 'gate', ha='center', fontsize=8.5, color='white')
    # lateral diffusion
    for x0 in [3.4, 6.0]:
        ax.add_patch(Rectangle((x0, 2.55), 0.6, 0.45, fill=False, hatch='////', ec=VIOLET, lw=0))
    ax.annotate('', xy=(3.4, 4.05), xytext=(4.0, 4.05), arrowprops=dict(arrowstyle='<->', color=VIOLET, lw=1))
    ax.text(3.7, 4.25, '$L_D$', ha='center', fontsize=9, color=VIOLET)
    ax.annotate('', xy=(6.0, 4.05), xytext=(6.6, 4.05), arrowprops=dict(arrowstyle='<->', color=VIOLET, lw=1))
    ax.text(6.3, 4.25, '$L_D$', ha='center', fontsize=9, color=VIOLET)
    ax.annotate('', xy=(4.0, 1.75), xytext=(6.0, 1.75), arrowprops=dict(arrowstyle='<->', color=INK, lw=1))
    ax.text(5.0, 1.35, '$L_{eff}=L_{drawn}-2L_D$', ha='center', fontsize=8.5)
    ax.text(10.2, 2.8, 'overlap:\n$C_{gd}=C_{gs}\\approx C_{ox}WL_D$\n($=WC_{ov}$ in Razavi)', fontsize=8.5, color=VIOLET, va='center')
    ax.set_xlim(-0.2, 14.8); ax.set_ylim(0.9, 4.7)
    save(fig, 'p_overlap')


def fig_capvgs():
    fig, ax = plt.subplots(figsize=(4.4, 2.6))
    vt, vd = 1.0, 2.0
    cox, cov = 1.0, 0.12
    vg = np.linspace(0, 5, 500)
    cgs = np.where(vg < vt, cov, np.where(vg < vd + vt, 2 / 3 * cox + cov, 0.5 * cox + cov))
    cgd = np.where(vg < vt, cov, np.where(vg < vd + vt, cov, 0.5 * cox + cov))
    ax.plot(vg, cgs, color=BLUE, label='$C_{GS}$')
    ax.plot(vg, cgd, color=ORANGE, label='$C_{GD}$')
    ax.set_yticks([cov, 0.5 + cov, 2 / 3 + cov]); ax.set_yticklabels(['$WC_{ov}$', '$\\frac{1}{2}WLC_{ox}+WC_{ov}$', '$\\frac{2}{3}WLC_{ox}+WC_{ov}$'], fontsize=8)
    ax.set_xticks([vt, vd + vt]); ax.set_xticklabels(['$V_{TH}$', '$V_D+V_{TH}$'])
    ax.text(0.2, 0.2, 'off', fontsize=8.5, color=MUTED); ax.text(1.7, 0.85, 'saturation', fontsize=8.5, color=MUTED); ax.text(3.6, 0.7, 'triode', fontsize=8.5, color=MUTED)
    ax.text(1.4, 0.72, '$C_{GS}$', color=BLUE, fontsize=9); ax.text(1.4, 0.2, '$C_{GD}$', color=ORANGE, fontsize=9)
    ax.set_xlabel('$V_{GS}$ (fixed $V_D$)'); ax.set_ylim(0, 1.0); ax.set_xlim(0, 5)
    ax.set_title('After Razavi Fig. 2.34', fontsize=8.5, loc='left', color=MUTED)
    save(fig, 'p_capvgs')


def fig_timing():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.8, 4.4), sharex=True, gridspec_kw=dict(hspace=0.18, height_ratios=[1, 1.4]))
    t = np.linspace(0, 12, 3000)
    tin1, tin2, tr = 1.0, 6.5, 0.25
    vin = np.clip((t - tin1 + tr / 2) / tr, 0, 1) * (t < tin2 - tr) + np.clip(1 - (t - tin2 + tr / 2) / tr, 0, 1) * (t >= tin2 - tr)
    a1.plot(t, vin, color=INK, lw=1.8)
    a1.axhline(0.5, color=GRID, ls='--', lw=0.9)
    a1.set_yticks([0, 0.5, 1]); a1.set_yticklabels(['$V_{OL}$', '$V_{50\\%}$', '$V_{OH}$'])
    a1.set_ylabel('$V_{in}$'); a1.set_ylim(-0.1, 1.15)
    tf_, tr_ = 0.9, 1.2
    d = 0.12
    vout = np.ones_like(t)
    m1 = (t >= tin1 + d) & (t < tin2 + d)
    vout[m1] = np.exp(-(t[m1] - tin1 - d) / tf_)
    m2 = t >= tin2 + d
    vend = np.exp(-(tin2 - tin1) / tf_)
    vout[m2] = 1 - (1 - vend) * np.exp(-(t[m2] - tin2 - d) / tr_)
    a2.plot(t, vout, color=BLUE, lw=2.2)
    for y in [0.1, 0.5, 0.9]:
        a2.axhline(y, color=GRID, ls='--', lw=0.9)
    a2.set_yticks([0, 0.1, 0.5, 0.9, 1]); a2.set_yticklabels(['$V_{OL}$', '10%', '$V_{50\\%}$', '90%', '$V_{OH}$'])
    a2.set_ylabel('$V_{out}$')
    t1, t3 = tin1, tin2
    t2 = tin1 + d + tf_ * np.log(2)
    t4 = tin2 + d + tr_ * np.log(2)
    t90f, t10f = tin1 + d + tf_ * np.log(1 / 0.9), tin1 + d + tf_ * np.log(10)
    t10r, t90r = tin2 + d + tr_ * np.log(1 / 0.9), tin2 + d + tr_ * np.log(10)
    for x in [t1, t2, t3, t4]:
        a1.axvline(x, color=MUTED, lw=0.6, ls=':'); a2.axvline(x, color=MUTED, lw=0.6, ls=':')
    a2.annotate('', xy=(t1, 0.5), xytext=(t2, 0.5), arrowprops=dict(arrowstyle='<->', color=VIOLET, lw=1.2))
    a2.text(t2 + 0.12, 0.56, '$\\tau_{PHL}=t_2-t_1$', color=VIOLET, fontsize=9.5)
    a2.annotate('', xy=(t3, 0.5), xytext=(t4, 0.5), arrowprops=dict(arrowstyle='<->', color=VIOLET, lw=1.2))
    a2.text(t4 + 0.12, 0.40, '$\\tau_{PLH}=t_4-t_3$', color=VIOLET, fontsize=9.5)
    a2.annotate('', xy=(t90f, 0.24), xytext=(t10f, 0.24), arrowprops=dict(arrowstyle='<->', color=ORANGE, lw=1.1))
    a2.text(t10f + 0.12, 0.2, '$t_{fall}$', color=ORANGE, fontsize=9.5)
    a2.annotate('', xy=(t10r, 0.76), xytext=(t90r, 0.76), arrowprops=dict(arrowstyle='<->', color=AQUA, lw=1.1))
    a2.text(t90r + 0.12, 0.72, '$t_{rise}$', color='#11734f', fontsize=9.5)
    a2.set_xticks([t1, t2, t3, t4]); a2.set_xticklabels(['$t_1$', '$t_2$', '$t_3$', '$t_4$'])
    a2.set_xlabel('time'); a2.set_xlim(0, 11.5); a2.set_ylim(-0.08, 1.1)
    save(fig, 'p_timing')


EX = dict(c=0.3e-12, kn=200e-6, kp=80e-6, vtn=0.6, vtp=-0.7, vdd=3.3)


def fig_discharge():
    c, kn, vtn, voh = EX['c'], EX['kn'], EX['vtn'], EX['vdd']
    tot, ts, tl = inv.tphl(c, kn, vtn, voh, 0)
    tavg, i1, i2, iav = inv.tphl_avg(c, kn, vtn, voh, 0)
    t, v = inv.simulate_fall(c, kn, vtn, voh, 3.0 * tot)
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    ax.plot(t * 1e9, v, color=BLUE, lw=2.2, label='exact $V_{out}(t)$')
    ax.axhline(voh - vtn, color=GRID, ls='--', lw=0.9)
    ax.axhline(voh / 2, color=GRID, ls='--', lw=0.9)
    ax.plot([0, tavg * 1e9], [voh, voh / 2], color=ORANGE, lw=1.5, ls='--')
    ax.text(tot * 1e9 * 1.25, 2.55, 'dashed: average-current method\n(straight line, slope $-I_{avg}/C_{load}$)', color=ORANGE, fontsize=8.3, ha='left')
    for x, lab in [(ts, "$t_1'$"), (tot, '$t_2$')]:
        ax.axvline(x * 1e9, color=MUTED, lw=0.7, ls=':')
    ax.axvspan(0, ts * 1e9, color=BLUE, alpha=0.07)
    ax.axvspan(ts * 1e9, tot * 1e9, color=AQUA, alpha=0.07)
    ax.text(ts * 1e9 / 2, 0.45, 'NMOS\nsat.', ha='center', fontsize=8, color=BLUE)
    ax.text((ts + tot) * 1e9 / 2, 0.45, 'NMOS linear', ha='center', fontsize=8, color='#11734f')
    ax.set_xticks([0, ts * 1e9, tot * 1e9, 2 * tot * 1e9, 3 * tot * 1e9])
    ax.set_xticklabels(['$t_1$=0', f"$t_1'$\n{ts*1e12:.0f} ps", f"$t_2$\n{tot*1e12:.0f} ps", f'{2*tot*1e12:.0f}', f'{3*tot*1e12:.0f} ps'], fontsize=8)
    ax.set_yticks([0, voh / 2, voh - vtn, voh]); ax.set_yticklabels(['0', '$V_{50\\%}$=1.65', '$V_{OH}-V_{T0,n}$=2.7', '$V_{OH}$=3.3'], fontsize=8)
    ax.set_xlim(0, 3 * tot * 1e9); ax.set_ylim(0, 3.45)
    ax.set_xlabel('time after the (ideal) input step'); ax.set_ylabel('$V_{out}$ (V)')
    save(fig, 'p_discharge')
    return tot, ts, tl, tavg


def fig_iavg():
    kn, vtn, voh = EX['kn'], EX['vtn'], EX['vdd']
    vo = np.linspace(0, voh, 400)
    i = np.array([inv.idn(voh, x, kn, vtn) for x in vo]) * 1e6
    tavg, i1, i2, iav = inv.tphl_avg(EX['c'], kn, vtn, voh, 0)
    fig, ax = plt.subplots(figsize=(5.0, 3.0))
    ax.plot(vo, i, color=BLUE, lw=2)
    m = vo >= voh / 2
    ax.fill_between(vo[m], 0, i[m], color=BLUE, alpha=0.08)
    ax.plot([voh, voh / 2], [i1 * 1e6, i2 * 1e6], 'o', color=INK, ms=5)
    ax.hlines(iav * 1e6, voh / 2, voh, color=ORANGE, lw=1.4, ls='--')
    ax.text(2.2, iav * 1e6 - 75, f'$I_{{avg}}$ = {iav*1e6:.0f} µA', color=ORANGE, fontsize=8.8, ha='center')
    ax.text(voh - 0.02, i1 * 1e6 + 40, f'{i1*1e6:.0f} µA', fontsize=8.5, ha='right')
    ax.text(voh / 2 - 0.08, i2 * 1e6 + 10, f'{i2*1e6:.0f} µA', fontsize=8.5, ha='right')
    ax.axvline(voh - vtn, color=GRID, ls='--', lw=0.9)
    ax.text(voh - vtn + 0.05, 80, 'sat.', fontsize=8, color=MUTED, ha='left'); ax.text(voh - vtn - 0.05, 80, 'lin.', fontsize=8, color=MUTED, ha='right')
    ax.set_xlabel('$V_{out}$ (V)   (time runs right → left)'); ax.set_ylabel('$i_{D,n}$ (µA)')
    ax.set_xlim(0, voh); ax.set_ylim(0, 900)
    save(fig, 'p_iavg')


def fig_sizing():
    """delay vs beta = (W/L)p/(W/L)n with self-loading; next stage identical."""
    kn1, kp1 = 200e-6, 80e-6   # per unit (W/L)=1 ... use kn' (W/L)n = 1 unit
    vdd, vtn, vtp = 3.3, 0.6, -0.7
    beta = np.linspace(0.5, 5, 300)
    cn_unit = 10e-15          # cap per unit width at the output and at next gate (drain + gate)
    cfix = 20e-15
    C = cfix + cn_unit * (1 + beta) * 2     # own drains + next-stage gates
    thl = np.array([inv.tphl(c, kn1, vtn, vdd, 0)[0] for c in C])
    tlh = np.array([inv.tplh(c, kp1 * b, vtp, vdd, 0)[0] for c, b in zip(C, beta)])
    avg = (thl + tlh) / 2
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.plot(beta, thl * 1e12, color=BLUE)
    ax.plot(beta, tlh * 1e12, color=ORANGE)
    ax.plot(beta, avg * 1e12, color=INK, lw=2.2)
    k = np.argmin(avg)
    ax.plot(beta[k], avg[k] * 1e12, 'o', color=INK)
    eq = np.argmin(abs(thl - tlh))
    ax.plot(beta[eq], thl[eq] * 1e12, 'o', color=VIOLET)
    ax.annotate(f'$\\tau_{{PHL}}=\\tau_{{PLH}}$ at β = {beta[eq]:.2f}', xy=(beta[eq], thl[eq] * 1e12), xytext=(3.3, 90),
                fontsize=8, color=VIOLET, arrowprops=dict(arrowstyle='-', color=VIOLET, lw=0.8))
    ax.text(4.6, thl[-1] * 1e12 + 5, '$\\tau_{PHL}$', color=BLUE, fontsize=9)
    ax.text(4.6, tlh[-1] * 1e12 - 18, '$\\tau_{PLH}$', color=ORANGE, fontsize=9)
    ax.text(0.62, avg[0] * 1e12 - 45, '$\\tau_P$ (average)', color=INK, fontsize=9)
    ax.set_xlabel('β = $(W/L)_p\\,/\\,(W/L)_n$'); ax.set_ylabel('delay (ps)')
    ax.set_ylim(0, max(tlh[0], thl[-1]) * 1e12 * 1.1)
    save(fig, 'p_sizing')
    return beta[k], beta[eq]


def fig_ring_wave():
    fig, ax = plt.subplots(figsize=(6.0, 1.9))
    t = np.linspace(0, 14, 2000)
    TD = 1.0
    def sq(t, d):
        ph = ((t - d) % 6) / 6
        return np.where(ph < 0.5, 1.0, 0.0)
    for k, (d, nm, c) in enumerate([(0, 'X', BLUE), (1, 'Y', ORANGE), (2, 'Z', AQUA)]):
        y = sq(t, d * 3 + (0 if k == 0 else 0))
    # simple: X high 0..3, Y low for 1..4, ... draw with explicit edges
    for k, (nm, c) in enumerate([('X', BLUE), ('Y', ORANGE), ('Z', AQUA)]):
        start = k * TD
        level = 1 if k % 2 == 0 else 0
        sig = np.zeros_like(t)
        # node k toggles at times k*TD + m*3TD
        for i, tt in enumerate(t):
            n = np.floor((tt - start) / (3 * TD)) if tt >= start else -1
            v0 = level
            sig[i] = v0 if n < 0 else (1 - v0 if n % 2 == 0 else v0)
        ax.plot(t, sig + (2 - k) * 1.5, color=c, lw=1.8)
        ax.text(-0.4, (2 - k) * 1.5 + 0.5, nm, color=c, fontsize=10, ha='right', va='center')
    ax.annotate('', xy=(0, -0.4), xytext=(6, -0.4), arrowprops=dict(arrowstyle='<->', color=INK, lw=1))
    ax.text(3, -0.85, 'period $T = 6\\tau_P$ (3 stages) — in general $T=2N\\tau_P$', ha='center', fontsize=8.5)
    ax.annotate('', xy=(0, 2.4), xytext=(1, 2.4), arrowprops=dict(arrowstyle='<->', color=VIOLET, lw=1))
    ax.text(0.5, 2.15, '$\\tau_P$', color=VIOLET, ha='center', fontsize=9)
    ax.axis('off'); ax.set_xlim(-0.8, 14); ax.set_ylim(-1.1, 4.2)
    save(fig, 'p_ring_wave')


def fig_razavi211_sol():
    """Razavi 2.11 (a) source follower charging, (b) triode discharge; VTH=0.7, gamma=0, un Cox=134.3u."""
    kp_ = 134.3e-6 * 50 / 0.5 * 0 + 1   # placeholder: plot normalised time
    fig, axs = plt.subplots(1, 2, figsize=(6.6, 2.4))
    # (a): dVx/dt = (k/2C)(3 - 0.7 - Vx)^2 -> Vx -> 2.3 V, t normalised by C/k
    tau = np.linspace(0, 10, 400)
    a = 2.3
    v0 = 1.0
    # solution: 1/(a - v) = 1/(a - v0) + tau/2
    va = a - 1 / (1 / (a - v0) + tau / 2)
    ax = axs[0]
    ax.plot(tau, va, color=BLUE)
    ax.axhline(2.3, color=GRID, ls='--', lw=0.9)
    ax.text(5, 2.38, '$V_{in}-V_{TH}=2.3$ V (never quite reached)', fontsize=7.8, ha='center')
    ax.set_ylim(0.8, 2.6); ax.set_xlabel('$t$ / $(C_1/k_n)$'); ax.set_ylabel('$V_X$ (V)')
    ax.set_title('(a) charges toward $V_{in}-V_{TH}$, saturated', fontsize=8.5, loc='left', color=MUTED)
    # (b): triode: C dV/dt = -(k/2)(2*2.3*V - V^2) -> V = 2a V0 e^{-a' t}/(...) ; solve numerically
    ax = axs[1]
    t = np.linspace(0, 3, 600)
    v = np.empty_like(t); v[0] = 1.0
    dt = t[1] - t[0]
    for i in range(1, len(t)):
        x = v[i - 1]
        f = lambda y: -0.5 * (2 * 2.3 * y - y * y)
        k1 = f(x); k2 = f(x + dt / 2 * k1); k3 = f(x + dt / 2 * k2); k4 = f(x + dt * k3)
        v[i] = x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    ax.plot(t, v, color=BLUE)
    ax.set_ylim(0, 1.1); ax.set_xlabel('$t$ / $(C_1/k_n)$'); ax.set_ylabel('$V_X$ (V)')
    ax.set_title('(b) discharges to 0, triode throughout', fontsize=8.5, loc='left', color=MUTED)
    fig.tight_layout(w_pad=2)
    save(fig, 'p_razavi211')


# ---------------------------------------------------------------- page header strip
def fig_header():
    fig, ax = plt.subplots(figsize=(7.8, 1.05))
    ax.set_xlim(0, 31.2); ax.set_ylim(-2.1, 2.1); ax.axis('off'); ax.set_aspect('equal')
    m = mos(ax, 1.0, 0.1, 'n', BLUE, None, lead=0.5)
    ax.text(m['top'][0] + 0.14, m['top'][1], 'D', fontsize=8, color=BLUE, va='center')
    ax.text(m['bot'][0] + 0.14, m['bot'][1], 'S', fontsize=8, color=BLUE, va='center')
    ax.text(m['g'][0] - 0.1, 0.1, 'G', fontsize=8, color=BLUE, ha='right', va='center')
    arrow(ax, (m['top'][0] + 0.6, 1.0), (m['top'][0] + 0.6, -0.2), BLUE, lw=1.1, ms=8)
    ax.text(m['top'][0] + 0.75, 0.4, '$I_D$', fontsize=8.5, color=BLUE)
    ax.text(1.0, -1.6, 'NMOS', fontsize=8, color=BLUE, ha='center', weight='bold')
    p = mos(ax, 4.6, 0.1, 'p', ORANGE, None, lead=0.5)
    ax.text(p['top'][0] + 0.14, p['top'][1], 'S', fontsize=8, color=ORANGE, va='center')
    ax.text(p['bot'][0] + 0.14, p['bot'][1], 'D', fontsize=8, color=ORANGE, va='center')
    ax.text(p['g'][0] - 0.1, 0.1, 'G', fontsize=8, color=ORANGE, ha='right', va='center')
    arrow(ax, (p['top'][0] + 0.6, 1.0), (p['top'][0] + 0.6, -0.2), ORANGE, lw=1.1, ms=8)
    ax.text(p['top'][0] + 0.75, 0.4, '$I_D$', fontsize=8.5, color=ORANGE)
    ax.text(4.6, -1.6, 'PMOS', fontsize=8, color=ORANGE, ha='center', weight='bold')
    fs = 8.6
    x0 = 7.4
    ax.plot([x0 - 0.4, x0 - 0.4], [-1.9, 1.9], color='#d6d4ce', lw=0.8)
    ax.text(x0, 1.35, '$\\mathbf{lin:}\\ V_{DS}<V_{GS}-V_{T0,n}$   $I_D=\\frac{k_n}{2}[2(V_{GS}-V_{T0,n})V_{DS}-V_{DS}^2]$', fontsize=fs, color=BLUE, va='center')
    ax.text(x0 + 15.0, 1.35, '$\\mathbf{sat:}\\ V_{DS}\\geq V_{GS}-V_{T0,n}$   $I_D=\\frac{k_n}{2}(V_{GS}-V_{T0,n})^2$', fontsize=fs, color=BLUE, va='center')
    ax.text(x0, 0.0, '$\\mathbf{lin:}\\ V_{DS}>V_{GS}-V_{T0,p}$   $I_D=\\frac{k_p}{2}[2(V_{GS}-V_{T0,p})V_{DS}-V_{DS}^2]$', fontsize=fs, color=ORANGE, va='center')
    ax.text(x0 + 15.0, 0.0, '$\\mathbf{sat:}\\ V_{DS}\\leq V_{GS}-V_{T0,p}$   $I_D=\\frac{k_p}{2}(V_{GS}-V_{T0,p})^2$', fontsize=fs, color=ORANGE, va='center')
    ax.text(x0, -1.35, '$k=\\mu C_{ox}\\frac{W}{L}$,  $k_R=\\frac{k_n}{k_p}$,  $V_{T0,p}<0$     inverter: $V_{GS,n}=V_{in}$, $V_{DS,n}=V_{out}$, $V_{GS,p}=V_{in}-V_{DD}$, $V_{DS,p}=V_{out}-V_{DD}$', fontsize=fs, color='#3d3c39', va='center')
    fig.savefig(os.path.join(OUT, 'hdr.svg'), bbox_inches='tight', pad_inches=0.01, transparent=True)
    fig.savefig(os.path.join(OUT, 'hdr.png'), bbox_inches='tight', pad_inches=0.01, dpi=150, facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    fig_idvds(); fig_vtc_generic(); fig_nm_bars()
    fig_regionmap(); fig_vtc_current()
    fig_kr_family(); fig_sym(); fig_layout()
    fig_overlap(); fig_capvgs(); fig_timing()
    print('discharge', fig_discharge()); fig_iavg(); print('sizing', fig_sizing()); fig_razavi211_sol()
    fig_header()
