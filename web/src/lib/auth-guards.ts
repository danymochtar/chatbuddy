// Auth guards — small server-only helpers that resolve session +
// profile or short-circuit via redirect. Use them at the top of any
// server component that needs a signed-in user or a complete Profile.
//
// Two flavors:
//   requireSession() — proves Auth.js session exists; redirects to
//   /sign-in if not.
//   requireProfile() — proves the user has a populated Profile;
//   redirects to /onboarding if not.
//
// Both are wrapped in React.cache so multiple call sites in the same
// request (e.g. layout + page) hit the DB once.

import { cache } from "react";
import { redirect } from "next/navigation";

import { auth } from "@/lib/auth";
import { prisma } from "@/lib/db/prisma";

export const requireSession = cache(async () => {
  const session = await auth();
  if (!session?.user) {
    redirect("/sign-in");
  }
  return session.user;
});

export const requireProfile = cache(async () => {
  const user = await requireSession();
  const profile = await prisma.profile.findUnique({
    where: { userId: user.id },
  });
  if (!profile) {
    redirect("/onboarding");
  }
  return { user, profile };
});

/**
 * Inverse — used by the onboarding page itself: if the user already
 * has a Profile, kick them to /beranda so they can't create a duplicate.
 */
export const requireNoProfile = cache(async () => {
  const user = await requireSession();
  const profile = await prisma.profile.findUnique({
    where: { userId: user.id },
    select: { id: true },
  });
  if (profile) {
    redirect("/beranda");
  }
  return user;
});
