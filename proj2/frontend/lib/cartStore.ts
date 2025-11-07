"use client";
import { create } from "zustand";
import type { CartItem, Purchasable } from "./types";
import { CartApiService } from "./cartApi";

/**
 * Cart state interface defining the structure of the shopping cart store
 * @interface CartState
 */
type CartState = {
  /** Array of items currently in the cart */
  items: CartItem[];
  /** Loading state for async operations */
  isLoading: boolean;
  /** Current error message, null if no error */
  error: string | null;
  /** Maps product IDs to backend cart item IDs */
  cartItemMap: Map<string, string>;
  
  // Actions
  /** Loads cart items from the backend API */
  loadCart(): Promise<void>;
  /** Adds an item to the cart with specified quantity */
  add(item: Purchasable, qty?: number): Promise<void>;
  /** Increases quantity of an existing cart item */
  increment(id: string, qty?: number): Promise<void>;
  /** Decreases quantity of an existing cart item */
  decrement(id: string, qty?: number): Promise<void>;
  /** Removes an item completely from the cart */
  remove(id: string): Promise<void>;
  /** Removes all items from the cart */
  clear(): Promise<void>;
  /** Gets the current quantity of a specific item */
  getQty(id: string): number;
  
  // Internal state management
  /** Updates the loading state */
  setLoading(loading: boolean): void;
  /** Updates the error state */
  setError(error: string | null): void;
  /** Updates the cart items array */
  setItems(items: CartItem[]): void;
};

/**
 * Zustand store for managing shopping cart state and operations
 * Provides reactive state management for cart items with backend synchronization
 * 
 * @example
 * ```typescript
 * const { items, add, remove, getQty } = useCartStore();
 * 
 * // Add item to cart
 * await add({ id: "popcorn", name: "Popcorn", price: 6.99 }, 2);
 * 
 * // Get quantity of specific item
 * const quantity = getQty("popcorn");
 * 
 * // Remove item from cart
 * await remove("popcorn");
 * ```
 */
export const useCartStore = create<CartState>((set, get) => ({
  items: [], // Empty cart initially - will be loaded from backend
  isLoading: false,
  error: null,
  cartItemMap: new Map(),

  // Load cart from backend
  loadCart: async () => {
    const { setLoading, setError, setItems } = get();
    try {
      setLoading(true);
      setError(null);
      const items = await CartApiService.getCartItems();
      setItems(items);
    } catch (error) {
      const err = error as Error;
      setError(err.message || "Failed to load cart");
    } finally {
      setLoading(false);
    }
  },

  // Add item to cart (calls backend)
  add: async (item: Purchasable, qty = 1) => {
    const { setLoading, setError, loadCart } = get();
    try {
      setLoading(true);
      setError(null);
      await CartApiService.addToCart("1", item.id, qty);
      await loadCart(); // Refresh cart from backend
    } catch (error) {
      const err = error as Error;
      setError(err.message || "Failed to add item to cart");
    } finally {
      setLoading(false);
    }
  },

  // Increment item quantity
  increment: async (id: string, qty = 1) => {
    const { items, setLoading, setError, loadCart } = get();
    const item = items.find(i => i.id === id);
    if (!item) return;

    try {
      setLoading(true);
      setError(null);
      // In a real implementation, you'd need the cart_item_id from backend
      // For now, we'll simulate by calling add
      await CartApiService.addToCart("1", id, qty);
      await loadCart();
    } catch (error) {
      const err = error as Error;
      setError(err.message || "Failed to update item quantity");
    } finally {
      setLoading(false);
    }
  },

  // Decrement item quantity
  decrement: async (id: string, qty = 1) => {
    const { items, setLoading, setError, loadCart } = get();
    const item = items.find(i => i.id === id);
    if (!item) return;

    try {
      setLoading(true);
      setError(null);
      
      if (item.qty <= qty) {
        // Remove item completely if quantity would be 0 or less
        await get().remove(id);
      } else {
        // Update quantity (would need cart_item_id in real implementation)
        // For now, we'll simulate by reloading
        await loadCart();
      }
    } catch (error) {
      const err = error as Error;
      setError(err.message || "Failed to update item quantity");
    } finally {
      setLoading(false);
    }
  },

  // Remove item from cart
  remove: async (id: string) => {
    const { setLoading, setError, loadCart } = get();
    try {
      setLoading(true);
      setError(null);
      // In real implementation, would use actual cart_item_id
      // For now, we'll simulate by filtering locally and then reloading
      set((s) => ({ items: s.items.filter((i) => i.id !== id) }));
      // await CartApiService.removeCartItem(cartItemId);
      await loadCart();
    } catch (error) {
      const err = error as Error;
      setError(err.message || "Failed to remove item from cart");
    } finally {
      setLoading(false);
    }
  },

  // Clear entire cart
  clear: async () => {
    const { setLoading, setError } = get();
    try {
      setLoading(true);
      setError(null);
      await CartApiService.clearCart();
      set({ items: [] });
    } catch (error) {
      const err = error as Error;
      setError(err.message || "Failed to clear cart");
    } finally {
      setLoading(false);
    }
  },

  // Get quantity of specific item
  getQty: (id: string) => get().items.find((i) => i.id === id)?.qty ?? 0,

  // Internal state management
  setLoading: (loading: boolean) => set({ isLoading: loading }),
  setError: (error: string | null) => set({ error }),
  setItems: (items: CartItem[]) => set({ items }),
}));
