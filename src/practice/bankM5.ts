/**
 * Fixed bank for the lectures after the mid-sem (L5–L9): Tutorial 4 Q1–Q2 (gain boosting), Tutorial 5 Q1
 * (triode CMFB), Tutorial 6 Q1–Q3 (slewing and settling), Quiz 2 A–C (CMFB, verified against the key).
 * Tutorials 4–6 have no answer key; each assumption is stated in the flags.
 */
import { quiz2, QUIZ2_A, QUIZ2_B, QUIZ2_C, tut4Q1, tut4Q2, tut5Q1, tut6Q1, tut6Q2, tut6Q3, type Quiz2Part } from '../physics';
import type { Problem } from './schema';
import { texNum, texSI } from './tex';

const NO_KEY = 'Tutorials 4–6 have no answer key. These numbers come from the engine with the assumptions listed; check them against your class solution.';

function t4q1(): Problem {
  const r = tut4Q1();
  const vov3 = Math.sqrt((2 * 100e-6) / (172.35e-6 * 200));
  const vov2 = Math.sqrt((2 * 0.5e-3) / (172.35e-6 * 200));
  return {
    id: 'bank-t4q1',
    source: 'Tutorial 4 Q1 (adapted Razavi 9.10)',
    tags: ['L6'],
    title: 'Tutorial 4 Q1: regulated cascode with an NMOS auxiliary',
    statement: 'I1 = 100 µA, I2 = 0.5 mA, (W/L)1–3 = 100/0.5, VDD = 3 V, µnCox = 172.35 µA/V², Vthn = 0.7 V, λn = 0.1 V⁻¹. M3 (gate at X = drain of M1, loaded by I1) drives M2’s gate. (a) Gate biases of M2 and M3. (b) Gain with ideal current sources. (c) With PMOS current sources ((W/L)p = 50/0.5, µpCox = 51.7 µA/V², |Vthp| = 0.8 V, λp = 0.2 V⁻¹): output swing and gain.',
    figure: { kind: 'gainBoost', props: { vx: r.vx, vg2: r.vg2, vout: 1.8, i1: 100e-6, i2: 0.5e-3 } },
    givens: [
      { sym: 'I_1', value: 100e-6, unit: 'A' },
      { sym: 'I_2', value: 0.5e-3, unit: 'A' },
      { sym: '(W/L)_{1-3}', value: 200, unit: '' },
      { sym: '\\mu_n C_{ox}', value: 172.35e-6, unit: 'A/V²' },
      { sym: 'V_{thn}', value: 0.7, unit: 'V' },
      { sym: '\\lambda_n', value: 0.1, unit: '' },
    ],
    unknowns: [
      { key: 'vx', sym: 'V_{G3} = V_X', label: '(a) Gate of M3 (= X)', unit: 'V' },
      { key: 'vg2', sym: 'V_{G2}', label: '(a) Gate of M2', unit: 'V' },
      { key: 'av', sym: '|A_v|', label: '(b) Gain, ideal sources', unit: 'V/V', tol: 0.03 },
      { key: 'vmin', sym: 'V_{out,min}', label: '(c) Lowest output', unit: 'V' },
      { key: 'vmax', sym: 'V_{out,max}', label: '(c) Highest output', unit: 'V' },
      { key: 'avP', sym: '|A_v|_{PMOS}', label: '(c) Gain with PMOS sources', unit: 'V/V', tol: 0.03 },
    ],
    answers: { vx: r.vx, vg2: r.vg2, av: r.av, vmin: r.voutMin, vmax: r.voutMax, avP: r.avP },
    wrong: { avP: [{ mistake: 'cascodeSimpleLoad', value: r.av }] },
    steps: [
      { tag: 'A', title: 'M3 carries I1 with its source at ground, so X sits one VGS3 up', tex: `V_X = 0.7 + \\sqrt{\\tfrac{2(100\\mu)}{172.35\\mu\\times 200}} = ${texSI(0.7 + vov3, 'V', 4)}`, produces: 'vx', value: 0.7 + vov3 },
      { tag: 'A', title: 'M2 carries I2 with its source at X', tex: `V_{G2} = V_X + 0.7 + \\sqrt{\\tfrac{2(0.5\\mathrm{m})}{172.35\\mu\\times 200}} = ${texSI(0.7 + vov3 + 0.7 + vov2, 'V', 4)}`, produces: 'vg2', value: 0.7 + vov3 + 0.7 + vov2 },
      { tag: 'C', title: 'Auxiliary gain A1 = gm3·rO3; boosted Rout = rO1 + rO2 + (1 + A1)gm2 rO2 rO1', tex: `A_1 = ${texNum(r.a3)},\\; R_{out} = ${texSI(r.rout, 'Ω')}` },
      { tag: 'D', title: '(b) Av = gm1·Rout (ideal I2)', tex: `|A_v| = ${texNum(r.av)}`, produces: 'av', value: r.av },
      { tag: '✓', title: '(c) Floor: M2 fence, Vout ≥ VG2 − Vth', tex: `${texSI(r.vg2 - 0.7, 'V', 4)}`, produces: 'vmin', value: r.vg2 - 0.7 },
      { tag: '✓', title: 'Ceiling: the PMOS source needs its |Vov|', tex: `3 - \\sqrt{\\tfrac{2(0.5\\mathrm{m})}{51.7\\mu\\times 100}} = ${texSI(3 - Math.sqrt(1e-3 / (51.7e-6 * 100)), 'V', 4)}`, produces: 'vmax', value: 3 - Math.sqrt(1e-3 / (51.7e-6 * 100)) },
      { tag: 'D', title: 'The load trap again: the PMOS rO (10 kΩ) is in parallel with hundreds of MΩ', tex: `|A_v| = g_{m1}(R_{boost}\\parallel r_{OP}) = ${texNum(r.avP)}`, produces: 'avP', value: r.avP },
    ],
    hints: ['Walk up from ground: X = VGS3, then VG2 = X + VGS2.', 'Gain boosting multiplies the cascode’s Rout by (1 + A1).', 'Rout = rO1 + rO2 + (1 + A1)gm2rO2rO1; with a PMOS load, Rout ≈ rO,p.', `A1 = gm3·rO3 = ${r.a3.toFixed(0)}.`],
    flags: [NO_KEY, 'Rout uses the lecture-notes form rO1 + rO2 + (1 + A1)gm2rO2rO1 (Lec 07).'],
  };
}

