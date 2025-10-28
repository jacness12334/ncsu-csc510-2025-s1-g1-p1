"use client";

import { useState } from "react";
import Link from "next/link";
import { useCartStore } from "@/lib/cartStore";

const TAX_RATE = 0.0725; // 7.25%
const DELIVERY_FEE = 3.99;
const FREE_DELIVERY_THRESHOLD = 35;

function money(n: number) {
  return `$${n.toFixed(2)}`;
}

export default function CartPage() {
  const { items, add, decrement, remove } = useCartStore();

  const [tipMode, setTipMode] = useState<"0" | "10" | "15" | "20" | "custom">("0");
  const [customTipPct, setCustomTipPct] = useState<string>("");

  const subtotal = items.reduce((n, i) => n + i.price * i.qty, 0);
  const tax = subtotal * TAX_RATE;

  const delivery = subtotal >= FREE_DELIVERY_THRESHOLD ? 0 : DELIVERY_FEE;

  const tipPct =
    tipMode === "custom"
      ? Math.max(0, Number(customTipPct || 0)) / 100
      : Number(tipMode) / 100;

  const tipAmount = subtotal * tipPct;
  const total = subtotal + tax + delivery + tipAmount;

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
                  <div className="text-xs text-gray-600">{money(i.price)} each</div>
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
                    onClick={() => add({ id: i.id, name: i.name, price: i.price }, 1)}
                    className="h-7 w-7 rounded-lg border text-sm"
                    aria-label="increase"
                  >
                    +
                  </button>

                  <span className="text-sm w-16 text-right">{money(i.price * i.qty)}</span>

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

          {/* Breakdown */}
          <div className="mt-6 grid gap-4 rounded-2xl border p-4">
            <div className="flex justify-between">
              <span className="text-sm text-gray-700">Subtotal</span>
              <span className="text-sm font-medium">{money(subtotal)}</span>
            </div>

            <div className="flex justify-between">
              <span className="text-sm text-gray-700">
                Tax <span className="text-xs text-gray-500">({(TAX_RATE * 100).toFixed(2)}%)</span>
              </span>
              <span className="text-sm font-medium">{money(tax)}</span>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-700">
                Delivery Fee{" "}
                {subtotal >= FREE_DELIVERY_THRESHOLD && (
                  <span className="text-xs text-green-600 ml-1">(Free over ${FREE_DELIVERY_THRESHOLD})</span>
                )}
              </span>
              <span className={`text-sm font-medium ${subtotal >= FREE_DELIVERY_THRESHOLD ? "text-green-600" : ""}`}>
                {subtotal >= FREE_DELIVERY_THRESHOLD ? "Free" : money(DELIVERY_FEE)}
              </span>
            </div>

            {/* Tip */}
            <div className="flex flex-col gap-2">
              <span className="text-sm text-gray-700">
                Tip <span className="text-xs text-gray-500">(on subtotal)</span>
              </span>
              <div className="flex flex-wrap gap-2">
                {(["0", "10", "15", "20"] as const).map((pct) => (
                  <button
                    key={pct}
                    onClick={() => setTipMode(pct)}
                    className={`rounded-xl border px-3 py-1.5 text-sm ${
                      tipMode === pct ? "bg-black text-white border-black" : "hover:bg-gray-100"
                    }`}
                  >
                    {pct}%
                  </button>
                ))}
                <button
                  onClick={() => setTipMode("custom")}
                  className={`rounded-xl border px-3 py-1.5 text-sm ${
                    tipMode === "custom" ? "bg-black text-white border-black" : "hover:bg-gray-100"
                  }`}
                >
                  Custom
                </button>
                {tipMode === "custom" && (
                  <div className="flex items-center gap-2">
                    <input
                      inputMode="decimal"
                      value={customTipPct}
                      onChange={(e) => setCustomTipPct(e.target.value)}
                      placeholder="e.g. 12"
                      className="w-20 rounded-lg border px-2 py-1 text-sm"
                    />
                    <span className="text-sm text-gray-600">%</span>
                  </div>
                )}
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-700">Tip Amount</span>
                <span className="text-sm font-medium">{money(tipAmount)}</span>
              </div>
            </div>

            {/* Total */}
            <div className="flex justify-between border-t pt-3">
              <span className="text-sm font-semibold">Total</span>
              <span className="text-sm font-semibold">{money(total)}</span>
            </div>
          </div>

          {/* Buttons */}
          <div className="mt-6 flex flex-col sm:flex-row gap-3 justify-center">
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
        </>
      )}
    </section>
  );
}
