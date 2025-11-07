// app/layout.tsx
import type { Metadata } from "next";
import type { ReactNode } from "react";

import "../styles/globals.css";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

/**
 * Next.js metadata configuration for the application
 * Defines default title and description for SEO and browser display
 */
export const metadata: Metadata = {
  title: "Movie Munchers",
  description: "Snacks for every movie night",
};

/**
 * Root layout component that wraps all pages in the application
 * Provides consistent structure with navigation, main content area, and footer
 * 
 * @param props - Component props
 * @param props.children - Child components/pages to render in main content area
 * @returns Complete page structure with HTML document wrapper
 * 
 * @example
 * ```tsx
 * // Automatically wraps all pages in Next.js app directory
 * // Usage in pages:
 * export default function HomePage() {
 *   return <div>Page content goes here</div>;
 * }
 * ```
 */
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
