// app/components/Navbar.tsx
"use client";
import Link from "next/link";

/**
 * Main navigation component for the Movie Munchers application
 * Provides consistent navigation links across all pages with responsive design
 * 
 * @returns Rendered navigation header component
 * 
 * @example
 * ```tsx
 * // Used in layout.tsx
 * <Navbar />
 * ```
 */
export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b bg-white/70 backdrop-blur">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link href="/" className="font-bold tracking-tight">🍿 Movie Munchers</Link>

        <div className="flex items-center gap-5 text-sm">
          <Link href="/">Home</Link>
          <Link href="/editdetails">My Profile</Link>
          <Link href="/menu">Menu</Link>
          <Link href="/checkout">Checkout</Link>
          <Link href="/track/12345">Track Order</Link>
          <Link href="/suppliers">Suppliers</Link>
          <Link href="/staff">Staff</Link>

          <Link
            href="/login"
            className="rounded-xl border border-gray-300 px-4 py-1.5 text-sm hover:bg-gray-100 transition"
          >
            Log In
          </Link>
          <Link
            href="/signup"
            className="rounded-xl bg-black px-4 py-1.5 text-sm text-white opacity-80"
          >
            Sign Up
          </Link>
        </div>
      </nav>
    </header>
  );
}
