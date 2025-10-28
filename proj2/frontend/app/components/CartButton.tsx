"use client";

import Link from "next/link";
import { useState, useEffect } from "react";

export default function CartButton() {
	const [count, setCount] = useState<number>(0);

	useEffect(() => {
		try {
			const raw = localStorage.getItem("cartCount");
			if (raw) setCount(Number(raw));
		} catch (e) {
			// ignore (SSR or privacy)
		}
	}, []);

	return (
		<Link href="/cart" className="relative inline-flex items-center px-3 py-1 text-sm font-medium text-gray-700 hover:text-gray-900">
			🛒
			{count > 0 && (
				<span className="ml-2 inline-flex h-5 w-5 items-center justify-center rounded-full bg-red-600 text-xs text-white">
					{count}
				</span>
			)}
		</Link>
	);
}