function t4q2(): Problem {
  const r = tut4Q2();
  return {
    id: 'bank-t4q2',
    source: 'Tutorial 4 Q2',
    tags: ['L6'],
    title: 'Tutorial 4 Q2: gain boosting with a PMOS auxiliary',
    statement: 'VDD = 1.8 V, µnCox = 150 µA/V², µpCox = 100 µA/V², (W/L)n = 150, (W/L)p = 100, Vthn = 0.7 V, |Vthp| = 0.85 V, ID1 = 0.1 mA. (a) Vbp. (b) With VP = Vov1 and Vout,min = 2Vov1, is M3 saturated? (c) With Vov4 = 0.1 V, the required VS. (d) With the auxiliary removed and M5 ideal (0.1 mA), λn for a gain of about 2550. (e) With λp = 1.3λn, the gain of the full circuit.',
    givens: [
      { sym: 'V_{DD}', value: 1.8, unit: 'V' },
      { sym: 'I_{D1}', value: 0.1e-3, unit: 'A' },
      { sym: '(W/L)_n', value: 150, unit: '' },
      { sym: '(W/L)_p', value: 100, unit: '' },
    ],
    unknowns: [
      { key: 'vbp', sym: 'V_{bp}', label: '(a) Vbp', unit: 'V' },
      { key: 'm3', sym: 'M_3', label: '(b) M3 region', unit: '', choices: ['Saturated', 'Triode'] },
      { key: 'vs', sym: 'V_S', label: '(c) VS', unit: 'V' },
      { key: 'lam', sym: '\\lambda_n', label: '(d) λn (gain ≈ (gm·rO)²)', unit: '', tol: 0.025 },
    ],
    answers: { vbp: r.vbp, m3: r.m3Saturated ? 0 : 1, vs: r.vs, lam: r.lambdaApprox },
    wrong: { vbp: [{ mistake: 'vovNotVgs', value: 1.8 - Math.sqrt((2 * 0.1e-3) / (100e-6 * 100)) }] },
    steps: [
      { tag: 'A', title: '(a) M5 carries 0.1 mA: Vbp = VDD − |VGS5|', tex: `V_{bp} = 1.8 - \\left(0.85 + \\sqrt{\\tfrac{2(0.1\\mathrm{m})}{100\\mu\\times 100}}\\right) = ${texSI(1.8 - (0.85 + Math.sqrt(0.02)), 'V', 4)}`, produces: 'vbp', value: 1.8 - (0.85 + Math.sqrt(0.02)) },
      { tag: '✓', title: '(b) M3’s drain is M2’s gate: VP + VGS2. PMOS fence: VD3 ≤ VG3 + |Vthp| = VP + 0.85', tex: `V_{D3} = ${texSI(r.vg2, 'V', 4)} \\le ${texSI(r.vp + 0.85, 'V', 4)}\\;\\checkmark\\;(\\text{i.e. } V_{GS2} \\le |V_{th3}|)`, produces: 'm3', value: r.vg2 <= r.vp + 0.85 ? 0 : 1 },
      { tag: 'A', title: '(c) M4 at Vov = 0.1 V sets the current; M3 carries it', tex: `I = \\tfrac12(150\\mu)(150)(0.1)^2 = ${texSI(r.i4, 'A')},\\; V_S = V_P + |V_{GS3}| = ${texSI(r.vs, 'V', 4)}`, produces: 'vs', value: r.vp + 0.85 + Math.sqrt((2 * r.i4) / (100e-6 * 100)) },
      { tag: 'D', title: '(d) Plain cascode, ideal load: |Av| ≈ (gm·rO)² = 2550', tex: `g_m r_O = \\sqrt{2550} = 50.5,\\; \\lambda_n = \\frac{g_m}{50.5\\,I_D} = ${texNum(r.lambdaApprox, 3)}\\,\\mathrm{V^{-1}}\\;(\\text{exact form: } ${texNum(r.lambdaExact, 3)})`, produces: 'lam', value: r.gm / (Math.sqrt(2550) * 0.1e-3) },
      { tag: 'D', title: '(e) Boosted Rout is huge, but M5’s rO (λp = 1.3λn) loads the output: the load trap', tex: `|A_v| = g_m(R_{boost}\\parallel r_{O5}) \\approx ${texNum(r.av)}\\;(${texNum(r.avIdealLoad)}\\text{ with an ideal load})` },
    ],
    hints: ['Walk the node voltages first, then the fences.', 'M3 is a PMOS: saturated while VD ≤ VG + |Vth|.', 'Plain cascode gain ≈ (gm·rO)².', `gm = ${(r.gm * 1e3).toPrecision(3)} mA/V.`],
    flags: [NO_KEY, '(d) accepts both 0.420 (from (gm·rO)²) and 0.428 (from 2gm·rO + (gm·rO)²).'],
  };
}

