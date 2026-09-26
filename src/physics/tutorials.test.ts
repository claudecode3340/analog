/**
 * CLAUDE.md §11.3 — Tutorials 2 and 3 (Razavi 9.1–9.4, 9.6, 9.8) solved by the engine.
 * These pin the engine's answers; agreement/disagreement with the student's preliminary values
 * is reported in content/inventory.md §7.
 */
import { describe, expect, it } from 'vitest';
import { tut2Q1, tut2Q2, tut2Q3, tut3Q1, tut3Q2, tut3Q3 } from './solvers';

function near(actual: number, expected: number, relTol = 0.003) {
  expect(Math.abs(actual - expected), `got ${actual}, expected ${expected}`).toBeLessThanOrEqual(Math.abs(expected) * relTol);
}

describe('Tutorial 2', () => {
  it('Q1 (Razavi 9.1b,c)', () => {
    const r = tut2Q1();
    near(r.av, 24.43);
    near(r.voutMin, 0.6);
    near(r.voutMax, 2.489);
    near(r.diffSwing, 3.779);
    near(r.peak.rTriode, 5214);
    near(r.peak.avAtPeak, 19.8, 0.005);
  });
  it('Q2 (Razavi 9.2a–c)', () => {
    const r = tut2Q2();
    near(r.wlPmin, 212.8);
    near(r.wMin, 106.4e-6);
    near(r.voutMinStack, 0.7);
    near(r.voutMaxStack, 1.5);
    near(r.buffer.upper, 1.207);
    near(r.buffer.width, 0.507);
    near(r.av, 1301);
  });
  it('Q3 (Razavi 9.3)', () => {
    const r = tut2Q3();
    near(r.vovEach, 0.45);
    near(r.fc.av, 246.9);
    near(r.fc.avExact, 226.9);
    expect(r.canReachZero).toBe(true);
    near(r.fc.vinCmMin, -0.35);
  });
});

describe('Tutorial 3', () => {
  it('Q1 (Razavi 9.4a–d)', () => {
    const r = tut3Q1();
    near(r.vinCmMax, 1.507);
    near(r.vx, 1.839);
    near(r.window.lower, 1.0);
    near(r.window.upper, 1.507);
    near(r.vb2Min, 1.039);
    near(r.vb2Max, 1.478);
  });
  it('Q2 (Razavi 9.6)', () => {
    const r = tut3Q2();
    near(r.vxy, 1.689);
    near(r.vinCmMax, 2.389);
    near(r.av, 451.1);
    near(r.diffSwing, 4.433);
  });
  it('Q3 (Razavi 9.8)', () => {
    const r = tut3Q3();
    near(r.vxy, 1.839);
    near(r.wlN, 16.62);
    near(r.wlP, 92.62);
    near(r.av, 3952);
  });
});
