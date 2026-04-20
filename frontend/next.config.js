/** @type {import('next').NextConfig} */
const nextConfig = {
  // In local dev, proxy /api/* → http://localhost:8000/api/*
  // So you can call /api/... without CORS issues during development
  async rewrites() {
    return process.env.NODE_ENV === "development"
      ? [
          {
            source: "/api/:path*",
            destination: "http://localhost:8000/api/:path*",
          },
        ]
      : [];
  },
};

module.exports = nextConfig;
