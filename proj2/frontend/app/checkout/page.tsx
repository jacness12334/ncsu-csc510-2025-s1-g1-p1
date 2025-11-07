// app/checkout/page.tsx
"use client";

import Link from "next/link";
import { useState, useEffect, useMemo } from "react";
import { useRouter } from "next/navigation";

// --- 1. Define Data Structures (based on models.py) ---

// Interface for a CartItem, joined with Product details
// Based on CartItems and Products models
interface CartItem {
  id: string; // CartItems.id
  product_id: string; // CartItems.product_id
  quantity: number; // CartItems.quantity
  name: string; // From Products.name
  unit_price: number; // From Products.unit_price
  discount: number; // From Products.discount
}

// Interface for a Customer's saved payment method
// Based on PaymentMethods model and customer_routes.py GET response
interface PaymentMethod {
  id: string; // PaymentMethods.id
  card_number: string; // Masked, e.g., "************1234"
  expiration_month: number;
  expiration_year: number;
  is_default: boolean;
}

// Interface for a Customer's active showing
// A frontend-friendly representation of CustomerShowings model
interface CustomerShowing {
  id: string; // CustomerShowings.id
  movie_title: string; // Joined from Movies.title
  seat_info: string; // Joined from Seats (e.g., "Auditorium 3, Seat A12")
  start_time: string; // Joined from MovieShowings.start_time
}

// --- Main Checkout Page Component ---

