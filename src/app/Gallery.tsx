/**
 * Figure gallery (#/gallery): every parametric figure with representative props, used by the Playwright
 * diagram check at 1280 px and 390 px in light and dark mode.
 */
import {
  ChannelCrossSection,
  CsSmallSignal,
  IdVdsFamily,
  MosBias,
  NmosRd,
  ParallelPair,
  PmosRd,
  ResStack,
  SmallSignalModel,
  TransferCurve,
  WaterAnalogy,
} from '../circuits/figures';
import { CascodeFig, CommonGateFig, CsLoadFig, FollowerFig, ImpedanceFig, MirrorFig, TelescopicFig } from '../circuits/figures2';
import { DrawStyleContext } from '../circuits/primitives';
import { VoltageLadder } from '../circuits/schematic';
import { BodePlot, DiffPairFig, FiveTOtaFig, HalfCircuitFig, StepPlot, SteeringPlot } from '../circuits/figures3';
import { CmfbTriodeFig, FoldedCascodeFig, GainBoostFig, MirrorTeleFig, NonInvertingFig, TwoStageFig } from '../circuits/figures4';
import { EX_9_7, SET_A, ps1P6, tut4Q1, tut5Q1, ex97, fiveTOtaQuiz, QUIZ1_C, SET_B, tut1Q1, tut1Q4 } from '../physics';

const E97 = ex97();
const T1 = tut1Q1();
const T4 = tut1Q4();
const EXAM = fiveTOtaQuiz(QUIZ1_C);
const P6 = ps1P6();
const T41 = tut4Q1();
const T51 = tut5Q1();
const WL11 = (2 * 0.75e-3) / (SET_A.kpp * 0.4 * 0.4);

