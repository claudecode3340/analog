import { useMemo, useRef, useState, useEffect } from 'react';
import { Figure } from '../circuits/figures';
import { BANK_BY_ID, GENERATOR_BY_ID, LESSON_BY_ID, UNIT_BY_ID } from '../content';
import type { Lesson } from '../content/types';
import { MASTERY, recordCheck, recordLessonStep, useProgress } from '../app/store';
import { generate } from '../practice/generate';
import { ProblemView, StepTrace } from '../practice/ProblemView';
import type { CheckResult } from '../practice/checker';
import type { Problem } from '../practice/schema';
import { newSeed } from '../practice/rng';
import { Prose, RichText, Term } from '../ui/RichText';
import { Tex } from '../ui/Tex';
import { WIDGETS } from './widgets';
import { nextLessonAfter } from '../app/progress';

const SECTIONS = ['Why you need this', 'The picture', 'Predict', 'The idea', 'The rule', 'Worked example', 'Your turn', 'Lock it in'];

function Visual({ v }: { v: Lesson['picture']['visual'] }) {
  if ('widget' in v) {
    const W = WIDGETS[v.widget];
    return W ? <W {...(v.props ?? {})} /> : <p className="callout bad">Missing widget {v.widget}</p>;
  }
  return <Figure kind={v.kind} props={v.props} />;
}

function Predict({ lesson, onAnswered, answered }: { lesson: Lesson; onAnswered: (choice: number) => void; answered: number | null }) {
  const q = lesson.predict;
  return (
    <div className="predict">
      <p className="predict-prompt">
        <RichText text={q.prompt} />
      </p>
      <div className="choices" role="group" aria-label="Your prediction">
        {q.choices.map((c, i) => {
          const state = answered === null ? '' : i === q.answer ? 'right' : i === answered ? 'picked-wrong' : '';
          return (
            <button key={i} type="button" className={`btn choice ${state}`} disabled={answered !== null} onClick={() => onAnswered(i)} data-choice={i}>
              {c}
            </button>
          );
        })}
      </div>
      {answered !== null && (
        <p className={`callout ${answered === q.answer ? 'ok' : 'bad'}`} role="status">
          <strong>{answered === q.answer ? 'Right.' : 'Not quite.'}</strong> <RichText text={q.explain} />
        </p>
      )}
    </div>
  );
}

function workedProblem(l: Lesson): Problem | null {
  if ('generator' in l.worked) return generate(GENERATOR_BY_ID[l.worked.generator], l.worked.seed);
  if ('bank' in l.worked) return BANK_BY_ID[l.worked.bank];
  return null;
}

