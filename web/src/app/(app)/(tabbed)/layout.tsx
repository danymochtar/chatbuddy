// Tabbed layout — wraps the 5-tab pages (Beranda / Diri / Vibe /
// Tools / Profil) with the fixed BottomTabBar. Sits inside the (app)
// auth-gate so users without a session never reach this layer; the
// requireProfile() call also redirects users without a Profile to
// /onboarding.

import { BottomTabBar } from "@/components/bottom-tab-bar";
import { requireProfile } from "@/lib/auth-guards";

export default async function TabbedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  await requireProfile();
  return (
    <>
      {/* pb-20 (≈ tab bar height) so content never sits underneath the bar */}
      <div className="flex-1 pb-20">{children}</div>
      <BottomTabBar />
    </>
  );
}
