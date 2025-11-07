"use client";

import { useState, useEffect } from "react";
import { CartApiService } from "@/lib/cartApi";
import type { MenuItem } from "@/lib/types";

interface AddItemToCartProps {
  onAddItem: (item: MenuItem, quantity: number) => void;
  onClose: () => void;
}

export default function AddItemToCart({ onAddItem, onClose }: AddItemToCartProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>("All");
  const [quantities, setQuantities] = useState<Record<string, number>>({});
  const [menu, setMenu] = useState<MenuItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load menu items from backend
  useEffect(() => {
    const loadMenu = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const products = await CartApiService.getProducts();
        
        // Transform backend products to MenuItem format
        const menuItems: MenuItem[] = products.map(product => ({
          id: product.id,
          name: product.name,
          price: product.unit_price,
          category: product.category,
          available: product.is_available,
        }));
        
        setMenu(menuItems);
      } catch (err) {
        console.error("Error loading menu:", err);
        setError("Failed to load menu items. Please try again.");
      } finally {
        setIsLoading(false);
      }
    };

    loadMenu();
  }, []);

  const categories = ["All", ...Array.from(new Set(menu.map(item => item.category || "Other")))];
  
  const filteredMenu = selectedCategory === "All" 
    ? menu 
    : menu.filter(item => item.category === selectedCategory);

  const handleQuantityChange = (itemId: string, quantity: number) => {
    setQuantities(prev => ({
      ...prev,
      [itemId]: Math.max(0, quantity)
    }));
  };

  const handleAddToCart = (item: MenuItem) => {
    const quantity = quantities[item.id] || 1;
    onAddItem(item, quantity);
    
    // Reset quantity for this item
    setQuantities(prev => ({
      ...prev,
      [item.id]: 0
    }));
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
        <div className="flex items-center justify-between p-6 border-b">
          <h2 className="text-2xl font-bold">Add Items to Cart</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ×
          </button>
        </div>

        <div className="p-6">
          {/* Loading State */}
          {isLoading && (
            <div className="flex items-center justify-center py-8">
              <div className="text-gray-600">Loading menu items...</div>
            </div>
          )}

          {/* Error State */}
          {error && (
            <div className="mb-6 rounded-lg bg-red-50 border border-red-200 p-4">
              <p className="text-red-800">{error}</p>
              <button
                onClick={() => window.location.reload()}
                className="mt-2 text-sm text-red-600 hover:text-red-800 underline"
              >
                Refresh Page
              </button>
            </div>
          )}

          {/* Menu Content */}
          {!isLoading && !error && (
            <>
              {/* Category Filter */}
              <div className="mb-6">
                <div className="flex gap-2 flex-wrap">
                  {categories.map(category => (
                    <button
                      key={category}
                      onClick={() => setSelectedCategory(category)}
                      className={`px-4 py-2 rounded-lg text-sm transition ${
                        selectedCategory === category
                          ? "bg-black text-white"
                          : "border border-gray-300 hover:bg-gray-50"
                      }`}
                    >
                      {category}
                    </button>
                  ))}
                </div>
              </div>

              {/* Menu Items */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-h-96 overflow-y-auto">
                {filteredMenu.length === 0 ? (
                  <div className="col-span-full text-center py-8">
                    <p className="text-gray-600">No menu items available.</p>
                  </div>
                ) : (
                  filteredMenu.map(item => {
                    const quantity = quantities[item.id] || 1;
                    
                    return (
                      <div key={item.id} className="border rounded-lg p-4">
                        <div className="mb-3">
                          <h3 className="font-semibold">{item.name}</h3>
                          {item.description && (
                            <p className="text-sm text-gray-600 mb-2">{item.description}</p>
                          )}
                          <p className="font-bold text-lg">${item.price.toFixed(2)}</p>
                        </div>

                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <button
                              onClick={() => handleQuantityChange(item.id, quantity - 1)}
                              className="h-8 w-8 rounded border text-sm hover:bg-gray-100 transition"
                              disabled={quantity <= 1}
                            >
                              −
                            </button>
                            <span className="w-8 text-center">{quantity}</span>
                            <button
                              onClick={() => handleQuantityChange(item.id, quantity + 1)}
                              className="h-8 w-8 rounded border text-sm hover:bg-gray-100 transition"
                            >
                              +
                            </button>
                          </div>

                          <button
                            onClick={() => handleAddToCart(item)}
                            className="rounded-lg bg-black px-4 py-2 text-sm text-white hover:bg-gray-800 transition"
                          >
                            Add ${(item.price * quantity).toFixed(2)}
                          </button>
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </>
          )}
        </div>

        <div className="border-t p-6">
          <div className="flex justify-end gap-3">
            <button
              onClick={onClose}
              className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
            >
              Done
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}