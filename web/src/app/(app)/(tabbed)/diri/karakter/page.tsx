// Karakter leaf — sample of how a leaf page looks. Renders the 5
// core number cards + each number's headline meaning. AI-generated
// narrative ("kompleksitas_prompt" in the Streamlit version) streams
// in here from Anthropic in Sesi 5; the structured data already
// shows up immediately from the persisted profile.

import { BackLink } from "@/components/back-link";
import { NumberCard, NumberCardGrid } from "@/components/number-card";
import { requireProfile } from "@/lib/auth-guards";
import { type NumerologyProfile, data as numerologyData } from "@/lib/numerology";

export const metadata = {
  title: "Karakter · Supernova",
};

export default async function KarakterPage() {
  const { profile } = await requireProfile();
  const num = profile.numerology as unknown as NumerologyProfile;
  const A = numerologyData.ARCHETYPES.id;
  const M = numerologyData.MEANINGS;

  const cards = [
    { label: "Misi Hidup", num: num.lifePath, key: "lifePath" as const },
    { label: "Bakat Bawaan", num: num.expression, key: "expression" as const },
    { label: "Panggilan Hati", num: num.soulUrge, key: "soulUrge" as const },
    { label: "Aura Luar", num: num.personality, key: "personality" as const },
    { label: "Talenta Lahir", num: num.birthday, key: "birthday" as const },
  ];

  return (
    <div className="flex flex-col gap-5 pt-4">
      <BackLink href="/diri" label="Diri" />

      <header className="space-y-1">
        <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">
          Karakter
        </p>
        <h1 className="font-serif text-2xl font-semibold tracking-tight">
          Karakter inti lo
        </h1>
        <p className="text-sm text-muted-foreground">
          Lima angka utama dari nama lengkap & tanggal lahir lo —
          peta singkat siapa lo.
        </p>
      </header>

      <NumberCardGrid>
        {cards.map((c) => (
          <NumberCard
            key={c.key}
            label={c.label}
            num={c.num}
            archetype={A[c.num]}
          />
        ))}
      </NumberCardGrid>

      {/* Number-by-number breakdown */}
      <section className="space-y-4">
        {cards.map((c) => (
          <article key={c.key} className="space-y-1">
            <h2 className="font-serif text-base font-semibold text-primary">
              <span className="font-mono mr-1.5">{c.num}</span>
              {c.label} · <em className="not-italic font-normal text-muted-foreground">{A[c.num]}</em>
            </h2>
            <p className="text-sm text-foreground/85 leading-relaxed">
              {M[c.num] ?? ""}
            </p>
          </article>
        ))}
      </section>

      {/* Placeholder for the AI narrative — wired in Sesi 5. */}
      <section className="rounded-xl border border-dashed border-border/60 bg-card/40 p-4 text-sm text-muted-foreground italic">
        ✨ Narasi mendalam dari Supernova bakal nongol di sini di
        Sesi 5 (begitu /api/chat streaming nya nyala).
      </section>
    </div>
  );
}
