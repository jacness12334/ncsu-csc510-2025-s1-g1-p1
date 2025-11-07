"use client";
import { useState, FormEvent, useEffect } from "react";
import { useRouter } from 'next/navigation';

type PaymentMethod = {
  id: string;
  cardNumber: string;
  expirationMonth: string;
  expirationYear: string;
  billingAddress: string;
  isDefault: boolean;
};

type jsonPaymentMethodRecieveType = {
  billing_address: string;
  id: string;
  card_number: string;
  expiration_month: string;
  expiration_year: string;
  is_default: boolean;
};

export default function EditDetailsPage() {
  const router = useRouter();
  // Original values (simulate fetched from backend)
  const [originalName, setOriginalName] = useState("");
  const [originalEmail, setOriginalEmail] = useState("");
  const [originalPhone, setOriginalPhone] = useState("");
  const [originalBirthday, setOriginalBirthday] = useState("");
  const [originalTheatreId, setOriginalTheatreId] = useState("");
  const [userId, setUserId] = useState("");
  const [userType, setUserType] = useState("");

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [birthday, setBirthday] = useState("");
  const [TheatreId, setTheatreId] = useState("");

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");

  // Payment methods state and handlers
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([]);
  const [showAddPayment, setShowAddPayment] = useState(false);
  const [editingPaymentId, setEditingPaymentId] = useState<string | null>(null);

  const [newCardNumber, setNewCardNumber] = useState("");
  const [newExpMonth, setNewExpMonth] = useState("");
  const [newExpYear, setNewExpYear] = useState("");
  const [newBillingAddress, setNewBillingAddress] = useState("");

  const deleteUser = async () => {

    try {

      if (userType != 'customer') {
        throw new Error("Not implemented yet");
      }

      const response = await fetch("http://localhost:5000/api/customers/" + userId, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include"
      });

      if (!response.ok) {
        // If server responds with 400/500 code, get the specific message
        const errorData = await response.json();
        throw new Error(errorData.message || response.statusText);
      }

      // Success path:
      // setCookie('sessionToken', '', 1);
      alert("User successfully deleted");
      router.push("/");

    } catch (error: unknown) {
      // This catches network errors AND the error thrown above
      console.error(error);
      alert("Error: " + (error instanceof Error ? error.message : String(error)));
    }
  }

  const handleAddPayment = async () => {
    if (!newCardNumber || !newExpMonth || !newExpYear || !newBillingAddress) {
      alert("Please fill in all payment fields.");
      return;
    }

    const response = await fetch("http://localhost:5000/api/customers/" + userId + "/payment-methods", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        card_number: newCardNumber,
        expiration_month: newExpMonth,
        expiration_year: newExpYear,
        billing_address: newBillingAddress
      }),
      credentials: "include"
    });

    if (!response.ok) {
      // If server responds with 400/500 code, get the specific message
      const errorData = await response.json();
      console.log(response);
      alert(errorData.message || response.statusText);
      throw new Error(errorData.message || response.statusText);

    }

    const rt = await response.json();

    // Success path:
    const newPaymentMethod: PaymentMethod = {
      id: rt.id,
      cardNumber: newCardNumber,
      expirationMonth: newExpMonth,
      expirationYear: newExpYear,
      billingAddress: newBillingAddress,
      isDefault: paymentMethods.length === 0,
    };
    setPaymentMethods([...paymentMethods, newPaymentMethod]);
    setNewCardNumber("");
    setNewExpMonth("");
    setNewExpYear("");
    setNewBillingAddress("");
    setShowAddPayment(false);
  };

  const handleEditPayment = async (id: string) => {

    const method = paymentMethods.find((m) => m.id === id);
    if (method) {
      setNewCardNumber(method.cardNumber);
      setNewExpMonth(method.expirationMonth);
      setNewExpYear(method.expirationYear);
      setNewBillingAddress(method.billingAddress);
      setEditingPaymentId(id);
      setShowAddPayment(true);
    }

    let response = await fetch("http://localhost:5000/api/customers/" + userId + "/payment-methods", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        cart_item_id: id
      }),
      credentials: "include"
    });

    if (!response.ok) {
      // If server responds with 400/500 code, get the specific message
      const errorData = await response.json();
      console.log(response);
      alert(errorData.message || response.statusText);
      throw new Error(errorData.message || response.statusText);

    }

    let rt = await response.json();

    response = await fetch("http://localhost:5000/api/customers/" + userId + "/payment-methods", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        cart_item_id: id
      }),
      credentials: "include"
    });

    if (!response.ok) {
      // If server responds with 400/500 code, get the specific message
      const errorData = await response.json();
      console.log(response);
      alert(errorData.message || response.statusText);
      throw new Error(errorData.message || response.statusText);

    }

    rt = await response.json();

    // Success path:
    const newPaymentMethod: PaymentMethod = {
      id: rt.id,
      cardNumber: newCardNumber,
      expirationMonth: newExpMonth,
      expirationYear: newExpYear,
      billingAddress: newBillingAddress,
      isDefault: paymentMethods.length === 0,
    };
    setPaymentMethods([...paymentMethods, newPaymentMethod]);
    setNewCardNumber("");
    setNewExpMonth("");
    setNewExpYear("");
    setNewBillingAddress("");
    setShowAddPayment(false);

  };

  const handleSaveEditPayment = () => {
    if (!newCardNumber || !newExpMonth || !newExpYear || !newBillingAddress) {
      alert("Please fill in all payment fields.");
      return;
    }
    setPaymentMethods(
      paymentMethods.map((m) =>
        m.id === editingPaymentId
          ? {
            ...m,
            cardNumber: newCardNumber,
            expirationMonth: newExpMonth,
            expirationYear: newExpYear,
            billingAddress: newBillingAddress,
          }
          : m
      )
    );
    setNewCardNumber("");
    setNewExpMonth("");
    setNewExpYear("");
    setNewBillingAddress("");
    setEditingPaymentId(null);
    setShowAddPayment(false);
  };

  const handleDeletePayment = (id: string) => {
    setPaymentMethods(paymentMethods.filter((m) => m.id !== id));
  };

  const handleSetDefault = (id: string) => {
    setPaymentMethods(
      paymentMethods.map((m) => ({ ...m, isDefault: m.id === id }))
    );
  };

  useEffect(() => {
    const f = async () => {
      try {
        let response = await fetch("http://localhost:5000/api/users/me", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include"
        });

        if (!response.ok) {
          // If server responds with 400/500 code, get the specific message
          const errorData = await response.json();
          throw new Error(errorData.message || response.statusText);
        }

        let rt = await response.json();
        console.log(rt);

        // Success path:
        setOriginalBirthday(rt.birthday);
        setOriginalEmail(rt.email);
        setOriginalName(rt.name);
        setOriginalPhone(rt.phone);
        setUserId(rt.user_id);
        setBirthday(rt.birthday);
        setEmail(rt.email);
        setName(rt.name);
        setPhone(rt.phone);
        setUserType(rt.role);

        const user_id = rt.user_id;

        response = await fetch("http://localhost:5000/api/customers/" + user_id, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include"
        });

        if (!response.ok) {
          // If server responds with 400/500 code, get the specific message
          const errorData = await response.json();
          throw new Error(errorData.message || response.statusText);
        }

        rt = await response.json();
        console.log(rt);
        setTheatreId(rt.default_theatre_id);
        setOriginalTheatreId(rt.default_theatre_id);

        response = await fetch("http://localhost:5000/api/customers/" + rt.user_id + "/payment-methods", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include"
        });

        if (!response.ok) {
          // If server responds with 400/500 code, get the specific message
          const errorData = await response.json();
          throw new Error(errorData.message || response.statusText);
        }

        rt = await response.json();
        console.log(rt.payment_methods);
        setPaymentMethods(rt.payment_methods.map((item: jsonPaymentMethodRecieveType, index: number) => {
          return {
            id: item.id,
            cardNumber: item.card_number,
            expirationMonth: item.expiration_month,
            expirationYear: item.expiration_year,
            billingAddress: item.billing_address,
            isDefault: item.is_default

          }
        }));

      } catch (error: unknown) {
        // This catches network errors AND the error thrown above
        console.error(error);
        alert("Error: " + (error instanceof Error ? error.message : String(error)));
      }
    }
    f();

  }, []);

  // Check if any form fields have changed
  const hasChanges =
    name !== originalName ||
    email !== originalEmail ||
    phone !== originalPhone ||
    birthday !== originalBirthday ||
    TheatreId !== originalTheatreId ||
    currentPassword !== "" ||
    newPassword !== "" ||
    confirmNewPassword !== "";

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (newPassword || confirmNewPassword) {
      if (newPassword.length < 8) {
        alert("New password must be at least 8 characters.");
        return;
      }
      if (newPassword !== confirmNewPassword) {
        alert("New passwords do not match.");
        return;
      }
    }
    console.log({
      name, email, phone, birthday,
      TheatreId
    });
    alert("Details saved (placeholder). Backend integration to be added.");
  };



  return (
    <section className="mx-auto mt-10 max-w-2xl">
      <h1 className="mb-2 text-2xl font-bold">Edit Details</h1>
      <p className="mb-6 text-sm text-gray-600">Update your account and preferences.</p>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <label htmlFor="name" className="mb-1 block text-sm font-medium">Full Name</label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              placeholder="Jane Doe"
              className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
            />
          </div>
          <div>
            <label htmlFor="email" className="mb-1 block text-sm font-medium">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="you@example.com"
              className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
            />
          </div>
          <div>
            <label htmlFor="phone" className="mb-1 block text-sm font-medium">Phone</label>
            <input
              id="phone"
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              required
              placeholder="(555) 123-4567"
              className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
            />
          </div>
          <div>
            <label htmlFor="birthday" className="mb-1 block text-sm font-medium">Birthday</label>
            <input
              id="birthday"
              type="date"
              value={birthday}
              onChange={(e) => setBirthday(e.target.value)}
              required
              className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
            />
          </div>
        </div>

        <div>
          <label htmlFor="defaultTheatre" className="mb-1 block text-sm font-medium">Default Theatre</label>
          <input
            id="defaultTheatre"
            value={TheatreId}
            onChange={(e) => setTheatreId(e.target.value)}
            className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
          >
          </input>
        </div>

        <fieldset className="rounded-2xl border p-4">
          <legend className="px-2 text-sm font-semibold">Change Password (optional)</legend>
          <div className="grid gap-4 sm:grid-cols-3">
            <div>
              <label htmlFor="currentPassword" className="mb-1 block text-sm font-medium">Current</label>
              <input
                id="currentPassword"
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>
            <div>
              <label htmlFor="newPassword" className="mb-1 block text-sm font-medium">New</label>
              <input
                id="newPassword"
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="••••••••"
                minLength={8}
                className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>
            <div>
              <label htmlFor="confirmNewPassword" className="mb-1 block text-sm font-medium">Confirm</label>
              <input
                id="confirmNewPassword"
                type="password"
                value={confirmNewPassword}
                onChange={(e) => setConfirmNewPassword(e.target.value)}
                placeholder="••••••••"
                minLength={8}
                className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>
          </div>
        </fieldset>

        <fieldset className="rounded-2xl border p-4">
          <legend className="px-2 text-sm font-semibold">Payment Methods</legend>
          <div className="space-y-3">
            {paymentMethods.map((method) => (
              <div
                key={method.id}
                className="flex items-center justify-between rounded-lg border p-3"
              >
                <div>
                  <p className="text-sm font-medium">
                    •••• •••• •••• {method.cardNumber.slice(-4)}
                    {method.isDefault && (
                      <span className="ml-2 text-xs text-green-600">(Default)</span>
                    )}
                  </p>
                  <p className="text-xs text-gray-600">
                    Exp: {method.expirationMonth}/{method.expirationYear}
                  </p>
                  <p className="text-xs text-gray-600">{method.billingAddress}</p>
                </div>
                <div className="flex gap-2">
                  {!method.isDefault && (
                    <button
                      type="button"
                      onClick={() => handleSetDefault(method.id)}
                      className="text-xs text-blue-600 hover:underline"
                    >
                      Set Default
                    </button>
                  )}
                  <button
                    type="button"
                    onClick={() => handleEditPayment(method.id)}
                    className="text-xs text-gray-600 hover:underline"
                  >
                    Edit
                  </button>
                  <button
                    type="button"
                    onClick={() => handleDeletePayment(method.id)}
                    className="text-xs text-red-600 hover:underline"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}

            {!showAddPayment ? (
              <button
                type="button"
                onClick={() => setShowAddPayment(true)}
                className="w-full rounded-lg border border-dashed border-gray-300 px-4 py-2 text-sm text-gray-600 hover:bg-gray-50 transition"
              >
                + Add Payment Method
              </button>
            ) : (
              <div className="space-y-3 rounded-lg border-2 border-blue-200 bg-blue-50 p-4">
                <p className="text-sm font-medium">
                  {editingPaymentId ? "Edit Payment Method" : "New Payment Method"}
                </p>
                <div>
                  <label className="mb-1 block text-xs font-medium">Card Number</label>
                  <input
                    type="text"
                    value={newCardNumber}
                    onChange={(e) => setNewCardNumber(e.target.value)}
                    placeholder="1234 5678 9012 3456"
                    maxLength={16}
                    className="w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
                  />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="mb-1 block text-xs font-medium">Exp. Month</label>
                    <input
                      type="text"
                      value={newExpMonth}
                      onChange={(e) => setNewExpMonth(e.target.value)}
                      placeholder="MM"
                      maxLength={2}
                      className="w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
                    />
                  </div>
                  <div>
                    <label className="mb-1 block text-xs font-medium">Exp. Year</label>
                    <input
                      type="text"
                      value={newExpYear}
                      onChange={(e) => setNewExpYear(e.target.value)}
                      placeholder="YYYY"
                      maxLength={4}
                      className="w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
                    />
                  </div>
                </div>
                <div>
                  <label className="mb-1 block text-xs font-medium">Billing Address</label>
                  <input
                    type="text"
                    value={newBillingAddress}
                    onChange={(e) => setNewBillingAddress(e.target.value)}
                    placeholder="123 Main St, City, ST 12345"
                    className="w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
                  />
                </div>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={editingPaymentId ? handleSaveEditPayment : handleAddPayment}
                    className="rounded-lg bg-black px-4 py-2 text-xs text-white hover:bg-gray-800 transition"
                  >
                    {editingPaymentId ? "Save Changes" : "Add Method"}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setShowAddPayment(false);
                      setEditingPaymentId(null);
                      setNewCardNumber("");
                      setNewExpMonth("");
                      setNewExpYear("");
                      setNewBillingAddress("");
                    }}
                    className="rounded-lg border px-4 py-2 text-xs hover:bg-gray-100 transition"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </div>
        </fieldset>

        <div className="flex items-center justify-end">
          <button
            className="rounded-xl bg-white px-5 py-2 text-sm text-black hover:bg-gray-700 transition border-2 border-black border-solid mr-[5%]"
            onClick={() => { confirm("Really delete user?") ? deleteUser : undefined }}
          >
            Delete User
          </button>
          <button
            type="submit"
            className="rounded-xl bg-black px-5 py-2 text-sm text-white hover:bg-gray-800 transition border-2 border-black border-solid"
          >
            Save Changes
          </button>
        </div>

      </form>
    </section >
  );
}