function t5q1(): Problem {
  const r = tut5Q1();
  const wl = (2 * 0.5e-3) / (135e-6 * 0.1 * (3 - 1.4));
  return {
    id: 'bank-t5q1',
    source: 'Tutorial 5 Q1 (Razavi 9.11 extended)',
    tags: ['L7'],
    title: 'Tutorial 5 Q1: size the triode CMFB devices',
    statement: 'Each branch carries 0.5 mA. M7, M8 (gates on Vout1, Vout2) form the tail in deep triode. VDD = 3 V, µnCox = 135 µA/V², µpCox = 40 µA/V², Vthn = 0.7 V, |Vthp| = 0.8 V. (a) Size M7, M8 for an output CM of 1.5 V with VP = 100 mV. (b) If all transistors have that size, Vb1. (c) The maximum differential swing.',
    figure: { kind: 'cmfbTriode', props: { vout1: 1.5, vout2: 1.5, vp: 0.1, wl: r.wl } },
    givens: [
      { sym: 'I_D', value: 0.5e-3, unit: 'A' },
      { sym: 'V_{out,CM}', value: 1.5, unit: 'V' },
      { sym: 'V_P', value: 0.1, unit: 'V' },
    ],
    unknowns: [
      { key: 'wl', sym: '(W/L)_{7,8}', label: '(a) Size of M7, M8', unit: '', tol: 0.07 },
      { key: 'vb1', sym: 'V_{b1}', label: '(b) Vb1 (all devices this size)', unit: 'V' },
      { key: 'swing', sym: 'V_{pp,diff}', label: '(c) Differential swing', unit: 'V' },
    ],
    answers: { wl: r.wl, vb1: r.vb1, swing: r.diffSwing },
    wrong: {},
    steps: [
      { tag: 'A', title: 'Deep triode: each device is a resistor 1/(µnCox(W/L)(VGS − Vth)); the two in parallel carry 2ID with VP across them', tex: `\\frac{W}{L} = \\frac{2I_D}{\\mu_n C_{ox} V_P (V_{out1}+V_{out2} - 2V_{th})} = \\frac{1\\,\\mathrm{mA}}{135\\mu\\times 0.1\\times 1.6} = ${texNum(wl)}`, produces: 'wl', value: wl },
      { tag: 'A', title: '(b) Vb1 is the PMOS source gate: VDD − |VGS| at 0.5 mA', tex: `V_{b1} = ${texSI(r.vb1, 'V', 4)}`, produces: 'vb1', value: r.vb1 },
      { tag: '✓', title: '(c) Output range: VP + 2Vov,N up to VDD − 2|Vov,P|; differential doubles it', tex: `2(${texNum(r.voutMax, 3)} - ${texNum(r.voutMin, 3)}) = ${texSI(r.diffSwing, 'V')}`, produces: 'swing', value: r.diffSwing },
    ],
    hints: ['Two deep-triode devices in parallel act as one resistor.', 'Ron = 1/(µnCox(W/L)(VGS − Vth)); VP = 2ID·Rtot.', 'W/L = 2ID/(µnCox·VP·(Vout1 + Vout2 − 2Vth)).', 'Rtot = 0.1 V / 1 mA = 100 Ω.'],
    flags: [NO_KEY, 'Deep-triode form (Lec 11) gives 46.3; the full triode equation (with VDS²/2) gives 49.4. Both are marked right.', '(b) and (c) assume “all transistors have the same size” means W/L = 46.3 for every device.'],
  };
}

