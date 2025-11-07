// app/components/MenuCard.tsx
"use client";
import type { MenuItem } from "@/lib/types";
import { useCartStore } from "@/lib/cartStore";

/**
 * React component for displaying a single menu item with add-to-cart functionality
 * Integrates with the cart store for quantity management and provides interactive controls
 * 
 * @param props - Component props
 * @param props.item - Menu item data to display
 * @returns Rendered menu card component
 * 
 * @example
 * ```tsx
 * const menuItem = {
 *   id: "popcorn-lg",
 *   name: "Large Popcorn",
 *   description: "Buttery and delicious",
 *   price: 8.99,
 *   category: "Snacks"
 * };
 * 
 * <MenuCard item={menuItem} />
 * ```
 */
export default function MenuCard({ item }: { item: MenuItem }) {
  const add = useCartStore((s) => s.add);
  const dec = useCartStore((s) => s.decrement);
  const qty = useCartStore((s) => s.getQty(item.id));

  return (
    <div className="rounded-2xl border p-4 shadow-sm">
      <h3 className="text-base font-semibold">{item.name}</h3>
      <p className="mt-1 text-sm text-gray-600">{item.description ?? "Tasty snack"}</p>

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
