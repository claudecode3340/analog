"""Builds the SVG figures for the Lecture 25 guide and fills them into guide_src.html.

Every curve is computed from the square-law model, so the pictures match the numbers in the text.
"""
from math import log
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

BLUE, ORANGE, GREEN, PURPLE, RED, AMBER, INK, MUTE = (
    "#2563eb", "#ea580c", "#059669", "#7c3aed", "#dc2626", "#b45309", "#1f2633", "#8a92a3")


# ---------- model ----------
def i_d(k, u, v):
    """Square-law drain current magnitude: overdrive u, |VDS| v."""
    if u <= 0:
        return 0.0
    return k * (u * v - v * v / 2) if v < u else k * u * u / 2


def discharge(C, k, VT, VDD, V0, t_end, dt=1e-3):
    """NMOS with gate at VDD discharging C from V0. Returns [(t, V)]. Units: fF, uA/V^2 -> ns."""
    u, V, t, pts = VDD - VT, V0, 0.0, [(0.0, V0)]
    while t < t_end:
        f = lambda x: -i_d(k, u, x) / C
        k1 = f(V); k2 = f(V + dt / 2 * k1); k3 = f(V + dt / 2 * k2); k4 = f(V + dt * k3)
        V += dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t += dt
        pts.append((t, V))
    return pts


# ---------- svg helpers ----------
def svg(w, h, body, cls="fig"):
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" width="{w}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Inter, Segoe UI, sans-serif" font-size="13">{body}</svg>')


def line(x1, y1, x2, y2, c=INK, w=2, dash=None, extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} {extra}/>'


def poly(pts, c=INK, w=2, fill="none", dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{p}" fill="{fill}" stroke="{c}" stroke-width="{w}"{d} stroke-linejoin="round"/>'


def text(x, y, s, c=INK, size=13, anchor="start", weight=400, italic=False):
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" text-anchor="{anchor}" '
            f'font-weight="{weight}"{st}>{s}</text>')


def dot(x, y, c=INK, r=3.5):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def arrow(x1, y1, x2, y2, c=INK, w=2):
    return line(x1, y1, x2, y2, c, w, extra=f'marker-end="url(#ah{c[1:]})"')


