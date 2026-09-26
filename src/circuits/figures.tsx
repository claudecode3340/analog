/**
 * Parametric figures for Milestone 1 (U0–U5). Each takes physical values as props and draws them live.
 * Layout rule: device names and region badges sit on one side, resistor labels on the other, and node
 * voltage tags sit on the wire side away from both, so labels never collide.
 */
import { formatSI } from '../practice/units';
import { idSat, idTriode, region as regionOf, solveNmosRd, type Region } from '../physics';
import {
  Canvas,
  CurrentArrow,
  Dot,
  Ground,
  Label,
  Nmos,
  Pmos,
  Rail,
  Resistor,
  Sym,
  Terminal,
  VoltageSource,
  VoltageTag,
  Wire,
  stroke,
} from './primitives';
import { Plot } from './Plot';

const V = (x: number) => formatSI(x, 'V');
const R = (x: number) => formatSI(x, 'Ω');
const I = (x: number) => formatSI(x, 'A');

// ─── U0 ────────────────────────────────────────────────────────────────────

/** Water analogy: VDD is a tank's water height, a resistor is a narrow pipe, ground is sea level. */
export function WaterAnalogy({ height = 1.8, highlight }: { height?: number; highlight?: string[] }) {
  const top = 40;
  const sea = 200;
  const level = sea - (height / 2) * 140;
  return (
    <Canvas w={420} h={230} title="Water analogy: voltage is height, current is flow, a resistor is a narrow pipe" highlight={highlight} maxWidth={520}>
      {/* sea */}
      <rect x={250} y={sea} width={160} height={24} fill="color-mix(in srgb, var(--pmos) 25%, var(--paper))" />
      <Label x={330} y={sea + 16} text="sea level = ground (0 V)" anchor="middle" size={12} />
      {/* tank */}
      <rect x={30} y={top} width={90} height={sea - top} fill="none" stroke="var(--ink)" strokeWidth={1.5} />
      <rect x={31} y={level} width={88} height={sea - level} fill="color-mix(in srgb, var(--pmos) 30%, var(--paper))" />
      <Label x={75} y={level - 8} text={`water height = ${height} V`} anchor="middle" size={12} weight={600} />
      <Label x={75} y={sea + 16} text="tank = supply" anchor="middle" size={12} />
      {/* pipe with a narrow section */}
      <path d={`M120 ${sea - 20} H175 V${sea - 14} H215 V${sea - 20} H250`} fill="none" stroke="var(--ink)" strokeWidth={1.5} />
      <path d={`M120 ${sea - 4} H175 V${sea - 10} H215 V${sea - 4} H250`} fill="none" stroke="var(--ink)" strokeWidth={1.5} />
      <Label x={195} y={sea - 28} text="narrow pipe = resistor" anchor="middle" size={12} />
      <CurrentArrow x={150} y={sea - 12} dir="right" />
      <Label x={190} y={sea + 16} text="flow = current" anchor="middle" size={12} color="var(--signal)" />
    </Canvas>
  );
}

/** Two resistors in series from VDD to ground with the middle node A. */
export function ResStack({ vdd, r1, r2, showValues = true, highlight }: { vdd: number; r1: number; r2: number; showValues?: boolean; highlight?: string[] }) {
  const i = vdd / (r1 + r2);
  const va = vdd - i * r1;
  return (
    <Canvas w={280} h={200} title="Two resistors in series from VDD to ground" highlight={highlight}>
      <Rail x1={100} x2={180} y={24} label={`VDD = ${V(vdd)}`} />
      <Resistor x={140} y1={24} y2={96} label={<Sym base="R" sub="1" />} value={R(r1)} id="r1" />
      <Dot x={140} y={96} id="nodeA" />
      <Label x={130} y={100} text="A" anchor="end" weight={600} />
      {showValues && <VoltageTag x={128} y={116} v={`VA = ${V(va)}`} anchor="end" id="nodeA" />}
      <Resistor x={140} y1={96} y2={168} label={<Sym base="R" sub="2" />} value={R(r2)} id="r2" />
      <Ground x={140} y={168} />
      <CurrentArrow x={140} y={36} dir="down" />
      {showValues && <Label x={130} y={48} text={`I = ${I(i)}`} anchor="end" mono size={12} color="var(--signal)" bg />}
    </Canvas>
  );
}

