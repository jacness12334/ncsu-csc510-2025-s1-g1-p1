// lib/types.ts

export type Purchasable = { id: string; name: string; price: number };

export type MenuItem = {
  id: string;
  name: string;
  description?: string;
  price: number;
  image?: string;
  category?: string;   // "Snacks", "Beverages", "Desserts", etc.
  available?: boolean;
};

export type CartItem = {
  id: string;
  name: string;
  price: number;
  qty: number;
};

export type PaymentMethod = {
  id: string;
  customer_id: string;
  card_number: string; // last 4 digits only for display
  expiration_month: number;
  expiration_year: number;
  billing_address: string;
  balance: number;
  is_default: boolean;
  date_added?: string;
  last_updated?: string;
};

export type CustomerShowing = {
  id: string;
  customer_id: string;
  movie_showing_id: string;
  seat_id: string;
  date_added?: string;
};

export type DeliveryOrder = {
  id: string;
  driver_id?: string;
  customer_showing_id: string;
  payment_method_id: string;
  staff_id?: string;
  payment_status: 'pending' | 'completed' | 'failed';
  total_price: number;
  delivery_time?: string;
  delivery_status: 'pending' | 'accepted' | 'in_progress' | 'ready_for_pickup' | 'in_transit' | 'delivered' | 'fulfilled' | 'cancelled';
  date_added?: string;
  last_updated?: string;
};

export type DeliveryItem = {
  id: string;
  product_id: string;
  delivery_id: string;
  quantity: number;
  discount: number;
};
