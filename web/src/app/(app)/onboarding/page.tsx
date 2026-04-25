import { requireNoProfile } from "@/lib/auth-guards";
import { OnboardingForm } from "./onboarding-form";

export const metadata = {
  title: "Kenalan dulu · Supernova",
};

export default async function OnboardingPage() {
  await requireNoProfile();
  return (
    <div className="flex flex-1 flex-col gap-6 py-8">
      <div className="space-y-2">
        <span className="sn-wordmark">✨ Supernova</span>
        <h1 className="font-serif text-2xl font-semibold tracking-tight">
          Kenalan dulu
        </h1>
        <p className="text-sm text-muted-foreground leading-relaxed">
          Lo gak perlu jawab semuanya — yang penting nama lengkap & tanggal
          lahir. Sisanya bikin pembacaan lebih dalam.
        </p>
      </div>
      <OnboardingForm />
    </div>
  );
}
