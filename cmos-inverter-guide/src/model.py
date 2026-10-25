import numpy as np
def idn(vgs, vds, k, vt, lam=0.0):
    ov = vgs - vt
    if ov <= 0: return 0.0
    if vds < ov: i = k/2*(2*ov*vds - vds**2)
    else: i = k/2*ov**2
    return i*(1+lam*vds)
def vout_of(vin, VDD, vtn, vtp, kn, kp, lam=1e-4):
    # PMOS in magnitudes
    f = lambda v: idn(vin, v, kn, vtn, lam) - idn(VDD-vin, VDD-v, kp, -vtp, lam)
    lo, hi = 0.0, VDD
    for _ in range(200):
        m = (lo+hi)/2
        if f(m) > 0: hi = m
        else: lo = m
    return (lo+hi)/2
def crit(VDD, vtn, vtp, kn, kp, n=20001):
    vin = np.linspace(0, VDD, n)
    vo = np.array([vout_of(v, VDD, vtn, vtp, kn, kp) for v in vin])
    g = np.gradient(vo, vin)
    idx = np.where(g <= -1)[0]
    vil, vih = vin[idx[0]], vin[idx[-1]]
    vth = vin[np.argmin(abs(vo - vin))]
    return vil, vih, vth
def closed(VDD, vtn, vtp, kR):
    r_th = 1/np.sqrt(kR)
    r_il = (2*np.sqrt(kR*(kR+3)) - kR)/(kR*(kR+4))
    r_ih = (1+2*np.sqrt(1+3*kR))/(3*kR)
    X = lambda r: (vtn + r*(VDD+vtp))/(1+r)
    return X(r_il), X(r_ih), X(r_th)
