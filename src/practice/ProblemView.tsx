import { useState } from 'react';
import { Figure } from '../circuits/figures';
import { logMistake, recordPractice, useProgress } from '../app/store';
import { Tex } from '../ui/Tex';
import { checkAnswer, type CheckResult } from './checker';
import type { Problem, TraceStep } from './schema';
import { texSI } from './tex';

export type ProblemMode = 'worked' | 'faded' | 'independent';

const TAG_NAMES: Record<string, string> = {
  A: 'Step A · DC recipe',
  B: 'Step B · roles',
  C: 'Step C · impedances',
  D: 'Step D · gain',
  '✓': 'Check',
  '·': '',
};

export function Givens({ problem }: { problem: Problem }) {
  return (
    <dl className="givens">
      {problem.givens.map((g, i) => (
        <div key={i} className="given">
          <dt>
            <Tex tex={g.sym} />
          </dt>
          <dd className="mono">
            <Tex tex={g.unit === '' ? String(g.value) : texSI(g.value, g.unit, 4)} />
          </dd>
        </div>
      ))}
    </dl>
  );
}

export function StepTrace({ steps, onFocusStep, hideValues }: { steps: TraceStep[]; onFocusStep?: (s: TraceStep | null) => void; hideValues?: boolean }) {
  return (
    <ol className="trace">
      {steps.map((s, i) => (
        <li
          key={i}
          className={`trace-step tag-${s.tag === '✓' ? 'check' : s.tag === '·' ? 'plain' : s.tag}`}
          tabIndex={0}
          onMouseEnter={() => onFocusStep?.(s)}
          onMouseLeave={() => onFocusStep?.(null)}
          onFocus={() => onFocusStep?.(s)}
          onBlur={() => onFocusStep?.(null)}
        >
          {TAG_NAMES[s.tag] && <span className="trace-tag">{TAG_NAMES[s.tag]}</span>}
          <div className="trace-title">{s.title}</div>
          {s.tex && !hideValues && (
            <div className="trace-tex">
              <Tex tex={s.tex} />
            </div>
          )}
          {s.note && <div className="small muted">{s.note}</div>}
        </li>
      ))}
    </ol>
  );
}

function AnswerRow({
  problem,
  k,
  onResult,
  disabled,
}: {
  problem: Problem;
  k: string;
  onResult: (k: string, r: CheckResult, first: boolean) => void;
  disabled?: boolean;
}) {
  const u = problem.unknowns.find((x) => x.key === k)!;
  const { settings } = useProgress();
  const [input, setInput] = useState('');
  const [result, setResult] = useState<CheckResult | null>(null);
  const [tries, setTries] = useState(0);
  const solved = result?.status === 'correct';
  const submit = (value: string) => {
    const r = checkAnswer(problem, k, value, settings.tol);
    setResult(r);
    if (r.status === 'invalid') return;
    const first = tries === 0;
    setTries((t) => t + 1);
    onResult(k, r, first);
    if (r.status === 'wrong') logMistake({ problem: problem.id, key: k, mistake: r.mistake, input: value });
    recordPractice(r.status === 'correct');
  };
  return (
    <div className={`answer ${solved ? 'solved' : result?.status === 'wrong' ? 'wrong' : ''}`}>
      <div className="answer-label">
        <span className="answer-sym">
          <Tex tex={u.sym} />
        </span>
        <span>{u.label}</span>
        {solved && <span className="badge ok">✓ correct</span>}
      </div>
      {u.choices ? (
        <div className="choices" role="group" aria-label={u.label}>
          {u.choices.map((c, i) => (
            <button
              key={i}
              type="button"
              className={`btn small ${solved && problem.answers[k] === i ? 'primary' : ''}`}
              disabled={disabled || solved}
              onClick={() => submit(String(i))}
            >
              {c}
            </button>
          ))}
        </div>
      ) : (
        <form
          className="answer-form"
          onSubmit={(e) => {
            e.preventDefault();
            submit(input);
          }}
        >
          <div className="input-unit">
            <input
              type="text"
              inputMode="text"
              autoComplete="off"
              spellCheck={false}
              aria-label={`${u.label} in ${u.unit || 'plain number'}`}
              placeholder={u.unit === 'A' ? 'e.g. 90u or 90 µA' : u.unit === 'Ω' ? 'e.g. 9k' : u.unit === 'S' ? 'e.g. 0.6m' : u.unit === 'V' ? 'e.g. 0.9' : 'number'}
              value={input}
              disabled={disabled || solved}
              onChange={(e) => setInput(e.target.value)}
            />
            {u.unit && <span className="unit-chip">{u.unit}</span>}
          </div>
          <button className="btn small dark" type="submit" disabled={disabled || solved || !input.trim()}>
            Check
          </button>
        </form>
      )}
      {result && (
        <p className={`feedback ${result.status}`} role="status">
          {result.status === 'correct' ? '✓ ' : result.status === 'wrong' ? '✗ ' : ''}
          {result.message}
        </p>
      )}
    </div>
  );
}

