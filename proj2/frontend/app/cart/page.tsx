"use client";

import Link from "next/link";
import { useCartStore } from "@/lib/cartStore";

export default function CartPage() {
  const { items, add, decrement, remove } = useCartStore();
  const total = items.reduce((n, i) => n + i.price * i.qty, 0);

  return (
    <section className="mx-auto max-w-2xl mt-10">
      <h2 className="text-2xl font-bold mb-6 text-center">Your Cart</h2>

      {items.length === 0 ? (
        <div className="text-center">
          <p className="text-sm text-gray-600 mb-6">Your cart is empty.</p>
          <Link
            href="/menu"
            className="rounded-xl border border-gray-300 px-5 py-2 text-sm hover:bg-gray-100 transition"
          >
            ← Back to Menu
          </Link>
        </div>
      ) : (
        <>
          <ul className="divide-y">
            {items.map((i) => (
              <li key={i.id} className="flex items-center justify-between py-3">
                <div>
                  <div className="text-sm font-medium">{i.name}</div>
                  <div className="text-xs text-gray-600">${i.price.toFixed(2)} each</div>
                </div>

                <div className="flex items-center gap-3">
                  <button
                    onClick={() => decrement(i.id)}
                    className="h-7 w-7 rounded-lg border text-sm"
                    aria-label="decrease"
                  >
                    −
                  </button>
                  <span className="min-w-[2ch] text-sm text-center">{i.qty}</span>
                  <button
                    onClick={() => add({ id: i.id, name: i.name, price: i.price, description: "" }, 1)}
                    className="h-7 w-7 rounded-lg border text-sm"
                    aria-label="increase"
                  >
                    +
                  </button>

                  <span className="text-sm w-16 text-right">
                    ${(i.price * i.qty).toFixed(2)}
                  </span>

                  <button
                    onClick={() => remove(i.id)}
                    className="text-xs underline text-gray-600 hover:text-gray-900"
                  >
                    remove
                  </button>
                </div>
              </li>
            ))}
          </ul>

          <div className="mt-4 flex items-center justify-between border-t pt-4">
            <span className="text-sm font-medium">Total</span>
            <span className="text-sm font-semibold">${total.toFixed(2)}</span>
          </div>

          <div className="mt-6 flex flex-col sm:flex-row gap-3 justify-center">
            <Link
              href="/menu"
              className="rounded-xl border border-gray-300 px-5 py-2 text-sm hover:bg-gray-100 transition"
            >
              ← Back to Menu
            </Link>
            <Link
              href="/checkout"
              className="rounded-xl bg-black px-5 py-2 text-sm text-white hover:bg-gray-800 transition"
            >
              Proceed to Checkout →
            </Link>
          </div>
        </>
      )}
    </section>
  );
}
