"use client";
import React, { useState, useEffect } from 'react';
import Cookies from 'js-cookie';

/**
 * ProductCard component to display individual product information.
 * Uses robust Tailwind styling for a clean, responsive card layout.
 */
const ProductCard = ({ product, supplierName, onAddToCart }: any) => (
  <div className="p-4 bg-white shadow-xl rounded-xl transition hover:shadow-2xl hover:scale-[1.02] duration-300 transform border border-gray-100">
    <div className="flex justify-between items-start mb-2">
      <h2 className="text-xl font-semibold text-gray-800">{product.name}</h2>
      <span className={`px-3 py-1 text-xs font-medium rounded-full ${product.is_available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
        {product.is_available ? 'Available' : 'Out of Stock'}
      </span>
    </div>

    {/* ADD SUPPLIER NAME HERE */}
    <p className="text-xs text-gray-500 mb-3 font-medium">
      Supplier: {supplierName}
    </p>

    {/* Display the price prominently */}
    <p className="text-3xl font-bold text-indigo-600 mb-3">${product.unit_price.toFixed(2)}</p>

    {/* ADD TO CART BUTTON */}
    <button
      onClick={() => onAddToCart(product.id)}
      disabled={!product.is_available || product.inventory_quantity === 0}
      className={`mt-4 w-full py-2 px-4 rounded-lg font-bold transition duration-200 shadow-md ${product.is_available && product.inventory_quantity > 0
        ? 'bg-indigo-600 hover:bg-indigo-700 text-white'
        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        }`}
      title={product.is_available && product.inventory_quantity > 0 ? "Add to Cart" : "Currently unavailable"}
    >
      {/* Icon: Shopping Cart */}
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 inline mr-2 -mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
      {product.inventory_quantity === 0 ? 'Sold Out' : 'Add to Cart'}
    </button>

    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm text-gray-600">
      {/* Category */}
      <div className="flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" /></svg>
        <span className="font-medium">Category:</span> {product.category}
      </div>
      {/* Size */}
      <div className="flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c1.657 0 3 .895 3 2s-1.343 2-3 2-3-.895-3-2 1.343-2 3-2z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 14c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 4v4" /></svg>
        <span className="font-medium">Size:</span> {product.size}
      </div>
      {/* Inventory */}
      <div className="flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 7v10c0 1.1.9 2 2 2h12a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" /></svg>
        <span className="font-medium">Inventory:</span> {product.inventory_quantity}
      </div>
      {/* Discount */}
      <div className="flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 11.5V14m0-2.5v2.5M15 11.5V14m0-2.5v2.5M8 10a1 1 0 011-1h6a1 1 0 011 1v4a1 1 0 01-1 1H9a1 1 0 01-1-1v-4zM7 4h10a2 2 0 012 2v1h-14V6a2 2 0 012-2z" /></svg>
        <span className="font-medium">Discount:</span> {product.discount * 100}%
      </div>
    </div>
  </div>
);

/**
 * Main application component responsible for fetching and displaying the menu.
 */
const App = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [supplierMap, setSupplierMap] = useState({}); // <-- ADD THIS LINE

  // Helper function for fetching with exponential backoff
  const exponentialBackoffFetch = async (url: any, options: any, retries = 3) => {
    for (let i = 0; i < retries; i++) {
      try {
        const response = await fetch(url, options);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response;
      } catch (e) {
        if (i < retries - 1) {
          const delay = Math.pow(2, i) * 1000;
          await new Promise(resolve => setTimeout(resolve, delay));
        } else {
          throw e;
        }
      }
    }
  };

  // Function to handle adding a product to the cart
  const addToCart = async (productId: any) => {
    try {
      const response = await exponentialBackoffFetch(`http://localhost:5000/api/customers/${Cookies.get('user_id')}/cart`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_id: productId,
          quantity: 1 // Always adding 1 unit for simplicity
        }),
      });

      if (!response) throw new Error("Add to cart request failed.");

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      // Use console.log for success feedback (since alert() is forbidden)
      console.log(`✅ Success: Product ${productId} added to cart. Cart Item ID: ${data.cart_item_id}`);

    } catch (err: unknown) {
      console.error("Failed to add item to cart:", err instanceof Error ? err.message : "");
      // Log an error if the request fails
      console.error(`❌ Error adding product ${productId}: ${err instanceof Error ? err.message : ""}`);
    }
  };

  // Function to fetch all supplier names and create a map
  const fetchSuppliers = async () => {
    try {
      // Endpoint is now relative: /api/suppliers/all becomes just '/suppliers/all'
      const response = await exponentialBackoffFetch('http://localhost:5000/api/suppliers/all', {
        method: 'GET',
        // No headers/body needed for this standard GET route
      });

      if (!response) throw new Error("Supplier list failed.");

      const data = await response.json();
      if (data.error) throw new Error(data.error);

      // Create a map: { 'supplierId1': 'CompanyName A', ...}
      const map = data.suppliers.reduce((acc: any, s: any) => {
        // Ensure user_id is a string for mapping consistency
        acc[String(s.user_id)] = s.company_name;
        return acc;
      }, {});

      setSupplierMap(map);
      return map;

    } catch (err) {
      console.error("Failed to fetch suppliers:", err);
      return {};
    }
  };

  const fetchProducts = async () => {
    setLoading(true);
    setError("");
    try {
      // 1. FETCH SUPPLIERS FIRST
      const suppliers = await fetchSuppliers(); // Gets the ID -> Name Map

      // 2. FETCH PRODUCTS using the new /products/menu route
      const response = await exponentialBackoffFetch('http://localhost:5000/api/products/menu', {
        method: 'GET',
        // NOTE: No headers or body are needed for this standard GET route!
      });

      if (!response) throw new Error("Network request failed or returned no response.");

      const data = await response.json();
      if (data.error) throw new Error(data.error);

      // 3. ENRICH AND SANITIZE PRODUCT DATA
      const enrichedProducts = data.products.map((p: any) => {
        // Find the supplier name using the product's supplier_id
        const name = suppliers[String(p.supplier_id)] || "Unknown Supplier";

        return {
          ...p,
          supplierName: name, // <-- Attach the fetched name
          unit_price: parseFloat(p.unit_price) || 0.0,
          inventory_quantity: parseInt(p.inventory_quantity) || 0,
          size: p.size || "Standard",
          keywords: Array.isArray(p.keywords) ? p.keywords : [],
          discount: parseFloat(p.discount) || 0.0,
          is_available: !!p.is_available
        };
      });

      // NEW FILTER: Only keep products whose supplierName is NOT "Unknown Supplier"
      const filteredProducts = enrichedProducts.filter(
        (p: any) => p.supplierName !== "Unknown Supplier"
      );

      setProducts(filteredProducts); // <-- Use the filtered list

    } catch (err) {
      console.error("Failed to fetch products:", err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch data on component mount
  useEffect(() => {
    fetchProducts();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-4 sm:p-8 font-sans">
      <section className="max-w-7xl mx-auto">
        <header className="text-center mb-10 pt-4">
          <h1 className="text-4xl sm:text-5xl font-extrabold text-indigo-800 mb-3 tracking-tight">
            Our Menu
          </h1>
          <p className="text-lg text-gray-600 max-w-xl mx-auto">
            Explore our curated selection of products. Inventory status is updated in real-time.
          </p>
        </header>

        {/* Loading State UI */}
        {loading && (
          <div className="flex flex-col justify-center items-center h-64 text-indigo-600">
            <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-indigo-500"></div>
            <p className="mt-4 text-xl font-medium">Fetching the latest menu...</p>
          </div>
        )}

        {/* Error State UI */}
        {error && !loading && (
          <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-lg shadow max-w-lg mx-auto mb-6" role="alert">
            <strong className="font-bold">Connection Issue:</strong>
            <span className="block sm:inline ml-2">{error}</span>
          </div>
        )}

        {/* Empty Menu State UI */}
        {!loading && products.length === 0 && !error && (
          <div className="text-center py-12 bg-white rounded-xl shadow-lg border border-gray-100">
            <p className="text-xl text-gray-500 font-medium">The menu is currently empty.</p>
            <p className="text-md text-gray-400 mt-1">Please check back soon for new additions!</p>
          </div>
        )}

        {/* Products Grid Display */}
        {!loading && products.length > 0 && (
          <div className="grid grid-cols-1 gap-6">
            {products.map((product: any) => (
              <ProductCard
                key={product.id}
                product={product}
                supplierName={product.supplierName} // <-- USE THE NAME FROM THE PRODUCT OBJECT
                onAddToCart={addToCart}
              />
            ))}
          </div>
        )}

        <footer className="mt-16 text-center text-sm text-gray-400">
          Product data is retrieved from the supplier's backend system.
        </footer>
      </section>
    </div>
  );
};

export default App;