export function ProblemView({
  problem,
  mode = 'independent',
  onResult,
  compact,
  number,
}: {
  problem: Problem;
  mode?: ProblemMode;
  onResult?: (k: string, r: CheckResult, first: boolean) => void;
  compact?: boolean;
  number?: number;
}) {
  const [hints, setHints] = useState(0);
  const [showSolution, setShowSolution] = useState(mode === 'worked');
  const [focus, setFocus] = useState<TraceStep | null>(null);
  return (
    <article className={`problem ${compact ? 'compact' : ''}`} aria-label={problem.title}>
      <header className="problem-head">
        {number !== undefined && <span className="problem-num">{number}</span>}
        <div>
          <div className="eyebrow">
            {mode === 'faded' ? 'Guided · ' : mode === 'worked' ? 'Worked example · ' : ''}
            {problem.source} · {problem.tags.join(', ')}
          </div>
          <h3>{problem.title}</h3>
        </div>
      </header>
      {problem.flags?.map((f, i) => (
        <p key={i} className="callout small">
          ⚑ {f}
        </p>
      ))}
      <div className="problem-body">
        {problem.figure && (
          <div className="problem-figure bench">
            <Figure kind={problem.figure.kind} props={problem.figure.props} highlight={focus?.highlight} />
          </div>
        )}
        <div className="problem-text">
          <p>{problem.statement}</p>
          <Givens problem={problem} />
        </div>
      </div>
      {mode === 'faded' && (
        <div className="scaffold">
          <div className="eyebrow">The method (fill in the numbers yourself)</div>
          <StepTrace steps={problem.steps} hideValues />
        </div>
      )}
      {mode !== 'worked' && (
        <div className="answers">
          {problem.unknowns.map((u) => (
            <AnswerRow key={u.key} problem={problem} k={u.key} onResult={(k, r, f) => onResult?.(k, r, f)} />
          ))}
        </div>
      )}
      {mode !== 'worked' && (
        <div className="hints">
          {problem.hints.slice(0, hints).map((h, i) => (
            <p key={i} className="hint">
              <span className="hint-rung">Hint {i + 1}</span> {h}
            </p>
          ))}
          <div className="row">
            {hints < 4 && (
              <button type="button" className="btn small ghost" onClick={() => setHints((h) => h + 1)}>
                {hints === 0 ? 'I’m stuck: give me a nudge' : 'Next hint'}
              </button>
            )}
            <button type="button" className="btn small ghost" onClick={() => setShowSolution((s) => !s)}>
              {showSolution ? 'Hide full solution' : 'Show full solution'}
            </button>
          </div>
        </div>
      )}
      {showSolution && (
        <div className="solution">
          <div className="eyebrow">{mode === 'worked' ? 'Worked example: hover a step to see it on the circuit' : 'Full solution'}</div>
          <StepTrace steps={problem.steps} onFocusStep={setFocus} />
          <p className="small muted">
            Answers:{' '}
            {problem.unknowns.map((u, i) => (
              <span key={u.key}>
                {i > 0 && ' · '}
                <Tex tex={u.sym} /> = {u.choices ? u.choices[problem.answers[u.key]] : <Tex tex={u.unit ? texSI(problem.answers[u.key], u.unit, 3) : String(Number(problem.answers[u.key].toPrecision(3)))} />}
              </span>
            ))}
          </p>
        </div>
      )}
    </article>
  );
}