export function LessonView({ id }: { id: string }) {
  const lesson = LESSON_BY_ID[id];
  const progress = useProgress();
  const [step, setStep] = useState(0);
  const [predicted, setPredicted] = useState<number | null>(null);
  const [predictRight, setPredictRight] = useState<boolean | null>(null);
  const [seedBase, setSeedBase] = useState(() => newSeed());
  const [results, setResults] = useState<Record<string, boolean>>({});
  const [checkSaved, setCheckSaved] = useState(false);
  const bottom = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setStep(0);
    setPredicted(null);
    setPredictRight(null);
    setResults({});
    setCheckSaved(false);
    setSeedBase(newSeed());
    window.scrollTo({ top: 0 });
  }, [id]);

  const worked = useMemo(() => (lesson ? workedProblem(lesson) : null), [lesson]);
  const turnProblems = useMemo(() => {
    if (!lesson) return [];
    const out: Problem[] = [];
    for (let i = 0; i < lesson.yourTurn.count; i++) {
      const gid = lesson.yourTurn.generators[i % lesson.yourTurn.generators.length];
      out.push(generate(GENERATOR_BY_ID[gid], seedBase + i * 101));
    }
    return out;
  }, [lesson, seedBase]);

  const totalItems = 1 + turnProblems.reduce((n, p) => n + p.unknowns.length, 0);
  const firstTryRight = (predictRight ? 1 : 0) + Object.values(results).filter(Boolean).length;
  const answeredAll = turnProblems.every((p) => p.unknowns.every((u) => `${p.id}:${u.key}` in results));
  const score = firstTryRight / totalItems;
  const numericRight = turnProblems.some((p) => p.unknowns.some((u) => !u.choices && results[`${p.id}:${u.key}`]));

  useEffect(() => {
    if (lesson && answeredAll && !checkSaved && step >= 6) {
      setCheckSaved(true);
      recordCheck(lesson.id, score, numericRight, lesson.lockIn.cards.map((c) => c.id));
    }
  }, [lesson, answeredAll, checkSaved, step, score, numericRight]);

  if (!lesson) return <p className="page">Lesson not found.</p>;
  const unit = UNIT_BY_ID[lesson.unit];
  const lp = progress.lessons[lesson.id];

  const advance = () => {
    const s = Math.min(step + 1, SECTIONS.length - 1);
    setStep(s);
    recordLessonStep(lesson.id, s);
    setTimeout(() => bottom.current?.scrollIntoView({ behavior: 'smooth', block: 'end' }), 30);
  };

  const onTurnResult = (p: Problem) => (k: string, r: CheckResult, first: boolean) => {
    const key = `${p.id}:${k}`;
    if (!first) return;
    setResults((prev) => ({ ...prev, [key]: r.status === 'correct' }));
  };
  const canContinue = step !== 2 || predicted !== null;
  const next = nextLessonAfter(lesson.id);

  return (
    <div className="page narrow lesson">
      <nav className="crumbs small">
        <a href="#/path">Path</a> › {unit.id} {unit.title}
      </nav>
      <header className="lesson-head">
        <div className="eyebrow">
          {unit.id} · {lesson.minutes} min
          {lp?.status === 'mastered' && <span className="badge ok">mastered</span>}
        </div>
        <h1>{lesson.title}</h1>
        <p className="small muted refs">
          {lesson.refs.razavi && <>Razavi 2nd ed {lesson.refs.razavi} · </>}
          {lesson.refs.notes && <>Your notes: {lesson.refs.notes} · </>}
          {lesson.refs.conversation && <>Conversation: {lesson.refs.conversation}</>}
        </p>
      </header>

      <div className="sheet">
        {SECTIONS.slice(0, step + 1).map((title, i) => (
          <section key={title} className="lesson-step" aria-labelledby={`sec-${i}`}>
            <span className="margin-tag">{i + 1}</span>
            <h2 id={`sec-${i}`} className="step-title">
              {title}
            </h2>
            {i === 0 && (
              <p className="why">
                <RichText text={lesson.why} />
              </p>
            )}
            {i === 1 && (
              <>
                <Visual v={lesson.picture.visual} />
                <p className="caption">
                  <RichText text={lesson.picture.caption} />
                </p>
              </>
            )}
            {i === 2 && (
              <Predict
                lesson={lesson}
                answered={predicted}
                onAnswered={(choice) => {
                  setPredicted(choice);
                  setPredictRight(choice === lesson.predict.answer);
                }}
              />
            )}
            {i === 3 && (
              <>
                <Prose text={lesson.idea} />
                {lesson.analogy && (
                  <p className="analogy">
                    <span className="eyebrow">Picture it</span> <RichText text={lesson.analogy} />
                  </p>
                )}
              </>
            )}
            {i === 4 && (
              <>
                <div className="rule-box">
                  {lesson.rule.tex.map((t, j) => (
                    <div key={j} className="rule-line">
                      <Tex tex={t} />
                    </div>
                  ))}
                </div>
                <p className="small symbols">
                  Symbols:{' '}
                  {lesson.rule.symbols.map((s, j) => (
                    <span key={s}>
                      {j > 0 && ', '}
                      <Term k={s} />
                    </span>
                  ))}{' '}
                  <span className="muted">(tap any symbol for its meaning)</span>
                </p>
                {lesson.rule.note && (
                  <p className="callout small">
                    <RichText text={lesson.rule.note} />
                  </p>
                )}
              </>
            )}
            {i === 5 && (
              <>
                {worked ? (
                  <ProblemView problem={worked} mode="worked" />
                ) : 'custom' in lesson.worked ? (
                  <article className="problem">
                    <h3>{lesson.worked.custom.title}</h3>
                    <div className="problem-body">
                      <div className="problem-figure">
                        <Figure kind={lesson.worked.custom.figure.kind} props={lesson.worked.custom.figure.props} />
                      </div>
                      <div className="problem-text">
                        <p>{lesson.worked.custom.setup}</p>
                      </div>
                    </div>
                    <StepTrace steps={lesson.worked.custom.steps} />
                  </article>
                ) : null}
              </>
            )}
            {i === 6 && (
              <>
                <p className="small muted">
                  The first one shows the method (you fill in the numbers). After that you’re on your own. Use prefixes: <code>90u</code>, <code>9k</code>, <code>0.6m</code>.
                </p>
                {turnProblems.map((p, j) => (
                  <ProblemView key={p.id} problem={p} mode={j === 0 ? 'faded' : 'independent'} onResult={onTurnResult(p)} compact />
                ))}
              </>
            )}
            {i === 7 && (
              <div className="lockin">
                <p className="summary">
                  <RichText text={lesson.lockIn.summary} />
                </p>
                <p className="hook">
                  <span className="eyebrow">Memory hook</span> {lesson.lockIn.hook}
                </p>
                {answeredAll ? (
                  <p className={`callout ${score >= MASTERY && numericRight ? 'ok' : 'bad'}`} role="status">
                    Check score: <strong>{Math.round(score * 100)}%</strong> first-try ({firstTryRight}/{totalItems}).{' '}
                    {score >= MASTERY && numericRight
                      ? 'Mastered: the next lessons are unlocked, and these cards are in your Review deck.'
                      : 'Mastery needs 80%, including a numeric answer. Try a fresh set; the cards are already in Review.'}
                  </p>
                ) : (
                  <p className="callout small">Finish the “Your turn” problems above to score this lesson.</p>
                )}
                <div className="cards-preview">
                  {lesson.lockIn.cards.map((c) => (
                    <div key={c.id} className="card-mini">
                      <div className="card-front">
                        <RichText text={c.front} />
                      </div>
                      <div className="card-back small">
                        <RichText text={c.back} />
                      </div>
                    </div>
                  ))}
                </div>
                <div className="row">
                  {!(score >= MASTERY && numericRight) && answeredAll && (
                    <button
                      className="btn"
                      type="button"
                      onClick={() => {
                        setSeedBase(newSeed());
                        setResults({});
                        setCheckSaved(false);
                        setStep(6);
                      }}
                    >
                      Try a fresh set
                    </button>
                  )}
                  {lesson.lab && (
                    <a className="btn" href={`#/labs/${lesson.lab.id}`}>
                      Open the lab
                    </a>
                  )}
                  {next && (
                    <a className="btn primary" href={`#/learn/${next}`}>
                      Next lesson →
                    </a>
                  )}
                </div>
              </div>
            )}
          </section>
        ))}
        {step < SECTIONS.length - 1 && (
          <div className="continue">
            <button type="button" className="btn primary" onClick={advance} disabled={!canContinue}>
              {step === 2 && predicted === null ? 'Make a prediction first' : `Continue: ${SECTIONS[step + 1]}`}
            </button>
          </div>
        )}
        <div ref={bottom} />
      </div>
    </div>
  );
}
