/**
 * Content lint (CLAUDE.md §11.5): every symbol defined; a visual present; a prediction question present;
 * text per step ≤ ~120 words; notation matches §6.
 */
import { describe, expect, it } from 'vitest';
import { wordCount } from '../ui/RichText';
import { GLOSSARY } from './glossary';
import { BANK_BY_ID, GENERATOR_BY_ID, LESSONS, UNITS } from './index';

import { WIDGETS as WIDGET_MAP } from '../learn/widgets';
const WIDGETS = Object.keys(WIDGET_MAP);
/** Symbols that are NOT the course notation (§6): Razavi's V_OD/V_TH, Sedra's V_t, k'n. */
const FORBIDDEN = [/V_\{?OD\}?/, /V_\{?TH\}?(?![a-z])/, /\bVOD\b/, /\bVTH\b/, /k'n/, /k′n/];

function allText(l: (typeof LESSONS)[number]): string[] {
  return [l.why, l.picture.caption, l.predict.prompt, l.predict.explain, ...l.predict.choices, l.idea, l.analogy ?? '', l.rule.note ?? '', l.lockIn.summary, l.lockIn.hook, ...l.lockIn.cards.flatMap((c) => [c.front, c.back])];
}

describe.each(LESSONS.map((l) => [l.id, l] as const))('lesson %s', (_id, l) => {
  it('follows the template: picture, predict, rule, worked, your turn, lock-in', () => {
    expect(l.why.length).toBeGreaterThan(20);
    const v = l.picture.visual;
    const key = 'widget' in v ? v.widget : v.kind;
    expect(key.length).toBeGreaterThan(0);
    if ('widget' in v) expect(WIDGETS).toContain(v.widget);
    expect(l.predict.choices.length).toBeGreaterThanOrEqual(2);
    expect(l.predict.answer).toBeLessThan(l.predict.choices.length);
    expect(l.rule.tex.length).toBeGreaterThan(0);
    expect(l.lockIn.cards.length).toBeGreaterThan(0);
    expect(l.yourTurn.count).toBeGreaterThanOrEqual(2);
  });

  it('keeps every step to ≤ 120 words', () => {
    for (const t of allText(l)) expect(wordCount(t), t.slice(0, 60)).toBeLessThanOrEqual(120);
  });

  it('references only existing glossary terms, generators and bank problems', () => {
    for (const t of allText(l)) {
      for (const m of t.matchAll(/\{\{([^}|]+)/g)) expect(GLOSSARY, `{{${m[1]}}}`).toHaveProperty(m[1]);
    }
    for (const s of l.rule.symbols) expect(GLOSSARY, s).toHaveProperty(s);
    if ('generator' in l.worked) expect(GENERATOR_BY_ID).toHaveProperty(l.worked.generator);
    if ('bank' in l.worked) expect(BANK_BY_ID).toHaveProperty(l.worked.bank);
    for (const g of l.yourTurn.generators) expect(GENERATOR_BY_ID).toHaveProperty(g);
  });

  it('uses the course notation', () => {
    for (const t of [...allText(l), ...l.rule.tex]) for (const re of FORBIDDEN) expect(t).not.toMatch(re);
  });
});

describe('curriculum', () => {
  it('every unit lesson exists and prerequisites point to real units', () => {
    const ids = new Set(LESSONS.map((l) => l.id));
    const unitIds = new Set(UNITS.map((u) => u.id));
    for (const u of UNITS) {
      for (const l of u.lessons) expect(ids.has(l), l).toBe(true);
      for (const p of u.prereqs) expect(unitIds.has(p), p).toBe(true);
    }
  });
  it('every lesson belongs to its unit', () => {
    for (const l of LESSONS) expect(UNITS.find((u) => u.id === l.unit)?.lessons).toContain(l.id);
  });
  it('every glossary term is introduced in a real lesson', () => {
    const ids = new Set(LESSONS.map((l) => l.id));
    for (const [k, g] of Object.entries(GLOSSARY)) expect(ids.has(g.firstIn), `${k} → ${g.firstIn}`).toBe(true);
  });
  it('glossary TeX survived escaping (no control characters, no bare command names)', () => {
    for (const [k, g] of Object.entries(GLOSSARY)) {
      expect(g.tex, k).not.toMatch(/[\u0000-\u001f]/);
      expect(g.tex, k).not.toMatch(/^(overline|beta|omega|gamma|mu|lambda|tau|varepsilon)/);
    }
  });
  it('card ids are unique', () => {
    const ids = LESSONS.flatMap((l) => l.lockIn.cards.map((c) => c.id));
    expect(new Set(ids).size).toBe(ids.length);
  });
});

/**
 * TeX escaping lint: a TeX string written with a single backslash inside a JS string loses it (\f becomes a
 * form feed, \o becomes “o”). Catch control characters and bare TeX command names in every TeX field.
 */
describe('TeX strings keep their backslashes', () => {
  const CTRL = /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/;
  const BARE = /(^|[^\\a-zA-Z])(frac|sqrt|overline|mathrm|text|tfrac|dfrac|left|right)[{(|.]/;
  const check = (where: string, tex: string) => {
    expect(CTRL.test(tex), `${where}: control character in ${JSON.stringify(tex)}`).toBe(false);
    expect(BARE.test(tex), `${where}: TeX command without backslash in ${JSON.stringify(tex)}`).toBe(false);
  };
  it('in lessons (rule, idea maths, cards)', () => {
    for (const l of LESSONS) {
      l.rule.tex.forEach((t) => check(`${l.id} rule`, t));
      for (const t of allText(l)) expect(CTRL.test(t), `${l.id}: control character`).toBe(false);
      for (const m of l.idea.match(/\$[^$]+\$/g) ?? []) check(`${l.id} idea`, m);
    }
  });
  it('in the fixed bank and generated problems (steps, givens, unknowns)', async () => {
    const { BANK } = await import('./index');
    const { generate } = await import('../practice/generate');
    const probs = [...BANK, ...Object.values(GENERATOR_BY_ID).map((g) => generate(g, 7))];
    for (const p of probs) {
      p.steps.forEach((s) => s.tex && check(`${p.id} step`, s.tex));
      p.givens.forEach((g) => check(`${p.id} given`, g.sym));
      p.unknowns.forEach((u) => check(`${p.id} unknown`, u.sym));
    }
  });
});