def defs(*colors):
    m = "".join(
        f'<marker id="ah{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for c in colors)
    return f"<defs>{m}</defs>"


ALLC = (INK, BLUE, ORANGE, GREEN, PURPLE, RED, AMBER, MUTE)


def nmos(x, y, c=INK, label=None):
    """Channel line at x. Gate input at (x-30,y). Drain top (x+18,y-35). Source bottom (x+18,y+35)."""
    s = line(x, y - 18, x, y + 18, c, 3) + line(x - 7, y - 16, x - 7, y + 16, c, 2) + line(x - 30, y, x - 7, y, c)
    s += poly([(x, y - 12), (x + 18, y - 12), (x + 18, y - 35)], c) + poly([(x, y + 12), (x + 18, y + 12), (x + 18, y + 35)], c)
    s += arrow(x + 16, y + 12, x + 3, y + 12, c, 1.6)
    if label:
        s += text(x + 26, y + 5, label, c, 12)
    return s


def pmos(x, y, c=INK, label=None):
    """Source top (x+18,y-35). Drain bottom (x+18,y+35). Gate (x-30,y) with bubble."""
    s = line(x, y - 18, x, y + 18, c, 3) + line(x - 7, y - 16, x - 7, y + 16, c, 2) + line(x - 30, y, x - 16, y, c)
    s += f'<circle cx="{x-11.5}" cy="{y}" r="4.5" fill="white" stroke="{c}" stroke-width="2"/>'
    s += poly([(x, y - 12), (x + 18, y - 12), (x + 18, y - 35)], c) + poly([(x, y + 12), (x + 18, y + 12), (x + 18, y + 35)], c)
    if label:
        s += text(x + 26, y + 5, label, c, 12)
    return s


def gnd(x, y, c=INK):
    return line(x, y, x, y + 8, c) + line(x - 12, y + 8, x + 12, y + 8, c) + line(x - 7, y + 13, x + 7, y + 13, c) + line(x - 3, y + 18, x + 3, y + 18, c)


def vdd(x, y, c=INK):
    return line(x - 12, y, x + 12, y, c, 2.5) + text(x, y - 7, "V<tspan font-size='9' dy='3'>DD</tspan>", c, 13, "middle")


def cap(x, y, c=INK, label=None, horiz=False):
    """Vertical capacitor: top lead from (x,y) to plates, bottom lead to (x,y+40)."""
    s = line(x, y, x, y + 16, c) + line(x - 13, y + 16, x + 13, y + 16, c, 3) + line(x - 13, y + 24, x + 13, y + 24, c, 3) + line(x, y + 24, x, y + 40, c)
    if label:
        s += text(x + 18, y + 25, label, c, 13)
    return s


def inverter(cx, cy, cp=INK, cn=INK, vin_label=True):
    """Inverter: PMOS at (cx, cy-50), NMOS at (cx, cy+50). Output node at (cx+18, cy). Input node at (cx-30, cy)."""
    s = pmos(cx, cy - 50, cp) + nmos(cx, cy + 50, cn)
    s += line(cx + 18, cy - 15, cx + 18, cy + 15, INK) + line(cx - 30, cy - 50, cx - 30, cy + 50, INK)
    s += vdd(cx + 18, cy - 85) + gnd(cx + 18, cy + 85)
    s += dot(cx - 30, cy) + dot(cx + 18, cy)
    return s


class Plot:
    def __init__(self, w, h, xr, yr, pad=(60, 20, 20, 44)):
        self.w, self.h, self.xr, self.yr = w, h, xr, yr
        self.l, self.t, self.r, self.b = pad
        self.parts = []

    def X(self, x):
        return self.l + (x - self.xr[0]) / (self.xr[1] - self.xr[0]) * (self.w - self.l - self.r)

    def Y(self, y):
        return self.h - self.b - (y - self.yr[0]) / (self.yr[1] - self.yr[0]) * (self.h - self.t - self.b)

    def add(self, s):
        self.parts.append(s)

    def curve(self, pts, c=BLUE, w=2.6, dash=None):
        self.add(poly([(self.X(x), self.Y(y)) for x, y in pts], c, w, dash=dash))

    def axes(self, xlabel, ylabel, xticks=(), yticks=()):
        s = line(self.l, self.t - 5, self.l, self.h - self.b, MUTE, 1.3) + line(self.l, self.h - self.b, self.w - self.r + 5, self.h - self.b, MUTE, 1.3)
        for v, lab in xticks:
            s += line(self.X(v), self.h - self.b, self.X(v), self.h - self.b + 5, MUTE, 1.3) + text(self.X(v), self.h - self.b + 18, lab, INK, 12, "middle")
        for v, lab in yticks:
            s += line(self.l - 5, self.Y(v), self.l, self.Y(v), MUTE, 1.3) + text(self.l - 8, self.Y(v) + 4, lab, INK, 12, "end")
        s += text((self.l + self.w - self.r) / 2, self.h - 6, xlabel, INK, 13, "middle")
        s += f'<text x="14" y="{(self.t + self.h - self.b) / 2}" fill="{INK}" font-size="13" text-anchor="middle" transform="rotate(-90 14 {(self.t + self.h - self.b) / 2})">{ylabel}</text>'
        self.parts.insert(0, s)

    def hline(self, y, c=MUTE, dash="4 4", w=1.2):
        self.add(line(self.l, self.Y(y), self.w - self.r, self.Y(y), c, w, dash))

    def vline(self, x, c=MUTE, dash="4 4", w=1.2):
        self.add(line(self.X(x), self.t, self.X(x), self.h - self.b, c, w, dash))

    def band(self, x0, x1, c, op=0.10):
        self.add(f'<rect x="{self.X(x0)}" y="{self.t}" width="{self.X(x1)-self.X(x0)}" height="{self.h-self.t-self.b}" fill="{c}" opacity="{op}"/>')

    def render(self):
        return svg(self.w, self.h, defs(*ALLC) + "".join(self.parts))


# ---------- figures ----------
def fig_bucket():
    """The big picture: bucket + taps next to the real circuit."""
    s = defs(*ALLC)
    # left: bucket analogy
    s += text(150, 22, "The picture", INK, 14, "middle", 700)
    s += poly([(90, 70), (90, 210), (210, 210), (210, 70)], INK, 3)
    s += f'<rect x="92" y="130" width="116" height="78" fill="{BLUE}" opacity="0.25"/>'
    s += line(92, 130, 208, 130, BLUE, 2)
    s += text(150, 175, "charge Q = C·V", BLUE, 12, "middle", 600)
    s += arrow(222, 130, 222, 90, PURPLE, 1.8) + text(228, 108, "height = V", PURPLE, 12)
    s += arrow(150, 222, 208, 222, PURPLE, 1.8) + arrow(150, 222, 92, 222, PURPLE, 1.8) + text(150, 240, "width = C", PURPLE, 12, "middle")
    # top tap
    s += poly([(40, 45), (120, 45), (120, 62)], ORANGE, 6)
    s += arrow(120, 62, 120, 118, ORANGE, 2.5)
    s += text(30, 38, "tap from V_DD = PMOS", ORANGE, 12, "start", 600)
    # bottom drain
    s += poly([(180, 210), (180, 250), (260, 250)], GREEN, 6)
    s += arrow(200, 262, 262, 262, GREEN, 2.5)
    s += text(160, 285, "plug to ground = NMOS", GREEN, 12, "start", 600)
    # right: circuit
    ox = 420
    s += text(ox + 30, 22, "The circuit", INK, 14, "middle", 700)
    s += inverter(ox, 140, ORANGE, GREEN)
    s += line(ox - 60, 140, ox - 30, 140) + text(ox - 64, 145, "V_in", INK, 13, "end")
    s += line(ox + 18, 140, ox + 110, 140) + dot(ox + 110, 140) + text(ox + 116, 135, "V_out", INK, 13)
    s += cap(ox + 80, 140, BLUE, "C_load") + gnd(ox + 80, 180, BLUE)
    s += text(ox + 50, 285, "C_load is the bucket. Its voltage is V_out.", INK, 12, "middle")
    s = s.replace("V_DD", "V<tspan font-size='9' dy='3'>DD</tspan><tspan dy='-3'></tspan>")
    s = s.replace("V_in", "V<tspan font-size='9' dy='3'>in</tspan><tspan dy='-3'></tspan>")
    s = s.replace("V_out", "V<tspan font-size='9' dy='3'>out</tspan><tspan dy='-3'></tspan>")
    s = s.replace("C_load", "C<tspan font-size='9' dy='3'>load</tspan><tspan dy='-3'></tspan>")
    return svg(600, 300, s)


def sub(s):
    """Turn X_ab into X with a subscript inside SVG text."""
    import re
    return re.sub(r"([A-Za-zτ)])_\{([^}]*)\}|([A-Za-zτ)])_([A-Za-z0-9%]+(?:,[A-Za-z]+)?)",
                  lambda m: (m.group(1) or m.group(3)) + "<tspan font-size='9' dy='3'>" + (m.group(2) or m.group(4)) + "</tspan><tspan dy='-3'></tspan>", s)


def fig_load():
    """Inverter 1 driving inverter 2, with every capacitor that sits on Vout."""
    s = defs(*ALLC)
    a, cy = 120, 190
    s += inverter(a, cy)
    s += line(a - 70, cy, a - 30, cy) + text(a - 74, cy + 5, sub("V_in"), INK, 13, "end")
    b = 540
    s += line(a + 18, cy, b - 30, cy, INK)
    s += inverter(b, cy, MUTE, MUTE)
    s += line(b + 18, cy, b + 50, cy, MUTE) + text(b + 54, cy + 5, "next stage", MUTE, 12)

    def hcap(x, y, c, lab, laby):
        return (line(x - 22, y, x - 4, y, c) + line(x - 4, y - 11, x - 4, y + 11, c, 3) + line(x + 4, y - 11, x + 4, y + 11, c, 3)
                + line(x + 4, y, x + 22, y, c) + text(x, laby, sub(lab), c, 13, "middle", 700))
    # Cgd,p: input rail -> over the top -> output
    s += poly([(a - 30, cy - 30), (a - 55, cy - 30), (a - 55, 55), (a - 22, 55)], PURPLE, 1.6) + hcap(a, 55, PURPLE, "C_{gd,p}", 40)
    s += poly([(a + 22, 55), (a + 48, 55), (a + 48, cy)], PURPLE, 1.6)
    # Cgd,n: input rail -> under the bottom -> output
    s += poly([(a - 30, cy + 30), (a - 55, cy + 30), (a - 55, 325), (a - 22, 325)], PURPLE, 1.6) + hcap(a, 325, PURPLE, "C_{gd,n}", 350)
    s += poly([(a + 22, 325), (a + 48, 325), (a + 48, cy)], PURPLE, 1.6)
    s += dot(a + 48, cy, PURPLE, 3.5) + dot(a - 30, cy - 30, PURPLE, 3) + dot(a - 30, cy + 30, PURPLE, 3)
    # Cdb,p up to VDD, Cdb,n down to ground
    x = 215
    s += dot(x, cy) + line(x, cy, x, cy - 20, GREEN) + line(x - 13, cy - 20, x + 13, cy - 20, GREEN, 3) + line(x - 13, cy - 28, x + 13, cy - 28, GREEN, 3) + line(x, cy - 28, x, cy - 60, GREEN) + line(x - 10, cy - 60, x + 10, cy - 60, GREEN, 2.5) + text(x, cy - 67, sub("V_DD"), GREEN, 11, "middle")
    s += text(x + 17, cy - 22, sub("C_{db,p}"), GREEN, 13, "start", 700)
    s += cap(x, cy, GREEN) + gnd(x, cy + 40, GREEN) + text(x + 17, cy + 25, sub("C_{db,n}"), GREEN, 13, "start", 700)
    x = 320
    s += dot(x, cy) + cap(x, cy, AMBER) + gnd(x, cy + 40, AMBER) + text(x + 17, cy + 25, sub("C_{int}"), AMBER, 13, "start", 700) + text(x + 17, cy + 41, "(wire)", AMBER, 11)
    x = 420
    s += dot(x, cy) + cap(x, cy, RED) + gnd(x, cy + 40, RED) + text(x + 17, cy + 25, sub("C_g"), RED, 13, "start", 700) + text(x + 17, cy + 41, "(next gate)", RED, 11)
    s += text(330, 20, "Test: is one plate on " + sub("V_out") + "? → it counts", INK, 13, "middle", 700)
    s += text(330, 385, "All six have one plate on the output node, so every change of the output must fill or empty them.", INK, 12, "middle")
    s += text(330, 403, "This inverter's own " + sub("C_gs") + " sits between " + sub("V_in") + " and a rail → it loads the INPUT, not the output.", MUTE, 12, "middle")
    return svg(660, 412, s)


def fig_two_cases():
    s = defs(*ALLC)
    for i, (title, on, col) in enumerate([("Input steps UP → output FALLS (τ_PHL)", "n", BLUE),
                                         ("Input steps DOWN → output RISES (τ_PLH)", "p", ORANGE)]):
        ox = 110 + i * 320
        cp = ORANGE if on == "p" else "#c3c8d2"
        cn = BLUE if on == "n" else "#c3c8d2"
        s += text(ox + 70, 22, sub(title), col, 13, "middle", 700)
        s += inverter(ox, 150, cp, cn)
        s += line(ox - 60, 150, ox - 30, 150)
        s += text(ox - 64, 145, "V_in:", INK, 12, "end").replace("V_in", sub("V_in"))
        s += text(ox - 64, 160, "0 → V_DD" if on == "n" else "V_DD → 0", INK, 12, "end").replace("V_DD", sub("V_DD"))
        s += line(ox + 18, 150, ox + 110, 150) + dot(ox + 110, 150) + text(ox + 115, 155, sub("V_out"), INK, 13)
        s += cap(ox + 80, 150, INK, sub("C_load")) + gnd(ox + 80, 190)
        if on == "n":
            s += text(ox + 40, 100, "OFF", MUTE, 12, "start", 700)
            s += poly([(ox + 80, 160), (ox + 60, 160), (ox + 60, 200), (ox + 35, 200), (ox + 35, 225)], BLUE, 2.5)
            s += arrow(ox + 35, 215, ox + 35, 232, BLUE, 2.5)
            s += text(ox + 70, 290, "NMOS empties the bucket into ground", BLUE, 12, "middle", 600)
            s += text(ox + 70, 307, sub("V_GS,n = V_DD,  V_DS,n = V_out"), BLUE, 12, "middle")
        else:
            s += text(ox + 40, 210, "OFF", MUTE, 12, "start", 700)
            s += poly([(ox + 35, 75), (ox + 35, 110), (ox + 60, 110), (ox + 60, 140)], ORANGE, 2.5)
            s += arrow(ox + 60, 128, ox + 78, 142, ORANGE, 2.5)
            s += text(ox + 70, 290, sub("PMOS fills the bucket from V_DD"), ORANGE, 12, "middle", 600)
            s += text(ox + 70, 307, sub("|V_GS,p| = V_DD,  |V_DS,p| = V_DD − V_out"), ORANGE, 12, "middle")
    return svg(660, 320, s)


def fig_definitions():
    VDD = 3.3
    sc, base = 0.6, 0.0          # output panel scale
    isc, ibase = 0.28, 2.45      # input panel
    p = Plot(640, 340, (-0.3, 12), (-0.45, 3.5), (64, 14, 14, 30))
    t_up, t_dn = 0.5, 5.0
    fall = discharge(300, 200, 0.6, VDD, VDD, t_dn - t_up, 2e-3)
    rise = discharge(300, 80, 0.7, VDD, VDD, 12 - t_dn, 2e-3)
    tin = [(-0.3, 0), (t_up, 0), (t_up, VDD), (t_dn, VDD), (t_dn, 0), (12, 0)]
    vout = [(-0.3, VDD), (t_up, VDD)] + [(t_up + t, v) for t, v in fall] + [(t_dn + t, VDD - v) for t, v in rise]
    Yi = lambda v: ibase + v * isc
    Yo = lambda v: base + v * sc
    for f, lab in ((0.9, "90%"), (0.5, "50%"), (0.1, "10%")):
        p.add(line(p.X(-0.3), p.Y(Yo(f * VDD)), p.X(12), p.Y(Yo(f * VDD)), MUTE if f == 0.5 else "#d6d9df", 1, "4 4" if f == 0.5 else "2 4"))
        p.add(text(p.X(-0.3) - 6, p.Y(Yo(f * VDD)) + 4, lab, MUTE, 11, "end"))
    p.add(line(p.X(-0.3), p.Y(Yi(VDD / 2)), p.X(12), p.Y(Yi(VDD / 2)), MUTE, 1, "4 4"))
    p.add(text(p.X(-0.3) - 6, p.Y(Yi(VDD / 2)) + 4, "50%", MUTE, 11, "end"))
    p.curve([(x, Yi(y)) for x, y in tin], INK, 2.2)
    p.curve([(x, Yo(y)) for x, y in vout], BLUE, 2.6)
    p.add(text(p.X(-0.3) - 6, p.Y(Yi(VDD)) + 4, sub("V_in"), INK, 13, "end", 700))
    p.add(text(p.X(-0.3) - 6, p.Y(Yo(VDD)) - 6, sub("V_out"), BLUE, 13, "end", 700))
    y50 = p.Y(Yo(VDD / 2))
    for t0, tau, lab in ((t_up, 0.703, "τ_PHL"), (t_dn, 1.882, "τ_PLH")):
        p.add(line(p.X(t0), p.Y(Yi(VDD / 2)), p.X(t0), y50 + 26, PURPLE, 1, "2 3"))
        p.add(line(p.X(t0 + tau), y50, p.X(t0 + tau), y50 + 26, PURPLE, 1, "2 3"))
        p.add(arrow(p.X(t0), y50 + 22, p.X(t0 + tau), y50 + 22, PURPLE, 1.6) + arrow(p.X(t0 + tau), y50 + 22, p.X(t0), y50 + 22, PURPLE, 1.6))
        p.add(text(p.X(t0 + tau) + 5, y50 + 27, sub(lab), PURPLE, 13, "start", 700))
    tf90 = next(t for t, v in fall if v <= 0.9 * VDD); tf10 = next(t for t, v in fall if v <= 0.1 * VDD)
    y = p.Y(Yo(0)) + 16
    p.add(arrow(p.X(t_up + tf90), y, p.X(t_up + tf10), y, ORANGE, 1.6) + arrow(p.X(t_up + tf10), y, p.X(t_up + tf90), y, ORANGE, 1.6))
    p.add(text(p.X(t_up + tf10) + 6, y + 4, sub("t_fall") + " (90%→10%)", ORANGE, 12, "start", 600))
    tr10 = next(t for t, v in rise if VDD - v >= 0.1 * VDD); tr90 = next(t for t, v in rise if VDD - v >= 0.9 * VDD)
    y = p.Y(Yo(VDD)) - 6
    p.add(arrow(p.X(t_dn + tr10), y, p.X(t_dn + tr90), y, GREEN, 1.6) + arrow(p.X(t_dn + tr90), y, p.X(t_dn + tr10), y, GREEN, 1.6))
    p.add(text(p.X(t_dn + tr10), y - 7, sub("t_rise") + " (10%→90%)", GREEN, 12, "start", 600))
    p.add(text(p.X(11.8), p.h - 8, "time →", INK, 12, "end"))
    return p.render()


def fig_journey():
    """Ex 25.2 fall: Vout(t) with saturated and linear segments shaded, plus the average-current straight line."""
    C, k, VT, VDD = 300, 200, 0.6, 3.3
    pts = discharge(C, k, VT, VDD, VDD, 2.4, 1e-3)
    t1 = next(t for t, v in pts if v <= VDD - VT)
    t2 = next(t for t, v in pts if v <= VDD / 2)
    p = Plot(640, 330, (0, 2.4), (0, 3.5), (78, 24, 24, 44))
    p.band(0, t1, BLUE, 0.10); p.band(t1, t2, GREEN, 0.10)
    p.hline(VDD - VT); p.hline(VDD / 2)
    p.curve(pts, BLUE, 2.8)
    Iavg = (729 + 618.75) / 2
    tav = C * 1.65 / Iavg
    p.curve([(0, VDD), (tav, VDD / 2)], ORANGE, 2, "6 4")
    p.axes("time after the input step (ns)", "V_out (V)".replace("V_out", sub("V_out")),
           [(0, "0"), (t1, f"{t1:.3f}"), (t2, f"{t2:.3f}"), (1.5, "1.5"), (2.0, "2.0")],
           [(0, "0"), (VDD / 2, "1.65"), (VDD - VT, "2.7"), (VDD, "3.3")])
    p.add(text(p.X(t1 / 2), p.Y(0.55), "NMOS", BLUE, 12, "middle", 700) + text(p.X(t1 / 2), p.Y(0.35), "SAT", BLUE, 12, "middle", 700))
    p.add(text(p.X((t1 + t2) / 2), p.Y(0.55), "NMOS", GREEN, 12, "middle", 700) + text(p.X((t1 + t2) / 2), p.Y(0.35), "LINEAR", GREEN, 12, "middle", 700))
    p.add(text(p.X(1.25), p.Y(1.45), "segment 1: constant current → straight line", BLUE, 12))
    p.add(text(p.X(1.25), p.Y(1.25), "segment 2: current shrinks → curve bends", GREEN, 12))
    p.add(text(p.X(1.25), p.Y(1.05), "dashed: average-current method (0.734 ns)", ORANGE, 12))
    p.add(dot(p.X(t2), p.Y(VDD / 2), PURPLE, 5))
    p.add(text(p.X(t2) + 8, p.Y(VDD / 2) - 8, sub("τ_PHL = 0.703 ns"), PURPLE, 13, "start", 700))
    p.add(text(p.X(2.38), p.Y(VDD - VT) - 5, sub("V_DD − V_T = 2.7 V: region changes here"), MUTE, 11, "end"))
    p.add(text(p.X(2.38), p.Y(VDD / 2) - 5, "50% point = 1.65 V: stop the clock here", MUTE, 11, "end"))
    return p.render()


def fig_current():
    """NMOS current vs Vout for Ex 25.2, with the two end points and their average."""
    k, u = 200, 2.7
    pts = [(v / 100, i_d(k, u, v / 100)) for v in range(0, 331)]
    p = Plot(600, 300, (0, 3.4), (0, 820), (70, 20, 20, 44))
    p.band(1.65, 3.3, BLUE, 0.08)
    p.curve(pts, BLUE, 2.8)
    p.vline(2.7)
    p.add(line(p.X(1.65), p.Y(673.9), p.X(3.3), p.Y(673.9), ORANGE, 2.2, "6 4"))
    p.add(dot(p.X(3.3), p.Y(729), INK, 5) + dot(p.X(1.65), p.Y(618.75), INK, 5))
    p.axes("V_out (V)    ← during the fall, time runs right-to-left".replace("V_out", sub("V_out")), "i_D,n (µA)".replace("i_D,n", sub("i_{D,n}")),
           [(0, "0"), (1.65, "1.65"), (2.7, "2.7"), (3.3, "3.3")], [(0, "0"), (200, "200"), (400, "400"), (600, "600"), (800, "800")])
    p.add(text(p.X(3.3), p.Y(729) - 12, "start: SAT, 729 µA", INK, 12, "end", 600))
    p.add(text(p.X(1.65) + 8, p.Y(618.75) + 20, "50% point: LINEAR, 618.75 µA", INK, 12, "start", 600))
    p.add(text(p.X(0.1), p.Y(760), "average = (729 + 618.75)/2 = 673.9 µA", ORANGE, 12, "start", 600))
    p.add(text(p.X(2.72), p.Y(80), "linear | sat", MUTE, 11, "middle"))
    return p.render()


def fig_lone_nmos():
    """Q3.4 (discharge, cap on drain) and Q3.5 (follower, cap on source)."""
    s = defs(*ALLC)
    # (b) discharge
    ox = 100
    s += text(ox + 40, 20, "(b) C on the DRAIN: discharge", INK, 13, "middle", 700)
    s += nmos(ox, 140, BLUE)
    s += line(ox - 60, 140, ox - 30, 140) + text(ox - 64, 135, "gate:", INK, 12, "end") + text(ox - 64, 150, "0 → 3 V", INK, 12, "end")
    s += gnd(ox + 18, 175)
    s += line(ox + 18, 105, ox + 18, 80) + line(ox + 18, 80, ox + 90, 80) + dot(ox + 90, 80) + text(ox + 18, 72, "X", INK, 13, "middle", 700)
    s += cap(ox + 90, 80, BLUE, "C₁ = 1 pF") + gnd(ox + 90, 120)
    s += text(ox + 40, 225, "starts at V_X = 1 V".replace("V_X", sub("V_X")), INK, 12, "middle")
    s += text(ox + 40, 242, sub("V_GS = 3 V fixed, V_DS = V_X"), BLUE, 12, "middle")
    # (a) follower
    ox = 420
    s += text(ox + 40, 20, "(a) C on the SOURCE: follower", INK, 13, "middle", 700)
    s += nmos(ox, 120, ORANGE)
    s += line(ox - 60, 120, ox - 30, 120) + text(ox - 64, 115, "gate:", INK, 12, "end") + text(ox - 64, 130, "0 → 3 V", INK, 12, "end")
    s += vdd(ox + 18, 75) + text(ox + 45, 70, "= 3 V", INK, 12)
    s += line(ox + 18, 155, ox + 18, 170) + dot(ox + 18, 170) + text(ox + 2, 175, "X", INK, 13, "end", 700)
    s += cap(ox + 18, 170, ORANGE, "C₁ = 1 pF") + gnd(ox + 18, 210)
    s += text(ox + 40, 252, sub("V_GS = 3 − V_X shrinks as X rises"), ORANGE, 12, "middle")
    return svg(620, 262, s)


def fig_follow_curves():
    k, C = 13430, 1000  # uA/V^2, fF -> ns
    # discharge
    u = 2.3
    d = discharge(C, k, 0.7, 3.0, 1.0, 0.2, 1e-5)
    # follower: dV/dt = k/2 (2.3 - V)^2 / C
    V, t, f = 1.0, 0.0, [(0, 1.0)]
    while t < 1.2:
        V += k / 2 * (2.3 - V) ** 2 / C * 1e-4; t += 1e-4; f.append((t, V))
    p = Plot(600, 280, (0, 1.2), (0, 2.6), (60, 20, 20, 44))
    p.hline(2.3, ORANGE)
    p.curve([(t * 1, v) for t, v in f], ORANGE, 2.6)
    p.curve([(t, v) for t, v in d], BLUE, 2.6)
    p.add(dot(p.X(0.3818), p.Y(2.0), ORANGE, 5) + text(p.X(0.3818) + 8, p.Y(2.0) + 18, "(a) 2.0 V at 0.38 ns", ORANGE, 12, "start", 600))
    p.add(dot(p.X(0.02665), p.Y(0.5), BLUE, 5) + text(p.X(0.02665) + 10, p.Y(0.5) + 4, "(b) 0.5 V at 26.6 ps (very fast)", BLUE, 12, "start", 600))
    p.add(text(p.X(1.18), p.Y(2.3) - 6, "(a) creeps toward 2.3 V, never reaches it", ORANGE, 11, "end"))
    p.axes("time (ns)", sub("V_X (V)"), [(0, "0"), (0.4, "0.4"), (0.8, "0.8"), (1.2, "1.2")], [(0, "0"), (1, "1"), (2, "2"), (2.3, "2.3")])
    return p.render()


def fig_ring():
    s = defs(*ALLC)
    xs = [80, 200, 320, 440, 560]
    for i, x in enumerate(xs):
        s += poly([(x - 25, 60), (x - 25, 110), (x + 20, 85), (x - 25, 60)], INK, 2)
        s += f'<circle cx="{x+25}" cy="85" r="5" fill="white" stroke="{INK}" stroke-width="2"/>'
        s += text(x - 8, 132, f"{i+1}", MUTE, 12, "middle")
        if i < 4:
            s += line(x + 30, 85, xs[i + 1] - 25, 85)
    s += poly([(xs[-1] + 30, 85), (xs[-1] + 60, 85), (xs[-1] + 60, 160), (20, 160), (20, 85), (xs[0] - 25, 85)], ORANGE, 2.2)
    s += arrow(300, 160, 260, 160, ORANGE, 2.2)
    s += text(310, 185, "odd N (here 5): no stable state, so an edge runs round forever", INK, 12, "middle")
    s += text(310, 204, "one period = edge goes round TWICE (once rising, once falling) → T = 2Nτ_P".replace("τ_P", sub("τ_P")), ORANGE, 12, "middle", 600)
    return svg(640, 214, s)


def fig_energy():
    s = defs(*ALLC)
    s += text(160, 22, "Output rises (charging)", ORANGE, 13, "middle", 700)
    s += text(470, 22, "Output falls (discharging)", BLUE, 13, "middle", 700)
    # boxes
    def box(x, y, w, h, c, t1, t2):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{c}" opacity="0.12" stroke="{c}"/>' +
                text(x + w / 2, y + 22, t1, c, 12, "middle", 700) + text(x + w / 2, y + 40, t2, c, 12, "middle"))
    s += box(20, 40, 280, 50, INK, "supply gives Q·V_DD = C·V_DD²".replace("V_DD", sub("V_DD")), "(Q = C·V_DD flows out of V_DD)".replace("V_DD", sub("V_DD")))
    s += arrow(100, 92, 100, 130, ORANGE) + arrow(220, 92, 220, 130, BLUE)
    s += box(20, 132, 150, 55, ORANGE, "½ C V_DD²".replace("V_DD", sub("V_DD")), "burned in PMOS")
    s += box(180, 132, 120, 55, BLUE, "½ C V_DD²".replace("V_DD", sub("V_DD")), "stored in C")
    s += arrow(300, 160, 380, 160, BLUE)
    s += box(380, 132, 180, 55, GREEN, "½ C V_DD²".replace("V_DD", sub("V_DD")), "burned in NMOS")
    s += text(320, 220, "Per full cycle (up and down): energy C·V_DD², power P = C·V_DD²·f".replace("V_DD", sub("V_DD")), INK, 13, "middle", 700)
    return svg(640, 232, s)


