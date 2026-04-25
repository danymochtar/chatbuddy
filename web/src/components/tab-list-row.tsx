import Link from "next/link";
import { ChevronRight } from "lucide-react";

import { cn } from "@/lib/utils";

type Props = {
  href: string;
  icon: string;
  title: string;
  sub?: string;
  className?: string;
};

/**
 * iOS-Settings-style tappable row used by the tab landing pages.
 * icon · title + sub · ›. Hover lifts the border to gold.
 */
export function TabListRow({ href, icon, title, sub, className }: Props) {
  return (
    <Link
      href={href}
      className={cn(
        "group flex items-center gap-3 rounded-xl border border-border/60 bg-card px-4 py-3.5 transition-[border-color,transform] hover:border-primary/60 active:scale-[0.99]",
        className,
      )}
    >
      <span className="text-2xl leading-none flex-shrink-0" aria-hidden>
        {icon}
      </span>
      <div className="flex flex-1 flex-col min-w-0">
        <span className="font-medium text-foreground text-[0.95rem] leading-tight">
          {title}
        </span>
        {sub ? (
          <span className="text-xs text-muted-foreground leading-snug mt-0.5">
            {sub}
          </span>
        ) : null}
      </div>
      <ChevronRight
        className="size-4 text-muted-foreground/60 group-hover:text-primary/80 flex-shrink-0"
        aria-hidden
      />
    </Link>
  );
}