export default function CheckoutPage() {
  const router = useRouter();
  const CUSTOMER_ID = "123"; // Placeholder for logged-in user ID

  // --- 2. Define All Necessary State Variables ---

  // Data states
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([]);
  const [customerShowings, setCustomerShowings] = useState<CustomerShowing[]>(
    []
  );

  // Selection states
  const [selectedShowingId, setSelectedShowingId] = useState<string | null>(
    null
  );
  const [selectedPaymentMethodId, setSelectedPaymentMethodId] = useState<
    string | null
  >(null);

  // Loading and error states
  const [isLoading, setIsLoading] = useState(true);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // --- 3. Model API Calls (based on *_routes.py) ---

  useEffect(() => {
    // Fetches all necessary data for the checkout page
    const fetchCheckoutData = async () => {
      setIsLoading(true);
      setError(null);
      try {
        // --- Fetch Cart Items ---
        // This models a GET /api/customers/<id>/cart endpoint
        // (Implied by customer_service.get_cart_items)
        const cartResponse = await fetch(
          `https://PICKLE.COM/api/customers/${CUSTOMER_ID}/cart`,
          { method: "GET" }
        );
        if (!cartResponse.ok) throw new Error("Failed to fetch cart items.");
        // Mocked successful response (as we can't call PICKLE.COM)
        const cartData: CartItem[] = [
          {
            id: "ci1",
            product_id: "p1",
            name: "Large Popcorn",
            unit_price: 12.5,
            discount: 1.0,
            quantity: 1,
          },
          {
            id: "ci2",
            product_id: "p2",
            name: "Soda",
            unit_price: 5.0,
            discount: 0.0,
            quantity: 2,
          },
        ];
        // In real app: const cartData = await cartResponse.json();
        setCartItems(cartData);

        // --- Fetch Payment Methods ---
        // This matches GET /api/customers/<id>/payment-methods in customer_routes.py
        const paymentResponse = await fetch(
          `https://PICKLE.COM/api/customers/${CUSTOMER_ID}/payment-methods`,
          { method: "GET" }
        );
        if (!paymentResponse.ok)
          throw new Error("Failed to fetch payment methods.");
        // Mocked successful response
        const paymentData: { payment_methods: PaymentMethod[] } = {
          payment_methods: [
            {
              id: "pm1",
              card_number: "************1234",
              expiration_month: 12,
              expiration_year: 2028,
              is_default: true,
            },
            {
              id: "pm2",
              card_number: "************5678",
              expiration_month: 6,
              expiration_year: 2026,
              is_default: false,
            },
          ],
        };
        // In real app: const paymentData = await paymentResponse.json();
        setPaymentMethods(paymentData.payment_methods);
        // Automatically select the default payment method
        const defaultPayment = paymentData.payment_methods.find(
          (pm) => pm.is_default
        );
        if (defaultPayment) {
          setSelectedPaymentMethodId(defaultPayment.id);
        }

        // --- Fetch Customer Showings ---
        // This models a GET /api/customers/<id>/showings endpoint
        // (Implied by the need to create a delivery for a showing)
        const showingResponse = await fetch(
          `https://PICKLE.COM/api/customers/${CUSTOMER_ID}/showings`,
          { method: "GET" }
        );
        if (!showingResponse.ok)
          throw new Error("Failed to fetch active showings.");
        // Mocked successful response
        const showingData: CustomerShowing[] = [
          {
            id: "cs1",
            movie_title: "Dune: Part Two",
            seat_info: "Auditorium 1, Seat D12",
            start_time: "2025-11-06T19:30:00Z",
          },
          {
            id: "cs2",
            movie_title: "The Matrix",
            seat_info: "Auditorium 4, Seat F9",
            start_time: "2025-11-06T21:00:00Z",
          },
        ];
        // In real app: const showingData = await showingResponse.json();
        setCustomerShowings(showingData);
        if (showingData.length > 0) {
          setSelectedShowingId(showingData[0].id); // Default to first showing
        }
      } catch (error) {
        setError(
          error instanceof Error ? error.message : "An unknown error occurred"
        );
      } finally {
        setIsLoading(false);
      }
    };

    fetchCheckoutData();
  }, []); // Runs once on component mount

  // --- 4. Calculate Order Summary ---
  const orderSummary = useMemo(() => {
    // This calculation is based on customer_service.calculate_total_price
    const subtotal = cartItems.reduce((acc, item) => {
      const itemPrice = item.unit_price - item.discount;
      return acc + itemPrice * item.quantity;
    }, 0);

    // In this model, tax and shipping are simplified.
    // The backend `Deliveries` model has a `total_price`
    // which is calculated in `charge_payment_method`.
    // We'll mimic that simple calculation.
    const tax = subtotal * 0.08; // 8% tax
    const total = subtotal + tax;
    return { subtotal, tax, total };
  }, [cartItems]);

  // --- 5. Handle Order Submission (Create Delivery) ---

  const handlePlaceOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedShowingId || !selectedPaymentMethodId) {
      setError(
        "Please select a showing and a payment method to place your order."
      );
      return;
    }

    setIsProcessing(true);
    setError(null);

    // This payload matches the requirements for `create_delivery`
    // in customer_service.py and customer_routes.py
    const orderPayload = {
      customer_showing_id: selectedShowingId,
      payment_method_id: selectedPaymentMethodId,
      // driver_id and staff_id are set by the service, not the customer
    };

    try {
      // This models the POST /api/deliveries API call
      const response = await fetch("https://PICKLE.COM/api/deliveries", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(orderPayload),
      });

      if (response.status === 402) {
        // Handle "Insufficient funds" as per customer_routes.py
        throw new Error("Insufficient funds. Please try a different card.");
      }

      if (!response.ok) {
        throw new Error("Failed to place order. Please try again.");
      }

      // Mocked successful response
      const orderData = {
        message: "Delivery created successfully",
        delivery_id: "d12345",
        total_price: orderSummary.total,
      };
      // In real app: const orderData = await response.json();

      alert(`Order placed successfully! Delivery ID: ${orderData.delivery_id}`);
      // On success, redirect to an order confirmation page
      router.push(`/order-confirmation/${orderData.delivery_id}`);
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to place order.");
    } finally {
      setIsProcessing(false);
    }
  };

  // --- 6. Render Helper Components ---

  const renderOrderSummary = () => {
    if (cartItems.length === 0) {
      return <p className="text-gray-500">Your cart is empty.</p>;
    }
    return (
      <div className="space-y-4">
        <div className="space-y-3">
          {cartItems.map((item) => (
            <div key={item.id} className="flex justify-between items-center text-sm">
              <div>
                <p className="font-medium text-gray-800">{item.name}</p>
                <p className="text-gray-500">Qty: {item.quantity}</p>
              </div>
              <p className="text-gray-800">
                ${((item.unit_price - item.discount) * item.quantity).toFixed(2)}
              </p>
            </div>
          ))}
        </div>
        <div className="border-t border-gray-200 pt-4 space-y-2 text-sm">
          <div className="flex justify-between">
            <p className="text-gray-600">Subtotal</p>
            <p className="text-gray-800">${orderSummary.subtotal.toFixed(2)}</p>
          </div>
          <div className="flex justify-between">
            <p className="text-gray-600">Tax</p>
            <p className="text-gray-800">${orderSummary.tax.toFixed(2)}</p>
          </div>
          <div className="flex justify-between text-base font-semibold border-t border-gray-200 pt-2 mt-2">
            <p>Total</p>
            <p>${orderSummary.total.toFixed(2)}</p>
          </div>
        </div>
      </div>
    );
  };

  if (isLoading) {
    return (
      <div className="text-center py-20 text-gray-600">Loading checkout...</div>
    );
  }

  // --- 7. Main Component Render ---

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-extrabold text-gray-900 mb-8 text-center">
        Checkout
      </h1>

      {error && !isProcessing && (
        <div className="max-w-3xl mx-auto bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
          <p>{error}</p>
        </div>
      )}

      <form
        onSubmit={handlePlaceOrder}
        className="flex flex-col lg:flex-row gap-10"
      >
        {/* Delivery & Payment Selection */}
        <div className="flex-1 space-y-10">
          {/* --- Delivery Location (Showings) --- */}
          <section className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
            <h2 className="text-xl font-semibold mb-4 border-b pb-2">
              Deliver To
            </h2>
            {customerShowings.length > 0 ? (
              <div className="space-y-4">
                {customerShowings.map((showing) => (
                  <label
                    key={showing.id}
                    className="flex items-center p-4 border rounded-lg has-[:checked]:bg-indigo-50 has-[:checked]:border-indigo-500 transition-colors cursor-pointer"
                  >
                    <input
                      type="radio"
                      name="customerShowing"
                      value={showing.id}
                      checked={selectedShowingId === showing.id}
                      onChange={(e) => setSelectedShowingId(e.target.value)}
                      className="h-4 w-4 text-indigo-600 border-gray-300 focus:ring-indigo-500"
                    />
                    <div className="ml-3 text-sm">
                      <p className="font-medium text-gray-900">
                        {showing.movie_title}
                      </p>
                      <p className="text-gray-600">{showing.seat_info}</p>
                      <p className="text-gray-500 text-xs">
                        {new Date(showing.start_time).toLocaleString()}
                      </p>
                    </div>
                  </label>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">
                You have no active showings to deliver to.
              </p>
            )}
          </section>

          {/* --- Payment Method --- */}
          <section className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
            <h2 className="text-xl font-semibold mb-4 border-b pb-2">
              Payment Method
            </h2>
            {paymentMethods.length > 0 ? (
              <div className="space-y-4">
                {paymentMethods.map((pm) => (
                  <label
                    key={pm.id}
                    className="flex items-center p-4 border rounded-lg has-[:checked]:bg-indigo-50 has-[:checked]:border-indigo-500 transition-colors cursor-pointer"
                  >
                    <input
                      type="radio"
                      name="paymentMethod"
                      value={pm.id}
                      checked={selectedPaymentMethodId === pm.id}
                      onChange={(e) =>
                        setSelectedPaymentMethodId(e.target.value)
                      }
                      className="h-4 w-4 text-indigo-600 border-gray-300 focus:ring-indigo-500"
                    />
                    <div className="ml-3 text-sm">
                      <p className="font-medium text-gray-900">
                        Card ending in {pm.card_number.slice(-4)}
                      </p>
                      <p className="text-gray-600">
                        Expires: {pm.expiration_month}/{pm.expiration_year}
                      </p>
                    </div>
                  </label>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">
                You have no saved payment methods.
              </p>
            )}
          </section>
        </div>

        {/* Order Summary & Actions */}
        <div className="lg:w-96">
          <section className="bg-white p-6 rounded-xl shadow-lg border border-gray-200 sticky top-4">
            <h2 className="text-xl font-semibold mb-4 border-b pb-2">
              Your Order
            </h2>

            {renderOrderSummary()}

            {error && isProcessing && (
              <p className="text-red-600 text-sm mt-4 text-center">{error}</p>
            )}

            <button
              type="submit"
              disabled={
                isProcessing ||
                isLoading ||
                cartItems.length === 0 ||
                !selectedShowingId ||
                !selectedPaymentMethodId
              }
              className={`w-full mt-6 px-6 py-3 text-lg font-bold text-white rounded-xl transition-colors ${isProcessing || isLoading || cartItems.length === 0 || !selectedShowingId || !selectedPaymentMethodId
                ? "bg-indigo-300 cursor-not-allowed"
                : "bg-indigo-600 hover:bg-indigo-700"
                }`}
            >
              {isProcessing ? "Processing..." : "Place Order"}
            </button>

            <Link
              href="/cart"
              className="block mt-4 text-center text-sm text-indigo-600 hover:text-indigo-800 transition"
            >
              ← Back to Cart
            </Link>
          </section>
        </div>
      </form>
    </div>
  );
}