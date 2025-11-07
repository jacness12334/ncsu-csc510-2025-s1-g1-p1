# Frontend How-To Guides

This directory contains practical, step-by-step tutorials for common frontend development tasks in our Next.js + TypeScript + Zustand application.

## Available Guides

- **[add-to-cart.md](./add-to-cart.md)** - Add items to cart and show real-time quantity updates in the UI
- **[checkout-default-payment.md](./checkout-default-payment.md)** - Implement streamlined checkout flow using customer's default payment method  
- **[track-order-realtime.md](./track-order-realtime.md)** - Display live order status updates via WebSocket with visual timeline

## Guide Format

Each guide follows a consistent format:
- **When to use this** - Context for when to apply the pattern
- **Prerequisites** - Required dependencies and setup
- **Step-by-step** - Numbered instructions with TypeScript code blocks
- **Common pitfalls** - Things to watch out for
- **Quick test checklist** - Verification steps

## Code Standards

All guides use:
- Existing types: `MenuItem`, `CartItem`, `PaymentMethod`, `DeliveryOrder`
- Secure practices (never store full card numbers, only last4)
- Serializable state patterns (`Record<string,string>` over `Map`)
- Environment variables (`NEXT_PUBLIC_API_BASE_URL`)
- Error handling and loading states