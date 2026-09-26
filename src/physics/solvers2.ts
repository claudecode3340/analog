/**
 * Solvers for the lectures after the mid-sem (L5–L9): gain boosting (Tutorial 4), CMFB (Tutorial 5),
 * slewing and settling (Tutorial 6). These tutorials are not Razavi problems and have no answer key;
 * every assumption is written next to the number (see content/inventory.md, §7b).
 */
import { gmFromIdVov, rO, vovFromId } from './device';
import { parallel } from './impedance';
import { triodeSenseWl } from './cmfb';

/** Gain-boosted (regulated) cascode, lecture-notes form: Rout = rO1 + rO2 + (1 + A1)·gm2·rO2·rO1. */
export function boostedRout(p: { gm2: number; rO2: number; rO1: number; a1: number }): number {
  return p.rO1 + p.rO2 + (1 + p.a1) * p.gm2 * p.rO2 * p.rO1;
}

/** Plain cascode in the same form (A1 = 0). */
export function cascodeRoutExact(p: { gm2: number; rO2: number; rO1: number }): number {
  return boostedRout({ ...p, a1: 0 });
}

// ─── Tutorial 4 Q1 (adapted Razavi 9.10): regulated cascode with an NMOS CS auxiliary M3 ──

export function tut4Q1() {
  const kpn = 172.35e-6, vth = 0.7, wl = 200, ln = 0.1, i1 = 100e-6, i2 = 0.5e-3, vdd = 3;
  const kpp = 51.7e-6, vthp = 0.8, lp = 0.2, wlp = 100;
  const vov3 = vovFromId(i1, kpn, wl);
  const vov2 = vovFromId(i2, kpn, wl);
  const vgs3 = vth + vov3; // X = VGS3 (M3's gate is at X, its source at ground)
  const vx = vgs3;
  const vg2 = vx + vth + vov2;
  const gm1 = gmFromIdVov(i2, vov2), gm2 = gm1, gm3 = gmFromIdVov(i1, vov3);
  const ro1 = rO(ln, i2), ro2 = ro1, ro3 = rO(ln, i1);
  // (b) ideal current sources
  const a3 = gm3 * ro3;
  const rout = boostedRout({ gm2, rO2: ro2, rO1: ro1, a1: a3 });
  const av = gm1 * rout;
  // (c) PMOS current sources
  const roP1 = rO(lp, i1), roP2 = rO(lp, i2);
  const a3p = gm3 * parallel(ro3, roP1);
  const routP = parallel(boostedRout({ gm2, rO2: ro2, rO1: ro1, a1: a3p }), roP2);
  const avP = gm1 * routP;
  const vovP2 = vovFromId(i2, kpp, wlp);
  const voutMin = vg2 - vth;
  const voutMax = vdd - vovP2;
  return { vx, vg2, vgs3, a3, rout, av, a3p, routP, avP, voutMin, voutMax, swing: voutMax - voutMin, vthp };
}

// ─── Tutorial 4 Q2: gain boosting with a PMOS CS auxiliary (M3) loaded by NMOS M4 ──

export function tut4Q2() {
  const vdd = 1.8, kpn = 150e-6, kpp = 100e-6, wln = 150, wlp = 100, vthn = 0.7, vthp = 0.85, id = 0.1e-3;
  const vov5 = vovFromId(id, kpp, wlp);
  const vbp = vdd - (vthp + vov5); // (a)
  const vov1 = vovFromId(id, kpn, wln);
  const vp = vov1; // (b) target
  const vg2 = vp + vthn + vov1; // M2's gate = M3's drain
  const m3Saturated = vg2 <= vp + vthp; // PMOS fence: VD ≤ VG + |Vth|
  const i4 = 0.5 * kpn * wln * 0.1 * 0.1; // (c) Vov4 = 0.1 V
  const vov3 = vovFromId(i4, kpp, wlp);
  const vs = vp + vthp + vov3; // M3 source
  // (d) plain cascode, ideal source: (gm rO)^2 ≈ 2550
  const gm = gmFromIdVov(id, vov1);
  const lambdaApprox = gm / (Math.sqrt(2550) * id); // gm·rO = √2550 → rO = √2550/gm → λ = 1/(rO·ID)
  const x = -1 + Math.sqrt(1 + 2550); // exact: x² + 2x = 2550 with x = gm·rO (Rout = 2rO + gm rO²)
  const lambdaExact = gm / (x * id);
  // (e) λp = 1.3 λn; the auxiliary M3/M4 boosts; M5 (PMOS, rO5) loads the output
  const ln = lambdaApprox, lp = 1.3 * ln;
  const ro = rO(ln, id), ro5 = rO(lp, id);
  const gm3 = gmFromIdVov(i4, vov3);
  const a1 = gm3 * parallel(rO(lp, i4), rO(ln, i4));
  const rBoost = boostedRout({ gm2: gm, rO2: ro, rO1: ro, a1 });
  const av = gm * parallel(rBoost, ro5);
  const avIdealLoad = gm * rBoost;
  return { vbp, vov1, vp, vg2, m3Saturated, i4, vs, gm, lambdaApprox, lambdaExact, a1, rBoost, av, avIdealLoad };
}