/** Current I into a node with RA and RB to ground. */
export function ParallelPair({ ra, rb, i, highlight }: { ra: number; rb: number; i: number; highlight?: string[] }) {
  return (
    <Canvas w={300} h={180} title="A current splitting between two parallel resistors" highlight={highlight}>
      <Wire points={[[30, 40], [210, 40]]} />
      <Terminal x={30} y={40} />
      <CurrentArrow x={70} y={40} dir="right" label={`I = ${I(i)}`} />
      <Dot x={130} y={40} />
      <Dot x={210} y={40} />
      <Resistor x={130} y1={40} y2={140} label={<Sym base="R" sub="A" />} value={R(ra)} labelSide="left" id="ra" />
      <Resistor x={210} y1={40} y2={140} label={<Sym base="R" sub="B" />} value={R(rb)} id="rb" />
      <Wire points={[[130, 140], [210, 140]]} />
      <Ground x={170} y={140} />
    </Canvas>
  );
}

// ─── U2: the device ────────────────────────────────────────────────────────

/** An NMOS with a VGS source on its gate and a VDS source on its drain. */
export function MosBias({ vgs, vds, region, highlight }: { vgs: number; vds: number; region?: Region; highlight?: string[] }) {
  return (
    <Canvas w={320} h={180} title="NMOS biased by a gate-source source VGS and a drain-source source VDS" highlight={highlight}>
      <Nmos x={170} y={90} name="M1" id="m1" region={region} />
      <Wire points={[[140, 90], [80, 90]]} />
      <VoltageSource x={80} y1={90} y2={150} label={`VGS = ${V(vgs)}`} />
      <Wire points={[[170, 60], [170, 30], [250, 30]]} />
      <VoltageSource x={250} y1={30} y2={150} />
      <Label x={268} y={94} text={`VDS = ${V(vds)}`} />
      <Wire points={[[170, 120], [170, 150]]} />
      <Wire points={[[80, 150], [250, 150]]} />
      <Ground x={170} y={150} />
    </Canvas>
  );
}

/**
 * Cross-section with the channel drawn to scale: thickness at position x ∝ local overdrive Vov − V(x),
 * from the gradual-channel solution. In saturation the channel pinches off before the drain.
 */