export const GALLERY_ITEMS: Array<{ id: string; title: string; el: React.ReactElement }> = [
  { id: 'water', title: 'Water analogy', el: <WaterAnalogy /> },
  { id: 'resstack', title: 'Resistor stack', el: <ResStack vdd={1.8} r1={10e3} r2={8e3} /> },
  { id: 'parallel', title: 'Parallel pair', el: <ParallelPair ra={10e3} rb={40e3} i={100e-6} /> },
  { id: 'mosbias', title: 'MOS bias', el: <MosBias vgs={0.7} vds={0.5} region="saturation" /> },
  { id: 'channel-tri', title: 'Channel, triode', el: <ChannelCrossSection vov={0.3} vds={0.1} maxVov={0.5} /> },
  { id: 'channel-sat', title: 'Channel, saturation', el: <ChannelCrossSection vov={0.3} vds={0.8} maxVov={0.5} /> },
  { id: 'channel-off', title: 'Channel, off', el: <ChannelCrossSection vov={-0.1} vds={0.5} maxVov={0.5} /> },
  { id: 'idvds', title: 'ID–VDS family', el: <IdVdsFamily kp={200e-6} wl={10} lambda={0.1} vovs={[0.1, 0.2, 0.3, 0.4]} op={{ vov: 0.3, vds: 0.8 }} /> },
  { id: 'nmosrd', title: 'NMOS + RD (WE1)', el: <NmosRd vdd={1.8} vg={0.7} rd={10e3} vd={0.9} region="saturation" current="90 µA" /> },
  { id: 'nmosrd-vin', title: 'NMOS + RD with vin', el: <NmosRd vdd={1.8} vg={0.7} rd={10e3} showVin /> },
  { id: 'pmosrd', title: 'PMOS + RD (WE3)', el: <PmosRd vdd={1.8} vg={0.9} rd={5e3} vd={0.8} region="saturation" current="160 µA" /> },
  { id: 'ssm', title: 'Small-signal model', el: <SmallSignalModel /> },
  { id: 'cs-ss', title: 'CS small signal', el: <CsSmallSignal /> },
  { id: 'transfer', title: 'CS transfer curve', el: <TransferCurve vdd={1.8} vth={0.4} kp={200e-6} wl={10} rd={10e3} vinQ={0.7} /> },
  { id: 'imp-gate', title: 'Into the gate', el: <ImpedanceFig terminal="gate" r={Infinity} /> },
  { id: 'imp-drain', title: 'Into the drain (degenerated)', el: <ImpedanceFig terminal="drain" rs={2e3} r={1.2e6} /> },
  { id: 'imp-source', title: 'Into the source (RD on drain)', el: <ImpedanceFig terminal="source" rd={10e3} r={1.8e3} /> },
  { id: 'mirror', title: 'Current mirror', el: <MirrorFig iref={20e-6} wlRef={10} wlOut={20} iout={40e-6} vgs={0.6} /> },
  ...(['resistor', 'diode', 'current', 'triode', 'active', 'degenerated'] as const).map((load) => ({
    id: `cs-${load}`,
    title: `CS, ${load} load`,
    el: <CsLoadFig load={load} vin={0.62} vout={0.9} id={90e-6} rd={10e3} rs={2e3} />,
  })),
  { id: 'follower', title: 'Source follower', el: <FollowerFig vin={1.2} vout={0.5} i={100e-6} /> },
  { id: 'cg', title: 'Common gate', el: <CommonGateFig vb={1} vout={1.2} vs={0.4} i={100e-6} rd={6e3} /> },
  ...(['resistor', 'current', 'cascode'] as const).map((load) => ({
    id: `cascode-${load}`,
    title: `Cascode, ${load} load`,
    el: <CascodeFig load={load} proc={SET_B} id={100e-6} wl={20} vb1={1.0} vout={1.1} rd={7e3} />,
  })),
  { id: 'telescopic', title: 'Telescopic (Ex 9.7)', el: <TelescopicFig proc={EX_9_7} iss={3e-3} wlN={E97.wlN} wlP={E97.wlP} wl9={E97.wl9} vinCm={E97.vinCm} vb1={E97.vb1} vb2={E97.vb2} vout={1.65} /> },
  {
    id: 'ladder',
    title: 'Voltage ladder (Ex 9.7)',
    el: (
      <VoltageLadder
        vmax={3}
        nodes={[
          { label: 'VDD', v: 3 },
          { label: 'Vb2', v: E97.vb2 },
          { label: 'Vout,max', v: E97.voutMax, tone: 'ok' },
          { label: 'Vb1', v: E97.vb1 },
          { label: 'Vin,CM', v: E97.vinCm, tone: 'signal' },
          { label: 'Vout,min', v: E97.voutMin, tone: 'ok' },
          { label: 'X', v: 0.7 },
          { label: 'P', v: 0.5 },
        ]}
        bands={[
          { from: 3, to: 2.7, label: '|Vov7| 0.3', kind: 'p' },
          { from: 2.7, to: 2.4, label: '|Vov5| 0.3', kind: 'p' },
          { from: 2.4, to: 0.9, label: 'swing 1.5 V', kind: 'swing' },
          { from: 0.9, to: 0.7, label: 'Vov3', kind: 'n' },
          { from: 0.7, to: 0.5, label: 'Vov1', kind: 'n' },
          { from: 0.5, to: 0, label: 'VISS 0.5', kind: 'tail' },
        ]}
      />
    ),
  },
  { id: 'dp-t1q1', title: 'Diff pair, mirror tail (Tut 1 Q1)', el: <DiffPairFig vdd={0.9} vss={-0.9} iss={0.2e-3} kp={400e-6} wl={T1.wl12} vth={0.35} vin1={0} vin2={0} rd={T1.rd} tail="mirror" wlTail={T1.wl3} r={T1.r} names={['Q1', 'Q2', 'Q3', 'Q4']} /> },
  { id: 'dp-t1q4', title: 'Diff pair, RSS tail (Tut 1 Q4)', el: <DiffPairFig vdd={5} iss={1e-3} kp={2.5e-3} wl={1} vth={0.7} vin1={T4.vcm} vin2={T4.vcm} rd={T4.rd} tail="rss" rss={1e3} names={['Q1', 'Q2']} /> },
  { id: 'dp-diode', title: 'Diff pair, diode loads (Tut 1 Q2)', el: <DiffPairFig vdd={1.8} iss={200e-6} kp={400e-6} wl={12.5} vth={0.5} vin1={0.9} vin2={0.9} load="diode" kpp={100e-6} wlp={50} vthp={0.5} names={['Q1', 'Q2', 'Q3', 'Q4']} /> },
  { id: 'dp-current', title: 'Diff pair, current-source loads (Tut 1 Q3)', el: <DiffPairFig vdd={1.8} iss={200e-6} kp={400e-6} wl={12.5} vth={0.5} vin1={0.9} vin2={0.9} load="current" kpp={100e-6} wlp={50} vthp={0.5} names={['Q1', 'Q2', 'Q3', 'Q4']} /> },
  { id: 'dp-steered', title: 'Diff pair, steered', el: <DiffPairFig vdd={1.8} iss={200e-6} kp={200e-6} wl={20} vth={0.4} vin1={1.0} vin2={0.9} rd={5e3} /> },
  { id: 'half-dm', title: 'DM half circuit', el: <HalfCircuitFig mode="dm" rd={3.2e3} /> },
  { id: 'half-cm', title: 'CM half circuit', el: <HalfCircuitFig mode="cm" rd={3.2e3} rss={1e3} /> },
  { id: 'ota-exam', title: '5-T OTA (exam, with bias)', el: <FiveTOtaFig proc={SET_B} iss={QUIZ1_C.iRef} wl12={EXAM.design.wl12} wl34={EXAM.design.wl34} wlTail={QUIZ1_C.wlTail} vinCm={1.1} bias cl={4e-12} /> },
  { id: 'ota-signal', title: '5-T OTA signal currents', el: <FiveTOtaFig proc={SET_B} iss={QUIZ1_C.iRef} wl12={EXAM.design.wl12} wl34={EXAM.design.wl34} wlTail={QUIZ1_C.wlTail} vinCm={1.1} signal cl={4e-12} /> },
  { id: 'ota-buffer', title: '5-T OTA buffer', el: <FiveTOtaFig proc={SET_B} iss={QUIZ1_C.iRef} wl12={EXAM.design.wl12} wl34={EXAM.design.wl34} wlTail={QUIZ1_C.wlTail} vinCm={1.1} buffer /> },
  { id: 'steering', title: 'Steering curve', el: <SteeringPlot kp={200e-6} wl={20} iss={200e-6} dvin={0.1} /> },
  { id: 'bode', title: 'Bode with 1/β', el: <BodePlot a0={1000} f0={1e5} beta={0.1} /> },
  { id: 'step', title: 'Step, slewing then settling', el: <StepPlot vstep={1} tau={5e-9} eps={0.01} sr={100e6} /> },
  { id: 'folded', title: 'Folded cascode (PS1 P6)', el: <FoldedCascodeFig proc={SET_A} iss={0.75e-3} i={0.375e-3} wl1={P6.m1.wl} wl3={P6.m3.wl} wl5={P6.m5.wl} wl7={P6.m7.wl} wl9={P6.m9.wl} wl11={WL11} vinCm={0.6} vout={1.5} /> },
  { id: 'mirrortele', title: 'Mirror-loaded telescopic (PS1 P5)', el: <MirrorTeleFig proc={SET_A} iss={1e-3} wlN={200} wlP={200} vinCm={1.2} vb1={1.6} vout={1.2} bias="diodes" /> },
  { id: 'mirrortele-vb2', title: 'Telescopic, Vb2 mirror, buffer (Tut 3 Q1)', el: <MirrorTeleFig proc={SET_A} iss={1e-3} wlN={200} wlP={200} vinCm={1.2} vb1={1.7} vout={1.3} bias="vb2" vb2={1.2} buffer /> },
  { id: 'twostage', title: 'Two-stage (Tut 3 Q2)', el: <TwoStageFig proc={SET_A} iss={1e-3} id2={1e-3} wl={200} vinCm={1.5} vout={1.5} /> },
  { id: 'noninv', title: 'Non-inverting amplifier', el: <NonInvertingFig r1={9e3} r2={1e3} a={1000} cl={2e-12} /> },
  { id: 'gainboost', title: 'Gain-boosted cascode (Tut 4 Q1)', el: <GainBoostFig vx={T41.vx} vg2={T41.vg2} vout={1.8} i1={100e-6} i2={0.5e-3} /> },
  { id: 'cmfb', title: 'Triode CMFB (Tut 5 Q1)', el: <CmfbTriodeFig vout1={1.5} vout2={1.5} vp={0.1} wl={T51.wl} /> },
];

export function Gallery() {
  return (
    <div className="page">
      <h1>Figure gallery</h1>
      {(['symbol', 'box'] as const).map((style) => (
        <DrawStyleContext.Provider key={style} value={style}>
          <h2>{style === 'symbol' ? 'Transistor symbols' : 'Simplified boxes'}</h2>
          <div className="gallery">
            {GALLERY_ITEMS.map((g) => (
              <figure key={g.id} className="gallery-item bench" data-fig={`${style}-${g.id}`}>
                {g.el}
                <figcaption className="small muted">{g.title}</figcaption>
              </figure>
            ))}
          </div>
        </DrawStyleContext.Provider>
      ))}
    </div>
  );
}
