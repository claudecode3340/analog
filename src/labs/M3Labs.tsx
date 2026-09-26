/**
 * Milestone 3 labs (CLAUDE.md §8.3, 8.6, 8.7, 8.8): differential pair, five-transistor OTA,
 * feedback/Bode/settling, and the headroom stack. Every number from src/physics.
 */
import { useState } from 'react';
import { LogBars } from '../circuits/figures2';
import { BodePlot, DiffPairFig, FiveTOtaFig, HalfCircuitFig, StepPlot, SteeringPlot } from '../circuits/figures3';
import { VoltageLadder, type LadderBand, type LadderNode } from '../circuits/schematic';
import {
  closedLoopGain,
  cmGain,
  db,
  diffPairNodes,
  ex97,
  fiveTNodes,
  fiveTOtaQuiz,
  fiveTransistorOta,
  gainError,
  gmAtBalance,
  QUIZ1_C,
  regionFromNodesPure,
  SET_B,
  settlingTime,
  slewTime,
  splitInputs,
  steering,
  tauClosed,
  wlFromId,
} from '../physics';
import { formatSI } from '../practice/units';
import { Seg } from '../ui/Seg';
import { Readout, Slider } from '../ui/Slider';
import { LabShell } from './LabShell';

const V = (x: number) => formatSI(x, 'V');
const A = (x: number) => formatSI(x, 'A');
const Ohm = (x: number) => formatSI(x, 'Ω');
const S = (x: number) => formatSI(x, 'S');
const Hz = (x: number) => formatSI(x, 'Hz');

// ─── Differential pair lab ─────────────────────────────────────────────────

