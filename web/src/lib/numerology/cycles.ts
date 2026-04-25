// Personal cycles — Year, Month, Day. Plus Universal Day. Mirrors
// numerology.py: personal_year, personal_month, personal_day,
// universal_day{,_full}, personal_cycles_full.

import {
  type BirthDate,
  type ChainInfo,
  chainInfo,
  digitSum,
  reduceFullWithChain,
  reduceNumber,
  reduceStopAtMaster,
  reduceToSingle,
} from "./core";

/**
 * Personal Year — uses TODAY's universal year, not the birth year.
 * Master-preserved: 11, 22 can land here as the year theme.
 */
export function personalYear(dob: BirthDate, today: BirthDate): number {
  const bm = reduceNumber(dob.month);
  const bd = reduceNumber(dob.day);
  const cy = reduceNumber(digitSum(today.year));
  return reduceNumber(bm + bd + cy);
}

/** Personal Month — Personal Year + reduced current month. Master-preserved. */
export function personalMonth(dob: BirthDate, today: BirthDate): number {
  const py = personalYear(dob, today);
  const cm = reduceNumber(today.month);
  return reduceNumber(py + cm);
}

/**
 * Personal Day — Decoz: daily vibration is ALWAYS fully reduced to
 * 1-9. Master numbers can appear as intermediates in the chain
 * (captured in personalCyclesFull) but the day's primary energy is
 * single digit.
 */
export function personalDay(dob: BirthDate, today: BirthDate): number {
  const pm = personalMonth(dob, today);
  return reduceToSingle(pm + today.day);
}

/**
 * Universal Day — sum of all DDMMYYYY digits, fully reduced to 1-9.
 * Master numbers do NOT stop the reduction (per Decoz).
 */
export function universalDay(today: BirthDate): number {
  const total =
    digitSum(today.day) + digitSum(today.month) + digitSum(today.year);
  return reduceToSingle(total);
}

/** Universal Day with master intermediates captured in chain notation. */
export function universalDayFull(today: BirthDate): ChainInfo {
  const total =
    digitSum(today.day) + digitSum(today.month) + digitSum(today.year);
  return chainInfo(total, false);
}

// ─── Personal cycles bundle (used by buildProfile + /vibe page) ──────

export type PersonalCycles = {
  py: { raw: number; reduced: number; notation: string };
  pm: { raw: number; reduced: number; notation: string };
  pd: { raw: number; reduced: number; notation: string };
  masterNumbers: number[];
};

/**
 * Hans Decoz personal cycles for the given dob at the given today.
 *
 * - Personal Year & Personal Month: master numbers PRESERVED
 *   (big-picture cycles where master matters).
 * - Personal Day: FULLY reduced to 1-9 — master intermediates are
 *   recorded in the notation/chain (e.g. 29 → 11 → 2), but the
 *   vibration for the day is always single digit.
 */
export function personalCyclesFull(
  dob: BirthDate,
  today: BirthDate,
): PersonalCycles {
  const bm = reduceNumber(dob.month);
  const bd = reduceNumber(dob.day);
  const cy = reduceNumber(digitSum(today.year));

  const pyRaw = bm + bd + cy;
  const py = reduceStopAtMaster(pyRaw);

  const cm = reduceNumber(today.month);
  const pmRaw = py.final + cm;
  const pm = reduceStopAtMaster(pmRaw);

  const pdRaw = pm.final + today.day;
  const pd = reduceFullWithChain(pdRaw);

  const masters = new Set<number>(pd.masters);
  if ([11, 22, 33].includes(py.final)) masters.add(py.final);
  if ([11, 22, 33].includes(pm.final)) masters.add(pm.final);

  return {
    py: { raw: pyRaw, reduced: py.final, notation: py.notation },
    pm: { raw: pmRaw, reduced: pm.final, notation: pm.notation },
    pd: { raw: pdRaw, reduced: pd.final, notation: pd.notation },
    masterNumbers: [...masters].sort((a, b) => a - b),
  };
}
