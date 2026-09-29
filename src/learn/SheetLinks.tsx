/**
 * The real questions for a topic: tutorials, problem sets, quizzes, Razavi examples and lab sheets that you can
 * solve once this topic is done (“solve now”), plus those that use it but need a later topic (“coming up”).
 * Each opens straight in Practice. Driven by the problem tags, so new questions appear here automatically.
 */
import { sheetProblems, UNIT_BY_ID, homeUnit } from '../content';
import { bankGroup, GROUP_ORDER } from '../practice/bankGroups';
import type { Problem } from '../practice/schema';

function order(ps: Problem[]): Problem[] {
  return [...ps].sort((a, b) => GROUP_ORDER.indexOf(bankGroup(a)) - GROUP_ORDER.indexOf(bankGroup(b)) || a.title.localeCompare(b.title, undefined, { numeric: true }));
}

/** Short chip label: the source without its bracket; chat questions use their own title (they share a source). */
function chipLabel(p: Problem): string {
  if (bankGroup(p) === 'Questions from our chat') {
    const t = p.title.replace(/^Chat:\s*/, '');
    return t.length > 30 ? `${t.slice(0, 28)}…` : t;
  }
  return p.source.replace(/\s*\(.*\)$/, '');
}

function Item({ p, note }: { p: Problem; note?: string }) {
  const group = bankGroup(p);
  const showGroup = !p.title.toLowerCase().startsWith(group.toLowerCase().split(' (')[0]);
  return (
    <li>
      <a href={`#/practice/${p.id}`} className="sheet-link">
        {showGroup && <span className="sheet-src">{group}</span>}
        <span className="sheet-title">{p.title}</span>
      </a>
      {note && <span className="small muted"> {note}</span>}
    </li>
  );
}

export function SheetLinks({ unit, compact = false }: { unit: string; compact?: boolean }) {
  const { now, later } = sheetProblems(unit);
  if (!now.length && !later.length) return null;
  if (compact)
    return (
      <div className="sheet-links compact">
        <span className="small muted">Questions for this topic:</span>{' '}
        {order(now).map((p) => (
          <a key={p.id} href={`#/practice/${p.id}`} className="chip-link" title={p.title}>
            {chipLabel(p)}
          </a>
        ))}
        {!now.length && <span className="small muted">none yet (see later topics)</span>}
      </div>
    );
  return (
    <section className="sheet-links card" aria-label="Tutorial and problem-set questions for this topic">
      <h3>Your tutorial and problem-set questions for this topic</h3>
      {now.length > 0 ? (
        <>
          <p className="small muted">You can solve these now. Each opens in Practice with hints and a full solution.</p>
          <ul>
            {order(now).map((p) => (
              <Item key={p.id} p={p} />
            ))}
          </ul>
        </>
      ) : (
        <p className="small muted">No sheet question needs only this topic yet.</p>
      )}
      {later.length > 0 && (
        <details>
          <summary className="small">Coming up: {later.length} more use this topic once you reach a later one</summary>
          <ul>
            {order(later).map((p) => {
              const h = homeUnit(p);
              return <Item key={p.id} p={p} note={h ? `after ${h} ${UNIT_BY_ID[h]?.title ?? ''}` : undefined} />;
            })}
          </ul>
        </details>
      )}
    </section>
  );
}
