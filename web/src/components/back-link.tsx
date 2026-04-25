import Link from "next/link";
import { ChevronLeft } from "lucide-react";

import { cn } from "@/lib/utils";

type Props = {
  href: string;
  label: string;
  className?: string;
};

/**
 * iOS-Settings-style back link on leaf pages. Pairs with the bottom
 * tab bar's parent-tab highlight so users always see where the back
 * link will take them.
 */
export function BackLink({ href, label, className }: Props) {
  return (
    <Link
      href={href}
      className={cn(
        "inline-flex items-center gap-0.5 text-sm font-medium text-primary hover:text-foreground transition-colors -ml-1",
        className,
      )}
    >
      <ChevronLeft className="size-4" aria-hidden />
      <span>{label}</span>
    </Link>
  );
}
