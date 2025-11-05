"use client";
import Link from "next/link";
import { useCartStore } from "@/lib/cartStore";

export default function CartPage() {
	const items = useCartStore((s) => s.items);
	const add = useCartStore((s) => s.add);
	const decrement = useCartStore((s) => s.decrement);
	const remove = useCartStore((s) => s.remove);
	const clear = useCartStore((s) => s.clear);

	const subtotal = items.reduce((sum, it) => sum + it.price * it.qty, 0);

	return (
		<section className="mx-auto mt-10 max-w-3xl">
			<h1 className="mb-2 text-2xl font-bold">Your Cart</h1>
			<p className="mb-6 text-sm text-gray-600">Review items before checkout.</p>

			{items.length === 0 ? (
				<div className="rounded-2xl border p-6 text-center">
					<p className="mb-4">Your cart is empty.</p>
					<Link
						href="/order"
						className="rounded-xl bg-black px-5 py-2 text-sm text-white hover:bg-gray-800 transition"
					>
						Back to Ordering
					</Link>
				</div>
			) : (
				<div className="space-y-4">
					<ul className="divide-y rounded-2xl border">
						{items.map((it) => (
							<li key={it.id} className="flex items-center justify-between p-4">
								<div>
									<p className="font-medium">{it.name}</p>
									<p className="text-sm text-gray-600">${it.price.toFixed(2)} each</p>
								</div>

								<div className="flex items-center gap-3">
									<button
										aria-label={`Decrease ${it.name}`}
										className="h-8 w-8 rounded-lg border text-sm hover:bg-gray-100"
										onClick={() => decrement(it.id, 1)}
									>
										−
									</button>
									<span className="w-6 text-center">{it.qty}</span>
									<button
										aria-label={`Increase ${it.name}`}
										className="h-8 w-8 rounded-lg border text-sm hover:bg-gray-100"
										onClick={() => add({ id: it.id, name: it.name, price: it.price }, 1)}
									>
										+
									</button>

									<span className="ml-4 w-20 text-right font-medium">
										${(it.price * it.qty).toFixed(2)}
									</span>

									<button
										aria-label={`Remove ${it.name}`}
										className="ml-4 rounded-lg border px-3 py-1 text-xs hover:bg-gray-100"
										onClick={() => remove(it.id)}
									>
										Remove
									</button>
								</div>
							</li>
						))}
					</ul>

					<div className="flex items-center justify-between rounded-2xl border p-4">
						<button
							className="rounded-xl border px-4 py-2 text-sm hover:bg-gray-100"
							onClick={clear}
						>
							Clear Cart
						</button>
						<div className="text-right">
							<p className="text-sm text-gray-600">Subtotal</p>
							<p className="text-xl font-semibold">${subtotal.toFixed(2)}</p>
						</div>
					</div>

					<div className="flex items-center justify-end gap-3">
						<Link
							href="/order"
							className="rounded-xl border border-gray-300 px-5 py-2 text-sm hover:bg-gray-100 transition"
						>
							Continue Shopping
						</Link>
						<Link
							href="/checkout"
							className="rounded-xl bg-black px-5 py-2 text-sm text-white hover:bg-gray-800 transition"
						>
							Proceed to Checkout
						</Link>
					</div>
				</div>
			)}
		</section>
	);
}

