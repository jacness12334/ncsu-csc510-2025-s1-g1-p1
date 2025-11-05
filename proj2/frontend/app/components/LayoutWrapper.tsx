"use client";

import { usePathname } from "next/navigation";
import Navbar from "./Navbar";
import Footer from "./Footer";

export default function LayoutWrapper({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isHome = pathname === "/";

  return (
    <>
      {!isHome && <Navbar />}
      <main className="flex-grow mx-auto max-w-6xl px-4 py-8">{children}</main>
      {!isHome && <Footer />}
    </>
  );
}