export function ChannelCrossSection({ vov, vds, maxVov = 1 }: { vov: number; vds: number; maxVov?: number }) {
  const W = 420;
  const x0 = 110; // source edge
  const x1 = 310; // drain edge
  const surf = 110; // silicon surface
  const L = x1 - x0;
  const on = vov > 0;
  const vdEff = Math.min(Math.max(vds, 0), Math.max(vov, 0));
  const sat = on && vds >= vov;
  // Pinch-off point creeps toward the source as VDS grows beyond Vov (channel-length modulation, exaggerated).
  const Leff = sat ? L * (1 - 0.12 * Math.min(1, (vds - vov) / 1.0)) : L;
  const maxT = 26;
  const scale = maxT / Math.max(maxVov, 0.05);
  const pts: Array<[number, number]> = [];
  if (on) {
    const k = vov * vdEff - (vdEff * vdEff) / 2;
    const N = 40;
    for (let n = 0; n <= N; n++) {
      const f = n / N;
      const q = Math.sqrt(Math.max(0, vov * vov - 2 * f * k)); // = Vov − V(x)
      pts.push([x0 + f * Leff, surf + q * scale]);
    }
  }
  const poly = on ? [[x0, surf] as [number, number], ...pts, [x0 + Leff, surf] as [number, number]] : [];
  const reg = regionOf(vov, vds);
  return (
    <Canvas w={W} h={220} title={`MOSFET cross-section: channel ${reg === 'saturation' ? 'pinched off near the drain' : reg === 'triode' ? 'continuous from source to drain' : 'absent'}`} maxWidth={560}>
      {/* substrate */}
      <rect x={40} y={surf} width={340} height={90} fill="color-mix(in srgb, var(--muted) 14%, var(--paper))" stroke="var(--ink)" strokeWidth={1} />
      <Label x={210} y={surf + 80} text="p-type body" anchor="middle" size={12} color="var(--ink-2)" />
      {/* n+ wells */}
      <path d={`M60 ${surf} H${x0 + 8} V${surf + 30} Q${x0 + 8} ${surf + 40} ${x0 - 4} ${surf + 40} H60 Z`} fill="color-mix(in srgb, var(--nmos) 35%, var(--paper))" stroke="var(--nmos)" />
      <path d={`M${x1 - 8} ${surf} H360 V${surf + 40} H${x1 + 4} Q${x1 - 8} ${surf + 40} ${x1 - 8} ${surf + 30} Z`} fill="color-mix(in srgb, var(--nmos) 35%, var(--paper))" stroke="var(--nmos)" />
      <Label x={82} y={surf + 25} text="n+" size={12} color="var(--nmos)" weight={600} />
      <Label x={322} y={surf + 25} text="n+" size={12} color="var(--nmos)" weight={600} />
      {/* channel */}
      {on && <polygon points={poly.map((p) => p.join(',')).join(' ')} fill="var(--signal)" opacity={0.75} />}
      {sat && (
        <>
          <line x1={x0 + Leff} y1={surf - 2} x2={x0 + Leff} y2={surf + 34} stroke="var(--bad)" strokeDasharray="3 3" />
          <Label x={x0 + Leff - 4} y={surf + 48} text="pinch-off" anchor="end" size={11} color="var(--bad)" weight={600} bg />
        </>
      )}
      {/* oxide and gate */}
      <rect x={x0} y={surf - 10} width={L} height={10} fill="color-mix(in srgb, #e0c060 55%, var(--paper))" stroke="var(--ink)" strokeWidth={1} />
      <rect x={x0} y={surf - 30} width={L} height={20} fill="color-mix(in srgb, var(--ink) 70%, var(--paper))" />
      <Label x={210} y={surf - 16} text="gate" anchor="middle" size={12} color="var(--paper)" weight={600} />
      <Label x={x0 + L + 4} y={surf - 1} text="oxide" size={10} color="var(--ink-2)" />
      {/* terminals */}
      <Wire points={[[85, surf], [85, 40]]} />
      <Label x={85} y={34} text="S" anchor="middle" weight={600} />
      <Wire points={[[210, surf - 30], [210, 40]]} />
      <Label x={210} y={34} text="G" anchor="middle" weight={600} />
      <Wire points={[[348, surf], [348, 40]]} />
      <Label x={348} y={34} text="D" anchor="middle" weight={600} />
      <Label x={124} y={60} text={`Vov = ${V(vov)}`} mono size={12} />
      <Label x={296} y={60} text={`VDS = ${V(vds)}`} mono size={12} anchor="end" />
      <Label x={210} y={surf + 64} text={reg === 'off' ? 'no channel: OFF' : reg === 'triode' ? 'channel reaches the drain: TRIODE' : 'channel pinched off: SATURATION'} anchor="middle" size={12} weight={600} color={reg === 'saturation' ? 'var(--ok)' : 'var(--bad)'} bg />
    </Canvas>
  );
}

