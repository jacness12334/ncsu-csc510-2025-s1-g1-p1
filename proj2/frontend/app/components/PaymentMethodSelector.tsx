"use client";

import type { PaymentMethod } from "@/lib/types";

interface PaymentMethodSelectorProps {
  paymentMethods: PaymentMethod[];
  selectedPaymentMethod: string | null;
  onSelectPaymentMethod: (id: string) => void;
  onAddNewPaymentMethod: () => void;
}

/**
 * selects a payment method
 * @param param0 what to select
 * @returns 
 */
export default function PaymentMethodSelector({
  paymentMethods,
  selectedPaymentMethod,
  onSelectPaymentMethod,
  onAddNewPaymentMethod,
}: PaymentMethodSelectorProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Payment Method</h3>
        <button
          onClick={onAddNewPaymentMethod}
          className="rounded-lg border border-gray-300 px-3 py-1 text-sm hover:bg-gray-50 transition"
        >
          + Add New
        </button>
      </div>

      {paymentMethods.length === 0 ? (
        <div className="rounded-lg border border-dashed border-gray-300 p-6 text-center">
          <p className="text-gray-600 mb-2">No payment methods found</p>
          <button
            onClick={onAddNewPaymentMethod}
            className="rounded-lg bg-black px-4 py-2 text-sm text-white hover:bg-gray-800 transition"
          >
            Add Payment Method
          </button>
        </div>
      ) : (
        <div className="space-y-2">
          {paymentMethods.map((method) => (
            <div
              key={method.id}
              className={`cursor-pointer rounded-lg border p-4 transition ${selectedPaymentMethod === method.id
                  ? "border-black bg-gray-50"
                  : "border-gray-300 hover:border-gray-400"
                }`}
              onClick={() => onSelectPaymentMethod(method.id)}
            >
              <div className="flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <p className="font-medium">
                      •••• •••• •••• {method.card_number.slice(-4)}
                    </p>
                  </div>
                  <p className="text-sm text-gray-600">
                    Expires {method.expiration_month.toString().padStart(2, '0')}/{method.expiration_year}
                  </p>
                  <p className="text-sm text-gray-600">
                    Balance: ${method.balance.toFixed(2)}
                  </p>
                </div>
                <div className="flex items-center">
                  <input
                    type="radio"
                    name="paymentMethod"
                    checked={selectedPaymentMethod === method.id}
                    onChange={() => onSelectPaymentMethod(method.id)}
                    className="h-4 w-4"
                    aria-label={`Select payment method ending in ${method.card_number.slice(-4)}`}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}