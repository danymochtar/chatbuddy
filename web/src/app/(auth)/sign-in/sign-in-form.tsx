"use client";

import { useActionState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { sendMagicLink, type SignInState } from "./actions";

const initial: SignInState = {};

export function SignInForm() {
  const [state, formAction, pending] = useActionState(sendMagicLink, initial);

  if (state.success) {
    return (
      <div className="rounded-xl border border-border bg-card p-5 text-sm text-muted-foreground">
        ✨ Cek inbox lo. Kalau gak nongol dalam semenit, intip folder spam.
      </div>
    );
  }

  return (
    <form action={formAction} className="flex flex-col gap-3">
      <div className="flex flex-col gap-1.5">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          name="email"
          type="email"
          required
          autoComplete="email"
          placeholder="kamu@contoh.com"
          disabled={pending}
        />
      </div>
      {state.error ? (
        <p className="text-sm text-destructive">{state.error}</p>
      ) : null}
      <Button type="submit" className="h-11 mt-1" disabled={pending}>
        {pending ? "Ngirim…" : "Kirim magic link"}
      </Button>
    </form>
  );
}
