from app.models import *
from app.app import db

class SupplierService:

    def __init__(self, user_id):
        self.user_id = user_id


    def validate_supplier(self):
        supplier = Suppliers.query.filter_by(user_id=self.user_id).first()
        if not supplier:
            raise ValueError(f"Supplier {self.user_id} not found")
        return supplier
    

    def get_supplier(self):
        supplier = self.validate_supplier()
        return supplier
    

    def edit_supplier(self, company_name, company_address, contact_phone, is_open):
        supplier = self.validate_supplier()
        supplier.company_name = company_name
        supplier.company_address = company_address
        supplier.contact_phone = contact_phone
        supplier.is_open = is_open
        db.session.commit()
        return supplier
    

    def set_is_open(self, is_open):
        supplier = self.validate_supplier()
        supplier.is_open = is_open
        db.session.commit()
        return supplier
    
    
    def get_products(self):
        supplier = self.validate_supplier()
        products = Products.query.filter_by(supplier_id=self.user_id).all()
        return products

    
    
    def add_product(self, name, unit_price, inventory_quantity, size, keywords, category, discount, is_available):
        supplier = self.validate_supplier()
        product = Products(supplier_id=supplier.user_id, name=name, unit_price=unit_price, inventory_quantity=inventory_quantity, size=size, keywords=keywords, category=category, discount=discount, is_available=is_available)
        db.session.add(product)
        db.session.commit()
        return product
    

    def edit_product(self, product_id, name, unit_price, inventory_quantity, size, keywords, category, discount, is_available):
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
        supplier = self.validate_supplier()
        product = Products.query.filter_by(id=product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        db.session.delete(product)
        db.session.commit()

    def get_all_suppliers(self):
        suppliers = Suppliers.query.filter(Suppliers.is_open.is_(True)).order_by(Suppliers.company_name.asc()).all()
        return suppliers
