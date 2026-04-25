// Weton (Javanese 5-day-week × 7-day-week reading). Mirrors zodiac.py:
// DINA, DINA_NEPTU, PASARAN, PASARAN_NEPTU, DINA_TRAITS, PASARAN_TRAITS,
// NEPTU_RANGE_MEANINGS, weton, current_pasaran.

import { type BirthDate, daysBetween, pyWeekday } from "@/lib/numerology/core";

export const DINA = [
  "Senin",
  "Selasa",
  "Rabu",
  "Kamis",
  "Jumat",
  "Sabtu",
  "Minggu",
] as const;
export type Dina = (typeof DINA)[number];

const DINA_NEPTU: Record<Dina, number> = {
  Minggu: 5,
  Senin: 4,
  Selasa: 3,
  Rabu: 7,
  Kamis: 8,
  Jumat: 6,
  Sabtu: 9,
};

export const DINA_TRAITS: Record<Dina, string> = {
  Senin: "lembut, tenang, sabar, mudah bergaul",
  Selasa: "penuh semangat, tegas, ambisius",
  Rabu: "pandai komunikasi, analitis, cepat tanggap",
  Kamis: "bijaksana, dewasa, berjiwa pemimpin",
  Jumat: "sabar, penuh kasih, spiritual",
  Sabtu: "mandiri, pekerja keras, disiplin",
  Minggu: "kreatif, optimis, ceria",
};

export const PASARAN = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"] as const;
export type Pasaran = (typeof PASARAN)[number];

const PASARAN_NEPTU: Record<Pasaran, number> = {
  Legi: 5,
  Pahing: 9,
  Pon: 7,
  Wage: 4,
  Kliwon: 8,
};

export const PASARAN_TRAITS: Record<Pasaran, string> = {
  Legi: "manis, lembut, disukai banyak orang",
  Pahing: "tegas, keras kemauan, pantang menyerah",
  Pon: "cerdas, banyak bicara, mudah bergaul",
  Wage: "sederhana, jujur, kerja keras",
  Kliwon: "misterius, kuat spiritual, penuh intuisi",
};

export type NeptuRange = "rendah" | "sedang" | "tinggi" | "sangat_tinggi";

export const NEPTU_RANGE_MEANINGS: Record<NeptuRange, string> = {
  rendah: "karakter lembut & sabar (neptu 7-11)",
  sedang: "karakter seimbang, fleksibel (neptu 12-14)",
  tinggi: "karakter kuat, berkarisma (neptu 15-17)",
  sangat_tinggi: "karakter dominan, ambisius (neptu 18+)",
};

/** Reference: 17 May 1995 = Rabu Legi (Legi = pasaran index 0). */
const PASARAN_REFERENCE: BirthDate = { year: 1995, month: 5, day: 17 };

export type Weton = {
  dina: Dina;
  pasaran: Pasaran;
  weton: string; // "Rabu Legi"
  neptu: number;
  neptuRange: NeptuRange;
  dinaTraits: string;
  pasaranTraits: string;
  neptuMeaning: string;
};

export function weton(dob: BirthDate): Weton {
  const days = daysBetween(PASARAN_REFERENCE, dob);
  // ((d % 5) + 5) % 5 normalizes negative diffs.
  const pasaranIdx = ((days % 5) + 5) % 5;
  const pasaranName = PASARAN[pasaranIdx];
  const dinaName = DINA[pyWeekday(dob)];
  const neptu = DINA_NEPTU[dinaName] + PASARAN_NEPTU[pasaranName];
  const range: NeptuRange =
    neptu <= 11
      ? "rendah"
      : neptu <= 14
        ? "sedang"
        : neptu <= 17
          ? "tinggi"
          : "sangat_tinggi";
  return {
    dina: dinaName,
    pasaran: pasaranName,
    weton: `${dinaName} ${pasaranName}`,
    neptu,
    neptuRange: range,
    dinaTraits: DINA_TRAITS[dinaName],
    pasaranTraits: PASARAN_TRAITS[pasaranName],
    neptuMeaning: NEPTU_RANGE_MEANINGS[range],
  };
}

/** Today's pasaran — used for the Vibe page's "today" reading. */
export function currentPasaran(today: BirthDate): {
  name: Pasaran;
  traits: string;
} {
  const days = daysBetween(PASARAN_REFERENCE, today);
  const idx = ((days % 5) + 5) % 5;
  const name = PASARAN[idx];
  return { name, traits: PASARAN_TRAITS[name] };
}