export function DiffPairLab() {
  const [vin1, setVin1] = useState(1.0);
  const [vin2, setVin2] = useState(1.0);
  const [load, setLoad] = useState<'rd' | 'diode' | 'current'>('rd');
  const [tail, setTail] = useState<'mirror' | 'rss'>('mirror');
  const [rd, setRd] = useState(5e3);
  const [rss, setRss] = useState(3e3);
  const [half, setHalf] = useState(false);
  const kp = 200e-6, wl = 20, iss = 200e-6, vth = 0.4, vdd = 1.8, lambda = 0.1;
  const wlTail = wlFromId(iss, kp, 0.2);
  const n = diffPairNodes({ kp, wl, vth, vdd, iss, rd, vin1, vin2, wlTail: tail === 'mirror' ? wlTail : undefined });
  const { vcm, vd } = splitInputs(vin1, vin2);
  const gm = gmAtBalance(kp, wl, iss);
  const ro = 1 / (lambda * (iss / 2));
  const loadR = load === 'rd' ? rd : load === 'diode' ? 1 / gmAtBalance(100e-6, 20, iss) : ro;
  const ad = gm * (1 / (1 / loadR + 1 / ro));
  const rtail = tail === 'rss' ? rss : ro * 2; // transistor tail: its rO at ISS
  const acm = cmGain({ gm, rd: loadR, rss: rtail });
  const vov = Math.sqrt(iss / (kp * wl));
  const reg = Object.fromEntries(Object.entries(n.devices).map(([k, d]) => [k, regionFromNodesPure(d)]));
  const challenges = [
    { id: 'cm', text: 'Move both inputs up together by 0.2 V. Do the drain currents change?', done: Math.abs(vd) < 0.002 && Math.abs(vcm - 1.0) >= 0.2 && reg.m1 === 'saturation' },
    { id: 'steer', text: 'Steer ALL the tail current into M1. How big must vd be?', done: n.id2 < 1e-9 },
    { id: 'low', text: 'With the transistor tail, lower the input CM until the tail leaves saturation.', done: tail === 'mirror' && reg.m3 === 'triode' },
    { id: 'high', text: 'Raise the input CM until M1 leaves saturation (its gate passes its drain + Vth).', done: load === 'rd' && reg.m1 === 'triode' && Math.abs(vd) < 0.05 },
    { id: 'half', text: 'Show the half circuits. Why does each half see 2RSS in common mode?', done: half },
  ];
  return (
    <LabShell
      title="Differential pair lab"
      intro="Two matched NMOS share a tail current. Move the inputs together (common mode) or apart (differential). Every transistor is live: hover it for its fence check."
      figures={
        <>
          <DiffPairFig vdd={vdd} iss={iss} kp={kp} wl={wl} vth={vth} vin1={vin1} vin2={vin2} rd={rd} load={load} kpp={100e-6} wlp={20} vthp={0.5} tail={tail === 'mirror' ? 'mirror' : 'rss'} rss={rss} wlTail={wlTail} r={(vdd - (vth + 0.2)) / iss} />
          <SteeringPlot kp={kp} wl={wl} iss={iss} dvin={vd} />
          {half && (
            <div className="lab-figures-row">
              <HalfCircuitFig mode="dm" rd={loadR} />
              <HalfCircuitFig mode="cm" rd={loadR} rss={rtail} />
            </div>
          )}
        </>
      }
      controls={
        <>
          <Seg label="Load" value={load} onChange={setLoad} options={[{ value: 'rd', label: 'Resistors RD' }, { value: 'diode', label: 'PMOS diodes' }, { value: 'current', label: 'PMOS sources' }]} />
          <Seg label="Tail" value={tail} onChange={setTail} options={[{ value: 'mirror', label: 'Transistor tail' }, { value: 'rss', label: 'Resistor RSS' }]} />
          <Slider label="Vin1" value={vin1} min={0.4} max={1.8} step={0.005} onChange={setVin1} format={V} />
          <Slider label="Vin2" value={vin2} min={0.4} max={1.8} step={0.005} onChange={setVin2} format={V} />
          {load === 'rd' && <Slider label="RD" value={rd} min={1e3} max={10e3} step={100} onChange={setRd} format={Ohm} />}
          {tail === 'rss' && <Slider label="RSS" value={rss} min={0.5e3} max={20e3} step={250} onChange={setRss} format={Ohm} />}
          <label className="small check">
            <input type="checkbox" checked={half} onChange={(e) => setHalf(e.target.checked)} /> Show the DM and CM half circuits
          </label>
          <div className="readouts">
            <Readout label="VCM / vd" value={`${V(vcm)} / ${V(vd)}`} />
            <Readout label="ID1 / ID2" value={`${A(n.id1)} / ${A(n.id2)}`} tone="signal" />
            <Readout label="full steering at" value={`±${V(Math.SQRT2 * vov)}`} />
            <Readout label="gm (balance)" value={S(gm)} />
            <Readout label="Ad = gm·(load ‖ rO)" value={ad.toFixed(2)} />
            <Readout label="ACM = −R/(1/gm + 2Rtail)" value={acm.toFixed(4)} />
            <Readout label="CMRR" value={`${db(ad / acm).toFixed(1)} dB`} tone="ok" />
          </div>
          <p className="small muted">µnCox 200 µA/V², W/L 20, Vth 0.4 V, ISS 200 µA, VDD 1.8 V, λ = 0.1 V⁻¹ (small signal). The transistor tail acts as a {Ohm(rtail / 2)} source resistance (its rO).</p>
        </>
      }
      challenges={challenges}
    />
  );
}

// ─── Five-transistor OTA lab ───────────────────────────────────────────────

const EXAM = fiveTOtaQuiz(QUIZ1_C);

