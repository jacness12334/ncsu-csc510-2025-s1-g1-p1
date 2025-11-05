// app/track/[orderId]/page.tsx
import Link from "next/link";

export default function TrackPage({ params }: { params: { orderId: string } }) {
  return (
    <section className="text-center mt-16">
      <h2 className="text-2xl font-bold mb-2">Order Tracking</h2>
      <p className="text-sm text-gray-600 mb-6">
        Order #{params.orderId}: Status
      </p>
      
      <Link
        href="/order"
        className="inline-block rounded-xl border border-gray-300 px-5 py-2 text-sm hover:bg-gray-100 transition"
      >
        Back to Ordering
      </Link>
    </section>
  );
}
