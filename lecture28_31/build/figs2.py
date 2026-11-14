"""Figures for the Lectures 28-31 guide (logic gates, layout, RC delay, logical effort).

Reuses the drawing helpers of the Lecture 25 guide. Run: python3 figs2.py
"""
import os, sys, re
from math import exp, log, sqrt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "lecture25", "build"))
import figs as F  # noqa: E402
from figs import (svg, line, poly, text, dot, arrow, defs, nmos, pmos, gnd, vdd, cap, inverter, Plot, sub,
                  vtc, BLUE, ORANGE, GREEN, PURPLE, RED, AMBER, INK, MUTE, ALLC)  # noqa: E402

GREY = "#c3c8d2"


# ---------- small building blocks ----------
def res(x, y, c=INK, label=None, h=40):
    """Vertical resistor from (x,y) down to (x,y+h)."""
    z = [(x, y), (x, y + 8)]
    for i in range(6):
        z.append((x + (7 if i % 2 == 0 else -7), y + 8 + (i + 0.5) * (h - 16) / 6))
    z += [(x, y + h - 8), (x, y + h)]
    s = poly(z, c, 2)
    if label:
        s += text(x + 12, y + h / 2 + 4, label, c, 12.5, "start", 600)
    return s


def nfet(x, y, g, c=INK, w=None):
    """NMOS with drain top (x+18,y-35), source bottom (x+18,y+35); gate label g at left."""
    s = nmos(x, y, c) + text(x - 34, y + 5, g, c, 13, "end", 700)
    if w is not None:
        s += text(x + 24, y + 5, str(w), MUTE, 12, "start", 700)
    return s


def pfet(x, y, g, c=INK, w=None):
    s = pmos(x, y, c) + text(x - 34, y + 5, g, c, 13, "end", 700)
    if w is not None:
        s += text(x + 24, y + 5, str(w), MUTE, 12, "start", 700)
    return s


def gate_shape(kind, x, y, label=None, c=INK, size=1.0):
    """Logic symbol with input side at x, centre height y. Returns (svg, out_x)."""
    s = ""
    w, h = 50 * size, 40 * size
    if kind == "inv":
        s += poly([(x, y - h / 2), (x, y + h / 2), (x + w * 0.8, y), (x, y - h / 2)], c, 2)
        bx = x + w * 0.8 + 5
    elif kind == "nand":
        s += f'<path d="M{x},{y-h/2} L{x+w*0.5},{y-h/2} A{h/2},{h/2} 0 0 1 {x+w*0.5},{y+h/2} L{x},{y+h/2} Z" fill="none" stroke="{c}" stroke-width="2"/>'
        bx = x + w * 0.5 + h / 2 + 5
    elif kind == "nor":
        s += (f'<path d="M{x},{y-h/2} Q{x+w*0.55},{y-h/2} {x+w*0.95},{y} Q{x+w*0.55},{y+h/2} {x},{y+h/2} '
              f'Q{x+w*0.25},{y} {x},{y-h/2} Z" fill="none" stroke="{c}" stroke-width="2"/>')
        bx = x + w * 0.95 + 5
    s += f'<circle cx="{bx}" cy="{y}" r="5" fill="white" stroke="{c}" stroke-width="2"/>'
    if label:
        s += text(x + (w * 0.32 if kind != "nor" else w * 0.4), y + 5, sub(label), c, 13, "middle", 700)
    return s, bx + 5


# ---------- Lecture 28 ----------
def fig_switches():
    s = defs(*ALLC)
    for i, (title, fn, on, off, c) in enumerate([("NMOS = switch that closes on a 1", nmos, "gate = 1 → ON (closed)", "gate = 0 → OFF (open)", BLUE),
                                                 ("PMOS = switch that closes on a 0", pmos, "gate = 0 → ON (closed)", "gate = 1 → OFF (open)", ORANGE)]):
        ox = 40 + i * 330
        s += text(ox + 140, 22, title, c, 13, "middle", 700)
        s += fn(ox + 60, 90, c)
        s += line(ox + 78, 55, ox + 78, 40, c) + line(ox + 78, 125, ox + 78, 140, c)
        # switch pictures
        for j, (lab, closed) in enumerate(((on, True), (off, False))):
            yy = 60 + j * 55
            sx = ox + 150
            s += line(sx, yy, sx + 25, yy, c) + dot(sx + 25, yy, c, 3)
            s += (line(sx + 25, yy, sx + 60, yy, c, 2.5) if closed else line(sx + 25, yy, sx + 55, yy - 16, c, 2.5))
            s += dot(sx + 60, yy, c, 3) + line(sx + 60, yy, sx + 80, yy, c)
            s += text(sx + 40, yy + 22, lab, INK, 11.5, "middle")
    s += text(330, 178, "So NMOS are good at connecting the output to GROUND, PMOS at connecting it to V_DD.".replace("V_DD", sub("V_DD")), INK, 12.5, "middle")
    return svg(660, 190, s)


def fig_pun_pdn():
    s = defs(*ALLC)
    x = 260
    s += vdd(x, 30)
    s += line(x, 30, x, 50)
    s += f'<rect x="{x-60}" y="50" width="120" height="70" rx="10" fill="{ORANGE}" opacity="0.14" stroke="{ORANGE}" stroke-width="2"/>'
    s += text(x, 80, "pull-up network", ORANGE, 13, "middle", 700) + text(x, 100, "(PMOS only)", ORANGE, 12, "middle")
    s += line(x, 120, x, 160) + dot(x, 140) + line(x, 140, x + 120, 140) + dot(x + 120, 140) + text(x + 128, 145, "Y", INK, 14, "start", 700)
    s += f'<rect x="{x-60}" y="160" width="120" height="70" rx="10" fill="{BLUE}" opacity="0.14" stroke="{BLUE}" stroke-width="2"/>'
    s += text(x, 190, "pull-down network", BLUE, 13, "middle", 700) + text(x, 210, "(NMOS only)", BLUE, 12, "middle")
    s += line(x, 230, x, 245) + gnd(x, 245)
    for i, lab in enumerate(("A₁", "A₂", "⋮", "A_N")):
        yy = 70 + i * 40
        s += text(70, yy + 5, sub(lab) if "_" in lab else lab, INK, 13, "end", 700)
        if lab != "⋮":
            s += line(76, yy, 120, yy, MUTE, 1.5)
    s += line(120, 70, 120, 190, MUTE, 1.5) + line(120, 85, x - 60, 85, MUTE, 1.5) + line(120, 195, x - 60, 195, MUTE, 1.5)
    s += text(470, 70, "Rule: for every input pattern", INK, 12.5, "start", 700)
    s += text(470, 90, "exactly ONE network is on.", INK, 12.5, "start")
    s += text(470, 120, "PDN on → Y = 0", BLUE, 12.5, "start", 700)
    s += text(470, 140, "PUN on → Y = 1", ORANGE, 12.5, "start", 700)
    s += text(470, 170, "Never both: no DC current", INK, 12.5, "start")
    s += text(470, 190, "(that is why CMOS has", INK, 12.5, "start")
    s += text(470, 210, "almost zero static power)", INK, 12.5, "start")
    return svg(680, 275, s)


def fig_pseudo():
    s = defs(*ALLC)
    x = 150
    s += pmos(x, 70, ORANGE) + vdd(x + 18, 35)
    s += line(x - 30, 70, x - 50, 70, ORANGE) + gnd(x - 50, 70, ORANGE)
    s += text(x - 56, 60, "gate grounded", ORANGE, 11.5, "end")
    s += line(x + 18, 105, x + 18, 135) + dot(x + 18, 120) + line(x + 18, 120, x + 90, 120) + text(x + 96, 125, sub("V_out"), INK, 13, "start", 700)
    s += nmos(x, 170, BLUE) + line(x - 30, 170, x - 60, 170) + text(x - 64, 175, sub("V_in"), INK, 13, "end", 700) + gnd(x + 18, 205)
    s += text(420, 60, "Pseudo-NMOS (lecture's first sketch)", INK, 13, "middle", 700)
    s += text(420, 90, "• PMOS is ALWAYS on (a load resistor)", INK, 12.5, "middle")
    s += text(420, 112, "• only the NMOS network does the logic", INK, 12.5, "middle")
    s += text(420, 134, "• output low = a tug-of-war → V_OL > 0".replace("V_OL", sub("V_OL")), RED, 12.5, "middle")
    s += text(420, 156, "• current flows whenever output is low", RED, 12.5, "middle")
    s += text(420, 178, "→ CMOS fixes both by switching the PMOS too", GREEN, 12.5, "middle", 700)
    return svg(620, 232, s)


