"use client";
import { useState, useEffect } from "react";
import Cookies from "js-cookie";
import { useRouter } from "next/navigation";

interface Theatre {
    id: number;
    name: string;
    address?: string;
    phone?: string;
    is_open: boolean;
}

interface Staff {
    user_id: number;
    name: string;
    role: "admin" | "runner";
    theatre_id: number;
    is_available: boolean;
}

interface Delivery {
    id: number;
    productName: string;
    theatreName: string;
    quantity: number;
    delivery_status:
        | "pending"
        | "accepted"
        | "in_progress"
        | "ready_for_pickup"
        | "in_transit"
        | "delivered"
        | "fulfilled"
        | "cancelled";
}

export default function StaffPage() {
    const router = useRouter();
    const [role, setRole] = useState<"admin" | "runner" | null>(null);
    const [theatres, setTheatres] = useState<Theatre[]>([]);
    const [staff, setStaff] = useState<Staff[]>([]);
    const [deliveries, setDeliveries] = useState<Delivery[]>([]);
    const [expanded, setExpanded] = useState({
        theatres: true,
        staff: true,
        deliveries: true,
    });
    const [loading, setLoading] = useState(true);
    const [showAddForm, setShowAddForm] = useState(false);
    const [newStaff, setNewStaff] = useState({
        name: "",
        email: "",
        phone: "",
        birthday: "",
        password: "",
        role: "runner" as "runner" | "admin",
        theatre_id: theatres[0]?.id || 0,
    });

    const userId = Number(Cookies.get("user_id") || 0);

    const toggle = (section: "theatres" | "staff" | "deliveries") => {
        setExpanded((prev) => ({ ...prev, [section]: !prev[section] }));
    };

    /** Authentication check + fetch all data */
    useEffect(() => {
        const fetchData = async () => {
            if (!userId) return;

            try {
                const staffRes = await fetch(
                    `http://localhost:5000/api/staff/${userId}`
                );
                if (!staffRes.ok)
                    throw new Error("Failed to get staff details");
                const staffInfo = await staffRes.json();
                if (!staffInfo || !staffInfo.role) return;
                setRole(staffInfo.role);

                const theatreRes = await fetch(
                    `http://localhost:5000/api/theatres/${userId}`
                );
                const theatreData = await theatreRes.json();
                setTheatres(theatreData.theatres || []);

                const staffList: Staff[] = [];
                if (staffInfo.role === "admin") {
                    for (const theatre of theatreData.theatres || []) {
                        const res = await fetch(
                            `http://localhost:5000/api/staff/list/${theatre.id}`,
                            {
                                method: "PUT",
                                headers: { "Content-Type": "application/json" },
                                body: JSON.stringify({ user_id: userId }),
                            }
                        );
                        const data = await res.json();

                        for (const s of data.staff || []) {
                            try {
                                const userRes = await fetch(
                                    `http://localhost:5000/api/users/${s.user_id}`
                                );
                                const userData = await userRes.json();
                                staffList.push({
                                    ...s,
                                    name: userData.name || "Unnamed",
                                });
                            } catch {
                                staffList.push({ ...s, name: "Unknown" });
                            }
                        }
                    }
                }
                setStaff(staffList);

                const deliveryList: Delivery[] = [];
                for (const theatre of theatreData.theatres || []) {
                    const res = await fetch(
                        `http://localhost:5000/api/deliveries/list/${theatre.id}`
                    );
                    const data = await res.json();
                    deliveryList.push(
                        ...(data.deliveries || []).map((d: any) => ({
                            id: d.id,
                            productName: "Order",
                            theatreName: theatre.name,
                            quantity: 1,
                            delivery_status: d.delivery_status,
                        }))
                    );
                }
                console.log(deliveryList);
                setDeliveries(deliveryList);
            } catch (err) {
                console.error("Error fetching data:", err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [userId, router]);

    /** Theatre actions */
    const toggleTheatreStatus = async (id: number) => {
        try {
            const theatre = theatres.find((t) => t.id === id);
            if (!theatre) return;

            await fetch(`http://localhost:5000/api/theatres`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: userId,
                    theatre_id: id,
                    is_open: !theatre.is_open,
                }),
            });

            setTheatres((prev) =>
                prev.map((t) =>
                    t.id === id ? { ...t, is_open: !t.is_open } : t
                )
            );
        } catch (err) {
            console.error(err);
        }
    };

    /** Staff actions */
    const addStaff = async () => {
        try {
            if (!theatres.length) return;
            const res = await fetch(`http://localhost:5000/api/staff`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: userId,
                    name: "New Staff",
                    email: "newstaff@example.com",
                    phone: "1234567890",
                    birthday: "2000-01-01",
                    password: "password123",
                    theatre_id: theatres[0].id,
                    role: "runner",
                }),
            });
            const data = await res.json();
            if (data.user_id) {
                setStaff((prev) => [
                    ...prev,
                    {
                        user_id: data.user_id,
                        name: "New Staff",
                        role: "runner",
                        theatre_id: theatres[0].id,
                        is_available: true,
                    },
                ]);
            }
        } catch (err) {
            console.error(err);
        }
    };

    const removeStaff = async (staffUserId: number) => {
        try {
            await fetch(`http://localhost:5000/api/staff/${staffUserId}`, {
                method: "DELETE",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId }),
            });
            setStaff((prev) => prev.filter((s) => s.user_id !== staffUserId));
        } catch (err) {
            console.error(err);
        }
    };

    /** Delivery actions */
    const acceptDelivery = async (id: number) => {
        try {
            await fetch(`http://localhost:5000/api/deliveries/${id}/accept`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId }),
            });
            setDeliveries((prev) =>
                prev.map((d) =>
                    d.id === id ? { ...d, delivery_status: "accepted" } : d
                )
            );
        } catch (err) {
            console.error(err);
        }
    };

    const fulfillDelivery = async (id: number) => {
        try {
            await fetch(`http://localhost:5000/api/deliveries/${id}/fulfill`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId }),
            });
            setDeliveries((prev) =>
                prev.map((d) =>
                    d.id === id ? { ...d, delivery_status: "fulfilled" } : d
                )
            );
        } catch (err) {
            console.error(err);
        }
    };

    /** Status badge helper */
    const statusBadge = (
        text: string,
        type:
            | "green"
            | "red"
            | "gray"
            | "blue"
            | "yellow"
            | "orange"
            | "purple"
            | "pink"
    ) => {
        const colors: Record<string, string> = {
            green: "bg-green-100 text-green-700 border border-green-300",
            red: "bg-red-100 text-red-700 border border-red-300",
            gray: "bg-gray-100 text-gray-700 border border-gray-300",
            blue: "bg-blue-100 text-blue-700 border border-blue-300",
            yellow: "bg-yellow-100 text-yellow-700 border border-yellow-300",
            orange: "bg-orange-100 text-orange-700 border border-orange-300",
            purple: "bg-purple-100 text-purple-700 border border-purple-300",
            pink: "bg-pink-100 text-pink-700 border border-pink-300",
        };
        return (
            <span
                className={`px-2 py-1 rounded-full font-medium ${colors[type]}`}
            >
                {text}
            </span>
        );
    };

    /** UI Rendering */
    if (loading) {
        return (
            <div className="flex justify-center items-center min-h-screen text-lg text-gray-500">
                Loading staff dashboard...
            </div>
        );
    }

    if (!role) {
        return (
            <div className="flex justify-center items-center min-h-screen text-red-500">
                Unauthorized – Please log in as staff.
            </div>
        );
    }

    return (
        <section className="mx-auto max-w-6xl px-4 py-8 space-y-6">
            <div>
                <h1 className="text-3xl font-bold mb-2">Staff Dashboard</h1>
                <p className="text-gray-600">Welcome, {role.toUpperCase()}</p>
            </div>

            {/* Theatres */}
            <div className="border rounded shadow-sm p-4 bg-white">
                <button
                    onClick={() => toggle("theatres")}
                    className="w-full text-left font-semibold text-lg mb-3 hover:text-blue-600 transition"
                >
                    Theatres {expanded.theatres ? "▲" : "▼"}
                </button>
                {expanded.theatres && (
                    <ul className="space-y-2">
                        {theatres.map((t) => (
                            <li
                                key={t.id}
                                className="flex justify-between items-center border-b py-2"
                            >
                                <span>
                                    {t.name}{" "}
                                    <span className="text-sm text-gray-500">
                                        {t.address}
                                    </span>
                                </span>
                                <div className="flex items-center gap-2">
                                    {statusBadge(
                                        t.is_open ? "Open" : "Closed",
                                        t.is_open ? "green" : "red"
                                    )}
                                    {role === "admin" && (
                                        <button
                                            onClick={() =>
                                                toggleTheatreStatus(t.id)
                                            }
                                            className={`px-3 py-1 rounded font-medium transition ${
                                                t.is_open
                                                    ? "bg-red-100 text-red-700 hover:bg-red-200 active:bg-red-300"
                                                    : "bg-green-100 text-green-700 hover:bg-green-200 active:bg-green-300"
                                            }`}
                                        >
                                            {t.is_open ? "Close" : "Open"}
                                        </button>
                                    )}
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </div>

            {/* Staff (admin only) */}
            {role === "admin" && (
                <div className="border rounded shadow-sm p-4 bg-white">
                    <button
                        onClick={() => toggle("staff")}
                        className="w-full text-left font-semibold text-lg mb-3 hover:text-blue-600 transition"
                    >
                        Staff {expanded.staff ? "▲" : "▼"}
                    </button>
                    {expanded.staff && (
                        <div className="space-y-2">
                            {!showAddForm ? (
                                <button
                                    onClick={() => setShowAddForm(true)}
                                    className="mb-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 active:bg-blue-800 transition"
                                >
                                    Add Staff
                                </button>
                            ) : (
                                <form
                                    onSubmit={async (e) => {
                                        e.preventDefault();
                                        try {
                                            const res = await fetch(
                                                `http://localhost:5000/api/staff`,
                                                {
                                                    method: "POST",
                                                    headers: {
                                                        "Content-Type":
                                                            "application/json",
                                                    },
                                                    body: JSON.stringify({
                                                        user_id: userId,
                                                        ...newStaff,
                                                    }),
                                                }
                                            );
                                            const data = await res.json();
                                            if (data.user_id) {
                                                setStaff((prev) => [
                                                    ...prev,
                                                    {
                                                        user_id: data.user_id,
                                                        name: newStaff.name,
                                                        role: newStaff.role,
                                                        theatre_id:
                                                            newStaff.theatre_id,
                                                        is_available: true,
                                                    },
                                                ]);
                                                setShowAddForm(false);
                                                setNewStaff({
                                                    name: "",
                                                    email: "",
                                                    phone: "",
                                                    birthday: "",
                                                    password: "",
                                                    role: "runner",
                                                    theatre_id:
                                                        theatres[0]?.id || 0,
                                                });
                                            }
                                        } catch (err) {
                                            console.error(err);
                                        }
                                    }}
                                    className="border p-4 rounded bg-gray-50 space-y-3"
                                >
                                    <div className="grid grid-cols-2 gap-3">
                                        <input
                                            type="text"
                                            placeholder="Full Name"
                                            value={newStaff.name}
                                            onChange={(e) =>
                                                setNewStaff((p) => ({
                                                    ...p,
                                                    name: e.target.value,
                                                }))
                                            }
                                            className="border rounded px-3 py-2 w-full"
                                            required
                                        />
                                        <input
                                            type="email"
                                            placeholder="Email"
                                            value={newStaff.email}
                                            onChange={(e) =>
                                                setNewStaff((p) => ({
                                                    ...p,
                                                    email: e.target.value,
                                                }))
                                            }
                                            className="border rounded px-3 py-2 w-full"
                                            required
                                        />
                                        <input
                                            type="text"
                                            placeholder="Phone"
                                            value={newStaff.phone}
                                            onChange={(e) =>
                                                setNewStaff((p) => ({
                                                    ...p,
                                                    phone: e.target.value,
                                                }))
                                            }
                                            className="border rounded px-3 py-2 w-full"
                                        />
                                        <input
                                            type="date"
                                            value={newStaff.birthday}
                                            onChange={(e) =>
                                                setNewStaff((p) => ({
                                                    ...p,
                                                    birthday: e.target.value,
                                                }))
                                            }
                                            className="border rounded px-3 py-2 w-full"
                                        />
                                        <input
                                            type="password"
                                            placeholder="Password"
                                            value={newStaff.password}
                                            onChange={(e) =>
                                                setNewStaff((p) => ({
                                                    ...p,
                                                    password: e.target.value,
                                                }))
                                            }
                                            className="border rounded px-3 py-2 w-full"
                                            required
                                        />
                                        <select
                                            value={newStaff.role}
                                            onChange={(e) =>
                                                setNewStaff((p) => ({
                                                    ...p,
                                                    role: e.target.value as
                                                        | "admin"
                                                        | "runner",
                                                }))
                                            }
                                            className="border rounded px-3 py-2 w-full"
                                        >
                                            <option value="runner">
                                                Runner
                                            </option>
                                            <option value="admin">Admin</option>
                                        </select>
                                        <select
                                            value={newStaff.theatre_id}
                                            onChange={(e) =>
                                                setNewStaff((p) => ({
                                                    ...p,
                                                    theatre_id: Number(
                                                        e.target.value
                                                    ),
                                                }))
                                            }
                                            className="border rounded px-3 py-2 w-full col-span-2"
                                        >
                                            <option value={0}>
                                                Select Theatre
                                            </option>
                                            {theatres.map((t) => (
                                                <option key={t.id} value={t.id}>
                                                    {t.name}
                                                </option>
                                            ))}
                                        </select>
                                    </div>
                                    <div className="flex justify-end gap-2">
                                        <button
                                            type="button"
                                            onClick={() =>
                                                setShowAddForm(false)
                                            }
                                            className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
                                        >
                                            Cancel
                                        </button>
                                        <button
                                            type="submit"
                                            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                                        >
                                            Save Staff
                                        </button>
                                    </div>
                                </form>
                            )}
                            <ul className="space-y-2">
                                {staff.map((s) => (
                                    <li
                                        key={s.user_id}
                                        className="flex justify-between items-center border-b py-2"
                                    >
                                        <span>
                                            {s.name} ({s.role}) — Theatre{" "}
                                            {s.theatre_id}
                                        </span>
                                        <div className="flex items-center gap-2">
                                            {statusBadge(
                                                s.is_available
                                                    ? "Available"
                                                    : "Busy",
                                                s.is_available
                                                    ? "green"
                                                    : "gray"
                                            )}
                                            <button
                                                onClick={() =>
                                                    removeStaff(s.user_id)
                                                }
                                                className="px-3 py-1 bg-red-100 text-red-700 rounded hover:bg-red-200 active:bg-red-300 transition"
                                            >
                                                Remove
                                            </button>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            )}

            {/* Deliveries */}
            <div className="border rounded shadow-sm p-4 bg-white">
                <button
                    onClick={() => toggle("deliveries")}
                    className="w-full text-left font-semibold text-lg mb-3 hover:text-blue-600 transition"
                >
                    Deliveries {expanded.deliveries ? "▲" : "▼"}
                </button>
                {expanded.deliveries && (
                    <ul className="space-y-2">
                        {deliveries.map((d) => {
                            let badgeColor: any = "gray";
                            switch (d.delivery_status) {
                                case "pending":
                                    badgeColor = "gray";
                                    break;
                                case "accepted":
                                    badgeColor = "blue";
                                    break;
                                case "in_progress":
                                    badgeColor = "purple";
                                    break;
                                case "ready_for_pickup":
                                    badgeColor = "orange";
                                    break;
                                case "in_transit":
                                    badgeColor = "pink";
                                    break;
                                case "delivered":
                                    badgeColor = "yellow";
                                    break;
                                case "fulfilled":
                                    badgeColor = "green";
                                    break;
                                case "cancelled":
                                    badgeColor = "red";
                                    break;
                            }

                            return (
                                <li
                                    key={d.id}
                                    className="flex justify-between items-center border-b py-2"
                                >
                                    <span>
                                        {d.productName} → {d.theatreName} (Qty:{" "}
                                        {d.quantity})
                                    </span>
                                    <div className="flex items-center gap-2">
                                        {statusBadge(
                                            d.delivery_status,
                                            badgeColor
                                        )}
                                        {(role === "admin" ||
                                            role === "runner") &&
                                            d.delivery_status === "pending" && (
                                                <button
                                                    onClick={() =>
                                                        acceptDelivery(d.id)
                                                    }
                                                    className="px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 active:bg-blue-300 transition"
                                                >
                                                    Accept
                                                </button>
                                            )}
                                        {(role === "admin" ||
                                            role === "runner") &&
                                            d.delivery_status ===
                                                "delivered" && (
                                                <button
                                                    onClick={() =>
                                                        fulfillDelivery(d.id)
                                                    }
                                                    className="px-3 py-1 bg-green-100 text-green-700 rounded hover:bg-green-200 active:bg-green-300 transition"
                                                >
                                                    Fulfill
                                                </button>
                                            )}
                                    </div>
                                </li>
                            );
                        })}
                    </ul>
                )}
            </div>
        </section>
    );
}