/** ID–VDS family for several overdrives, with the pinch-off locus VDS = Vov and a live operating point. */
export function IdVdsFamily({ kp, wl, lambda = 0, vovs, op, vdsMax = 1.5 }: { kp: number; wl: number; lambda?: number; vovs: number[]; op?: { vov: number; vds: number }; vdsMax?: number }) {
  const N = 60;
  const series = vovs.map((vov, i) => {
    const pts: Array<[number, number]> = [];
    for (let n = 0; n <= N; n++) {
      const vds = (n / N) * vdsMax;
      const id = vds < vov ? idTriode(kp, wl, vov, vds) : idSat(kp, wl, vov, lambda, vds);
      pts.push([vds, id * 1e6]);
    }
    return { points: pts, color: op && Math.abs(op.vov - vov) < 1e-9 ? 'var(--signal)' : i % 2 ? 'var(--nmos)' : 'var(--ink-2)', width: op && Math.abs(op.vov - vov) < 1e-9 ? 2.5 : 1.6, label: `Vov ${vov.toFixed(2)}` };
  });
  const vmax = Math.max(...vovs, op?.vov ?? 0);
  const idMax = idSat(kp, wl, vmax, lambda, vdsMax) * 1e6 * 1.12;
  const locus: Array<[number, number]> = [];
  for (let n = 0; n <= N; n++) {
    const v = (n / N) * Math.min(vdsMax, vmax * 1.05);
    locus.push([v, idSat(kp, wl, v, lambda, v) * 1e6]);
  }
  series.push({ points: locus, color: 'var(--bad)', width: 1.2, dashed: true, label: '' } as never);
  const markers = op
    ? [
        {
          x: op.vds,
          y: (op.vds < op.vov ? idTriode(kp, wl, op.vov, op.vds) : idSat(kp, wl, op.vov, lambda, op.vds)) * 1e6,
          label: 'Q',
          labelPos: 'above' as const,
        },
      ]
    : [];
  return (
    <Plot
      title="ID versus VDS for several overdrives"
      xRange={[0, vdsMax]}
      yRange={[0, idMax]}
      xLabel="VDS (V)"
      yLabel="ID (µA)"
      series={series}
      markers={markers}
      xFmt={(v) => v.toFixed(1)}
      yFmt={(v) => (v >= 100 ? v.toFixed(0) : v.toPrecision(2))}
    >
      {(sx, sy) => {
        const lx = Math.min(vdsMax, vmax * 1.05) * 0.55;
        return <Label x={sx(lx) - 6} y={sy(idSat(kp, wl, lx, lambda, lx) * 1e6) - 8} text="VDS = Vov" anchor="end" size={11} color="var(--bad)" bg />;
      }}
    </Plot>
  );
}

// ─── U3 / U5: bias circuits ────────────────────────────────────────────────

export function NmosRd({
  vdd,
  vg,
  rd,
  vd,
  showVin,
  labelOnly,
  region,
  current,
  highlight,
}: {
  vdd: number;
  vg?: number;
  rd?: number;
  vd?: number;
  showVin?: boolean;
  labelOnly?: boolean;
  region?: Region;
  current?: string;
  highlight?: string[];
}) {
  const gateLabel = labelOnly || vg === undefined ? 'VG' : `VG = ${V(vg)}`;
  return (
    <Canvas w={320} h={190} title="NMOS common-source stage with drain resistor RD" highlight={highlight}>
      <Rail x1={130} x2={210} y={24} label={`VDD = ${V(vdd)}`} />
      <Resistor x={170} y1={24} y2={84} label={<Sym base="R" sub="D" />} value={labelOnly || rd === undefined ? undefined : R(rd)} id="rd" labelSide="left" />
      <Dot x={170} y={84} id="vd" />
      <Nmos x={170} y={114} name="M1" id="m1" region={region} current={current} />
      <Wire points={[[140, 114], [100, 114]]} id="gate" />
      <Terminal x={100} y={114} />
      <Label x={92} y={118} text={showVin ? `${gateLabel} + vin` : gateLabel} anchor="end" />
      <Wire points={[[170, 144], [170, 152]]} />
      <Ground x={170} y={152} />
      <Wire points={[[170, 84], [250, 84]]} id="vd" />
      <Terminal x={250} y={84} />
      <Label x={258} y={88} text={showVin ? 'vout' : 'VD'} />
      {vd !== undefined && <VoltageTag x={206} y={76} v={V(vd)} anchor="middle" id="vd" />}
    </Canvas>
  );
}

