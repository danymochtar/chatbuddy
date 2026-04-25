// buildProfile — orchestrator that mirrors numerology.py:build_profile.
// Stitches the math + data layers into a single snapshot suitable for
// persistence (Profile.numerology JSON column), Anthropic system prompt
// context, and the UI's number cards / pages.

import {
  type BirthDate,
  type ChainInfo,
  ageYears,
  chainInfo,
  reduceToSingle,
  todayJakarta,
} from "./core";
import {
  type LifePathInfo,
  birthdayFull,
  expressionFull,
  lifePathFull,
  maturityNumber,
  personalityFull,
  rationalThoughtFull,
  soulUrgeFull,
} from "./numbers";
import {
  personalCyclesFull,
  personalDay,
  personalMonth,
  personalYear,
  universalDayFull,
} from "./cycles";
import {
  bridge,
  capstone,
  cornerstone,
  expressionKarmic,
  firstVowel,
  hiddenPassion,
  karmicLessons,
  lifePathKarmic,
  personalityKarmic,
  planesOfExpression,
  soulUrgeKarmic,
  subconsciousSelf,
  type PlanesOfExpression,
} from "./extras";
import {
  type CurrentPeriodCycle,
  type CurrentPinnacleChallenge,
  type Essence,
  type Pinnacle,
  type Transits,
  challenges,
  currentPeriodCycle,
  currentPinnacleChallenge,
  essence,
  pinnacles,
  transits,
} from "./forecast";
import {
  DAILY_VIBES,
  MEANINGS,
  MONTH_THEMES,
  YEAR_THEMES,
} from "./data/archetypes";

// ─── Public type ──────────────────────────────────────────────────────

export type MaturityPhase = "latent" | "emerging" | "active";

export type NumerologyProfile = {
  fullName: string;
  nickname: string;
  dob: string; // ISO YYYY-MM-DD
  today: string; // ISO

  // Core numbers (master-preserved per Decoz)
  lifePath: number;
  expression: number;
  soulUrge: number;
  personality: number;
  birthday: number;

  // Cycles
  personalYear: number;
  personalMonth: number;
  personalDay: number;

  // Karmic + supporting
  karmicDebts: {
    lifePath: number | null;
    expression: number | null;
    soulUrge: number | null;
    personality: number | null;
  };
  karmicLessons: number[];
  hiddenPassion: number[];
  maturity: number;
  rationalThought: number;
  pinnacles: Pinnacle[];
  challenges: Pinnacle[];
  currentPhase: CurrentPinnacleChallenge;

  // Decoz extras
  age: number;
  maturityPhase: MaturityPhase;
  subconsciousSelf: number;
  cornerstone: string;
  capstone: string;
  firstVowel: string;
  planes: PlanesOfExpression;
  bridges: {
    lifePathExpression: number;
    soulUrgePersonality: number;
  };
  transits: Transits;
  essence: Essence;
  periodNow: CurrentPeriodCycle;

  // Rich chain_info dicts (notation, components, masters, karmic intermediates)
  info: {
    lifePath: LifePathInfo;
    expression: ReturnType<typeof expressionFull>;
    soulUrge: ReturnType<typeof soulUrgeFull>;
    personality: ReturnType<typeof personalityFull>;
    birthday: ChainInfo;
    rationalThought: ChainInfo;
    universalDayToday: ChainInfo;
  };

  meanings: {
    lifePath: string;
    expression: string;
    soulUrge: string;
    personality: string;
    birthday: string;
    personalYear: string;
    personalMonth: string;
    personalDay: string;
    maturity: string;
    rationalThought: string;
  };
};

// ─── Build ───────────────────────────────────────────────────────────

const ISO_DATE = (d: BirthDate) =>
  `${d.year.toString().padStart(4, "0")}-` +
  `${d.month.toString().padStart(2, "0")}-` +
  `${d.day.toString().padStart(2, "0")}`;

function pickMeaning(n: number): string {
  return MEANINGS[n] ?? MEANINGS[reduceToSingle(n)] ?? "";
}

