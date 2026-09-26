const LABS = [
  { id: 'mosfet', title: 'MOSFET lab', desc: 'Channel cross-section, ID–VDS family, region, gm, rO, gm·rO.', ready: true },
  { id: 'dc', title: 'DC recipe stepper', desc: 'Step A one click at a time, with the fence check in green or red.', ready: true },
  { id: 'headroom', title: 'Headroom stack', desc: 'Stacked overdrives, VISS, diode costs; the swing left over.', ready: false, m: 3 },
  { id: 'impedance', title: 'Impedance explorer', desc: 'Click a terminal: ∞, rO, 1/gm, and why the device fights back.', ready: false, m: 2 },
  { id: 'cs', title: 'CS amplifier lab', desc: 'Every load, transfer curve with a draggable Q, Gm·Rout.', ready: false, m: 2 },
  { id: 'diffpair', title: 'Differential pair lab', desc: 'Current steering, ±√2·Vov, DM and CM half circuits.', ready: false, m: 3 },
  { id: 'ota', title: 'Five-transistor OTA lab', desc: 'Signal currents through the mirror, CM range, swing, buffer.', ready: false, m: 3 },
  { id: 'feedback', title: 'Feedback, Bode and settling', desc: '1/β line, ε band, 4.6τ, slewing then settling.', ready: false, m: 3 },
  { id: 'cascode', title: 'Cascode lab', desc: 'Telescopic and folded, bias ladder, Rout comparison.', ready: false, m: 2 },
];

export function LabsIndex() {
  return (
    <div className="page">
      <h1>Labs</h1>
      <p className="muted">Free-play simulators. Every lesson links to the lab it uses.</p>
      <ul className="labs-list">
        {LABS.map((l) => (
          <li key={l.id} className={l.ready ? '' : 'coming'}>
            {l.ready ? (
              <a href={`#/labs/${l.id}`}>
                <strong>{l.title}</strong>
              </a>
            ) : (
              <strong className="muted">{l.title}</strong>
            )}
            <div className="small muted">
              {l.desc}
              {!l.ready && ` · coming in Milestone ${l.m}`}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
