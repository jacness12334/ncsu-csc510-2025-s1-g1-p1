import pytest
from app.services.supplier_service import SupplierService
from app.models import *
from decimal import Decimal

class TestSupplierService:
        
    def test_validate_supplier_success(self, app, sample_supplier):
        with app.app_context():
            supplier_service = SupplierService(sample_supplier)

            supplier = supplier_service.validate_supplier()
            assert supplier is not None
            assert supplier.user_id is not None
            assert supplier.company_name == "Snacks Inc"


    def test_validate_sample_not_found(self, app, sample_user):
        with app.app_context():
            supplier_service = SupplierService(sample_user)

            with pytest.raises(ValueError, match="not found"):
                supplier_service.validate_supplier()


    def test_get_supplier_returns_correct_supplier(self, app, sample_supplier):
        with app.app_context():
            supplier_service = SupplierService(sample_supplier)
            supplier = supplier_service.get_supplier()
            assert supplier.user_id == sample_supplier
            assert supplier.company_name == "Snacks Inc"
    

    def test_edit_supplier_success(self, app, sample_supplier):
        with app.app_context():
            supplier_service = SupplierService(sample_supplier)
            supplier = supplier_service.edit_supplier(
                company_name='New Name',
                company_address='New Address',
                contact_phone='5559998888',
                is_open=False
            )
            assert supplier.company_name == 'New Name'
            assert supplier.company_address == 'New Address'
            assert supplier.contact_phone == '5559998888'
            assert supplier.is_open == False


    def test_set_is_open(self, app, sample_supplier):
        with app.app_context():
            service = SupplierService(sample_supplier)
            supplier = service.set_is_open(False)
            assert supplier.is_open is False
            supplier = service.set_is_open(True)
            assert supplier.is_open is True


    def test_get_products_returns_list(self, app, sample_supplier, sample_product):
        with app.app_context():
            service = SupplierService(sample_supplier)
            products = service.get_products()
            assert isinstance(products, list)
            assert len(products) > 0
            assert products[0].supplier_id == sample_supplier


    def test_get_products_no_products(self, app, sample_supplier):
        with app.app_context():
            service = SupplierService(sample_supplier)
            Products.query.filter_by(supplier_id=sample_supplier).delete()
            db.session.commit()
            products = service.get_products()
            assert products == []


    def test_add_product_success(self, app, sample_supplier):
        with app.app_context():
            service = SupplierService(sample_supplier)
            product = service.add_product(
                name='Soda',
                unit_price=2.99,
                inventory_quantity=50,
                size='Large',
                keywords='drink',
                category='beverages',
                discount=10,
                is_available=True
            )
            assert product.name == 'Soda'
            assert product.supplier_id == sample_supplier

            db.session.delete(product)
            db.session.commit()

    def test_edit_product_success(self, app, sample_supplier, sample_product):
        with app.app_context():
            service = SupplierService(sample_supplier)
            product = service.edit_product(
                product_id=sample_product,
                name='Popcorn Deluxe',
                unit_price=6.99,
                inventory_quantity=150,
                size='Large',
                keywords='snack, popcorn',
                category='snacks',
                discount=5,
                is_available=False
            )
            assert product.name == 'Popcorn Deluxe'
            assert product.unit_price == Decimal('6.99')
            assert product.inventory_quantity == 150
            assert product.is_available is False


    def test_edit_product_not_found(self, app, sample_supplier):
        with app.app_context():
            service = SupplierService(sample_supplier)
            with pytest.raises(ValueError, match="Product 99999 not found"):
                service.edit_product(
                    product_id=99999,
                    name='X',
                    unit_price=0,
                    inventory_quantity=0,
                    size='N/A',
                    keywords='none',
                    category='none',
                    discount=0,
                    is_available=True
                )


    def test_remove_product_success(self, app, sample_supplier, sample_product):
        with app.app_context():
            service = SupplierService(sample_supplier)
            service.remove_product(sample_product)
            assert Products.query.filter_by(id=sample_product).first() is None


    def test_remove_product_not_found(self, app, sample_supplier):
        with app.app_context():
            service = SupplierService(sample_supplier)
            with pytest.raises(ValueError, match="Product 99999 not found"):
                service.remove_product(99999)
