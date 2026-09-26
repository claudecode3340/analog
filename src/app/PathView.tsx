import { EXAMS } from '../content/curriculum';
import { LESSON_BY_ID, UNITS } from '../content';
import { daysUntil, lessonUnlocked, nextStep, unitState } from './progress';
import { useProgress } from './store';

function Countdown() {
  const upcoming = EXAMS.map((e) => ({ ...e, days: daysUntil(e.date) })).filter((e) => e.days >= 0);
  const next = upcoming[0];
  if (!next) return null;
  return (
    <div className="countdown" aria-label="Exam countdown">
      <div className="countdown-big">
        <span className="countdown-num mono">{next.days}</span>
        <span className="countdown-unit">{next.days === 1 ? 'day' : 'days'}</span>
      </div>
      <div>
        <div className="countdown-name">
          to the <strong>{next.name}</strong>
        </div>
        <div className="small muted">
          {new Date(next.date + 'T00:00:00').toLocaleDateString(undefined, { weekday: 'short', day: 'numeric', month: 'short' })} · {next.note}
        </div>
        <div className="small muted">{upcoming.slice(1).map((e) => `${e.name} in ${e.days} d`).join(' · ')}</div>
      </div>
    </div>
  );
}

export function PathView() {
  const p = useProgress();
  const ns = nextStep(p);
  const nextLesson = ns.lesson ? LESSON_BY_ID[ns.lesson] : undefined;
  const mastered = Object.values(p.lessons).filter((l) => l.status === 'mastered').length;
  const total = UNITS.reduce((n, u) => n + u.lessons.length, 0);
  return (
    <div className="page">
      <div className="path-top">
        <Countdown />
        <div className="next-step">
          <div className="eyebrow">Your next step</div>
          {nextLesson ? (
            <>
              <h2>
                {nextLesson.unit} · {nextLesson.title}
              </h2>
              <p className="muted small">{nextLesson.why}</p>
              <a className="btn primary" href={`#/learn/${nextLesson.id}`}>
                {p.lessons[nextLesson.id] ? 'Continue' : 'Start'} →
              </a>
            </>
          ) : ns.done ? (
            <p>Every available lesson is mastered. Mix it up in Practice, or clear today’s Review cards.</p>
          ) : (
            <p>Master the unit before {ns.unit} to unlock it (or turn on the override in Settings).</p>
          )}
          <p className="small muted">
            {mastered}/{total} lessons mastered · {p.practice.correct}/{p.practice.attempted} practice answers right
          </p>
        </div>
      </div>

      <h2 className="path-heading">Foundations: where you are now</h2>
      <ol className="path">
        {UNITS.filter((u) => u.group === 'foundations').map((u) => (
          <UnitRow key={u.id} id={u.id} />
        ))}
      </ol>
      <h2 className="path-heading">Handout lectures</h2>
      <p className="small muted">
        Numbered as in the course handout. Your own notes are numbered by class date; the matching notes are shown on each lecture.
      </p>
      <ol className="path">
        {UNITS.filter((u) => u.group === 'handout').map((u) => (
          <UnitRow key={u.id} id={u.id} />
        ))}
      </ol>
    </div>
  );
}

function UnitRow({ id }: { id: string }) {
  const p = useProgress();
  const u = UNITS.find((x) => x.id === id)!;
  const st = unitState(u, p);
  const label = { locked: 'locked', learning: 'learning', mastered: 'mastered', coming: `coming in M${u.milestone}` }[st];
  const tone = { locked: 'muted', learning: 'signal', mastered: 'ok', coming: 'muted' }[st];
  return (
    <li className={`unit unit-${st}`}>
      <div className="unit-node" aria-hidden="true">
        {st === 'mastered' ? '✓' : st === 'locked' || st === 'coming' ? '·' : '○'}
      </div>
      <div className="unit-body">
        <div className="unit-head">
          <span className="unit-id mono">{u.id}</span>
          <span className="unit-title">{u.title}</span>
          <span className={`badge ${tone}`}>{label}</span>
        </div>
        <div className="small muted">
          {u.short}
          {u.ref && <> · {u.ref}</>}
          {u.notes && <> · {u.notes}</>}
        </div>
        {u.lessons.length > 0 && (
          <ul className="lesson-list">
            {u.lessons.map((lid) => {
              const l = LESSON_BY_ID[lid];
              const lp = p.lessons[lid];
              const open = lessonUnlocked(lid, p);
              return (
                <li key={lid}>
                  {open ? (
                    <a href={`#/learn/${lid}`}>
                      {lp?.status === 'mastered' ? '✓ ' : lp ? '◐ ' : '○ '}
                      {l.title}
                    </a>
                  ) : (
                    <span className="muted">🔒 {l.title}</span>
                  )}
                  {lp && <span className="small muted"> · best {Math.round(lp.best * 100)}%</span>}
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </li>
  );
}
