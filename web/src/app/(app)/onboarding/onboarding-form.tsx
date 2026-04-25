"use client";

import { useActionState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { INDONESIA_CITIES } from "@/lib/zodiac";
import { submitOnboarding, type OnboardingState } from "./actions";

const initial: OnboardingState = {};
const cityOptions = Object.keys(INDONESIA_CITIES).sort();

export function OnboardingForm() {
  const [state, action, pending] = useActionState(submitOnboarding, initial);

  const fieldError = (k: keyof NonNullable<OnboardingState["fieldErrors"]>) =>
    state.fieldErrors?.[k];

  return (
    <form action={action} className="flex flex-col gap-5">
      <Field
        label="Nama lengkap"
        name="fullName"
        placeholder="Contoh: Budi Santoso"
        helper="Nama lengkap di akta — itu yang dibaca numerologi."
        required
        autoComplete="name"
        error={fieldError("fullName")}
      />

      <Field
        label="Nickname (opsional)"
        name="nickname"
        placeholder="Yang biasa lo dipanggil"
        autoComplete="nickname"
        error={fieldError("nickname")}
      />

      <Field
        label="Tanggal lahir"
        name="dob"
        type="date"
        required
        error={fieldError("dob")}
      />

      <div className="grid grid-cols-2 gap-3">
        <Field
          label="Jam lahir"
          name="birthTime"
          placeholder="13:30"
          helper="Buat moon & rising. Skip kalo gak tau."
          error={fieldError("birthTime")}
        />
        <Field
          label="Kota lahir"
          name="birthCity"
          placeholder="Jakarta"
          listId="cities"
          autoComplete="address-level2"
          error={fieldError("birthCity")}
        />
      </div>
      <datalist id="cities">
        {cityOptions.map((c) => (
          <option key={c} value={c.charAt(0).toUpperCase() + c.slice(1)} />
        ))}
      </datalist>

      {state.error ? (
        <p className="text-sm text-destructive">{state.error}</p>
      ) : null}

      <Button type="submit" className="h-11 mt-1" disabled={pending}>
        {pending ? "Lagi nyusun…" : "Mulai baca diri"}
      </Button>

      <p className="text-xs text-muted-foreground/70 leading-relaxed">
        Data ini dipake buat hitung angka & lapisan lo. Disimpen di akun
        lo aja, gak dikirim ke pihak ketiga selain Anthropic untuk
        bahan obrolan.
      </p>
    </form>
  );
}

function Field({
  label,
  name,
  type = "text",
  placeholder,
  helper,
  required,
  autoComplete,
  listId,
  error,
}: {
  label: string;
  name: string;
  type?: string;
  placeholder?: string;
  helper?: string;
  required?: boolean;
  autoComplete?: string;
  listId?: string;
  error?: string;
}) {
  return (
    <div className="flex flex-col gap-1.5">
      <Label htmlFor={name}>{label}</Label>
      <Input
        id={name}
        name={name}
        type={type}
        placeholder={placeholder}
        required={required}
        autoComplete={autoComplete}
        list={listId}
        aria-invalid={Boolean(error) || undefined}
      />
      {helper && !error ? (
        <p className="text-xs text-muted-foreground">{helper}</p>
      ) : null}
      {error ? <p className="text-xs text-destructive">{error}</p> : null}
    </div>
  );
}
