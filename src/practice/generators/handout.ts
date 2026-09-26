/**
 * Generators for the handout lectures: L1 gain error (Ex 9.1 style), L3 telescopic design from specs
 * (Ex 9.7 style), L4 folded-cascode design from specs (Tut 2 Q3 / PS1 P6 style).
 */
import { closedLoopGain, foldedCascodePmosInput, gainError, minOpenLoopGain, telescopic, wlFromId, type Process } from '../../physics';
import { nice, pick, type Rng } from '../rng';
import type { Generator, GeneratorOutput, Problem } from '../schema';
import { texNum, texSI } from '../tex';

function base(id: string, unit: string, title: string): Pick<Problem, 'id' | 'generator' | 'source' | 'tags' | 'title'> {
  return { id, generator: id, source: 'generated', tags: [unit], title };
}

export const genGainError: Generator = {
  id: 'l1-gain',
  unit: 'L1',
  title: 'Feedback: closed-loop gain, gain error, required open-loop gain',
  make(rng: Rng): GeneratorOutput {
    const acl = pick(rng, [2, 4, 5, 8, 10, 20]);
    const a = pick(rng, [100, 200, 500, 1000, 2000, 5000]);
    const epsTarget = pick(rng, [0.01, 0.005, 0.001]);
    const beta = 1 / acl;
    const acTrue = closedLoopGain(a, beta);
    const eps = gainError(a, beta);
    const amin = minOpenLoopGain(acl, epsTarget);
    const problem: Problem = {
      ...base('l1-gain', 'L1', 'Feedback: closed-loop gain, gain error, required open-loop gain'),
      statement: `A non-inverting amplifier is designed for a closed-loop gain of ${acl} (β = 1/${acl}) with an op amp of open-loop gain A = ${a}. Find the actual closed-loop gain, the gain error, and the open-loop gain needed for an error of ${epsTarget * 100}%.`,
      figure: { kind: 'nonInverting', props: { r1: (acl - 1) * 1e3, r2: 1e3, a } },
      givens: [
        { sym: '1/\\beta', value: acl, unit: '' },
        { sym: 'A', value: a, unit: '' },
        { sym: '\\varepsilon_{target}', value: epsTarget, unit: '' },
      ],
      unknowns: [
        { key: 'ac', sym: 'A_{closed}', label: 'Actual closed-loop gain', unit: '', tol: 0.001 },
        { key: 'eps', sym: '\\varepsilon', label: 'Gain error (fraction)', unit: '' },
        { key: 'amin', sym: 'A_{min}', label: 'Open-loop gain for the target error', unit: '', tol: 0.012 },
      ],
      answers: { ac: acTrue, eps, amin },
      wrong: { ac: [{ mistake: 'aInsteadOfInvBeta', value: a }], eps: [{ mistake: 'betaVsBetaA', value: beta }], amin: [{ mistake: 'aInsteadOfInvBeta', value: 1 / epsTarget }] },
      steps: [
        { tag: '·', title: 'Loop gain βA', tex: `\\beta A = \\frac{${a}}{${acl}} = ${texNum(a / acl)}` },
        { tag: '·', title: 'Aclosed = A/(1 + βA): a little under 1/β', tex: `A_{closed} = \\frac{${a}}{1 + ${texNum(a / acl)}} = ${texNum(a / (1 + a / acl), 5)}`, produces: 'ac', value: a / (1 + a / acl) },
        { tag: '·', title: 'Gain error is one over (1 + loop gain)', tex: `\\varepsilon = \\frac{1}{1 + \\beta A} = ${texNum(1 / (1 + a / acl), 4)}`, produces: 'eps', value: 1 / (1 + a / acl) },
        { tag: '·', title: 'Design form: A ≥ Aclosed/ε', tex: `A_{min} = \\frac{${acl}}{${epsTarget}} = ${texNum(acl / epsTarget)}`, produces: 'amin', value: acl / epsTarget },
      ],
      hints: ['β is what comes back; 1/β is what you get.', 'Gain error is one over loop gain.', 'Aclosed = A/(1 + βA); ε = 1/(1 + βA); Amin = Aclosed/ε.', `βA = ${(a / acl).toFixed(1)}.`],
    };
    return { problem, sane: true };
  },
};

const EX_LIKE: Process = { name: 'Ex 9.7-like', kpn: 60e-6, kpp: 30e-6, vthn: 0.7, vthp: 0.7, lambdan: 0.1, lambdap: 0.2, vdd: 3 };

