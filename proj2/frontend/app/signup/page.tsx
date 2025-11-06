"use client";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import Link from "next/link";

export default function SignupPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [birthday, setBirthday] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [userType, setUserType] = useState("");

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    // TODO: Add validation and actual signup logic when backend is ready
    // For now, just navigate to order page
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    try {
      switch (userType) {
        case 'customer':
          let response = await fetch("http://localhost:5000/api/users/register", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              name: name,
              email: email,
              phone: phone,
              birthday: birthday,
              password: password,
              role: 'customer',
              default_theatre_id: -1
            })
          });

          if (!response.ok) {
            // If server responds with 400/500 code, get the specific message
            const errorData = await response.json();
            throw new Error(errorData.message || response.statusText);
          }

          // Success path:
          router.push("/login");
          alert("Registration successful!");

          break;

        case 'staff-runner':
        case 'staff-admin':
          response = await fetch("http://localhost:5000/api/staff", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              name: name,
              email: email,
              phone: phone,
              birthday: birthday,
              password: password,
              role: userType.split('-')[1],
              theatre_id: -1
            })
          });

          if (!response.ok) {
            // If server responds with 400/500 code, get the specific message
            const errorData = await response.json();
            throw new Error(errorData.message || response.statusText);
          }

          // Success path:
          router.push("/login");
          alert("Registration successful!");
          break;

        case 'supplier':
          break;

        case 'driver':
          break;

        default:
          alert("Error: User type not registered. Please contact admin for details.");
          break;
      }

    } catch (error: unknown) {
      // This catches network errors AND the error thrown above
      console.error(error);
      alert("Error: " + (error instanceof Error ? error.message : String(error)));
    }
  };



  return (
    <section className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-2">Sign Up</h1>
      <p className="text-sm text-gray-600 mb-6">Create an account to start ordering.</p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium mb-1">
            User Type
          </label>
          <select
            id="name"
            value={userType}
            onChange={(e) => setUserType(e.target.value)}
            required
            className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black">
            <option value='customer'>Customer</option>
            <option value='staff-runner'>Staff (runner)</option>
            <option value='staff-admin'>Staff (admin)</option>
            <option value='driver'>Driver</option>
            <option value='supplier'>Supplier</option>
          </select>
        </div>
        <div>
          <label htmlFor="name" className="block text-sm font-medium mb-1">
            Full Name
          </label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="John Doe"
          />
        </div>

        <div>
          <label htmlFor="email" className="block text-sm font-medium mb-1">
            Email
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="you@example.com"
          />
        </div>

        <div>
          <label htmlFor="phone" className="block text-sm font-medium mb-1">
            Phone Number
          </label>
          <input
            type="tel"
            id="phone"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            required
            className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="(555) 123-4567"
          />
        </div>

        <div>
          <label htmlFor="birthday" className="block text-sm font-medium mb-1">
            Birthday
          </label>
          <input
            type="date"
            id="birthday"
            value={birthday}
            onChange={(e) => setBirthday(e.target.value)}
            required
            className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
          />
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium mb-1">
            Password
          </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
            className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="••••••••"
          />
        </div>

        <div>
          <label htmlFor="confirmPassword" className="block text-sm font-medium mb-1">
            Confirm Password
          </label>
          <input
            type="password"
            id="confirmPassword"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            minLength={8}
            className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="••••••••"
          />
        </div>

        <button
          type="submit"
          className="w-full rounded-xl bg-black px-5 py-2.5 text-sm text-white hover:bg-gray-800 transition"
        >
          Sign Up
        </button>
      </form>

      <p className="mt-4 text-center text-sm text-gray-600">
        Already have an account?{" "}
        <Link href="/login" className="font-medium text-black underline">
          Log in
        </Link>
      </p>
    </section>
  );
}