export function buildProfile(args: {
  fullName: string;
  dob: BirthDate;
  today?: BirthDate;
  nickname?: string | null;
}): NumerologyProfile {
  const { fullName } = args;
  const today = args.today ?? todayJakarta();
  const { dob } = args;

  let lpInfo = lifePathFull(dob);
  const exInfo = expressionFull(fullName);
  const suInfo = soulUrgeFull(fullName);
  const peInfo = personalityFull(fullName);
  const bdInfo = birthdayFull(dob);
  const rtInfo = rationalThoughtFull(fullName, dob);
  const udInfo = universalDayFull(today);

  // Decoz Master 33 rule: Life Path 33 only counts as master if at
  // least one other master (11/22/33) appears elsewhere in the core
  // chart. Otherwise demote to 6.
  if (lpInfo.final === 33) {
    const otherMasters: number[] = [];
    for (const info of [exInfo, suInfo, peInfo, bdInfo]) {
      otherMasters.push(...info.masters);
    }
    if (otherMasters.length === 0) {
      const demoted = chainInfo(lpInfo.raw, false);
      lpInfo = {
        ...demoted,
        components: lpInfo.components,
        demotedFrom33: true,
      };
    }
  }

  const lp = lpInfo.final;
  const ex = exInfo.final;
  const su = suInfo.final;
  const pe = peInfo.final;
  const bd = bdInfo.final;
  const rational = rtInfo.final;

  const py = personalYear(dob, today);
  const pm = personalMonth(dob, today);
  const pd = personalDay(dob, today);

  const debts = {
    lifePath: lifePathKarmic(dob),
    expression: expressionKarmic(fullName),
    soulUrge: soulUrgeKarmic(fullName),
    personality: personalityKarmic(fullName),
  };
  const lessons = karmicLessons(fullName);
  const passion = hiddenPassion(fullName);
  const maturity = maturityNumber(lp, ex);
  const pins = pinnacles(dob);
  const chals = challenges(dob);
  const current = currentPinnacleChallenge(dob, today);

  // Decoz Maturity activation: late 30s emerging, ~50+ active.
  const age = ageYears(dob, today);
  const maturityPhase: MaturityPhase =
    age >= 50 ? "active" : age >= 35 ? "emerging" : "latent";

  const planes = planesOfExpression(fullName);
  const cs = cornerstone(fullName);
  const cap = capstone(fullName);
  const fv = firstVowel(fullName);
  const sub = subconsciousSelf(fullName);
  const bridges = {
    lifePathExpression: bridge(lp, ex),
    soulUrgePersonality: bridge(su, pe),
  };
  const transitData = transits(fullName, dob, today);
  const essenceData = essence(fullName, dob, today);
  const periodNow = currentPeriodCycle(dob, today);

  const nick =
    (args.nickname ?? "").trim() || fullName.trim().split(/\s+/)[0];

  return {
    fullName,
    nickname: nick,
    dob: ISO_DATE(dob),
    today: ISO_DATE(today),
    lifePath: lp,
    expression: ex,
    soulUrge: su,
    personality: pe,
    birthday: bd,
    personalYear: py,
    personalMonth: pm,
    personalDay: pd,
    karmicDebts: debts,
    karmicLessons: lessons,
    hiddenPassion: passion,
    maturity,
    rationalThought: rational,
    pinnacles: [...pins],
    challenges: [...chals],
    currentPhase: current,
    age,
    maturityPhase,
    subconsciousSelf: sub,
    cornerstone: cs,
    capstone: cap,
    firstVowel: fv,
    planes,
    bridges,
    transits: transitData,
    essence: essenceData,
    periodNow,
    info: {
      lifePath: lpInfo,
      expression: exInfo,
      soulUrge: suInfo,
      personality: peInfo,
      birthday: bdInfo,
      rationalThought: rtInfo,
      universalDayToday: udInfo,
    },
    meanings: {
      lifePath: pickMeaning(lp),
      expression: pickMeaning(ex),
      soulUrge: pickMeaning(su),
      personality: pickMeaning(pe),
      birthday: pickMeaning(bd),
      personalYear: YEAR_THEMES[py] ?? "",
      personalMonth: MONTH_THEMES[pm] ?? "",
      personalDay: DAILY_VIBES[pd] ?? "",
      maturity: pickMeaning(maturity),
      rationalThought: pickMeaning(rational),
    },
  };
}
