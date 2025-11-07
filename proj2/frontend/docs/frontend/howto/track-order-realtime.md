# Track Order's Live Status via WebSocket and Display Timeline

## When to use this

Use this guide when implementing real-time order tracking that shows customers live updates as their order progresses through different stages. This provides transparency and reduces customer anxiety about order status.

## Prerequisites

- WebSocket support in your environment
- Order tracking API endpoints configured
- `DeliveryOrder` type from `@/lib/types`
- Order ID available from URL params or props
- Real-time backend that emits order status changes

## Step-by-step

1. **Set up the order tracking component with WebSocket state**

```typescript
"use client";
import { useState, useEffect, useRef } from "react";
import { useParams } from "next/navigation";
import type { DeliveryOrder } from "@/lib/types";

type OrderStatus = 'pending' | 'accepted' | 'in_progress' | 'ready_for_pickup' | 'in_transit' | 'delivered' | 'fulfilled' | 'cancelled';

interface OrderStatusUpdate {
  orderId: string;
  status: OrderStatus;
  timestamp: string;
  message?: string;
}

export default function OrderTracker() {
  const params = useParams();
  const orderId = params.orderId as string;
  
  const [order, setOrder] = useState<DeliveryOrder | null>(null);
  const [statusHistory, setStatusHistory] = useState<Record<string, OrderStatusUpdate>>({});
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('connecting');
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
```

2. **Create the WebSocket connection and event handlers**

```typescript
  useEffect(() => {
    const connectWebSocket = () => {
      const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:5000';
      const ws = new WebSocket(`${wsUrl}/orders/${orderId}/track`);
      
      ws.onopen = () => {
        console.log('WebSocket connected for order:', orderId);
        setConnectionStatus('connected');
        setError(null);
      };
      
      ws.onmessage = (event) => {
        try {
          const update: OrderStatusUpdate = JSON.parse(event.data);
          
          setStatusHistory(prev => ({
            ...prev,
            [update.status]: update
          }));
          
          // Update order status if we have the order loaded
          if (order) {
            setOrder(prev => prev ? { ...prev, delivery_status: update.status } : null);
          }
        } catch (err) {
          console.error('Failed to parse WebSocket message:', err);
        }
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setError('Connection error occurred');
      };
      
      ws.onclose = () => {
        setConnectionStatus('disconnected');
        // Attempt to reconnect after 3 seconds
        setTimeout(connectWebSocket, 3000);
      };
      
      wsRef.current = ws;
    };

    connectWebSocket();
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [orderId, order]);
```

3. **Load initial order data**

```typescript
  useEffect(() => {
    const loadOrder = async () => {
      try {
        const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5000';
        const response = await fetch(`${API_BASE_URL}/api/orders/${orderId}`);
        
        if (!response.ok) {
          throw new Error('Order not found');
        }
        
        const orderData: DeliveryOrder = await response.json();
        setOrder(orderData);
        
        // Initialize status history with current status
        setStatusHistory({
          [orderData.delivery_status]: {
            orderId,
            status: orderData.delivery_status,
            timestamp: orderData.last_updated || orderData.date_added || new Date().toISOString(),
          }
        });
        
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load order');
      }
    };

    if (orderId) {
      loadOrder();
    }
  }, [orderId]);
```

4. **Define the status timeline configuration**

```typescript
  const statusSteps: Array<{ status: OrderStatus; label: string; description: string }> = [
    { status: 'pending', label: 'Order Placed', description: 'Your order has been received' },
    { status: 'accepted', label: 'Order Confirmed', description: 'Restaurant is preparing your order' },
    { status: 'in_progress', label: 'In Kitchen', description: 'Your food is being prepared' },
    { status: 'ready_for_pickup', label: 'Ready for Pickup', description: 'Order is ready for delivery' },
    { status: 'in_transit', label: 'Out for Delivery', description: 'Driver is on the way' },
    { status: 'delivered', label: 'Delivered', description: 'Order has been delivered' },
  ];

  const getStepStatus = (stepStatus: OrderStatus) => {
    if (!order) return 'upcoming';
    
    const currentIndex = statusSteps.findIndex(step => step.status === order.delivery_status);
    const stepIndex = statusSteps.findIndex(step => step.status === stepStatus);
    
    if (stepIndex < currentIndex) return 'completed';
    if (stepIndex === currentIndex) return 'current';
    return 'upcoming';
  };
```

5. **Create the timeline component**

