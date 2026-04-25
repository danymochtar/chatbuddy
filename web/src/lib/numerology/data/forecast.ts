// Forecast / cycle narratives — Period Cycle, Pinnacle, Challenge,
// Transit Layer, Essence. Mirrors numerology.py:
// PERIOD_CYCLE_MEANINGS, PINNACLE_MEANINGS, CHALLENGE_MEANINGS,
// TRANSIT_LAYER_MEANINGS, ESSENCE_MEANINGS.

import type { Plane } from "./planes";

/** Period Cycle (one of three big chapters of the Life Path). */
export const PERIOD_CYCLE_MEANINGS: Record<number, string> = {
  1: "Babak inisiatif & jadi diri sendiri — fondasi self-direction.",
  2: "Babak hubungan & sensitivity — belajar diplomasi & cooperation.",
  3: "Babak ekspresi & sosial — kreativitas, comunication, joy of being seen.",
  4: "Babak kerja keras & fondasi material — disiplin, building, security.",
  5: "Babak perubahan & freedom — adventure, eksplorasi, banyak shift.",
  6: "Babak tanggung jawab & care — keluarga, komitmen, healing orang.",
  7: "Babak introspektif & wisdom — solo work, study, spiritual.",
  8: "Babak power & material achievement — karir, pengaruh, autoritas.",
  9: "Babak humanis & legacy — service, completion, lepas dari ego personal.",
  11: "Babak master 11 — channeling intuisi, jadi inspirator.",
  22: "Babak master 22 — building skala besar, monumen yg lasting.",
  33: "Babak master 33 — service universal, kasih tanpa syarat.",
};

/** Pinnacle (1 of 4 quarters). Master numbers possible. */
export const PINNACLE_MEANINGS: Record<number, string> = {
  1: "fase kepemimpinan & inisiatif — saat jadi diri sendiri, berani ambil risiko",
  2: "fase sabar & bangun hubungan — diplomasi, kerja dengan orang lain",
  3: "fase ekspresi & kreativitas — karya, sosial, joy",
  4: "fase kerja keras & fondasi — bangun sistem, disiplin, stabilitas",
  5: "fase perubahan & kebebasan — adventure, eksplor hal baru",
  6: "fase tanggung jawab & keluarga — komitmen, nurture orang terdekat",
  7: "fase introspektif & spiritual — refleksi, cari wisdom, inner work",
  8: "fase power & pencapaian — karir, finansial, legacy",
  9: "fase penutupan & humanis — legacy, service, letting go",
  11: "master pinnacle — awakening, jadi inspirator",
  22: "master pinnacle — building impact jangka panjang",
  33: "master pinnacle — service ke komunitas besar",
};

/**
 * Challenge (1 of 4, paired with Pinnacles). Range 0-8 — challenge
 * 0 means "universal challenge / from inside yourself".
 */
export const CHALLENGE_MEANINGS: Record<number, string> = {
  0: "tantangan universal — dari dalem diri sendiri, eksplorasi karakter bebas",
  1: "tantangan assertiveness — belajar stand up buat diri sendiri tanpa ego",
  2: "tantangan kesabaran & kerja sama — kelola sensitivity, ga over-people-pleasing",
  3: "tantangan ekspresi — kelola mood swing, jangan kebawa emosi",
  4: "tantangan disiplin & detail — kelola rasa stuck / kewalahan sama rutinitas",
  5: "tantangan kebebasan — jangan lari dari komitmen atau kecanduan sensasi",
  6: "tantangan responsibility — balance antara ngurus orang & diri sendiri",
  7: "tantangan kepercayaan — jangan isolate diri, belajar open-up ke orang",
  8: "tantangan power & uang — belajar equitable dengan uang & autoritas",
};

/** Transit layer label — physical / mental / spiritual (NOT 'intuitive'). */
export type TransitLayer = "physical" | "mental" | "spiritual";

export const TRANSIT_LAYER_MEANINGS: Record<TransitLayer, string> = {
  physical:
    "Lapisan fisik & dunia material — kerjaan, kesehatan, hubungan eksternal, hal-hal kasat mata.",
  mental:
    "Lapisan mental & emosional — pola pikir, perasaan, dinamika internal di balik tindakan.",
  spiritual:
    "Lapisan spiritual & jangka panjang — arah hidup, makna, growth lewat satu chapter penuh.",
};

/** Note: transit layers (physical/mental/spiritual) are different from
 *  Plane of Expression layers (which include 'intuitive', 'emotional').
 *  Re-export the Plane type for callers that need both. */
export type { Plane };

/** Essence Cycle — one-year sum from active transit letters. */
export const ESSENCE_MEANINGS: Record<number, string> = {
  1: "Tahun esensi 1 — momentum bikin lo lebih mandiri & inisiatif. Bisa muncul dorongan mulai sesuatu sendiri.",
  2: "Tahun esensi 2 — fokus ke hubungan & kerja sama. Pelajaran soal sabar & sensitivity ke orang.",
  3: "Tahun esensi 3 — ekspresi & kreatif lagi naik. Sosial, karya, bisa rame ide & emosi.",
  4: "Tahun esensi 4 — kerja keras & disiplin. Bangun fondasi, rapi-rapiin sistem, hasil dari kerja konsisten.",
  5: "Tahun esensi 5 — perubahan, freedom, banyak shift. Bisa pindah, ganti pekerjaan, hubungan baru.",
  6: "Tahun esensi 6 — rumah, keluarga, tanggung jawab. Komitmen lebih mendalam, ngurus orang.",
  7: "Tahun esensi 7 — refleksi, study, spiritual. Pelan-pelan, tarik diri, deep work.",
  8: "Tahun esensi 8 — power, materi, achievement. Karir bisa naik level, urusan finansial signifikan.",
  9: "Tahun esensi 9 — penutupan & lepas. Mengakhiri chapter, persiapan siklus baru.",
  11: "Tahun esensi 11 (master) — intuisi tajam, momen awakening, jadi inspirator.",
  22: "Tahun esensi 22 (master) — building skala besar, dampak jangka panjang.",
  33: "Tahun esensi 33 (master) — service, devotion, kasih meluap ke komunitas.",
};
