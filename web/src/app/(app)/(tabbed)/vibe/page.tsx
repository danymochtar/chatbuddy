// Vibe tab — today's energy reading at the top + 3 alternate-lens
// rows underneath (Zodiak, Shio, Weton). The reading uses persisted
// numerology data + same-day computations; AI-generated narrative
// for each lens lives on its own leaf page (later sessions).

import { TabListRow } from "@/components/tab-list-row";
import { requireProfile } from "@/lib/auth-guards";
import {
  type BirthDate,
  data as numerologyData,
  personalDay,
  todayJakarta,
  universalDay,
} from "@/lib/numerology";
import { currentPasaran } from "@/lib/zodiac";

export const metadata = {
  title: "Vibe · Supernova",
};

/** Prisma stores DOB as a UTC midnight; pull year/month/day in UTC. */
function birthDateFromDob(d: Date): BirthDate {
  return {
    year: d.getUTCFullYear(),
    month: d.getUTCMonth() + 1,
    day: d.getUTCDate(),
  };
}

function formatDateID(d: BirthDate): string {
  const date = new Date(Date.UTC(d.year, d.month - 1, d.day));
  return date.toLocaleDateString("id-ID", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  });
}

export default async function VibePage() {
  const { profile } = await requireProfile();
  const today = todayJakarta();
  const dob = birthDateFromDob(profile.dob);
  const pd = personalDay(dob, today);
  const ud = universalDay(today);
  const pasaran = currentPasaran(today);

  return (
    <div className="flex flex-col gap-5 pt-6">
      <header className="space-y-1">
        <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">
          Vibe
        </p>
        <h1 className="font-serif text-2xl font-semibold tracking-tight">
          Energi hari ini
        </h1>
      </header>

      {/* Today's vibe card */}
      <section
        className="rounded-xl border border-border/60 bg-card p-5 space-y-3"
        aria-label="Personal day reading"
      >
        <p className="text-xs uppercase tracking-wider text-muted-foreground">
          {formatDateID(today)}
        </p>
        <div className="flex items-baseline gap-3">
          <span
            className="font-mono text-4xl text-primary leading-none"
            style={{
              textShadow: "0 0 14px rgba(233, 199, 123, 0.3)",
            }}
          >
            {pd}
          </span>
          <span className="text-sm text-muted-foreground italic">
            Personal Day
          </span>
        </div>
        <p className="text-sm text-foreground/90 leading-relaxed">
          {numerologyData.DAILY_VIBES[pd]}
        </p>
        <div className="flex flex-wrap gap-x-4 gap-y-1 pt-2 border-t border-border/40 text-xs text-muted-foreground">
          <span>
            Universal day:{" "}
            <span className="font-mono text-foreground/80">{ud}</span>
          </span>
          <span>
            Pasaran:{" "}
            <span className="text-foreground/80">{pasaran.name}</span>
          </span>
        </div>
      </section>

      {/* Lens list */}
      <section>
        <p className="text-xs uppercase tracking-[0.14em] text-muted-foreground mb-2 px-1">
          Lensa lain
        </p>
        <div className="flex flex-col gap-2">
          <TabListRow
            href="/vibe/zodiak"
            icon="♈"
            title="Zodiak"
            sub="Sun · Moon · Rising — drama langit lo"
          />
          <TabListRow
            href="/vibe/shio"
            icon="🐉"
            title="Shio"
            sub="Energi tahun lahir versi Cina"
          />
          <TabListRow
            href="/vibe/weton"
            icon="🌿"
            title="Weton"
            sub="Primbon Jawa — neptu hari lahir lo"
          />
        </div>
      </section>
    </div>
  );
}
