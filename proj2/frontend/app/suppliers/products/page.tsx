"use client";
import { useState } from "react";
import Link from "next/link";

interface Product {
  id: number;
  name: string;
  unit_price: number;
  inventory_quantity: number;
  size: 'small' | 'medium' | 'large' | null;
  keywords: string;
  category: 'beverages' | 'snacks' | 'candy' | 'food';
  is_available: boolean;
}

export default function ManageProductsPage() {
  // Backend integration ready - replace with API calls
  const [products, setProducts] = useState<Product[]>([]);

  const [showAddForm, setShowAddForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterCategory, setFilterCategory] = useState<string>("");

  // New/Edit Product Form State
  const [formData, setFormData] = useState({
    name: "",
    unit_price: 0,
    inventory_quantity: 0,
    size: null as 'small' | 'medium' | 'large' | null,
    keywords: "",
    category: "beverages" as 'beverages' | 'snacks' | 'candy' | 'food',
    is_available: true
  });

  const resetForm = () => {
    setFormData({
      name: "",
      unit_price: 0,
      inventory_quantity: 0,
      size: null,
      keywords: "",
      category: "beverages",
      is_available: true
    });
    setEditingProduct(null);
    setShowAddForm(false);
  };

  const handleAddProduct = () => {
    if (!formData.name || formData.unit_price < 0 || formData.inventory_quantity < 0) {
      alert("Please fill in all required fields with valid values.");
      return;
    }

    const newProduct: Product = {
      id: Date.now(), // In real app, backend would generate this
      ...formData
    };

    // TODO: Backend integration - POST /api/products
    console.log("Adding product:", newProduct);
    setProducts([...products, newProduct]);
    resetForm();
  };

  const handleEditProduct = () => {
    if (!editingProduct || !formData.name || formData.unit_price < 0 || formData.inventory_quantity < 0) {
      alert("Please fill in all required fields with valid values.");
      return;
    }

    // TODO: Backend integration - PUT /api/products/{productId}
    console.log("Editing product:", editingProduct.id, formData);
    setProducts(products.map(p => 
      p.id === editingProduct.id ? { ...editingProduct, ...formData } : p
    ));
    resetForm();
  };

  const handleDeleteProduct = (productId: number) => {
    if (confirm("Are you sure you want to delete this product?")) {
      // TODO: Backend integration - DELETE /api/products/{productId}
      console.log("Deleting product:", productId);
      setProducts(products.filter(p => p.id !== productId));
    }
  };

  const startEdit = (product: Product) => {
    setEditingProduct(product);
    setFormData({
      name: product.name,
      unit_price: product.unit_price,
      inventory_quantity: product.inventory_quantity,
      size: product.size,
      keywords: product.keywords,
      category: product.category,
      is_available: product.is_available
    });
    setShowAddForm(true);
  };

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.keywords.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = filterCategory === "" || product.category === filterCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <section className="mx-auto max-w-6xl px-4 py-8">
      <div className="mb-6">
        <Link
          href="/suppliers"
          className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900"
        >
          ← Return to Dashboard
        </Link>
      </div>
      
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="mb-2 text-3xl font-bold">Manage Products</h1>
          <p className="text-gray-600">Add, edit, and manage your product inventory</p>
        </div>
        <button
          onClick={() => setShowAddForm(true)}
          className="rounded-lg bg-black px-4 py-2 text-white hover:bg-gray-800 transition"
        >
          Add New Product
        </button>
      </div>

      {/* Search and Filter */}
      <div className="mb-6 flex gap-4">
        <div className="flex-1">
          <input
            type="text"
            placeholder="Search products..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
          />
        </div>
        <select
          value={filterCategory}
          onChange={(e) => setFilterCategory(e.target.value)}
          aria-label="Filter by category"
          className="rounded-lg border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
        >
          <option value="">All Categories</option>
          <option value="beverages">Beverages</option>
          <option value="snacks">Snacks</option>
          <option value="candy">Candy</option>
          <option value="food">Food</option>
        </select>
      </div>

      {/* Add/Edit Product Form */}
      {showAddForm && (
        <div className="mb-8 rounded-lg border-2 border-blue-200 bg-blue-50 p-6">
          <h2 className="mb-4 text-xl font-semibold">
            {editingProduct ? 'Edit Product' : 'Add New Product'}
          </h2>
          
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <div>
              <label className="mb-1 block text-sm font-medium">Product Name *</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                placeholder="Pepsi"
                className="w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium">Category *</label>
              <select
                value={formData.category}
                onChange={(e) => setFormData({...formData, category: e.target.value as 'beverages' | 'snacks' | 'candy' | 'food'})}
                aria-label="Product category"
                className="w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              >
                <option value="beverages">Beverages</option>
                <option value="snacks">Snacks</option>
                <option value="candy">Candy</option>
                <option value="food">Food</option>
              </select>
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium">Unit Price *</label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={formData.unit_price}
                onChange={(e) => setFormData({...formData, unit_price: parseFloat(e.target.value) || 0})}
                placeholder="3.00"
                className="w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium">Inventory Quantity *</label>
              <input
                type="number"
                min="0"
                value={formData.inventory_quantity}
                onChange={(e) => setFormData({...formData, inventory_quantity: parseInt(e.target.value) || 0})}
                placeholder="10"
                className="w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>

            <div>
              <label className="mb-1 block text-sm font-medium">Size</label>
              <select
                value={formData.size || ""}
                onChange={(e) => setFormData({...formData, size: e.target.value === "" ? null : e.target.value as 'small' | 'medium' | 'large'})}
                aria-label="Product size"
                className="w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              >
                <option value="">No Size</option>
                <option value="small">Small</option>
                <option value="medium">Medium</option>
                <option value="large">Large</option>
              </select>
            </div>

            <div className="flex items-center">
              <input
                id="is_available"
                type="checkbox"
                checked={formData.is_available}
                onChange={(e) => setFormData({...formData, is_available: e.target.checked})}
                className="mr-2 h-4 w-4 rounded border-gray-300 text-black focus:ring-black"
              />
              <label htmlFor="is_available" className="text-sm font-medium">
                Available for sale
              </label>
            </div>
          </div>

          <div className="mt-4">
            <label className="mb-1 block text-sm font-medium">Keywords (comma-separated)</label>
            <input
              type="text"
              value={formData.keywords}
              onChange={(e) => setFormData({...formData, keywords: e.target.value})}
              placeholder="sweet, refreshing, cold, quick, energy"
              className="w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
            />
          </div>

          <div className="mt-6 flex gap-3">
            <button
              onClick={editingProduct ? handleEditProduct : handleAddProduct}
              className="rounded-lg bg-black px-4 py-2 text-sm text-white hover:bg-gray-800 transition"
            >
              {editingProduct ? 'Save Changes' : 'Add Product'}
            </button>
            <button
              onClick={resetForm}
              className="rounded-lg border px-4 py-2 text-sm hover:bg-gray-100 transition"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Products Table */}
      <div className="rounded-lg border">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">Product</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">Category</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">Price</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">Stock</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white">
              {filteredProducts.map((product) => (
                <tr key={product.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div>
                      <div className="font-medium text-gray-900">{product.name}</div>
                      {product.size && (
                        <div className="text-xs text-gray-500 capitalize">Size: {product.size}</div>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="rounded-full bg-gray-100 px-2 py-1 text-xs font-medium text-gray-800 capitalize">
                      {product.category}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-gray-900">
                    ${product.unit_price.toFixed(2)}
                  </td>
                  <td className="px-6 py-4">
                    <span className={`font-medium ${
                      product.inventory_quantity === 0 
                        ? 'text-red-600' 
                        : product.inventory_quantity <= 5 
                        ? 'text-yellow-600' 
                        : 'text-green-600'
                    }`}>
                      {product.inventory_quantity}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex rounded-full px-2 py-1 text-xs font-semibold ${
                      product.is_available 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {product.is_available ? 'Available' : 'Unavailable'}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex gap-2">
                      <button
                        onClick={() => startEdit(product)}
                        className="text-sm text-blue-600 hover:text-blue-500"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDeleteProduct(product.id)}
                        className="text-sm text-red-600 hover:text-red-500"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {filteredProducts.length === 0 && (
          <div className="p-8 text-center text-gray-500">
            No products found matching your criteria.
          </div>
        )}
      </div>
    </section>
  );
}