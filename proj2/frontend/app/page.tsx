// app/page.tsx
import Link from "next/link";

export default function HomePage() {
  return (
    <section className="flex flex-col items-center justify-center min-h-screen bg-white text-center px-4">
      <h1 className="text-3xl font-bold mb-10">Movie Munchers</h1>

      <div className="flex flex-col gap-4 w-full max-w-xs">
        <Link
          href="/login"
          className="rounded-xl bg-black text-white px-5 py-2 text-sm font-medium hover:bg-gray-800 transition"
        >
          Log In
        </Link>

        <Link
          href="/signup"
          className="rounded-xl border border-gray-300 px-5 py-2 text-sm font-medium hover:bg-gray-100 transition"
        >
          Sign Up
        </Link>

        <Link
          href="/order"
          className="rounded-xl bg-gray-200 px-5 py-2 text-sm font-medium hover:bg-gray-300 transition"
        >
          Continue as Guest
        </Link>
      </div>
    </section>
  );
}
