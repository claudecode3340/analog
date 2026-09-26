import { useMemo, useState } from 'react';
import { BANK, GENERATORS, UNIT_BY_ID } from '../content';
import { unitState } from '../app/progress';
import { useProgress } from '../app/store';
import { generate } from './generate';
import { ProblemView } from './ProblemView';
import { newSeed } from './rng';
import type { Problem } from './schema';

/** Group the fixed bank by where each problem comes from. */
function bankGroup(p: Problem): string {
  const s = p.source;
  if (/^Mid-sem|^Quiz/.test(s)) return 'Exam and quizzes';
  if (/^Tutorial (\d)/.test(s)) return `Tutorial ${s.match(/^Tutorial (\d)/)![1]}`;
  if (/^Problem Set/.test(s)) return 'Problem Set 1 (chat)';
  if (/^Razavi/.test(s)) return 'Razavi examples';
  if (/^Lab/.test(s)) return 'Lab sheets (calculations)';
  if (/chat|conversation/i.test(s)) return 'Questions from our chat';
  return 'Worked examples';
}
const GROUP_ORDER = ['Exam and quizzes', 'Tutorial 1', 'Tutorial 2', 'Tutorial 3', 'Tutorial 4', 'Tutorial 5', 'Tutorial 6', 'Problem Set 1 (chat)', 'Razavi examples', 'Lab sheets (calculations)', 'Questions from our chat', 'Worked examples'];
const BANK_GROUPS: Array<[string, Problem[]]> = GROUP_ORDER.map((g) => [g, BANK.filter((b) => bankGroup(b) === g)] as [string, Problem[]]).filter(([, xs]) => xs.length > 0);

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
        Endless fresh problems, each checked twice before you see it. Type answers with prefixes like <code>90u</code>, <code>9k</code>, <code>0.6m</code>. Answers within ±{Math.round(p.settings.tol * 100)}% count as right.
      </p>
      <div className="practice-grid">
        <aside className="practice-menu card" aria-label="Choose problems">
          <div className="eyebrow">Interleaved</div>
          <button type="button" className={`menu-item ${source.kind === 'mix' ? 'active' : ''}`} onClick={() => { setSource({ kind: 'mix' }); setSeed(newSeed()); }}>
            <span className="menu-unit">mix</span>
            <span>Mixed set {mixPool.length ? `(${mixPool.length} types)` : '(unlocks as you master units)'}</span>
          </button>
          <div className="eyebrow">Your tutorials, exams and labs</div>
          {BANK_GROUPS.map(([group, items]) => (
            <details key={group} className="bank-group" open={items.some((b) => source.kind === 'bank' && source.id === b.id)}>
              <summary>
                {group} <span className="badge">{items.length}</span>
              </summary>
              {items.map((b) => (
                <button key={b.id} type="button" className={`menu-item ${source.kind === 'bank' && source.id === b.id ? 'active' : ''}`} onClick={() => setSource({ kind: 'bank', id: b.id })}>
                  <span className="menu-unit">★</span>
                  <span>{b.title}</span>
                </button>
              ))}
            </details>
          ))}
          <div className="eyebrow">By topic</div>
          {GENERATORS.map((g) => {
            const open = available.includes(g);
            return (
              <button key={g.id} type="button" disabled={!open} className={`menu-item ${source.kind === 'gen' && source.id === g.id ? 'active' : ''}`} onClick={() => { setSource({ kind: 'gen', id: g.id }); setSeed(newSeed()); }}>
                <span className="menu-unit">{g.unit}</span>
                <span>
                  {open ? '' : '🔒 '}
                  {g.title}
                </span>
              </button>
            );
          })}
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