export function OtaLab() {
  const [vcm, setVcm] = useState(1.1);
  const [vdm, setVdm] = useState(0); // mV
  const [issu, setIssu] = useState(120);
  const [clp, setClp] = useState(4);
  const [buffer, setBuffer] = useState(false);
  const [signal, setSignal] = useState(true);
  const iss = issu * 1e-6, cl = clp * 1e-12;
  const o = fiveTransistorOta({ proc: SET_B, iss, wl12: EXAM.design.wl12, wl34: EXAM.design.wl34, viss: Math.sqrt((2 * iss) / (SET_B.kpn * QUIZ1_C.wlTail)), cl });
  const n = fiveTNodes({ proc: SET_B, iss, wl12: EXAM.design.wl12, wl34: EXAM.design.wl34, wlTail: QUIZ1_C.wlTail, vinCm: vcm, vd: buffer ? 0 : vdm / 1000 });
  const bad = Object.entries(n.devices).filter(([k, d]) => k !== 'm6' && regionFromNodesPure(d) !== 'saturation').map(([k]) => k.toUpperCase());
  const s = steering({ kp: SET_B.kpn, wl: EXAM.design.wl12, iss, dvin: vdm / 1000 });
  const challenges = [
    { id: 'edges', text: 'Find both ends of the input CM range. Which transistor fails at each end?', done: bad.length > 0 },
    { id: 'signal', text: 'Push vd = +2 mV and follow the currents: +i, copied +i, −i, 2i into the output.', done: !buffer && vdm >= 2 },
    { id: 'buffer', text: 'Close the unity-gain loop. What happens to Rout and to the bandwidth?', done: buffer },
    { id: 'iss', text: 'Double ISS. What happens to GBW (∝ gm ∝ √ISS) and to the slew rate (∝ ISS)?', done: issu >= 240 },
    { id: 'exam', text: 'Set the exam values (ISS 120 µA, CL 4 pF) and read off answers (b)–(e).', done: issu === 120 && clp === 4 && buffer },
  ];
  return (
    <LabShell
      title="Five-transistor OTA lab"
      intro="Your exam OTA (Quiz 1 Part C sizes). Follow the signal currents through the mirror, sweep the input CM to find the range, and close the loop as a buffer."
      figures={
        <>
          <FiveTOtaFig proc={SET_B} iss={iss} wl12={EXAM.design.wl12} wl34={EXAM.design.wl34} wlTail={QUIZ1_C.wlTail} vinCm={vcm} vd={buffer ? 0 : vdm / 1000} bias signal={signal && !buffer} buffer={buffer} cl={cl} />
          <BodePlot a0={o.av} f0={o.f3dB!} beta={buffer ? 1 : undefined} />
        </>
      }
      controls={
        <>
          <Slider label="Vin,CM" value={vcm} min={0.5} max={1.7} step={0.005} onChange={setVcm} format={V} />
          {!buffer && <Slider label="vd = Vin1 − Vin2" value={vdm} min={-5} max={5} step={0.1} onChange={setVdm} format={(v) => `${v.toFixed(1)} mV`} />}
          <Slider label="ISS (= I1)" value={issu} min={40} max={400} step={10} onChange={setIssu} format={(v) => `${v} µA`} />
          <Slider label="CL" value={clp} min={0.5} max={10} step={0.5} onChange={setClp} format={(v) => `${v} pF`} />
          <label className="small check">
            <input type="checkbox" checked={buffer} onChange={(e) => setBuffer(e.target.checked)} /> Unity-gain buffer (Vout tied to Vin2)
          </label>
          <label className="small check">
            <input type="checkbox" checked={signal} onChange={(e) => setSignal(e.target.checked)} /> Show signal currents
          </label>
          <div className="readouts">
            <Readout label="saturated" value={bad.length ? `${bad.join(', ')} out ✗` : 'all ✓'} tone={bad.length ? 'bad' : 'ok'} />
            <Readout label="CM range" value={`${V(o.vinCmMin)} to ${V(o.vinCmMax)}`} />
            <Readout label="swing" value={`${V(o.voutMin)} to ${V(o.voutMax)}`} />
            <Readout label="i = gm·vd/2" value={A(s.id1 - iss / 2)} />
            <Readout label="gm1" value={S(o.gm1)} />
            <Readout label="Av = gm1(rO2 ‖ rO4)" value={o.av.toFixed(1)} tone="signal" />
            <Readout label={buffer ? 'Rout (buffer) ≈ 1/gm' : 'Rout = rO2 ‖ rO4'} value={Ohm(buffer ? o.bufferRout : o.rout)} />
            <Readout label={buffer ? 'bandwidth ≈ gm/(2πCL)' : 'f−3dB = 1/(2πRout·CL)'} value={Hz(buffer ? o.bufferF3dB! : o.f3dB!)} tone="signal" />
            <Readout label="GBW = gm/(2πCL)" value={Hz(o.omegaU! / (2 * Math.PI))} />
            <Readout label="SR = ISS/CL" value={`${(o.slewRate! / 1e6).toFixed(1)} V/µs`} />
          </div>
        </>
      }
      challenges={challenges}
    />
  );
}

// ─── Feedback, Bode and settling lab ───────────────────────────────────────

