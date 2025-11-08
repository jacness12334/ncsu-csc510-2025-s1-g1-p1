"use client";

import { useState } from "react";

interface AddPaymentMethodProps {
  onAdd: (paymentData: {
    card_number: string;
    expiration_month: number;
    expiration_year: number;
    billing_address: string;
    balance: number;
    is_default: boolean;
  }) => void;
  onCancel: () => void;
  isLoading?: boolean;
}

/**
 * adds new payment method
 * @param param0 new payment method
 * @returns new payment method
 */
export default function AddPaymentMethod({
  onAdd,
  onCancel,
  isLoading = false,
}: AddPaymentMethodProps) {
  const [formData, setFormData] = useState({
    card_number: "",
    expiration_month: "",
    expiration_year: "",
    billing_address: "",
    balance: "100.00",
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  /**
   * submit form data api call
   * @returns 
   */
  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    // Card number validation (16 digits)
    if (!/^\d{16}$/.test(formData.card_number.replace(/\s/g, ""))) {
      newErrors.card_number = "Card number must be 16 digits";
    }

    // Expiration month (1-12)
    const month = parseInt(formData.expiration_month);
    if (!month || month < 1 || month > 12) {
      newErrors.expiration_month = "Valid month required (1-12)";
    }

    // Expiration year (current year or later)
    const year = parseInt(formData.expiration_year);
    const currentYear = new Date().getFullYear();
    if (!year || year < currentYear) {
      newErrors.expiration_year = `Year must be ${currentYear} or later`;
    }

    // Billing address
    if (!formData.billing_address.trim()) {
      newErrors.billing_address = "Billing address is required";
    }

    // Balance
    const balance = parseFloat(formData.balance);
    if (isNaN(balance) || balance < 0) {
      newErrors.balance = "Valid balance amount required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * validates and submits
   * @param e form data
   * @returns 
   */
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    onAdd({
      card_number: formData.card_number.replace(/\s/g, ""),
      expiration_month: parseInt(formData.expiration_month),
      expiration_year: parseInt(formData.expiration_year),
      billing_address: formData.billing_address.trim(),
      balance: parseFloat(formData.balance),
      is_default: false, // Always false since we removed default functionality
    });
  };

  /**
   * formats card number
   * @param value card number
   * @returns card number formatted
   */
  const formatCardNumber = (value: string) => {
    const v = value.replace(/\s+/g, "").replace(/[^0-9]/gi, "");
    const matches = v.match(/\d{4,16}/g);
    const match = (matches && matches[0]) || "";
    const parts = [];
    for (let i = 0, len = match.length; i < len; i += 4) {
      parts.push(match.substring(i, i + 4));
    }
    if (parts.length) {
      return parts.join(" ");
    } else {
      return v;
    }
  };

  return (
    <div className="rounded-lg border p-6">
      <h3 className="text-lg font-semibold mb-4">Add Payment Method</h3>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="card_number" className="block text-sm font-medium mb-1">
            Card Number
          </label>
          <input
            id="card_number"
            type="text"
            value={formData.card_number}
            onChange={(e) =>
              setFormData({
                ...formData,
                card_number: formatCardNumber(e.target.value),
              })
            }
            placeholder="1234 5678 9012 3456"
            maxLength={19}
            className={`w-full rounded-lg border px-3 py-2 ${errors.card_number ? "border-red-500" : "border-gray-300"
              }`}
            disabled={isLoading}
          />
          {errors.card_number && (
            <p className="text-sm text-red-600 mt-1">{errors.card_number}</p>
          )}
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label htmlFor="expiration_month" className="block text-sm font-medium mb-1">
              Expiration Month
            </label>
            <select
              id="expiration_month"
              value={formData.expiration_month}
              onChange={(e) =>
                setFormData({ ...formData, expiration_month: e.target.value })
              }
              className={`w-full rounded-lg border px-3 py-2 ${errors.expiration_month ? "border-red-500" : "border-gray-300"
                }`}
              disabled={isLoading}
            >
              <option value="">Month</option>
              {Array.from({ length: 12 }, (_, i) => i + 1).map((month) => (
                <option key={month} value={month}>
                  {month.toString().padStart(2, "0")}
                </option>
              ))}
            </select>
            {errors.expiration_month && (
              <p className="text-sm text-red-600 mt-1">{errors.expiration_month}</p>
            )}
          </div>

          <div>
            <label htmlFor="expiration_year" className="block text-sm font-medium mb-1">
              Expiration Year
            </label>
            <select
              id="expiration_year"
              value={formData.expiration_year}
              onChange={(e) =>
                setFormData({ ...formData, expiration_year: e.target.value })
              }
              className={`w-full rounded-lg border px-3 py-2 ${errors.expiration_year ? "border-red-500" : "border-gray-300"
                }`}
              disabled={isLoading}
            >
              <option value="">Year</option>
              {Array.from({ length: 10 }, (_, i) => new Date().getFullYear() + i).map(
                (year) => (
                  <option key={year} value={year}>
                    {year}
                  </option>
                )
              )}
            </select>
            {errors.expiration_year && (
              <p className="text-sm text-red-600 mt-1">{errors.expiration_year}</p>
            )}
          </div>
        </div>

        <div>
          <label htmlFor="billing_address" className="block text-sm font-medium mb-1">
            Billing Address
          </label>
          <textarea
            id="billing_address"
            value={formData.billing_address}
            onChange={(e) =>
              setFormData({ ...formData, billing_address: e.target.value })
            }
            placeholder="123 Main St, City, State 12345"
            rows={3}
            className={`w-full rounded-lg border px-3 py-2 ${errors.billing_address ? "border-red-500" : "border-gray-300"
              }`}
            disabled={isLoading}
          />
          {errors.billing_address && (
            <p className="text-sm text-red-600 mt-1">{errors.billing_address}</p>
          )}
        </div>

        <div>
          <label htmlFor="balance" className="block text-sm font-medium mb-1">
            Initial Balance
          </label>
          <div className="relative">
            <span className="absolute left-3 top-2 text-gray-500">$</span>
            <input
              id="balance"
              type="number"
              step="0.01"
              min="0"
              value={formData.balance}
              onChange={(e) =>
                setFormData({ ...formData, balance: e.target.value })
              }
              className={`w-full rounded-lg border pl-8 pr-3 py-2 ${errors.balance ? "border-red-500" : "border-gray-300"
                }`}
              disabled={isLoading}
            />
          </div>
          {errors.balance && (
            <p className="text-sm text-red-600 mt-1">{errors.balance}</p>
          )}
        </div>



        <div className="flex gap-3">
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 rounded-lg border border-gray-300 px-4 py-2 text-sm hover:bg-gray-50 transition"
            disabled={isLoading}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="flex-1 rounded-lg bg-black px-4 py-2 text-sm text-white hover:bg-gray-800 transition disabled:bg-gray-400"
            disabled={isLoading}
          >
            {isLoading ? "Adding..." : "Add Payment Method"}
          </button>
        </div>
      </form>
    </div>
  );
}