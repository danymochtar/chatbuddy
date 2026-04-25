// Augment NextAuth's Session.user so server components can read
// `session.user.id` as a string, matching the shape produced by the
// session callback in src/lib/auth.ts.

import "next-auth";

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      email?: string | null;
      name?: string | null;
      image?: string | null;
    };
  }
}
