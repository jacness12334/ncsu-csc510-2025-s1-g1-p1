// app/components/Navbar.tsx
"use client";
import Link from "next/link";
import CartButton from "./CartButton";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b bg-white/70 backdrop-blur">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link href="/" className="font-bold tracking-tight">🍿 Movie Munchers</Link>

        <div className="flex items-center gap-5 text-sm">
          <Link href="/">Home</Link>
          <Link href="/order">Order</Link>
          <Link href="/track/12345">Track Order</Link>
          <Link href="/userdetails">User Details</Link>
          <CartButton />

          {/* Placeholder auth buttons */}
          <button className="rounded-xl border border-gray-300 px-4 py-1.5 text-sm hover:bg-gray-100 transition" disabled>
            Log In
          </button>
          <button className="rounded-xl bg-black px-4 py-1.5 text-sm text-white opacity-80" disabled>
            Sign Up
          </button>
        </div>
      </nav>
    </header>
  );
}
