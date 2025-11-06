"use client";
import { useState } from "react";
import Link from "next/link";

export default function SuppliersPage() {
  const [isOpen, setIsOpen] = useState(false);

  // Backend integration ready - replace with API calls
  const metrics = {
    totalProducts: 0,
    availableProducts: 0,
    outOfStock: 0,
    lowStock: 0
  };

  const recentProducts: Array<{
    id: number;
    name: string;
    category: string;
    price: number;
    inventory: number;
    isAvailable: boolean;
  }> = [];

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
              onClick={() => setIsOpen(!isOpen)}
              className={`rounded-lg px-4 py-2 text-sm font-medium transition ${
                isOpen 
                  ? 'bg-red-100 text-red-700 hover:bg-red-200' 
                  : 'bg-green-100 text-green-700 hover:bg-green-200'
              }`}
            >
              {isOpen ? 'Close Store' : 'Open Store'}
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
                      ${product.price.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`font-medium ${product.inventory === 0 ? 'text-red-600' : product.inventory <= 5 ? 'text-yellow-600' : 'text-green-600'}`}>
                        {product.inventory}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex rounded-full px-2 py-1 text-xs font-semibold ${
                        product.isAvailable 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {product.isAvailable ? 'Available' : 'Unavailable'}
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
