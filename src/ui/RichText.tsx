/**
 * Tiny markup for lesson text: **bold**, *italic*, $inline TeX$, and {{glossary}} terms that show a
 * definition on hover, focus or tap.
 */
import { useState, type ReactNode } from 'react';
import { GLOSSARY } from '../content/glossary';
import { Tex } from './Tex';

export function Term({ k, children }: { k: string; children?: ReactNode }) {
  const g = GLOSSARY[k];
  const [open, setOpen] = useState(false);
  if (!g) return <span className="term-missing">{children ?? k}</span>;
  return (
    <span className="term-wrap">
      <button
        type="button"
        className="term"
        aria-expanded={open}
        onClick={() => setOpen((o) => !o)}
        onBlur={() => setOpen(false)}
        onMouseEnter={() => setOpen(true)}
        onMouseLeave={() => setOpen(false)}
      >
        {children ?? <Tex tex={g.tex} />}
      </button>
      {open && (
        <span role="tooltip" className="term-tip">
          <strong>
            <Tex tex={g.tex} /> {g.name}
          </strong>
          {g.unit && <span className="term-unit"> [{g.unit}]</span>}
          <br />
          {g.def}
        </span>
      )}
    </span>
  );
}

const TOKEN = /(\*\*[^*]+\*\*|\*[^*]+\*|\$[^$]+\$|\{\{[^}]+\}\})/g;

export function RichText({ text }: { text: string }) {
  const parts = text.split(TOKEN).filter((p) => p !== '');
  return (
    <>
      {parts.map((p, i) => {
        if (p.startsWith('**')) return <strong key={i}>{p.slice(2, -2)}</strong>;
        if (p.startsWith('*')) return <em key={i}>{p.slice(1, -1)}</em>;
        if (p.startsWith('$')) return <Tex key={i} tex={p.slice(1, -1)} />;
        if (p.startsWith('{{')) {
          const inner = p.slice(2, -2);
          const [k, label] = inner.split('|');
          return (
            <Term key={i} k={k}>
              {label}
            </Term>
          );
        }
        return <span key={i}>{p}</span>;
      })}
    </>
  );
}

/** Paragraphs separated by blank lines. */
export function Prose({ text }: { text: string }) {
  return (
    <>
      {text
        .trim()
        .split(/\n\s*\n/)
        .map((para, i) => (
          <p key={i}>
            <RichText text={para.replace(/\s*\n\s*/g, ' ')} />
          </p>
        ))}
    </>
  );
}

/** Words in a piece of lesson text, ignoring markup (for the ≤ 120-word lint). */
export function wordCount(text: string): number {
  return text
    .replace(/\$[^$]+\$/g, ' x ')
    .replace(/\{\{([^}|]+)(\|([^}]+))?\}\}/g, ' x ')
    .replace(/[*#]/g, '')
    .split(/\s+/)
    .filter(Boolean).length;
}
