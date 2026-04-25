// Numerology primitives — Pythagorean letter→number mapping, reductions,
// chain walking. Mirrors the Python `numerology.py` module function-for-
// function so behavior stays identical; the parity-check script verifies
// known outputs.

// ─── Types ────────────────────────────────────────────────────────────

/**
 * Date-only structure — avoids JS Date timezone gotchas. Month is 1-12.
 */
export type BirthDate = {
  year: number;
  month: number; // 1-12
  day: number;
};

/** Output of chainInfo() — every field the Python helper returned. */
export type ChainInfo = {
  raw: number;
  chain: number[];
  final: number;
  single: number;
  masters: number[];
  karmicDebts: number[];
  notation: string;
};

// ─── Constants ────────────────────────────────────────────────────────

export const PYTHAGOREAN: Record<string, number> = {
  A: 1, B: 2, C: 3, D: 4, E: 5, F: 6, G: 7, H: 8, I: 9,
  J: 1, K: 2, L: 3, M: 4, N: 5, O: 6, P: 7, Q: 8, R: 9,
  S: 1, T: 2, U: 3, V: 4, W: 5, X: 6, Y: 7, Z: 8,
};

// Decoz / World Numerology treats Y as a vowel.
export const VOWELS = new Set(["A", "E", "I", "O", "U", "Y"]);
export const MASTER_NUMBERS = new Set([11, 22, 33]);
export const KARMIC_DEBTS = new Set([13, 14, 16, 19]);

// ─── Date helpers ─────────────────────────────────────────────────────

const MS_PER_DAY = 86_400_000;

/** Days between two BirthDates, ignoring time-of-day and timezone. */
export function daysBetween(a: BirthDate, b: BirthDate): number {
  const ma = Date.UTC(a.year, a.month - 1, a.day);
  const mb = Date.UTC(b.year, b.month - 1, b.day);
  return Math.floor((mb - ma) / MS_PER_DAY);
}

/** Age in years (floor at day boundary, like Python's `(today-dob).days // 365`). */
export function ageYears(dob: BirthDate, today: BirthDate): number {
  return Math.floor(daysBetween(dob, today) / 365);
}

/** Today in the Asia/Jakarta timezone, as a BirthDate. */
export function todayJakarta(): BirthDate {
  const fmt = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Jakarta",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
  // en-CA gives ISO-like "2026-04-25" output.
  const parts = fmt.format(new Date()).split("-");
  return {
    year: Number(parts[0]),
    month: Number(parts[1]),
    day: Number(parts[2]),
  };
}

/** ISO day-of-week (Mon=0…Sun=6) — matches Python's date.weekday(). */
export function pyWeekday(d: BirthDate): number {
  const js = new Date(Date.UTC(d.year, d.month - 1, d.day)).getUTCDay();
  // JS: Sun=0…Sat=6. Python: Mon=0…Sun=6.
  return (js + 6) % 7;
}

// ─── Number reductions ────────────────────────────────────────────────

export function digitSum(n: number): number {
  let total = 0;
  let v = Math.abs(n);
  while (v > 0) {
    total += v % 10;
    v = Math.floor(v / 10);
  }
  return total;
}

/** Reduce until 1-9 OR a master number. */
export function reduceNumber(n: number): number {
  let v = n;
  while (v > 9 && !MASTER_NUMBERS.has(v)) {
    v = digitSum(v);
  }
  return v;
}

/** Reduce all the way to 1-9, ignoring master numbers. */
export function reduceToSingle(n: number): number {
  let v = n;
  while (v > 9) v = digitSum(v);
  return v;
}

/**
 * Walk the reduction chain. Returns every intermediate, the final
 * (master-preserved when keepMaster), the single-digit form, masters
 * encountered, karmic debts encountered, and a slash-notation string
 * of the meaningful waypoints (raw / master / final).
 */
