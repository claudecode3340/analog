/**
 * Global glossary: every symbol in CLAUDE.md §6, defined once, hoverable everywhere.
 * Lesson text refers to entries as {{key}}.
 */
export interface GlossaryEntry {
  tex: string;
  name: string;
  def: string;
  unit?: string;
  firstIn: string; // lesson id where it is introduced
}

export const GLOSSARY: Record<string, GlossaryEntry> = {
  VDD: { tex: 'V_{DD}', name: 'supply voltage', def: 'The positive supply rail: the top of the tank. Every node voltage is measured from ground up to it.', unit: 'V', firstIn: 'u0-drops' },
  VSS: { tex: 'V_{SS}', name: 'negative supply', def: 'The bottom rail when a circuit uses a split supply (e.g. −0.9 V).', unit: 'V', firstIn: 'u0-drops' },
  ground: { tex: '0\\,\\mathrm{V}', name: 'ground', def: 'The reference node, 0 V. Sea level in the water picture.', firstIn: 'u0-drops' },
  I: { tex: 'I', name: 'current', def: 'Flow of charge through a branch, in amperes. The same current flows through everything in series.', unit: 'A', firstIn: 'u0-drops' },
  R: { tex: 'R', name: 'resistance', def: 'How hard it is to push current through: V = I·R. A narrow pipe.', unit: 'Ω', firstIn: 'u0-drops' },
  par: { tex: 'R_1 \\parallel R_2', name: 'parallel', def: 'Two resistors across the same two nodes: R1R2/(R1 + R2). Always smaller than either; the smallest resistance wins.', firstIn: 'u0-parallel' },
  VG: { tex: 'V_G', name: 'gate voltage', def: 'Voltage of the gate node, measured from ground.', unit: 'V', firstIn: 'u1-mosfet' },
  VD: { tex: 'V_D', name: 'drain voltage', def: 'Voltage of the drain node, measured from ground.', unit: 'V', firstIn: 'u1-mosfet' },
  VS: { tex: 'V_S', name: 'source voltage', def: 'Voltage of the source node, measured from ground.', unit: 'V', firstIn: 'u1-mosfet' },
  VGS: { tex: 'V_{GS}', name: 'gate-source voltage', def: 'VG − VS: how hard the gate is pulling electrons into the channel.', unit: 'V', firstIn: 'u1-mosfet' },
  VDS: { tex: 'V_{DS}', name: 'drain-source voltage', def: 'VD − VS: the voltage that pushes electrons along the channel.', unit: 'V', firstIn: 'u1-mosfet' },
  Vth: { tex: 'V_{th}', name: 'threshold voltage', def: 'The VGS at which a channel first forms. Below it the device is off. Vthn for NMOS, |Vthp| for PMOS.', unit: 'V', firstIn: 'u1-mosfet' },
  Vov: { tex: 'V_{ov}', name: 'overdrive', def: 'Vov = VGS − Vth: how far past threshold the gate is. Sets the channel thickness. The most important number in the course.', unit: 'V', firstIn: 'u1-mosfet' },
  WL: { tex: 'W/L', name: 'aspect ratio', def: 'Channel width over length: the size of the tap. You choose it when you design.', firstIn: 'u1-mosfet' },
  muCox: { tex: '\\mu_n C_{ox}', name: 'process transconductance', def: 'Mobility × oxide capacitance per area, fixed by the process (µnCox for NMOS, µpCox for PMOS). Given as one number, e.g. 200 µA/V².', unit: 'A/V²', firstIn: 'u1-mosfet' },
  ID: { tex: 'I_D', name: 'drain current', def: 'Current flowing into the drain and out of the source (NMOS).', unit: 'A', firstIn: 'u2-squarelaw' },
  lambda: { tex: '\\lambda', name: 'channel-length modulation', def: 'The small upward slope of the “flat” saturation curve. λ ∝ 1/L. Gives the device a finite rO.', unit: 'V⁻¹', firstIn: 'u2-squarelaw' },
  pinch: { tex: 'V_{DS} = V_{ov}', name: 'pinch-off', def: 'The point where the channel thickness at the drain end reaches zero. Beyond it the device is saturated.', firstIn: 'u2-pinchoff' },
  fence: { tex: 'V_D \\ge V_G - V_{th}', name: 'the saturation fence', def: 'NMOS is saturated when its drain stays above its gate minus one threshold. PMOS: VD ≤ VG + |Vth|.', firstIn: 'u2-pinchoff' },
  gm: { tex: 'g_m', name: 'transconductance', def: 'How much drain current changes per volt of gate wiggle: gm = 2ID/Vov = √(2µCox(W/L)ID) = µCox(W/L)Vov.', unit: 'S (A/V)', firstIn: 'u4-gm' },
  rO: { tex: 'r_O', name: 'output resistance', def: 'The small-signal resistance looking into the drain: rO = 1/(λID).', unit: 'Ω', firstIn: 'u4-ro' },
  gmro: { tex: 'g_m r_O', name: 'intrinsic gain', def: 'The largest gain one transistor can give: gm·rO = 2/(λVov). At a fixed overdrive it does not depend on ID.', firstIn: 'u4-ro' },
  Av: { tex: 'A_v', name: 'voltage gain', def: 'vout/vin for small signals. Negative means the stage inverts.', unit: 'V/V', firstIn: 'u5-cs' },
  Gm: { tex: 'G_m', name: 'stage transconductance', def: 'Output short-circuit current per input volt, for a whole stage.', unit: 'S', firstIn: 'u5-cs' },
  Rout: { tex: 'R_{out}', name: 'output resistance', def: 'Resistance seen looking into the output node with the input grounded.', unit: 'Ω', firstIn: 'u5-cs' },
  RS: { tex: 'R_S', name: 'source resistor', def: 'A resistor under the source (degeneration). It fights back: raises Rout (up multiplies) and lowers Gm.', unit: 'Ω', firstIn: 'u6-rules' },
  Rdown: { tex: 'R_{down}', name: 'resistance looking down', def: 'From the output node down into the NMOS stack. For a cascode ≈ gm·rO·rO.', unit: 'Ω', firstIn: 'u9-cascode' },
  Rup: { tex: 'R_{up}', name: 'resistance looking up', def: 'From the output node up into the PMOS load. rO for a simple source, ≈ gm·rO² for a cascoded one.', unit: 'Ω', firstIn: 'u9-cascode' },
  VISS: { tex: 'V_{ISS}', name: 'tail headroom', def: 'The voltage the tail current source needs across it to stay saturated (its Vov for a transistor tail). Not a supply.', unit: 'V', firstIn: 'u9-telescopic' },
  ISS: { tex: 'I_{SS}', name: 'tail current', def: 'The current of the source under a differential pair. At balance each side carries ISS/2.', unit: 'A', firstIn: 'u10-steering' },
  VCM: { tex: 'V_{CM}', name: 'common-mode voltage', def: 'The average of the two inputs, (Vin1 + Vin2)/2. The pair ignores it (within its CM range).', unit: 'V', firstIn: 'u10-steering' },
  vd: { tex: 'v_d', name: 'differential input', def: 'The difference Vin1 − Vin2. The pair amplifies this.', unit: 'V', firstIn: 'u10-steering' },
  Ad: { tex: 'A_d', name: 'differential gain', def: 'Output difference per input difference. From the DM half circuit: gm·(load).', unit: 'V/V', firstIn: 'u10-half' },
  ACM: { tex: 'A_{CM}', name: 'common-mode gain', def: 'How much an output moves when both inputs move together. Small; from the CM half circuit with 2RSS.', unit: 'V/V', firstIn: 'u10-half' },
  CL: { tex: 'C_L', name: 'load capacitance', def: 'The capacitor at the output node: it sets the dominant pole and the slew rate.', unit: 'F', firstIn: 'u12-poles' },
  omegau: { tex: '\\omega_u', name: 'unity-gain frequency (GBW)', def: 'Where the open-loop gain falls to 1. One-stage op amp: gm/CL. In Hz divide by 2π.', unit: 'rad/s', firstIn: 'u12-poles' },
  tau: { tex: '\\tau', name: 'time constant', def: 'Closed-loop settling time constant: 1/(β·ωu) = Aclosed/ωu.', unit: 's', firstIn: 'u12-settling' },
  eps: { tex: '\\varepsilon', name: 'error', def: 'The fraction still missing: gain error 1/(1 + βA), or the settling band (0.01 = 1%).', firstIn: 'u12-settling' },
  beta: { tex: '\\beta', name: 'feedback factor', def: 'The fraction of the output fed back to the input. A divider R2/(R1 + R2); 1 for a buffer.', firstIn: 'u12-settling' },
  SR: { tex: 'SR', name: 'slew rate', def: 'The fastest the output can move: SR = ISS/CL for a one-stage OTA.', unit: 'V/s', firstIn: 'u12-settling' },
  Aopen: { tex: 'A_{open}', name: 'open-loop gain', def: 'The op amp’s own gain, with no feedback. Huge but sloppy: it changes with temperature and process.', firstIn: 'l1-gain' },
  Aclosed: { tex: 'A_{closed}', name: 'closed-loop gain', def: 'The gain with feedback: A/(1 + βA) ≈ 1/β, set by resistors.', firstIn: 'l1-gain' },
  RD: { tex: 'R_D', name: 'drain resistor', def: 'Load resistor from VDD to the drain.', unit: 'Ω', firstIn: 'u3-recipe' },
};
