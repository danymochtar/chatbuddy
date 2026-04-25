// Onboarding server action — builds the numerology + zodiac snapshot
// from the user's submitted identity, persists a Profile row, and
// redirects to /beranda. Idempotent: refuses to overwrite an existing
// profile (the form gates that, but we re-check server-side).

"use server";

import { redirect } from "next/navigation";
import { z } from "zod";

import { requireSession } from "@/lib/auth-guards";
import { prisma } from "@/lib/db/prisma";
import { buildProfile, type BirthDate } from "@/lib/numerology";
import { chineseZodiac, sunSign, weton } from "@/lib/zodiac";

const FormSchema = z.object({
  fullName: z
    .string()
    .min(2, "Nama lengkap minimal 2 huruf.")
    .max(120, "Nama lengkap kepanjangan."),
  nickname: z.string().max(40, "Nickname kepanjangan.").optional(),
  dob: z
    .string()
    .regex(/^\d{4}-\d{2}-\d{2}$/, "Format tanggal lahir gak valid."),
  birthTime: z
    .string()
    .regex(/^([01]\d|2[0-3]):[0-5]\d$/, "Format jam lahir HH:MM (24 jam).")
    .optional()
    .or(z.literal("")),
  birthCity: z.string().max(80).optional(),
});

export type OnboardingState = {
  error?: string;
  fieldErrors?: Partial<Record<keyof z.infer<typeof FormSchema>, string>>;
};

function parseDob(iso: string): BirthDate {
  const [y, m, d] = iso.split("-").map(Number);
  return { year: y, month: m, day: d };
}

export async function submitOnboarding(
  _prev: OnboardingState,
  formData: FormData,
): Promise<OnboardingState> {
  const user = await requireSession();

  const parsed = FormSchema.safeParse({
    fullName: formData.get("fullName"),
    nickname: formData.get("nickname") ?? "",
    dob: formData.get("dob"),
    birthTime: formData.get("birthTime") ?? "",
    birthCity: formData.get("birthCity") ?? "",
  });

  if (!parsed.success) {
    const fieldErrors: OnboardingState["fieldErrors"] = {};
    for (const issue of parsed.error.issues) {
      const k = issue.path[0] as keyof z.infer<typeof FormSchema>;
      if (k && !fieldErrors[k]) fieldErrors[k] = issue.message;
    }
    return { fieldErrors };
  }

  const { fullName, nickname, dob, birthTime, birthCity } = parsed.data;
  const dobObj = parseDob(dob);

  // Build the numerology + zodiac snapshots that get stored as JSON
  // on the Profile row. Same math the Streamlit app uses (verified
  // by parity-check.ts in Sesi 3.9).
  const numerology = buildProfile({
    fullName,
    dob: dobObj,
    nickname: nickname || null,
  });
  const zodiac = {
    sun: sunSign(dobObj),
    shio: chineseZodiac(dobObj),
    weton: weton(dobObj),
  };

  // Refuse to clobber an existing profile (defensive — UI also gates).
  const existing = await prisma.profile.findUnique({
    where: { userId: user.id },
    select: { id: true },
  });
  if (existing) {
    redirect("/beranda");
  }

  await prisma.profile.create({
    data: {
      userId: user.id,
      fullName,
      nickname: nickname || null,
      dob: new Date(Date.UTC(dobObj.year, dobObj.month - 1, dobObj.day)),
      birthTime: birthTime || null,
      birthCity: birthCity || null,
      numerology,
      zodiac,
    },
  });

  redirect("/beranda");
}