export function PmosRd({ vdd, vg, rd, vd, labelOnly, region, current, highlight }: { vdd: number; vg?: number; rd?: number; vd?: number; labelOnly?: boolean; region?: Region; current?: string; highlight?: string[] }) {
  const gateLabel = labelOnly || vg === undefined ? 'VG' : `VG = ${V(vg)}`;
  return (
    <Canvas w={320} h={190} title="PMOS with its source at VDD and RD from drain to ground" highlight={highlight}>
      <Rail x1={130} x2={210} y={24} label={`VDD = ${V(vdd)}`} />
      <Pmos x={170} y={54} name="M1" id="m1" region={region} current={current} />
      <Wire points={[[140, 54], [100, 54]]} />
      <Terminal x={100} y={54} />
      <Label x={92} y={58} text={gateLabel} anchor="end" />
      <Dot x={170} y={84} id="vd" />
      <Wire points={[[170, 84], [250, 84]]} id="vd" />
      <Terminal x={250} y={84} />
      <Label x={258} y={88} text="VD" />
      {vd !== undefined && <VoltageTag x={210} y={100} v={V(vd)} anchor="middle" id="vd" />}
      <Resistor x={170} y1={84} y2={152} label={<Sym base="R" sub="D" />} value={labelOnly || rd === undefined ? undefined : R(rd)} id="rd" labelSide="left" />
      <Ground x={170} y={152} />
    </Canvas>
  );
}

/** Dependent current source (diamond) between (x,y1) top and (x,y2) bottom, arrow down. */
function DependentSource({ x, y1, y2, label, id }: { x: number; y1: number; y2: number; label: string; id?: string }) {
  const mid = (y1 + y2) / 2;
  const r = 14;
  return (
    <g>
      <line x1={x} y1={y1} x2={x} y2={mid - r} {...stroke(false)} />
      <polygon points={`${x},${mid - r} ${x + r},${mid} ${x},${mid + r} ${x - r},${mid}`} fill="var(--paper)" stroke="var(--signal)" strokeWidth={2} data-id={id} />
      <line x1={x} y1={mid - 7} x2={x} y2={mid + 5} stroke="var(--signal)" strokeWidth={1.5} />
      <polyline points={`${x - 4},${mid + 1} ${x},${mid + 7} ${x + 4},${mid + 1}`} fill="none" stroke="var(--signal)" strokeWidth={1.5} />
      <line x1={x} y1={mid + r} x2={x} y2={y2} {...stroke(false)} />
      <Label x={x - r - 6} y={mid + 4} text={label} anchor="end" mono size={12} color="var(--signal)" />
    </g>
  );
}

/** The saturated MOSFET's small-signal model: open gate, gm·vgs ‖ rO. */
export function SmallSignalModel({ highlight }: { highlight?: string[] }) {
  return (
    <Canvas w={320} h={170} title="Small-signal model: the gate draws no current; drain current gm·vgs in parallel with rO" highlight={highlight}>
      <Terminal x={40} y={50} />
      <Label x={40} y={38} text="G" anchor="middle" weight={600} />
      <Label x={52} y={68} text="+" size={14} />
      <Label x={52} y={92} text="vgs" mono size={12} />
      <Label x={52} y={116} text="−" size={14} />
      <Wire points={[[40, 130], [260, 130]]} />
      <Terminal x={40} y={130} />
      <Label x={40} y={150} text="S" anchor="middle" weight={600} />
      <Label x={70} y={54} text="no current into the gate" size={11} color="var(--ink-2)" />
      <Wire points={[[180, 30], [260, 30]]} />
      <Terminal x={290} y={30} />
      <Wire points={[[260, 30], [290, 30]]} />
      <Label x={290} y={18} text="D" anchor="middle" weight={600} />
      <DependentSource x={180} y1={30} y2={130} label="gm·vgs" id="gm" />
      <Resistor x={260} y1={30} y2={130} label={<Sym base="r" sub="O" />} id="ro" />
      <Dot x={180} y={130} />
      <Dot x={260} y={130} />
      <Dot x={260} y={30} />
    </Canvas>
  );
}

