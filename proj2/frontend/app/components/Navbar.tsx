// app/components/Navbar.tsx
"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from 'next/navigation';

/**
 * Main navigation component for the Movie Munchers application
 * Provides consistent navigation links across all pages with responsive design
 * 
 * @returns Rendered navigation header component
 * 
 * @example
 * ```tsx
 * // Used in layout.tsx
 * <Navbar />
 * ```
 */
export default function Navbar({ updateTrigger }: any) {
  const [loggedIn, setLoggedIn] = useState(false);

  const determine_if_logged_in = async () => {
    const response = await fetch("http://localhost:5000/api/users/me", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include"
    });

    const responseData = await response.json();
    console.log(responseData);

    if (response.status == 200 && responseData.user_id) {
      setLoggedIn(true);
    } else if (response.status == 401) {
      setLoggedIn(false);
    }
  };

  useEffect(() => {
    determine_if_logged_in();
  }, [updateTrigger]);

  const router = useRouter();

  const logOut = async () => {
    const response = await fetch("http://localhost:5000/api/users/logout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include"
    });

    setLoggedIn(false);
    router.push('/');
  }

  return (
    <header className="sticky top-0 z-50 border-b bg-white/70 backdrop-blur">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link href="/" className="font-bold tracking-tight">🍿 Movie Munchers</Link>

        <div className="flex items-center gap-5 text-sm">
          <Link href="/">Home</Link>
          <Link href="/editdetails">My Profile</Link>
          <Link href="/menu">Menu</Link>
          <Link href="/checkout">Checkout</Link>
          <Link href="/track/12345">Track Order</Link>
          <Link href="/suppliers">Suppliers</Link>
          <Link href="/staff">Staff</Link>

          {!loggedIn && (<Link
            href="/login"
            className="rounded-xl border border-gray-300 px-4 py-1.5 text-sm hover:bg-gray-100 transition"
          >
            Login
          </Link>
          )}

          {!loggedIn && (
            <Link
              href="/signup"
              className="rounded-xl bg-black px-4 py-1.5 text-sm text-white opacity-80"
            >
              Signup
            </Link>)}

          {loggedIn && (
            <button
              onClick={(e) => { logOut(); }}
              className="rounded-xl bg-black px-4 py-1.5 text-sm text-white opacity-80">
              Logout
            </button>
          )}
        </div>
      </nav>
    </header>
  );
}
