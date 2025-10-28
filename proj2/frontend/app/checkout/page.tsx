"use client";

import Link from "next/link";

export default function CheckoutPage() {
  return (
    <section className="max-w-2xl mx-auto text-center mt-10">
      <h2 className="text-2xl font-bold mb-4">Checkout</h2>
      <p className="text-sm text-gray-600 mb-8">
        Review your payment details and confirm your order.  
        (Payment integration coming soon.)
      </p>

      {/* Back button */}
      <Link
        href="/cart"
        className="inline-block rounded-xl border border-gray-300 px-5 py-2 text-sm hover:bg-gray-100 transition"
      >
        ← Back to Cart
      </Link>
    </section>
  );
}
