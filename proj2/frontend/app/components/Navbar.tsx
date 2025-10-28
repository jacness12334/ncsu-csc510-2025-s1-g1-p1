"use client";
import Link from "next/link";
import CartButton from "./CartButton";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b bg-white/70 backdrop-blur">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link href="/" className="font-bold tracking-tight">
          🍿 Movie Munchers
        </Link>

        <div className="flex gap-5 text-sm">
          <Link href="/menu">Menu</Link>
          <Link href="/track/12345">Track Order</Link>
          <CartButton />
        </div>
      </nav>
    </header>
  );
}