def nor2_schem(ox=150, labels=True, wn=None, wp=None, cA=INK, cB=INK):
    s = ""
    # PMOS series: A top, B below
    s += pfet(ox, 70, "A", cA, wp) + pfet(ox, 140, "B", cB, wp)
    s += vdd(ox + 18, 35)
    # output node at y=175 ; two NMOS in parallel below
    s += line(ox + 18, 175, ox + 18, 190) + line(ox - 40, 190, ox + 110, 190)
    s += nfet(ox - 40 + 0, 225, "A", cA, wn)
    s += nfet(ox + 92, 225, "B", cB, wn)
    s += line(ox - 22, 190, ox - 22, 190)
    s += line(ox - 40 + 18, 190, ox - 40 + 18, 190)
    s += line(ox - 22, 260, ox + 110, 260) + gnd(ox + 44, 260)
    s += dot(ox + 18, 190) + line(ox + 110, 190, ox + 170, 190) + dot(ox + 170, 190) + text(ox + 178, 195, "Y", INK, 14, "start", 700)
    return s


def fig_nor2():
    s = defs(*ALLC)
    ox = 150
    # explicit drawing for clarity
    s += pfet(ox, 70, "A", ORANGE) + pfet(ox, 140, "B", ORANGE) + vdd(ox + 18, 35)
    s += line(ox + 18, 175, ox + 18, 195)
    s += line(ox - 22, 195, ox + 128, 195)
    s += nfet(ox - 40, 230, "A", BLUE) + nfet(ox + 110, 230, "B", BLUE)
    s += line(ox - 22, 265, ox + 128, 265) + gnd(ox + 53, 265)
    s += dot(ox + 18, 195) + line(ox + 128, 195, ox + 180, 195) + dot(ox + 180, 195) + text(ox + 188, 200, "Y", INK, 14, "start", 700)
    s += text(520, 18, "NOR2: Y = (A + B)'", INK, 14, "middle", 700)
    s += text(ox + 62, 120, "PMOS in SERIES", ORANGE, 12, "start", 600)
    s += text(ox + 53, 300, "NMOS in PARALLEL", BLUE, 12, "middle", 600)
    # truth table
    tx = 450
    s += text(tx + 70, 48, "A  B  |  Y", INK, 13, "middle", 700)
    for i, (a, b, yv) in enumerate(((0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 0))):
        s += text(tx + 70, 66 + i * 24, f"{a}  {b}  |  {yv}", GREEN if yv else INK, 13, "middle", 600)
    s += text(tx + 70, 180, "Y = 1 only when both", INK, 12, "middle")
    s += text(tx + 70, 198, "inputs are 0 (both PMOS on)", INK, 12, "middle")
    s += text(tx + 70, 230, "Any input = 1 → its NMOS", INK, 12, "middle")
    s += text(tx + 70, 248, "pulls Y to ground", INK, 12, "middle")
    return svg(620, 320, s)


def fig_nand2():
    s = defs(*ALLC)
    ox = 170
    s += line(ox - 22, 35, ox + 128, 35) + vdd(ox + 53, 35)
    s += pfet(ox - 40, 70, "A", ORANGE) + pfet(ox + 110, 70, "B", ORANGE)
    s += line(ox - 22, 105, ox + 128, 105) + dot(ox + 53, 105) + line(ox + 53, 105, ox + 53, 125)
    s += line(ox + 128, 105, ox + 190, 105) + dot(ox + 190, 105) + text(ox + 198, 110, "Y", INK, 14, "start", 700)
    s += nfet(ox + 35, 160, "B", BLUE) + nfet(ox + 35, 230, "A", BLUE) + gnd(ox + 53, 265)
    s += text(530, 18, "NAND2: Y = (A·B)'", INK, 14, "middle", 700)
    s += text(ox + 128, 70, "PMOS in PARALLEL", ORANGE, 12, "start", 600)
    s += text(ox + 80, 200, "NMOS in SERIES", BLUE, 12, "start", 600)
    tx = 470
    s += text(tx + 60, 48, "A  B  |  Y", INK, 13, "middle", 700)
    for i, (a, b, yv) in enumerate(((0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0))):
        s += text(tx + 60, 66 + i * 24, f"{a}  {b}  |  {yv}", RED if not yv else INK, 13, "middle", 600)
    s += text(tx + 60, 180, "Y = 0 only when both", INK, 12, "middle")
    s += text(tx + 60, 198, "inputs are 1 (both NMOS on)", INK, 12, "middle")
    return svg(620, 300, s)


def fig_wl():
    s = defs(*ALLC)
    # pipes picture
    s += text(160, 22, "Parallel: pipes side by side", GREEN, 13, "middle", 700)
    for i in range(2):
        s += f'<rect x="{70+i*90}" y="40" width="60" height="80" rx="6" fill="{BLUE}" opacity="0.25" stroke="{BLUE}"/>'
        s += text(100 + i * 90, 85, f"W/L = 2", BLUE, 12, "middle", 600)
    s += text(160, 150, "total = 2 + 2 = 4  (wider → easier flow)", INK, 12.5, "middle", 700)
    s += text(480, 22, "Series: pipes one after another", ORANGE, 13, "middle", 700)
    for i in range(2):
        s += f'<rect x="{390+i*95}" y="60" width="85" height="40" rx="6" fill="{ORANGE}" opacity="0.25" stroke="{ORANGE}"/>'
        s += text(432 + i * 95, 85, "W/L = 2", ORANGE, 12, "middle", 600)
    s += text(480, 150, "total = 1/(1/2 + 1/2) = 1  (longer → harder)", INK, 12.5, "middle", 700)
    s += text(320, 186, "W/L behaves like a CONDUCTANCE (1/resistance): parallel adds, series combines like resistors in parallel.", MUTE, 12, "middle")
    return svg(660, 198, s)


def fig_nor2_collapse():
    s = defs(*ALLC)
    s += text(240, 300 - 270, "NOR2 with A = B = V_in".replace("V_in", sub("V_in")), INK, 13, "start", 700)
    ox = 110
    s += pfet(ox, 70, "", ORANGE, None) + pfet(ox, 140, "", ORANGE, None) + vdd(ox + 18, 35)
    s += text(ox + 30, 75, "(W/L)_p".replace("(W/L)_p", "(W/L)" + "<tspan font-size='9' dy='3'>p</tspan><tspan dy='-3'></tspan>"), ORANGE, 12, "start")
    s += text(ox + 30, 145, "(W/L)" + "<tspan font-size='9' dy='3'>p</tspan><tspan dy='-3'></tspan>", ORANGE, 12, "start")
    s += line(ox + 18, 175, ox + 18, 195) + line(ox - 22, 195, ox + 118, 195)
    s += nmos(ox - 40, 230, BLUE) + nmos(ox + 100, 230, BLUE)
    s += line(ox - 22, 265, ox + 118, 265) + gnd(ox + 48, 265)
    s += arrow(330, 160, 400, 160, PURPLE, 2.5) + text(365, 150, "same as", PURPLE, 12, "middle", 700)
    s += text(240, 250, "all four gates", INK, 12, "start", 600) + text(240, 266, "= V_in".replace("V_in", sub("V_in")), INK, 12, "start", 600)
    s += inverter(480, 160, ORANGE, BLUE)
    s += text(510, 115, "½ (W/L)" + "<tspan font-size='9' dy='3'>p</tspan><tspan dy='-3'></tspan>", ORANGE, 13, "start", 700)
    s += text(510, 215, "2 (W/L)" + "<tspan font-size='9' dy='3'>n</tspan><tspan dy='-3'></tspan>", BLUE, 13, "start", 700)
    s += text(480, 22, "equivalent inverter", INK, 13, "middle", 700)
    s += text(330, 312, "So the NOR2 acts like an inverter with k_R,eff = (2k_n)/(½k_p) = 4k_R".replace("k_R,eff", sub("k_{R,eff}")).replace("k_n", sub("k_n")).replace("k_p", sub("k_p")).replace("k_R", sub("k_R")), PURPLE, 13, "middle", 700)
    return svg(660, 324, s)


def fig_vth_compare():
    VDD = 3.3
    kn, kp = 60 * 2, 25 * 2
    inv = vtc(VDD, 0.6, -0.7, kn, kp)
    nor = vtc(VDD, 0.6, -0.7, 2 * kn, kp / 2)
    nand = vtc(VDD, 0.6, -0.7, kn / 2, 2 * kp)
    p = Plot(600, 330, (0, 3.3), (0, 3.5), (60, 20, 20, 44))
    p.curve([(0, 0), (3.3, 3.3)], GREY, 1.4, "5 4")
    p.curve(nor, BLUE, 2.6); p.curve(inv, INK, 2.2, "6 4"); p.curve(nand, ORANGE, 2.6)
    for v, c, lab, dx in ((1.088, BLUE, "NOR2 1.09 V", -10), (1.385, INK, "INV 1.38 V", 10), (1.727, ORANGE, "NAND2 1.73 V", 10)):
        p.add(dot(p.X(v), p.Y(v), c, 5) + text(p.X(v) + dx, p.Y(v) + (4 if dx > 0 else 4), lab, c, 12.5, "start" if dx > 0 else "end", 700))
    p.axes(sub("V_in") + " (both inputs together) (V)", sub("V_out") + " (V)", [(0, "0"), (1, "1"), (2, "2"), (3.3, "3.3")], [(0, "0"), (1, "1"), (2, "2"), (3.3, "3.3")])
    return p.render()


