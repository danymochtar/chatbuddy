// Core numbers — Life Path, Expression, Soul Urge, Personality, Birthday.
// Mirrors numerology.py: life_path{,_full}, expression{_full,_number},
// soul_urge{_full,_number}, personality{_full,_number}, birthday{_full,_number}.

import {
  type BirthDate,
  type ChainInfo,
  PYTHAGOREAN,
  chainInfo,
  digitSum,
  nameFull,
  nameWords,
  reduceNumber,
  wordLetterSum,
} from "./core";

// ─── Life Path ────────────────────────────────────────────────────────

export type LifePathInfo = ChainInfo & {
  components: {
    month: ChainInfo;
    day: ChainInfo;
    year: ChainInfo;
  };
  /** Set when a 33 was demoted to 6 because no other masters appeared. */
  demotedFrom33?: boolean;
};

/**
 * Decoz Life Path — reduce Month, Day, Year separately first, then sum.
 *
 * The per-component reduction is what surfaces karmic debt at the
 * summing stage (e.g. 5 + 8 + 6 = 19 — karmic debt 19 — even though
 * every component reduces cleanly).
 */
export function lifePathFull(dob: BirthDate): LifePathInfo {
  const mRaw = dob.month;
  const dRaw = dob.day;
  const yDigitsSum = digitSum(dob.year);
  const mRed = reduceNumber(mRaw);
  const dRed = reduceNumber(dRaw);
  const yRed = reduceNumber(yDigitsSum);
  const total = mRed + dRed + yRed;
  const info = chainInfo(total, true);
  return {
    ...info,
    components: {
      month: chainInfo(mRaw, true),
      day: chainInfo(dRaw, true),
      year: chainInfo(yDigitsSum, true),
    },
  };
}

export function lifePath(dob: BirthDate): number {
  return lifePathFull(dob).final;
}

// ─── Expression / Soul Urge / Personality (per-word reduce-then-sum) ──

export function expressionFull(fullName: string) {
  return nameFull(fullName);
}

export function soulUrgeFull(fullName: string) {
  return nameFull(fullName, { onlyVowels: true });
}

export function personalityFull(fullName: string) {
  return nameFull(fullName, { onlyConsonants: true });
}

export function expressionNumber(fullName: string): number {
  return expressionFull(fullName).final;
}

export function soulUrgeNumber(fullName: string): number {
  return soulUrgeFull(fullName).final;
}

export function personalityNumber(fullName: string): number {
  return personalityFull(fullName).final;
}

// ─── Birthday ─────────────────────────────────────────────────────────

/** Birth Day single-digit (or master) reading. */
export function birthdayNumber(dob: BirthDate): number {
  return reduceNumber(dob.day);
}

/**
 * Full Birth Day info — preserves the double digit so karmic debts
 * (13, 14, 16, 19) and master Birth Days (11, 22) surface naturally.
 * Day 22 stays 22 (master), day 13 reduces to 4 with karmic 13 in chain.
 */
export function birthdayFull(dob: BirthDate): ChainInfo {
  return chainInfo(dob.day, true);
}

// ─── Maturity / Balance / Rational Thought ────────────────────────────

export function maturityNumber(lp: number, ex: number): number {
  return reduceNumber(lp + ex);
}

/** First letter of each name word, summed and reduced. */
export function balanceNumber(fullName: string): number {
  let total = 0;
  for (const word of fullName.toUpperCase().split(/\s+/)) {
    for (const ch of word) {
      if (ch in PYTHAGOREAN) {
        total += PYTHAGOREAN[ch];
        break;
      }
    }
  }
  return reduceNumber(total);
}

/**
 * Decoz Rational Thought — sum of letters in first name + Birth Day
 * number. Master numbers preserved.
 */
export function rationalThoughtFull(
  fullName: string,
  dob: BirthDate,
): ChainInfo {
  const words = nameWords(fullName);
  const firstNameSum = words.length ? wordLetterSum(words[0]) : 0;
  return chainInfo(firstNameSum + dob.day, true);
}
