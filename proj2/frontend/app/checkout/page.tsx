// app/checkout/page.tsx
"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
// import { useRouter } from "next/navigation";
import { useCartStore } from "@/lib/cartStore";
import { CheckoutApiService } from "@/lib/checkoutApi";
import type { PaymentMethod, DeliveryOrder } from "@/lib/types";

import AddPaymentMethod from "@/app/components/AddPaymentMethod";

type CheckoutStep = "review" | "payment" | "add-payment" | "confirm" | "success" | "error";

export default function CheckoutPage() {
  // const router = useRouter();
  const items = useCartStore((s) => s.items);
  const add = useCartStore((s) => s.add);
  const decrement = useCartStore((s) => s.decrement);
  const remove = useCartStore((s) => s.remove);
  const clear = useCartStore((s) => s.clear);
  
  const [currentStep, setCurrentStep] = useState<CheckoutStep>("review");
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([]);
  const [selectedPaymentMethod, setSelectedPaymentMethod] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [order, setOrder] = useState<DeliveryOrder | null>(null);

  // Load payment methods and cart on mount
  useEffect(() => {
    loadPaymentMethods();
    // Also ensure cart is loaded from backend
    const { loadCart } = useCartStore.getState();
    loadCart().catch(console.error);
  }, []);

  const loadPaymentMethods = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const methods = await CheckoutApiService.getPaymentMethods();
      setPaymentMethods(methods);
      
      // Customer must manually select payment method - no auto-selection
    } catch (err) {
      console.error("Error loading payment methods:", err);
      setError("Failed to load payment methods. Please refresh and try again or add a payment method.");
      setPaymentMethods([]); // Set empty array on error
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddPaymentMethod = async (paymentData: {
    card_number: string;
    expiration_month: number;
    expiration_year: number;
    billing_address: string;
    balance: number;
    is_default: boolean;
  }) => {
    try {
      setIsLoading(true);
      const newMethod = await CheckoutApiService.addPaymentMethod("1", paymentData);
      setPaymentMethods(prev => [...prev, newMethod]);
      setSelectedPaymentMethod(newMethod.id);
      setCurrentStep("review");
    } catch (err) {
      console.error("Error adding payment method:", err);
      setError("Failed to add payment method");
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdateQuantity = (itemId: string, newQty: number) => {
    if (newQty === 0) {
      remove(itemId);
    } else {
      const currentItem = items.find(item => item.id === itemId);
      if (currentItem) {
        const diff = newQty - currentItem.qty;
        if (diff > 0) {
          add(currentItem, diff);
        } else {
          decrement(itemId, Math.abs(diff));
        }
      }
    }
  };

  const handleRemoveItem = (itemId: string) => {
    remove(itemId);
  };

  const handlePlaceOrder = async () => {
    if (!selectedPaymentMethod) {
      setError("Please select a payment method");
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      
      // TODO: Get customer showing from previous booking/selection flow
      const customerShowings = await CheckoutApiService.getCustomerShowings("1"); // TODO: Get from auth
      const customerShowingId = customerShowings[0]?.id || "1";
      
      const newOrder = await CheckoutApiService.createDelivery({
        customer_showing_id: customerShowingId,
        payment_method_id: selectedPaymentMethod,
      });
      
      setOrder(newOrder);
      setCurrentStep("success");
      clear(); // Clear cart after successful order
    } catch (err) {
      const error = err as Error;
      setError(error.message || "Failed to place order");
      setCurrentStep("error");
    } finally {
      setIsLoading(false);
    }
  };

  // Removed cart empty check for testing
  const subtotal = items.reduce((sum, item) => sum + item.price * item.qty, 0);
  const tax = subtotal * 0.08;
  const deliveryFee = 3.99;
  const total = subtotal + tax + deliveryFee;

  const selectedMethod = paymentMethods.find(m => m.id === selectedPaymentMethod);
  const hasInsufficientFunds = selectedMethod && selectedMethod.balance < total;

  return (
    <section className="mx-auto mt-10 max-w-4xl px-4">
      <div className="mb-6">
        <Link
          href="/menu"
          className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900 transition"
        >
          ← Back to Menu
        </Link>
      </div>

      <h1 className="text-3xl font-bold mb-8">Cart & Checkout</h1>

      {error && (
        <div className="mb-6 rounded-lg bg-red-50 border border-red-200 p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Cart Management Section */}
          <div className="rounded-lg border p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold">Your Cart ({items.length} items)</h2>
              <div className="flex gap-3">
                {items.length > 0 && (
                  <button
                    onClick={clear}
                    className="rounded-lg border border-gray-300 px-4 py-2 text-sm hover:bg-gray-50 transition"
                  >
                    Clear Cart
                  </button>
                )}
              </div>
            </div>

            {items.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-600 mb-4">Your cart is empty. Please add items from the menu page first.</p>
              </div>
            ) : (
              <div className="space-y-3">
                {items.map((item) => (
                  <div key={item.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex-1">
                      <p className="font-medium">{item.name}</p>
                      <p className="text-sm text-gray-600">${item.price.toFixed(2)} each</p>
                    </div>

                    <div className="flex items-center gap-3">
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handleUpdateQuantity(item.id, Math.max(0, item.qty - 1))}
                          className="h-8 w-8 rounded border text-sm hover:bg-gray-100 transition"
                          disabled={item.qty <= 1}
                        >
                          −
                        </button>
                        <span className="w-8 text-center">{item.qty}</span>
                        <button
                          onClick={() => handleUpdateQuantity(item.id, item.qty + 1)}
                          className="h-8 w-8 rounded border text-sm hover:bg-gray-100 transition"
                        >
                          +
                        </button>
                      </div>
                      <div className="text-right min-w-[4rem]">
                        <p className="font-medium">${(item.price * item.qty).toFixed(2)}</p>
                      </div>
                      <button
                        onClick={() => handleRemoveItem(item.id)}
                        className="text-red-600 hover:text-red-800 ml-2"
                        title="Remove item"
                      >
                        ×
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Checkout Steps - Only show if cart has items */}
          {items.length > 0 && (
            <>
              {/* Step 1: Payment Method */}
              <div className={`rounded-lg border p-6 ${currentStep === "payment" || currentStep === "add-payment" ? "border-black" : "border-gray-200"}`}>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold">1. Payment Method</h2>

                {currentStep === "confirm" && selectedMethod && (
                  <button
                    onClick={() => setCurrentStep("payment")}
                    className="text-sm text-blue-600 hover:text-blue-800"
                  >
                    Change
                  </button>
                )}
              </div>

              {/* Payment method selection - always visible when cart has items */}
              {paymentMethods.length > 0 && (
                <div className="space-y-3">
                  <p className="text-sm text-gray-600 mb-3">
                    Select a payment method ({paymentMethods.length} available):
                  </p>
                  <div className="space-y-2">
                    {paymentMethods.map((method) => (
                      <div
                        key={method.id}
                        onClick={() => setSelectedPaymentMethod(method.id)}
                        className={`cursor-pointer rounded-lg border p-4 transition ${
                          selectedPaymentMethod === method.id
                            ? "border-black bg-gray-50"
                            : "border-gray-300 hover:border-gray-400"
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="flex items-center gap-2">
                              <p className="font-medium">
                                •••• •••• •••• {method.card_number.slice(-4)}
                              </p>
                              <input
                                type="radio"
                                name="paymentMethod"
                                checked={selectedPaymentMethod === method.id}
                                onChange={() => setSelectedPaymentMethod(method.id)}
                                className="h-4 w-4"
                                aria-label={`Select payment method ending in ${method.card_number.slice(-4)}`}
                              />
                            </div>
                            <p className="text-sm text-gray-600">
                              Expires {method.expiration_month.toString().padStart(2, '0')}/{method.expiration_year}
                            </p>
                            <p className="text-sm text-gray-600">
                              Balance: ${method.balance.toFixed(2)}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  
                  {/* Add new payment method option */}
                  <button
                    onClick={() => setCurrentStep("add-payment")}
                    className="w-full rounded-lg border border-dashed border-gray-300 p-4 text-sm text-gray-600 hover:bg-gray-50 transition"
                  >
                    + Add New Payment Method
                  </button>
                </div>
              )}

              {currentStep === "add-payment" ? (
                <AddPaymentMethod
                  onAdd={handleAddPaymentMethod}
                  onCancel={() => setCurrentStep("review")}
                  isLoading={isLoading}
                />
              ) : null}
              
              {/* Insufficient funds warning */}
              {hasInsufficientFunds && selectedMethod && (
                <div className="mt-4 rounded-lg bg-yellow-50 border border-yellow-200 p-4">
                  <p className="text-yellow-800 text-sm">
                    <strong>Insufficient funds:</strong> Selected payment method has ${selectedMethod?.balance.toFixed(2)} 
                    but order total is ${total.toFixed(2)}. Please add funds or select another payment method.
                  </p>
                </div>
              )}
              </div>
            </>
          )}



          {/* Success State */}
          {currentStep === "success" && order && (
            <div className="rounded-lg border border-green-300 bg-green-50 p-6 text-center">
              <div className="mb-4">
                <div className="mx-auto mb-4 h-12 w-12 rounded-full bg-green-100 flex items-center justify-center">
                  <svg className="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <h2 className="text-2xl font-bold text-green-800 mb-2">Order Placed Successfully!</h2>
                <p className="text-green-700">
                  Your order #{order.id} has been confirmed and is being prepared.
                </p>
              </div>
              
              <div className="space-y-3">
                <Link
                  href={`/track/${order.id}`}
                  className="inline-block rounded-lg bg-green-600 px-6 py-2 text-white hover:bg-green-700 transition"
                >
                  Track Your Order
                </Link>
                <div>
                  <Link
                    href="/menu"
                    className="inline-block rounded-lg border border-green-600 px-6 py-2 text-green-600 hover:bg-green-50 transition"
                  >
                    Continue Shopping
                  </Link>
                </div>
              </div>
            </div>
          )}

          {/* Error State */}
          {currentStep === "error" && (
            <div className="rounded-lg border border-red-300 bg-red-50 p-6 text-center">
              <div className="mb-4">
                <div className="mx-auto mb-4 h-12 w-12 rounded-full bg-red-100 flex items-center justify-center">
                  <svg className="h-6 w-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </div>
                <h2 className="text-2xl font-bold text-red-800 mb-2">Order Failed</h2>
                <p className="text-red-700 mb-4">{error}</p>
              </div>
              
              <div className="space-y-3">
                <button
                  onClick={() => {
                    setCurrentStep("payment");
                    setError(null);
                  }}
                  className="inline-block rounded-lg bg-red-600 px-6 py-2 text-white hover:bg-red-700 transition"
                >
                  Try Again
                </button>
                <div>
                  <Link
                    href="/menu"
                    className="inline-block rounded-lg border border-red-600 px-6 py-2 text-red-600 hover:bg-red-50 transition"
                  >
                    Back to Menu
                  </Link>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Order Total Summary */}
        {currentStep !== "success" && currentStep !== "error" && items.length > 0 && (
          <div className="lg:col-span-1">
            <div className="rounded-lg border p-6 sticky top-4">
              <h3 className="text-lg font-semibold mb-4">Order Total</h3>
              
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Subtotal ({items.length} items)</span>
                  <span>${subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Tax (8%)</span>
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
              
              {/* Place Order Button - Simple one-click payment */}
              {currentStep === "review" && (
                <div className="mt-6">
                  {paymentMethods.length === 0 ? (
                    <div className="text-center">
                      <p className="text-sm text-gray-600 mb-3">
                        Add a payment method to continue
                      </p>
                      <button
                        onClick={() => setCurrentStep("add-payment")}
                        className="w-full rounded-lg bg-gray-800 px-4 py-3 font-semibold text-white hover:bg-gray-700 transition"
                      >
                        Add Payment Method
                      </button>
                    </div>
                  ) : !selectedPaymentMethod ? (
                    <div className="text-center">
                      <p className="text-sm text-gray-600 mb-3">
                        Select a payment method above to continue
                      </p>
                      <button
                        disabled
                        className="w-full rounded-lg bg-gray-400 px-4 py-3 font-semibold text-white cursor-not-allowed"
                      >
                        Select Payment Method
                      </button>
                    </div>
                  ) : hasInsufficientFunds ? (
                    <button
                      disabled
                      className="w-full rounded-lg bg-gray-400 px-4 py-3 font-semibold text-white cursor-not-allowed"
                    >
                      Insufficient Funds
                    </button>
                  ) : (
                    <button
                      onClick={handlePlaceOrder}
                      disabled={isLoading}
                      className="w-full rounded-lg bg-green-600 px-4 py-3 font-semibold text-white hover:bg-green-700 transition disabled:bg-gray-400"
                    >
                      {isLoading ? "Placing Order..." : `Place Order - $${total.toFixed(2)}`}
                    </button>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </div>


    </section>
  );
}
