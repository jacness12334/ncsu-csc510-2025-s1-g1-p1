// app/track/[orderId]/page.tsx
export default function TrackPage({ params }: { params: { orderId: string } }) {
  return (
    <section className="text-center mt-16">
      <h2 className="text-2xl font-bold mb-2">Order Tracking</h2>
      <p className="text-sm text-gray-600">
        Order #{params.orderId}: Preparing → En route → Delivered
      </p>
    </section>
  );
}
