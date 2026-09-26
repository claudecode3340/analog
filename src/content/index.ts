import { FIXED_BANK } from '../practice/bank';
import { M3_BANK } from '../practice/bankM3';
import { ALL_GENERATORS } from '../practice/generators';

import type { Generator, Problem } from '../practice/schema';
import { UNITS } from './curriculum';
import { FOUNDATION_LESSONS } from './lessons/foundations';
import { SINGLE_STAGE_LESSONS } from './lessons/single';
import { DIFF_LESSONS } from './lessons/diff';
import type { Lesson, Unit } from './types';

export const LESSONS: Lesson[] = [...FOUNDATION_LESSONS, ...SINGLE_STAGE_LESSONS, ...DIFF_LESSONS];
export const LESSON_BY_ID: Record<string, Lesson> = Object.fromEntries(LESSONS.map((l) => [l.id, l]));
export const UNIT_BY_ID: Record<string, Unit> = Object.fromEntries(UNITS.map((u) => [u.id, u]));
export const GENERATORS: Generator[] = ALL_GENERATORS;
export const GENERATOR_BY_ID: Record<string, Generator> = Object.fromEntries(GENERATORS.map((g) => [g.id, g]));
export const BANK: Problem[] = [...FIXED_BANK, ...M3_BANK];
export const BANK_BY_ID: Record<string, Problem> = Object.fromEntries(BANK.map((p) => [p.id, p]));

export { UNITS };

/** All review cards, by id, with the lesson they come from. */
export const CARDS = LESSONS.flatMap((l) => l.lockIn.cards.map((c) => ({ ...c, lesson: l.id, unit: l.unit })));
export const CARD_BY_ID = Object.fromEntries(CARDS.map((c) => [c.id, c]));
