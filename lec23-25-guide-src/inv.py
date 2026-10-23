"""CMOS inverter model (long-channel square law, lambda = gamma = 0), Kang & Leblebici notation.
kn = un*Cox*(W/L)n, kp = up*Cox*(W/L)p, VT0p is negative, kR = kn/kp."""
import math
import numpy as np


def idn(vin, vout, kn, vtn):
    vgs, vds = vin, vout
    if vgs <= vtn:
        return 0.0
    ov = vgs - vtn
    if vds >= ov:
        return kn / 2 * ov * ov
    return kn / 2 * (2 * ov * vds - vds * vds)


def idp(vin, vout, kp, vtp, vdd):
    """current flowing from VDD into the output (positive)."""
    vsg, vsd, vt = vdd - vin, vdd - vout, -vtp
    if vsg <= vt:
        return 0.0
    ov = vsg - vt
    if vsd >= ov:
        return kp / 2 * ov * ov
    return kp / 2 * (2 * ov * vsd - vsd * vsd)


def vout_of(vin, p):
    """solve idn = idp by bisection for Vout in [0, VDD]."""
    vdd, kn, kp, vtn, vtp = p['vdd'], p['kn'], p['kp'], p['vtn'], p['vtp']
    lo, hi = 0.0, vdd
    f = lambda v: idp(vin, v, kp, vtp, vdd) - idn(vin, v, kn, vtn)
    if f(hi) >= 0 and f(lo) >= 0 and idn(vin, 0.0, kn, vtn) == 0:
        return vdd
    for _ in range(200):
        m = 0.5 * (lo + hi)
        if f(m) > 0:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


def vth(p):
    kr = p['kn'] / p['kp']
    r = 1 / math.sqrt(kr)
    return (p['vtn'] + r * (p['vdd'] + p['vtp'])) / (1 + r)


def rho_il(kr):
    return (-kr + 2 * math.sqrt(kr * (kr + 3))) / (kr * (kr + 4))


def rho_ih(kr):
    return (1 + 2 * math.sqrt(1 + 3 * kr)) / (3 * kr)


def vil(p):
    kr = p['kn'] / p['kp']
    r = rho_il(kr)
    v = (p['vtn'] + r * (p['vdd'] + p['vtp'])) / (1 + r)
    vo = 0.5 * ((1 + kr) * v + p['vdd'] - p['vtp'] - kr * p['vtn'])
    return v, vo


def vih(p):
    kr = p['kn'] / p['kp']
    s = rho_ih(kr)
    v = (p['vtn'] + s * (p['vdd'] + p['vtp'])) / (1 + s)
    vo = (kr * (v - p['vtn']) - (p['vdd'] - v + p['vtp'])) / (2 * kr)
    return v, vo


def summary(p):
    a, ao = vil(p)
    b, bo = vih(p)
    t = vth(p)
    return dict(kr=p['kn'] / p['kp'], vth=t, vil=a, vout_il=ao, vih=b, vout_ih=bo,
                nml=a, nmh=p['vdd'] - b)


def vth_target_kr(vthv, p):
    return ((p['vdd'] + p['vtp'] - vthv) / (vthv - p['vtn'])) ** 2


# ---------- delays (step input, state-equation / exact) ----------
def tphl(c, kn, vtn, voh, vol):
    a = voh - vtn
    v50 = (voh + vol) / 2
    t_sat = 2 * c * vtn / (kn * a * a)
    t_lin = c / (kn * a) * math.log(4 * a / (voh + vol) - 1)
    return t_sat + t_lin, t_sat, t_lin


def tplh(c, kp, vtp, voh, vol):
    a = voh - vol - abs(vtp)
    t_sat = 2 * c * abs(vtp) / (kp * a * a)
    t_lin = c / (kp * a) * math.log(4 * a / (voh - vol) - 1)
    return t_sat + t_lin, t_sat, t_lin


def tphl_avg(c, kn, vtn, voh, vol):
    v50 = (voh + vol) / 2
    i1 = kn / 2 * (voh - vtn) ** 2
    i2 = kn / 2 * (2 * (voh - vtn) * v50 - v50 ** 2) if v50 < voh - vtn else i1
    iav = 0.5 * (i1 + i2)
    return c * (voh - v50) / iav, i1, i2, iav


def tplh_avg(c, kp, vtp, voh, vol, vdd):
    v50 = (voh + vol) / 2
    ov = vdd - vol - abs(vtp)
    i1 = kp / 2 * ov ** 2                      # Vout = VOL: PMOS VSD = VDD, saturated
    vsd = vdd - v50
    i2 = kp / 2 * (2 * ov * vsd - vsd ** 2) if vsd < ov else i1
    iav = 0.5 * (i1 + i2)
    return c * (v50 - vol) / iav, i1, i2, iav


def simulate_fall(c, kn, vtn, voh, tmax, n=4000):
    """Vout(t) for an ideal step Vin: 0 -> VOH, PMOS off."""
    t = np.linspace(0, tmax, n)
    v = np.empty(n)
    v[0] = voh
    dt = t[1] - t[0]
    for i in range(1, n):
        def f(x):
            return -idn(voh, x, kn, vtn) / c
        x = v[i - 1]
        k1 = f(x); k2 = f(x + dt / 2 * k1); k3 = f(x + dt / 2 * k2); k4 = f(x + dt * k3)
        v[i] = x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return t, v


if __name__ == '__main__':
    q4 = dict(vdd=3.3, kn=60e-6 * 8, kp=25e-6 * 12, vtn=0.6, vtp=-0.7)
    q3 = dict(vdd=3.3, kn=200e-6, kp=80e-6, vtn=0.6, vtp=-0.7)
    sym = dict(vdd=2.5, kn=120e-6, kp=120e-6, vtn=0.6, vtp=-0.6)
    for name, p in [('Q4', q4), ('Q3', q3), ('sym', sym)]:
        s = summary(p)
        # brute-force check of VIL, VIH from the numerical VTC
        vin = np.linspace(0, p['vdd'], 20001)
        vo = np.array([vout_of(x, p) for x in vin])
        g = np.gradient(vo, vin)
        idx = np.where(np.diff(np.sign(g + 1)))[0]
        print(name, {k: round(v, 4) for k, v in s.items()}, 'numeric -1 crossings:', vin[idx].round(4))
