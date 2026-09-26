import type { Generator } from '../schema';
import { FOUNDATION_GENERATORS } from './foundations';
import { SINGLE_STAGE_GENERATORS } from './single';
import { DIFF_GENERATORS } from './diff';
import { HANDOUT_GENERATORS } from './handout';

export const ALL_GENERATORS: Generator[] = [...FOUNDATION_GENERATORS, ...SINGLE_STAGE_GENERATORS, ...DIFF_GENERATORS, ...HANDOUT_GENERATORS];
