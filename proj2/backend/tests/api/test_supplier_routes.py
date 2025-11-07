import json
from app.app import db
from app.models import *
from decimal import Decimal


class TestSupplierRoutes:

    def test_get_supplier_success(self, client, sample_supplier):
        response = client.get('/api/suppliers', json={'user_id': sample_supplier})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['supplier']['company_name'] == "Snacks Inc"
        assert data['supplier']['is_open'] is True

    def test_get_supplier_not_found(self, client):
        response = client.get('/api/suppliers', json={'user_id': 9999})
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['error'] == "Supplier 9999 not found"

    def test_edit_supplier_success(self, client, sample_supplier):
        response = client.put('/api/suppliers', json={
            'user_id': sample_supplier, 
            'company_name': 'Updated Supplier',
            'company_address': '456 Updated St.',
            'contact_phone': '555-1234',
            'is_open': False
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == "Supplier details changed successfully"
        assert data['supplier_id'] == sample_supplier

        updated_supplier = Suppliers.query.filter_by(user_id=sample_supplier).first()
        assert updated_supplier.company_name == 'Updated Supplier'
        assert updated_supplier.is_open is False

    def test_edit_supplier_missing_fields(self, client, sample_supplier):
        response = client.put('/api/suppliers', json={
            'user_id': sample_supplier,
            'company_name': 'Updated Supplier',
            'company_address': '456 Updated St.',
            'contact_phone': '555-1234'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == "Missing required fields"

    def test_set_availability_success(self, client, sample_supplier):
        response = client.put('/api/suppliers/status', json={'user_id': sample_supplier, 'is_open': False})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == "Supplier set to False"

        updated_supplier = Suppliers.query.filter_by(user_id=sample_supplier).first()
        assert updated_supplier.is_open is False

    def test_set_availability_missing_is_open(self, client, sample_supplier):
        response = client.put('/api/suppliers/status', json={'user_id': sample_supplier})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == "Missing is_open field"

    def test_get_products_success(self, client, sample_supplier, sample_product):
        response = client.get('/api/products', json={'user_id': sample_supplier})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['products']) == 1
        assert data['products'][0]['name'] == "Popcorn"
        assert data['products'][0]['unit_price'] == 5.99

    def test_get_products_no_products(self, client, sample_supplier):
        response = client.get('/api/products', json={'user_id': sample_supplier})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['products']) == 0

    def test_add_product_success(self, client, sample_supplier):
        response = client.post('/api/products', json={
            'user_id': sample_supplier,
            'name': 'New Product',
            'unit_price': 15.0,
            'inventory_quantity': 200,
            'size': 'large',
            'keywords': 'new, product',
            'category': 'snacks',
            'discount': 0.05,
            'is_available': True
        })
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == "Product added successfully"
        assert data['product_id'] is not None

        product = Products.query.filter_by(id=data['product_id']).first()
        assert product.name == "New Product"
        assert product.unit_price == 15.0

    def test_add_product_missing_fields(self, client, sample_supplier):
        response = client.post('/api/products', json={
            'user_id': sample_supplier,
            'name': 'New Product',
            'unit_price': 15.0,
            'inventory_quantity': 200,
            'size': 'large',
            'keywords': 'new, product',
            'category': 'snacks'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == "Missing required fields"

    def test_edit_product_success(self, client, sample_product):
        response = client.put(f'/api/products/{sample_product}', json={
            'user_id': sample_product,
            'name': 'Updated Product',
            'unit_price': 20.0,
            'inventory_quantity': 150,
            'size': 'large',
            'keywords': 'updated, product',
            'category': 'snacks',
            'discount': 0.1,
            'is_available': False
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == "Product details changed successfully"
        assert data['product_id'] == sample_product

        updated_product = Products.query.filter_by(id=sample_product).first()
        assert updated_product.name == 'Updated Product'
        assert updated_product.unit_price == 20.0

    def test_edit_product_not_found(self, client, sample_supplier):
        response = client.put('/api/products/9999', json={
            'user_id': sample_supplier,
            'name': 'Nonexistent Product',
            'unit_price': 30.0,
            'inventory_quantity': 100,
            'size': 'small',
            'keywords': 'nonexistent',
            'category': 'snacks',
            'discount': 0.2,
            'is_available': True
        })
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['error'] == "Product 9999 not found"

    def test_remove_product_success(self, client, sample_product):
        response = client.delete(f'/api/products/{sample_product}', json={'user_id': sample_product})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == "Product successfully removed"

        removed_product = Products.query.filter_by(id=sample_product).first()
        assert removed_product is None

    def test_remove_product_not_found(self, client, sample_supplier):
        response = client.delete('/api/products/9999', json={'user_id': sample_supplier})
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['error'] == "Product 9999 not found"