export const genTeleDesign: Generator = {
  id: 'l3-design',
  unit: 'L3',
  title: 'Design a telescopic op amp from power and swing (Ex 9.7 style)',
  make(rng) {
    const proc = EX_LIKE;
    const power = pick(rng, [6, 8, 10, 12]) * 1e-3;
    const swing = pick(rng, [2, 2.4, 2.8, 3]);
    const vov9 = pick(rng, [0.3, 0.4, 0.5]);
    const vovP = pick(rng, [0.2, 0.25, 0.3]);
    const iss = power / proc.vdd;
    const vovN = (proc.vdd - swing / 2 - vov9 - 2 * vovP) / 2;
    const id = iss / 2;
    const wlN = wlFromId(id, proc.kpn, vovN);
    const wlP = wlFromId(id, proc.kpp, vovP);
    const t = vovN > 0.08 ? telescopic({ proc, iss, wlN, wlP, viss: vov9 }) : undefined;
    const problem: Problem = {
      ...base('l3-design', 'L3', 'Design a telescopic op amp from power and swing (Ex 9.7 style)'),
      statement: `Fully differential telescopic, VDD = 3 V, power ${power * 1e3} mW, differential swing ${swing} Vpp. Tail overdrive ${vov9} V, every PMOS |Vov| = ${vovP} V; the NMOS share what is left. µnCox = 60 µA/V², µpCox = 30 µA/V², Vth = 0.7 V, λn = 0.1, λp = 0.2 V⁻¹. Find ISS, the NMOS overdrive, the sizes and the gain.`,
      givens: [
        { sym: 'P', value: power, unit: '' },
        { sym: 'V_{pp,diff}', value: swing, unit: 'V' },
        { sym: 'V_{ov9}', value: vov9, unit: 'V' },
        { sym: '|V_{ov,P}|', value: vovP, unit: 'V' },
      ],
      unknowns: [
        { key: 'iss', sym: 'I_{SS}', label: 'Tail current', unit: 'A' },
        { key: 'vovN', sym: 'V_{ov,N}', label: 'NMOS overdrive', unit: 'V' },
        { key: 'wlN', sym: '(W/L)_{1-4}', label: 'NMOS size', unit: '' },
        { key: 'wlP', sym: '(W/L)_{5-8}', label: 'PMOS size', unit: '' },
        { key: 'av', sym: 'A_v', label: 'Gain', unit: 'V/V' },
      ],
      answers: { iss, vovN, wlN, wlP, av: t?.av ?? NaN },
      wrong: { vovN: [{ mistake: 'signFlip', value: proc.vdd - swing - vov9 - 2 * vovP }] },
      steps: [
        { tag: 'A', title: '1. Power → current', tex: `I_{SS} = \\frac{P}{V_{DD}} = ${texSI(power / 3, 'A')}`, produces: 'iss', value: power / 3 },
        { tag: 'A', title: '2–3. Swing → what is left for the NMOS stack (each output swings half the differential swing)', tex: `2V_{ov,N} = 3 - \\tfrac{${swing}}{2} - ${vov9} - 2(${vovP}) \\Rightarrow V_{ov,N} = ${texSI((3 - swing / 2 - vov9 - 2 * vovP) / 2, 'V')}`, produces: 'vovN', value: (3 - swing / 2 - vov9 - 2 * vovP) / 2 },
        { tag: 'A', title: '4. Sizes from the square law at ISS/2', tex: `\\left(\\tfrac{W}{L}\\right)_N = \\frac{2 I_D}{60\\mu\\,V_{ov,N}^2} = ${texNum((2 * id) / (60e-6 * vovN * vovN))}`, produces: 'wlN', value: (2 * id) / (60e-6 * vovN * vovN) },
        { tag: 'A', title: 'PMOS', tex: `\\left(\\tfrac{W}{L}\\right)_P = \\frac{2 I_D}{30\\mu\\,|V_{ov,P}|^2} = ${texNum((2 * id) / (30e-6 * vovP * vovP))}`, produces: 'wlP', value: (2 * id) / (30e-6 * vovP * vovP) },
        { tag: 'D', title: '5. Gain gm1 (gm3 rO3 rO1 ‖ gm5 rO5 rO7)', tex: `A_v = ${texNum(t?.av ?? NaN)}`, produces: 'av', value: t?.av ?? NaN },
      ],
      hints: ['Start with power, even if nobody asked.', 'Swing budget: VDD − swing/2 − Vov9 − 2|Vov,P| is what the two NMOS share.', 'W/L = 2ID/(µCox·Vov²); Av = gm1(Rdown ‖ Rup).', `ISS = ${(iss * 1e3).toFixed(2)} mA.`],
    };
    return { problem, sane: vovN > 0.08, why: 'no headroom left for the NMOS' };
  },
};

