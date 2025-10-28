"use client";

import Link from "next/link";

export default function OrderPage() {
  return (
    <section className="flex flex-col items-center justify-center mt-10">
      <h2 className="text-2xl font-bold mb-6">Choose Where to Order From</h2>

      <div className="grid gap-6 sm:grid-cols-2 max-w-3xl w-full">
        {/* Concession Option */}
        <div className="rounded-2xl border p-6 text-center shadow-sm hover:shadow-md transition">
          <h3 className="text-lg font-semibold mb-2">🎬 Concession Stand</h3>
          <p className="text-sm text-gray-600 mb-4">
            Order snacks directly from the theater concession stand.
          </p>
          <Link
            href="/menu"
            className="inline-block rounded-xl bg-black px-5 py-2 text-sm text-white"
          >
            Order from Concessions
          </Link>
        </div>

        {/* Local Restaurants Option */}
        <div className="rounded-2xl border p-6 text-center opacity-60 cursor-not-allowed">
          <h3 className="text-lg font-semibold mb-2">🍔 Local Restaurants</h3>
          <p className="text-sm text-gray-600 mb-4">
            Coming soon — partner with local restaurants for “Dinner + Movie” bundles.
          </p>
          <button
            className="rounded-xl border px-5 py-2 text-sm cursor-not-allowed"
            disabled
          >
            Coming Soon
          </button>
        </div>
      </div>
    </section>
  );
}
