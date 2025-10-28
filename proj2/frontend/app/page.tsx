import Link from "next/link";

export default function Home() {
  return (
    <section className="mt-16 grid place-items-center">
      <div className="w-full max-w-2xl text-center">
        <h1 className="text-3xl font-bold">Welcome to Movie Munchers</h1>
        <p className="mt-2 text-sm text-gray-600">
          Mindful snacks, family bundles, and a theater experience anywhere.
        </p>

        <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
          <Link
            href="/order"
            className="rounded-xl border border-gray-300 px-5 py-2 text-sm"
          >
            Continue as Guest
          </Link>
          <button
            disabled
            className="rounded-xl border border-gray-300 px-5 py-2 text-sm text-gray-500 cursor-not-allowed"
          >
            Log In
          </button>
          <button
            disabled
            className="rounded-xl bg-black px-5 py-2 text-sm text-white opacity-80 cursor-not-allowed"
          >
            Sign Up
          </button>
        </div>
      </div>
    </section>
  );
}
