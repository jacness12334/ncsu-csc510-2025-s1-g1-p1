// lib/types.ts

export type Purchasable = { id: string; name: string; price: number };

export type NutritionInfo = {
  calories: number;
  protein?: number;
  carbs?: number;
  fat?: number;
  servingSize?: string; // e.g., "per person", "per tray", "16 oz"
};

export type MenuItem = {
  id: string;
  name: string;
  description?: string;
  price: number;
  image?: string;
  nutrition?: NutritionInfo;
  category?: string;   // "Snacks", "Beverages", "Desserts", etc.
  available?: boolean;
};

/** Premade bundle sold as a single item */
export type BundleItem = {
  id: string;
  name: string;
  description?: string;
  price: number;
  image?: string;
  serves: number;                     // people
  perPersonNutrition: NutritionInfo;  // nutrition per person
  includes: string[];                 // what's inside the bundle
};

export type CartItem = {
  id: string;
  name: string;
  price: number;
  qty: number;
};
