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
import { DrawStyleContext } from '../circuits/primitives';

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
              <figure key={g.id} className="gallery-item" data-fig={`${style}-${g.id}`}>
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
