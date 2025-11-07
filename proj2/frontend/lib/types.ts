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
