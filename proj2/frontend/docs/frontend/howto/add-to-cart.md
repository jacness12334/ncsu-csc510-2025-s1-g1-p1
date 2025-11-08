# Add an Item to Cart and Show Quantity in UI

## When to use this

Use this guide when implementing shopping cart functionality where users can add menu items to their cart and see real-time quantity updates in the UI. This pattern works for any product catalog where users browse items and build up a cart before checkout.

## Prerequisites

- Next.js app with Zustand store configured
- `useCartStore` hook available from `@/lib/cartStore`
- `MenuItem` type defined in `@/lib/types`
- API endpoints configured with `NEXT_PUBLIC_API_BASE_URL`
- `CartApiService` available from `@/lib/cartApi`

## Step-by-step

1. **Import the necessary dependencies in your component**

```typescript
"use client";
import { useState } from "react";
import { useCartStore } from "@/lib/cartStore";
import type { MenuItem } from "@/lib/types";
```

2. **Set up the cart store hooks in your component**

```typescript
export default function ProductCard({ item }: { item: MenuItem }) {
  const { add, getQty, isLoading, error } = useCartStore();
  const [isAdding, setIsAdding] = useState(false);
  
  // Get current quantity for this item
  const currentQty = getQty(item.id);
```

3. **Create the add to cart handler function**

```typescript
  const handleAddToCart = async (quantity: number = 1) => {
    if (isAdding || isLoading) return;
    
    setIsAdding(true);
    try {
      await add(item, quantity);
    } catch (err) {
      console.error("Failed to add item to cart:", err);
      // Handle error in UI if needed
    } finally {
      setIsAdding(false);
    }
  };
```

4. **Implement conditional rendering for cart states**

```typescript
  const renderCartButton = () => {
    if (currentQty === 0) {
      return (
        <button
          onClick={() => handleAddToCart(1)}
          disabled={isAdding || isLoading || !item.available}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {isAdding ? "Adding..." : "Add to Cart"}
        </button>
      );
    }

    return (
      <div className="flex items-center gap-2">
        <button
          onClick={() => useCartStore.getState().decrement(item.id, 1)}
          disabled={isLoading}
          className="w-8 h-8 rounded border flex items-center justify-center"
        >
          −
        </button>
        <span className="min-w-[2ch] text-center">{currentQty}</span>
        <button
          onClick={() => handleAddToCart(1)}
          disabled={isLoading}
          className="w-8 h-8 rounded border flex items-center justify-center"
        >
          +
        </button>
      </div>
    );
  };
```

5. **Add error handling display**

```typescript
  if (error) {
    return (
      <div className="p-4 border border-red-300 rounded bg-red-50">
        <p className="text-red-700">Error: {error}</p>
        <button
          onClick={() => useCartStore.getState().setError(null)}
          className="text-red-600 underline text-sm"
        >
          Dismiss
        </button>
      </div>
    );
  }
```

6. **Implement the complete component JSX**

```typescript
  return (
    <div className="border rounded-lg p-4 shadow-sm">
      <h3 className="font-semibold text-lg">{item.name}</h3>
      <p className="text-gray-600 text-sm">{item.description}</p>
      <div className="flex justify-between items-center mt-4">
        <span className="font-bold text-lg">${item.price.toFixed(2)}</span>
        {renderCartButton()}
      </div>
      {!item.available && (
        <p className="text-red-500 text-sm mt-2">Currently unavailable</p>
      )}
    </div>
  );
}
```

7. **Add optimistic UI updates for better UX**

```typescript
const handleOptimisticAdd = async (quantity: number = 1) => {
  // Optimistically update local state
  const optimisticItem = { ...item, qty: currentQty + quantity };
  
  try {
    await add(item, quantity);
  } catch (err) {
    // Revert optimistic update on error
    console.error("Failed to add item, reverting:", err);
  }
};
```

8. **Setup cart total indicator (optional)**

```typescript
export function CartTotalIndicator() {
  const { items } = useCartStore();
  const totalItems = items.reduce((sum, item) => sum + item.qty, 0);
  
  if (totalItems === 0) return null;
  
  return (
    <div className="fixed top-4 right-4 bg-blue-600 text-white px-3 py-1 rounded-full">
      Cart ({totalItems})
    </div>
  );
}
```

## Common pitfalls

- **Not handling loading states**: Always disable buttons during API calls to prevent double-submissions
- **Missing error boundaries**: Wrap cart operations in try-catch blocks and display errors to users
- **Forgetting to check item availability**: Always verify `item.available` before allowing additions
- **State synchronization issues**: Use the store's `getQty()` method rather than maintaining separate local state
- **Not handling concurrent updates**: Use the store's loading state to prevent race conditions

## Quick test checklist

- [ ] Click "Add to Cart" and verify quantity increases in UI immediately
- [ ] Verify increment/decrement buttons work correctly  
- [ ] Test that unavailable items cannot be added to cart
- [ ] Confirm loading states prevent double-clicks
- [ ] Check that errors are displayed and dismissible