function t6q1(): Problem {
  const r = tut6Q1();
  const acl = 1e4 / (1 + 1e4 * 0.2);
  const tau = (8e-12 * 50e3) / (1 + 1e4 * 0.2);
  return {
    id: 'bank-t6q1',
    source: 'Tutorial 6 Q1',
    tags: ['L9', 'L1'],
    title: 'Tutorial 6 Q1: linear settling versus slewing',
    statement: 'Non-inverting amplifier: R1 = 4 MΩ, R2 = 1 MΩ, CL = 8 pF, A = 80 dB, Rout = 50 kΩ, Imax = 160 µA. (a) Closed-loop gain, time constant, and Vout 1 ns after a 50 mV step. (b) The initial slope for that step. (c) The slew rate and the step size above which slewing starts. (d) For a 1 V step, how long the output slews.',
    figure: { kind: 'nonInverting', props: { r1: 4e6, r2: 1e6, a: 1e4, cl: 8e-12 } },
    givens: [
      { sym: 'A', value: 1e4, unit: '' },
      { sym: 'R_{out}', value: 50e3, unit: 'Ω' },
      { sym: 'C_L', value: 8e-12, unit: 'F' },
      { sym: 'I_{max}', value: 160e-6, unit: 'A' },
    ],
    unknowns: [
      { key: 'acl', sym: 'A_{CL}', label: '(a) Closed-loop gain', unit: '' },
      { key: 'tau', sym: '\\tau', label: '(a) Time constant', unit: 's' },
      { key: 'v1', sym: 'V_{out}(1\\,\\mathrm{ns})', label: '(a) Output at 1 ns', unit: 'V' },
      { key: 'slope', sym: 'dV/dt|_{0}', label: '(b) Initial slope', unit: 'V/s' },
      { key: 'sr', sym: 'SR', label: '(c) Slew rate', unit: 'V/s' },
      { key: 'v0c', sym: 'V_{0,crit}', label: '(c) Critical step', unit: 'V' },
      { key: 'ts', sym: 't_{slew}', label: '(d) Slewing time for 1 V', unit: 's' },
    ],
    answers: { acl: r.acl, tau: r.tau, v1: r.vAt1ns, slope: r.slope0, sr: r.sr, v0c: r.v0crit, ts: r.tslew },
    wrong: { acl: [{ mistake: 'aInsteadOfInvBeta', value: 1e4 }], tau: [{ mistake: 'betaVsBetaA', value: 8e-12 * 50e3 }] },
    steps: [
      { tag: '·', title: 'β = R2/(R1 + R2) = 0.2; ACL = A/(1 + βA)', tex: `A_{CL} = \\frac{10^4}{1 + 2000} = ${texNum(acl, 5)}`, produces: 'acl', value: acl },
      { tag: '·', title: 'Feedback divides the output time constant RoutCL by (1 + βA)', tex: `\\tau = \\frac{(8\\,\\mathrm{pF})(50\\,\\mathrm{k\\Omega})}{2001} = ${texSI(tau, 's')}`, produces: 'tau', value: tau },
      { tag: '·', title: 'Linear step response', tex: `V_{out} = 0.05\\times ${texNum(acl, 4)}\\,(1 - e^{-1\\,\\mathrm{ns}/\\tau}) = ${texSI(0.05 * acl * (1 - Math.exp(-1e-9 / tau)), 'V', 4)}`, produces: 'v1', value: 0.05 * acl * (1 - Math.exp(-1e-9 / tau)) },
      { tag: '·', title: '(b) Initial slope = final value / τ', tex: `\\frac{0.05\\times ${texNum(acl, 4)}}{\\tau} = ${texSI((0.05 * acl) / tau, 'V/s')}`, produces: 'slope', value: (0.05 * acl) / tau },
      { tag: '·', title: '(c) The op amp can deliver at most Imax into CL', tex: `SR = \\frac{160\\,\\mu\\mathrm{A}}{8\\,\\mathrm{pF}} = ${texSI(160e-6 / 8e-12, 'V/s')}`, produces: 'sr', value: 160e-6 / 8e-12 },
      { tag: '·', title: 'Slewing starts when V0·ACL/τ exceeds SR', tex: `V_{0,crit} = \\frac{SR\\,\\tau}{A_{CL}} = ${texSI((20e6 * tau) / acl, 'V')}`, produces: 'v0c', value: (20e6 * tau) / acl },
      { tag: '·', title: '(d) Ramp at SR until the remaining error is SR·τ, then settle linearly', tex: `t_{slew} = \\frac{V_0 A_{CL} - SR\\,\\tau}{SR} = ${texSI((acl - 20e6 * tau) / 20e6, 's')}`, produces: 'ts', value: (acl - 20e6 * tau) / 20e6 },
    ],
    hints: ['β = R2/(R1 + R2).', 'τ = RoutCL/(1 + βA) (the formula printed on the sheet).', 'Initial slope = V0·ACL/τ; slewing when that exceeds Imax/CL.', 'β = 0.2.'],
    flags: [NO_KEY],
  };
}

