// Auth.js v5 (NextAuth beta) — magic-link email via Resend, persisted via
// the Prisma adapter. The exported handlers / signIn / signOut / auth are
// imported by the route handler, server actions, and middleware.

import NextAuth from "next-auth";
import Resend from "next-auth/providers/resend";
import { PrismaAdapter } from "@auth/prisma-adapter";

import { prisma } from "@/lib/db/prisma";
import { sendMagicLinkEmail } from "@/lib/email/magic-link";

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: PrismaAdapter(prisma),
  session: { strategy: "database" },
  pages: {
    signIn: "/sign-in",
    verifyRequest: "/verify-request",
  },
  providers: [
    Resend({
      apiKey: process.env.RESEND_API_KEY,
      from: process.env.EMAIL_FROM,
      // Custom email content — overrides the default plaintext template.
      sendVerificationRequest: async ({ identifier, url, provider }) => {
        await sendMagicLinkEmail({
          to: identifier,
          url,
          from: provider.from as string,
          resendApiKey: provider.apiKey as string,
        });
      },
    }),
  ],
  callbacks: {
    // Add the user id to the session so server components can read it.
    session: async ({ session, user }) => {
      if (session.user) {
        session.user.id = user.id;
      }
      return session;
    },
  },
});
