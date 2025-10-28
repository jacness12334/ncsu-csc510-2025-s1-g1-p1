import { MENU } from "../../lib/sampleData";
import MenuCard from "../components/MenuCard";
import BundleBuilder from "../components/BundleBuilder";

export default function MenuPage() {
  return (
    <section className="grid gap-8">
      <div>
        <h2 className="mb-4 text-xl font-bold">Menu</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {MENU.map((m) => (
            <MenuCard key={m.id} item={m} />
          ))}
        </div>
      </div>

      {/* Bundle Section */}
      <div>
        <h3 className="text-lg font-semibold">Build a Bundle</h3>
        <p className="text-sm text-gray-600 mb-2">
          Choose multiple snacks to create your own family or group bundle.
        </p>
        <BundleBuilder />
      </div>
    </section>
  );
}
