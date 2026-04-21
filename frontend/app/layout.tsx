import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";
import BackendWarmup from "@/components/BackendWarmup";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Credit Risk AI | Advanced Scoring",
  description: "AI-powered credit risk and lending decision support system.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark scroll-smooth">
      <body className={`${inter.className} bg-black text-white antialiased`}>
        <BackendWarmup />
        <Navbar />
        <main className="min-h-screen">
          {children}
        </main>
      </body>
    </html>
  );
}