def stick(cols, top, bot, title, out_cols_top, out_cols_bot, vdd_cols, gnd_cols, w=660, links=()):
    """Generic stick diagram. cols: gate names in order. top/bot: diffusion node names between/around gates (len = len(cols)+1)."""
    s = defs(*ALLC)
    n = len(cols)
    x0, dx = 90, (w - 180) / n
    yp, yn = 90, 200
    s += text(w / 2, 20, title, INK, 13, "middle", 700)
    # rails
    s += line(40, 45, w - 40, 45, BLUE, 5) + text(30, 50, sub("V_DD"), BLUE, 12, "end", 700)
    s += line(40, 255, w - 40, 255, BLUE, 5) + text(30, 260, "GND", BLUE, 12, "end", 700)
    # diffusion rows
    s += f'<rect x="{x0-30}" y="{yp-16}" width="{n*dx+60}" height="32" fill="{AMBER}" opacity="0.25" stroke="{AMBER}"/>'
    s += f'<rect x="{x0-30}" y="{yn-16}" width="{n*dx+60}" height="32" fill="{GREEN}" opacity="0.22" stroke="{GREEN}"/>'
    # poly gates
    for i, g in enumerate(cols):
        gx = x0 + (i + 0.5) * dx
        s += line(gx, yp - 30, gx, yn + 30, RED, 5)
        s += text(gx, yn + 50 + 0, g, RED, 14, "middle", 700)
    # node labels & contacts
    for i in range(n + 1):
        nx = x0 - 10 + i * dx if i == 0 else (x0 + i * dx if i < n else x0 + n * dx + 10)
        for row, names, yy in (("p", top, yp), ("n", bot, yn)):
            nm = names[i]
            s += text(nx, yy + 4, sub({"VDD": "V_DD"}.get(nm, nm)), INK, 11, "middle", 700)
            if nm in ("VDD", "GND", "Y"):
                pass
    # vertical connections for VDD/GND contacts
    for i in vdd_cols:
        nx = x0 - 10 + i * dx if i == 0 else (x0 + i * dx if i < n else x0 + n * dx + 10)
        s += line(nx, 45, nx, yp - 16, BLUE, 3) + f'<rect x="{nx-5}" y="{yp-26}" width="10" height="10" fill="{INK}"/>'
    for i in gnd_cols:
        nx = x0 - 10 + i * dx if i == 0 else (x0 + i * dx if i < n else x0 + n * dx + 10)
        s += line(nx, yn + 16, nx, 255, BLUE, 3) + f'<rect x="{nx-5}" y="{yn+16}" width="10" height="10" fill="{INK}"/>'
    # output wiring
    ys = 145
    xs = []
    for i in out_cols_top:
        nx = x0 - 10 + i * dx if i == 0 else (x0 + i * dx if i < n else x0 + n * dx + 10)
        s += line(nx, yp + 16, nx, ys, BLUE, 3); xs.append(nx)
    for i in out_cols_bot:
        nx = x0 - 10 + i * dx if i == 0 else (x0 + i * dx if i < n else x0 + n * dx + 10)
        s += line(nx, yn - 16, nx, ys, BLUE, 3); xs.append(nx)
    if xs:
        s += line(min(xs), ys, w - 50, ys, BLUE, 3) + text(w - 44, ys + 5, "Y", BLUE, 14, "start", 700)
    for row, cols_ in links:
        yy = (yp - 30) if row == "p" else (yn + 30)
        xs_ = [x0 - 10 + i * dx if i == 0 else (x0 + i * dx if i < n else x0 + n * dx + 10) for i in cols_]
        for nx in xs_:
            s += line(nx, yy, nx, (yp - 16) if row == "p" else (yn + 16), PURPLE, 3)
        s += line(min(xs_), yy, max(xs_), yy, PURPLE, 3)
    s += text(w / 2, 286, "top row = PMOS (p-diffusion, amber)    bottom row = NMOS (n-diffusion, green)", MUTE, 11.5, "middle")
    s += text(w / 2, 303, "red = poly gate    blue = metal    purple = second metal (may cross blue)    ■ = contact", MUTE, 11.5, "middle")
    return svg(w, 312, s)


def fig_stick_nor2():
    # PMOS: VDD -A- x -B- Y ; NMOS: Y -A- GND -B- Y  (order A, B)
    return stick(["A", "B"], ["VDD", "p1", "Y"], ["Y", "GND", "Y"], "NOR2 stick diagram (gate order A, B)", [2], [0, 2], [0], [1])


def fig_stick_nand2():
    # PMOS: Y -A- VDD -B- Y ; NMOS: GND -A- n1 -B- Y
    return stick(["A", "B"], ["Y", "VDD", "Y"], ["GND", "n1", "Y"], "NAND2 stick diagram (gate order A, B)", [0, 2], [2], [1], [0])


# ---------- Lecture 29 ----------
def fig_complex():
    s = defs(*ALLC)
    # PUN: (A || (D-E)) series (B || C)
    s += line(110, 35, 330, 35) + vdd(220, 35)
    s += pfet(110, 75, "A", ORANGE)          # A from 40..110 (drain bottom at y 110)
    s += pfet(270, 60, "D", ORANGE) + pfet(270, 130, "E", ORANGE)
    s += line(128, 40, 128, 35) + line(288, 25, 288, 35)
    s += line(128, 110, 128, 175) + line(288, 165, 288, 175) + line(128, 175, 288, 175)
    s += text(150, 125, "p1", MUTE, 11)
    s += pfet(110, 215, "B", ORANGE) + pfet(270, 215, "C", ORANGE)
    s += line(128, 175, 128, 180) + line(288, 175, 288, 180)
    s += line(128, 250, 128, 265) + line(288, 250, 288, 265) + line(128, 265, 288, 265)
    s += dot(208, 265) + line(288, 265, 400, 265) + dot(400, 265) + text(408, 270, "Y", INK, 15, "start", 700)
    # PDN: (A series (D||E)) || (B series C)
    s += line(208, 265, 208, 285) + line(128, 285, 330, 285)
    s += nfet(110, 320, "A", BLUE)
    s += line(128, 355, 128, 365) + line(80, 365, 160, 365)
    s += nfet(62, 400, "D", BLUE) + nfet(142, 400, "E", BLUE)
    s += line(80, 435, 160, 435) + gnd(120, 435)
    s += line(312, 285, 312, 285) + nfet(294, 320, "B", BLUE) + nfet(294, 390, "C", BLUE) + gnd(312, 425)
    s += line(312, 285, 312, 285)
    s += text(470, 60, "Y = [A(D+E) + BC]'", INK, 14, "start", 700)
    s += text(470, 100, "Pull-down (blue) = expression", BLUE, 12.5, "start", 700)
    s += text(470, 120, "without the bar:", BLUE, 12.5, "start")
    s += text(470, 140, "AND → series, OR → parallel", BLUE, 12.5, "start")
    s += text(470, 180, "Pull-up (orange) = the DUAL:", ORANGE, 12.5, "start", 700)
    s += text(470, 200, "every series ↔ parallel swapped", ORANGE, 12.5, "start")
    s += text(470, 240, "Check one case: A=1, D=1 →", INK, 12.5, "start")
    s += text(470, 260, "A–D path conducts → Y = 0 ✓", INK, 12.5, "start")
    return svg(680, 470, s)


def fig_euler():
    s = defs(*ALLC)

    offs = {"n1": (-20, 4), "n2": (22, 4), "p1": (-20, 4), "p2": (22, 4), "GND": (0, 22), "Y": (0, -12), "VDD": (0, -12)}

    def node(x, y, lab, c=INK):
        dx_, dy_ = offs.get(lab, (0, 22))
        return f'<circle cx="{x}" cy="{y}" r="6" fill="white" stroke="{c}" stroke-width="2.2"/>' + text(x + dx_, y + dy_, sub({"VDD": "V_DD"}.get(lab, lab)), INK, 12, "middle", 700)

    def _old_node(x, y, lab, c=INK):
        return f'<circle cx="{x}" cy="{y}" r="6" fill="white" stroke="{c}" stroke-width="2.2"/>' + text(x, y + (-12 if lab in ("Y", "VDD") else 22), sub(lab), INK, 12, "middle", 700)

    def edge(p1, p2, lab, c, bend=0, num=None):
        (x1, y1), (x2, y2) = p1, p2
        qx, qy = (x1 + x2) / 2 + bend, (y1 + y2) / 2
        cx, cy = (x1 + x2) / 2 + bend / 2, (y1 + y2) / 2
        sg = 1 if (bend > 0 or (bend == 0 and x2 >= x1)) else -1
        e = f'<path d="M{x1},{y1} Q{qx},{qy} {x2},{y2}" fill="none" stroke="{c}" stroke-width="2.4"/>'
        e += text(cx + sg * 13, cy + 5, lab, c, 14, "middle", 700)
        if num:
            e += f'<circle cx="{cx + sg*30}" cy="{cy}" r="9" fill="{PURPLE}"/>' + text(cx + sg * 30, cy + 4, str(num), "white", 11, "middle", 700)
        return e
    # PDN graph
    s += text(160, 22, "Pull-down graph (NMOS)", BLUE, 13, "middle", 700)
    Y, n1, n2, G = (160, 50), (90, 150), (230, 150), (160, 270)
    s += edge(Y, n1, "A", BLUE, -10, 3) + edge(n1, G, "D", BLUE, -40, 2) + edge(n1, G, "E", BLUE, 30, 1) + edge(Y, n2, "B", BLUE, 10, 4) + edge(n2, G, "C", BLUE, 20, 5)
    for p_, l in ((Y, "Y"), (n1, "n1"), (n2, "n2"), (G, "GND")):
        s += node(*p_, l)
    s += text(480, 22, "Pull-up graph (PMOS)", ORANGE, 13, "middle", 700)
    V, p2, p1, Y2 = (470, 50), (560, 115), (470, 180), (470, 270)
    s += edge(V, p1, "A", ORANGE, -60, 3) + edge(V, p2, "D", ORANGE, 15, 2) + edge(p2, p1, "E", ORANGE, 15, 1) + edge(p1, Y2, "B", ORANGE, -30, 4) + edge(p1, Y2, "C", ORANGE, 30, 5)
    for p_, l in ((V, "VDD"), (p2, "p2"), (p1, "p1"), (Y2, "Y")):
        s += node(*p_, l)
    s += text(320, 312, "Nodes = diffusion areas, edges = transistors (named by their input).", INK, 12.5, "middle")
    s += text(320, 334, "Euler path = one pen stroke over every edge once. Same order in BOTH graphs: E → D → A → B → C", PURPLE, 12.5, "middle", 700)
    return svg(660, 344, s)


