/**
 * DC node voltages of every multi-transistor circuit the app draws (Step A of the master method, for
 * whole circuits). Each function returns the node voltages and the current in each device; the region of
 * every device then follows from its fence (NMOS VD ≥ VG − Vth, PMOS VD ≤ VG + |Vth|), so moving a bias
 * voltage in a lab shows exactly which transistor leaves saturation first.
 *
 * λ = 0 for the DC bias (as in the notes); rO is reported with the process λ for the small-signal step.
 */
import { gmFromIdVov, rO, vovFromId } from './device';
import { steering } from './diffpair';
import type { Process } from './process';

export interface NodeDevice {
  kind: 'n' | 'p';
  vg: number;
  vs: number;
  vd: number;
  vth: number;
  id: number;
  gm: number;
  rO: number;
}

function nDev(proc: Process, id: number, wl: number, vg: number, vs: number, vd: number, lambda = proc.lambdan): NodeDevice {
  const vov = vovFromId(id, proc.kpn, wl);
  return { kind: 'n', vg, vs, vd, vth: proc.vthn, id, gm: id > 0 ? gmFromIdVov(id, vov) : 0, rO: rO(lambda, id) };
}
function pDev(proc: Process, id: number, wl: number, vg: number, vs: number, vd: number, lambda = proc.lambdap): NodeDevice {
  const vov = vovFromId(id, proc.kpp, wl);
  return { kind: 'p', vg, vs, vd, vth: proc.vthp, id, gm: id > 0 ? gmFromIdVov(id, vov) : 0, rO: rO(lambda, id) };
}

/** VGS (magnitude) that carries `id` in a device of size `wl`. */
export function vgsFor(id: number, kp: number, wl: number, vth: number): number {
  return vth + vovFromId(id, kp, wl);
}

// ─── Telescopic cascode, fully differential (Razavi Fig. 9.8, Ex 9.7 numbering) ──

export interface TelescopicNodesInput {
  proc: Process;
  iss: number;
  wlN: number; // M1–M4
  wlP: number; // M5–M8
  wl9: number; // tail
  vinCm: number;
  vb1: number; // NMOS cascode gates
  vb2: number; // PMOS cascode gates
  /** Output CM, set in practice by CMFB. */
  vout: number;
  /** Differential input (small), splits the current by the steering law. */
  vd?: number;
}

export function telescopicNodes(p: TelescopicNodesInput) {
  const { proc } = p;
  const id = p.iss / 2;
  const vgsN = vgsFor(id, proc.kpn, p.wlN, proc.vthn);
  const vgsP = vgsFor(id, proc.kpp, p.wlP, proc.vthp);
  const vov9 = vovFromId(p.iss, proc.kpn, p.wl9);
  const vbTail = proc.vthn + vov9;
  const vP = p.vinCm - vgsN;
  const vX = p.vb1 - vgsN; // sources of M3, M4
  const vY = p.vb2 + vgsP; // sources of M5, M6 (PMOS: VS = VG + |VGS|)
  const vb3 = proc.vdd - vgsP; // gate of M7, M8 for current ID
  const st = steering({ kp: proc.kpn, wl: p.wlN, iss: p.iss, dvin: p.vd ?? 0 });
  const vo1 = p.vout, vo2 = p.vout;
  return {
    vP,
    vX,
    vY,
    vb3,
    vbTail,
    devices: {
      m1: nDev(proc, st.id1, p.wlN, p.vinCm + (p.vd ?? 0) / 2, vP, vX),
      m2: nDev(proc, st.id2, p.wlN, p.vinCm - (p.vd ?? 0) / 2, vP, vX),
      m3: nDev(proc, st.id1, p.wlN, p.vb1, vX, vo1),
      m4: nDev(proc, st.id2, p.wlN, p.vb1, vX, vo2),
      m5: pDev(proc, id, p.wlP, p.vb2, vY, vo1),
      m6: pDev(proc, id, p.wlP, p.vb2, vY, vo2),
      m7: pDev(proc, id, p.wlP, vb3, proc.vdd, vY),
      m8: pDev(proc, id, p.wlP, vb3, proc.vdd, vY),
      m9: nDev(proc, p.iss, p.wl9, vbTail, 0, vP),
    },
  };
}

// ─── Five-transistor OTA (M1,2 NMOS input, M3,4 PMOS mirror, M5 tail, M6 tail bias diode) ──

export interface FiveTNodesInput {
  proc: Process;
  iss: number;
  wl12: number;
  wl34: number;
  wlTail: number;
  vinCm: number;
  /** Differential input vd = Vin1 − Vin2 (Vin1 on M1's gate, the side with the diode). */
  vd?: number;
}

