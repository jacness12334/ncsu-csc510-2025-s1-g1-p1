// lib/types.ts

/**
 * Base interface for items that can be purchased
 * @interface Purchasable
 */
export type Purchasable = { 
  /** Unique identifier for the purchasable item */
  id: string; 
  /** Display name of the item */
  name: string; 
  /** Price of the item in currency units */
  price: number; 
};

/**
 * Represents a menu item available for purchase at the movie theater
 * @interface MenuItem
 */
export type MenuItem = {
  /** Unique identifier for the menu item */
  id: string;
  /** Display name of the menu item */
  name: string;
  /** Optional description of the menu item */
  description?: string;
  /** Price of the menu item in currency units */
  price: number;
  /** Optional URL to the item's image */
  image?: string;
  /** Category classification (e.g., "Snacks", "Beverages", "Desserts") */
  category?: string;
  /** Whether the item is currently available for purchase */
  available?: boolean;
};

/**
 * Represents an item in the shopping cart with quantity information
 * @interface CartItem
 */
export type CartItem = {
  /** Unique identifier matching the original product ID */
  id: string;
  /** Display name of the cart item */
  name: string;
  /** Unit price of the item */
  price: number;
  /** Quantity of this item in the cart */
  qty: number;
};

/**
 * Represents a customer's payment method for processing transactions
 * @interface PaymentMethod
 */
export type PaymentMethod = {
  /** Unique identifier for the payment method */
  id: string;
  /** ID of the customer who owns this payment method */
  customer_id: string;
  /** Last 4 digits of the card number for display purposes */
  card_number: string;
  /** Expiration month (1-12) */
  expiration_month: number;
  /** Expiration year (YYYY format) */
  expiration_year: number;
  /** Billing address associated with the card */
  billing_address: string;
  /** Available balance on the payment method */
  balance: number;
  /** Whether this is the customer's default payment method */
  is_default: boolean;
  /** ISO timestamp when the payment method was added */
  date_added?: string;
  /** ISO timestamp when the payment method was last updated */
  last_updated?: string;
};

/**
 * Represents a customer's reservation for a specific movie showing
 * @interface CustomerShowing
 */
export type CustomerShowing = {
  /** Unique identifier for the customer showing record */
  id: string;
  /** ID of the customer */
  customer_id: string;
  /** ID of the movie showing */
  movie_showing_id: string;
  /** ID of the reserved seat */
  seat_id: string;
  /** ISO timestamp when the reservation was made */
  date_added?: string;
};

/**
 * Represents a delivery order for movie theater concessions
 * @interface DeliveryOrder
 */
export type DeliveryOrder = {
  /** Unique identifier for the delivery order */
  id: string;
  /** Optional ID of the assigned delivery driver */
  driver_id?: string;
  /** ID of the customer showing this order is for */
  customer_showing_id: string;
  /** ID of the payment method used */
  payment_method_id: string;
  /** Optional ID of the staff member handling the order */
  staff_id?: string;
  /** Current payment processing status */
  payment_status: 'pending' | 'completed' | 'failed';
  /** Total price of the order including taxes and fees */
  total_price: number;
  /** Optional estimated or actual delivery time */
  delivery_time?: string;
  /** Current delivery status */
  delivery_status: 'pending' | 'accepted' | 'in_progress' | 'ready_for_pickup' | 'in_transit' | 'delivered' | 'fulfilled' | 'cancelled';
  /** ISO timestamp when the order was created */
  date_added?: string;
  /** ISO timestamp when the order was last updated */
  last_updated?: string;
};

/**
 * Represents an individual item within a delivery order
 * @interface DeliveryItem
 */
export type DeliveryItem = {
  /** Unique identifier for the delivery item */
  id: string;
  /** ID of the product being delivered */
  product_id: string;
  /** ID of the parent delivery order */
  delivery_id: string;
  /** Quantity of this product in the delivery */
  quantity: number;
  /** Discount amount applied to this item */
  discount: number;
};
