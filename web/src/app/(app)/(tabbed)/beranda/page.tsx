// Beranda — chat shell (placeholder until Sesi 5 wires the streaming).
// Gates behind requireProfile() so users without a Profile get sent to
// /onboarding before they reach the chat.

import { signOut } from "@/lib/auth";
import { requireProfile } from "@/lib/auth-guards";
import { Button } from "@/components/ui/button";

export const metadata = {
  title: "Beranda · Supernova",
};

async function handleSignOut() {
  "use server";
  await signOut({ redirectTo: "/" });
}

export default async function BerandaPage() {
  const { profile } = await requireProfile();
  return (
    <div className="flex flex-1 flex-col gap-6 py-6">
      <div className="flex items-center justify-between">
        <span className="sn-wordmark">✨ Supernova</span>
      </div>

      <div className="rounded-xl border border-border bg-card p-5 space-y-2">
        <p className="text-xs uppercase tracking-wider text-muted-foreground">
          Hi
        </p>
        <p className="font-medium text-lg">
          {profile.nickname ?? profile.fullName.split(" ")[0]}
        </p>
        <p className="text-xs text-muted-foreground">
          {profile.fullName} · lahir {profile.dob.toISOString().slice(0, 10)}
        </p>
      </div>

      <div className="text-sm text-muted-foreground leading-relaxed">
        <p className="mb-2">✓ Sesi 1 — scaffold</p>
        <p className="mb-2">✓ Sesi 2 — auth + DB</p>
        <p className="mb-2">✓ Sesi 3 — port numerology</p>
        <p className="mb-2">✓ Sesi 4.1 — onboarding</p>
        <p className="opacity-60">○ Sesi 4.2-4.7 — tab pages</p>
        <p className="opacity-60">○ Sesi 5 — chat streaming</p>
        <p className="opacity-60">○ Sesi 6 — PWA + deploy</p>
      </div>

      <form action={handleSignOut} className="mt-auto">
        <Button type="submit" variant="ghost" className="w-full h-11">
          Keluar
        </Button>
      </form>
    </div>
  );
}
