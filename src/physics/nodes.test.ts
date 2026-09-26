/** Whole-circuit DC solves: every device's region follows from its fence. */
import { describe, expect, it } from 'vitest';
import { cascodeNodes, diffPairNodes, fiveTNodes, telescopicNodes } from './nodes';
import { EX_9_7, SET_B } from './process';
import { ex97, fiveTOtaQuiz, QUIZ1_C, tut1Q1 } from './solvers';
import { regionFromNodesPure } from './nodes.helpers';

const regions = (devs: Record<string, { kind: 'n' | 'p'; vg: number; vs: number; vd: number; vth: number }>) =>
  Object.fromEntries(Object.entries(devs).map(([k, d]) => [k, regionFromNodesPure(d)]));

describe('telescopic nodes (Razavi Ex 9.7)', () => {
  const e = ex97();
  const base = { proc: EX_9_7, iss: 3e-3, wlN: e.wlN, wlP: e.wlP, wl9: e.wl9, vinCm: e.vinCm, vb1: e.vb1, vb2: e.vb2, vout: 1.65 };
  it('reproduces the book bias: VP = 0.5, VX = 0.7, VY = 2.7', () => {
    const n = telescopicNodes(base);
    expect(n.vP).toBeCloseTo(0.5, 6);
    expect(n.vX).toBeCloseTo(0.7, 6);
    expect(n.vY).toBeCloseTo(2.7, 6);
  });
  it('all nine saturated at mid swing', () => {
    expect(Object.values(regions(telescopicNodes(base).devices)).every((r) => r === 'saturation')).toBe(true);
  });
  it('output below Vout,min = 0.9 V pushes M3/M4 into triode first', () => {
    const r = regions(telescopicNodes({ ...base, vout: 0.85 }).devices);
    expect(r.m3).toBe('triode');
    expect(r.m1).toBe('saturation');
  });
  it('Vb1 too low starves M1/M2 (they go triode)', () => {
    const r = regions(telescopicNodes({ ...base, vb1: 1.5 }).devices);
    expect(r.m1).toBe('triode');
  });
});

describe('5-T OTA nodes (exam question)', () => {
  const { design, ota } = fiveTOtaQuiz(QUIZ1_C);
  const base = { proc: SET_B, iss: QUIZ1_C.iRef, wl12: design.wl12, wl34: design.wl34, wlTail: QUIZ1_C.wlTail, vinCm: 1.1 };
  it('balanced: output sits at the diode node VDD − |VGS3|', () => {
    const n = fiveTNodes(base);
    expect(n.vOut).toBeCloseTo(SET_B.vdd - ota.vgs3, 9);
    expect(Object.values(regions(n.devices)).every((r) => r === 'saturation')).toBe(true);
  });
  it('the CM limits are exactly the fence edges', () => {
    const lo = fiveTNodes({ ...base, vinCm: QUIZ1_C.vinCmMin });
    expect(lo.devices.m5.vd - lo.devices.m5.vs).toBeCloseTo(lo.vov5, 9);
    const hi = fiveTNodes({ ...base, vinCm: QUIZ1_C.vinCmMax });
    expect(hi.devices.m1.vd).toBeCloseTo(hi.devices.m1.vg - SET_B.vthn, 9);
    expect(regions(fiveTNodes({ ...base, vinCm: QUIZ1_C.vinCmMin - 0.05 }).devices).m5).toBe('triode');
    expect(regions(fiveTNodes({ ...base, vinCm: QUIZ1_C.vinCmMax + 0.05 }).devices).m1).toBe('triode');
  });
});

describe('diff pair nodes (Tutorial 1 Q1)', () => {
  const q = tut1Q1();
  const base = { kp: 400e-6, wl: q.wl12, vth: 0.35, vdd: 0.9, vss: -0.9, iss: 0.2e-3, rd: q.rd, vin1: 0, vin2: 0, wlTail: q.wl3 };
  it('balanced: drains at 0 V, tail node at −0.5 V', () => {
    const n = diffPairNodes(base);
    expect(n.vD1).toBeCloseTo(0, 9);
    expect(n.vP).toBeCloseTo(-0.5, 9);
    expect(Object.values(regions(n.devices)).every((r) => r === 'saturation')).toBe(true);
  });
  it('CMIR edges: −0.25 V (tail fence) and +0.35 V (M1 fence)', () => {
    expect(regions(diffPairNodes({ ...base, vin1: -0.26, vin2: -0.26 }).devices).m3).toBe('triode');
    expect(regions(diffPairNodes({ ...base, vin1: -0.24, vin2: -0.24 }).devices).m3).toBe('saturation');
    expect(regions(diffPairNodes({ ...base, vin1: 0.36, vin2: 0.36 }).devices).m1).toBe('triode');
    expect(regions(diffPairNodes({ ...base, vin1: 0.34, vin2: 0.34 }).devices).m1).toBe('saturation');
  });
});

describe('cascode nodes', () => {
  it('VX = Vb1 − VGS2, and a too-low Vb1 pushes M1 into triode', () => {
    const base = { proc: SET_B, id: 100e-6, wl1: 20, wl2: 20, vb1: 1.0, vout: 1.2, load: 'current' as const };
    const n = cascodeNodes(base);
    expect(n.vX).toBeCloseTo(1.0 - (0.4 + Math.sqrt((2 * 100e-6) / (200e-6 * 20))), 9);
    expect(Object.values(regions(n.devices)).every((r) => r === 'saturation')).toBe(true);
    expect(regions(cascodeNodes({ ...base, vb1: 0.7 }).devices).m1).toBe('triode');
  });
});
