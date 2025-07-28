import type { NextConfig } from "next";

const glyphdTarget = process.env.GLYPHD_HOST || "http://localhost:8080";

const nextConfig: NextConfig = {
  productionBrowserSourceMaps: true,
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${glyphdTarget}/api/:path*`,
      },
    ];
  },
  env: {
    GLYPHD_HOST: process.env.GLYPHD_HOST,
  },
};

export default nextConfig;
