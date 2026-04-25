// Number card — gold mono digit, uppercase eyebrow label, italic
// archetype subtitle. Used on Profil (5 core numbers) and on leaf
// pages like Karakter (same five plus more context).

import { cn } from "@/lib/utils";

type Props = {
  label: string;
  num: number | string;
  archetype?: string;
  className?: string;
};

export function NumberCard({ label, num, archetype, className }: Props) {
  return (
    <div
      className={cn(
        "flex flex-col gap-1 rounded-xl border border-border/60 bg-card px-4 py-3 transition-colors hover:border-primary/60",
        className,
      )}
    >
      <span className="text-[0.66rem] uppercase tracking-[0.12em] text-muted-foreground">
        {label}
      </span>
      <span
        className="font-mono text-2xl text-primary leading-none"
        style={{ textShadow: "0 0 12px rgba(233, 199, 123, 0.25)" }}
      >
        {num}
      </span>
      {archetype ? (
        <span className="text-[0.78rem] italic text-muted-foreground leading-tight">
          {archetype}
        </span>
      ) : null}
    </div>
  );
}

/** Wraps a list of NumberCards in a responsive grid (2 cols on mobile). */
export function NumberCardGrid({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "grid gap-2 grid-cols-2 sm:grid-cols-3",
        className,
      )}
    >
      {children}
    </div>
  );
}