def fig_drain():
    """Drain geometry for Cdb: top view."""
    s = defs(*ALLC)
    s += f'<rect x="60" y="40" width="120" height="140" fill="{BLUE}" opacity="0.12" stroke="{BLUE}"/>'
    s += text(120, 115, "source", BLUE, 12, "middle")
    s += f'<rect x="180" y="30" width="26" height="160" fill="{RED}" opacity="0.35" stroke="{RED}"/>'
    s += text(193, 22, "gate (L)", RED, 12, "middle")
    s += f'<rect x="206" y="40" width="110" height="140" fill="{GREEN}" opacity="0.18" stroke="{GREEN}" stroke-width="2.5"/>'
    s += text(261, 115, "drain", GREEN, 13, "middle", 700)
    s += arrow(330, 110, 330, 42, INK, 1.5) + arrow(330, 110, 330, 178, INK, 1.5) + text(338, 114, "W", INK, 13, "start", 700)
    s += arrow(261, 196, 208, 196, INK, 1.5) + arrow(261, 196, 314, 196, INK, 1.5) + text(261, 214, "E", INK, 13, "middle", 700)
    s += text(400, 70, "bottom area = W·E", GREEN, 13, "start", 700)
    s += text(400, 90, "→ times C_j (fF/µm²)".replace("C_j", sub("C_j")), INK, 12)
    s += text(400, 125, "perimeter = 2(W + E)", GREEN, 13, "start", 700)
    s += text(400, 145, "→ times C_jsw (fF/µm)".replace("C_jsw", sub("C_jsw")), INK, 12)
    s += text(400, 185, sub("C_db = W·E·C_j + 2(W+E)·C_jsw"), INK, 13, "start", 700)
    return svg(640, 224, s)


