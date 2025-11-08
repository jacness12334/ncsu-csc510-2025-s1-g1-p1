// app/components/Footer.tsx
import Link from "next/link";

/**
 * 
 * @returns extra information and links
 */
export default function Footer() {
  return (
    <footer className="mt-auto border-t py-6 text-center text-xs text-gray-600">
      <div className="flex flex-col items-center gap-3 px-4">
        <div className="flex flex-col gap-1">
          <p>© {new Date().getFullYear()} Jacob Phillips, Aadya Maurya, Janelle Correia, Galav Sharma, Aarya Rajoju</p>
          <p className="text-gray-500">Licensed under the MIT License · Movie Munchers · For demo purposes only</p>
        </div>
        <div className="flex flex-col sm:flex-row sm:gap-6 gap-2 text-gray-500">
          <Link href="/about" className="hover:text-gray-800 transition underline-offset-2 hover:underline">About</Link>
          <Link href="/contact" className="hover:text-gray-800 transition underline-offset-2 hover:underline">Contact</Link>
          <Link href="/donate" className="hover:text-gray-800 transition underline-offset-2 hover:underline">Donations</Link>
        </div>
      </div>
    </footer>
  );
}
