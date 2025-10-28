// app/menu/page.tsx
import Link from "next/link";
import { MENU, BUNDLES } from "@/lib/sampleData";
import MenuCard from "../components/MenuCard";
import BundleCard from "@/app/components/BundleCard";

export default function MenuPage() {
  return (
    <section className="grid gap-8">
      
      {/* Regular menu */}
      <div>
        <h3 className="mb-4 text-lg font-semibold">Concessions</h3>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {MENU.map((m) => (
            <MenuCard key={m.id} item={m} />
          ))}
        </div>
      </div>

      {/* Bundles */}
      <div>
        <h2 className="mb-2 text-xl font-bold">Family Movie Night Bundles</h2>
        <p className="text-sm text-gray-600 mb-4">
          Premade bundles with per-person nutrition.
        </p>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {BUNDLES.map((b) => (
            <BundleCard key={b.id} bundle={b} />
          ))}
        </div>
      </div>

      {/* Go to Cart */}
      <div className="flex justify-center mt-4">
        <Link
          href="/cart"
          className="rounded-xl bg-black px-6 py-2 text-sm text-white hover:bg-gray-800 transition"
        >
          Go to Cart
        </Link>
      </div>
    </section>
  );
}
