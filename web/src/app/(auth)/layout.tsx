// Auth route group — minimal shell, no bottom tab bar (user isn't signed
// in yet). Just centers the form vertically.

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <main className="sn-shell flex flex-col justify-center min-h-[100dvh] py-12">
      {children}
    </main>
  );
}