export function FeedbackLab() {
  const [a0db, setA0db] = useState(60);
  const [f0, setF0] = useState(100e3);
  const [acl, setAcl] = useState(10);
  const [eps, setEps] = useState(0.01);
  const [big, setBig] = useState(false);
  const [issu, setIssu] = useState(100);
  const a0 = 10 ** (a0db / 20);
  const beta = 1 / acl;
  const fu = a0 * f0;
  const wu = 2 * Math.PI * fu;
  const tau = tauClosed(beta, wu);
  const cl = 2e-12;
  const sr = (issu * 1e-6) / cl;
  const vstep = big ? 1 : 0.02;
  const err = gainError(a0, beta);
  const challenges = [
    { id: 'ex91', text: 'Razavi Ex 9.1: closed-loop gain 10 with under 1% gain error. Find the smallest A0 that works.', done: acl === 10 && err <= 0.01 && a0db <= 61 },
    { id: 'desens', text: 'Change A0 by 20 dB at Aclosed = 2. How much does the closed-loop gain change?', done: acl === 2 && a0db >= 70 },
    { id: 'gbw', text: 'Double the closed-loop gain. What happens to the closed-loop bandwidth?', done: acl >= 20 },
    { id: 'slew', text: 'Take a big step with a small ISS: see the ramp (slewing) before the curve.', done: big && slewTime(vstep, tau, sr) > 0 },
    { id: 'tight', text: 'Tighten the band from 1% to 0.1%. How many extra τ does it cost?', done: eps <= 0.001 },
  ];
  return (
    <LabShell
      title="Feedback, Bode and settling"
      intro="A one-pole op amp in a closed loop. The Bode plot shows the open-loop gain, the 1/β line and the closed-loop response; the step response shows the ε band, the 4.6τ/6.9τ settling and slewing."
      figures={
        <>
          <BodePlot a0={a0} f0={f0} beta={beta} />
          <StepPlot vstep={vstep} tau={tau} eps={eps} sr={sr} />
        </>
      }
      controls={
        <>
          <Slider label="A0 (open-loop DC gain)" value={a0db} min={20} max={100} step={1} onChange={setA0db} format={(v) => `${v} dB (${(10 ** (v / 20)).toFixed(0)})`} />
          <Slider label="f0 (open-loop pole)" value={f0} min={1e3} max={10e6} step={1e3} onChange={setF0} format={Hz} />
          <Slider label="Aclosed = 1/β" value={acl} min={1} max={50} step={1} onChange={setAcl} />
          <Seg label="Settling band" value={String(eps)} onChange={(v) => setEps(Number(v))} options={[{ value: '0.01', label: '1%' }, { value: '0.001', label: '0.1%' }]} />
          <Slider label="ISS (CL = 2 pF)" value={issu} min={10} max={500} step={10} onChange={setIssu} format={(v) => `${v} µA`} />
          <label className="small check">
            <input type="checkbox" checked={big} onChange={(e) => setBig(e.target.checked)} /> Big step (1 V)
          </label>
          <div className="readouts">
            <Readout label="exact Aclosed = A0/(1 + βA0)" value={closedLoopGain(a0, beta).toFixed(4)} tone="signal" />
            <Readout label="gain error ε = 1/(1 + βA0)" value={`${(err * 100).toFixed(3)} %`} tone={err <= 0.01 ? 'ok' : 'bad'} />
            <Readout label="loop gain βA0" value={(beta * a0).toFixed(1)} />
            <Readout label="GBW fu = A0·f0" value={Hz(fu)} />
            <Readout label="closed-loop bandwidth ≈ β·fu" value={Hz(beta * fu)} />
            <Readout label="τ = Aclosed/ωu" value={formatSI(tau, 's')} />
            <Readout label={`settling to ${eps * 100}%`} value={formatSI(slewTime(vstep, tau, sr) + settlingTime(tau, eps), 's')} tone="signal" />
            <Readout label="SR = ISS/CL" value={`${(sr / 1e6).toFixed(0)} V/µs`} />
          </div>
        </>
      }
      challenges={challenges}
    />
  );
}

// ─── Headroom stack ────────────────────────────────────────────────────────

