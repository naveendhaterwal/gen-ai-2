/** @type {import('next').NextConfig} */
const nextConfig = {
  // In local development, proxy /_/backend/* → http://localhost:8000/*
  // This mirrors how Vercel routes the backend in production
  async rewrites() {
    return [
      {
        source: "/_/backend/:path*",
        destination: "http://localhost:8000/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
