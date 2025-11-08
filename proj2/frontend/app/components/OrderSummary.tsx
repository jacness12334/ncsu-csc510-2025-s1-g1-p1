"use client";

import type { CartItem } from "@/lib/types";

interface OrderSummaryProps {
  items: CartItem[];
  className?: string;
  showControls?: boolean;
  onUpdateQuantity?: (id: string, newQty: number) => void;
  onRemoveItem?: (id: string) => void;
  onAddItem?: () => void;
  showCheckoutButton?: boolean;
  onContinueToPayment?: () => void;
  checkoutButtonText?: string;
}


export default function OrderSummary({
  items,
  className = "",
  showControls = false,
  onUpdateQuantity,
  onRemoveItem,
  onAddItem,
  showCheckoutButton = false,
  onContinueToPayment,
  checkoutButtonText = "Continue to Payment"
}: OrderSummaryProps) {
  const subtotal = items.reduce((sum, item) => sum + item.price * item.qty, 0);
  const tax = subtotal * 0.08; // 8% tax rate
  const deliveryFee = 3.99;
  const total = subtotal + tax + deliveryFee;

  return (
    <div className={`rounded-lg border p-6 ${className}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">Order Summary</h3>
        {showControls && onAddItem && (
          <button
            onClick={onAddItem}
            className="rounded-lg border border-gray-300 px-3 py-1 text-sm hover:bg-gray-50 transition"
          >
            + Add Item
          </button>
        )}
      </div>

      {items.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-600 mb-4">Your cart is empty</p>
          {showControls && onAddItem && (
            <button
              onClick={onAddItem}
              className="rounded-lg bg-black px-4 py-2 text-sm text-white hover:bg-gray-800 transition"
            >
              Add Items to Cart
            </button>
          )}
        </div>
      ) : (
        <>
          <div className="space-y-3 mb-4">
            {items.map((item) => (
              <div key={item.id} className="flex justify-between items-center">
                <div className="flex-1">
                  <p className="font-medium">{item.name}</p>
                  <p className="text-sm text-gray-600">
                    ${item.price.toFixed(2)} each
                  </p>
                </div>

                {showControls ? (
                  <div className="flex items-center gap-3">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => onUpdateQuantity?.(item.id, Math.max(0, item.qty - 1))}
                        className="h-7 w-7 rounded border text-sm hover:bg-gray-100 transition"
                        disabled={item.qty <= 1}
                      >
                        −
                      </button>
                      <span className="w-8 text-center text-sm">{item.qty}</span>
                      <button
                        onClick={() => onUpdateQuantity?.(item.id, item.qty + 1)}
                        className="h-7 w-7 rounded border text-sm hover:bg-gray-100 transition"
                      >
                        +
                      </button>
                    </div>
                    <div className="text-right min-w-[4rem]">
                      <p className="font-medium text-sm">${(item.price * item.qty).toFixed(2)}</p>
                    </div>
                    <button
                      onClick={() => onRemoveItem?.(item.id)}
                      className="text-red-600 hover:text-red-800 text-sm ml-2"
                      title="Remove item"
                    >
                      ×
                    </button>
                  </div>
                ) : (
                  <div className="text-right">
                    <p className="text-sm text-gray-600">{item.qty}×</p>
                    <p className="font-medium">${(item.price * item.qty).toFixed(2)}</p>
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="border-t pt-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span>Subtotal</span>
              <span>${subtotal.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>Tax</span>
              <span>${tax.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>Delivery Fee</span>
              <span>${deliveryFee.toFixed(2)}</span>
            </div>
            <div className="flex justify-between font-semibold text-lg border-t pt-2">
              <span>Total</span>
              <span>${total.toFixed(2)}</span>
            </div>
          </div>

          {/* Checkout Button */}
          {showCheckoutButton && onContinueToPayment && items.length > 0 && (
            <div className="mt-6">
              <button
                onClick={onContinueToPayment}
                className="w-full rounded-lg bg-black px-4 py-3 font-semibold text-white hover:bg-gray-800 transition"
              >
                {checkoutButtonText}
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}