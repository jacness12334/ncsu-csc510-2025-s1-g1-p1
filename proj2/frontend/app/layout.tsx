// app/layout.tsx
import type { Metadata } from "next";
import type { ReactNode } from "react";

import "../styles/globals.css";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

export const metadata: Metadata = {
  title: "Movie Munchers",
  description: "Snacks for every movie night",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-screen flex flex-col bg-white text-gray-900">
        <Navbar />
        <main className="flex-grow mx-auto w-full max-w-6xl px-4 py-8">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
