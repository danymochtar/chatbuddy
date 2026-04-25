// Parity check — compares the TypeScript port output against the
// Python source for a fixed sample input. Run via:
//
//   npm run parity
//
// Shells out to scripts/python-snapshot.py (which imports the Python
// numerology + zodiac modules at /home/user/chatbuddy) for the
// expected values, then runs the TS equivalents and diffs.

import { execFileSync } from "node:child_process";
import path from "node:path";
import { buildProfile } from "../src/lib/numerology";
import { chineseZodiac, sunSign, weton } from "../src/lib/zodiac";

const fullName = "Budi Santoso";
const dob = { year: 1990, month: 5, day: 17 } as const;
const today = { year: 2026, month: 4, day: 25 } as const;

const isoDob = `${dob.year}-${String(dob.month).padStart(2, "0")}-${String(dob.day).padStart(2, "0")}`;
const isoToday = `${today.year}-${String(today.month).padStart(2, "0")}-${String(today.day).padStart(2, "0")}`;

// Resolve the snapshot script relative to the package root — npm run
// always invokes from there, and tsx may run as CJS so import.meta is
// not reliable.
const snapshotPath = path.resolve(process.cwd(), "scripts/python-snapshot.py");
const pyJson = execFileSync(
  "python3",
  [snapshotPath, fullName, isoDob, isoToday],
  { encoding: "utf-8" },
);
const py = JSON.parse(pyJson);

const ts = buildProfile({ fullName, dob, today });
const tsShio = chineseZodiac(dob);
const tsWeton = weton(dob);

type Check = { name: string; expected: unknown; actual: unknown };

const checks: Check[] = [
  { name: "lifePath", expected: py.life_path, actual: ts.lifePath },
  { name: "expression", expected: py.expression, actual: ts.expression },
  { name: "soulUrge", expected: py.soul_urge, actual: ts.soulUrge },
  { name: "personality", expected: py.personality, actual: ts.personality },
  { name: "birthday", expected: py.birthday, actual: ts.birthday },
  { name: "personalYear", expected: py.personal_year, actual: ts.personalYear },
  { name: "personalMonth", expected: py.personal_month, actual: ts.personalMonth },
  { name: "personalDay", expected: py.personal_day, actual: ts.personalDay },
  { name: "maturity", expected: py.maturity, actual: ts.maturity },
  { name: "subconsciousSelf", expected: py.subconscious_self, actual: ts.subconsciousSelf },
  { name: "cornerstone", expected: py.cornerstone, actual: ts.cornerstone },
  { name: "capstone", expected: py.capstone, actual: ts.capstone },
  { name: "firstVowel", expected: py.first_vowel, actual: ts.firstVowel },
  { name: "karmicLessons", expected: py.karmic_lessons, actual: ts.karmicLessons },
  { name: "hiddenPassion", expected: py.hidden_passion, actual: ts.hiddenPassion },
  { name: "planes.dominant", expected: py.planes_dominant, actual: ts.planes.dominant },
  { name: "bridges.lp_ex", expected: py.bridges_lp_ex, actual: ts.bridges.lifePathExpression },
  { name: "bridges.su_pe", expected: py.bridges_su_pe, actual: ts.bridges.soulUrgePersonality },
  { name: "sunSign", expected: py.sun_sign, actual: sunSign(dob) },
  { name: "shio.animal", expected: py.shio_animal, actual: tsShio.animal },
  { name: "shio.element", expected: py.shio_element, actual: tsShio.element },
  { name: "weton.dina", expected: py.weton_dina, actual: tsWeton.dina },
  { name: "weton.pasaran", expected: py.weton_pasaran, actual: tsWeton.pasaran },
  { name: "weton.neptu", expected: py.weton_neptu, actual: tsWeton.neptu },
];

const pad = (s: string, w: number) => s + " ".repeat(Math.max(0, w - s.length));
let pass = 0;
let fail = 0;
for (const { name, expected, actual } of checks) {
  const ok = JSON.stringify(expected) === JSON.stringify(actual);
  const tick = ok ? "[32m✓[0m" : "[31m✗[0m";
  if (ok) {
    console.log(`${tick} ${pad(name, 18)} ${JSON.stringify(actual)}`);
    pass++;
  } else {
    console.log(
      `${tick} ${pad(name, 18)} expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`,
    );
    fail++;
  }
}
console.log(
  `\n${pass}/${checks.length} passed${fail ? ` · ${fail} failed` : ""}`,
);
process.exit(fail > 0 ? 1 : 0);
