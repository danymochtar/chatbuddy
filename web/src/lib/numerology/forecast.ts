// Decoz forecast layer — Period Cycles, Pinnacles, Challenges,
// Transits, Essence. Mirrors numerology.py: period_cycles,
// current_period_cycle, pinnacles, challenges, current_pinnacle_challenge,
// _transit_for_word, transits, essence.

import {
  type BirthDate,
  type ChainInfo,
  MASTER_NUMBERS,
  PYTHAGOREAN,
  absReduce,
  ageYears,
  chainInfo,
  digitSum,
  nameWords,
  reduceNumber,
} from "./core";
import { lifePath } from "./numbers";

// ─── Period Cycles (3 chapters of life) ───────────────────────────────

export type PeriodCycle = {
  period: 1 | 2 | 3;
  number: number;
  startAge: number;
  /** null = open-ended (period 3 runs to end of life). */
  endAge: number | null;
};

export type CurrentPeriodCycle = PeriodCycle & { age: number };

/**
 * Decoz Three Period Cycles — the three chapters of your Life Path.
 *
 * - Period 1 = birth month (master preserved). From birth to the
 *   first Personal Year 1 that lands on age >= 27.
 * - Period 2 = birth day (master preserved). Lasts 27 years.
 * - Period 3 = birth year reduced (master preserved). Rest of life.
 */
export function periodCycles(dob: BirthDate): [PeriodCycle, PeriodCycle, PeriodCycle] {
  const bm = reduceNumber(dob.month);
  const bd = reduceNumber(dob.day);
  const by = reduceNumber(digitSum(dob.year));

  // Locate the first Personal Year 1 that occurs on or after age 27.
  let transitionYear: number | null = null;
  const baseYear = dob.year + 27;
  for (let y = baseYear; y < baseYear + 9; y++) {
    const uy = reduceNumber(digitSum(y));
    const py = reduceNumber(bm + bd + uy);
    if (py === 1) {
      transitionYear = y;
      break;
    }
  }
  if (transitionYear === null) transitionYear = baseYear;

  const p1EndAge = transitionYear - dob.year;

  return [
    { period: 1, number: bm, startAge: 0, endAge: p1EndAge },
    { period: 2, number: bd, startAge: p1EndAge + 1, endAge: p1EndAge + 27 },
    { period: 3, number: by, startAge: p1EndAge + 28, endAge: null },
  ];
}

export function currentPeriodCycle(
  dob: BirthDate,
  today: BirthDate,
): CurrentPeriodCycle {
  const age = ageYears(dob, today);
  const cycles = periodCycles(dob);
  for (const cyc of cycles) {
    const end = cyc.endAge ?? Number.POSITIVE_INFINITY;
    if (age <= end) return { ...cyc, age };
  }
  return { ...cycles[cycles.length - 1], age };
}

// ─── Pinnacles + Challenges (4 phases) ────────────────────────────────

export type Pinnacle = {
  period: 1 | 2 | 3 | 4;
  startAge: number;
  endAge: number | null;
  number: number;
};

export type Challenge = Pinnacle;

function firstPinnacleEndAge(lp: number): number {
  const reduced = MASTER_NUMBERS.has(lp)
    ? reduceNumber(Math.floor(lp / 10) + (lp % 10))
    : lp;
  return 36 - reduced;
}

export function pinnacles(dob: BirthDate): [Pinnacle, Pinnacle, Pinnacle, Pinnacle] {
  const m = reduceNumber(dob.month);
  const d = reduceNumber(dob.day);
  const y = reduceNumber(digitSum(dob.year));
  const p1 = reduceNumber(m + d);
  const p2 = reduceNumber(d + y);
  const p3 = reduceNumber(p1 + p2);
  const p4 = reduceNumber(m + y);
  const lp = lifePath(dob);
  const end1 = firstPinnacleEndAge(lp);
  return [
    { period: 1, startAge: 0, endAge: end1, number: p1 },
    { period: 2, startAge: end1 + 1, endAge: end1 + 9, number: p2 },
    { period: 3, startAge: end1 + 10, endAge: end1 + 18, number: p3 },
    { period: 4, startAge: end1 + 19, endAge: null, number: p4 },
  ];
}

export function challenges(
  dob: BirthDate,
): [Challenge, Challenge, Challenge, Challenge] {
  const m = reduceNumber(dob.month);
  const d = reduceNumber(dob.day);
  const y = reduceNumber(digitSum(dob.year));
  const c1 = absReduce(m - d);
  const c2 = absReduce(d - y);
  const c3 = absReduce(c1 - c2);
  const c4 = absReduce(m - y);
  const lp = lifePath(dob);
  const end1 = firstPinnacleEndAge(lp);
  return [
    { period: 1, startAge: 0, endAge: end1, number: c1 },
    { period: 2, startAge: end1 + 1, endAge: end1 + 9, number: c2 },
    { period: 3, startAge: end1 + 10, endAge: end1 + 18, number: c3 },
    { period: 4, startAge: end1 + 19, endAge: null, number: c4 },
  ];
}

