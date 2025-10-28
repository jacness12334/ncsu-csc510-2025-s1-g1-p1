"use client";
import { create } from "zustand";
import type { CartItem, Purchasable } from "./types";

type CartState = {
  items: CartItem[];
  add(item: Purchasable, qty?: number): void;
  decrement(id: string, qty?: number): void;
  remove(id: string): void;
  clear(): void;
  getQty(id: string): number;
};

export const useCartStore = create<CartState>((set, get) => ({
  items: [],

  add: (item, qty = 1) =>
    set((s) => {
      const i = s.items.findIndex((x) => x.id === item.id);
      if (i >= 0) {
        const cp = [...s.items];
        cp[i] = { ...cp[i], qty: cp[i].qty + qty };
        return { items: cp };
      }
      return { items: [...s.items, { id: item.id, name: item.name, price: item.price, qty }] };
    }),

  decrement: (id, qty = 1) =>
    set((s) => {
      const i = s.items.findIndex((x) => x.id === id);
      if (i === -1) return s;
      const cp = [...s.items];
      const newQty = cp[i].qty - qty;
      if (newQty <= 0) cp.splice(i, 1);
      else cp[i] = { ...cp[i], qty: newQty };
      return { items: cp };
    }),

  remove: (id) => set((s) => ({ items: s.items.filter((i) => i.id !== id) })),
  clear: () => set({ items: [] }),
  getQty: (id) => get().items.find((i) => i.id === id)?.qty ?? 0,
}));
