"use client";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import Link from "next/link";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const setCookie = (name: string, value: string, days: number) => {
    const expirationDate = new Date();
    expirationDate.setDate(expirationDate.getDate() + days); // Set expiration in days
    document.cookie = `${name}=${value}; expires=${expirationDate.toUTCString()}; path=/`;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();


    try {
      const response = await fetch("http://localhost:5000/api/users/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password
        }),
        credentials: "include"
      });

      if (!response.ok) {
        // If server responds with 400/500 code, get the specific message
        const errorData = await response.json();
        throw new Error(errorData.message || response.statusText);
      }

      console.log(await response.text());

      // Success path:
      // setCookie('sessionToken', '', 1);
      // router.push("/order");
      alert("Login successful!");

    } catch (error: any) {
      // This catches network errors AND the error thrown above
      console.error(error);
      alert("Error: " + error.message);
    }

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
