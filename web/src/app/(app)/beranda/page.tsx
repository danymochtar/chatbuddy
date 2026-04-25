// Beranda placeholder — replaced in Sesi 4 with the real chat UI.

import { auth, signOut } from "@/lib/auth";
import { Button } from "@/components/ui/button";

export const metadata = {
  title: "Beranda · Supernova",
};

async function handleSignOut() {
  "use server";
  await signOut({ redirectTo: "/" });
}

export default async function BerandaPage() {
  const session = await auth();
  return (
    <div className="flex flex-1 flex-col gap-6 py-6">
      <div className="flex items-center justify-between">
        <span className="sn-wordmark">✨ Supernova</span>
      </div>

      <div className="rounded-xl border border-border bg-card p-5 space-y-2">
        <p className="text-xs uppercase tracking-wider text-muted-foreground">
          Signed in as
        </p>
        <p className="font-medium">{session?.user?.email}</p>
      </div>

      <div className="text-sm text-muted-foreground leading-relaxed">
        <p className="mb-2">✓ Sesi 1 — scaffold</p>
        <p className="mb-2">✓ Sesi 2 — auth + DB</p>
        <p className="opacity-60">○ Sesi 3 — port numerology</p>
        <p className="opacity-60">○ Sesi 4 — 5 tab pages</p>
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