def fig_flow():
    s = defs(*ALLC)
    rows = [
        ("Asks V_IL, V_IH, noise margins, V_th, W_n/W_p for a V_th?", "DC · Lectures 23–24 (refresher R)", "T8 Q1–Q4", PURPLE),
        ("Asks C_load, or gives C_ox, C_j, L_D, C_db …?", "TYPE 1 · Find C_load (B1)", "D Q1, Q2", PURPLE),
        ("Inverter + k, V_T, V_DD, C; asks τ_PHL, τ_PLH, τ_P?", "TYPE 2 · Delay (B4, B5)", "T9 Q2 · D Q3", BLUE),
        ("Asks 10%→90% rise or 90%→10% fall time?", "TYPE 3 · Rise / fall time (B6)", "T9 Q1, Q5b · D Q4", BLUE),
        ("Gives a target delay or V_th and asks W?", "TYPE 4 · Design / sizing (B8)", "T9 Q3, Q4, Q5a · D Q5, Q6", GREEN),
        ("One transistor + one capacitor, odd limits?", "TYPE 5 · Lone MOSFET + C (B7)", "T9 Q3 · D Q7, Q8", ORANGE),
        ("Odd number of inverters in a loop?", "TYPE 6 · Ring oscillator (B9)", "D Q9", AMBER),
        ("Input has a rise/fall time (not a step)?", "Lecture 26 correction (B10)", "B10 example", AMBER),
        ("Asks power or energy?", "TYPE 7 · Dynamic power (B9)", "D Q10", RED),
    ]
    y = 14
    for q, t, where, c in rows:
        s += f'<rect x="6" y="{y}" width="318" height="44" rx="8" fill="#f6f8fb" stroke="#e3e7ee"/>'
        s += text(16, y + 27, sub(q), INK, 11.5)
        s += arrow(326, y + 22, 352, y + 22, c, 2)
        s += f'<rect x="356" y="{y}" width="214" height="44" rx="8" fill="{c}" opacity="0.13" stroke="{c}"/>'
        s += text(366, y + 27, sub(t), c, 11.5, "start", 700)
        s += text(580, y + 27, where, INK, 11.5, "start", 600)
        y += 52
    return svg(740, y, s)




