"use client";

import { useState } from "react";
import { MenuItem } from "../../lib/sampleData";

export default function BundleBuilder() {
	const [items, setItems] = useState<MenuItem[]>([]);

	return (
		<div className="rounded border p-4">
			<p className="text-sm text-gray-600 mb-2">(Bundle builder placeholder)</p>
			<div className="text-sm">Selected: {items.length} items</div>
		</div>
	);
}

