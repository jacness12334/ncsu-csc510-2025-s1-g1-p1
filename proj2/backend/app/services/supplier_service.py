from app.models import *
from app.app import db


class SupplierService:
    """Business logic for supplier profiles and product/catalog management.

    This service validates supplier identity and provides operations to view and
    update supplier details, manage products, and list open suppliers.
    """

    def __init__(self, user_id):
        """Initialize the supplier service with acting user context.

        Args:
            user_id: The supplier's user id used for authorization and filtering.
        """
        self.user_id = user_id

    def validate_supplier(self):
        """Validate that the current user id belongs to a supplier.

        Returns:
            Suppliers: The supplier record.

        Raises:
            ValueError: If the supplier record does not exist.
        """
        supplier = Suppliers.query.filter_by(user_id=self.user_id).first()
        if not supplier:
            raise ValueError(f"Supplier {self.user_id} not found")
        return supplier

    def get_supplier(self):
        """Return the supplier record for the current context user.

        Returns:
            Suppliers: The supplier record associated with self.user_id.

        Raises:
            ValueError: If the supplier record does not exist.
        """
        supplier = self.validate_supplier()
        return supplier

    def edit_supplier(self, company_name, company_address, contact_phone, is_open):
        """Update supplier profile fields.

        Args:
            company_name: New company name.
            company_address: New company address.
            contact_phone: New contact phone number.
            is_open: Whether the supplier is currently open.

        Returns:
            Suppliers: The updated supplier record.

        Raises:
            ValueError: If the supplier record does not exist.
        """
        supplier = self.validate_supplier()
        supplier.company_name = company_name
        supplier.company_address = company_address
        supplier.contact_phone = contact_phone
        supplier.is_open = is_open
        db.session.commit()
        return supplier

    def set_is_open(self, is_open):
        """Set the supplier's open/closed status.

        Args:
            is_open: Boolean open flag to set.

        Returns:
            Suppliers: The updated supplier record.

        Raises:
            ValueError: If the supplier record does not exist.
        """
        supplier = self.validate_supplier()
        supplier.is_open = is_open
        db.session.commit()
        return supplier

    def get_products(self):
        """List all products owned by the current supplier.

        Returns:
            list[Products]: All product rows for this supplier (possibly empty).

        Raises:
            ValueError: If the supplier record does not exist.
        """
        supplier = self.validate_supplier()
        products = Products.query.filter_by(supplier_id=self.user_id).all()
        return products

    def add_product(self, name, unit_price, inventory_quantity, size, keywords, category, discount, is_available):
        """Create a new product for the current supplier.

        Args:
            name: Product name.
            unit_price: Unit price as numeric/Decimal-compatible value.
            inventory_quantity: Initial inventory quantity (non-negative).
            size: Optional size (e.g., 'small', 'medium', 'large' or None).
            keywords: Optional search keywords.
            category: Product category (must satisfy DB enum).
            discount: Per-unit discount value (non-negative).
            is_available: Whether the product is available for ordering.

        Returns:
            Products: The newly created product.

        Raises:
            ValueError: If the supplier record does not exist.
        """
        supplier = self.validate_supplier()
        product = Products(
            supplier_id=supplier.user_id,
            name=name,
            unit_price=unit_price,
            inventory_quantity=inventory_quantity,
            size=size,
            keywords=keywords,
            category=category,
            discount=discount,
            is_available=is_available
        )
        db.session.add(product)
        db.session.commit()
        return product

    def edit_product(self, product_id, name, unit_price, inventory_quantity, size, keywords, category, discount, is_available):
        """Edit a product owned by the current supplier.

        Args:
            product_id: Product primary key.
            name: New product name.
            unit_price: New unit price.
            inventory_quantity: New inventory quantity.
            size: New size value or None.
            keywords: New keywords string.
            category: New category value.
            discount: New discount value.
            is_available: New availability flag.

        Returns:
            Products: The updated product.

        Raises:
            ValueError: If the supplier record does not exist or product is not found.
        """
        supplier = self.validate_supplier()
        product = Products.query.filter_by(id=product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        product.name = name
        product.unit_price = unit_price
        product.inventory_quantity = inventory_quantity
        product.size = size
        product.keywords = keywords
        product.category = category
        product.discount = discount
        product.is_available = is_available
        db.session.commit()
        return product

    def remove_product(self, product_id):
        """Delete a product by id.

        Args:
            product_id: Product primary key.

        Returns:
            None

        Raises:
            ValueError: If the supplier record does not exist or product is not found.
        """
        supplier = self.validate_supplier()
        product = Products.query.filter_by(id=product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        db.session.delete(product)
        db.session.commit()

    def get_all_suppliers(self):
        """Return all open suppliers ordered by company name.

        Returns:
            list[Suppliers]: Open suppliers sorted ascending by company name.
        """
        suppliers = Suppliers.query.filter(Suppliers.is_open.is_(True)).order_by(Suppliers.company_name.asc()).all()
        return suppliers
