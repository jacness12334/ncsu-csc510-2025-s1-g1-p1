import Link from "next/link";

export default function CustomerProfilePage() {
  return (
    <section className="max-w-3xl mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-2">Profile</h1>
      <p className="text-sm text-gray-600 mb-6">Customer Profile here. (Coming soon)</p>

      <div className="flex gap-3">
        <Link
          href="/editdetails"
          className="rounded-xl bg-black px-5 py-2 text-sm text-white hover:bg-gray-800 transition"
        >
          Edit Details
        </Link>
        <Link
          href="/order"
          className="rounded-xl border border-gray-300 px-5 py-2 text-sm hover:bg-gray-100 transition"
        >
          Back to Ordering
        </Link>
      </div>
    </section>
  );
}