// ─── Tutorial 5 Q1 (Razavi 9.11 extended): triode-device CMFB in the tail ──

export function tut5Q1() {
  const vdd = 3, kpn = 135e-6, kpp = 40e-6, vthn = 0.7, vthp = 0.8, id = 0.5e-3, voutCm = 1.5, vp = 0.1;
  const wl = triodeSenseWl({ id, kpn, vp, voutSum: 2 * voutCm, vthn });
  // exact triode equation (keeps the VDS²/2 term): ID = µnCox(W/L)[(VGS − Vth)VDS − VDS²/2]
  const wlExact = id / (kpn * ((voutCm - vthn) * vp - (vp * vp) / 2));
  // (b), (c) assuming every transistor has this same W/L
  const vovP = vovFromId(id, kpp, wl);
  const vovN = vovFromId(id, kpn, wl);
  const vb1 = vdd - (vthp + vovP);
  const voutMax = vdd - 2 * vovP;
  const voutMin = vp + 2 * vovN;
  return { wl, wlExact, vb1, voutMax, voutMin, diffSwing: 2 * (voutMax - voutMin) };
}

// ─── Tutorial 6: slewing and linear settling ───────────────────────────────

/** Q1: non-inverting amp, R1 4 MΩ, R2 1 MΩ, CL 8 pF, A0 80 dB, Rout 50 kΩ, Imax 160 µA. */
export function tut6Q1() {
  const a = 1e4, r1 = 4e6, r2 = 1e6, cl = 8e-12, rout = 50e3, imax = 160e-6, v0 = 0.05, vBig = 1;
  const beta = r2 / (r1 + r2);
  const acl = a / (1 + a * beta);
  const tau = (cl * rout) / (1 + a * beta);
  const vAt1ns = v0 * acl * (1 - Math.exp(-1e-9 / tau));
  const slope0 = (v0 * acl) / tau;
  const sr = imax / cl;
  const v0crit = (sr * tau) / acl;
  const tslew = (vBig * acl - sr * tau) / sr;
  return { beta, acl, tau, vAt1ns, slope0, sr, v0crit, tslew };
}

/** Q2: 5-T OTA in a non-inverting loop, ISS 200 µA, CL 5 pF, R1 3 MΩ, R2 1 MΩ, k = 4 mA/V², VA 20 V. */
export function tut6Q2() {
  const iss = 200e-6, cl = 5e-12, r1 = 3e6, r2 = 1e6, k = 4e-3, va = 20, v0 = 1.2;
  const beta = r2 / (r1 + r2);
  const sr = iss / cl;
  const dvinMin = Math.sqrt((2 * iss) / k); // √2·Vov at balance
  const vx = v0 - dvinMin; // X = β·Vout when M2 turns back on
  const voutAtEnd = vx / beta;
  const tslew = voutAtEnd / sr;
  const id = iss / 2;
  const ro = va / id;
  const rout = parallel(ro, ro);
  const gm = Math.sqrt(2 * k * id);
  const a0 = gm * rout;
  const w0 = 1 / (rout * cl);
  const tau = 1 / ((1 + beta * a0) * w0);
  const acl = a0 / (1 + beta * a0);
  const vFinal = acl * v0;
  const tLinear = tau * Math.log((vFinal - voutAtEnd) / (0.01 * vFinal));
  return { beta, sr, dvinMin, vx, voutAtEnd, tslew, rout, gm, a0, tau, acl, vFinal, tLinear, total: tslew + tLinear };
}

/** Q3: NMOS-input folded cascode with a cascode-mirror bottom, ISS 300 µA, IP 200 µA, CL 4 pF, Vov1,2 150 mV. */
export function tut6Q3() {
  const iss = 300e-6, ip = 200e-6, cl = 4e-12, vov = 0.15;
  // Output current = (IP − ID2) − copy of (IP − ID1), each branch clamped at ≥ 0.
  const branch = (x: number) => Math.max(0, x);
  const srPlus = (branch(ip - 0) - branch(ip - iss)) / cl;
  const srMinus = (branch(ip - 0) - branch(ip - iss)) / cl; // mirror image: sink = IP, source = max(0, IP − ISS)
  return { srPlus, srMinus, limitedBy: ip < iss ? 'IP' : 'ISS', ipMin: iss, dvinMin: Math.SQRT2 * vov };
}
