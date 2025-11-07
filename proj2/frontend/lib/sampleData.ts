// lib/sampleData.ts
import type { MenuItem, PaymentMethod } from "./types";

/**
 * Sample menu data for development and testing purposes
 * Provides a representative set of movie theater concession items
 * 
 * @example
 * ```typescript
 * import { MENU } from "@/lib/sampleData";
 * 
 * // Filter by category
 * const snacks = MENU.filter(item => item.category === "Snacks");
 * 
 * // Find specific item
 * const popcorn = MENU.find(item => item.id === "popcorn-sm");
 * ```
 */
export const MENU: MenuItem[] = [
  {
    id: "popcorn-sm",
    name: "Classic Butter Popcorn",
    description: "Fresh & buttery",
    price: 6.99,
    category: "Snacks",
  },
  {
    id: "nachos",
    name: "Nachos with Cheese",
    description: "Crispy chips + cheddar dip",
    price: 7.49,
    category: "Snacks",
  },
  {
    id: "pretzel-bites",
    name: "Pretzel Bites",
    description: "Soft baked bites + warm cheese",
    price: 5.99,
    category: "Snacks",
  },
  {
    id: "soda-md",
    name: "Soda (Medium)",
    description: "Coke, Diet, Sprite, Fanta",
    price: 3.99,
    category: "Beverages",
  },
  {
    id: "water",
    name: "Bottled Water",
    description: "16.9 fl oz",
    price: 2.49,
    category: "Beverages",
  },
  {
    id: "cookie",
    name: "Chocolate Chip Cookie",
    description: "Freshly baked",
    price: 3.49,
    category: "Desserts",
  },
];

// Sample payment methods for testing
export const SAMPLE_PAYMENT_METHODS: PaymentMethod[] = [
  {
    id: "pm_1",
    customer_id: "1",
    card_number: "1234567812345678",
    expiration_month: 12,
    expiration_year: 2026,
    billing_address: "123 Main St, Raleigh, NC 27606",
    balance: 150.00,
    is_default: false,
    date_added: new Date().toISOString(),
    last_updated: new Date().toISOString(),
  },
  {
    id: "pm_2", 
    customer_id: "1",
    card_number: "9876543298765432",
    expiration_month: 8,
    expiration_year: 2027,
    billing_address: "456 Oak Ave, Durham, NC 27701",
    balance: 75.50,
    is_default: false,
    date_added: new Date().toISOString(),
    last_updated: new Date().toISOString(),
  },
  {
    id: "pm_3",
    customer_id: "1", 
    card_number: "5555444433332222",
    expiration_month: 3,
    expiration_year: 2028,
    billing_address: "789 Pine St, Chapel Hill, NC 27514",
    balance: 200.75,
    is_default: false,
    date_added: new Date().toISOString(),
    last_updated: new Date().toISOString(),
  },
];