# ---------- tutorial figures ----------
def bis(f, a, b):
    fa = f(a)
    for _ in range(80):
        m = (a + b) / 2; fm = f(m)
        if (fm > 0) == (fa > 0): a, fa = m, fm
        else: b = m
    return (a + b) / 2


def vtc(VDD, Vn, Vp, kn, kp, n=400):
    pts = []
    for i in range(n + 1):
        vi = VDD * i / n
        f = lambda vo: i_d(kp, VDD - vi + Vp, VDD - vo) - i_d(kn, vi - Vn, vo)
        if vi <= Vn:
            vo = VDD
        elif vi >= VDD + Vp:
            vo = 0.0
        else:
            vo = bis(f, 0, VDD)
        pts.append((vi, vo))
    return pts


def fig_t8_vtc():
    VDD = 3.3
    pts = vtc(VDD, 0.6, -0.7, 200, 80)
    p = Plot(600, 380, (0, 3.3), (0, 3.5), (60, 20, 20, 44))
    p.band(1.0645, 1.5533, PURPLE, 0.07)
    p.curve([(0, 0), (3.3, 3.3)], "#c3c8d2", 1.4, "5 4")
    p.curve(pts, BLUE, 2.8)
    for vi, vo, lab, dx, anchor in ((1.0645, 3.1129, "V_IL = 1.06", -8, "end"), (1.5533, 0.2673, "V_IH = 1.55", 8, "start")):
        p.curve([(vi - 0.35, vo + 0.35), (vi + 0.35, vo - 0.35)], ORANGE, 2)
        p.add(dot(p.X(vi), p.Y(vo), ORANGE, 5))
        p.add(text(p.X(vi) + dx, p.Y(vo) + (24 if dx < 0 else -12), sub(lab) + " V", ORANGE, 13, anchor, 700))
    p.add(dot(p.X(1.3749), p.Y(1.3749), PURPLE, 5) + text(p.X(1.3749) + 10, p.Y(1.3749) + 4, sub("V_th = 1.37 V") + " (VTC meets V_out = V_in)".replace("V_out", sub("V_out")).replace("V_in", sub("V_in")), PURPLE, 12, "start", 600))
    p.add(text(p.X(2.25), p.Y(2.6), "orange lines: slope = −1", ORANGE, 12))
    p.add(text(p.X(2.25), p.Y(2.35), "they just touch the VTC at", ORANGE, 12))
    p.add(text(p.X(2.25), p.Y(2.1), sub("V_IL") + " and " + sub("V_IH"), ORANGE, 12))
    p.axes(sub("V_in") + " (V)", sub("V_out") + " (V)", [(0, "0"), (1, "1"), (2, "2"), (3.3, "3.3")], [(0, "0"), (1, "1"), (2, "2"), (3.3, "3.3")])
    return p.render()


def fig_t8_feedback():
    s = defs(*ALLC)
    cx, cy = 260, 215
    s += inverter(cx, cy)
    y = 62                      # M3 channel height
    xl, xr = cx - 90, cx + 100  # left/right legs
    s += line(cx - 30, cy, xl, cy) + line(xl, cy, xl, y)
    s += line(cx + 18, cy, cx + 140, cy) + dot(cx + 140, cy) + text(cx + 148, cy + 5, sub("V_out"), INK, 14, "start", 700)
    s += line(xr, cy, xr, y)
    m = (xl + xr) / 2
    s += line(xl, y, m - 30, y, GREEN) + line(m + 30, y, xr, y, GREEN)
    s += line(m - 30, y, m - 30, y - 8, GREEN) + line(m + 30, y, m + 30, y - 8, GREEN)
    s += line(m - 34, y - 8, m + 34, y - 8, GREEN, 3) + line(m - 30, y - 15, m + 30, y - 15, GREEN, 2) + line(m, y - 15, m, y - 38, GREEN)
    s += line(m - 10, y - 38, m + 10, y - 38, GREEN, 2.5) + text(m + 16, y - 34, "gate = 3.3 V", GREEN, 12)
    s += text(xr + 8, y - 6, "M3 (2/0.8)", GREEN, 13, "start", 700)
    s += dot(xl, cy) + dot(xr, cy)
    s += text(xl - 6, cy + 20, "input", MUTE, 12, "end")
    s += text(m, y + 22, "no current flows through M3", RED, 12, "middle", 600)
    s += text(280, 330, "So V_in = V_out: the inverter must sit where its VTC crosses V_out = V_in, which is V_th".replace("V_in", sub("V_in")).replace("V_out", sub("V_out")).replace("V_th", sub("V_th")), INK, 12, "middle")
    return svg(560, 342, s)


def fig_t8_range():
    s = defs(*ALLC)
    x0, x1, v0, v1 = 60, 560, 1.25, 1.55
    X = lambda v: x0 + (v - v0) / (v1 - v0) * (x1 - x0)
    s += line(x0, 70, x1, 70, MUTE, 2)
    for v in (1.25, 1.30, 1.35, 1.40, 1.45, 1.50, 1.55):
        s += line(X(v), 64, X(v), 76, MUTE, 1.5) + text(X(v), 96, f"{v:.2f}", INK, 12, "middle")
    s += f'<rect x="{X(1.290)}" y="58" width="{X(1.510)-X(1.290)}" height="24" rx="6" fill="{PURPLE}" opacity="0.18"/>'
    s += dot(X(1.290), 70, BLUE, 6) + dot(X(1.40), 70, INK, 6) + dot(X(1.510), 70, ORANGE, 6)
    s += text(X(1.290), 40, "min 1.29 V", BLUE, 13, "middle", 700) + text(X(1.40), 40, "nominal 1.40 V", INK, 13, "middle", 700) + text(X(1.510), 40, "max 1.51 V", ORANGE, 13, "middle", 700)
    s += text(X(1.290), 122, sub("V_T0,n") + " low, " + sub("|V_T0,p|") + " high", BLUE, 12, "middle")
    s += text(X(1.510), 122, sub("V_T0,n") + " high, " + sub("|V_T0,p|") + " low", ORANGE, 12, "middle")
    s += text(310, 148, "(switching threshold in volts)", MUTE, 12, "middle")
    return svg(620, 156, s)


def fig_t9q1():
    C, k, VT, VDD = 1000, 200, 1.0, 5.0
    pts = discharge(C, k, VT, VDD, 4.5, 6.0, 1e-3)
    p = Plot(620, 330, (0, 6), (0, 5.2), (60, 20, 20, 44))
    p.band(0, 0.3125, BLUE, 0.12); p.band(0.3125, 3.6976, GREEN, 0.09)
    for v in (4.5, 4.0, 0.5):
        p.hline(v)
    p.curve(pts, BLUE, 2.8)
    p.curve([(0, 4.5), (4.0506, 0.5)], ORANGE, 2, "6 4")
    p.add(dot(p.X(3.6976), p.Y(0.5), PURPLE, 5) + text(p.X(3.6), p.Y(0.12), "exact: 3.70 ns", PURPLE, 13, "end", 700))
    p.add(dot(p.X(4.0506), p.Y(0.5), ORANGE, 5) + text(p.X(4.15), p.Y(1.25), "average: 4.05 ns", ORANGE, 13, "start", 700))
    p.add(text(p.X(0.16), p.Y(4.85), "SAT", BLUE, 11, "middle", 700))
    p.add(text(p.X(2.0), p.Y(4.85), "LINEAR (4 V → 0.5 V)", GREEN, 12, "middle", 700))
    p.add(text(p.X(5.9), p.Y(4.0) + 16, sub("V_DD − V_T = 4 V: region changes"), MUTE, 11, "end"))
    p.axes("time after the input step (ns)", sub("V_out") + " (V)", [(0, "0"), (0.3125, "0.31"), (2, "2"), (4, "4"), (6, "6")], [(0, "0"), (0.5, "0.5"), (4.0, "4"), (4.5, "4.5")])
    return p.render()