/** Small-signal equivalent of the CS stage: gm·vin into RD ‖ rO. */
export function CsSmallSignal({ highlight }: { highlight?: string[] }) {
  return (
    <Canvas w={340} h={170} title="Small-signal CS stage: gm·vin flows into RD in parallel with rO" highlight={highlight}>
      <Terminal x={30} y={60} />
      <Label x={30} y={48} text="vin" anchor="middle" mono />
      <Wire points={[[30, 60], [60, 60]]} />
      <Label x={64} y={64} text="(gate: open)" size={11} color="var(--ink-2)" />
      <Wire points={[[160, 30], [300, 30]]} id="vout" />
      <Terminal x={300} y={30} />
      <Label x={300} y={18} text="vout" anchor="middle" mono />
      <DependentSource x={160} y1={30} y2={130} label="gm·vin" id="gm" />
      <Resistor x={220} y1={30} y2={130} label={<Sym base="r" sub="O" />} id="ro" />
      <Resistor x={280} y1={30} y2={130} label={<Sym base="R" sub="D" />} id="rd" />
      <Wire points={[[160, 130], [280, 130]]} />
      <Ground x={220} y={130} />
      <Dot x={220} y={30} />
      <Dot x={220} y={130} />
      <Label x={230} y={160} text="VDD and ground are both AC ground" anchor="middle" size={11} color="var(--ink-2)" />
    </Canvas>
  );
}

/** CS transfer curve Vout(Vin) with off / saturation / triode regions, a Q point and its tangent. */
export function TransferCurve({ vdd, vth, kp, wl, rd, vinQ }: { vdd: number; vth: number; kp: number; wl: number; rd: number; vinQ: number }) {
  const vout = (vin: number) => solveNmosRd({ vdd, vg: vin, vth, kp, wl, rd }).vd;
  const vinMax = Math.min(vdd, vth + 1.2);
  const N = 120;
  const pts: Array<[number, number]> = [];
  for (let n = 0; n <= N; n++) {
    const vin = (n / N) * vinMax;
    pts.push([vin, vout(vin)]);
  }
  // Edge of triode: first vin where Vout = Vin − Vth.
  let vinEdge = vinMax;
  for (let n = 0; n <= 2000; n++) {
    const vin = vth + (n / 2000) * (vinMax - vth);
    if (vout(vin) <= vin - vth + 1e-6) {
      vinEdge = vin;
      break;
    }
  }
  const vq = vout(vinQ);
  const h = 1e-4;
  const slope = (vout(vinQ + h) - vout(vinQ - h)) / (2 * h);
  const tangent: Array<[number, number]> = [
    [vinQ - 0.12, vq - 0.12 * slope],
    [vinQ + 0.12, vq + 0.12 * slope],
  ];
  const inSat = vinQ > vth && vinQ < vinEdge;
  return (
    <Plot
      title="Common-source transfer curve"
      xRange={[0, vinMax]}
      yRange={[0, vdd * 1.05]}
      xLabel="Vin (V)"
      yLabel="Vout (V)"
      xFmt={(v) => v.toFixed(1)}
      yFmt={(v) => v.toFixed(1)}
      shades={[
        { x0: 0, x1: vth, color: 'var(--muted)', label: 'OFF', labelAt: 'bottom' },
        { x0: vth, x1: vinEdge, color: 'var(--ok)', label: 'SAT', labelAt: 'bottom' },
        { x0: vinEdge, x1: vinMax, color: 'var(--bad)', label: 'TRI', labelAt: 'top' },
      ]}
      series={[
        { points: pts, color: 'var(--ink)', width: 2.2 },
        { points: tangent, color: 'var(--signal)', width: 2, dashed: true },
      ]}
      markers={[{ x: vinQ, y: vq, label: inSat ? `slope = ${slope.toFixed(1)}` : 'Q', labelPos: 'right' }]}
    />
  );
}

// ─── Registry for FigureSpec (problems and lesson steps) ───────────────────

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const FIGURES: Record<string, (props: any) => React.ReactElement> = {
  water: WaterAnalogy,
  resStack: ResStack,
  parallelPair: ParallelPair,
  mosBias: MosBias,
  channel: ChannelCrossSection,
  idvds: IdVdsFamily,
  nmosRd: NmosRd,
  pmosRd: PmosRd,
  smallSignalModel: SmallSignalModel,
  csSmallSignal: CsSmallSignal,
  transfer: TransferCurve,
};

export function Figure({ kind, props, highlight }: { kind: string; props?: Record<string, unknown>; highlight?: string[] }) {
  const C = FIGURES[kind];
  if (!C) return <p className="callout bad">Missing figure: {kind}</p>;
  return <C {...(props ?? {})} highlight={highlight} />;
}