export type CurrentPinnacleChallenge = {
  age: number;
  period: 1 | 2 | 3 | 4;
  pinnacle: number;
  challenge: number;
};

export function currentPinnacleChallenge(
  dob: BirthDate,
  today: BirthDate,
): CurrentPinnacleChallenge {
  const age = ageYears(dob, today);
  const pins = pinnacles(dob);
  const chals = challenges(dob);
  for (let i = 0; i < pins.length; i++) {
    const end = pins[i].endAge ?? Number.POSITIVE_INFINITY;
    if (age <= end) {
      return {
        age,
        period: pins[i].period,
        pinnacle: pins[i].number,
        challenge: chals[i].number,
      };
    }
  }
  return {
    age,
    period: 4,
    pinnacle: pins[3].number,
    challenge: chals[3].number,
  };
}

// ─── Transits (active letter per name layer) ──────────────────────────

export type TransitInfo = {
  letter: string;
  value: number;
  startedAtAge: number;
  endsAtAge: number;
  yearInLetter: number;
  remainingYears: number;
};

/**
 * Find the active letter in a transit cycle at a given age.
 *
 * Each letter is active for as many years as its Pythagorean value.
 * After the last letter, cycle restarts from the first. So a name
 * summing to N years repeats every N years.
 */
function transitForWord(word: string, age: number): TransitInfo | null {
  const letters: { ch: string; val: number }[] = [];
  for (const ch of word.toUpperCase()) {
    if (ch in PYTHAGOREAN) letters.push({ ch, val: PYTHAGOREAN[ch] });
  }
  if (letters.length === 0) return null;
  const cycleLength = letters.reduce((a, b) => a + b.val, 0);
  const pos = age % cycleLength;
  let cumulative = 0;
  for (const { ch, val } of letters) {
    if (cumulative + val > pos) {
      const yearInLetter = pos - cumulative + 1;
      const started = age - (yearInLetter - 1);
      return {
        letter: ch,
        value: val,
        startedAtAge: started,
        endsAtAge: started + val - 1,
        yearInLetter,
        remainingYears: val - yearInLetter,
      };
    }
    cumulative += val;
  }
  return null;
}

export type Transits = {
  age: number;
  physical: TransitInfo | null;
  mental: TransitInfo | null;
  spiritual: TransitInfo | null;
};

/**
 * Decoz Three Transits — currently active letter per name layer:
 * Physical = first name, Mental = middle name, Spiritual = last name.
 *
 * Edge cases:
 * - 1 word: all three layers cycle through the same word.
 * - 2 words: Physical=first, Spiritual=last, Mental absent.
 * - 3+ words: Mental uses the first middle word.
 */
export function transits(
  fullName: string,
  dob: BirthDate,
  today: BirthDate,
): Transits {
  const age = ageYears(dob, today);
  const words = nameWords(fullName);
  if (words.length === 0) {
    return { age, physical: null, mental: null, spiritual: null };
  }
  let first: string;
  let middle: string | null;
  let last: string;
  if (words.length === 1) {
    first = middle = last = words[0];
  } else if (words.length === 2) {
    first = words[0];
    last = words[1];
    middle = null;
  } else {
    first = words[0];
    middle = words[1];
    last = words[words.length - 1];
  }
  return {
    age,
    physical: transitForWord(first, age),
    mental: middle ? transitForWord(middle, age) : null,
    spiritual: transitForWord(last, age),
  };
}

// ─── Essence Cycle ────────────────────────────────────────────────────

export type EssenceContributor = { letter: string; value: number } | null;

export type Essence = ChainInfo & {
  contributors: {
    physical: EssenceContributor;
    mental: EssenceContributor;
    spiritual: EssenceContributor;
  };
  age: number;
};

/**
 * Decoz Essence Cycle — sum of the three currently active transit
 * letter values for the year. Double-digit form preserved so karmic
 * debts (13/14/16/19) and masters (11/22/33) surface as flavor; the
 * reduced single digit is the headline theme.
 *
 * If a layer is missing (no middle name), it contributes 0.
 */
export function essence(
  fullName: string,
  dob: BirthDate,
  today: BirthDate,
): Essence {
  const t = transits(fullName, dob, today);
  let raw = 0;
  const contributors: Essence["contributors"] = {
    physical: null,
    mental: null,
    spiritual: null,
  };
  for (const layer of ["physical", "mental", "spiritual"] as const) {
    const info = t[layer];
    if (info) {
      raw += info.value;
      contributors[layer] = { letter: info.letter, value: info.value };
    }
  }
  const info = raw
    ? chainInfo(raw, true)
    : {
        raw: 0,
        chain: [0],
        final: 0,
        single: 0,
        masters: [],
        karmicDebts: [],
        notation: "0",
      };
  return { ...info, contributors, age: t.age };
}