def fig_t9q2():
    k, u = 640, 2.5
    p = Plot(560, 300, (0, 3.5), (0, 2.3), (60, 20, 20, 44))
    p.curve([(v / 100, i_d(k, u, v / 100) / 1000) for v in range(0, 351)], BLUE, 2.8)
    p.vline(2.5); p.hline(2.0)
    p.add(dot(p.X(2.5), p.Y(2.0), ORANGE, 5))
    p.add(text(p.X(2.6), p.Y(1.55), "corner:", ORANGE, 12, "start", 700) + text(p.X(2.6), p.Y(1.37), sub("V_DS") + " = 2.5 V", ORANGE, 12, "start", 700) + text(p.X(2.6), p.Y(1.19), "I = 2 mA", ORANGE, 12, "start", 700))
    p.add(text(p.X(0.3), p.Y(2.15), "linear", GREEN, 12, "start", 600) + text(p.X(2.9), p.Y(2.15), "saturation", BLUE, 12, "start", 600))
    p.add(text(p.X(1.25), p.Y(0.6), "corner sits at V_DS = V_GS − V_T".replace("V_DS", sub("V_DS")).replace("V_GS", sub("V_GS")).replace("V_T", sub("V_T")), INK, 12, "middle"))
    p.add(text(p.X(1.25), p.Y(0.4), "→ 3.3 − V_T = 2.5 → V_T = 0.8 V".replace("V_T", sub("V_T")), INK, 12, "middle", 700))
    p.axes(sub("V_DS") + " (V), with " + sub("V_GS") + " = 3.3 V", sub("I_D") + " (mA)", [(0, "0"), (1, "1"), (2.5, "2.5"), (3.3, "3.3")], [(0, "0"), (1, "1"), (2, "2")])
    return p.render()


def fig_t9q3():
    s = defs(*ALLC)
    x0, x1, v0, v1 = 50, 590, 600, 1000
    X = lambda v: x0 + (v - v0) / (v1 - v0) * (x1 - x0)
    rows = [(729.3, "fall 2 V → 0.5 V in 0.35 ns", GREEN), (770.8, "τ_PLH ≤ 0.15 ns (via k_p = k_n / 0.51)", ORANGE), (945.4, "τ_PHL ≤ 0.2 ns", BLUE)]
    y = 30
    for v, lab, c in rows:
        s += f'<rect x="{X(v)}" y="{y}" width="{x1-X(v)}" height="22" rx="5" fill="{c}" opacity="0.18"/>'
        s += line(X(v), y - 4, X(v), y + 26, c, 2.5) + text(X(v) - 8, y + 16, sub(lab) + f"  → k_n ≥ {v:.0f}".replace("k_n", sub("k_n")).replace("k_p", sub("k_p")), c, 12, "end", 600)
        y += 40
    s += line(x0, y + 10, x1, y + 10, MUTE, 1.5)
    for v in (600, 700, 800, 900, 1000):
        s += line(X(v), y + 5, X(v), y + 15, MUTE, 1.5) + text(X(v), y + 32, str(v), INK, 12, "middle")
    s += text((x0 + x1) / 2, y + 52, sub("k_n") + " (µA/V²)  — the strictest rule wins: " + sub("k_n") + " ≥ 945 µA/V²", INK, 13, "middle", 700)
    return svg(640, y + 62, s)


def fig_t9q5():
    from math import log
    B = 2 * 0.8 / 4.2 + log(4 * 4.2 / 5 - 1)
    f = lambda W: (680 + 26.5 * W) / (50 * W * 4.2) * B
    p = Plot(580, 300, (1, 14), (0, 3.4), (60, 20, 20, 44))
    p.hline(0.825, RED)
    p.curve([(W / 10, f(W / 10)) for W in range(10, 141)], BLUE, 2.8)
    p.hline(B * 26.5 / 210, MUTE, "2 4")
    p.add(dot(p.X(6.0), p.Y(0.825), RED, 5) + text(p.X(6.0) + 8, p.Y(0.825) - 10, sub("W_n") + " = 6.0 µm", RED, 13, "start", 700))
    p.add(text(p.X(13.9), p.Y(0.825) + 16, "target 0.825 ns", RED, 12, "end"))
    p.add(text(p.X(13.9), p.Y(B * 26.5 / 210) - 6, "floor 0.156 ns: a wider transistor also adds C", MUTE, 11, "end"))
    p.add(text(p.X(3.0), p.Y(2.8), "small W: weak tap → slow", BLUE, 12, "start", 600))
    p.axes(sub("W_n") + " (µm)   [with " + sub("W_p") + " = 2.5 " + sub("W_n") + "]", sub("τ_PHL") + " (ns)", [(2, "2"), (6, "6"), (10, "10"), (14, "14")], [(0, "0"), (0.825, "0.825"), (2, "2"), (3, "3")])
    return p.render()


def fig_slope():
    s = defs(*ALLC)
    s += text(160, 20, "Ideal step input (lecture formulas)", INK, 12, "middle", 700)
    s += poly([(40, 120), (90, 120), (90, 40), (280, 40)], INK, 2.4)
    s += text(480, 20, "Real input with rise time τ_r".replace("τ_r", sub("τ_r")), INK, 12, "middle", 700)
    s += poly([(360, 120), (420, 120), (500, 40), (600, 40)], INK, 2.4)
    s += arrow(420, 140, 500, 140, ORANGE, 1.6) + arrow(500, 140, 420, 140, ORANGE, 1.6) + text(460, 158, sub("τ_r"), ORANGE, 13, "middle", 700)
    s += text(320, 190, "A slow input turns the transistor on gradually, so the output starts later → the delay grows.", INK, 12, "middle")
    return svg(640, 200, s)




# ---------- one figure per question ----------
def barh(rows, unit, w=620, title=None, maxv=None):
    """Horizontal bar chart. rows = [(label, value, colour)]."""
    s = defs(*ALLC)
    lx, bx, bw = 215, 225, w - 310
    maxv = maxv or max(v for _, v, _ in rows)
    y = 34 if title else 12
    if title:
        s += text(w / 2, 20, title, INK, 13, "middle", 700)
    for lab, v, c in rows:
        s += text(lx, y + 16, sub(lab), INK, 12.5, "end")
        s += f'<rect x="{bx}" y="{y}" width="{max(2, v / maxv * bw):.1f}" height="22" rx="4" fill="{c}" opacity="0.85"/>'
        s += text(bx + v / maxv * bw + 8, y + 16, f"{v:g} {unit}", c, 12.5, "start", 700)
        y += 32
    return svg(w, y + 6, s)


def fig_t8q1_regions():
    s = defs(*ALLC)
    for i, (title, pc, nc, plab, nlab, vin, vout) in enumerate([
            ("At V_IL = 1.06 V (output still high, 3.11 V)", ORANGE, BLUE, "PMOS: LINEAR (fully on)", "NMOS: SAT (just on)", "1.06 V", "3.11 V"),
            ("At V_IH = 1.55 V (output nearly low, 0.27 V)", ORANGE, BLUE, "PMOS: SAT (nearly off)", "NMOS: LINEAR (fully on)", "1.55 V", "0.27 V")]):
        ox = 110 + i * 320
        s += text(ox + 70, 22, sub(title), INK, 12.5, "middle", 700)
        s += inverter(ox, 150, pc, nc)
        s += line(ox - 60, 150, ox - 30, 150) + text(ox - 64, 155, vin, INK, 12, "end", 600)
        s += line(ox + 18, 150, ox + 70, 150) + dot(ox + 70, 150) + text(ox + 76, 155, vout, INK, 12, "start", 600)
        s += text(ox + 50, 104, plab, ORANGE, 12, "start", 700)
        s += text(ox + 50, 204, nlab, BLUE, 12, "start", 700)
    s += text(320, 270, "Same equations every time: currents equal + slope dV_out/dV_in = −1".replace("V_out", sub("V_out")).replace("V_in", sub("V_in")), INK, 12.5, "middle")
    return svg(660, 282, s)


def fig_t8q2_vtc():
    VDD = 3.3
    pts = vtc(VDD, 0.6, -0.7, 480, 300)
    p = Plot(600, 360, (0, 3.3), (0, 3.5), (60, 20, 20, 44))
    p.band(1.1985, 1.6958, PURPLE, 0.07)
    p.curve([(0, 0), (3.3, 3.3)], "#c3c8d2", 1.4, "5 4")
    p.curve(pts, BLUE, 2.8)
    for vi, vo, lab, dx, anchor in ((1.1985, 3.078, "V_IL = 1.20", -8, "end"), (1.6958, 0.2653, "V_IH = 1.70", 8, "start")):
        p.curve([(vi - 0.35, vo + 0.35), (vi + 0.35, vo - 0.35)], ORANGE, 2)
        p.add(dot(p.X(vi), p.Y(vo), ORANGE, 5))
        p.add(text(p.X(vi) + dx, p.Y(vo) + (24 if dx < 0 else -12), sub(lab) + " V", ORANGE, 13, anchor, 700))
    p.add(dot(p.X(1.483), p.Y(1.483), PURPLE, 5) + text(p.X(1.483) + 10, p.Y(1.483) + 4, sub("V_th = 1.48 V"), PURPLE, 13, "start", 700))
    p.add(text(p.X(2.2), p.Y(2.6), "k_R = 1.6 (closer to 1 than Q1)".replace("k_R", sub("k_R")), INK, 12))
    p.add(text(p.X(2.2), p.Y(2.35), "→ V_th closer to the middle".replace("V_th", sub("V_th")), INK, 12))
    p.axes(sub("V_in") + " (V)", sub("V_out") + " (V)", [(0, "0"), (1, "1"), (2, "2"), (3.3, "3.3")], [(0, "0"), (1, "1"), (2, "2"), (3.3, "3.3")])
    return p.render()


