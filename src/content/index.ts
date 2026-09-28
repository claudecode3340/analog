import { FIXED_BANK } from '../practice/bank';
import { M3_BANK } from '../practice/bankM3';
import { M4_BANK } from '../practice/bankM4';
import { M5_BANK } from '../practice/bankM5';
import { M6_BANK } from '../practice/bankM6';
import { LAB_BANK } from '../practice/bankLabs';
import { CHAT_BANK } from '../practice/bankChat';
import { ALL_GENERATORS } from '../practice/generators';

import type { Generator, Problem } from '../practice/schema';
import { AUDIT_CARDS } from './audit';
import { UNITS } from './curriculum';
import { FOUNDATION_LESSONS } from './lessons/foundations';
import { SINGLE_STAGE_LESSONS } from './lessons/single';
import { DIFF_LESSONS } from './lessons/diff';
import { HANDOUT_LESSONS } from './lessons/handout';
import { LATE_LESSONS } from './lessons/late';
import { STABILITY_LESSONS } from './lessons/stability';
import type { Lesson, Unit } from './types';

const RAW_LESSONS: Lesson[] = [...FOUNDATION_LESSONS, ...SINGLE_STAGE_LESSONS, ...DIFF_LESSONS, ...HANDOUT_LESSONS, ...LATE_LESSONS, ...STABILITY_LESSONS];
/** Curriculum order: by unit, then by the unit's own lesson list (so "next lesson" follows the Path). */
const ORDER: Record<string, number> = Object.fromEntries(UNITS.flatMap((u) => u.lessons).map((id, i) => [id, i]));
export const LESSONS: Lesson[] = [...RAW_LESSONS].sort((a, b) => (ORDER[a.id] ?? 1e9) - (ORDER[b.id] ?? 1e9));
export const LESSON_BY_ID: Record<string, Lesson> = Object.fromEntries(LESSONS.map((l) => [l.id, l]));
export const UNIT_BY_ID: Record<string, Unit> = Object.fromEntries(UNITS.map((u) => [u.id, u]));
export const GENERATORS: Generator[] = ALL_GENERATORS;
export const GENERATOR_BY_ID: Record<string, Generator> = Object.fromEntries(GENERATORS.map((g) => [g.id, g]));
export const BANK: Problem[] = [...FIXED_BANK, ...M3_BANK, ...M4_BANK, ...M5_BANK, ...M6_BANK, ...LAB_BANK, ...CHAT_BANK];
export const BANK_BY_ID: Record<string, Problem> = Object.fromEntries(BANK.map((p) => [p.id, p]));

export { UNITS };

/** All review cards, by id, with the lesson they come from. */
export const CARDS = [
  ...LESSONS.flatMap((l) => l.lockIn.cards.map((c) => ({ ...c, lesson: l.id, unit: l.unit }))),
  ...AUDIT_CARDS.map((c) => ({ ...c, lesson: 'audit', unit: 'Audit' })),
];
export const CARD_BY_ID = Object.fromEntries(CARDS.map((c) => [c.id, c]));
