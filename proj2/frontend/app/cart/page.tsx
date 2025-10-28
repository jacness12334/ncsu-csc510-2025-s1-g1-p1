"use client";

import Link from "next/link";

export default function CartPage() {
  return (
    <section className="flex flex-col items-center justify-center mt-16 text-center">
      <h2 className="text-2xl font-bold mb-6">Your Cart</h2>
      <p className="text-sm text-gray-600 mb-8">(Cart details coming soon)</p>

      {/* Buttons */}
      <div className="flex flex-col sm:flex-row gap-4">
        <Link
          href="/menu"
          className="rounded-xl border border-gray-300 px-5 py-2 text-sm hover:bg-gray-100 transition"
        >
          ← Go Back to Menu
        </Link>

        <Link
          href="/checkout"
          className="rounded-xl bg-black px-5 py-2 text-sm text-white hover:bg-gray-800 transition"
        >
          Proceed to Checkout →
        </Link>
      </div>
    </section>
  );
}
