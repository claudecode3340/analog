/**
 * Milestone 4 lab: the folded cascode (CLAUDE.md §8.9, folded part). Eleven live transistors, bias
 * sliders, the current divider at the folding node, Rup/Rdown/Rout, swing and input CM range.
 */
import { useState } from 'react';
import { LogBars } from '../circuits/figures2';
import { FoldedCascodeFig } from '../circuits/figures4';
import { foldedCascodePmosInput, foldedNodes, regionFromNodesPure, SET_A, wlFromId } from '../physics';
import { formatSI } from '../practice/units';
import { Readout, Slider } from '../ui/Slider';
import { LabShell } from './LabShell';

const V = (x: number) => formatSI(x, 'V');
const Ohm = (x: number) => formatSI(x, 'Ω');

export function FoldedLab() {
  const [issm, setIssm] = useState(0.75);
  const [im, setIm] = useState(0.375);
  const [vov, setVov] = useState(0.5);
  const [vov1, setVov1] = useState(0.3);
  const [vinCm, setVinCm] = useState(0.6);
  const [vout, setVout] = useState(1.5);
  const [dvbn, setDvbn] = useState(0);
  const proc = SET_A;
  const iss = issm * 1e-3, i = im * 1e-3;
  const fc = foldedCascodePmosInput({ proc, iss, i, vov1, vovNcas: vov, vovNsrc: vov, vovPcas: vov, vovPsrc: vov, viss: 0.4, cl: 2e-12 });
  const wl11 = wlFromId(iss, proc.kpp, 0.4);
  const base = foldedNodes({ proc, iss, i, wl1: fc.m1.wl, wl3: fc.m3.wl, wl5: fc.m5.wl, wl7: fc.m7.wl, wl9: fc.m9.wl, wl11, vinCm, vout });
  const vbn = base.vbn + dvbn;
  const n = foldedNodes({ proc, iss, i, wl1: fc.m1.wl, wl3: fc.m3.wl, wl5: fc.m5.wl, wl7: fc.m7.wl, wl9: fc.m9.wl, wl11, vinCm, vout, vbn });
  const bad = Object.entries(n.devices).filter(([, d]) => regionFromNodesPure(d) !== 'saturation').map(([k]) => k.toUpperCase());
  const challenges = [
    { id: 'ground', text: 'Take the input CM below 0 V. Does anything break? Why can a PMOS input do this?', done: vinCm < 0 && bad.length === 0 },
    { id: 'cmtop', text: 'Raise the input CM until the tail source runs out of room. Which device fails?', done: bad.includes('M11') },
    { id: 'same', text: 'Set input CM = output CM = 1.5 V with everything saturated (impossible in a telescopic).', done: Math.abs(vinCm - 1.5) < 0.02 && Math.abs(vout - 1.5) < 0.02 && bad.length === 0 },
    { id: 'vbn', text: 'Lower the NMOS cascode bias Vb1 by 0.1 V. Which device leaves saturation, and why?', done: dvbn <= -0.1 && bad.length > 0 },
    { id: 'divider', text: 'Raise the branch current I. Why does the fraction reaching the output fall slightly?', done: im >= 0.6 },
  ];
  return (
    <LabShell
      title="Folded-cascode lab"
      intro="Problem Set 1 P6 design (Set A, 4.5 mW, 2 Vpp). Eleven live transistors: move the input CM, the output level and the cascode bias and watch the fences; the bars show where the signal current goes."
      figures={
        <>
          <FoldedCascodeFig proc={proc} iss={iss} i={i} wl1={fc.m1.wl} wl3={fc.m3.wl} wl5={fc.m5.wl} wl7={fc.m7.wl} wl9={fc.m9.wl} wl11={wl11} vinCm={vinCm} vout={vout} vbn={vbn} />
          <div className="splitbar" aria-label={`${(fc.fraction * 100).toFixed(1)}% of M1’s signal current reaches the output`}>
            <div className="splitbar-a" style={{ width: `${fc.fraction * 100}%` }}>
              to the output {(fc.fraction * 100).toFixed(1)}%
            </div>
            <div className="splitbar-b" />
          </div>
          <LogBars
            lo={1e3}
            hi={1e8}
            title="Folded cascode resistances"
            items={[
              { label: '1/gm3', value: 1 / fc.m3.gm, tone: 'n' },
              { label: 'rO1 ‖ rO5', value: 1 / (1 / fc.m1.rO + 1 / fc.m5.rO), tone: 'muted' },
              { label: 'R down', value: fc.rDown, tone: 'n' },
              { label: 'R up', value: fc.rUp, tone: 'p' },
              { label: 'Rout', value: fc.rout, tone: 'signal' },
            ]}
          />
        </>
      }
      controls={
        <>
          <Slider label="ISS (input pair)" value={issm} min={0.2} max={2} step={0.05} onChange={setIssm} format={(v) => `${v.toFixed(2)} mA`} />
          <Slider label="I (each cascode branch)" value={im} min={0.1} max={1.5} step={0.025} onChange={setIm} format={(v) => `${v.toFixed(3)} mA`} />
          <Slider label="swing-critical overdrive" value={vov} min={0.15} max={0.6} step={0.01} onChange={setVov} format={V} />
          <Slider label="input |Vov1,2|" value={vov1} min={0.1} max={0.6} step={0.01} onChange={setVov1} format={V} />
          <Slider label="Vin,CM" value={vinCm} min={-0.8} max={2.2} step={0.01} onChange={setVinCm} format={V} />
          <Slider label="Vout" value={vout} min={0.5} max={2.5} step={0.01} onChange={setVout} format={V} />
          <Slider label="Vb1 shift" value={dvbn} min={-0.3} max={0.3} step={0.01} onChange={setDvbn} format={(v) => `${v >= 0 ? '+' : ''}${v.toFixed(2)} V`} />
          <div className="readouts">
            <Readout label="saturated" value={bad.length ? `${bad.join(', ')} out ✗` : 'all 11 ✓'} tone={bad.length ? 'bad' : 'ok'} />
            <Readout label="power" value={`${(fc.power * 1e3).toFixed(2)} mW`} />
            <Readout label="M5,6 carry ISS/2 + I" value={formatSI(fc.idSrc, 'A')} />
            <Readout label="Rout = Rup ‖ Rdown" value={Ohm(fc.rout)} />
            <Readout label="Av (Gm = gm1 / exact)" value={`${fc.av.toFixed(0)} / ${fc.avExact.toFixed(0)}`} tone="signal" />
            <Readout label="output range" value={`${V(fc.voutMin)} to ${V(fc.voutMax)}`} />
            <Readout label="input CM range" value={`${V(fc.vinCmMin)} to ${V(fc.vinCmMax!)}`} />
            <Readout label="ωu = gm1/CL (CL 2 pF)" value={formatSI(fc.omegaU!, 'rad/s')} />
          </div>
        </>
      }
      challenges={challenges}
    />
  );
}