type Preset = 'fiveT' | 'telescopic' | 'mirrorTele' | 'folded' | 'ex97';

interface Stack {
  vdd: number;
  /** From ground up to the output: [label, cost, kind] */
  below: Array<[string, number, LadderBand['kind']]>;
  /** From VDD down to the output. */
  above: Array<[string, number, LadderBand['kind']]>;
  note: string;
}

function stackFor(p: Preset, vovN: number, vovP: number, viss: number, vdd: number, vthp: number): Stack {
  switch (p) {
    case 'fiveT':
      return { vdd, below: [['VISS (M5)', viss, 'tail'], ['Vov2', vovN, 'n']], above: [['|Vov4|', vovP, 'p']], note: 'Exam OTA: floor Vov5 + Vov2 (input CM at its minimum), ceiling VDD − |Vov4|.' };
    case 'telescopic':
    case 'ex97':
      return { vdd, below: [['VISS (M9)', viss, 'tail'], ['Vov1', vovN, 'n'], ['Vov3', vovN, 'n']], above: [['|Vov7|', vovP, 'p'], ['|Vov5|', vovP, 'p']], note: 'Every stacked device costs its overdrive. Differential swing = 2 × (ceiling − floor).' };
    case 'mirrorTele':
      return { vdd, below: [['VISS', viss, 'tail'], ['Vov1', vovN, 'n'], ['Vov3', vovN, 'n']], above: [['|Vov8|', vovP, 'p'], ['|Vthp| (diode)', vthp, 'bad'], ['|Vov6|', vovP, 'p']], note: 'Fig 9.9: the diode-biased PMOS cascode costs an extra threshold at the top.' };
    case 'folded':
      return { vdd, below: [['Vov5', vovN, 'n'], ['Vov3', vovN, 'n']], above: [['|Vov9|', vovP, 'p'], ['|Vov7|', vovP, 'p']], note: 'Folded cascode: the input pair is not in the output stack, so only four overdrives. The tail no longer counts.' };
  }
}

const PRESET_VALUES: Record<Preset, { vovN: number; vovP: number; viss: number; vdd: number }> = {
  fiveT: { vovN: EXAM.design.vov1, vovP: EXAM.design.vov3, viss: EXAM.design.vov5, vdd: 1.8 },
  telescopic: { vovN: 0.2, vovP: 0.25, viss: 0.3, vdd: 1.8 },
  mirrorTele: { vovN: 0.2, vovP: 0.25, viss: 0.3, vdd: 3 },
  folded: { vovN: 0.2, vovP: 0.25, viss: 0.3, vdd: 1.8 },
  ex97: { vovN: 0.2, vovP: 0.3, viss: 0.5, vdd: 3 },
};

