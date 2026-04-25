// Tools tab — 4 interactive menus that need user input before the
// AI generates anything: Karir (career analysis), Hubungan (relation-
// ship compatibility), Refleksi (guided journal), Oracle (single-
// question verdict). Leaf pages with the actual forms come later.

import { TabListRow } from "@/components/tab-list-row";

export const metadata = {
  title: "Tools · Supernova",
};

const ITEMS = [
  {
    href: "/tools/karir",
    icon: "💼",
    title: "Karir",
    sub: "Apakah pekerjaan lo cocok sama angka & energi diri lo",
  },
  {
    href: "/tools/hubungan",
    icon: "💑",
    title: "Hubungan",
    sub: "Kompatibilitas + friction sama orang penting di hidup lo",
  },
  {
    href: "/tools/refleksi",
    icon: "📝",
    title: "Refleksi",
    sub: "Jurnal terbimbing — pertanyaan yang nge-prompt lo",
  },
  {
    href: "/tools/oracle",
    icon: "🔮",
    title: "Oracle",
    sub: "Tanya satu hal, dapet verdict tegas",
  },
];

export default function ToolsPage() {
  return (
    <div className="flex flex-col gap-5 pt-6">
      <header className="space-y-1">
        <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">
          Tools
        </p>
        <h1 className="font-serif text-2xl font-semibold tracking-tight">
          Bahan obrolan
        </h1>
        <p className="text-sm text-muted-foreground">
          Form-form yang nge-feed konteks ke obrolan, biar Supernova
          bisa baca lo lebih spesifik.
        </p>
      </header>

      <div className="flex flex-col gap-2">
        {ITEMS.map((item) => (
          <TabListRow key={item.href} {...item} />
        ))}
      </div>
    </div>
  );
}
