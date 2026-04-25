// Decoz extras — karmic debts/lessons, hidden passion, planes of
// expression, bridges, cornerstone/capstone/first vowel, subconscious
// self. Mirrors numerology.py: _detect_karmic_debt, life_path_karmic,
// expression_karmic, soul_urge_karmic, personality_karmic,
// karmic_lessons, hidden_passion, planes_of_expression, bridge,
// cornerstone, capstone, first_vowel, subconscious_self.

import {
  type BirthDate,
  KARMIC_DEBTS,
  MASTER_NUMBERS,
  PYTHAGOREAN,
  VOWELS,
  digitSum,
  nameWords,
  reduceNumber,
  reduceToSingle,
} from "./core";
import { PLANE_LETTERS, type Plane } from "./data/planes";

// ─── Karmic debts ─────────────────────────────────────────────────────

/** Walk the master-preserving chain; return the first karmic debt encountered. */
function detectKarmicDebt(rawSum: number): number | null {
  let n = rawSum;
  while (n > 9 && !MASTER_NUMBERS.has(n)) {
    if (KARMIC_DEBTS.has(n)) return n;
    n = digitSum(n);
  }
  return null;
}

export function lifePathKarmic(dob: BirthDate): number | null {
  const m = reduceNumber(dob.month);
  const d = reduceNumber(dob.day);
  const y = reduceNumber(digitSum(dob.year));
  return detectKarmicDebt(m + d + y);
}

export function expressionKarmic(name: string): number | null {
  let total = 0;
  for (const ch of name.toUpperCase()) {
    if (ch in PYTHAGOREAN) total += PYTHAGOREAN[ch];
  }
  return detectKarmicDebt(total);
}

export function soulUrgeKarmic(name: string): number | null {
  let total = 0;
  for (const ch of name.toUpperCase()) {
    if (VOWELS.has(ch) && ch in PYTHAGOREAN) total += PYTHAGOREAN[ch];
  }
  return detectKarmicDebt(total);
}

export function personalityKarmic(name: string): number | null {
  let total = 0;
  for (const ch of name.toUpperCase()) {
    if (ch in PYTHAGOREAN && !VOWELS.has(ch)) total += PYTHAGOREAN[ch];
  }
  return detectKarmicDebt(total);
}

// ─── Karmic lessons ───────────────────────────────────────────────────

/** Numbers 1-9 missing from the full birth name. */
export function karmicLessons(name: string): number[] {
  const present = new Set<number>();
  for (const ch of name.toUpperCase()) {
    if (ch in PYTHAGOREAN) present.add(PYTHAGOREAN[ch]);
  }
  const lessons: number[] = [];
  for (let n = 1; n <= 9; n++) {
    if (!present.has(n)) lessons.push(n);
  }
  return lessons;
}

// ─── Hidden Passion ───────────────────────────────────────────────────

/** Most-frequent number(s) in the full name. */
export function hiddenPassion(name: string): number[] {
  const counts = new Map<number, number>();
  for (const ch of name.toUpperCase()) {
    if (ch in PYTHAGOREAN) {
      const v = PYTHAGOREAN[ch];
      counts.set(v, (counts.get(v) ?? 0) + 1);
    }
  }
  if (counts.size === 0) return [];
  const max = Math.max(...counts.values());
  return [...counts.entries()]
    .filter(([, c]) => c === max)
    .map(([n]) => n)
    .sort((a, b) => a - b);
}

// ─── Planes of Expression ─────────────────────────────────────────────

export type PlanesOfExpression = {
  sums: Record<Plane, number>;
  counts: Record<Plane, number>;
  reduced: Record<Plane, number>;
  dominant: Plane | null;
};

/**
 * Decoz Planes of Expression — categorize letters of the full name
 * into Physical / Mental / Emotional / Intuitive groupings, sum
 * values per plane, reduce, and surface the dominant plane.
 */
export function planesOfExpression(fullName: string): PlanesOfExpression {
  const sums: Record<Plane, number> = {
    physical: 0,
    mental: 0,
    emotional: 0,
    intuitive: 0,
  };
  const counts: Record<Plane, number> = {
    physical: 0,
    mental: 0,
    emotional: 0,
    intuitive: 0,
  };
  for (const ch of fullName.toUpperCase()) {
    if (!(ch in PYTHAGOREAN)) continue;
    const val = PYTHAGOREAN[ch];
    for (const plane of ["physical", "mental", "emotional", "intuitive"] as Plane[]) {
      if (PLANE_LETTERS[plane].has(ch)) {
        sums[plane] += val;
        counts[plane] += 1;
        break;
      }
    }
  }
  const reduced: Record<Plane, number> = {
    physical: sums.physical ? reduceNumber(sums.physical) : 0,
    mental: sums.mental ? reduceNumber(sums.mental) : 0,
    emotional: sums.emotional ? reduceNumber(sums.emotional) : 0,
    intuitive: sums.intuitive ? reduceNumber(sums.intuitive) : 0,
  };
  const anyPositive = Object.values(sums).some((s) => s > 0);
  let dominant: Plane | null = null;
  if (anyPositive) {
    let best: Plane = "physical";
    for (const plane of ["mental", "emotional", "intuitive"] as Plane[]) {
      if (sums[plane] > sums[best]) best = plane;
    }
    dominant = best;
  }
  return { sums, counts, reduced, dominant };
}

// ─── Bridges ──────────────────────────────────────────────────────────

/**
 * Decoz Bridge = absolute difference between two reduced single-digit
 * forms of related core numbers. Range 0-8. Master inputs are reduced
 * to single digit first for subtraction.
 */
export function bridge(num1: number, num2: number): number {
  return Math.abs(reduceToSingle(num1) - reduceToSingle(num2));
}

// ─── Cornerstone / Capstone / First Vowel ─────────────────────────────

/** First letter of first name — how you approach opportunities & obstacles. */
export function cornerstone(fullName: string): string {
  const words = nameWords(fullName);
  if (!words.length) return "";
  for (const ch of words[0]) {
    if (ch in PYTHAGOREAN) return ch;
  }
  return "";
}

/** Last letter of first name — how you finish what you start. */
export function capstone(fullName: string): string {
  const words = nameWords(fullName);
  if (!words.length) return "";
  for (let i = words[0].length - 1; i >= 0; i--) {
    const ch = words[0][i];
    if (ch in PYTHAGOREAN) return ch;
  }
  return "";
}

/** First vowel of first name — soul-level window into deepest motivations. */
export function firstVowel(fullName: string): string {
  const words = nameWords(fullName);
  if (!words.length) return "";
  for (const ch of words[0]) {
    if (VOWELS.has(ch)) return ch;
  }
  return "";
}

// ─── Subconscious Self ────────────────────────────────────────────────

/**
 * Decoz: 9 minus the number of Karmic Lessons (missing numbers in
 * full birth name). Range 3-9. Higher = more numerical "tools" in
 * the name → more confident in surprise situations.
 */
export function subconsciousSelf(fullName: string): number {
  return 9 - karmicLessons(fullName).length;
}
