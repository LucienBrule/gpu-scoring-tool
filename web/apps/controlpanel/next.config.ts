import type { NextConfig } from "next";

const glyphdTarget = process.env.GLYPHD_HOST || "http://localhost:8080";

const nextConfig: NextConfig = {
  productionBrowserSourceMaps: true,
  reactStrictMode: true,

  pageExtensions: ["js", "jsx", "ts", "tsx"],

  images: {
    unoptimized: true,
  },

  async rewrites() {
    return {
      beforeFiles: [
        {
          source: "/api/:path*",
          destination: `${glyphdTarget}/api/:path*`,
        },
      ],
    };
  },

  env: {
    GLYPHD_HOST: process.env.GLYPHD_HOST,
  },

  experimental: {
    optimizeCss: false,
  },
};

export default nextConfig;
