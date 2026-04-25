// Next 16 proxy (formerly middleware). Runs in the nodejs runtime so
// auth() can hit Postgres directly. Default-deny: anything not on the
// public whitelist is gated behind a valid Auth.js session.

import { NextResponse, type NextRequest } from "next/server";
import { auth } from "@/lib/auth";

const PUBLIC_PATHS = new Set<string>([
  "/",
  "/sign-in",
  "/verify-request",
]);

function isPublic(pathname: string) {
  if (PUBLIC_PATHS.has(pathname)) return true;
  if (pathname.startsWith("/api/auth/")) return true; // Auth.js callbacks
  if (pathname.startsWith("/_next/")) return true;
  if (pathname.startsWith("/icons/")) return true;
  if (pathname === "/manifest.webmanifest") return true;
  if (pathname === "/favicon.ico") return true;
  return false;
}

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (isPublic(pathname)) {
    return NextResponse.next();
  }

  const session = await auth();
  if (!session?.user) {
    const url = new URL("/sign-in", request.url);
    url.searchParams.set("next", pathname);
    return NextResponse.redirect(url);
  }

  return NextResponse.next();
}

export const config = {
  // Run on every route except static assets. The proxy itself handles
  // the public/auth check via isPublic().
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