export function HeadroomLab() {
  const [preset, setPreset] = useState<Preset>('ex97');
  const [vals, setVals] = useState(PRESET_VALUES.ex97);
  const [vout, setVout] = useState(1.65);
  const choose = (p: Preset) => {
    setPreset(p);
    setVals(PRESET_VALUES[p]);
    const st = stackFor(p, PRESET_VALUES[p].vovN, PRESET_VALUES[p].vovP, PRESET_VALUES[p].viss, PRESET_VALUES[p].vdd, 0.5);
    const fl = st.below.reduce((a, b) => a + b[1], 0);
    const ce = st.vdd - st.above.reduce((a, b) => a + b[1], 0);
    setVout((fl + ce) / 2);
  };
  const st = stackFor(preset, vals.vovN, vals.vovP, vals.viss, vals.vdd, 0.5);
  const floor = st.below.reduce((a, b) => a + b[1], 0);
  const ceiling = st.vdd - st.above.reduce((a, b) => a + b[1], 0);
  const swing = ceiling - floor;
  // Bands: stack from the bottom; the device nearest the output is squeezed first.
  const bands: LadderBand[] = [];
  let y = 0;
  st.below.forEach(([label, cost, kind], i) => {
    const last = i === st.below.length - 1;
    const top = last ? Math.max(y, Math.min(vout, st.vdd)) : y + cost;
    bands.push({ from: y, to: top, label, kind: last && vout < floor - 1e-9 ? 'bad' : kind });
    y = top;
  });
  let t = st.vdd;
  st.above.forEach(([label, cost, kind], i) => {
    const last = i === st.above.length - 1;
    const bot = last ? Math.min(t, Math.max(vout, 0)) : t - cost;
    bands.push({ from: t, to: bot, label, kind: last && vout > ceiling + 1e-9 ? 'bad' : kind });
    t = bot;
  });
  const nodes: LadderNode[] = [
    { label: 'VDD', v: st.vdd },
    { label: 'ceiling', v: ceiling, tone: 'ok' },
    { label: 'Vout', v: vout, tone: vout < floor || vout > ceiling ? 'bad' : 'signal' },
    { label: 'floor', v: floor, tone: 'ok' },
  ];
  const e = ex97();
  const challenges = [
    { id: 'ex97', text: 'Ex 9.7 preset: confirm the book’s 0.9 V to 2.4 V output range (3 V differential).', done: preset === 'ex97' && Math.abs(floor - e.voutMin) < 1e-9 && Math.abs(ceiling - e.voutMax) < 1e-9 },
    { id: 'squeeze', text: 'Push Vout below the floor. Which device is squeezed first?', done: vout < floor },
    { id: 'diode', text: 'Mirror-loaded telescopic: how much swing does the diode’s threshold cost?', done: preset === 'mirrorTele' },
    { id: 'folded', text: 'Folded cascode: why does the tail no longer appear in the output stack?', done: preset === 'folded' },
    { id: 'vov', text: 'Halve the NMOS overdrive. How much swing do you win, and what does it cost (hint: W/L)?', done: vals.vovN <= PRESET_VALUES[preset].vovN / 2 + 1e-9 },
  ];
  return (
    <LabShell
      title="Headroom stack"
      intro="A room with a floor and a ceiling. Each stacked transistor needs its overdrive of breathing room, a diode costs a whole |VGS|, the tail costs VISS. What is left is the output swing."
      figures={
        <>
          <VoltageLadder vmax={st.vdd} nodes={nodes} bands={bands} h={420} title="Headroom stack: the swing left between floor and ceiling" />
          <LogBars
            title="Swing"
            unit="V/V"
            lo={0.1}
            hi={10}
            items={[
              { label: 'single-ended', value: Math.max(swing, 0.1001), tone: swing > 0 ? 'ok' : 'bad' },
              { label: 'differential', value: Math.max(2 * swing, 0.1001), tone: 'signal' },
            ]}
          />
        </>
      }
      controls={
        <>
          <Seg
            label="Circuit"
            value={preset}
            onChange={choose}
            options={[
              { value: 'fiveT', label: '5-T OTA (exam)' },
              { value: 'telescopic', label: 'Telescopic' },
              { value: 'ex97', label: 'Ex 9.7' },
              { value: 'mirrorTele', label: 'Mirror-loaded tele.' },
              { value: 'folded', label: 'Folded cascode' },
            ]}
          />
          <Slider label="VDD" value={vals.vdd} min={1.2} max={3.3} step={0.05} onChange={(v) => setVals({ ...vals, vdd: v })} format={V} />
          <Slider label="NMOS Vov" value={vals.vovN} min={0.05} max={0.5} step={0.01} onChange={(v) => setVals({ ...vals, vovN: v })} format={V} />
          <Slider label="PMOS |Vov|" value={vals.vovP} min={0.05} max={0.5} step={0.01} onChange={(v) => setVals({ ...vals, vovP: v })} format={V} />
          {preset !== 'folded' && <Slider label="VISS (tail)" value={vals.viss} min={0.1} max={0.6} step={0.01} onChange={(v) => setVals({ ...vals, viss: v })} format={V} />}
          <Slider label="Vout" value={vout} min={0} max={vals.vdd} step={0.01} onChange={setVout} format={V} />
          <div className="readouts">
            <Readout label="floor" value={V(floor)} />
            <Readout label="ceiling" value={V(ceiling)} />
            <Readout label="single-ended swing" value={V(swing)} tone={swing > 0 ? 'ok' : 'bad'} />
            <Readout label="differential p-p" value={V(2 * swing)} tone="signal" />
          </div>
          <p className="small muted">{st.note}</p>
        </>
      }
      challenges={challenges}
    />
  );
}
