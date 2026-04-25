// Sun sign (Western zodiac). Mirrors zodiac.py: SIGN_TRAITS, sun_sign.

import type { BirthDate } from "@/lib/numerology/core";

export const SIGN_TRAITS: Record<string, string> = {
  Aries: "pelopor, impulsif, berani ambil risiko, energik",
  Taurus: "stabil, sensual, keras kepala, cinta kenyamanan & keindahan",
  Gemini: "komunikatif, ingin tahu, versatil, cepat bosan",
  Cancer: "sensitif, protektif, moody, ikatan keluarga kuat",
  Leo: "karismatik, bangga, generous, butuh pengakuan",
  Virgo: "analitis, perfeksionis, helpful, detail-oriented",
  Libra: "diplomat, estetik, mencari harmoni, kadang indesisif",
  Scorpio: "intens, misterius, pasionat, transformatif",
  Sagittarius: "petualang, filosofis, jujur, cinta kebebasan",
  Capricorn: "disiplin, ambisius, praktis, reserved",
  Aquarius: "independen, humanis, eksentrik, pemikir maju",
  Pisces: "empatik, kreatif, melankolis, intuitif",
};

/**
 * Sun sign by date — uses tropical-zodiac boundary dates. Edge dates
 * pick the later sign (e.g. 21 March → Aries, not Pisces).
 */
export function sunSign(dob: BirthDate): string {
  const boundaries: [number, number, string][] = [
    [1, 1, "Capricorn"],
    [1, 20, "Aquarius"],
    [2, 19, "Pisces"],
    [3, 21, "Aries"],
    [4, 20, "Taurus"],
    [5, 21, "Gemini"],
    [6, 21, "Cancer"],
    [7, 23, "Leo"],
    [8, 23, "Virgo"],
    [9, 23, "Libra"],
    [10, 23, "Scorpio"],
    [11, 22, "Sagittarius"],
    [12, 22, "Capricorn"],
  ];
  let sign = "Capricorn";
  for (const [m, d, s] of boundaries) {
    if (dob.month > m || (dob.month === m && dob.day >= d)) {
      sign = s;
    }
  }
  return sign;
}
