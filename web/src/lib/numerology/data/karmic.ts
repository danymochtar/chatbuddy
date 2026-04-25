// Karmic debt + karmic lesson dictionaries. Mirrors numerology.py:
// KARMIC_DEBT_SHORT{,_EN}, LESSON_SHORT{,_EN}, KARMIC_DEBT_MEANINGS,
// LESSON_MEANINGS.

import type { Lang } from "./archetypes";

/** Short labels (sidebar / quick reference). Bilingual. */
export const KARMIC_DEBT_SHORT: Record<Lang, Record<number, string>> = {
  id: {
    13: "disiplin & kerja keras",
    14: "kelola kebebasan",
    16: "lepas ego",
    19: "balance mandiri & empati",
  },
  en: {
    13: "discipline & hard work",
    14: "manage your freedom",
    16: "release the ego",
    19: "balance independence & empathy",
  },
};

export const LESSON_SHORT: Record<Lang, Record<number, string>> = {
  id: {
    1: "berani ambil pimpinan",
    2: "belajar kerjasama",
    3: "ekspresi diri",
    4: "disiplin & struktur",
    5: "adaptif ke perubahan",
    6: "tanggung jawab orang terdekat",
    7: "inner work & refleksi",
    8: "kelola power & uang",
    9: "kasih tanpa pamrih",
  },
  en: {
    1: "dare to take the lead",
    2: "learn to cooperate",
    3: "self-expression",
    4: "discipline & structure",
    5: "adapt to change",
    6: "responsibility for those closest",
    7: "inner work & reflection",
    8: "manage power & money",
    9: "love without strings",
  },
};

/**
 * Long-form karmic-debt narratives (Indonesian primary). The AI
 * translates dynamically when lang=en; data stays single-language
 * until we audit EN tone.
 */
export const KARMIC_DEBT_MEANINGS: Record<number, string> = {
  13: "kerja keras & disiplin berat — gampang ngerasa males atau stuck, tapi harus push terus buat manifest",
  14: "belajar batesin kebebasan & komitmen — bahaya kecanduan / lepas kendali kalau ga dijaga",
  16: "ego & kesombongan bakal diruntuhin — butuh ketenangan, relasi toxic bakal hancur sendiri",
  19: "belajar mandiri tanpa merugikan orang lain — balance independence dan empati",
};

/** Long-form karmic-lesson narratives. */
export const LESSON_MEANINGS: Record<number, string> = {
  1: "belajar berdiri sendiri & ambil pimpinan — kadang terlalu nurut / nunggu orang mulai duluan",
  2: "belajar kerjasama & diplomasi — kadang terlalu egois / ga sabar sama tempo orang lain",
  3: "belajar ekspresi diri & joy — kadang terlalu serius / kaku buat self-expression",
  4: "belajar disiplin & struktur — kadang berantakan, susah fokus ke detail",
  5: "belajar adaptif & embrace change — kadang kaku / takut sama hal baru",
  6: "belajar tanggung jawab pada keluarga & orang lain — kadang cenderung avoidance",
  7: "belajar inner work & kepercayaan — kadang terlalu permukaan, butuh ruang sendiri",
  8: "belajar kelola power & uang — kadang menghindar dari ambisi / urusan material",
  9: "belajar kasih sayang universal — kadang terlalu personal / sulit lepas",
};
