// Diri tab — landing page with 6 menu rows. Each row navigates to a
// leaf reading page (built in later sessions). The bottom tab bar
// keeps "Diri" highlighted on every /diri/* leaf.

import { TabListRow } from "@/components/tab-list-row";

export const metadata = {
  title: "Diri · Supernova",
};

const ITEMS = [
  {
    href: "/diri/karakter",
    icon: "👤",
    title: "Karakter",
    sub: "Karakter inti — yang lo bawa dari lahir",
  },
  {
    href: "/diri/inner",
    icon: "🔍",
    title: "Sisi Batin",
    sub: "Apa yang lo butuh, takutin, kejar diam-diam",
  },
  {
    href: "/diri/karmic",
    icon: "🎓",
    title: "PR Hidup",
    sub: "Pelajaran yang ngintilin lo seumur hidup",
  },
  {
    href: "/diri/fase",
    icon: "🎯",
    title: "Fase Hidup",
    sub: "Babak besar yang lagi lo jalanin",
  },
  {
    href: "/diri/arah",
    icon: "🧭",
    title: "Arah",
    sub: "Bulan & tahun ini — kemana energinya nuntun",
  },
  {
    href: "/diri/mbti",
    icon: "🧠",
    title: "MBTI",
    sub: "Tipe kepribadian — bagaimana lo proses dunia",
  },
];

export default function DiriPage() {
  return (
    <div className="flex flex-col gap-5 pt-6">
      <header className="space-y-1">
        <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">
          Diri
        </p>
        <h1 className="font-serif text-2xl font-semibold tracking-tight">
          Bacaan tentang lo
        </h1>
      </header>

      <div className="flex flex-col gap-2">
        {ITEMS.map((item) => (
          <TabListRow key={item.href} {...item} />
        ))}
      </div>
    </div>
  );
}
