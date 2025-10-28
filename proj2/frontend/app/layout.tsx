export const metadata = {
  title: "Movie Munchers",
  description: "Snacks for every movie night",
};

import React from "react";
import "../styles/globals.css";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-screen flex flex-col bg-white text-gray-900">
        {/* Navbar always on top */}
        <Navbar />

        {/* Main content grows to fill available space */}
        <main className="flex-grow mx-auto w-full max-w-6xl px-4 py-8">
          {children}
        </main>

        {/* Footer sticks to bottom when content is short */}
        <Footer />
      </body>
    </html>
  );
}
