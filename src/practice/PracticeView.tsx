import { useMemo, useState } from 'react';
import { BANK, GENERATORS, UNIT_BY_ID } from '../content';
import { unitState } from '../app/progress';
import { useProgress } from '../app/store';
import { generate } from './generate';
import { ProblemView } from './ProblemView';
import { newSeed } from './rng';
import type { Problem } from './schema';

type Source = { kind: 'gen'; id: string } | { kind: 'mix' } | { kind: 'bank'; id: string };

export function PracticeView() {
  const p = useProgress();
  const available = GENERATORS.filter((g) => unitState(UNIT_BY_ID[g.unit], p) !== 'locked');
  const masteredUnits = new Set(Object.keys(UNIT_BY_ID).filter((u) => unitState(UNIT_BY_ID[u], p) === 'mastered'));
  const mixPool = available.filter((g) => masteredUnits.has(g.unit));
  const [source, setSource] = useState<Source>(() => (available[0] ? { kind: 'gen', id: available[0].id } : { kind: 'bank', id: BANK[0].id }));
  const [seed, setSeed] = useState(() => newSeed());

  const problem: Problem = useMemo(() => {
    if (source.kind === 'bank') return BANK.find((b) => b.id === source.id)!;
    if (source.kind === 'mix') {
      const pool = mixPool.length ? mixPool : available;
      return generate(pool[seed % pool.length], seed);
    }
    return generate(GENERATORS.find((g) => g.id === source.id)!, seed);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [source, seed]);

  return (
    <div className="page">
      <h1>Practice</h1>
      <p className="muted">
        Endless generated problems (every one is solved twice and physically checked before you see it), plus the fixed bank. Type answers with prefixes: <code>90u</code>, <code>9k</code>, <code>0.6m</code>, <code>358 kHz</code>. Tolerance ±{Math.round(p.settings.tol * 100)}%.
      </p>
      <div className="practice-grid">
        <aside className="practice-menu" aria-label="Choose problems">
          <div className="eyebrow">Interleaved</div>
          <button type="button" className={`menu-item ${source.kind === 'mix' ? 'active' : ''}`} onClick={() => { setSource({ kind: 'mix' }); setSeed(newSeed()); }}>
            🔀 Mixed set {mixPool.length ? `(${mixPool.length} types from mastered units)` : '(unlocks as you master units)'}
          </button>
          <div className="eyebrow">By topic</div>
          {GENERATORS.map((g) => {
            const open = available.includes(g);
            return (
              <button key={g.id} type="button" disabled={!open} className={`menu-item ${source.kind === 'gen' && source.id === g.id ? 'active' : ''}`} onClick={() => { setSource({ kind: 'gen', id: g.id }); setSeed(newSeed()); }}>
                <span className="mono small">{g.unit}</span> {open ? '' : '🔒 '}
                {g.title}
              </button>
            );
          })}
          <div className="eyebrow">Fixed bank</div>
          {BANK.map((b) => (
            <button key={b.id} type="button" className={`menu-item ${source.kind === 'bank' && source.id === b.id ? 'active' : ''}`} onClick={() => setSource({ kind: 'bank', id: b.id })}>
              {b.title}
            </button>
          ))}
          <p className="small muted">Tutorials 1–3, the exam question and Problem Set 1 join the bank in Milestones 3–4; their answers are already verified in the engine.</p>
        </aside>
        <div>
          <ProblemView key={problem.id} problem={problem} />
          {source.kind !== 'bank' && (
            <div className="row" style={{ marginTop: 16 }}>
              <button type="button" className="btn primary" onClick={() => setSeed(newSeed())}>
                New problem →
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
