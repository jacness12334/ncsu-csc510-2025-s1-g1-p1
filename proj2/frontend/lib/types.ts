// Represents a single food or drink item available in the menu
export type NutritionInfo = {
  calories: number;
  protein?: number;
  carbs?: number;
  fat?: number;
};

// Basic menu item used in the concessions or restaurant menus
export type MenuItem = {
  id: string;
  name: string;
  description?: string;
  price: number;
  image?: string;
  nutrition?: NutritionInfo;
  category?: string;     // e.g. "Snacks", "Drinks", "Combos"
  available?: boolean;   // optional flag for future use
};

// Items added to the shopping cart
export type CartItem = {
  id: string;
  name: string;
  price: number;
  qty: number;
};

// Optional: for tracking orders (you can use later if needed)
export type Order = {
  id: string;
  items: CartItem[];
  total: number;
  status?: "pending" | "preparing" | "ready" | "delivered";
  createdAt?: string;
};

// Optional: for restaurant or concession data (for your “Order” page)
export type Restaurant = {
  id: string;
  name: string;
  description?: string;
  image?: string;
  isActive: boolean;
  type: "concession" | "restaurant";
};
