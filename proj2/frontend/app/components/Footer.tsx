import Link from "next/link";

export default function Footer() {
	return (
		<footer className="bg-gray-800 text-white mt-auto">
			<div className="mx-auto max-w-6xl px-4 py-6">
				<div className="flex justify-between items-center">
					<div>
						<h3 className="text-lg font-semibold">Movie Munchers</h3>
						<p className="text-sm text-gray-400">Snacks for every movie night</p>
					</div>
					<div className="flex space-x-6">
						<Link href="/about" className="hover:text-gray-300">About</Link>
						<Link href="/contact" className="hover:text-gray-300">Contact</Link>
						<Link href="/donate" className="hover:text-gray-300">Donate</Link>
					</div>
				</div>
				<div className="mt-4 text-center text-sm text-gray-400">
					© {new Date().getFullYear()} Movie Munchers. All rights reserved.
				</div>
			</div>
		</footer>
	);
}

