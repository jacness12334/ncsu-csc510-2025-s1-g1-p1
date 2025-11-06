"use client";
import { useState, useEffect } from "react";
import Link from "next/link";

// Product interface matching backend API response
interface Product {
  id: number;
  name: string;
  unit_price: number;
  inventory_quantity: number;
  size: 'small' | 'medium' | 'large' | null;
  keywords: string;
  category: 'beverages' | 'snacks' | 'candy' | 'food';
  discount: number;
  is_available: boolean;
}

export default function SuppliersPage() {
  // State for store status and UI
  const [isOpen, setIsOpen] = useState(false);
  const [userId, setUserId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  
  // Dashboard metrics calculated from products
  const [metrics, setMetrics] = useState({
    totalProducts: 0,
    availableProducts: 0,
    outOfStock: 0,
    lowStock: 0
  });
  
  // Recent products for dashboard table
  const [recentProducts, setRecentProducts] = useState<Product[]>([]);

  /**
   * Retrieves user ID from sessionToken cookie set during login
   * @returns user ID as number or null if not found
   */
  const getUserIdFromCookie = () => {
    const cookies = document.cookie.split(';');
    const sessionCookie = cookies.find(cookie => cookie.trim().startsWith('sessionToken='));
    if (sessionCookie) {
      const tokenValue = sessionCookie.split('=')[1];
      return parseInt(tokenValue) || null;
    }
    return null;
  };

  /**
   * Initialize user authentication and load dashboard data on component mount
   */
  useEffect(() => {
    const id = getUserIdFromCookie();
    if (id) {
      setUserId(id);
      loadDashboardData(id);
    } else {
      alert("Please log in to access supplier features");
    }
  }, []);

  /**
   * Loads dashboard data including products and calculates metrics
   * Calls GET /api/products endpoint from backend
   * @param userIdParam - The authenticated user's ID
   */
  const loadDashboardData = async (userIdParam: number) => {
    setIsLoading(true);
    try {
      // Call backend GET /api/products endpoint (available in backend branch)
      const response = await fetch(`http://localhost:5000/api/products?user_id=${userIdParam}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        }
      });

      if (response.ok) {
        const responseData = await response.json();
        // Backend returns {products: [...]} format
        const products = responseData.products || [];
        setRecentProducts(products.slice(0, 5)); // Show first 5 as recent products
        
        // Calculate dashboard metrics from products array
        const totalProducts = products.length;
        const availableProducts = products.filter((p: Product) => p.is_available).length;
        const outOfStock = products.filter((p: Product) => p.inventory_quantity === 0).length;
        const lowStock = products.filter((p: Product) => p.inventory_quantity > 0 && p.inventory_quantity <= 5).length;
        
        setMetrics({
          totalProducts,
          availableProducts,
          outOfStock,
          lowStock
        });
      } else {
        console.error("Failed to load dashboard data");
      }
    } catch (error) {
      console.error("Error loading dashboard data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Handles store open/closed status toggle
   * Calls PUT /api/suppliers/status endpoint
   */
  const handleToggleStore = async () => {
    if (!userId) {
      alert("User not authenticated");
      return;
    }

    setIsLoading(true);
    try {
      // Call backend PUT /api/suppliers/status endpoint
      const response = await fetch("http://localhost:5000/api/suppliers/status", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: userId,
          is_open: !isOpen
        })
      });

      if (response.ok) {
        setIsOpen(!isOpen);
        alert(`Store ${!isOpen ? 'opened' : 'closed'} successfully!`);
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.error || 'Failed to update store status'}`);
      }
    } catch (error) {
      console.error("Error updating store status:", error);
      alert("Error updating store status. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="mx-auto max-w-6xl px-4 py-8">
      <div className="mb-8">
        <h1 className="mb-2 text-3xl font-bold">Supplier Dashboard</h1>
        <p className="text-gray-600">Manage your store and products</p>
      </div>

      {/* Store Status Section */}
      <div className="mb-8 rounded-lg border p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold">Store Status</h2>
            <p className="text-gray-600">Your store is currently {isOpen ? 'open' : 'closed'}</p>
          </div>
          <div className="flex items-center gap-3">
            <span className={`h-3 w-3 rounded-full ${isOpen ? 'bg-green-500' : 'bg-red-500'}`}></span>
            <button
              onClick={handleToggleStore}
              disabled={isLoading}
              className={`rounded-lg px-4 py-2 text-sm font-medium transition disabled:opacity-50 ${
                isOpen 
                  ? 'bg-red-100 text-red-700 hover:bg-red-200' 
                  : 'bg-green-100 text-green-700 hover:bg-green-200'
              }`}
            >
              {isLoading ? 'Updating...' : isOpen ? 'Close Store' : 'Open Store'}
            </button>
          </div>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="mb-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-lg border p-6">
          <h3 className="text-sm font-medium text-gray-600">Total Products</h3>
          <p className="text-2xl font-bold">{metrics.totalProducts}</p>
        </div>
        <div className="rounded-lg border p-6">
          <h3 className="text-sm font-medium text-gray-600">Available</h3>
          <p className="text-2xl font-bold text-green-600">{metrics.availableProducts}</p>
        </div>
        <div className="rounded-lg border p-6">
          <h3 className="text-sm font-medium text-gray-600">Out of Stock</h3>
          <p className="text-2xl font-bold text-red-600">{metrics.outOfStock}</p>
        </div>
        <div className="rounded-lg border p-6">
          <h3 className="text-sm font-medium text-gray-600">Low Stock</h3>
          <p className="text-2xl font-bold text-yellow-600">{metrics.lowStock}</p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mb-8 grid gap-4 sm:grid-cols-2">
        <Link
          href="/suppliers/products"
          className="rounded-lg border p-6 text-center transition hover:bg-gray-50"
        >
          <h3 className="mb-2 font-semibold">Manage Products</h3>
          <p className="text-sm text-gray-600">View, add, edit, and delete products</p>
        </Link>
        <Link
          href="/suppliers/profile"
          className="rounded-lg border p-6 text-center transition hover:bg-gray-50"
        >
          <h3 className="mb-2 font-semibold">Edit Profile</h3>
          <p className="text-sm text-gray-600">Update company and personal information</p>
        </Link>
      </div>

      {/* Products */}
      <div className="rounded-lg border">
        <div className="border-b p-6">
          <h2 className="text-xl font-semibold">Products</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">Product</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">Category</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">Price</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">Stock</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white">
              {recentProducts.length > 0 ? (
                recentProducts.map((product) => (
                  <tr key={product.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="font-medium text-gray-900">{product.name}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="rounded-full bg-gray-100 px-2 py-1 text-xs font-medium text-gray-800 capitalize">
                        {product.category}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-900">
                      ${product.unit_price.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`font-medium ${product.inventory_quantity === 0 ? 'text-red-600' : product.inventory_quantity <= 5 ? 'text-yellow-600' : 'text-green-600'}`}>
                        {product.inventory_quantity}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex rounded-full px-2 py-1 text-xs font-semibold ${
                        product.is_available 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {product.is_available ? 'Available' : 'Unavailable'}
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-gray-500">
                    No products found. Add your first product to get started.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        <div className="border-t p-4">
          <Link
            href="/suppliers/products"
            className="text-sm text-blue-600 hover:text-blue-500"
          >
            View all products →
          </Link>
        </div>
      </div>
    </section>
  );
}
