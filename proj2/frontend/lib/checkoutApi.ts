// lib/checkoutApi.ts
import type { PaymentMethod, DeliveryOrder, CustomerShowing } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

// Default customer ID (in production, this should come from authentication)
const DEFAULT_CUSTOMER_ID = "1";

// Backend payment method interface
interface BackendPaymentMethod {
  id: string;
  customer_id: string;
  card_number: string;
  expiration_month: number;
  expiration_year: number;
  billing_address: string;
  balance?: number;
  is_default?: boolean;
  date_added?: string;
  last_updated?: string;
}

export class CheckoutApiService {
  // Payment Methods
  static async getPaymentMethods(customerId: string = DEFAULT_CUSTOMER_ID): Promise<PaymentMethod[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/customers/${customerId}/payment-methods`, {
        credentials: "include"
      });
      if (!response.ok) {
        throw new Error(`Failed to fetch payment methods: ${response.statusText}`);
      }
      const data = await response.json();
      
      // Handle the response structure from backend
      if (data.payment_methods && Array.isArray(data.payment_methods)) {
        // Transform backend response to frontend format
        return data.payment_methods.map((method: BackendPaymentMethod) => ({
          id: method.id,
          customer_id: method.customer_id || customerId,
          card_number: method.card_number,
          expiration_month: method.expiration_month,
          expiration_year: method.expiration_year,
          billing_address: method.billing_address,
          balance: method.balance || 0,
          is_default: method.is_default || false,
          date_added: method.date_added,
          last_updated: method.last_updated
        }));
      }
      
      return data; // Direct array response
    } catch (error) {
      console.error("Error fetching payment methods:", error);
      throw error; // Let the UI handle the error properly
    }
  }

  static async addPaymentMethod(
    customerId: string = DEFAULT_CUSTOMER_ID,
    paymentData: {
      card_number: string;
      expiration_month: number;
      expiration_year: number;
      billing_address: string;
      balance: number;
      is_default: boolean;
    }
  ): Promise<PaymentMethod> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/customers/${customerId}/payment-methods`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(paymentData),
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || errorData.message || `Failed to add payment method: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      // Transform backend response to frontend format if needed
      return {
        id: data.id,
        customer_id: data.customer_id || customerId,
        card_number: data.card_number,
        expiration_month: data.expiration_month,
        expiration_year: data.expiration_year,
        billing_address: data.billing_address,
        balance: data.balance || 0,
        is_default: data.is_default || false,
        date_added: data.date_added || new Date().toISOString(),
        last_updated: data.last_updated || new Date().toISOString(),
      };
    } catch (error) {
      console.error("Error adding payment method:", error);
      throw error; // Let the UI handle the error properly
    }
  }

  // Customer Showings
  static async getCustomerShowings(customerId: string): Promise<CustomerShowing[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/customers/${customerId}/showings`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
      
      if (!response.ok) {
        throw new Error("Failed to fetch customer showings");
      }
      
      return await response.json();
    } catch (error) {
      console.error("Error fetching customer showings:", error);
      throw error;
    }
  }

  // Create Delivery/Order
  static async createDelivery(orderData: {
    customer_showing_id: string;
    payment_method_id: string;
  }): Promise<DeliveryOrder> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/deliveries`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(orderData),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to create order");
      }
      
      return await response.json();
    } catch (error) {
      console.error("Error creating order:", error);
      throw error;
    }
  }

  // Get Delivery Status
  static async getDeliveryStatus(deliveryId: string): Promise<DeliveryOrder> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/deliveries/${deliveryId}`, {
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error("Failed to fetch delivery status");
      }
      return await response.json();
    } catch (error) {
      console.error("Error fetching delivery status:", error);
      throw error;
    }
  }

  // Cancel Delivery
  static async cancelDelivery(deliveryId: string): Promise<DeliveryOrder> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/deliveries/${deliveryId}/cancel`, {
        method: "POST",
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error("Failed to cancel delivery");
      }
      return await response.json();
    } catch (error) {
      console.error("Error cancelling delivery:", error);
      throw error;
    }
  }
}