interface Props {
	params: { orderId: string };
}

export default function OrderPage({ params }: Props) {
	return (
		<div className="py-8">
			<h1 className="text-2xl font-bold">Order {params.orderId}</h1>
			<p className="mt-4 text-gray-600">Tracking details will appear here.</p>
		</div>
	);
}