def fig_t8q3_tug():
    s = defs(*ALLC)
    s += text(320, 22, "Tug-of-war at the switching point: both transistors saturated, currents equal", INK, 12.5, "middle", 700)
    s += f'<rect x="60" y="50" width="200" height="56" rx="10" fill="{BLUE}" opacity="0.13" stroke="{BLUE}"/>'
    s += text(160, 74, "NMOS pulls output DOWN", BLUE, 12.5, "middle", 700) + text(160, 94, sub("k_n ∝ 60·W_n"), BLUE, 12, "middle")
    s += f'<rect x="380" y="50" width="200" height="56" rx="10" fill="{ORANGE}" opacity="0.13" stroke="{ORANGE}"/>'
    s += text(480, 74, "PMOS pulls output UP", ORANGE, 12.5, "middle", 700) + text(480, 94, sub("k_p ∝ 25·W_p"), ORANGE, 12, "middle")
    s += arrow(300, 78, 264, 78, BLUE, 3) + arrow(340, 78, 376, 78, ORANGE, 3) + dot(320, 78, INK, 6)
    s += text(320, 140, "Want V_th = 1.4 V (below the middle, 1.65 V) → the NMOS must win a little → k_R = 2.25".replace("V_th", sub("V_th")).replace("k_R", sub("k_R")), INK, 12.5, "middle")
    s += text(320, 162, "A weaker part (higher |V_T|) loses the tug-of-war → V_th moves toward it", MUTE, 12, "middle")
    return svg(640, 172, s)


def rise_pts(C, kp, VT, VDD, t_end, dt=2e-3):
    return [(t, VDD - v) for t, v in discharge(C, kp, VT, VDD, VDD, t_end, dt)]


def fig_t9q4():
    kp = 295.805
    p = Plot(640, 320, (0, 12), (0, 5.3), (92, 20, 20, 44))
    r5 = rise_pts(2000, kp, 1.0, 5.0, 12, 5e-3)
    r3 = rise_pts(2000, kp, 1.0, 3.3, 12, 5e-3)
    p.curve(r3, MUTE, 2.2, "6 4")
    p.curve(r5, ORANGE, 2.8)
    t10 = next(t for t, v in r5 if v >= 0.5); t90 = next(t for t, v in r5 if v >= 4.5)
    p.hline(0.5); p.hline(4.5)
    p.add(dot(p.X(t10), p.Y(0.5), ORANGE, 5) + dot(p.X(t90), p.Y(4.5), ORANGE, 5))
    y = p.Y(2.6)
    p.add(arrow(p.X(t10), y, p.X(t90), y, ORANGE, 1.8) + arrow(p.X(t90), y, p.X(t10), y, ORANGE, 1.8))
    p.add(text(p.X(5.6), p.Y(1.7), sub("τ_rise") + " = 5.0 ns → " + sub("W_p") + " = 14.8 µm", ORANGE, 13, "start", 700))
    p.add(text(p.X(11.8), p.Y(0.9), "dashed: same inverter at V_DD = 3.3 V (slower)".replace("V_DD", sub("V_DD")), MUTE, 12, "end"))
    p.axes("time after the input steps down (ns)", sub("V_out") + " (V)", [(0, "0"), (t10, f"{t10:.2f}"), (t90, f"{t90:.2f}"), (8, "8"), (12, "12")], [(0, "0"), (0.5, "0.5 (10%)"), (3.3, "3.3"), (4.5, "4.5 (90%)")])
    return p.render()


def fig_dq1():
    return barh([("C_g (next gate)", 6.65, RED), ("C_int (wire)", 5, AMBER), ("C_db,p", 4, GREEN), ("C_db,n", 2, GREEN),
                 ("C_gd,p", 0.76, PURPLE), ("C_gd,n", 0.304, PURPLE)], "fF", title="The six pieces of C_load = 18.7 fF".replace("C_load", sub("C_load")))


def fig_dq2():
    return barh([("C_g (next gate)", 28.8, RED), ("C_db,p", 14.84, GREEN), ("C_db,n", 4.66, GREEN),
                 ("C_gd,p", 3.0, PURPLE), ("C_gd,n", 2.0, PURPLE)], "fF", title="The pieces of C_load = 53.3 fF (no wire here)".replace("C_load", sub("C_load")))


