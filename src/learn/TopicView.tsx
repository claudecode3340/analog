/**
 * End of a topic: every tutorial, PYQ (quizzes and mid-sem), problem-set, Razavi and lab question you can solve
 * once this topic is done, attempted right here. Each question says whether the topics it needs are covered,
 * and gets a ✓ once every part has been answered right. “Coming up” lists the questions that also need a
 * later topic, with a link to where they live.
 */
import { useState } from 'react';
import { homeUnit, sheetProblems, UNIT_BY_ID } from '../content';
import { problemReady, problemSolved } from '../app/progress';
import { recordSheetPart, useProgress } from '../app/store';
import { bankGroup } from '../practice/bankGroups';
import { ProblemView } from '../practice/ProblemView';
import type { Problem } from '../practice/schema';

/** Tutorials first, then PYQs, then everything else, in the order you would meet them. */
const RANK = (p: Problem): number => {
  const g = bankGroup(p);
  if (g.startsWith('Tutorial')) return 0;
  if (g.includes('PYQ')) return 1;
  if (g.startsWith('Problem Set')) return 2;
  if (g.startsWith('Razavi') || g.startsWith('Your lecture')) return 3;
  if (g.startsWith('Lab')) return 4;
  return 5;
};
export function orderSheet(ps: Problem[]): Problem[] {
  return [...ps].sort((a, b) => RANK(a) - RANK(b) || a.title.localeCompare(b.title, undefined, { numeric: true }));
}

const KIND = ['Tutorials', 'PYQs (quizzes and mid-sem)', 'Problem sets', 'Razavi and lecture examples', 'Lab sheets', 'From our chat'];

function SheetItem({ p, open, onToggle }: { p: Problem; open: boolean; onToggle: () => void }) {
  const prog = useProgress();
  const { ready, missing } = problemReady(p.tags, prog);
  const solved = problemSolved(p.id, p.unknowns.map((u) => u.key), prog);
  const parts = prog.sheets?.[p.id] ?? {};
  const right = p.unknowns.filter((u) => parts[u.key]).length;
  return (
    <li className={`sheet-item ${solved ? 'solved' : ''}`}>
      <button type="button" className="sheet-toggle" aria-expanded={open} onClick={onToggle}>
        <span className="sheet-state" aria-hidden="true">{solved ? '✓' : open ? '▾' : '▸'}</span>
        <span className="sheet-main">
          <span className="sheet-title">{p.title}</span>
          <span className="small muted">{p.source}</span>
        </span>
        <span className={`sheet-pill ${solved ? 'ok' : ready ? 'ready' : 'wait'}`}>
          {solved ? 'solved' : right > 0 ? `${right}/${p.unknowns.length} parts` : ready ? 'ready' : `needs ${missing.join(', ')}`}
        </span>
      </button>
      {open && (
        <div className="sheet-body">
          {!ready && (
            <p className="callout small">
              This question also uses{' '}
              {missing.map((m, i) => (
                <span key={m}>
                  {i > 0 && ', '}
                  <a href={`#/learn/${UNIT_BY_ID[m].lessons[0]}`}>
                    {m} {UNIT_BY_ID[m].title}
                  </a>
                </span>
              ))}
              . You can still try it; the hints and the full solution are below.
            </p>
          )}
          <ProblemView problem={p} mode="independent" onResult={(k, r) => recordSheetPart(p.id, k, r.status === 'correct')} />
        </div>
      )}
    </li>
  );
}

export function TopicView({ unit }: { unit: string }) {
  const u = UNIT_BY_ID[unit];
  const prog = useProgress();
  const [open, setOpen] = useState<string | null>(null);
  if (!u) return <p className="page">Topic not found.</p>;
  const { now, later } = sheetProblems(unit);
  const ordered = orderSheet(now);
  const solved = ordered.filter((p) => problemSolved(p.id, p.unknowns.map((x) => x.key), prog)).length;
  const groups = KIND.map((label, r) => [label, ordered.filter((p) => RANK(p) === r)] as const).filter(([, xs]) => xs.length > 0);
  return (
    <div className="page topic-page">
      <p className="small">
        <a href="#/learn">Learn</a> › <a href={`#/learn/${u.lessons[0]}`}>{u.id} {u.title}</a>
      </p>
      <h1>Tutorials & PYQs: {u.title}</h1>
      <p className="lede">
        Everything from your sheets that you can solve once <strong>{u.id}</strong> is done. Open a question, attempt it here, and use the hints only when stuck.
      </p>
      <div className="topic-meter" role="status">
        <div className="topic-bar" style={{ ['--p' as string]: ordered.length ? `${(solved / ordered.length) * 100}%` : '0%' }} />
        <span className="small">
          {solved}/{ordered.length} solved
        </span>
      </div>
      {ordered.length === 0 && <p className="callout">No sheet question needs only this topic. The ones that use it are listed under “Coming up”.</p>}
      {groups.map(([label, ps]) => (
        <section key={label} className="sheet-group">
          <h2>{label}</h2>
          <ul className="sheet-list">
            {ps.map((p) => (
              <SheetItem key={p.id} p={p} open={open === p.id} onToggle={() => setOpen(open === p.id ? null : p.id)} />
            ))}
          </ul>
        </section>
      ))}
      {later.length > 0 && (
        <section className="sheet-group">
          <h2>Coming up</h2>
          <p className="small muted">These also use {u.id}, but need a later topic too. They sit at the end of that topic.</p>
          <ul className="sheet-later">
            {orderSheet(later).map((p) => {
              const h = homeUnit(p)!;
              return (
                <li key={p.id}>
                  <a href={`#/topic/${h}`}>{p.title}</a> <span className="small muted">· after {h} {UNIT_BY_ID[h].title}</span>
                </li>
              );
            })}
          </ul>
        </section>
      )}
    </div>
  );
}