function t6q2(): Problem {
  const r = tut6Q2();
  return {
    id: 'bank-t6q2',
    source: 'Tutorial 6 Q2',
    tags: ['L9', 'U11'],
    title: 'Tutorial 6 Q2: a 5-T OTA slews, then settles',
    statement: 'A five-transistor OTA in a non-inverting loop: ISS = 200 µA, CL = 5 pF, R1 = 3 MΩ, R2 = 1 MΩ, µnCox(W/L)1,2 = 4 mA/V², |VA| = 20 V. (a) SR+ and SR−. (b) The differential input that turns M2 fully off. (c) For a 1.2 V input step, how long it slews. (d) Rout, the closed-loop τ, and the total time to settle within 1%.',
    figure: { kind: 'nonInverting', props: { r1: 3e6, r2: 1e6, cl: 5e-12 } },
    givens: [
      { sym: 'I_{SS}', value: 200e-6, unit: 'A' },
      { sym: 'C_L', value: 5e-12, unit: 'F' },
      { sym: '\\mu_n C_{ox} W/L', value: 4e-3, unit: 'A/V²' },
      { sym: 'V_A', value: 20, unit: 'V' },
    ],
    unknowns: [
      { key: 'sr', sym: 'SR_{\\pm}', label: '(a) Slew rate (both)', unit: 'V/s' },
      { key: 'dv', sym: '\\Delta V_{in,min}', label: '(b) Input that turns M2 off', unit: 'V' },
      { key: 'ts', sym: 't_{slew}', label: '(c) Slewing time', unit: 's', tol: 0.03 },
      { key: 'rout', sym: 'R_{out}', label: '(d) Output resistance', unit: 'Ω' },
      { key: 'tau', sym: '\\tau_{cl}', label: '(d) Closed-loop τ', unit: 's' },
      { key: 'total', sym: 't_{total}', label: '(d) Total settling time (1%)', unit: 's', tol: 0.03 },
    ],
    answers: { sr: r.sr, dv: r.dvinMin, ts: r.tslew, rout: r.rout, tau: r.tau, total: r.total },
    wrong: { dv: [{ mistake: 'forgotSatCheck', value: r.dvinMin / Math.SQRT2 }], sr: [{ mistake: 'issNotHalf', value: r.sr / 2 }] },
    steps: [
      { tag: '·', title: '(a) Either way the whole tail current charges or discharges CL (through the mirror)', tex: `SR = \\frac{200\\,\\mu}{5\\,\\mathrm{p}} = ${texSI(200e-6 / 5e-12, 'V/s')}`, produces: 'sr', value: 200e-6 / 5e-12 },
      { tag: '·', title: '(b) Full steering at √2·Vov (Vov at balance)', tex: `\\sqrt{2}\\sqrt{\\tfrac{2(100\\mu)}{4\\,\\mathrm{m}}} = ${texSI(Math.SQRT2 * Math.sqrt(200e-6 / 4e-3), 'V')}`, produces: 'dv', value: Math.SQRT2 * Math.sqrt(200e-6 / 4e-3) },
      { tag: '·', title: '(c) Slewing ends when X = βVout = V0 − ΔVin,min', tex: `V_{out} = \\frac{1.2 - ${texNum(r.dvinMin, 3)}}{0.25} = ${texSI(r.voutAtEnd, 'V')},\\; t_{slew} = \\frac{V_{out}}{SR} = ${texSI(r.voutAtEnd / r.sr, 's')}`, produces: 'ts', value: r.voutAtEnd / r.sr },
      { tag: 'C', title: '(d) Rout = rO2 ‖ rO4 = (VA/ID)/2', tex: `R_{out} = \\frac{20/100\\mu}{2} = ${texSI(20 / 100e-6 / 2, 'Ω')}`, produces: 'rout', value: 20 / 100e-6 / 2 },
      { tag: '·', title: 'τcl = RoutCL/(1 + βA0), A0 = gm·Rout', tex: `\\tau_{cl} = ${texSI(r.tau, 's')}`, produces: 'tau', value: r.tau },
      { tag: '·', title: 'Linear settling of what is left after slewing, to 1% of the final value', tex: `t_{total} = t_{slew} + \\tau\\ln\\frac{V_{final} - V_{out}(t_{slew})}{0.01\\,V_{final}} = ${texSI(r.total, 's')}`, produces: 'total', value: r.tslew + r.tau * Math.log((r.vFinal - r.voutAtEnd) / (0.01 * r.vFinal)) },
    ],
    hints: ['A 5-T OTA slews at ISS/CL both ways.', 'M2 turns off at √2·Vov.', 'τcl = RoutCL/(1 + βA0).', 'β = 1/4.'],
    flags: [NO_KEY, 'Assumes Vout starts at 0 V and the divider (4 MΩ) does not load the 100 kΩ output.'],
  };
}

