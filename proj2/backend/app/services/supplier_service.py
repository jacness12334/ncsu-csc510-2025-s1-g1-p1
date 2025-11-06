from app.models import *
from app.app import db, get_app

config_name = 'development'
app = get_app(config_name)

with app.app_context():
    pass


## Edit supplier details
## Add, edit, delete products

class SupplierService:

    def __init__(self, user_id):
        self.user_id = user_id


    def validate_supplier(self):
        supplier = Suppliers.query.filter_by(user_id=self.user_id).first()
        if not supplier:
            raise ValueError(f"Supplier {self.user_id} not found")
        return supplier
    

    def edit_supplier(self, company_name, company_address, contact_phone, is_open):
        supplier = self.validate_supplier()
        if not supplier:
            return {"error":"Supplier Not Found"}, 404

        supplier.company_name = company_name
        supplier.company_address = company_address
        supplier.contact_phone = contact_phone
        supplier.is_open = is_open
        db.session.commit()
        return {"message":"Supplier details changed successfully", "supplier_id": supplier.id}, 200
    

    def set_is_open(self, is_open):
        supplier = self.validate_supplier()
        if not supplier:
            return {"error":"Unauthorized User - Not a supplier"}, 404

        supplier.is_open = is_open
        db.session.commit()
        return {"message":f"Supplier set to {is_open}"}, 200
    
    
    def add_product(self, name, unit_price, inventory_quantity, size, keywords, category, is_available):
        supplier = self.validate_supplier()
        if not supplier:
            return {"error":"Unauthorized User - Not a supplier"}, 403
        
        product = Products(supplier_id=supplier.id, name=name, unit_price=unit_price, inventory_quantity=inventory_quantity, size=size, keywords=keywords, category=category, is_available=is_available)
        db.session.add(product)
        db.session.commit()
        return {"message":"Prouct added successfully", "product_id": product.id}, 201
    

    def edit_product(self, product_id, name, unit_price, inventory_quantity, size, keywords, category, is_available):
        supplier = self.validate_supplier()
        if not supplier:
            return {"error":"Unauthorized User - Not a supplier"}, 403
        
        product = Products.query.filter_by(id=product_id).first()
        if not product:
            return {"error":"Product not found"}, 404

        product.name = name
        product.unit_price = unit_price
        product.inventory_quantity = inventory_quantity
        product.size = size
        product.keywords = keywords
        product.category = category
        product.is_available = is_available
        db.session.commit()
        return {"message":"Product details changed successfully", "product_id": product.id}, 200
    

    def remove_product(self, product_id):
        supplier = self.validate_supplier()
        if not supplier:
            return {"error":"Unauthorized User - Not a supplier"}, 403
        
        product = Products.query.filter_by(id=product_id).first()
        if not product:
            return {"error":"Product not found"}, 404
        
        db.session.delete(product)
        db.session.commit()
        return {"message":"Product successfully removed"}, 200

