import { IconBolt, IconLab, IconLock } from '../ui/Icons';

const LABS = [
  { id: 'mosfet', title: 'MOSFET lab', desc: 'Channel cross-section with moving electrons, ID–VDS curves, region, gm, rO, gm·rO.', ready: true },
  { id: 'dc', title: 'DC recipe stepper', desc: 'Step A one click at a time, with the saturation check turning green or red.', ready: true },
  { id: 'impedance', title: 'Impedance explorer', desc: 'Click a terminal: ∞, rO, 1/gm, and why the device fights back.', ready: false, m: 2 },
  { id: 'cs', title: 'CS amplifier lab', desc: 'Every load, a transfer curve with a draggable Q, Gm·Rout.', ready: false, m: 2 },
  { id: 'cascode', title: 'Cascode lab', desc: 'Telescopic and folded, the bias ladder, Rout comparison.', ready: false, m: 2 },
  { id: 'headroom', title: 'Headroom stack', desc: 'Stacked overdrives, VISS, diode costs: the swing left over.', ready: false, m: 3 },
  { id: 'diffpair', title: 'Differential pair lab', desc: 'Current steering, ±√2·Vov, DM and CM half circuits.', ready: false, m: 3 },
  { id: 'ota', title: 'Five-transistor OTA lab', desc: 'Signal currents through the mirror, CM range, swing, buffer.', ready: false, m: 3 },
  { id: 'feedback', title: 'Feedback, Bode and settling', desc: 'The 1/β line, the ε band, 4.6τ, slewing then settling.', ready: false, m: 3 },
];

export function LabsIndex() {
  return (
    <div className="page">
      <h1>Labs</h1>
      <p className="muted lab-intro">Play with real circuits. Drag the sliders and watch the currents, voltages and curves respond. Every number comes from the same equations you use in your tutorials.</p>
      <ul className="labs-grid">
        {LABS.map((l) => (
          <li key={l.id}>
            {l.ready ? (
              <a href={`#/labs/${l.id}`} className="lab-card card">
                <span className="lab-icon">{l.id === 'dc' ? <IconBolt size={22} /> : <IconLab size={22} />}</span>
                <strong>{l.title}</strong>
                <span className="small muted">{l.desc}</span>
              </a>
            ) : (
              <div className="lab-card card coming">
                <span className="lab-icon">
                  <IconLock size={20} />
                </span>
                <strong>{l.title}</strong>
                <span className="small muted">
                  {l.desc} Coming in Milestone {l.m}.
                </span>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
