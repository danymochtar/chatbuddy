// Server action that triggers the magic-link send via Auth.js. Imported
// by the sign-in form; runs server-side, no API key on the client.

"use server";

import { z } from "zod";
import { signIn } from "@/lib/auth";

const FormSchema = z.object({
  email: z.string().email("Email-nya kayaknya gak valid."),
});

export type SignInState = {
  error?: string;
  success?: boolean;
};

export async function sendMagicLink(
  _prev: SignInState,
  formData: FormData,
): Promise<SignInState> {
  const parsed = FormSchema.safeParse({
    email: formData.get("email"),
  });
  if (!parsed.success) {
    return { error: parsed.error.issues[0]?.message ?? "Form gak valid." };
  }

  try {
    await signIn("resend", {
      email: parsed.data.email,
      redirectTo: "/beranda",
      redirect: false,
    });
    return { success: true };
  } catch (err) {
    // Auth.js throws redirect errors when redirect: true; with redirect: false
    // a real failure surfaces here.
    const msg = err instanceof Error ? err.message : "Gak bisa kirim email.";
    return { error: msg };
  }
}