export const genFoldedDesign: Generator = {
  id: 'l4-folded',
  unit: 'L4',
  title: 'Design a folded cascode from power and swing',
  make(rng) {
    const proc: Process = { name: 'Set A', kpn: 134.28e-6, kpp: 38.36e-6, vthn: 0.7, vthp: 0.8, lambdan: 0.1, lambdap: 0.2, vdd: 3 };
    const power = pick(rng, [3, 4.5, 6, 9]) * 1e-3;
    const swing = nice(rng, 1.6, 2.8, 0.2);
    const vov1 = pick(rng, [0.2, 0.3, 0.4]);
    const itot = power / proc.vdd;
    const iss = itot / 2, i = iss / 2;
    const vov = (proc.vdd - swing / 2) / 4;
    const fc = foldedCascodePmosInput({ proc, iss, i, vov1, vovNcas: vov, vovNsrc: vov, vovPcas: vov, vovPsrc: vov });
    const problem: Problem = {
      ...base('l4-folded', 'L4', 'Design a folded cascode from power and swing'),
      statement: `Set A (VDD = 3 V). Design a PMOS-input folded cascode for ${power * 1e3} mW and a differential swing of ${swing.toFixed(1)} Vpp: half the current to the input pair, half to the two cascode branches; the four swing-critical devices share the headroom equally; |Vov1,2| = ${vov1} V. Find ISS, I, the overdrive, the NMOS source size and the gain.`,
      givens: [
        { sym: 'P', value: power, unit: '' },
        { sym: 'V_{pp,diff}', value: swing, unit: 'V' },
        { sym: '|V_{ov1,2}|', value: vov1, unit: 'V' },
      ],
      unknowns: [
        { key: 'iss', sym: 'I_{SS}', label: 'Tail current', unit: 'A' },
        { key: 'i', sym: 'I', label: 'Cascode branch current', unit: 'A' },
        { key: 'vov', sym: 'V_{ov}', label: 'Swing-critical overdrive', unit: 'V' },
        { key: 'wl5', sym: '(W/L)_{5,6}', label: 'NMOS source size', unit: '' },
        { key: 'av', sym: 'A_v', label: 'Gain (Gm = gm1)', unit: 'V/V' },
      ],
      answers: { iss, i, vov, wl5: fc.m5.wl, av: fc.av },
      wrong: { wl5: [{ mistake: 'issNotHalf', value: fc.m3.wl }], vov: [{ mistake: 'signFlip', value: (proc.vdd - swing) / 4 }] },
      steps: [
        { tag: 'A', title: 'Power → total current, split in two', tex: `I_{tot} = ${texSI(power / 3, 'A')},\\; I_{SS} = ${texSI(power / 3 / 2, 'A')}`, produces: 'iss', value: power / 3 / 2 },
        { tag: 'A', title: 'Each cascode branch gets I = ISS/2', tex: `I = ${texSI(power / 3 / 4, 'A')}`, produces: 'i', value: power / 3 / 4 },
        { tag: 'A', title: 'Four overdrives share VDD − swing/2', tex: `V_{ov} = \\frac{3 - ${texNum(swing / 2)}}{4} = ${texSI((3 - swing / 2) / 4, 'V')}`, produces: 'vov', value: (3 - swing / 2) / 4 },
        { tag: 'A', title: 'M5 carries ISS/2 + I', tex: `\\left(\\tfrac{W}{L}\\right)_5 = \\frac{2(I_{SS}/2 + I)}{134.28\\mu\\,V_{ov}^2} = ${texNum((2 * (iss / 2 + i)) / (134.28e-6 * vov * vov))}`, produces: 'wl5', value: (2 * (iss / 2 + i)) / (134.28e-6 * vov * vov) },
        { tag: 'D', title: 'Gain gm1 (Rup ‖ Rdown)', tex: `A_v \\approx ${texNum(fc.av)}`, produces: 'av', value: fc.av },
      ],
      hints: ['Folding costs current: two extra branches.', 'Only four devices in the output stack.', 'Vov = (VDD − swing/2)/4; ID5 = ISS/2 + I.', `ISS = ${(iss * 1e3).toFixed(2)} mA.`],
    };
    return { problem, sane: vov > 0.1 };
  },
};

export const HANDOUT_GENERATORS: Generator[] = [genGainError, genTeleDesign, genFoldedDesign];
