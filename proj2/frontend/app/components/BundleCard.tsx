// app/components/BundleCard.tsx
"use client";
import { useCartStore } from "@/lib/cartStore";
import type { BundleItem } from "@/lib/types";

export default function BundleCard({ bundle }: { bundle: BundleItem }) {
  const add = useCartStore((s) => s.add);
  const dec = useCartStore((s) => s.decrement);
  const qty = useCartStore((s) => s.getQty(bundle.id));

  return (
    <div className="rounded-2xl border p-4 shadow-sm">
      <h3 className="text-base font-semibold">{bundle.name}</h3>
      {bundle.description && <p className="mt-1 text-sm text-gray-600">{bundle.description}</p>}

      <div className="mt-2 rounded-lg border p-3 text-xs text-gray-700">
        <div className="mb-1 font-semibold">
          Serves {bundle.serves} · ~{bundle.perPersonNutrition.calories} cal/person
        </div>
        <ul className="list-disc pl-4 space-y-1">
          {bundle.includes.map((line, i) => <li key={i}>{line}</li>)}
        </ul>
      </div>

      <div className="mt-3 flex items-center justify-between">
        <span className="text-sm font-medium">${bundle.price.toFixed(2)}</span>
        {qty === 0 ? (
          <button
            onClick={() => add({ id: bundle.id, name: bundle.name, price: bundle.price }, 1)}
            className="rounded-xl bg-black px-3 py-1.5 text-xs text-white"
          >
            Add bundle
          </button>
        ) : (
          <div className="flex items-center gap-2">
            <button onClick={() => dec(bundle.id, 1)} className="h-7 w-7 rounded-lg border text-sm">−</button>
            <span className="min-w-[2ch] text-sm text-center">{qty}</span>
            <button
            
            onClick={() => add({ id: bundle.id, name: bundle.name, price: bundle.price }, 1)}
              className="h-7 w-7 rounded-lg border text-sm"
            >
              +
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