function t6q3(): Problem {
  const r = tut6Q3();
  return {
    id: 'bank-t6q3',
    source: 'Tutorial 6 Q3',
    tags: ['L9', 'L4'],
    title: 'Tutorial 6 Q3: folded-cascode slew rate',
    statement: 'NMOS-input folded cascode with a cascode-mirror bottom: CL = 4 pF, ISS = 300 µA, each folding PMOS source IP = 200 µA, VA = 25 V, Vov1,2 = 150 mV. (a) SR+. (b) SR− and what limits it. (c) The condition on IP for SR = ISS/CL both ways. (d) The input step that forces full slewing.',
    figure: { kind: 'step', props: { vstep: 1, tau: 5e-9, eps: 0.01, sr: r.srPlus } },
    givens: [
      { sym: 'I_{SS}', value: 300e-6, unit: 'A' },
      { sym: 'I_P', value: 200e-6, unit: 'A' },
      { sym: 'C_L', value: 4e-12, unit: 'F' },
      { sym: 'V_{ov1,2}', value: 0.15, unit: 'V' },
    ],
    unknowns: [
      { key: 'srp', sym: 'SR_+', label: '(a) Positive slew rate', unit: 'V/s' },
      { key: 'srm', sym: 'SR_-', label: '(b) Negative slew rate', unit: 'V/s' },
      { key: 'ipmin', sym: 'I_{P,min}', label: '(c) Minimum IP for SR = ISS/CL', unit: 'A' },
      { key: 'dv', sym: '\\Delta V_{in,min}', label: '(d) Step for full slewing', unit: 'V' },
    ],
    answers: { srp: r.srPlus, srm: r.srMinus, ipmin: r.ipMin, dv: r.dvinMin },
    wrong: { srp: [{ mistake: 'issNotHalf', value: 300e-6 / 4e-12 }] },
    steps: [
      { tag: '·', title: 'Output current = (IP − ID2) − copy of (IP − ID1); a branch cannot carry negative current', tex: '\\text{with } I_P < I_{SS}\\text{ one cascode branch turns off}' },
      { tag: '·', title: '(a) ID2 → 0: the right branch delivers IP; the left branch (IP − ISS < 0) is off, so the mirror sinks nothing', tex: `SR_+ = \\frac{I_P}{C_L} = ${texSI(200e-6 / 4e-12, 'V/s')}`, produces: 'srp', value: 200e-6 / 4e-12 },
      { tag: '·', title: '(b) ID2 → ISS: the right branch is off, the mirror sinks IP. Limited by IP', tex: `SR_- = ${texSI(200e-6 / 4e-12, 'V/s')}`, produces: 'srm', value: 200e-6 / 4e-12 },
      { tag: '·', title: '(c) To slew at ISS/CL both ways, no branch may turn off', tex: `I_P \\ge I_{SS} = ${texSI(300e-6, 'A')}`, produces: 'ipmin', value: 300e-6 },
      { tag: '·', title: '(d) Full steering at √2·Vov', tex: `\\sqrt{2}\\times 0.15 = ${texSI(Math.SQRT2 * 0.15, 'V')}`, produces: 'dv', value: Math.SQRT2 * 0.15 },
    ],
    hints: ['Write the output current as (right branch) − (mirror of left branch).', 'A cascode branch carries IP − ID; it cannot go negative.', 'With IP ≥ ISS both slew rates are ISS/CL.', 'IP = 200 µA < ISS = 300 µA.'],
    flags: [NO_KEY, 'Assumes the bottom M5–M8 is a cascode current mirror (diode on the left), as drawn.'],
  };
}