```typescript
  const renderTimeline = () => (
    <div className="space-y-4">
      {statusSteps.map((step, index) => {
        const stepState = getStepStatus(step.status);
        const statusUpdate = statusHistory[step.status];
        
        return (
          <div key={step.status} className="flex items-start space-x-4">
            {/* Timeline indicator */}
            <div className="flex flex-col items-center">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                stepState === 'completed' ? 'bg-green-500 text-white' :
                stepState === 'current' ? 'bg-blue-500 text-white' :
                'bg-gray-200 text-gray-500'
              }`}>
                {stepState === 'completed' ? (
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                ) : (
                  <span>{index + 1}</span>
                )}
              </div>
              {index < statusSteps.length - 1 && (
                <div className={`w-0.5 h-12 ${
                  stepState === 'completed' ? 'bg-green-500' : 'bg-gray-200'
                }`} />
              )}
            </div>
            
            {/* Content */}
            <div className="flex-1 pb-8">
              <h3 className={`font-semibold ${
                stepState === 'current' ? 'text-blue-600' :
                stepState === 'completed' ? 'text-green-600' :
                'text-gray-500'
              }`}>
                {step.label}
              </h3>
              <p className="text-gray-600 text-sm">{step.description}</p>
              {statusUpdate && (
                <p className="text-xs text-gray-500 mt-1">
                  {new Date(statusUpdate.timestamp).toLocaleString()}
                </p>
              )}
              {statusUpdate?.message && (
                <p className="text-sm text-blue-600 mt-1">{statusUpdate.message}</p>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
```

6. **Add connection status indicator**

```typescript
  const renderConnectionStatus = () => (
    <div className={`flex items-center space-x-2 px-3 py-2 rounded text-sm ${
      connectionStatus === 'connected' ? 'bg-green-50 text-green-700' :
      connectionStatus === 'connecting' ? 'bg-yellow-50 text-yellow-700' :
      'bg-red-50 text-red-700'
    }`}>
      <div className={`w-2 h-2 rounded-full ${
        connectionStatus === 'connected' ? 'bg-green-500' :
        connectionStatus === 'connecting' ? 'bg-yellow-500' :
        'bg-red-500'
      }`} />
      <span>
        {connectionStatus === 'connected' ? 'Live updates active' :
         connectionStatus === 'connecting' ? 'Connecting...' :
         'Connection lost - attempting to reconnect'}
      </span>
    </div>
  );
```

7. **Create the estimated delivery time display**

```typescript
  const renderDeliveryEstimate = () => {
    if (!order || order.delivery_status === 'delivered') return null;
    
    // Calculate estimated delivery based on current status
    const getEstimatedMinutes = () => {
      switch (order.delivery_status) {
        case 'pending': return 45;
        case 'accepted': return 35;
        case 'in_progress': return 25;
        case 'ready_for_pickup': return 15;
        case 'in_transit': return 10;
        default: return 0;
      }
    };
    
    const estimatedMinutes = getEstimatedMinutes();
    const estimatedTime = new Date(Date.now() + estimatedMinutes * 60000);
    
    return (
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-semibold text-blue-900">Estimated Delivery</h3>
        <p className="text-blue-700">
          {estimatedTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </p>
        <p className="text-blue-600 text-sm">
          Approximately {estimatedMinutes} minutes
        </p>
      </div>
    );
  };
```

8. **Implement the complete tracker component**

```typescript
  if (error) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="bg-red-50 border border-red-300 rounded-lg p-4">
          <h2 className="text-lg font-semibold text-red-800">Error</h2>
          <p className="text-red-700">{error}</p>
        </div>
      </div>
    );
  }

  if (!order) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-gray-200 rounded w-1/3" />
          <div className="h-4 bg-gray-200 rounded w-1/2" />
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-2xl font-bold">Order #{order.id.slice(-8)}</h1>
          <p className="text-gray-600">Total: ${order.total_price.toFixed(2)}</p>
        </div>
        {renderConnectionStatus()}
      </div>
      
      {renderDeliveryEstimate()}
      {renderTimeline()}
      
      {order.delivery_status === 'delivered' && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
          <h3 className="font-semibold text-green-900">Order Delivered!</h3>
          <p className="text-green-700">Thank you for your order. We hope you enjoyed your meal!</p>
        </div>
      )}
    </div>
  );
}
```

## Common pitfalls

- **WebSocket connection management**: Always clean up WebSocket connections and handle reconnection logic
- **State synchronization**: Ensure WebSocket updates don't conflict with initial data loading
- **Error handling**: Handle both network errors and malformed WebSocket messages gracefully
- **Memory leaks**: Use useRef for WebSocket instances and properly clean up event listeners
- **Stale closure issues**: Be careful with state dependencies in WebSocket event handlers

## Quick test checklist

- [ ] Verify initial order data loads correctly with proper status
- [ ] Confirm WebSocket connection establishes and shows "live updates active"
- [ ] Test timeline updates in real-time when status changes
- [ ] Check reconnection works when WebSocket connection is lost
- [ ] Validate estimated delivery time updates based on current status