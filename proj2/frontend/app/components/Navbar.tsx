"use client";

import Link from "next/link";

export default function Navbar() {
	return (
		<nav className="bg-gray-800 text-white">
			<div className="mx-auto max-w-6xl px-4 py-4">
				<div className="flex items-center justify-between">
					<div className="text-xl font-bold">Movie Munchers</div>
					<div className="flex space-x-6">
						<Link href="/" className="hover:text-gray-300">Home</Link>
						<Link href="/menu" className="hover:text-gray-300">Menu</Link>
						<Link href="/bundles" className="hover:text-gray-300">Bundles</Link>
						<Link href="/cart" className="hover:text-gray-300">Cart</Link>
					</div>
				</div>
			</div>
		</nav>
	);
}

