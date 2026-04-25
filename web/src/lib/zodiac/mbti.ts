// MBTI types — Indonesian personas. Mirrors zodiac.py: MBTI_TYPES.

export const MBTI_TYPES = {
  INTJ: "Si Arsitek — strategis, mandiri, visioner, perfeksionis dalam rencana jangka panjang",
  INTP: "Si Logisi — analitis, pencari kebenaran, kreatif dalam ide, kadang lupa praktikalitas",
  ENTJ: "Si Komandan — pemimpin alami, tegas, ambisius, efisien",
  ENTP: "Si Debater — inovatif, suka tantangan intelektual, cepat berubah pikiran",
  INFJ: "Si Advokat — idealis dalem, empatik, visioner, misi-driven",
  INFP: "Si Mediator — penuh kasih, idealis, kreatif, butuh ruang sendiri",
  ENFJ: "Si Protagonis — karismatik, inspiratif, peduli pertumbuhan orang lain",
  ENFP: "Si Juara — antusias, penuh ide, sosial, butuh kebebasan",
  ISTJ: "Si Logistik — disiplin, bisa diandalkan, setia pada tradisi",
  ISFJ: "Si Pelindung — setia, teliti, nurturing, prioritas harmoni keluarga",
  ESTJ: "Si Eksekutif — organisator, tegas, pekerja keras, to-the-point",
  ESFJ: "Si Konsul — sosial, peduli, suka menolong, butuh validasi",
  ISTP: "Si Virtuoso — praktis, observan, pintar teknis, tenang",
  ISFP: "Si Petualang — artistik, fleksibel, sensitif, hidup di momen",
  ESTP: "Si Pengusaha — energik, spontan, aksi-oriented, suka risiko",
  ESFP: "Si Penghibur — ceria, ekspresif, spontan, pencari kesenangan",
} as const;

export type MbtiType = keyof typeof MBTI_TYPES;

export function isMbtiType(value: string): value is MbtiType {
  return value in MBTI_TYPES;
}
