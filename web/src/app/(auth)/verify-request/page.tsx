import Link from "next/link";

import { Button } from "@/components/ui/button";

export const metadata = {
  title: "Cek email · Supernova",
};

export default function VerifyRequestPage() {
  return (
    <div className="space-y-6 text-center">
      <div className="space-y-3">
        <div className="mx-auto inline-flex h-16 w-16 items-center justify-center rounded-full border border-border bg-card text-3xl">
          ✉️
        </div>
        <h1 className="font-serif text-2xl font-semibold tracking-tight">
          Cek inbox lo
        </h1>
        <p className="text-sm text-muted-foreground leading-relaxed max-w-sm mx-auto">
          Magic link udah meluncur. Klik tombol di email buat masuk —
          link-nya berlaku 15 menit dan cuma bisa dipake sekali.
        </p>
      </div>
      <Button asChild variant="ghost" className="h-11">
        <Link href="/sign-in">Pake email lain</Link>
      </Button>
    </div>
  );
}
