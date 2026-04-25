// Authed app shell. The proxy.ts redirects unauth users to /sign-in
// before they reach this layout, but we still verify here as a
// defense-in-depth check (proxy could be misconfigured).

import { redirect } from "next/navigation";

import { auth } from "@/lib/auth";

export default async function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();
  if (!session?.user) {
    redirect("/sign-in");
  }

  return <main className="sn-shell flex flex-col min-h-[100dvh]">{children}</main>;
}