def fig_stick_complex():
    # order E D A B C ; NMOS: n1 -E- GND -D- n1 -A- Y -B- n2 -C- GND
    # PMOS: p1 -E- p2 -D- VDD -A- p1 -B- Y -C- p1
    return stick(["E", "D", "A", "B", "C"], ["p1", "p2", "VDD", "p1", "Y", "p1"], ["n1", "GND", "n1", "Y", "n2", "GND"],
                 "Stick diagram of Y = [A(D+E)+BC]' with the Euler order E D A B C", [4], [3], [2], [1, 5], links=(("p", [0, 3, 5]), ("n", [0, 2])))


# ---------- Lecture 30 ----------
def fig_tpd_tcd():
    p = Plot(600, 300, (0, 5), (-0.15, 1.75), (40, 20, 20, 40))
    p.curve([(0, 1.3), (0.6, 1.3), (0.6, 1.7), (5, 1.7)], INK, 2.2)
    curves = [(0.4, GREEN), (0.9, BLUE), (1.5, ORANGE)]
    for tau, c in curves:
        p.curve([(0.6 + t / 100, exp(-(t / 100) / tau)) for t in range(0, 440)], c, 2.4)
    p.curve([(0, 1.0), (0.6, 1.0)], BLUE, 2.4)
    p.hline(0.5)
    t_cd, t_pd = 0.6 + 0.4 * log(2), 0.6 + 1.5 * log(2)
    p.add(dot(p.X(t_cd), p.Y(0.5), GREEN, 5) + dot(p.X(t_pd), p.Y(0.5), ORANGE, 5))
    y = p.Y(-0.05)
    p.add(arrow(p.X(0.6), y, p.X(t_cd), y, GREEN, 1.6) + text(p.X(t_cd) + 6, y + 4, sub("t_cd") + " (fastest case)", GREEN, 12.5, "start", 700))
    p.add(arrow(p.X(0.6), p.Y(0.5) - 16, p.X(t_pd), p.Y(0.5) - 16, ORANGE, 1.6) + text(p.X(t_pd) + 6, p.Y(0.5) - 12, sub("t_pd") + " (slowest case)", ORANGE, 12.5, "start", 700))
    p.add(text(p.X(2.6), p.Y(0.85), "output: same gate, three input patterns", MUTE, 12, "start"))
    p.add(text(p.X(0.7), p.Y(1.5), "input steps", INK, 12, "start", 600))
    p.axes("time →", "", [], [])
    return p.render()


