"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { cn } from "@/lib/utils";

type Tab = {
  href: string;
  icon: string;
  label: string;
  /** All paths under this prefix highlight the tab. */
  group: string;
};

const TABS: Tab[] = [
  { href: "/beranda", icon: "✨", label: "Beranda", group: "/beranda" },
  { href: "/diri",    icon: "🪞", label: "Diri",    group: "/diri" },
  { href: "/vibe",    icon: "🌟", label: "Vibe",    group: "/vibe" },
  { href: "/tools",   icon: "🧰", label: "Tools",   group: "/tools" },
  { href: "/profil",  icon: "⚙️", label: "Profil",  group: "/profil" },
];

export function BottomTabBar() {
  const pathname = usePathname();
  return (
    <nav
      className="fixed bottom-0 left-0 right-0 z-50 border-t border-border/50 bg-card/85 backdrop-blur-md"
      style={{ paddingBottom: "env(safe-area-inset-bottom)" }}
      aria-label="Navigasi utama"
    >
      <div className="mx-auto flex max-w-[480px] items-stretch">
        {TABS.map((tab) => {
          const active = pathname.startsWith(tab.group);
          return (
            <Link
              key={tab.href}
              href={tab.href}
              className={cn(
                "flex flex-1 flex-col items-center justify-center gap-0.5 py-2 px-1 transition-[color,transform] active:scale-95",
                active
                  ? "text-primary"
                  : "text-muted-foreground hover:text-foreground",
              )}
              aria-current={active ? "page" : undefined}
            >
              <span
                className={cn(
                  "text-xl leading-none",
                  active && "drop-shadow-[0_0_10px_rgba(233,199,123,0.4)]",
                )}
                aria-hidden
              >
                {tab.icon}
              </span>
              <span className="text-[0.66rem] font-medium tracking-wide">
                {tab.label}
              </span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
