/**
 * Poles, feedback, settling and slewing (Razavi §6, §8.1, §9.1).
 * Formulas are in rad/s; convert to Hz only at the last line with toHz().
 */

export function toHz(omega: number): number {
  return omega / (2 * Math.PI);
}

export function toRad(f: number): number {
  return 2 * Math.PI * f;
}

/** One pole per node: ωp = 1/(R·C). */
export function pole(r: number, c: number): number {
  return 1 / (r * c);
}

/** GBW of a one-stage op amp: ωu = gm/CL (Rout cancels). */
export function gbwOneStage(gm: number, cl: number): number {
  return gm / cl;
}

/** ωu = A0·ω0. */
export function unityGainFrequency(a0: number, omega0: number): number {
  return a0 * omega0;
}

/** Feedback factor of a resistive divider: β = R2/(R1 + R2). */
export function betaDivider(r1: number, r2: number): number {
  return r2 / (r1 + r2);
}

/** Aclosed = A/(1 + βA). */
export function closedLoopGain(a: number, beta: number): number {
  return a / (1 + beta * a);
}

/** Gain error ε = 1/(1 + βA). */
export function gainError(a: number, beta: number): number {
  return 1 / (1 + beta * a);
}

/** Design equation (approximate, ε ≈ 1/βA): Amin = Aclosed/ε. */
export function minOpenLoopGain(aClosed: number, eps: number): number {
  return aClosed / eps;
}

/** Exact minimum open-loop gain from 1/(1+βA) ≤ ε: A ≥ (1/ε − 1)/β. */
export function minOpenLoopGainExact(beta: number, eps: number): number {
  return (1 / eps - 1) / beta;
}

/** Voltage-sensing feedback: Rout,closed = Rout/(1 + βA). */
export function routClosed(routOpen: number, a: number, beta: number): number {
  return routOpen / (1 + beta * a);
}

/** Closed-loop time constant, exact single-pole form: τ = 1/[(1 + βA0)ω0]. */
export function tauClosedExact(a0: number, omega0: number, beta: number): number {
  return 1 / ((1 + beta * a0) * omega0);
}

/** Closed-loop time constant, design form: τ ≈ 1/(β ωu) = Aclosed/ωu. */
export function tauClosed(beta: number, omegaU: number): number {
  return 1 / (beta * omegaU);
}

/** ln(1/ε): 1% → 4.605, 0.1% → 6.908. */
export function settlingTimeConstants(eps: number): number {
  return Math.log(1 / eps);
}

/** Linear settling to fractional error ε: t = τ·ln(1/ε). */
export function settlingTime(tau: number, eps: number): number {
  return tau * Math.log(1 / eps);
}

/** Required ωu for settling: ωu ≥ ln(1/ε)/(β·t). */
export function requiredOmegaU(p: { beta: number; eps: number; t: number }): number {
  return Math.log(1 / p.eps) / (p.beta * p.t);
}

/** First-order step response: final·(1 − e^(−t/τ)). */
export function stepResponse(final: number, tau: number, t: number): number {
  return final * (1 - Math.exp(-t / tau));
}

/** Slew rate SR = I/CL (V/s). */
export function slewRate(i: number, cl: number): number {
  return i / cl;
}
