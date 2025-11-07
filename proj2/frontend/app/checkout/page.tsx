// app/checkout/page.tsx
"use client";

import { useState, useEffect, useCallback, useMemo } from "react";
import { Router } from "next/router";
import Link from 'next/link';
import Cookies from 'js-cookie';

type Item = {
  item_id: string,
  quantity: string,

  product: Product
};

type Product = {
  id: string,
  name: string,
  unit_price: Float32Array,
  inventory_quantity: number,
  size: number,
  keywords: string,
  category: string,
  discount: number,
  is_available: boolean

  supplier: IDtoSupplier
}

type Supplier = {
  company_name: string,
  company_address: string,
  contact_phone: string,
  is_open: string
}

type IDtoSupplier = {
  id: string,
  supplier: Supplier
}

type PaymentMethod = {
  id: string,
  card_number: number,
  exp_month: number,
  exp_year: number,
  balance: Float32Array,
  is_default: boolean,
  billing_address: string
};

export default function CheckoutPage() {
  const [items, setItems] = useState<Item[]>([]);
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([]);

  const [suppliers, setSuppliers] = useState<IDtoSupplier[]>([]);

  const loadSuppliers = async () => {

  };

  useEffect(() => {
    loadSuppliers();
  }, []);

  // Helper function to safely cast/access product data
  const getProductData = (item: Item) => {
    // Assuming product data is available and price can be treated as a number
    const name = item.product?.name || "Unknown Product";
    // Assuming Float32Array for unit_price and balance is meant to be a single number
    const unitPrice = item.product?.unit_price ? (item.product.unit_price as unknown as number) : 0;
    const quantity = parseInt(item.quantity) || 0;
    const itemId = item.item_id;

    return { itemId, name, unitPrice, quantity };
  };

  // Helper function for PaymentMethod data
  const getPaymentData = (method: PaymentMethod) => {
    // Assuming card_number is a full number that needs conversion for display
    const cardNumberStr = String(method.card_number);
    const lastFour = cardNumberStr.slice(-4);
    const balance = method.balance ? (method.balance as unknown as number) : 0;
    const expMonth = String(method.exp_month).padStart(2, '0');
    const expYear = method.exp_year;

    return { lastFour, balance, expMonth, expYear };
  };

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

      {/* ERROR SECTION REMOVED: Needs 'error' state */}
      {/* {error && (
        <div className="mb-6 rounded-lg bg-red-50 border border-red-200 p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )} */}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Cart Management Section */}
          <div className="rounded-lg border p-6">
            <div className="flex items-center justify-between mb-4">
              {/* Using 'items' length */}
              <h2 className="text-xl font-semibold">Your Cart ({items.length} items)</h2>
              <div className="flex gap-3">
                {items.length > 0 && (
                  <button
                    // onClick={handleClearCart} REMOVED
                    className="rounded-lg border border-gray-300 px-4 py-2 text-sm hover:bg-gray-50 transition"
                  >
                    Clear Cart
                  </button>
                )}
              </div>
            </div>

            {/* Using 'items' length */}
            {items.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-600 mb-4">Your cart is empty. Please add items from the menu page first.</p>
              </div>
            ) : (
              <div className="space-y-3">
                {items.map((item) => {
                  const data = getProductData(item);
                  return (
                    // Using item.item_id as key
                    <div key={item.item_id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex-1">
                        {/* Using product data */}
                        <p className="font-medium">{data.name}</p>
                        <p className="text-sm text-gray-600">${data.unitPrice.toFixed(2)} each</p>
                      </div>

                      <div className="flex items-center gap-3">
                        <div className="flex items-center gap-2">
                          <button
                            // onClick={() => handleUpdateQuantity(item.id, Math.max(0, item.qty - 1))} REMOVED
                            className="h-8 w-8 rounded border text-sm hover:bg-gray-100 transition"
                          // disabled={item.qty <= 1} REMOVED
                          >
                            −
                          </button>
                          {/* Using quantity */}
                          <span className="w-8 text-center">{data.quantity}</span>
                          <button
                            // onClick={() => handleUpdateQuantity(item.id, item.qty + 1)} REMOVED
                            className="h-8 w-8 rounded border text-sm hover:bg-gray-100 transition"
                          >
                            +
                          </button>
                        </div>
                        <div className="text-right min-w-[4rem]">
                          {/* Using product data for calculation */}
                          <p className="font-medium">${(data.unitPrice * data.quantity).toFixed(2)}</p>
                        </div>
                        <button
                          // onClick={() => handleRemoveItem(item.id)} REMOVED
                          className="text-red-600 hover:text-red-800 ml-2"
                          title="Remove item"
                        >
                          ×
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Checkout Steps - Only show if cart has items */}
          {items.length > 0 && (
            <>
              {/* Step 1: Payment Method */}
              <div className={`rounded-lg border p-6 border-gray-200`}>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold">1. Payment Method</h2>

                  {/* REMOVED: Needs 'currentStep' and 'selectedMethod' */}
                  {/* {currentStep === "confirm" && selectedMethod && (
                    <button
                      onClick={() => setCurrentStep("payment")}
                      className="text-sm text-blue-600 hover:text-blue-800"
                    >
                      Change
                    </button>
                  )} */}
                </div>

                {/* Payment method selection - always visible when cart has items */}
                {paymentMethods.length > 0 && (
                  <div className="space-y-3">
                    <p className="text-sm text-gray-600 mb-3">
                      Select a payment method ({paymentMethods.length} available):
                    </p>
                    <div className="space-y-2">
                      {paymentMethods.map((method) => {
                        const data = getPaymentData(method);
                        return (
                          <div
                            key={method.id}
                            // onClick={() => setSelectedPaymentMethod(method.id)} REMOVED
                            className={`cursor-pointer rounded-lg border p-4 transition border-gray-300 hover:border-gray-400`}
                          >
                            <div className="flex items-center justify-between">
                              <div>
                                <div className="flex items-center gap-2">
                                  <p className="font-medium">
                                    {/* Using payment data */}
                                    •••• •••• •••• {data.lastFour}
                                  </p>
                                  <input
                                    type="radio"
                                    name="paymentMethod"
                                    // checked={selectedPaymentMethod === method.id} REMOVED
                                    // onChange={() => setSelectedPaymentMethod(method.id)} REMOVED
                                    className="h-4 w-4"
                                    aria-label={`Select payment method ending in ${data.lastFour}`}
                                  />
                                </div>
                                <p className="text-sm text-gray-600">
                                  {/* Using payment data */}
                                  Expires {data.expMonth}/{data.expYear}
                                </p>
                                <p className="text-sm text-gray-600">
                                  {/* Using payment data */}
                                  Balance: ${data.balance.toFixed(2)}
                                </p>
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>

                    {/* Add new payment method option */}
                    <button
                      // onClick={() => setCurrentStep("add-payment")} REMOVED
                      className="w-full rounded-lg border border-dashed border-gray-300 p-4 text-sm text-gray-600 hover:bg-gray-50 transition"
                    >
                      + Add New Payment Method
                    </button>
                  </div>
                )}

                {/* Insufficient funds warning REMOVED: Needs 'hasInsufficientFunds', 'selectedMethod', 'total' */}
                {/* {hasInsufficientFunds && selectedMethod && (
                  <div className="mt-4 rounded-lg bg-yellow-50 border border-yellow-200 p-4">
                    <p className="text-yellow-800 text-sm">
                      <strong>Insufficient funds:</strong> Selected payment method has ${selectedMethod?.balance.toFixed(2)}
                      but order total is ${total.toFixed(2)}. Please add funds or select another payment method.
                    </p>
                  </div>
                )} */}
              </div>
            </>
          )}

          {/* Success State REMOVED: Needs 'currentStep' and 'order' */}
          {/* {currentStep === "success" && order && ( ... )} */}

          {/* Error State REMOVED: Needs 'currentStep' and 'error' */}
          {/* {currentStep === "error" && ( ... )} */}
        </div>

        {/* Order Total Summary - Only show if cart has items */}
        {items.length > 0 && (
          <div className="lg:col-span-1">
            <div className="rounded-lg border p-6 sticky top-4">
              <h3 className="text-lg font-semibold mb-4">Order Total</h3>

              {/* All calculations are removed as they rely on undefined state/computed values (subtotal, tax, deliveryFee, total) */}
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Subtotal ({items.length} items)</span>
                  <span>$0.00</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Tax (8%)</span>
                  <span>$0.00</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Delivery Fee</span>
                  <span>$0.00</span>
                </div>
                <div className="flex justify-between font-semibold text-lg border-t pt-2">
                  <span>Total</span>
                  <span>$0.00</span>
                </div>
              </div>

              {/* Place Order Button - Simple one-click payment */}
              {/* Only rendering the 'Add Payment Method' section for simplicity */}
              <div className="mt-6">
                {paymentMethods.length === 0 ? (
                  <div className="text-center">
                    <p className="text-sm text-gray-600 mb-3">
                      Add a payment method to continue
                    </p>
                    <button
                      // onClick={() => setCurrentStep("add-payment")} REMOVED
                      className="w-full rounded-lg bg-gray-800 px-4 py-3 font-semibold text-white hover:bg-gray-700 transition"
                    >
                      Add Payment Method
                    </button>
                  </div>
                ) : (
                  // Fallback for when methods exist, but we can't determine the other states (selected, funds)
                  <button
                    disabled
                    className="w-full rounded-lg bg-gray-400 px-4 py-3 font-semibold text-white cursor-not-allowed"
                  >
                    Select Payment Method / Place Order
                  </button>
                )}
              </div>
              {/* The rest of the Place Order logic requires currentStep, selectedPaymentMethod, hasInsufficientFunds, isLoading, and total, which are all undefined. */}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}