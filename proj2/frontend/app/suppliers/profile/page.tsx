"use client";
import { useState, FormEvent, useEffect } from "react";
import Link from "next/link";

export default function SupplierProfilePage() {
  // Company Information (matches backend Suppliers model)
  const [companyName, setCompanyName] = useState("");
  const [companyAddress, setCompanyAddress] = useState("");
  const [contactPhone, setContactPhone] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  // Personal Information (matches backend Users model)
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [birthday, setBirthday] = useState("");

  // Password change form fields
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");

  // Application state management
  const [userId, setUserId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  /**
   * Retrieves user ID from sessionToken cookie set during login
   * @returns user ID as number or null if not found
   */
  const getUserIdFromCookie = () => {
    const cookies = document.cookie.split(';');
    const sessionCookie = cookies.find(cookie => cookie.trim().startsWith('sessionToken='));
    if (sessionCookie) {
      const tokenValue = sessionCookie.split('=')[1];
      return parseInt(tokenValue) || null;
    }
    return null;
  };

  /**
   * Initialize user authentication on component mount
   * Note: Would also load existing profile data when GET endpoints are available
   */
  useEffect(() => {
    const id = getUserIdFromCookie();
    if (id) {
      setUserId(id);
      // TODO: Load existing supplier and user data when GET /api/suppliers endpoint is enabled
      // loadProfileData(id);
    } else {
      alert("Please log in to access supplier features");
    }
  }, []);

  /**
   * Handles profile form submission
   * Note: PUT /api/suppliers endpoint excluded as requested
   * Form structure ready for future backend integration
   */
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    
    // Validate password fields if attempting to change password
    if (newPassword && newPassword !== confirmNewPassword) {
      alert("New passwords do not match.");
      return;
    }

    if (newPassword && newPassword.length < 8) {
      alert("New password must be at least 8 characters.");
      return;
    }

    if (!userId) {
      alert("User not authenticated");
      return;
    }

    setIsLoading(true);
    try {
      // Profile form data is structured and ready for backend integration
      // PUT /api/suppliers endpoint available but excluded per request
      // Personal info updates would require user routes integration
      
      console.log("Profile data structured for backend:", {
        supplier: { 
          user_id: userId,
          company_name: companyName, 
          company_address: companyAddress, 
          contact_phone: contactPhone, 
          is_open: isOpen 
        },
        user: { name, email, phone, birthday },
        password_change: newPassword ? { current_password: currentPassword, new_password: newPassword } : null
      });
      
      alert("Profile form ready for backend integration! (PUT /api/suppliers excluded as requested)");
    } catch (error) {
      console.error("Error preparing profile data:", error);
      alert("Error processing profile form. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  /* Profile Page Layout */
  return (
    <section className="mx-auto mt-10 max-w-2xl">
      {/* Header Section with Navigation */}
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

      {/* Profile Update Form */}
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
          
          {/* Personal details grid layout */}
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
          
          {/* Password fields grid layout */}
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

        {/* Form Submit Button */}
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