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
          <Link href="/editdetails">Edit Details</Link>
          <Link href="/order">Order</Link>
          <Link href="/track/12345">Track Order</Link>
          <CartButton />

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
