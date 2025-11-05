"use client";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import Link from "next/link";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    // TODO: Add actual authentication logic here when backend is ready
    // For now, just navigate to order page
    router.push("/order");
  };

  return (
    <section className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-2">Log In</h1>
      <p className="text-sm text-gray-600 mb-6">Sign in to manage your orders.</p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="email" className="block text-sm font-medium mb-1">
            Email
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="you@example.com"
          />
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium mb-1">
            Password
          </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="••••••••"
          />
        </div>

        <button
          type="submit"
          className="w-full rounded-xl bg-black px-5 py-2.5 text-sm text-white hover:bg-gray-800 transition"
        >
          Log In
        </button>
      </form>

      <p className="mt-4 text-center text-sm text-gray-600">
        Don&apos;t have an account?{" "}
        <Link href="/signup" className="font-medium text-black underline">
          Sign up
        </Link>
      </p>
    </section>
  );
}
