"use client";
import { useState, useEffect } from "react";
import Cookies from "js-cookie";

interface Driver {
    id: number;
    name: string;
    email: string;
    phone: string;
    total_deliveries: number;
    license_plate: string;
    vehicle_type: string;
    vehicle_color: string;
    duty_status: "available" | "unavailable" | "on_delivery";
}

interface Delivery {
    id: number;
    total_price: number;
    delivery_status:
        | "pending"
        | "accepted"
        | "in_progress"
        | "ready_for_pickup"
        | "in_transit"
        | "delivered"
        | "fulfilled"
        | "cancelled";
    delivery_time: string;
    address?: string;
    items?: { name: string; quantity: number }[];
}

export default function DriverDashboardPage() {
    const [driver, setDriver] = useState<Driver | null>(null);
    const [activeDelivery, setActiveDelivery] = useState<Delivery | null>(null);
    const [deliveryHistory, setDeliveryHistory] = useState<Delivery[]>([]);
    const [expanded, setExpanded] = useState({
        profile: true,
        activeDelivery: true,
        history: true,
    });
    const [vehicleForm, setVehicleForm] = useState({
        license_plate: "",
        vehicle_type: "",
        vehicle_color: "",
    });

    const driverId = Number(Cookies.get("user_id") || 0);

    const toggle = (section: "profile" | "activeDelivery" | "history") => {
        setExpanded((prev) => ({ ...prev, [section]: !prev[section] }));
    };

    const statusBadge = (text: string, type: "green" | "red" | "yellow") => {
        const colors: Record<string, string> = {
            green: "bg-green-100 text-green-700 border border-green-300",
            red: "bg-red-100 text-red-700 border border-red-300",
            yellow: "bg-yellow-100 text-yellow-700 border border-yellow-300",
        };
        return (
            <span
                className={`px-2 py-1 rounded-full font-medium ${colors[type]}`}
            >
                {text}
            </span>
        );
    };

    /** Fetch driver data + active + history */
    const fetchAllDriverData = async () => {
        try {
            const [driverRes, activeRes, historyRes] = await Promise.all([
                fetch(`http://localhost:5000/api/driver/${driverId}`),
                fetch(
                    `http://localhost:5000/api/driver/${driverId}/active-delivery`
                ),
                fetch(`http://localhost:5000/api/driver/${driverId}/history`),
            ]);

            const driverData = await driverRes.json();
            const activeData = await activeRes.json();
            const historyData = await historyRes.json();

            setDriver(driverData.driver);
            setVehicleForm({
                license_plate: driverData.driver.license_plate,
                vehicle_type: driverData.driver.vehicle_type,
                vehicle_color: driverData.driver.vehicle_color,
            });

            setActiveDelivery(activeData.active_delivery || null);
            setDeliveryHistory(historyData.history || []);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        if (driverId) fetchAllDriverData();
    }, [driverId]);

    /** Actions */
    const updateVehicleInfo = async () => {
        try {
            await fetch(`http://localhost:5000/api/driver/${driverId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(vehicleForm),
            });
            fetchAllDriverData(); // refetch to refresh display
        } catch (err) {
            console.error(err);
        }
    };

    const toggleDutyStatus = async () => {
        if (!driver) return;

        // Prevent status change if driver is on delivery
        if (driver.duty_status === "on_delivery") return;

        const newStatus =
            driver.duty_status === "available" ? "unavailable" : "available";

        try {
            await fetch(`http://localhost:5000/api/driver/${driverId}/status`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ new_status: newStatus }),
            });
            fetchAllDriverData(); // refetch after update
        } catch (err) {
            console.error(err);
        }
    };

    const completeDelivery = async (id: number) => {
        try {
            await fetch(`http://localhost:5000/api/deliveries/${id}/complete`, {
                method: "PUT",
            });
            await fetchAllDriverData(); // refetch everything to ensure accuracy
        } catch (err) {
            console.error(err);
        }
    };

    if (!driver) {
        return (
            <div className="flex justify-center items-center min-h-screen text-gray-500">
                Loading driver dashboard...
            </div>
        );
    }

    /** Status badge display logic */
    const dutyBadge = (() => {
        switch (driver.duty_status) {
            case "available":
                return statusBadge("Available", "green");
            case "unavailable":
                return statusBadge("Unavailable", "red");
            case "on_delivery":
                return statusBadge("On Delivery", "yellow");
            default:
                return statusBadge("Unknown", "red");
        }
    })();

    return (
        <section className="mx-auto max-w-6xl px-4 py-8 space-y-6">
            <div>
                <h1 className="text-3xl font-bold mb-2">Driver Dashboard</h1>
                <p className="text-gray-600">
                    Welcome, {driver.name} {dutyBadge}
                    <button
                        onClick={toggleDutyStatus}
                        disabled={driver.duty_status === "on_delivery"}
                        className={`ml-2 px-3 py-1 rounded font-medium transition ${
                            driver.duty_status === "available"
                                ? "bg-red-100 text-red-700 hover:bg-red-200"
                                : driver.duty_status === "unavailable"
                                ? "bg-green-100 text-green-700 hover:bg-green-200"
                                : "bg-gray-200 text-gray-500 cursor-not-allowed"
                        }`}
                    >
                        {driver.duty_status === "available"
                            ? "Change to Unavailable"
                            : driver.duty_status === "unavailable"
                            ? "Change to Available"
                            : "On Delivery"}
                    </button>
                </p>
            </div>

            {/* Active Delivery */}
            <div className="border rounded-lg shadow-lg p-6 bg-white">
                <button
                    onClick={() => toggle("activeDelivery")}
                    className="w-full text-left font-bold text-xl mb-4 text-gray-800 hover:text-blue-600 flex justify-between"
                >
                    Active Delivery {expanded.activeDelivery ? "▲" : "▼"}
                </button>
                {expanded.activeDelivery && (
                    <div className="space-y-4">
                        {activeDelivery ? (
                            <>
                                <div className="flex justify-between">
                                    <span className="font-semibold">
                                        Status:
                                    </span>
                                    {statusBadge(
                                        activeDelivery.delivery_status,
                                        activeDelivery.delivery_status ===
                                            "delivered" ||
                                            activeDelivery.delivery_status ===
                                                "fulfilled"
                                            ? "green"
                                            : "yellow"
                                    )}
                                </div>

                                <p>
                                    <span className="font-semibold">
                                        Address:
                                    </span>{" "}
                                    {activeDelivery.address}
                                </p>
                                <p>
                                    <span className="font-semibold">Time:</span>{" "}
                                    {new Date(
                                        activeDelivery.delivery_time
                                    ).toLocaleString()}
                                </p>

                                <ul className="list-disc ml-6 text-gray-600">
                                    {activeDelivery.items?.map((item, i) => (
                                        <li key={i}>
                                            {item.name} × {item.quantity}
                                        </li>
                                    ))}
                                </ul>

                                <p>
                                    <span className="font-semibold">
                                        Total:
                                    </span>{" "}
                                    ${activeDelivery.total_price.toFixed(2)}
                                </p>

                                {activeDelivery.delivery_status ===
                                    "accepted" && (
                                    <button
                                        onClick={() =>
                                            completeDelivery(activeDelivery.id)
                                        }
                                        className="mt-4 px-4 py-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200"
                                    >
                                        Mark as Completed
                                    </button>
                                )}
                            </>
                        ) : (
                            <p className="text-gray-500 italic">
                                No active delivery assigned.
                            </p>
                        )}
                    </div>
                )}
            </div>

            {/* Delivery History */}
            <div className="border rounded-lg shadow-lg p-6 bg-white">
                <button
                    onClick={() => toggle("history")}
                    className="w-full text-left font-bold text-xl mb-4 text-gray-800 hover:text-blue-600 flex justify-between"
                >
                    Delivery History {expanded.history ? "▲" : "▼"}
                </button>
                {expanded.history && (
                    <>
                        {deliveryHistory.length ? (
                            <div className="overflow-x-auto">
                                <table className="w-full border text-left">
                                    <thead className="bg-gray-100">
                                        <tr>
                                            <th className="border px-4 py-2">
                                                ID
                                            </th>
                                            <th className="border px-4 py-2">
                                                Status
                                            </th>
                                            <th className="border px-4 py-2">
                                                Price
                                            </th>
                                            <th className="border px-4 py-2">
                                                Time
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {deliveryHistory.map((d) => (
                                            <tr key={d.id} className="border-b">
                                                <td className="px-4 py-2">
                                                    {d.id}
                                                </td>
                                                <td className="px-4 py-2">
                                                    {statusBadge(
                                                        d.delivery_status,
                                                        d.delivery_status ===
                                                            "delivered" ||
                                                            d.delivery_status ===
                                                                "fulfilled"
                                                            ? "green"
                                                            : "yellow"
                                                    )}
                                                </td>
                                                <td className="px-4 py-2">
                                                    ${d.total_price.toFixed(2)}
                                                </td>
                                                <td className="px-4 py-2">
                                                    {new Date(
                                                        d.delivery_time
                                                    ).toLocaleString()}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        ) : (
                            <p className="text-gray-500 italic">
                                No completed deliveries yet.
                            </p>
                        )}
                    </>
                )}
            </div>

            {/* Profile & Vehicle Info */}
            <div className="border rounded-lg shadow-lg p-6 bg-white">
                <button
                    onClick={() => toggle("profile")}
                    className="w-full text-left font-bold text-xl mb-4 text-gray-800 hover:text-blue-600 flex justify-between"
                >
                    Profile & Vehicle Info {expanded.profile ? "▲" : "▼"}
                </button>
                {expanded.profile && (
                    <>
                        <p>
                            <strong>Email:</strong> {driver.email}
                        </p>
                        <p>
                            <strong>Phone:</strong> {driver.phone}
                        </p>
                        <p>
                            <strong>Total Deliveries:</strong>{" "}
                            {driver.total_deliveries}
                        </p>

                        <div className="mt-4 space-y-2">
                            <input
                                type="text"
                                value={vehicleForm.license_plate}
                                onChange={(e) =>
                                    setVehicleForm({
                                        ...vehicleForm,
                                        license_plate: e.target.value,
                                    })
                                }
                                className="border px-3 py-2 rounded w-full"
                                placeholder="License Plate"
                            />
                            <select
                                value={vehicleForm.vehicle_type}
                                onChange={(e) =>
                                    setVehicleForm({
                                        ...vehicleForm,
                                        vehicle_type: e.target.value,
                                    })
                                }
                                className="border px-3 py-2 rounded w-full"
                            >
                                <option value="car">Car</option>
                                <option value="bike">Bike</option>
                                <option value="scooter">Scooter</option>
                                <option value="other">Other</option>
                            </select>
                            <input
                                type="text"
                                value={vehicleForm.vehicle_color}
                                onChange={(e) =>
                                    setVehicleForm({
                                        ...vehicleForm,
                                        vehicle_color: e.target.value,
                                    })
                                }
                                className="border px-3 py-2 rounded w-full"
                                placeholder="Vehicle Color"
                            />
                            <button
                                onClick={updateVehicleInfo}
                                className="px-4 py-2 bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                            >
                                Save Vehicle Info
                            </button>
                        </div>
                    </>
                )}
            </div>
        </section>
    );
}