def fig_dq3():
    VDD = 3.3
    f = discharge(300, 200, 0.6, VDD, VDD, 4, 2e-3)
    r = rise_pts(300, 80, 0.7, VDD, 4)
    p = Plot(640, 320, (0, 4), (0, 3.5), (92, 20, 20, 44))
    p.hline(1.65)
    p.curve(f, BLUE, 2.8); p.curve(r, ORANGE, 2.8)
    p.add(dot(p.X(0.703), p.Y(1.65), BLUE, 5) + text(p.X(0.703) - 8, p.Y(1.65) + 22, sub("τ_PHL") + " = 0.703 ns", BLUE, 13, "end", 700))
    p.add(dot(p.X(1.882), p.Y(1.65), ORANGE, 5) + text(p.X(1.882) + 10, p.Y(1.65) + 22, sub("τ_PLH") + " = 1.88 ns", ORANGE, 13, "start", 700))
    p.add(text(p.X(3.9), p.Y(0.35), "fall (NMOS, k = 200)", BLUE, 12, "end", 600))
    p.add(text(p.X(3.9), p.Y(3.0), "rise (PMOS, k = 80): slower", ORANGE, 12, "end", 600))
    p.axes("time after the input step (ns)", sub("V_out") + " (V)", [(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4")], [(0, "0"), (1.65, "1.65 (50%)"), (3.3, "3.3")])
    return p.render()


def fig_dq4():
    VDD = 3.3
    f = discharge(300, 200, 0.6, VDD, VDD, 7, 2e-3)
    r = rise_pts(300, 80, 0.7, VDD, 7)
    p = Plot(640, 320, (0, 7), (0, 3.5), (92, 20, 20, 44))
    p.hline(0.33); p.hline(2.97)
    p.curve(f, BLUE, 2.8); p.curve(r, ORANGE, 2.8)
    f90 = next(t for t, v in f if v <= 2.97); f10 = next(t for t, v in f if v <= 0.33)
    r10 = next(t for t, v in r if v >= 0.33); r90 = next(t for t, v in r if v >= 2.97)
    for a, b, y, c, lab in ((f90, f10, 1.2, BLUE, "t_fall = 1.63 ns"), (r10, r90, 2.2, ORANGE, "t_rise = 4.29 ns")):
        p.add(arrow(p.X(a), p.Y(y), p.X(b), p.Y(y), c, 1.8) + arrow(p.X(b), p.Y(y), p.X(a), p.Y(y), c, 1.8))
        p.add(text(p.X(b) + 8, p.Y(y) + 4, sub(lab), c, 13, "start", 700))
        p.add(line(p.X(a), p.Y(y) - 8, p.X(a), p.Y(y) + 8, c, 1.5) + line(p.X(b), p.Y(y) - 8, p.X(b), p.Y(y) + 8, c, 1.5))
    p.axes("time after the input step (ns)", sub("V_out") + " (V)", [(0, "0"), (2, "2"), (4, "4"), (6, "6")], [(0, "0"), (0.33, "0.33 (10%)"), (2.97, "2.97 (90%)")])
    return p.render()


def fig_dq5():
    from math import log
    Bn = 2 * 0.6 / 2.7 + log(4 * 2.7 / 3.3 - 1); Bp = 2 * 0.7 / 2.6 + log(4 * 2.6 / 3.3 - 1)
    tn = lambda wl: 200 / (100 * wl * 2.7) * Bn
    tp = lambda wl: 200 / (40 * wl * 2.6) * Bp
    p = Plot(600, 320, (0.5, 8), (0, 2.2), (60, 20, 20, 44))
    p.hline(0.5, RED)
    p.curve([(w / 20, tn(w / 20)) for w in range(10, 161)], BLUE, 2.8)
    p.curve([(w / 20, tp(w / 20)) for w in range(16, 161)], ORANGE, 2.8)
    p.add(dot(p.X(1.875), p.Y(0.5), BLUE, 5) + text(p.X(1.875), p.Y(0.5) + 22, sub("(W/L)_n") + " = 1.87", BLUE, 13, "middle", 700))
    p.add(dot(p.X(5.018), p.Y(0.5), ORANGE, 5) + text(p.X(5.018), p.Y(0.5) + 22, sub("(W/L)_p") + " = 5.02", ORANGE, 13, "middle", 700))
    p.add(text(p.X(7.9), p.Y(0.5) - 8, "target 0.5 ns", RED, 12, "end"))
    p.add(text(p.X(1.6), p.Y(1.9), sub("τ_PLH") + " (PMOS, weaker per µm)", ORANGE, 12, "start", 600))
    p.add(text(p.X(3.0), p.Y(0.13), sub("τ_PHL") + " (NMOS)", BLUE, 12, "start", 600))
    p.axes("W/L", "delay (ns)", [(1, "1"), (2, "2"), (4, "4"), (6, "6"), (8, "8")], [(0, "0"), (0.5, "0.5"), (1, "1"), (2, "2")])
    return p.render()


def fig_dq6():
    return barh([("τ_PHL (NMOS, fixed)", 0.703, BLUE), ("τ_PLH, k_p = 80", 1.882, ORANGE), ("τ_PLH, k_p = 200 (×2.5)", 0.753, ORANGE),
                 ("τ_PLH, k_p = 214 (×2.68)", 0.703, GREEN)], "ns", w=640, title="Widening the PMOS until its edge matches the NMOS edge")


def fig_dq9():
    s = defs(*ALLC)
    tp, x0, sc = 1, 110, 50   # one τ_P = 50 px
    s += text(320, 20, "Nodes of a 5-stage ring: each node flips one τ_P after the one before it".replace("τ_P", sub("τ_P")), INK, 12.5, "middle", 700)
    for n in range(3):
        y = 50 + n * 54
        s += text(x0 - 12, y + 22, f"node {n+1}", INK, 12, "end", 600)
        pts = []
        lvl = (n % 2 == 0)
        t = n
        pts.append((x0, y + (6 if lvl else 34)))
        cur = lvl
        for k in range(12):
            edge = n + 5 * k
            if edge > 10:
                break
            xe = x0 + edge * sc / 1.0 * 0.95
            pts += [(xe, y + (6 if cur else 34)), (xe, y + (34 if cur else 6))]
            cur = not cur
        pts.append((x0 + 10.5 * sc * 0.95, y + (6 if cur else 34)))
        s += poly(pts, [BLUE, ORANGE, GREEN][n], 2.4)
    xa, xb = x0, x0 + 10 * sc * 0.95
    s += arrow(xa, 222, xb, 222, PURPLE, 1.8) + arrow(xb, 222, xa, 222, PURPLE, 1.8)
    s += text((xa + xb) / 2, 242, "period T = 2 × 5 × τ_P = 10 τ_P (node 1 rises, falls, rises again)".replace("τ_P", sub("τ_P")), PURPLE, 12.5, "middle", 700)
    return svg(660, 252, s)


def fig_dq10():
    return barh([("supply gives C·V_DD²", 450, INK), ("burned in PMOS (charging)", 225, ORANGE), ("burned in NMOS (discharging)", 225, GREEN)],
                "fJ", w=640, title="Energy per cycle at 50 fF and 3 V   (× 1 GHz → 0.45 mW)")


def fig_capstone():
    VDD = 2.5
    a = vtc(VDD, 0.5, -0.5, 300, 150)
    b = vtc(VDD, 0.5, -0.5, 300, 300)
    p = Plot(600, 340, (0, 2.5), (0, 2.7), (60, 20, 20, 44))
    p.curve([(0, 0), (2.5, 2.5)], "#c3c8d2", 1.4, "5 4")
    p.curve(b, GREEN, 2.4, "7 4")
    p.curve(a, BLUE, 2.8)
    p.add(dot(p.X(1.121), p.Y(1.121), BLUE, 5) + text(p.X(1.121) - 10, p.Y(1.121) + 4, sub("V_th") + " = 1.12 V (k_p = 150)".replace("k_p", sub("k_p")), BLUE, 12.5, "end", 700))
    p.add(dot(p.X(1.25), p.Y(1.25), GREEN, 5) + text(p.X(1.25) + 10, p.Y(1.25) + 4, sub("V_th") + " = 1.25 V after doubling (W/L)_p".replace("(W/L)_p", sub("(W/L)_p")), GREEN, 12.5, "start", 700))
    p.axes(sub("V_in") + " (V)", sub("V_out") + " (V)", [(0, "0"), (1.25, "1.25"), (2.5, "2.5")], [(0, "0"), (1.25, "1.25"), (2.5, "2.5")])
    return p.render()




def fig_master():
    s = defs(*ALLC)
    x0, x1 = 60, 600
    X = lambda v: x0 + v / 3.3 * (x1 - x0)
    y = 90
    s += text(330, 22, "x = |V_DS| of the driving transistor = distance of V_out from that transistor's rail".replace("V_DS", sub("V_DS")).replace("V_out", sub("V_out")), INK, 12.5, "middle", 700)
    s += f'<rect x="{X(0)}" y="{y-14}" width="{X(2.7)-X(0)}" height="28" fill="{GREEN}" opacity="0.13"/>'
    s += f'<rect x="{X(2.7)}" y="{y-14}" width="{X(3.3)-X(2.7)}" height="28" fill="{BLUE}" opacity="0.15"/>'
    s += line(x0, y + 14, x1, y + 14, INK, 2)
    s += text(X(1.35), y + 5, "LINEAR  (x < u)", GREEN, 12.5, "middle", 700) + text(X(3.0), y + 5, "SAT", BLUE, 12.5, "middle", 700)
    for v, lab in ((0, "0"), (2.7, "u"), (3.3, "V_DD")):
        s += line(X(v), y - 20, X(v), y + 20, INK, 1.5) + text(X(v), y + 38, sub(lab), INK, 13, "middle", 700)
    s += text(X(2.7), y - 26, "boundary: x = u = V_GS − |V_T|".replace("V_GS", sub("V_GS")).replace("V_T", sub("V_T")), MUTE, 12, "middle")
    # start/end markers
    s += arrow(X(3.3), y + 62, X(1.65), y + 62, PURPLE, 2.2) + text(X(1.65) - 6, y + 66, "x shrinks from x_i to x_f".replace("x_i", sub("x_i")).replace("x_f", sub("x_f")), PURPLE, 12.5, "end", 700)
    s += text(330, y + 98, "Cut the trip at x = u. Time the SAT piece with the bucket formula, the LINEAR piece with the ln formula, add.", INK, 12.5, "middle")
    return svg(660, y + 110, s)




def fig_ring3():
    s = defs(*ALLC)
    xs = [120, 300, 480]
    for i, x in enumerate(xs):
        s += poly([(x - 25, 60), (x - 25, 110), (x + 20, 85), (x - 25, 60)], INK, 2)
        s += f'<circle cx="{x+25}" cy="85" r="5" fill="white" stroke="{INK}" stroke-width="2"/>'
        s += text(x - 8, 50, str(i + 1), MUTE, 12, "middle")
        nx = x + 75
        s += line(x + 30, 85, (xs[i + 1] - 25) if i < 2 else x + 110, 85)
        s += dot(nx, 85) + cap(nx, 85, [BLUE, ORANGE, GREEN][i], sub(f"C_{i+1}")) + gnd(nx, 125, [BLUE, ORANGE, GREEN][i])
    s += poly([(xs[-1] + 110, 85), (xs[-1] + 110, 25), (60, 25), (60, 85), (xs[0] - 25, 85)], ORANGE, 2.2)
    s += arrow(300, 25, 260, 25, ORANGE, 2.2)
    s += text(320, 178, "Each stage charges and discharges its own capacitor: bigger C_i → that stage is slower".replace("C_i", sub("C_i")), INK, 12.5, "middle")
    s += text(320, 198, "T = Σ (τ_PHL,i + τ_PLH,i)".replace("τ_PHL,i", sub("τ_{PHL,i}")).replace("τ_PLH,i", sub("τ_{PLH,i}")), ORANGE, 13, "middle", 700)
    return svg(640, 208, s)


FIGS = {
    "FIG_BUCKET": fig_bucket, "FIG_LOAD": fig_load, "FIG_TWO": fig_two_cases, "FIG_DEF": fig_definitions,
    "FIG_JOURNEY": fig_journey, "FIG_CURRENT": fig_current, "FIG_LONE": fig_lone_nmos, "FIG_LONECURVES": fig_follow_curves,
    "FIG_RING": fig_ring, "FIG_T8VTC": fig_t8_vtc, "FIG_T8FB": fig_t8_feedback, "FIG_T8RANGE": fig_t8_range, "FIG_T9Q1": fig_t9q1, "FIG_T9Q2": fig_t9q2, "FIG_T9Q3": fig_t9q3, "FIG_T9Q5": fig_t9q5, "FIG_SLOPE": fig_slope, "FIG_MASTER": fig_master, "FIG_RING3": fig_ring3, "FIG_T8Q1": fig_t8q1_regions, "FIG_T8Q2": fig_t8q2_vtc, "FIG_T8Q3": fig_t8q3_tug, "FIG_T9Q4": fig_t9q4, "FIG_DQ1": fig_dq1, "FIG_DQ2": fig_dq2, "FIG_DQ3": fig_dq3, "FIG_DQ4": fig_dq4, "FIG_DQ5": fig_dq5, "FIG_DQ6": fig_dq6, "FIG_DQ9": fig_dq9, "FIG_DQ10": fig_dq10, "FIG_CAP": fig_capstone, "FIG_ENERGY": fig_energy, "FIG_DRAIN": fig_drain, "FIG_FLOW": fig_flow,
}

if __name__ == "__main__":
    src = open(os.path.join(HERE, "guide_src.html"), encoding="utf-8").read()
    for key, fn in FIGS.items():
        src = src.replace("{{" + key + "}}", fn())
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "Lecture25_Guide.html")
    open(out, "w", encoding="utf-8").write(src)
    print("wrote", out)
