# Complete Checkout with Default Payment Method

## When to use this

Use this guide when implementing a streamlined checkout flow that automatically uses the customer's default payment method. This pattern is ideal for repeat customers who want quick purchases without re-entering payment details.

## Prerequisites

- `CheckoutApiService` configured with API endpoints
- `PaymentMethod` and `CartItem` types from `@/lib/types`
- `useCartStore` for accessing cart state
- Customer authentication system in place
- Default payment method already saved for the customer

## Step-by-step

1. **Set up the checkout component with required state**

```typescript
"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useCartStore } from "@/lib/cartStore";
import { CheckoutApiService } from "@/lib/checkoutApi";
import type { PaymentMethod, CartItem } from "@/lib/types";

export default function QuickCheckout() {
  const router = useRouter();
  const { items, clear: clearCart } = useCartStore();
  const [defaultPayment, setDefaultPayment] = useState<PaymentMethod | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
```

2. **Load the default payment method on component mount**

```typescript
  useEffect(() => {
    const loadDefaultPayment = async () => {
      try {
        const paymentMethods = await CheckoutApiService.getPaymentMethods();
        const defaultMethod = paymentMethods.find(pm => pm.is_default);
        
        if (!defaultMethod) {
          setError("No default payment method found. Please add a payment method.");
          return;
        }
        
        setDefaultPayment(defaultMethod);
      } catch (err) {
        setError("Failed to load payment methods");
        console.error("Payment method loading error:", err);
      }
    };

    loadDefaultPayment();
  }, []);
```

3. **Calculate order totals**

```typescript
  const calculateTotals = () => {
    const subtotal = items.reduce((sum, item) => sum + (item.price * item.qty), 0);
    const tax = subtotal * 0.0875; // 8.75% tax rate
    const total = subtotal + tax;
    
    return { subtotal, tax, total };
  };

  const { subtotal, tax, total } = calculateTotals();
```

4. **Create the checkout processing function**

```typescript
  const processCheckout = async () => {
    if (!defaultPayment || items.length === 0) return;
    
    setIsProcessing(true);
    setError(null);
    
    try {
      // Prepare order data
      const orderData = {
        payment_method_id: defaultPayment.id,
        items: items.map(item => ({
          product_id: item.id,
          quantity: item.qty,
          unit_price: item.price
        })),
        subtotal,
        tax,
        total
      };

      // Process the order
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";
      const response = await fetch(`${API_BASE_URL}/api/orders`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(orderData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Failed to process order");
      }

      const order = await response.json();
      
      // Clear cart and redirect to success page
      await clearCart();
      router.push(`/order-confirmation/${order.id}`);
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Checkout failed";
      setError(errorMessage);
      console.error("Checkout error:", err);
    } finally {
      setIsProcessing(false);
    }
  };
```

5. **Render the payment method display**

```typescript
  const renderPaymentMethod = () => {
    if (!defaultPayment) return null;

    return (
      <div className="border rounded-lg p-4 bg-gray-50">
        <h3 className="font-semibold mb-2">Payment Method</h3>
        <div className="flex items-center justify-between">
          <div>
            <p className="font-medium">•••• •••• •••• {defaultPayment.card_number}</p>
            <p className="text-sm text-gray-600">
              Expires {defaultPayment.expiration_month}/{defaultPayment.expiration_year}
            </p>
            <p className="text-sm text-gray-600">{defaultPayment.billing_address}</p>
          </div>
          <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
            Default
          </span>
        </div>
      </div>
    );
  };
```

6. **Create the order summary display**

```typescript
  const renderOrderSummary = () => (
    <div className="border rounded-lg p-4">
      <h3 className="font-semibold mb-4">Order Summary</h3>
      
      {items.map(item => (
        <div key={item.id} className="flex justify-between py-2">
          <span>{item.name} × {item.qty}</span>
          <span>${(item.price * item.qty).toFixed(2)}</span>
        </div>
      ))}
      
      <hr className="my-3" />
      
      <div className="space-y-1">
        <div className="flex justify-between">
          <span>Subtotal</span>
          <span>${subtotal.toFixed(2)}</span>
        </div>
        <div className="flex justify-between">
          <span>Tax</span>
          <span>${tax.toFixed(2)}</span>
        </div>
        <div className="flex justify-between font-bold text-lg">
          <span>Total</span>
          <span>${total.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
```

7. **Implement the complete checkout component**

```typescript
  if (items.length === 0) {
    return (
      <div className="max-w-md mx-auto p-6 text-center">
        <h2 className="text-xl font-semibold mb-4">Your cart is empty</h2>
        <button
          onClick={() => router.push("/menu")}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
        >
          Continue Shopping
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">Quick Checkout</h1>
      
      {error && (
        <div className="bg-red-50 border border-red-300 rounded p-4">
          <p className="text-red-700">{error}</p>
        </div>
      )}
      
      {renderOrderSummary()}
      {renderPaymentMethod()}
      
      <button
        onClick={processCheckout}
        disabled={isProcessing || !defaultPayment || items.length === 0}
        className="w-full bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isProcessing ? "Processing..." : `Place Order - $${total.toFixed(2)}`}
      </button>
    </div>
  );
}
```

8. **Add order confirmation handling**

```typescript
// Optional: Create a confirmation component
export function OrderConfirmation({ orderId }: { orderId: string }) {
  return (
    <div className="max-w-md mx-auto p-6 text-center">
      <div className="mb-4">
        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
          <svg className="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        </div>
      </div>
      <h2 className="text-xl font-semibold mb-2">Order Confirmed!</h2>
      <p className="text-gray-600 mb-4">Order #{orderId}</p>
      <button
        onClick={() => router.push(`/track/${orderId}`)}
        className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
      >
        Track Order
      </button>
    </div>
  );
}
```

## Common pitfalls

- **Missing default payment validation**: Always check if a default payment method exists before showing checkout
- **Not handling insufficient funds**: Validate payment method balance before processing if applicable
- **Cart state persistence**: Ensure cart is only cleared after successful order confirmation
- **Security considerations**: Never log or expose full payment method details in error messages
- **Race conditions**: Disable checkout button during processing to prevent duplicate orders

## Quick test checklist

- [ ] Verify default payment method loads and displays correctly (masked card number)
- [ ] Confirm order totals calculate correctly including tax
- [ ] Test checkout button is disabled when no default payment method exists
- [ ] Verify cart clears only after successful order placement
- [ ] Check error handling for failed payments and network issues