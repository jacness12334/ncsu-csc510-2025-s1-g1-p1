// lib/sampleData.ts
import type { MenuItem } from "./types";

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
