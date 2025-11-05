// app/page.tsx
import Link from "next/link";

export default function Home() {
  return (
    <section className="mt-16 grid place-items-center">
      <div className="w-full max-w-2xl text-center">
        <h1 className="text-3xl font-bold">Welcome to Movie Munchers</h1>
        <p className="mt-2 text-sm text-gray-600">
          Snacks, family bundles, and a theater experience anywhere.
        </p>
      </div>
    </section>
  );
}
