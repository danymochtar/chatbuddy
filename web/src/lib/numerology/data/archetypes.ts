// Archetype labels + headline meanings + cycle themes for each number.
// Mirrors numerology.py: ARCHETYPES{,_EN}, MEANINGS, DAILY_VIBES,
// YEAR_THEMES, MONTH_THEMES. Long-form themes are ID-only (Python) —
// the AI persona handles EN translations dynamically when the user has
// language=en, so the data side stays single-language until we audit
// every translation.

export type Lang = "id" | "en";

/**
 * One-word archetype per number — used in number-card subtitles, sidebar
 * lookups, and "(1) — Pemimpin" inline tags. Bilingual.
 */
export const ARCHETYPES: Record<Lang, Record<number, string>> = {
  id: {
    1: "Pemimpin",
    2: "Pendamai",
    3: "Kreatif",
    4: "Pekerja",
    5: "Petualang",
    6: "Penyayang",
    7: "Pemikir",
    8: "Ambisius",
    9: "Idealis",
    11: "Visioner",
    22: "Pembangun",
    33: "Guru",
  },
  en: {
    1: "Leader",
    2: "Peacemaker",
    3: "Creator",
    4: "Worker",
    5: "Adventurer",
    6: "Nurturer",
    7: "Thinker",
    8: "Achiever",
    9: "Idealist",
    11: "Visionary",
    22: "Builder",
    33: "Teacher",
  },
};

/**
 * One-line headline meanings per number — used in profile summary cards,
 * AI system-prompt context, and meaning lookups in the chat. Indonesian
 * primary; the AI translates dynamically when needed.
 */
export const MEANINGS: Record<number, string> = {
  1: "Pemimpin, independen, ambisius, pionir",
  2: "Diplomat, harmonis, sensitif, kooperatif",
  3: "Kreatif, ekspresif, sosial, optimistis",
  4: "Pekerja keras, stabil, praktis, disiplin",
  5: "Petualang, bebas, dinamis, penuh rasa ingin tahu",
  6: "Penuh kasih, bertanggung jawab, pengasuh, harmonis",
  7: "Analitis, spiritual, introspektif, pencari kebenaran",
  8: "Ambisius, kuat, berorientasi materi dan kekuasaan",
  9: "Humanis, bijaksana, penuh kasih universal, idealis",
  11: "Master number — intuitif tinggi, visioner, inspirator spiritual",
  22: "Master number — master builder, mampu mewujudkan mimpi besar",
  33: "Master number — master teacher, pengabdi kemanusiaan tertinggi",
};

/** Daily-vibe theme for the Personal Day reading. */
export const DAILY_VIBES: Record<number, string> = {
  1: "Hari mulai-mulai baru — inisiatif, langkah pertama, keberanian ambil keputusan",
  2: "Hari kolaborasi & kesabaran — tarik napas, dengerin orang lain, jangan buru-buru",
  3: "Hari ekspresif & kreatif — cocok sosial, berkarya, have fun",
  4: "Hari pekerja keras — fokus bangun fondasi, beresin urusan detail & administratif",
  5: "Hari dinamis — perubahan, adventure, fleksibel, coba hal baru",
  6: "Hari keluarga & tanggung jawab — urus orang terdekat, bikin harmoni",
  7: "Hari introspektif — refleksi, belajar, pelan-pelan dulu, jangan dipaksa",
  8: "Hari kekuatan & pencapaian — momentum buat keputusan besar, urusan uang/bisnis",
  9: "Hari penutupan & pelepasan — selesaiin yang belum beres, let go dari yang udah ga relevan",
  11: "Master day — intuisi tajam banget, inspirasi datang, percaya gut feeling",
  22: "Master day — mewujudkan mimpi besar, action yang berdampak jangka panjang",
  33: "Master day — pengabdian, kasih sayang meluap, momen peduli sesama",
};

/** Personal Year theme (12-month chapter). */
export const YEAR_THEMES: Record<number, string> = {
  1: "Tahun awal baru — fondasi, visi jangka panjang, inisiatif besar",
  2: "Tahun sabar & kolaborasi — hubungan, partnership, perlahan tapi pasti",
  3: "Tahun kreatif — ekspresi diri, jaringan sosial meluas, karya",
  4: "Tahun kerja keras — bangun sistem, fondasi karir/finansial",
  5: "Tahun perubahan — freedom, adventure, banyak shift",
  6: "Tahun tanggung jawab — keluarga, rumah, komitmen",
  7: "Tahun refleksi — spiritual growth, belajar, inner work",
  8: "Tahun power — karir naik level, finansial, achievement",
  9: "Tahun penutupan — akhiri siklus, let go, persiapan siklus baru",
  11: "Master year — awakening spiritual, intuisi jadi kompas",
  22: "Master year — building mimpi raksasa jadi realita",
  33: "Master year — service ke komunitas / misi lebih besar",
};

/** Personal Month theme (intra-year micro chapter). */
export const MONTH_THEMES: Record<number, string> = {
  1: "Bulan inisiatif & awal baru — cocok buat mulai proyek / kebiasaan",
  2: "Bulan sabar & hubungan — perlahan, pertimbangkan feedback orang",
  3: "Bulan ekspresi & sosial — lagi cerah buat berkarya dan networking",
  4: "Bulan disiplin & bangun fondasi — fokus ke sistem & rutinitas",
  5: "Bulan perubahan & fleksibel — siap-siap shift, jangan kaku",
  6: "Bulan rumah & tanggung jawab — fokus ke orang terdekat & komitmen",
  7: "Bulan refleksi & belajar — tarik diri, deep thinking, studi",
  8: "Bulan power & pencapaian — momen ambil keputusan besar, uang/karir",
  9: "Bulan penutupan — selesaiin yang pending, release yang ga relevan",
  11: "Master month — intuisi kuat, bisa jadi inspirasi buat orang",
  22: "Master month — action skala besar, building jangka panjang",
  33: "Master month — service, pengabdian, care buat komunitas",
};
