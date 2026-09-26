import { LESSON_BY_ID, UNITS } from '../content';
import { lessonUnlocked, nextStep } from '../app/progress';
import { useProgress } from '../app/store';

export function LearnIndex() {
  const p = useProgress();
  const ns = nextStep(p);
  return (
    <div className="page narrow">
      <h1>Learn</h1>
      {ns.lesson && (
        <p>
          <a className="btn primary big" href={`#/learn/${ns.lesson}`}>
            Continue: {LESSON_BY_ID[ns.lesson].title} →
          </a>
        </p>
      )}
      {UNITS.filter((u) => u.lessons.length > 0).map((u) => (
        <section key={u.id} className="learn-unit">
          <h2>
            <span className="mono muted">{u.id}</span> {u.title}
          </h2>
          <div className="lesson-chips">
            {u.lessons.map((id) => {
              const l = LESSON_BY_ID[id];
              const st = p.lessons[id];
              const cls = st?.status === 'mastered' ? 'mastered' : st ? 'started' : '';
              return lessonUnlocked(id, p) ? (
                <a key={id} href={`#/learn/${id}`} className={`lesson-chip ${cls}`}>
                  <span className="chip-dot" />
                  {l.title}
                  <span className="small muted mono">{st?.status === 'mastered' ? '✓' : `${l.minutes} min`}</span>
                </a>
              ) : (
                <span key={id} className="lesson-chip locked">
                  🔒 {l.title}
                </span>
              );
            })}
          </div>
        </section>
      ))}
      <p className="small muted">Units U6–U12 and the handout lectures arrive in the next milestones.</p>
    </div>
  );
}
