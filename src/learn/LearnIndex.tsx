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
          <a className="btn primary" href={`#/learn/${ns.lesson}`}>
            Continue: {LESSON_BY_ID[ns.lesson].title} →
          </a>
        </p>
      )}
      {UNITS.filter((u) => u.lessons.length > 0).map((u) => (
        <section key={u.id} className="learn-unit">
          <h2>
            <span className="mono muted">{u.id}</span> {u.title}
          </h2>
          <ul className="lesson-list">
            {u.lessons.map((id) => {
              const l = LESSON_BY_ID[id];
              const st = p.lessons[id];
              return (
                <li key={id}>
                  {lessonUnlocked(id, p) ? <a href={`#/learn/${id}`}>{l.title}</a> : <span className="muted">🔒 {l.title}</span>}{' '}
                  <span className="small muted">
                    · {l.minutes} min {st?.status === 'mastered' ? '· ✓ mastered' : st ? `· best ${Math.round(st.best * 100)}%` : ''}
                  </span>
                </li>
              );
            })}
          </ul>
        </section>
      ))}
      <p className="small muted">Units U6–U12 and the handout lectures arrive in the next milestones.</p>
    </div>
  );
}