def fig_rc():
    s = defs(*ALLC)
    s += text(90, 40, "R", INK, 14, "middle", 700)
    z = [(40, 60), (60, 60)]
    for i in range(6):
        z.append((66 + i * 8, 52 if i % 2 == 0 else 68))
    z += [(114, 60), (150, 60)]
    s += poly(z, INK, 2) + dot(40, 60) + text(34, 65, sub("V_in"), INK, 13, "end", 700)
    s += dot(150, 60) + text(158, 52, sub("V_out"), INK, 13, "start", 700) + cap(150, 60, INK, "C") + gnd(150, 100)
    svg1 = s
    p = Plot(420, 230, (0, 4), (0, 1.1), (60, 14, 14, 40))
    p.curve([(t / 100, exp(-t / 100)) for t in range(0, 401)], BLUE, 2.6)
    p.hline(0.5)
    p.add(dot(p.X(log(2)), p.Y(0.5), PURPLE, 5) + text(p.X(log(2)) + 8, p.Y(0.5) - 8, "50% at t = 0.69 RC", PURPLE, 12.5, "start", 700))
    p.add(text(p.X(1.6), p.Y(0.85), sub("V_out") + " = " + sub("V_DD") + "·e<tspan dy='-6' font-size='10'>−t/RC</tspan>", BLUE, 13, "start", 700))
    p.axes("t / RC", sub("V_out") + "/" + sub("V_DD"), [(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4")], [(0, "0"), (0.5, "0.5"), (1, "1")])
    return svg(260, 140, svg1), p.render()


def fig_rc_pair():
    a, b = fig_rc()
    return f'<div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;align-items:center">{a}{b}</div>'


def fig_mos_rc():
    s = defs(*ALLC)
    for row, (title, fn, rl, c) in enumerate([("NMOS of width k", nmos, "R/k", BLUE), ("PMOS of width k", pmos, "2R/k", ORANGE)]):
        oy = 30 + row * 170
        s += text(90, oy, title, c, 13, "middle", 700)
        s += fn(90, oy + 70, c) + text(116, oy + 75, "k", c, 13, "start", 700)
        s += arrow(170, oy + 70, 230, oy + 70, PURPLE, 2.2) + arrow(230, oy + 70, 170, oy + 70, PURPLE, 2.2)
        x = 330
        # switch + resistor between D(top) and S(bottom); caps on G, D, S
        s += line(x, oy + 15, x, oy + 35, c) + dot(x, oy + 15, c, 3) + text(x - 8, oy + 12, "D" if row == 0 else "S", INK, 12, "end", 700)
        s += res(x, oy + 35, c, rl, 40)
        s += line(x, oy + 75, x, oy + 88, c) + line(x, oy + 88, x - 14, oy + 104, c, 2.5) + line(x, oy + 108, x, oy + 125, c)
        s += dot(x, oy + 125, c, 3) + text(x - 8, oy + 140, "S" if row == 0 else "D", INK, 12, "end", 700)
        s += line(x - 60, oy + 96, x - 12, oy + 96, c, 1.6) + text(x - 70, oy + 100, "G", INK, 12, "end", 700)
        s += cap(x - 45, oy + 96, c) .replace("", "")  # gate cap
        s += text(x - 64, oy + 128, "kC", c, 12, "end", 700) + gnd(x - 45, oy + 136, c)
        s += line(x, oy + 15, x + 50, oy + 15, c) + cap(x + 50, oy + 15, c) + text(x + 66, oy + 40, "kC", c, 12, "start", 700) + gnd(x + 50, oy + 55, c)
        s += line(x, oy + 125, x + 50, oy + 125, c) + cap(x + 50, oy + 125, c) + text(x + 66, oy + 150, "kC", c, 12, "start", 700) + gnd(x + 50, oy + 165, c)
    s += text(560, 70, "switch + resistor + 3 capacitors", INK, 12.5, "middle", 700)
    s += text(560, 95, "wider (k bigger) → LESS R,", INK, 12.5, "middle")
    s += text(560, 115, "but MORE C (k·C on each terminal)", INK, 12.5, "middle")
    s += text(560, 160, "PMOS: holes are ~2× slower,", ORANGE, 12.5, "middle")
    s += text(560, 180, "so same width → 2× resistance", ORANGE, 12.5, "middle")
    s += text(560, 225, "R = V_DS,avg / I_DS,avg".replace("V_DS,avg", sub("V_{DS,avg}")).replace("I_DS,avg", sub("I_{DS,avg}")), PURPLE, 13, "middle", 700)
    s += text(560, 245, "(an average 'on' resistance)", PURPLE, 12, "middle")
    return svg(700, 370, s)


def fig_inv_rc():
    s = defs(*ALLC)
    s += text(150, 20, "Unit inverter (P = 2, N = 1)", INK, 13, "middle", 700)
    s += inverter(140, 150, ORANGE, BLUE)
    s += text(166, 105, "2", ORANGE, 13, "start", 700) + text(166, 205, "1", BLUE, 13, "start", 700)
    s += line(80, 150, 110, 150) + line(158, 150, 220, 150) + text(226, 155, "Y", INK, 14, "start", 700)
    s += arrow(255, 100, 330, 100, PURPLE, 2.2) + text(292, 90, "model", PURPLE, 11.5, "middle")
    x = 450
    s += text(470, 20, "RC model", INK, 13, "middle", 700)
    s += vdd(x, 40) + line(x, 40, x, 60) + res(x, 60, ORANGE, "2R/2 = R", 45) + line(x, 105, x, 150) + dot(x, 150)
    s += line(x, 150, x + 120, 150) + text(x + 126, 155, "Y", INK, 14, "start", 700)
    s += line(x, 150, x, 175) + res(x, 175, BLUE, None, 45) + text(x - 12, 202, "R/1 = R", BLUE, 12.5, "end", 600) + gnd(x, 220)
    s += line(x + 60, 150, x + 60, 155) + cap(x + 60, 155, GREEN) + gnd(x + 60, 195, GREEN) + text(x + 78, 182, "2C + C = 3C", GREEN, 12.5, "start", 700)
    s += dot(370, 150, PURPLE) + text(370, 138, "input node", PURPLE, 11.5, "middle", 600)
    s += cap(370, 150, PURPLE) + gnd(370, 190, PURPLE) + text(356, 182, "3C", PURPLE, 12.5, "end", 700)
    s += text(330, 262, "Pull-up R = pull-down R = R (equal rise and fall). Input cap = 2C + C = 3C. Output diffusion = 3C.", INK, 12.5, "middle")
    return svg(680, 275, s)


def fig_nand_caps(n=2):
    s = defs(*ALLC)
    wn = n
    ox = 200
    pw = 160 if n == 2 else 110
    xs = [ox - 60 + i * pw / (n - 1) * (n - 1) / (n - 1) if n > 1 else ox for i in range(n)]
    xs = [ox - 80 + i * (160 / (n - 1)) for i in range(n)]
    s += line(xs[0] + 18, 35, xs[-1] + 18, 35) + vdd((xs[0] + xs[-1]) / 2 + 18, 35)
    names = ["A", "B", "C"][:n]
    for i, x in enumerate(xs):
        s += pfet(x, 70, names[i], ORANGE, 2)
    s += line(xs[0] + 18, 105, xs[-1] + 18, 105)
    ymid = (xs[0] + xs[-1]) / 2 + 18
    s += dot(ymid, 105) + line(ymid, 105, ymid, 125 + 0)
    y = 160
    for i, nm in enumerate(reversed(names)):
        s += nfet(ymid - 18, y + i * 70, nm, BLUE, wn)
    s += gnd(ymid, y + (n - 1) * 70 + 35)
    s += line(xs[-1] + 18, 105, xs[-1] + 110, 105) + dot(xs[-1] + 110, 105) + text(xs[-1] + 118, 110, "Y", INK, 14, "start", 700)
    out_c = 2 * n + wn
    s += text(xs[-1] + 60, 98, f"{out_c}C", GREEN, 13, "middle", 700)
    for i in range(n - 1):
        yy = y + 35 + i * 70
        s += line(ymid, yy, ymid + 50, yy, MUTE, 1.2) + text(ymid + 56, yy + 5, f"{wn}C (internal)", GREEN, 12.5, "start", 700)
    s += text(520, 60, f"NAND{n} sized for unit drive", INK, 13, "middle", 700)
    s += text(520, 90, f"NMOS: {n} in series, each width {wn}", BLUE, 12.5, "middle")
    s += text(520, 110, f"→ total R = {n}·(R/{wn}) = R ✓", BLUE, 12.5, "middle")
    s += text(520, 140, "PMOS: parallel, each width 2", ORANGE, 12.5, "middle")
    s += text(520, 160, "→ one on: 2R/2 = R ✓", ORANGE, 12.5, "middle")
    s += text(520, 190, f"Input cap per input = {wn}C + 2C = {wn+2}C", PURPLE, 12.5, "middle", 700)
    s += text(520, 215, f"Output: {n}×2C (PMOS) + {wn}C (top NMOS) = {out_c}C", GREEN, 12.5, "middle", 700)
    return svg(680, y + (n - 1) * 70 + 70, s)


def fig_elmore():
    s = defs(*ALLC)
    xs = [80, 230, 380, 530]
    s += text(330, 22, "Elmore delay of an RC ladder (driver on the left)", INK, 13, "middle", 700)
    s += text(xs[0] - 10, 70, "source", INK, 12, "end", 600) + dot(xs[0], 66)
    labs = [("R₁", "C₁"), ("R₂", "C₂"), ("R₃", "C₃")]
    for i in range(3):
        x1, x2 = xs[i], xs[i + 1]
        z = [(x1, 66), (x1 + 35, 66)]
        for j in range(6):
            z.append((x1 + 41 + j * 12, 58 if j % 2 == 0 else 74))
        z += [(x1 + 110, 66), (x2, 66)]
        s += poly(z, ORANGE, 2) + text((x1 + x2) / 2, 48, labs[i][0], ORANGE, 13, "middle", 700)
        s += dot(x2, 66) + cap(x2, 66, BLUE) + gnd(x2, 106, BLUE) + text(x2 + 18, 92, labs[i][1], BLUE, 13, "start", 700)
    s += text(330, 160, "t = R₁·C₁ + (R₁ + R₂)·C₂ + (R₁ + R₂ + R₃)·C₃", PURPLE, 15, "middle", 700)
    s += text(330, 185, "each capacitor × ALL the resistance between it and the source", INK, 12.5, "middle")
    return svg(660, 198, s)


def fig_nand3_elmore():
    s = defs(*ALLC)
    x = 150
    s += text(x, 22, "NAND3 pull-down, A switches last", INK, 13, "middle", 700)
    nodes = [(60, "Y", "9C", "R/3 + R/3 + R/3 = R"), (130, "n2", "3C", "R/3 + R/3 = 2R/3"), (200, "n1", "3C", "R/3")]
    s += dot(x, 60) + text(x - 10, 64, "Y", INK, 14, "end", 700)
    for i, nm in enumerate(("C", "B", "A")):
        yy = 60 + i * 70
        s += res(x, yy, BLUE, f"R/3  ({nm})", 70)
        if i < 2:
            s += dot(x, yy + 70)
    s += gnd(x, 270)
    for yy, nm, cv, rv in nodes:
        s += line(x, yy, x + 60, yy, MUTE, 1.2) + cap(x + 60, yy, GREEN) + gnd(x + 60, yy + 40, GREEN)
        s += text(x + 80, yy + 26, cv, GREEN, 13, "start", 700)
        s += text(x + 120, yy + 6, f"{nm}: R to ground = {rv}", INK, 12.5, "start")
    s += text(460, 230, "t_pdf = 9C·R + 3C·(2R/3) + 3C·(R/3)".replace("t_pdf", sub("t_pdf")), PURPLE, 13, "middle", 700)
    s += text(460, 252, "= 9RC + 2RC + RC = 12RC", PURPLE, 13, "middle", 700)
    return svg(660, 300, s)


# ---------- Lecture 31 / logical effort ----------
def fig_fanout(m_label="m", fo4=False):
    s = defs(*ALLC)
    g, ox = gate_shape("inv", 60, 120, "1")
    s += g + line(20, 120, 60, 120)
    n = 4
    s += line(ox, 120, 170, 120)
    s += line(170, 50, 170, 190)
    for i in range(n):
        yy = 50 + i * 46.6
        g2, o2 = gate_shape("inv", 200, yy, "1")
        s += line(170, yy, 200, yy) + g2 + line(o2, yy, o2 + 20, yy)
    s += text(300, 125, "×4 (FO4)" if fo4 else "× m", INK, 14, "start", 700)
    s += text(470, 60, "each load inverter: input cap 3C", INK, 12.5, "middle")
    s += text(470, 85, "load = own diffusion 3C + " + ("4" if fo4 else "m") + " × 3C", INK, 12.5, "middle")
    s += text(470, 120, (sub("t_pd") + " = R·(3C + 4·3C) = 5·3RC") if fo4 else (sub("t_pd") + " = R·(3C + 3mC) = (1 + m)·3RC"), PURPLE, 13, "middle", 700)
    s += text(470, 150, ("d = 1 + 4 = 5   →   t = 5τ = 15RC" if fo4 else "d = t_pd/τ = m + 1   (τ = 3RC)").replace("t_pd", sub("t_pd")), PURPLE, 13, "middle", 700)
    return svg(640, 220, s)


def fig_d_parts():
    p = Plot(560, 320, (0, 8), (0, 18), (60, 20, 20, 44))
    for g, c, lab in ((1, INK, "inverter g = 1, p = 1"), (4 / 3, BLUE, "NAND2 g = 4/3, p = 2"), (5 / 3, ORANGE, "NOR2 g = 5/3, p = 2")):
        pp = 1 if g == 1 else 2
        p.curve([(0, pp), (8, pp + 8 * g)], c, 2.6)
        yl = {1: 0, 4 / 3: 1, 5 / 3: 2}[g]
        p.add(line(p.X(0.4), p.Y(16.5 - yl * 1.6), p.X(1.0), p.Y(16.5 - yl * 1.6), c, 3) + text(p.X(1.15), p.Y(16.5 - yl * 1.6) + 4, lab, c, 12, "start", 700))
    p.add(text(p.X(0.2), p.Y(0.4), "intercept = parasitic delay p", MUTE, 11.5, "start"))
    p.add(text(p.X(3.5), p.Y(2.3), "slope = logical effort g", MUTE, 11.5, "start"))
    p.axes("electrical effort h = C_out / C_in".replace("C_out", sub("C_out")).replace("C_in", sub("C_in")), "normalized delay d", [(0, "0"), (2, "2"), (4, "4"), (6, "6"), (8, "8")], [(0, "0"), (5, "5"), (10, "10"), (15, "15")])
    return p.render()


def fig_le_gates():
    s = defs(*ALLC)
    for i, (title, nw, pw, cin, g) in enumerate((("Inverter", "1", "2", "3", "1"), ("NAND2", "2", "2", "4", "4/3"), ("NOR2", "1", "4", "5", "5/3"))):
        ox = 40 + i * 215
        s += text(ox + 95, 22, title, INK, 13, "middle", 700)
        s += text(ox + 95, 50, "NMOS width " + nw + ", PMOS width " + pw, MUTE, 12, "middle")
        s += f'<rect x="{ox+30}" y="66" width="130" height="34" rx="8" fill="{PURPLE}" opacity="0.12" stroke="{PURPLE}"/>'
        s += text(ox + 95, 88, f"C_in = {nw} + {pw} = {cin}".replace("C_in", sub("C_in")), PURPLE, 12.5, "middle", 700)
        s += text(ox + 95, 128, f"g = {cin}/3 = {g}" if g != "1" else "g = 3/3 = 1", BLUE, 14, "middle", 700)
    s += text(330, 165, "Logical effort = how much MORE input capacitance a gate needs than an inverter to give the SAME output current.", INK, 12, "middle")
    return svg(660, 178, s)


def fig_t10q4():
    s = defs(*ALLC)
    # stage 1: unit inverter
    g1, o1 = gate_shape("inv", 50, 70, "1")
    s += line(15, 70, 50, 70) + g1 + text(10, 74, "in", MUTE, 11, "end")
    node = 150
    s += line(o1, 70, 230, 70) + dot(node, 70)
    # NAND x2 (inputs at y 60 and 80)
    g2, o2 = gate_shape("nand", 230, 70, "x2", BLUE)
    s += g2
    s += line(o1, 70, 230, 70)
    s += line(15, 82, 230, 82, MUTE, 1.4) + text(10, 86, "in", MUTE, 11, "end")
    # NOR x3 (inputs y 160, 180)
    g3, o3 = gate_shape("nor", 230, 170, "x3", ORANGE)
    s += line(node, 70, node, 160) + line(node, 160, 236, 160) + g3
    s += line(15, 180, 236, 180, MUTE, 1.4) + text(10, 184, "in", MUTE, 11, "end")
    # NOR3 x4 (inputs y 130,145,160)
    g4, o4 = gate_shape("nor", 430, 145, "x4", ORANGE, 1.1)
    s += g4
    s += line(o2, 70, 380, 70) + line(380, 70, 380, 132) + line(380, 132, 437, 132)
    s += line(o3, 170, 380, 170) + line(380, 170, 380, 146) + line(380, 146, 440, 146)
    s += line(15, 230, 400, 230, MUTE, 1.4) + line(400, 230, 400, 158) + line(400, 158, 437, 158) + text(10, 234, "in", MUTE, 11, "end")
    # wire cap and x5
    s += line(o4, 145, 560, 145) + dot(520, 145) + line(520, 145, 520, 160) + cap(520, 160, AMBER) + gnd(520, 200, AMBER)
    s += text(538, 186, "C₄ = 10", AMBER, 12.5, "start", 700)
    g5, o5 = gate_shape("inv", 560, 145, "x5")
    s += g5 + line(o5, 145, 680, 145) + dot(670, 145) + line(670, 145, 670, 160) + cap(670, 160, INK) + gnd(670, 200) + text(688, 186, "C₅ = 12", INK, 12.5, "start", 700)
    s += text(255, 40, "NAND2: g = 4/3, p = 2", BLUE, 11.5, "middle")
    s += text(255, 208, "NOR2: g = 5/3, p = 2", ORANGE, 11.5, "middle")
    s += text(460, 105, "NOR3: g = 7/3, p = 3", ORANGE, 11.5, "middle")
    s += text(380, 268, "x = drive (size) of each gate; unit inverter = 1. A gate of drive x has input cap g·x.", INK, 12.5, "middle")
    return svg(760, 280, s)


def fig_nor2_sized():
    s = defs(*ALLC)
    ox = 150
    s += pfet(ox, 70, "A", ORANGE, 4) + pfet(ox, 140, "B", ORANGE, 4) + vdd(ox + 18, 35)
    s += line(ox + 18, 175, ox + 18, 195) + line(ox - 22, 195, ox + 128, 195)
    s += nfet(ox - 40, 230, "A", BLUE, 1) + nfet(ox + 110, 230, "B", BLUE, 1)
    s += line(ox - 22, 265, ox + 128, 265) + gnd(ox + 53, 265)
    s += dot(ox + 18, 195) + line(ox + 128, 195, ox + 180, 195) + dot(ox + 180, 195) + text(ox + 188, 200, "Y", INK, 14, "start", 700)
    s += line(ox + 18, 105, ox + 70, 105, MUTE, 1.2) + text(ox + 76, 110, "internal node: 4C + 4C = 8C", GREEN, 12.5, "start", 700)
    s += text(ox + 188, 222, "output: 4C + 1C + 1C = 6C", GREEN, 12.5, "start", 700)
    s += text(ox + 188, 242, "+ load: h × 5C", GREEN, 12.5, "start", 700)
    s += text(500, 30, "PMOS: 2 in series, need R total", ORANGE, 12.5, "middle")
    s += text(500, 48, "→ each R/2 → width 4 (2R/4)", ORANGE, 12.5, "middle", 700)
    s += text(500, 68, "NMOS: alone it must give R → width 1", BLUE, 12.5, "middle", 700)
    s += text(500, 86, "Input cap = 4C + 1C = 5C", PURPLE, 12.5, "middle", 700)
    return svg(660, 300, s)


def fig_aoi21():
    s = defs(*ALLC)
    # PUN: (A || B) series C ; PDN: (A series B) || C
    s += line(110, 35, 290, 35) + vdd(200, 35)
    s += pfet(110, 70, "A", ORANGE, 4) + pfet(255, 70, "B", ORANGE, 4)
    s += line(128, 105, 273, 105) + dot(200, 105) + text(206, 100, "p1", MUTE, 11)
    s += pfet(182, 140, "C", ORANGE, 4)
    s += dot(200, 175) + line(200, 175, 200, 195) + line(128, 195, 330, 195) + line(330, 195, 400, 195) + dot(400, 195) + text(408, 200, "Y", INK, 14, "start", 700)
    s += nfet(110, 230, "A", BLUE, 2) + nfet(110, 300, "B", BLUE, 2) + gnd(128, 335)
    s += text(134, 270, "n1", MUTE, 11)
    s += nfet(294, 230, "C", BLUE, 1) + gnd(312, 265)
    s += text(560, 40, "AOI21: Y = (AB + C)'", INK, 14, "middle", 700)
    s += text(560, 75, "NMOS A, B: series, width 2 each (R/2+R/2)", BLUE, 12, "middle")
    s += text(560, 95, "NMOS C: width 1 (R)", BLUE, 12, "middle")
    s += text(560, 125, "PMOS A ∥ B, then C in series:", ORANGE, 12, "middle")
    s += text(560, 145, "width 4 each (R/2 + R/2)", ORANGE, 12, "middle")
    s += text(560, 180, "Input caps: A = B = 6C, C = 5C", PURPLE, 12.5, "middle", 700)
    return svg(700, 350, s)


def fig_ring_le():
    s = defs(*ALLC)
    xs = [60, 170, 280]
    for x in xs:
        g, o = gate_shape("inv", x, 70)
        s += g + line(o, 70, o + 25, 70)
    s += text(420, 75, "· · ·", INK, 20, "middle", 700)
    g, o = gate_shape("inv", 470, 70)
    s += g + line(o, 70, 580, 70) + poly([(580, 70), (580, 130), (30, 130), (30, 70), (60, 70)], ORANGE, 2)
    s += text(320, 160, "each stage = inverter driving ONE inverter → d = gh + p = 1·1 + 1 = 2 → 2τ per stage", INK, 12.5, "middle")
    s += text(320, 182, "period T = 2 × N × 2τ = 4Nτ  →  f = 1/(4Nτ)", PURPLE, 13, "middle", 700)
    return svg(640, 194, s)




# ---------- pass-3 figures (one per question) ----------
def fig_norn():
    s = defs(*ALLC)
    x = 160
    s += vdd(x + 18, 30) + text(x + 140, 22, "NOR-n pull-up", INK, 13, "start", 700)
    names = ["A₁ (2n)", "A₂ (2n)", "⋮", "Aₙ (2n)"]
    y = 65
    for i, nm in enumerate(names):
        if nm == "⋮":
            s += line(x + 18, y - 35, x + 18, y + 10) + text(x + 30, y - 5, "⋮", INK, 16, "start", 700)
            y += 45
            continue
        s += pmos(x, y, ORANGE) + text(x - 36, y + 5, nm, ORANGE, 12.5, "end", 700)
        if i < len(names) - 1:
            s += line(x + 18, y + 35, x + 18, y + 45) + dot(x + 18, y + 40) + line(x + 18, y + 40, x + 70, y + 40, MUTE, 1.2)
            s += text(x + 76, y + 45, f"internal node {i+1}: 2nC, R to V_DD = {i+1}·R/n".replace("V_DD", sub("V_DD")), GREEN, 12, "start", 600)
        y += 80
    s += dot(x + 18, y - 45) + line(x + 18, y - 45, x + 120, y - 45) + text(x + 126, y - 40, "Y: 2nC + n·C = 3nC", GREEN, 12.5, "start", 700)
    s += text(330, y - 5, "each PMOS: width 2n → resistance 2R/2n = R/n; the n of them in series = R", INK, 12.5, "middle")
    return svg(660, y + 8, s)


def fig_4x():
    s = defs(*ALLC)
    for i, (title, wp, wn, cin, r) in enumerate((("unit inverter (1x)", 2, 1, "3", "R"), ("4x inverter", 8, 4, "12", "R/4"))):
        ox = 140 + i * 320
        s += text(ox + 10, 22, title, INK, 13, "middle", 700)
        s += inverter(ox, 140, ORANGE, BLUE) + text(ox + 26, 95, str(wp), ORANGE, 13, "start", 700) + text(ox + 26, 195, str(wn), BLUE, 13, "start", 700)
        s += line(ox - 70, 140, ox - 30, 140) + line(ox + 18, 140, ox + 70, 140)
        s += text(ox + 10, 260, f"input cap {cin} units · pull resistance {r}", PURPLE, 12.5, "middle", 700)
    s += text(320, 285, "4× the input cap, but 4× the current: same ratio → same g = 1; own diffusion ×4 but R ÷4 → same p", INK, 12, "middle")
    return svg(660, 295, s)


def fig_weak_p():
    s = defs(*ALLC)
    # NAND2 with PMOS 3 / NMOS 2 and NOR2 with PMOS 6 / NMOS 1, simple labelled blocks
    blocks = [("inverter", "1", "3", "4", "1"), ("NAND2", "2 (series)", "3 (parallel)", "5", "5/4"), ("NOR2", "1 (parallel)", "6 (series)", "7", "7/4")]
    for i, (nm, n, pw, cin, g) in enumerate(blocks):
        ox = 30 + i * 215
        s += f'<rect x="{ox}" y="30" width="190" height="150" rx="12" fill="#f6f8fb" stroke="#e3e7ee"/>'
        s += text(ox + 95, 55, nm, INK, 14, "middle", 700)
        s += text(ox + 95, 85, "PMOS width " + pw, ORANGE, 12.5, "middle", 600)
        s += text(ox + 95, 108, "NMOS width " + n, BLUE, 12.5, "middle", 600)
        s += text(ox + 95, 135, "input cap = " + cin, PURPLE, 12.5, "middle", 700)
        s += text(ox + 95, 162, "g = " + cin + "/4 = " + g if nm != "inverter" else "reference: 4", GREEN, 13, "middle", 700)
    s += text(330, 205, "PMOS is 3× weaker → a PMOS needs width 3 to match one unit NMOS (instead of 2)", INK, 12.5, "middle")
    return svg(660, 215, s)


def fig_p2_bars():
    from math import sqrt
    rows = []
    need = 1.05 / 0.95
    for nm, f, c in (("inverter", 1, INK), ("NOR2", 0.5, BLUE), ("NAND2", 2, ORANGE)):
        kR = (f / need) ** 2
        rows.append((nm, round(2.4 / kR, 2), c))
    return F.barh(rows, "", w=620, title="(W/L)p / (W/L)n needed for V_th = V_DD/2 = 1.65 V".replace("V_th", sub("V_th")).replace("V_DD", sub("V_DD")))


def fig_p3_vtc():
    VDD = 3.3
    inv = vtc(VDD, 0.6, -0.6, 100, 100)
    nor = vtc(VDD, 0.6, -0.6, 200, 50)
    nand = vtc(VDD, 0.6, -0.6, 50, 200)
    p = Plot(560, 320, (0, 3.3), (0, 3.5), (60, 20, 20, 44))
    p.curve([(0, 0), (3.3, 3.3)], GREY, 1.4, "5 4")
    p.curve(nor, BLUE, 2.6); p.curve(inv, INK, 2.2, "6 4"); p.curve(nand, ORANGE, 2.6)
    for v, c, lab in ((1.3, BLUE, "NOR2 1.30 V"), (1.65, INK, "INV 1.65 V"), (2.0, ORANGE, "NAND2 2.00 V")):
        p.add(dot(p.X(v), p.Y(v), c, 5) + text(p.X(v) + 10, p.Y(v) + 4, lab, c, 12.5, "start", 700))
    p.axes(sub("V_in") + " (V)", sub("V_out") + " (V)", [(0, "0"), (1.3, "1.3"), (2, "2"), (3.3, "3.3")], [(0, "0"), (1, "1"), (2, "2"), (3.3, "3.3")])
    return p.render()


def fig_p4():
    s = defs(*ALLC)
    def nm(x, y, g, on):
        c = BLUE if on else GREY
        return nfet(x, y, g, c, None) + text(x + 24, y + 5, "2", MUTE, 12, "start", 700) + text(x + 24, y + 20, "ON" if on else "off", GREEN if on else MUTE, 11, "start", 700)
    for k, (title, on) in enumerate((("(a) all inputs 1", dict(A=1, D=1, E=1, B=1, C=1)), ("(b) worst case: A = D = 1 only", dict(A=1, D=1, E=0, B=0, C=0)))):
        ox = 20 + k * 330
        s += text(ox + 150, 22, title, INK, 13, "middle", 700)
        s += line(ox + 108, 50, ox + 292, 50) + dot(ox + 200, 50) + line(ox + 200, 50, ox + 200, 38) + text(ox + 206, 40, "Y", INK, 13, "start", 700)
        s += nm(ox + 90, 85, "A", on["A"])
        s += line(ox + 108, 120, ox + 108, 130) + line(ox + 60, 130, ox + 140, 130)
        s += nm(ox + 42, 165, "D", on["D"]) + nm(ox + 122, 165, "E", on["E"])
        s += line(ox + 60, 200, ox + 140, 200) + gnd(ox + 100, 200)
        s += nm(ox + 274, 85, "B", on["B"]) + nm(ox + 274, 155, "C", on["C"]) + gnd(ox + 292, 190)
    s += text(330, 240, "(a) 1/(1/2 + 1/4) + 1/(1/2 + 1/2) = 4/3 + 1 = 7/3      (b) 1/(1/2 + 1/2) = 1", PURPLE, 13, "middle", 700)
    return svg(660, 252, s)


def fig_aoi22_euler():
    s = defs(*ALLC)

    def node(x, y, lab, dx=0, dy=22):
        return f'<circle cx="{x}" cy="{y}" r="6" fill="white" stroke="{INK}" stroke-width="2.2"/>' + text(x + dx, y + dy, sub({"VDD": "V_DD"}.get(lab, lab)), INK, 12, "middle", 700)

    def edge(p1, p2, lab, c, bend, num):
        (x1, y1), (x2, y2) = p1, p2
        qx, qy = (x1 + x2) / 2 + bend, (y1 + y2) / 2
        cx, cy = (x1 + x2) / 2 + bend / 2, (y1 + y2) / 2
        sg = 1 if bend >= 0 else -1
        e = f'<path d="M{x1},{y1} Q{qx},{qy} {x2},{y2}" fill="none" stroke="{c}" stroke-width="2.4"/>'
        e += text(cx + sg * 13, cy + 5, lab, c, 14, "middle", 700)
        e += f'<circle cx="{cx + sg*30}" cy="{cy}" r="9" fill="{PURPLE}"/>' + text(cx + sg * 30, cy + 4, str(num), "white", 11, "middle", 700)
        return e
    s += text(160, 22, "Pull-down (NMOS)", BLUE, 13, "middle", 700)
    Y, n1, n2, G = (160, 50), (90, 150), (230, 150), (160, 260)
    s += edge(Y, n1, "A", BLUE, -10, 1) + edge(n1, G, "B", BLUE, -10, 2) + edge(G, n2, "D", BLUE, 10, 3) + edge(n2, Y, "C", BLUE, 10, 4)
    s += node(*Y, "Y", 0, -12) + node(*n1, "n1", -22, 4) + node(*n2, "n2", 24, 4) + node(*G, "GND", 0, 22)
    s += text(480, 22, "Pull-up (PMOS)", ORANGE, 13, "middle", 700)
    V, P, Y2 = (480, 55), (480, 155), (480, 260)
    s += edge(P, V, "A", ORANGE, -50, 1) + edge(V, P, "B", ORANGE, 50, 2) + edge(P, Y2, "D", ORANGE, 50, 3) + edge(Y2, P, "C", ORANGE, -50, 4)
    s += node(*V, "VDD", 0, -12) + node(*P, "p", -22, 4) + node(*Y2, "Y", 0, 22)
    s += text(320, 300, "Same order A → B → D → C traces every edge once in both graphs", PURPLE, 13, "middle", 700)
    return svg(660, 312, s)


def fig_p7():
    s = defs(*ALLC)
    s += line(110, 35, 330, 35) + vdd(220, 35)
    s += pfet(110, 75, "A", ORANGE, 4)
    s += pfet(270, 60, "D", ORANGE, 6) + pfet(270, 130, "E", ORANGE, 6)
    s += line(128, 40, 128, 35) + line(288, 25, 288, 35)
    s += line(128, 110, 128, 175) + line(288, 165, 288, 175) + line(128, 175, 288, 175)
    s += pfet(110, 215, "B", ORANGE, 6) + pfet(270, 215, "C", ORANGE, 6)
    s += line(128, 250, 128, 265) + line(288, 250, 288, 265) + line(128, 265, 288, 265)
    s += dot(208, 265) + line(288, 265, 400, 265) + dot(400, 265) + text(408, 270, "Y", INK, 15, "start", 700)
    s += line(208, 265, 208, 285) + line(128, 285, 330, 285)
    s += nfet(110, 320, "A", BLUE, 2) + line(128, 355, 128, 365) + line(80, 365, 160, 365)
    s += nfet(62, 400, "D", BLUE, 2) + nfet(142, 400, "E", BLUE, 2) + line(80, 435, 160, 435) + gnd(120, 435)
    s += nfet(294, 320, "B", BLUE, 2) + nfet(294, 390, "C", BLUE, 2) + gnd(312, 425)
    s += text(470, 60, "Longest path through each transistor:", INK, 12.5, "start", 700)
    s += text(470, 85, "NMOS: every path has 2 → all width 2", BLUE, 12.5, "start")
    s += text(470, 110, "PMOS D, E: path D–E–B has 3 → width 6", ORANGE, 12.5, "start")
    s += text(470, 130, "PMOS B, C: also on D–E–B/C → width 6", ORANGE, 12.5, "start")
    s += text(470, 150, "PMOS A: paths A–B, A–C have 2 → width 4", ORANGE, 12.5, "start")
    s += text(470, 190, "Input caps: A 6C, D/E/B/C 8C", PURPLE, 12.5, "start", 700)
    s += text(470, 210, "g: A = 2, others = 8/3", PURPLE, 12.5, "start", 700)
    return svg(700, 470, s)


def fig_p8():
    s = defs(*ALLC)
    g1, o1 = gate_shape("inv", 60, 80, "1")
    s += line(20, 80, 60, 80) + g1
    g2, o2 = gate_shape("nand", 230, 80, "1", BLUE)
    s += line(o1, 80, 230, 80) + line(200, 92, 230, 92, MUTE, 1.4) + text(195, 96, "1", MUTE, 11, "end")
    s += g2 + line(o2, 80, 400, 80) + dot(380, 80) + line(380, 80, 380, 95) + cap(380, 95, INK) + gnd(380, 135) + text(398, 120, "12C", INK, 13, "start", 700)
    s += text(150, 140, "stage 1: inverter drives NAND2 input 4C", INK, 12, "middle")
    s += text(150, 158, "h₁ = 4C/3C = 4/3,  d₁ = 4/3 + 1 = 2.33", PURPLE, 12.5, "middle", 700)
    s += text(470, 30, "stage 2: NAND2 drives 12C", INK, 12, "middle")
    s += text(470, 48, "h₂ = 12C/4C = 3,  d₂ = (4/3)·3 + 2 = 6", PURPLE, 12.5, "middle", 700)
    s += text(330, 190, "path delay D = d₁ + d₂ = 8.33 τ  (= 25 ps when τ = 3 ps)", INK, 13, "middle", 700)
    return svg(660, 200, s)


def fig_ron():
    p = Plot(520, 260, (0, 42), (0, 1700), (70, 20, 20, 44))
    p.curve([(w / 10, 1 / (134.3e-6 * (w / 10) / 0.5 * 2.3)) for w in range(20, 421)], BLUE, 2.8)
    for w in (10, 20):
        r = 1 / (134.3e-6 * w / 0.5 * 2.3)
        p.add(dot(p.X(w), p.Y(r), ORANGE, 5) + text(p.X(w) + 8, p.Y(r) - 8, f"W = {w} µm: {r:.0f} Ω", ORANGE, 12.5, "start", 700))
    p.axes("W (µm), L = 0.5 µm", sub("R_on") + " (Ω)", [(2, "2"), (10, "10"), (20, "20"), (40, "40")], [(0, "0"), (500, "500"), (1000, "1000"), (1500, "1500")])
    return p.render()


def fig_fold():
    s = defs(*ALLC)
    s += text(150, 22, "one finger, W = 20 µm", INK, 13, "middle", 700)
    s += f'<rect x="60" y="40" width="60" height="200" fill="{BLUE}" opacity="0.15" stroke="{BLUE}"/>' + text(90, 145, "S", BLUE, 13, "middle", 700)
    s += f'<rect x="120" y="30" width="18" height="220" fill="{RED}" opacity="0.4"/>'
    s += f'<rect x="138" y="40" width="60" height="200" fill="{GREEN}" opacity="0.25" stroke="{GREEN}" stroke-width="2.5"/>' + text(168, 145, "D", GREEN, 13, "middle", 700)
    s += text(150, 268, "C_DB = 18.3 fF".replace("C_DB", sub("C_DB")), GREEN, 13, "middle", 700)
    s += text(470, 22, "two fingers, W = 10 µm each, shared drain", INK, 13, "middle", 700)
    ox = 360
    s += f'<rect x="{ox}" y="90" width="50" height="100" fill="{BLUE}" opacity="0.15" stroke="{BLUE}"/>' + text(ox + 25, 145, "S", BLUE, 13, "middle", 700)
    s += f'<rect x="{ox+50}" y="80" width="18" height="120" fill="{RED}" opacity="0.4"/>'
    s += f'<rect x="{ox+68}" y="90" width="60" height="100" fill="{GREEN}" opacity="0.25" stroke="{GREEN}" stroke-width="2.5"/>' + text(ox + 98, 145, "D", GREEN, 13, "middle", 700)
    s += f'<rect x="{ox+128}" y="80" width="18" height="120" fill="{RED}" opacity="0.4"/>'
    s += f'<rect x="{ox+146}" y="90" width="50" height="100" fill="{BLUE}" opacity="0.15" stroke="{BLUE}"/>' + text(ox + 171, 145, "S", BLUE, 13, "middle", 700)
    s += text(470, 268, "C_DB = 9.2 fF (drain area halved)".replace("C_DB", sub("C_DB")), GREEN, 13, "middle", 700)
    return svg(660, 280, s)


FIGS2 = {
    "F_SWITCH": fig_switches, "F_PUNPDN": fig_pun_pdn, "F_PSEUDO": fig_pseudo, "F_NOR2": fig_nor2, "F_NAND2": fig_nand2,
    "F_WL": fig_wl, "F_COLLAPSE": fig_nor2_collapse, "F_VTHCMP": fig_vth_compare, "F_STNOR": fig_stick_nor2, "F_STNAND": fig_stick_nand2,
    "F_COMPLEX": fig_complex, "F_EULER": fig_euler, "F_STCPX": fig_stick_complex, "F_TPDTCD": fig_tpd_tcd, "F_RC": fig_rc_pair,
    "F_MOSRC": fig_mos_rc, "F_INVRC": fig_inv_rc, "F_NAND2C": lambda: fig_nand_caps(2), "F_NAND3C": lambda: fig_nand_caps(3),
    "F_ELMORE": fig_elmore, "F_NAND3E": fig_nand3_elmore, "F_FANOUT": lambda: fig_fanout(), "F_FO4": lambda: fig_fanout(fo4=True),
    "F_DPARTS": fig_d_parts, "F_LEGATES": fig_le_gates, "F_T10Q4": fig_t10q4, "F_NOR2S": fig_nor2_sized, "F_AOI": fig_aoi21,
    "F_RINGLE": fig_ring_le, "F_NORN": fig_norn, "F_4X": fig_4x, "F_WEAKP": fig_weak_p, "F_P2": fig_p2_bars, "F_P3": fig_p3_vtc, "F_P4": fig_p4, "F_AOI22": fig_aoi22_euler, "F_P7": fig_p7, "F_P8": fig_p8, "F_RON": fig_ron, "F_FOLD": fig_fold,
}

if __name__ == "__main__":
    src = open(os.path.join(HERE, "guide_src.html"), encoding="utf-8").read()
    allf = dict(F.FIGS)
    allf.update(FIGS2)
    for key, fn in allf.items():
        tok = "{{" + key + "}}"
        if tok in src:
            src = src.replace(tok, fn())
    left = re.findall(r"\{\{[A-Z0-9_]+\}\}", src)
    if left:
        print("UNFILLED", left)
    out = os.path.join(HERE, "..", "Lectures28-31_Guide.html")
    open(out, "w", encoding="utf-8").write(src)
    print("wrote", out)
