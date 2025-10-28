// app/components/CartButton.tsx
"use client";
import Link from "next/link";
import { useCartStore } from "@/lib/cartStore";

export default function CartButton() {
  const count = useCartStore((s) => s.items.reduce((n, i) => n + i.qty, 0));
  return (
    <Link href="/cart" className="relative">
      Cart
      {count > 0 && (
        <span className="absolute -right-3 -top-2 rounded-full bg-black px-2 text-xs text-white">
          {count}
        </span>
      )}
    </Link>
  );
}
