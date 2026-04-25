// Auth.js v5 route handler — re-exports GET/POST from the central auth
// config. Matches /api/auth/* (callbacks, signin, signout, csrf, session).

import { handlers } from "@/lib/auth";

export const { GET, POST } = handlers;
