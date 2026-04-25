// Decoz Planes of Expression + Bridge Numbers + Subconscious Self.
// Mirrors numerology.py: PLANE_LETTERS, PLANE_MEANINGS{,_EN},
// PLANE_LABEL_EN, BRIDGE_MEANINGS, SUBCONSCIOUS_SELF_MEANINGS.

import type { Lang } from "./archetypes";

export type Plane = "physical" | "mental" | "emotional" | "intuitive";

/** Which letters belong to which plane. Each plane gets a Set for O(1) lookup. */
export const PLANE_LETTERS: Record<Plane, Set<string>> = {
  physical: new Set("EMW"),
  mental: new Set("AHJNPGL"),
  emotional: new Set("BIORSTXZ"),
  intuitive: new Set("CDFKQUVY"),
};

/** Bilingual plane label (capitalised) — used in Indonesian as well as EN. */
export const PLANE_LABEL: Record<Lang, Record<Plane, string>> = {
  id: {
    physical: "fisik",
    mental: "mental",
    emotional: "emosional",
    intuitive: "intuitif",
  },
  en: {
    physical: "physical",
    mental: "mental",
    emotional: "emotional",
    intuitive: "intuitive",
  },
};

export const PLANE_MEANINGS: Record<Lang, Record<Plane, string>> = {
  id: {
    physical:
      "Plane fisik kuat — praktis, durable, sensual, grounded, hands-on. Lo bekerja paling baik dengan tubuh & dunia material.",
    mental:
      "Plane mental kuat — logis, analitis, fact-driven, sering jadi leader pemikir.",
    emotional:
      "Plane emosional kuat — imajinatif, sentimental, artistik, simpatik. Reaksi pertama lo lewat hati.",
    intuitive:
      "Plane intuitif kuat (jarang dominan) — spiritual, visioner, sensitif terhadap halus & spiritual.",
  },
  en: {
    physical:
      "Strong physical plane — practical, durable, sensual, grounded, hands-on. You do your best work through the body & material world.",
    mental:
      "Strong mental plane — logical, analytical, fact-driven, often a thought leader.",
    emotional:
      "Strong emotional plane — imaginative, sentimental, artistic, sympathetic. Your first reaction is through the heart.",
    intuitive:
      "Strong intuitive plane (rarely dominant) — spiritual, visionary, sensitive to the subtle & sacred.",
  },
};

/** Bridge number narrative (0-8) — Indonesian primary. */
export const BRIDGE_MEANINGS: Record<number, string> = {
  0: "Dua angka identik — energinya nyatu, ekspresi tunggal yang kuat. Risk: terlalu monoton, miss balance.",
  1: "Develop independence, decisiveness, self-reliance. Berani jadi diri sendiri, ga tergantung suara orang.",
  2: "Practice patience, cooperation, sensitivity ke tempo orang lain. Belajar lebih lembut, less direct.",
  3: "Tambahin kreativitas, humor, self-expression — biar dua sisi lo sambungin lewat ekspresi.",
  4: "Tambahin disiplin, struktur, follow-through — biar visi punya kaki dan ground.",
  5: "Lebih fleksibel, willing to change, less afraid of risk — buat sambungin gap.",
  6: "Take on more responsibility — terutama buat keluarga / komunitas. Tanggung jawab nyambungin gap.",
  7: "Spend more time in study, contemplation, self-reflection. Inner work bridges the gap.",
  8: "Work on relationship sama power, money, accomplishment. Material maturity bridges the gap.",
};

/** Subconscious Self range 3-9 (9 minus karmic-lesson count). */
export const SUBCONSCIOUS_SELF_MEANINGS: Record<number, string> = {
  3: "Karakter belum lengkap — banyak situasi yang masih bikin lo bingung. Rentan panik di hal baru, tapi cepet adaptasi kalau udah dilatih.",
  4: "Beberapa area diri lo masih rapuh. Saat di luar zona nyaman, perlu waktu buat kalibrasi. Tapi sekali ngerti, lo solid.",
  5: "Mid-range — ada gap kepercayaan diri di beberapa situasi. Lo bisa pas-pasan sampai bagus, tergantung konteks.",
  6: "Lumayan tools-mu lengkap. Kebanyakan situasi bisa lo handle, tapi jangan over-confident karena masih ada blind spot.",
  7: "Cukup confident dalam banyak situasi — kalau ada yang surprise, biasanya lo cepet recover dan find footing.",
  8: "Hampir semua tools ada. Confident, jarang panik, bisa improvise di hampir semua situasi sosial / emosional.",
  9: "Semua angka 1-9 hadir di nama lo — confident penuh. Awas: bisa tergelincir ke aloof / over-confident di situasi yang sebenernya butuh humility.",
};
