import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { NavBar } from "@/components/NavBar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Tools",
  description:
    "A collection of AI tools including Multimodal QA and LLM Inference Calculator",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen bg-background`}>
        {/* <NavBar /> */}
        <main className="container mx-auto px-4 py-6">{children}</main>
      </body>
    </html>
  );
}
