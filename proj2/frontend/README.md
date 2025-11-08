# Movie Munchers Frontend Documentation

This documentation was generated automatically using TypeDoc from JSDoc comments in the source code.

## Viewing the Documentation

### Option 1: Open HTML files directly
Navigate to the `docs` folder and open `index.html` in your web browser.

### Option 2: Serve locally (recommended)
Run the following command to serve the documentation on a local server:

```bash
npm run docs:serve
```

This will:
1. Generate the latest documentation from JSDoc comments
2. Start a local server to serve the documentation
3. Open your browser to view the documentation

## Regenerating Documentation

To regenerate the documentation after making changes to JSDoc comments in the source code:

```bash
npm run docs
```

## Documentation Structure

The documentation includes:

### Types (`lib/types.ts`)
- `Purchasable` - Base interface for purchasable items
- `MenuItem` - Menu item structure
- `CartItem` - Shopping cart item structure  
- `PaymentMethod` - Customer payment method structure
- `CustomerShowing` - Movie showing reservation structure
- `DeliveryOrder` - Delivery order structure
- `DeliveryItem` - Individual delivery item structure

### Store Management (`lib/cartStore.ts`)
- `useCartStore` - Zustand store for cart state management

### API Services 
- `CartApiService` (`lib/cartApi.ts`) - Cart operations API
- `BackendCartItem` - Backend cart item interface

### Components
- `MenuCard` (`app/components/MenuCard.tsx`) - Menu item display component
- `Navbar` (`app/components/Navbar.tsx`) - Navigation component
- `RootLayout` (`app/layout.tsx`) - Root layout wrapper

### Sample Data (`lib/sampleData.ts`)
- `MENU` - Sample menu items for development

## Adding JSDoc Comments

When adding new exports, use the following JSDoc format:

```typescript
/**
 * Brief description of the function/component
 * 
 * @param paramName - Description of parameter
 * @returns Description of return value
 * 
 * @example
 * ```typescript
 * // Usage example
 * const result = myFunction("example");
 * ```
 */
export function myFunction(paramName: string): string {
  // Implementation
}
```

The documentation will automatically update when you run `npm run docs`.