function quiz2p(part: 'A' | 'B' | 'C', q: Quiz2Part): Problem {
  const r = quiz2(q);
  const vov34 = Math.sqrt((2 * q.id3) / (q.kpp * q.wlP34));
  const vov10 = Math.sqrt((2 * q.idN) / (q.kpn * q.wlN));
  const vp = q.vb1 - (q.vthn + vov10);
  const sum = 2 * q.cmFraction * q.vdd;
  return {
    id: `bank-quiz2${part.toLowerCase()}`,
    source: `Quiz 2 Part ${part}`,
    tags: ['L8', 'L7'],
    title: `Quiz 2 Part ${part}: triode-sensing CMFB on a telescopic`,
    statement: `Reconstructed from your Quiz 2 key (the question sheet was not uploaded). VDD = ${q.vdd} V, µnCox = ${q.kpn * 1e6} µA/V², µpCox = ${q.kpp * 1e6} µA/V², Vthn = ${q.vthn} V, |Vthp| = ${q.vthp} V, λn = ${q.lambdan} V⁻¹. PMOS M3,4: W/L = ${q.wlP34} at ${q.id3 * 1e6} µA. NMOS devices: W/L = ${q.wlN} at ${q.idN * 1e6} µA, Vb1 = ${q.vb1} V; output CM = ${q.cmFraction}·VDD. Find VD4, VP, (W/L)11,12 of the triode sensing pair, Vout,min and Rout looking down.`,
    givens: [{ sym: 'V_{b1}', value: q.vb1, unit: 'V' }],
    unknowns: [
      { key: 'vd4', sym: 'V_{D4}', label: 'VD4', unit: 'V' },
      { key: 'vp', sym: 'V_P', label: 'VP', unit: 'V' },
      { key: 'wl', sym: '(W/L)_{11,12}', label: 'Sensing devices', unit: '' },
      { key: 'vmin', sym: 'V_{out,min}', label: 'Lowest output', unit: 'V' },
      { key: 'rdown', sym: 'R_{out,down}', label: 'Rout looking down', unit: 'Ω' },
    ],
    answers: { vd4: r.vd4, vp: r.vp, wl: r.wl1112, vmin: r.voutMin, rdown: r.routDown },
    wrong: {},
    steps: [
      { tag: 'A', title: 'PMOS diode node: VDD − |VGS3,4|', tex: `V_{D4} = ${texNum(q.vdd)} - (${texNum(q.vthp)} + ${texNum(vov34, 3)}) = ${texSI(q.vdd - (q.vthp + vov34), 'V', 4)}`, produces: 'vd4', value: q.vdd - (q.vthp + vov34) },
      { tag: 'A', title: 'P sits one VGS10 below Vb1', tex: `V_P = ${texNum(q.vb1)} - (${texNum(q.vthn)} + ${texNum(vov10, 3)}) = ${texSI(vp, 'V', 4)}`, produces: 'vp', value: vp },
      { tag: 'A', title: 'Triode sensing pair: VP = 2ID/(µnCox(W/L)(Vout1 + Vout2 − 2Vth))', tex: `\\left(\\tfrac{W}{L}\\right)_{11,12} = \\frac{2I_D}{\\mu_n C_{ox} V_P (${texNum(sum, 3)} - 2V_{th})} = ${texNum((2 * q.idN) / (q.kpn * vp * (sum - 2 * q.vthn)), 4)}`, produces: 'wl', value: (2 * q.idN) / (q.kpn * vp * (sum - 2 * q.vthn)) },
      { tag: '✓', title: 'Lowest output: VP + two NMOS overdrives', tex: `${texSI(vp + 2 * vov10, 'V', 4)}`, produces: 'vmin', value: vp + 2 * vov10 },
      { tag: 'C', title: 'Looking down: gm·rO·rO', tex: `R_{out,down} = ${texSI(((2 * q.idN) / vov10) * (1 / (q.lambdan * q.idN)) ** 2, 'Ω')}`, produces: 'rdown', value: ((2 * q.idN) / vov10) * (1 / (q.lambdan * q.idN)) ** 2 },
    ],
    hints: ['Walk the nodes: PMOS diode from VDD, NMOS from Vb1.', 'Triode devices act as a resistor set by the output CM.', 'VP = 2ID·Rtot with Rtot = 1/(µnCox(W/L)(Vout1 + Vout2 − 2Vth)).', `VP = ${vp.toFixed(3)} V.`],
    flags: ['The key rounds intermediates (VP = 0.11 V), so its W/L differs by up to 1.3%; both are marked right.'],
  };
}

export const M5_BANK: Problem[] = [t4q1(), t4q2(), t5q1(), t6q1(), t6q2(), t6q3(), quiz2p('A', QUIZ2_A), quiz2p('B', QUIZ2_B), quiz2p('C', QUIZ2_C)];
