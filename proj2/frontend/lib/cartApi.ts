// lib/cartApi.ts
import type { CartItem } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

// Default customer ID (in production, this should come from authentication)
const DEFAULT_CUSTOMER_ID = "1";

/**
 * Interface representing cart item data structure from the backend API
 * @interface BackendCartItem
 */
export interface BackendCartItem {
  /** Unique cart item identifier */
  id: string;
  /** ID of the customer who owns this cart item */
  customer_id: string;
  /** ID of the product in the cart */
  product_id: string;
  /** Quantity of the product in the cart */
  quantity: number;
  /** Optional populated product information */
  product?: {
    /** Product unique identifier */
    id: string;
    /** Product display name */
    name: string;
    /** Product unit price */
    unit_price: number;
    /** Product category */
    category: string;
    /** Product availability status */
    is_available: boolean;
  };
}

/**
 * Service class for handling cart-related API operations
 * Provides methods to interact with the backend cart management system
 */
export class CartApiService {
  /**
   * Retrieves all cart items for a specific customer from the backend
   * Transforms backend cart item format to frontend CartItem format
   * 
   * @param customerId - Customer ID to fetch cart for (defaults to "1")
   * @returns Promise resolving to array of cart items
   * @throws Error when API request fails or returns invalid data
   * 
   * @example
   * ```typescript
   * try {
   *   const cartItems = await CartApiService.getCartItems("customer123");
   *   console.log(`Cart has ${cartItems.length} items`);
   * } catch (error) {
   *   console.error("Failed to load cart:", error);
   * }
   * ```
   */
  static async getCartItems(customerId: string = DEFAULT_CUSTOMER_ID): Promise<CartItem[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/customers/${customerId}/cart`);
      if (!response.ok) {
        throw new Error("Failed to fetch cart items");
      }
      
      const backendItems: BackendCartItem[] = await response.json();
      
      // Transform backend cart items to frontend format
      return backendItems.map(item => ({
        id: item.product?.id || item.product_id,
        name: item.product?.name || `Product ${item.product_id}`,
        price: item.product?.unit_price || 0,
        qty: item.quantity,
      }));
    } catch (error) {
      console.error("Error fetching cart items:", error);
      throw error; // Let the UI handle empty cart state
    }
  }

  /**
   * Adds a product to the customer's cart with specified quantity
   * 
   * @param customerId - Customer ID to add item for
   * @param productId - ID of the product to add to cart
   * @param quantity - Quantity of the product to add
   * @returns Promise resolving to the created cart item
   * @throws Error when API request fails or product is unavailable
   * 
   * @example
   * ```typescript
   * try {
   *   const cartItem = await CartApiService.addToCart("customer123", "popcorn-lg", 2);
   *   console.log("Added item to cart:", cartItem);
   * } catch (error) {
   *   console.error("Failed to add item:", error);
   * }
   * ```
   */
  static async addToCart(
    customerId: string = DEFAULT_CUSTOMER_ID,
    productId: string,
    quantity: number = 1
  ): Promise<BackendCartItem> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/customers/${customerId}/cart`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          product_id: productId,
          quantity: quantity,
        }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to add item to cart");
      }
      
      return await response.json();
    } catch (error) {
      console.error("Error adding to cart:", error);
      throw error;
    }
  }

  // Update cart item quantity
  static async updateCartItem(cartItemId: string, quantity: number): Promise<BackendCartItem> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/cart/${cartItemId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ quantity }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to update cart item");
      }
      
      return await response.json();
    } catch (error) {
      console.error("Error updating cart item:", error);
      throw error;
    }
  }

  // Remove item from cart
  static async removeCartItem(cartItemId: string): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/cart/${cartItemId}`, {
        method: "DELETE",
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to remove cart item");
      }
    } catch (error) {
      console.error("Error removing cart item:", error);
      throw error;
    }
  }

  // Clear all cart items for a customer
  static async clearCart(customerId: string = DEFAULT_CUSTOMER_ID): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/customers/${customerId}/cart`, {
        method: "DELETE",
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to clear cart");
      }
    } catch (error) {
      console.error("Error clearing cart:", error);
      throw error;
    }
  }

  // Get available products (for adding to cart)
  static async getProducts(): Promise<Array<{
    id: string;
    name: string;
    unit_price: number;
    category: string;
    is_available: boolean;
    supplier_id: string;
    inventory_quantity: number;
  }>> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/products`);
      if (!response.ok) {
        throw new Error("Failed to fetch products");
      }
      return await response.json();
    } catch (error) {
      console.error("Error fetching products:", error);
      throw error; // Let the UI handle error state properly
    }
  }
}