import Link from "next/link";

import { SignInForm } from "./sign-in-form";

export const metadata = {
  title: "Masuk · Supernova",
};

export default function SignInPage() {
  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <Link href="/" className="text-xs text-muted-foreground/70 hover:text-foreground">
          ‹ Balik
        </Link>
        <h1 className="font-serif text-3xl font-semibold tracking-tight">
          Masuk
        </h1>
        <p className="text-sm text-muted-foreground">
          Masukin email lo. Kita kirim link sekali pakai — gak perlu password.
        </p>
      </div>
      <SignInForm />
      <p className="text-xs text-muted-foreground/70 leading-relaxed">
        Dengan masuk, lo setuju Supernova nyimpen profile + chat lo di
        Postgres yang gw kelola. Lo bisa hapus akun + semua data kapan aja
        dari menu Profil.
      </p>
    </div>
  );
}
