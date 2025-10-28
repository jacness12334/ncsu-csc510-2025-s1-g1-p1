// app/components/MenuCard.tsx
"use client";
import type { MenuItem } from "@/lib/types";
import NutritionBadge from "./NutritionBadge";
import { useCartStore } from "@/lib/cartStore";

export default function MenuCard({ item }: { item: MenuItem }) {
  const add = useCartStore((s) => s.add);
  const dec = useCartStore((s) => s.decrement);
  const qty = useCartStore((s) => s.getQty(item.id));

  return (
    <div className="rounded-2xl border p-4 shadow-sm">
      <h3 className="text-base font-semibold">{item.name}</h3>
      <p className="mt-1 text-sm text-gray-600">{item.description ?? "Tasty snack"}</p>
      <NutritionBadge n={item.nutrition} />

      <div className="mt-3 flex items-center justify-between">
        <span className="text-sm font-medium">${item.price.toFixed(2)}</span>

        {qty === 0 ? (
          <button onClick={() => add(item, 1)} className="rounded-xl bg-black px-3 py-1.5 text-xs text-white">
            Add to cart
          </button>
        ) : (
          <div className="flex items-center gap-2">
            <button onClick={() => dec(item.id, 1)} className="h-7 w-7 rounded-lg border text-sm" aria-label="decrease">−</button>
            <span className="min-w-[2ch] text-sm text-center">{qty}</span>
            <button onClick={() => add(item, 1)} className="h-7 w-7 rounded-lg border text-sm" aria-label="increase">+</button>
          </div>
        )}
      </div>
    </div>
  );
}