export function fiveTNodes(p: FiveTNodesInput) {
  const { proc } = p;
  const vov5 = vovFromId(p.iss, proc.kpn, p.wlTail);
  const vbTail = proc.vthn + vov5;
  const st = steering({ kp: proc.kpn, wl: p.wl12, iss: p.iss, dvin: p.vd ?? 0 });
  const vin1 = p.vinCm + (p.vd ?? 0) / 2;
  // M1 sets the tail node: VP = Vin1 − VGS1(id1)
  const vP = st.id1 > 0 ? vin1 - vgsFor(st.id1, proc.kpn, p.wl12, proc.vthn) : p.vinCm - (p.vd ?? 0) / 2 - vgsFor(st.id2, proc.kpn, p.wl12, proc.vthn);
  const vgs3 = vgsFor(Math.max(st.id1, 1e-15), proc.kpp, p.wl34, proc.vthp);
  const vD1 = proc.vdd - vgs3; // diode node
  // Output: with vd = 0 (balanced) it equals the diode node. Otherwise it is set by the gain: clamp to the rails' fences.
  const id = p.iss / 2;
  const nBal = nDev(proc, id, p.wl12, p.vinCm, vP, vD1);
  const pBal = pDev(proc, id, p.wl34, vD1, proc.vdd, vD1);
  const av = nBal.gm * (1 / (1 / nBal.rO + 1 / pBal.rO));
  const lo = vP + 0; // cannot fall below the tail node
  const hi = proc.vdd;
  const vOut = Math.min(hi, Math.max(lo, vD1 + (Number.isFinite(av) ? av : 1e6) * (p.vd ?? 0)));
  return {
    vP,
    vD1,
    vOut,
    vbTail,
    vov5,
    av,
    devices: {
      m1: nDev(proc, st.id1, p.wl12, vin1, vP, vD1),
      m2: nDev(proc, st.id2, p.wl12, p.vinCm - (p.vd ?? 0) / 2, vP, vOut),
      m3: pDev(proc, st.id1, p.wl34, vD1, proc.vdd, vD1),
      m4: pDev(proc, st.id1, p.wl34, vD1, proc.vdd, vOut),
      m5: nDev(proc, p.iss, p.wlTail, vbTail, 0, vP),
      m6: nDev(proc, p.iss, p.wlTail, vbTail, 0, vbTail),
    },
  };
}

// ─── Resistively loaded differential pair (Tutorial 1 style) ────────────────

export interface DiffPairNodesInput {
  kp: number;
  wl: number;
  vth: number;
  lambda?: number;
  vdd: number;
  iss: number;
  rd: number;
  vin1: number;
  vin2: number;
  /** Bottom of the tail source (VSS for a split supply). */
  vss?: number;
  /** Tail device size; when given the tail is an NMOS (M3) whose fence is checked too. */
  wlTail?: number;
}

export function diffPairNodes(p: DiffPairNodesInput) {
  const st = steering({ kp: p.kp, wl: p.wl, iss: p.iss, dvin: p.vin1 - p.vin2 });
  const vss = p.vss ?? 0;
  const on1 = st.id1 >= st.id2;
  const vP = on1 ? p.vin1 - (p.vth + vovFromId(st.id1, p.kp, p.wl)) : p.vin2 - (p.vth + vovFromId(st.id2, p.kp, p.wl));
  const vD1 = p.vdd - st.id1 * p.rd;
  const vD2 = p.vdd - st.id2 * p.rd;
  const lam = p.lambda ?? 0;
  const mk = (id: number, vg: number, vd: number): NodeDevice => ({ kind: 'n', vg, vs: vP, vd, vth: p.vth, id, gm: id > 0 ? Math.sqrt(2 * p.kp * p.wl * id) : 0, rO: rO(lam, id) });
  const devices: Record<string, NodeDevice> = { m1: mk(st.id1, p.vin1, vD1), m2: mk(st.id2, p.vin2, vD2) };
  if (p.wlTail) {
    const vov3 = vovFromId(p.iss, p.kp, p.wlTail);
    devices.m3 = { kind: 'n', vg: vss + p.vth + vov3, vs: vss, vd: vP, vth: p.vth, id: p.iss, gm: gmFromIdVov(p.iss, vov3), rO: rO(lam, p.iss) };
  }
  return { ...st, vP, vD1, vD2, vout: vD1 - vD2, devices };
}

// ─── Cascode amplifier (M1 input, M2 cascode, optional PMOS cascode load M3/M4) ──

export interface CascodeNodesInput {
  proc: Process;
  id: number;
  wl1: number;
  wl2: number;
  vb1: number; // gate of M2
  vout: number;
  /** PMOS load: 'current' = M3 source only; 'cascode' = M3 cascode + M4 source; 'resistor' = RD. */
  load: 'resistor' | 'current' | 'cascode';
  wlP?: number;
  vb2?: number; // gate of the PMOS cascode (M3 when load = cascode)
}

export function cascodeNodes(p: CascodeNodesInput) {
  const { proc } = p;
  const vgs1 = vgsFor(p.id, proc.kpn, p.wl1, proc.vthn);
  const vgs2 = vgsFor(p.id, proc.kpn, p.wl2, proc.vthn);
  const vX = p.vb1 - vgs2;
  const devices: Record<string, NodeDevice> = {
    m1: nDev(proc, p.id, p.wl1, vgs1, 0, vX),
    m2: nDev(proc, p.id, p.wl2, p.vb1, vX, p.vout),
  };
  let vY: number | undefined;
  if (p.load !== 'resistor') {
    const wlP = p.wlP ?? p.wl2;
    const vgsP = vgsFor(p.id, proc.kpp, wlP, proc.vthp);
    if (p.load === 'current') {
      devices.m3 = pDev(proc, p.id, wlP, proc.vdd - vgsP, proc.vdd, p.vout);
    } else {
      const vb2 = p.vb2 ?? proc.vdd - (vgsP - proc.vthp) - vgsP; // M4 at its edge: VY = VDD − |Vov4|
      vY = vb2 + vgsP;
      devices.m3 = pDev(proc, p.id, wlP, vb2, vY, p.vout);
      devices.m4 = pDev(proc, p.id, wlP, proc.vdd - vgsP, proc.vdd, vY);
    }
  }
  return { vgs1, vX, vY, devices };
}