export function chainInfo(raw: number, keepMaster = true): ChainInfo {
  const chain: number[] = [raw];
  let n = raw;
  if (keepMaster) {
    while (n > 9 && !MASTER_NUMBERS.has(n)) {
      n = digitSum(n);
      chain.push(n);
    }
  } else {
    while (n > 9) {
      n = digitSum(n);
      chain.push(n);
    }
  }
  const final = chain[chain.length - 1];
  let single = final;
  while (single > 9) single = digitSum(single);

  const masters = chain.filter((x) => MASTER_NUMBERS.has(x));
  const debts = chain.filter((x) => KARMIC_DEBTS.has(x));

  // Build notation: include master intermediates between raw and final.
  const parts: number[] = [chain[0]];
  for (const mid of chain.slice(1, -1)) {
    if (MASTER_NUMBERS.has(mid)) parts.push(mid);
  }
  if (final !== chain[0]) parts.push(final);
  const notation = parts.length > 1 ? parts.join("/") : String(parts[0]);

  return { raw, chain, final, single, masters, karmicDebts: debts, notation };
}

/** Reduce raw to (notation, final) preserving master. */
export function reduceStopAtMaster(raw: number): {
  notation: string;
  final: number;
} {
  let n = raw;
  while (n > 9 && !MASTER_NUMBERS.has(n)) n = digitSum(n);
  return { notation: raw === n ? String(n) : `${raw}/${n}`, final: n };
}

/**
 * Reduce all the way to 1-9; return notation that keeps master
 * intermediates. Used for Personal Day where the daily vibration is
 * always single-digit but master intermediates add flavor.
 *
 * Examples: '29/11/2', '25/7', '7'.
 */
export function reduceFullWithChain(raw: number): {
  notation: string;
  final: number;
  masters: number[];
} {
  const chain: number[] = [raw];
  let n = raw;
  while (n > 9) {
    n = digitSum(n);
    chain.push(n);
  }
  const final = chain[chain.length - 1];
  const masters = chain.filter((x) => MASTER_NUMBERS.has(x));
  const parts: number[] = [chain[0]];
  for (const mid of chain.slice(1, -1)) {
    if (MASTER_NUMBERS.has(mid)) parts.push(mid);
  }
  parts.push(final);
  if (parts.length === 2 && parts[0] === parts[1]) {
    return { notation: String(final), final, masters };
  }
  return { notation: parts.join("/"), final, masters };
}

/** Reduce the absolute value of `n`, preserving master. */
export function absReduce(n: number): number {
  return reduceNumber(Math.abs(n));
}

// ─── Letter helpers ───────────────────────────────────────────────────

type LetterFilter = { onlyVowels?: boolean; onlyConsonants?: boolean };

function shouldCount(ch: string, filter: LetterFilter): boolean {
  if (!(ch in PYTHAGOREAN)) return false;
  if (filter.onlyVowels && !VOWELS.has(ch)) return false;
  if (filter.onlyConsonants && VOWELS.has(ch)) return false;
  return true;
}

export function lettersSum(name: string, filter: LetterFilter = {}): number {
  let total = 0;
  for (const ch of name.toUpperCase()) {
    if (shouldCount(ch, filter)) total += PYTHAGOREAN[ch];
  }
  return reduceNumber(total);
}

/** Split full name into individual word components, uppercased. */
export function nameWords(fullName: string): string[] {
  return fullName
    .toUpperCase()
    .split(/\s+/)
    .filter((w) => [...w].some((c) => c in PYTHAGOREAN));
}

export function wordLetterSum(word: string, filter: LetterFilter = {}): number {
  let total = 0;
  for (const ch of word) {
    if (shouldCount(ch, filter)) total += PYTHAGOREAN[ch];
  }
  return total;
}

/**
 * Hans Decoz: reduce each name (first/middle/last) separately, then
 * combine. Preserves master numbers + karmic debts that surface at
 * component level.
 */
export function nameFull(
  fullName: string,
  filter: LetterFilter = {},
): ChainInfo & { perWord: (ChainInfo & { word: string })[] } {
  const words = nameWords(fullName);
  const perWord = words.map((w) => {
    const raw = wordLetterSum(w, filter);
    return { ...chainInfo(raw, true), word: w };
  });
  const total = perWord.reduce((acc, w) => acc + w.final, 0);
  const overall = chainInfo(total, true);
  return { ...overall, perWord };
}
