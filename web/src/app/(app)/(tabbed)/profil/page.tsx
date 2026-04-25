// Profil tab — avatar + core numbers + account + sign out. The
// number values come from the persisted profile.numerology JSON
// (computed at onboarding time by buildProfile()).

import { Button } from "@/components/ui/button";
import { NumberCard, NumberCardGrid } from "@/components/number-card";
import { signOut } from "@/lib/auth";
import { requireProfile } from "@/lib/auth-guards";
import { type NumerologyProfile, data as numerologyData } from "@/lib/numerology";

export const metadata = {
  title: "Profil · Supernova",
};

async function handleSignOut() {
  "use server";
  await signOut({ redirectTo: "/" });
}

function formatDob(d: Date): string {
  return d.toLocaleDateString("id-ID", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  });
}

export default async function ProfilPage() {
  const { user, profile } = await requireProfile();
  const num = profile.numerology as unknown as NumerologyProfile;
  const initial = (profile.nickname || profile.fullName)
    .trim()
    .slice(0, 1)
    .toUpperCase();
  const A = numerologyData.ARCHETYPES.id;

  return (
    <div className="flex flex-1 flex-col gap-5 pt-6">
      <header className="space-y-1">
        <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">
          Profil
        </p>
        <h1 className="font-serif text-2xl font-semibold tracking-tight">
          Tentang lo
        </h1>
      </header>

      {/* Avatar row */}
      <section
        className="flex items-center gap-3 rounded-xl border border-border/60 bg-card px-4 py-3.5"
        aria-label="Identitas"
      >
        <div
          className="size-12 flex-shrink-0 rounded-full border-[1.5px] border-primary/60 bg-secondary flex items-center justify-center font-serif font-semibold text-primary text-xl"
          style={{ textShadow: "0 0 12px rgba(233, 199, 123, 0.3)" }}
          aria-hidden
        >
          {initial}
        </div>
        <div className="flex flex-col min-w-0">
          <span className="font-medium leading-tight">
            👋 {profile.nickname ?? profile.fullName.split(" ")[0]}
          </span>
          <span className="text-xs text-muted-foreground leading-tight mt-0.5">
            {profile.fullName} · lahir {formatDob(profile.dob)}
          </span>
        </div>
      </section>

      {/* Core numbers */}
      <section>
        <p className="text-xs uppercase tracking-[0.14em] text-muted-foreground mb-2 px-1">
          Angka inti
        </p>
        <NumberCardGrid>
          <NumberCard label="Misi Hidup" num={num.lifePath} archetype={A[num.lifePath]} />
          <NumberCard label="Bakat Bawaan" num={num.expression} archetype={A[num.expression]} />
          <NumberCard label="Panggilan Hati" num={num.soulUrge} archetype={A[num.soulUrge]} />
          <NumberCard label="Aura Luar" num={num.personality} archetype={A[num.personality]} />
          <NumberCard label="Talenta Lahir" num={num.birthday} archetype={A[num.birthday]} />
        </NumberCardGrid>
      </section>

      {/* Account */}
      <section className="rounded-xl border border-border/60 bg-card p-4 space-y-1">
        <p className="text-xs uppercase tracking-wider text-muted-foreground">
          Akun
        </p>
        <p className="text-sm break-all">{user.email}</p>
      </section>

      {/* Sign out */}
      <form action={handleSignOut} className="mt-auto pt-4">
        <Button
          type="submit"
          variant="ghost"
          className="w-full h-11 text-muted-foreground hover:text-destructive"
        >
          Keluar
        </Button>
      </form>
    </div>
  );
}
