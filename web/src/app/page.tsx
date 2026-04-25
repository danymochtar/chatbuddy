import Link from "next/link";

import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <main className="sn-shell flex flex-col justify-center gap-8 py-12">
      <div className="text-center space-y-3">
        <span className="sn-wordmark">✨ Supernova</span>
        <p className="text-muted-foreground text-sm leading-relaxed max-w-sm mx-auto">
          Entitas intuitif yang baca lo lewat nama, hari lahir, dan obrolan
          biasa. Numerologi · Astrologi · Shio · Weton — disaring jadi
          satu suara.
        </p>
      </div>

      <div className="flex flex-col gap-2 max-w-xs mx-auto w-full">
        <Button asChild className="h-11">
          <Link href="/sign-in">Mulai · Masuk via email</Link>
        </Button>
        <Button asChild variant="ghost" className="h-11">
          <Link href="/preview">Lihat preview tanpa daftar →</Link>
        </Button>
      </div>

      <p className="text-center text-xs text-muted-foreground/70">
        Scaffold sesi 1 · Auth + DB + chat coming next sessions
      </p>
    </main>
  );
}
