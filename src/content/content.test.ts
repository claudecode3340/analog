/**
 * Content lint (CLAUDE.md §11.5): every symbol defined; a visual present; a prediction question present;
 * text per step ≤ ~120 words; notation matches §6.
 */
import { describe, expect, it } from 'vitest';
import { wordCount } from '../ui/RichText';
import { GLOSSARY } from './glossary';
import { BANK_BY_ID, GENERATOR_BY_ID, LESSONS, UNITS } from './index';

const WIDGETS = ['nodeWalk', 'parallelSplit', 'tap', 'channel', 'family', 'recipeMini', 'pmosFlip', 'tangent', 'roSlope', 'csTransfer'];
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
  it('card ids are unique', () => {
    const ids = LESSONS.flatMap((l) => l.lockIn.cards.map((c) => c.id));
    expect(new Set(ids).size).toBe(ids.length);
  });
});
