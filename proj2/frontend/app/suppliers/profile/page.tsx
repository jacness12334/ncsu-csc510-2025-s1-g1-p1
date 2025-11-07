"use client";
import { useState, FormEvent, useEffect } from "react";
import Link from "next/link";
import Cookies from "js-cookie";

export default function SupplierProfilePage() {
  // Company Information (matches backend Suppliers model)
  const [companyName, setCompanyName] = useState("");
  const [companyAddress, setCompanyAddress] = useState("");
  const [contactPhone, setContactPhone] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  // Application state management
  const [userId, setUserId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const getUserIdFromCookie = () => {
    const id = Cookies.get("user_id");
    return id ? parseInt(id) || null : null;
  };

  // Load profile data from backend
  const loadProfileData = async (id: number) => {
    try {
      const res = await fetch(`http://localhost:5000/api/suppliers/${id}`);
      if (!res.ok) throw new Error("Failed to fetch supplier data");
      const data = await res.json();
      const supplier = data.supplier;

      setCompanyName(supplier.company_name);
      setCompanyAddress(supplier.company_address);
      setContactPhone(supplier.contact_phone);
      setIsOpen(supplier.is_open);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const id = getUserIdFromCookie();
    if (id) {
      setUserId(id);
      loadProfileData(id);
    } else {
    }
  }, []);

  // Toggle supplier availability immediately on checkbox change
  const handleAvailabilityChange = async (checked: boolean) => {
    setIsOpen(checked);
    if (!userId) return;
    try {
      const res = await fetch(`http://localhost:5000/api/suppliers/status`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, is_open: checked }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || "Failed to update availability");
      }
    } catch (error) {
      console.error(error);
      setIsOpen(!checked); // revert on failure
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!userId) {
      alert("User not authenticated");
      return;
    }

    setIsLoading(true);
    try {
      // Update supplier company info
      const supplierRes = await fetch(`http://localhost:5000/api/suppliers`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userId,
          company_name: companyName,
          company_address: companyAddress,
          contact_phone: contactPhone,
          is_open: isOpen,
        }),
      });

      if (!supplierRes.ok) {
        const err = await supplierRes.json();
        throw new Error(err.error || "Failed to update supplier profile");
      }

      // TODO: Integrate user personal info and password update when routes available

      alert("Profile updated successfully!");
    } catch (error) {
      console.error(error);
      alert("Error updating profile. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="mx-auto mt-10 max-w-2xl">
      <div className="mb-6">
        <div className="mb-4">
          <Link
            href="/suppliers"
            className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900"
          >
            ← Return to Dashboard
          </Link>
        </div>
        <h1 className="mb-2 text-2xl font-bold">Supplier Profile</h1>
        <p className="text-sm text-gray-600">Update your company and personal information.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        <fieldset className="rounded-lg border p-6">
          <legend className="px-2 text-lg font-semibold">Company Information</legend>
          <div className="mt-4 space-y-4">
            <div>
              <label htmlFor="companyName" className="mb-1 block text-sm font-medium">
                Company Name
              </label>
              <input
                id="companyName"
                type="text"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                required
                placeholder="Company A"
                className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>

            <div>
              <label htmlFor="companyAddress" className="mb-1 block text-sm font-medium">
                Company Address
              </label>
              <textarea
                id="companyAddress"
                value={companyAddress}
                onChange={(e) => setCompanyAddress(e.target.value)}
                required
                placeholder="123 Company Way, City, State 12345"
                rows={3}
                className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>

            <div>
              <label htmlFor="contactPhone" className="mb-1 block text-sm font-medium">
                Contact Phone
              </label>
              <input
                id="contactPhone"
                type="tel"
                value={contactPhone}
                onChange={(e) => setContactPhone(e.target.value)}
                required
                placeholder="555-0010"
                className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>

            <div className="flex items-center space-x-3">
              <input
                id="isOpen"
                type="checkbox"
                checked={isOpen}
                onChange={(e) => handleAvailabilityChange(e.target.checked)}
                className="h-4 w-4 rounded border-gray-300 text-black focus:ring-black"
              />
              <label htmlFor="isOpen" className="text-sm font-medium">
                Store is currently open for orders
              </label>
            </div>
          </div>
        </fieldset>

        <div className="flex items-center justify-end">
          <button
            type="submit"
            disabled={isLoading}
            className="rounded-xl bg-black px-6 py-2 text-sm text-white hover:bg-gray-800 transition disabled:opacity-50"
          >
            {isLoading ? "Processing..." : "Save Changes"}
          </button>
        </div>
      </form>
    </section>
  );
}
