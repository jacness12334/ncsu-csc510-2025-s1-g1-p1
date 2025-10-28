import Link from "next/link";
import { MenuItem } from "../../lib/sampleData";

export default function MenuCard({ item }: { item: MenuItem }) {
	return (
		<article className="rounded border p-4 shadow-sm">
			<div className="mb-2 font-semibold">{item.name}</div>
			<div className="text-sm text-gray-600 mb-3">{item.description}</div>
			<div className="flex items-center justify-between">
				<div className="font-medium">${item.price.toFixed(2)}</div>
				<Link href={`/menu/${item.id}`} className="text-sm text-blue-600">
					View
				</Link>
			</div>
		</article>
	);
}

