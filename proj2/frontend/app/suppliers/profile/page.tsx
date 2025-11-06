"use client";
import { useState, FormEvent } from "react";
import Link from "next/link";

export default function SupplierProfilePage() {
  // Company Information (from Suppliers model) - Backend integration ready
  const [companyName, setCompanyName] = useState("");
  const [companyAddress, setCompanyAddress] = useState("");
  const [contactPhone, setContactPhone] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  // Personal Information (from Users model) - Backend integration ready
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [birthday, setBirthday] = useState("");

  // Password Change
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    
    if (newPassword && newPassword !== confirmNewPassword) {
      alert("New passwords do not match.");
      return;
    }

    if (newPassword && newPassword.length < 8) {
      alert("New password must be at least 8 characters.");
      return;
    }

    // Here you would call the backend APIs:
    // PUT /api/suppliers - for company info
    // PUT /api/users/{id} - for personal info (if available)
    
    // TODO: Backend integration
    // PUT /api/suppliers - for company info
    // PUT /api/users/{id} - for personal info (if available)
    console.log("Form data ready for backend:", {
      company: { companyName, companyAddress, contactPhone, isOpen },
      personal: { name, email, phone, birthday }
    });
    
    alert("Profile updated successfully!");
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
        
        {/* Company Information Section */}
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
                onChange={(e) => setIsOpen(e.target.checked)}
                className="h-4 w-4 rounded border-gray-300 text-black focus:ring-black"
              />
              <label htmlFor="isOpen" className="text-sm font-medium">
                Store is currently open for orders
              </label>
            </div>
          </div>
        </fieldset>

        {/* Personal Information Section */}
        <fieldset className="rounded-lg border p-6">
          <legend className="px-2 text-lg font-semibold">Personal Information</legend>
          
          <div className="mt-4 grid gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="name" className="mb-1 block text-sm font-medium">
                Full Name
              </label>
              <input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                placeholder="John Supplier"
                className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>

            <div>
              <label htmlFor="email" className="mb-1 block text-sm font-medium">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="john@companya.com"
                className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>

            <div>
              <label htmlFor="phone" className="mb-1 block text-sm font-medium">
                Personal Phone
              </label>
              <input
                id="phone"
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                required
                placeholder="555-0011"
                className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>

            <div>
              <label htmlFor="birthday" className="mb-1 block text-sm font-medium">
                Birthday
              </label>
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
        </fieldset>

        {/* Password Change Section */}
        <fieldset className="rounded-lg border p-6">
          <legend className="px-2 text-lg font-semibold">Change Password (Optional)</legend>
          
          <div className="mt-4 grid gap-4 sm:grid-cols-3">
            <div>
              <label htmlFor="currentPassword" className="mb-1 block text-sm font-medium">
                Current Password
              </label>
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
              <label htmlFor="newPassword" className="mb-1 block text-sm font-medium">
                New Password
              </label>
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
              <label htmlFor="confirmNewPassword" className="mb-1 block text-sm font-medium">
                Confirm New Password
              </label>
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

        {/* Submit Button */}
        <div className="flex items-center justify-end">
          <button
            type="submit"
            className="rounded-xl bg-black px-6 py-2 text-sm text-white hover:bg-gray-800 transition"
          >
            Save Changes
          </button>
        </div>
      </form>
    </section>
  );
}