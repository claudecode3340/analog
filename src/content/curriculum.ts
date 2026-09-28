/**
 * The curriculum map (CLAUDE.md §7). Foundations U0–U12, then the handout lectures L1–L14 with the
 * 1st→2nd edition mapping and a pointer to your own lecture notes (numbered by date).
 */
import type { Unit } from './types';

export const UNITS: Unit[] = [
  { id: 'U0', title: 'Circuit language', short: 'Voltage drops, dividers, parallel', group: 'foundations', lessons: ['u0-drops', 'u0-parallel'], prereqs: [], milestone: 1 },
  { id: 'U1', title: 'The MOSFET', short: 'Gate, channel, Vth, Vov, W/L', group: 'foundations', lessons: ['u1-mosfet'], prereqs: ['U0'], ref: 'Razavi §2.1–2.2', milestone: 1 },
  { id: 'U2', title: 'Triode, saturation, pinch-off', short: 'The waterfall and the fence', group: 'foundations', lessons: ['u2-pinchoff', 'u2-squarelaw'], prereqs: ['U1'], ref: 'Razavi §2.2–2.3', milestone: 1 },
  { id: 'U3', title: 'DC recipe and PMOS', short: 'Assume, solve, walk, check', group: 'foundations', lessons: ['u3-recipe', 'u3-pmos-design'], prereqs: ['U2'], ref: 'Razavi §2.2, Tutorial 1 Q1', milestone: 1 },
  { id: 'U4', title: 'Small signal', short: 'gm three ways, rO, gm·rO', group: 'foundations', lessons: ['u4-gm', 'u4-ro'], prereqs: ['U3'], ref: 'Razavi §2.4.3', milestone: 1 },
  { id: 'U5', title: 'First amplifier: common source', short: 'Gain is a slope; Av = −Gm·Rout', group: 'foundations', lessons: ['u5-cs'], prereqs: ['U4'], ref: 'Razavi §3.3.1', milestone: 1 },
  { id: 'U6', title: 'Impedance rules, sources, diodes, mirrors', short: 'Gate ∞, drain rO, source 1/gm', group: 'foundations', lessons: ['u6-rules', 'u6-mirror'], prereqs: ['U5'], ref: 'Razavi §3.3, Ch 5', milestone: 2 },
  { id: 'U7', title: 'CS with every load + degeneration', short: 'The ratio rule', group: 'foundations', lessons: ['u7-loads', 'u7-degen'], prereqs: ['U6'], ref: 'Razavi §3.3', milestone: 2 },
  { id: 'U8', title: 'Source follower and common gate', short: 'Gain 1, Rout 1/gm; gain gm·RD, Rin 1/gm', group: 'foundations', lessons: ['u8-follower', 'u8-cg'], prereqs: ['U7'], ref: 'Razavi §3.4–3.5', milestone: 2 },
  { id: 'U9', title: 'Cascode', short: 'Shielding, gm·rO², the load trap', group: 'foundations', lessons: ['u9-cascode', 'u9-telescopic'], prereqs: ['U8'], ref: 'Razavi §3.6', milestone: 2 },
  { id: 'U10', title: 'Differential pair', short: 'CM/DM, half circuit, 2RSS', group: 'foundations', lessons: ['u10-steering', 'u10-half', 'u10-cmrange'], prereqs: ['U9'], ref: 'Razavi Ch 4 · Tutorial 1', milestone: 3 },
  { id: 'U11', title: 'Five-transistor OTA', short: 'The mirror recovers the lost half', group: 'foundations', lessons: ['u11-ota', 'u11-ota-range'], prereqs: ['U10'], ref: 'Razavi §5.3 · Quiz 1', milestone: 3 },
  { id: 'U12', title: 'Poles and bandwidth', short: 'GBW = gm/CL', group: 'foundations', lessons: ['u12-poles', 'u12-settling'], prereqs: ['U11'], ref: 'Razavi Ch 6', milestone: 3 },
  { id: 'L1', title: 'Performance parameters', short: 'Gain error, settling, slewing, swing', group: 'handout', lessons: ['l1-gain', 'l1-speed', 'l1-other'], prereqs: ['U12'], ref: 'Handout L1 · 1st ed §9.1 · 2nd ed §9.1', notes: 'Your notes: Lec 01, Lec 02, settling example', milestone: 4 },
  { id: 'L2', title: 'One-stage op amps', short: '5-T OTA, telescopic, buffer window', group: 'handout', lessons: ['l2-onestage', 'l2-buffer'], prereqs: ['L1'], ref: 'Handout L2 · 1st ed §9.2.1 · 2nd ed §9.2.1', notes: 'Your notes: Lec 02, 03, 04', milestone: 4 },
  { id: 'L3', title: 'Design procedure', short: 'Power → swing → Vov → W/L → gain', group: 'handout', lessons: ['l3-design', 'l3-scaling'], prereqs: ['L2'], ref: 'Handout L3 · 1st ed §9.2.2–9.2.3 · 2nd ed §9.2.2–9.2.3', notes: 'Your notes: Lec 04', milestone: 4 },
  { id: 'L4', title: 'Folded cascode', short: 'Folding flips the inequality', group: 'handout', lessons: ['l4-folding', 'l4-gain'], prereqs: ['L3'], ref: 'Handout L4 · 1st ed §9.2.4–9.2.5 · 2nd ed §9.2.4–9.2.6', notes: 'Your notes: Lec 06', milestone: 4 },
  { id: 'L5', title: 'Two-stage op amp', short: 'High gain, then high swing', group: 'handout', lessons: ['l5-twostage'], prereqs: ['L4'], ref: 'Handout L5 · 1st ed §9.3 · 2nd ed §9.3', notes: 'Your notes: Lec 07', milestone: 5 },
  { id: 'L6', title: 'Gain boosting', short: 'Rout × (1 + A1)', group: 'handout', lessons: ['l6-boost'], prereqs: ['L5'], ref: 'Handout L6 · 1st ed §9.4 · 2nd ed §9.4', notes: 'Your notes: Lec 06–09 · Tutorial 4', milestone: 5 },
  { id: 'L7', title: 'CMFB: concept and sensing', short: 'Why fully differential outputs float', group: 'handout', lessons: ['l7-cmfb'], prereqs: ['L6'], ref: 'Handout L7 · 1st ed §9.7.1–9.7.2 · 2nd ed §9.7.1–9.7.2', notes: 'Your notes: Lec 09–11 · Tutorial 5', milestone: 5 },
  { id: 'L8', title: 'CMFB techniques', short: 'Triode sensing and the loop', group: 'handout', lessons: ['l8-cmfb', 'l8-replica'], prereqs: ['L7'], ref: 'Handout L8 · 1st ed §9.7.3 · 2nd ed §9.7.3', notes: 'Your notes: Lec 11–12 · Quiz 2', milestone: 5 },
  { id: 'L9', title: 'Input range and slew rate', short: 'SR = ISS/CL', group: 'handout', lessons: ['l9-slew'], prereqs: ['L8'], ref: 'Handout L9 · 1st ed §9.8–9.9 · 2nd ed §9.8–9.10', notes: 'Your notes: Lec 13–14 · Tutorial 6', milestone: 5 },
  { id: 'L10', title: 'PSRR and noise', short: 'Supply rejection, input-referred noise', group: 'handout', lessons: ['l10-psrr', 'l10-noise'], prereqs: ['L9'], ref: 'Handout L10 · 1st ed §9.11–9.12 · 2nd ed §9.11–9.12', notes: 'Not in your notes yet: built from Razavi', milestone: 5 },
  { id: 'L11', title: 'Stability I', short: 'Barkhausen, multi-pole systems', group: 'handout', lessons: ['l11-barkhausen', 'l11-multipole'], prereqs: ['L10'], ref: 'Handout L11 · 1st ed §10.1–10.2 · 2nd ed §10.1–10.2', notes: 'Your notes: Lec 14–15', milestone: 5 },
  { id: 'L12', title: 'Stability II', short: 'Phase and gain margin', group: 'handout', lessons: ['l12-margins', 'l12-ringing'], prereqs: ['L11'], ref: 'Handout L12 · 1st ed §10.3 · 2nd ed §10.3', notes: 'Your notes: Lec 15–16', milestone: 5 },
  { id: 'L13', title: 'Compensation I', short: 'Dominant pole, Miller, pole splitting', group: 'handout', lessons: ['l13-dominant', 'l13-miller'], prereqs: ['L12'], ref: 'Handout L13 · 1st ed §10.4 · 2nd ed §10.4–10.5', notes: 'Your notes: Lec 17', milestone: 5 },
  { id: 'L14', title: 'Compensation II', short: 'CC, the RHP zero, Rz, slewing', group: 'handout', lessons: ['l14-twostage', 'l14-rz'], prereqs: ['L13'], ref: 'Handout L14 · 1st ed §10.5 · 2nd ed §10.5–10.6', notes: 'Your notes: Lec 17 (start)', milestone: 5 },
];

/** Exam dates from the course handout. */
export const EXAMS = [
  { name: 'Mid-semester exam', date: '2026-10-09', note: '90 min · closed book · 60 marks' },
  { name: 'Quiz III', date: '2026-10-30', note: '30 min · open book' },
  { name: 'Quiz IV', date: '2026-11-20', note: '30 min · open book' },
  { name: 'Comprehensive', date: '2026-12-08', note: '3 h · closed book' },
];
