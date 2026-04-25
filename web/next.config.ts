import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Prisma's query engine (binary in node_modules/.prisma/client) must
  // not be bundled by webpack/turbopack — keep it as an external module.
  serverExternalPackages: ["@prisma/client", "@prisma/engines", ".prisma/client"],
};

export default nextConfig;
