// Chinese zodiac (Shio). Mirrors zodiac.py: SHIO_ANIMALS, SHIO_TRAITS,
// ELEMENT_CYCLE, ELEMENT_TRAITS, chinese_zodiac.

import type { BirthDate } from "@/lib/numerology/core";

const SHIO_ANIMALS = [
  "Tikus",
  "Kerbau",
  "Macan",
  "Kelinci",
  "Naga",
  "Ular",
  "Kuda",
  "Kambing",
  "Monyet",
  "Ayam",
  "Anjing",
  "Babi",
] as const;

export type ShioAnimal = (typeof SHIO_ANIMALS)[number];

export const SHIO_TRAITS: Record<ShioAnimal, string> = {
  Tikus: "cerdas, cepat, oportunis, sosial",
  Kerbau: "sabar, pekerja keras, bisa diandalkan, keras kepala",
  Macan: "pemberani, pemimpin alami, kompetitif, rebellious",
  Kelinci: "lembut, diplomatis, peka, butuh harmoni",
  Naga: "karismatik, ambisius, penuh energi, dominan",
  Ular: "bijak, intuitif, tenang, misterius",
  Kuda: "bebas, energik, pencinta petualangan, impulsif",
  Kambing: "artistik, empatik, sensitif, kadang ragu-ragu",
  Monyet: "cerdik, inovatif, kreatif, gemar bersosialisasi",
  Ayam: "teratur, jujur, detail, bangga akan penampilan",
  Anjing: "loyal, protektif, jujur, kadang cemas",
  Babi: "tulus, murah hati, cinta kenyamanan, naif",
};

export type ShioElement = "Logam" | "Air" | "Kayu" | "Api" | "Tanah";

const ELEMENT_CYCLE: Record<number, ShioElement> = {
  0: "Logam",
  1: "Logam",
  2: "Air",
  3: "Air",
  4: "Kayu",
  5: "Kayu",
  6: "Api",
  7: "Api",
  8: "Tanah",
  9: "Tanah",
};

export const ELEMENT_TRAITS: Record<ShioElement, string> = {
  Logam: "disiplin, tegas, fokus pada pencapaian",
  Air: "adaptif, intuitif, mengalir dengan situasi",
  Kayu: "tumbuh, idealis, mencari ekspresi",
  Api: "pasionat, kreatif, berani mengambil risiko",
  Tanah: "stabil, praktis, bisa dipercaya",
};

export type ChineseZodiac = {
  animal: ShioAnimal;
  element: ShioElement;
  animalTraits: string;
  elementTraits: string;
  label: string; // e.g. "Air Tikus"
};

/**
 * Chinese zodiac for a birth date. Note: people born in January or
 * before Feb 5 fall under the previous Chinese New Year — we use a
 * fixed Feb-5 boundary for simplicity (close enough for the audience
 * and matches the Python reference).
 */
export function chineseZodiac(dob: BirthDate): ChineseZodiac {
  let year = dob.year;
  if (dob.month === 1 || (dob.month === 2 && dob.day < 5)) {
    year -= 1;
  }
  const animalIdx = ((year - 1900) % 12 + 12) % 12;
  const animal = SHIO_ANIMALS[animalIdx];
  const element = ELEMENT_CYCLE[((year % 10) + 10) % 10];
  return {
    animal,
    element,
    animalTraits: SHIO_TRAITS[animal],
    elementTraits: ELEMENT_TRAITS[element],
    label: `${element} ${animal}`,
  };
}
