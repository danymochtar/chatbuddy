# Supernova — Next.js mobile app

PWA rewrite of the Streamlit chatbot. Stack:

- **Next.js 16** App Router · **React 19.2** · **Tailwind v4**
- **shadcn/ui** (radix primitives, manually-vendored components)
- **Drizzle ORM** + **Neon Postgres** (serverless)
- **Auth.js v5** (`next-auth@beta`) — magic link via Resend
- **Vercel AI SDK** (`ai` + `@ai-sdk/anthropic`) — streaming chat
- **PWA** — manifest + service worker, installable to iPhone home screen

## Build status

- Sesi 1 ✅ scaffold + foundation
- Sesi 2 ⏳ DB schema + Auth.js + sign-in flow
- Sesi 3 ⏳ Port `numerology.py` + `zodiac.py` to TypeScript
- Sesi 4 ⏳ 5 tab pages (Beranda · Diri · Vibe · Tools · Profil)
- Sesi 5 ⏳ Anthropic streaming + chat persistence
- Sesi 6 ⏳ PWA + polish + deploy

## Local setup

```bash
cp .env.example .env.local
# fill in ANTHROPIC_API_KEY, DATABASE_URL, AUTH_SECRET, RESEND_API_KEY, EMAIL_FROM

npm install
npm run dev          # http://localhost:3000
```

## Folder structure

```
src/
├── app/
│   ├── (auth)/      # sign-in, magic-link verify
│   ├── (app)/       # authed app shell + 5 tabs
│   ├── api/         # /api/chat, /api/auth
│   ├── layout.tsx   # root: fonts + metadata + viewport
│   └── page.tsx     # public landing
├── components/
│   └── ui/          # shadcn primitives (button, card, dialog, ...)
├── lib/
│   ├── numerology/  # TS port of the math
│   ├── zodiac/      # sun/shio/weton helpers
│   ├── db/          # drizzle schema + client
│   └── i18n/        # bilingual TEXTS (id / en)
└── hooks/
```

## Notes for AI coders

This project uses **Next.js 16** which has breaking changes vs 15:
- All request APIs are async (`await cookies()`, `await params`, `await searchParams`)
- `middleware.ts` is now `proxy.ts`
- `next lint` removed — use ESLint CLI directly
- `revalidateTag(tag)` requires a second `cacheLife` arg
- Tailwind v4 — no `tailwind.config.ts`, theme tokens in `@theme inline {}`

Always check `node_modules/next/dist/docs/` for the canonical reference.
