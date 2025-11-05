import pytest
import json
from app import db
from models import Theatres, Products, Suppliers, MovieShowings, Movies, Auditoriums, Seats


class TestCustomerRoutes:    
    
    def test_create_customer_success(self, client, app):
        with app.app_context():
            theatre = Theatres(name='Test Cinema', address='123 Main St', phone='5551234567', is_open=True)
            db.session.add(theatre)
            db.session.commit()
            
            from services.user_service import UserService
            user_service = UserService()
            user = user_service.create_user(
                name='New Customer',
                email='newcustomer@example.com',
                phone='5559998888',
                birthday='1990-01-01',
                password='password123',
                role='customer'
            )
        
        response = client.post('/api/customers', json={
            'user_id': user.id,
            'default_theatre_id': theatre.id
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Customer created successfully'
        assert data['customer']['user_id'] == user.id
        assert data['customer']['default_theatre_id'] == theatre.id
    
    def test_create_customer_missing_fields(self, client):
        response = client.post('/api/customers', json={
            'user_id': 1
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_customer_success(self, client, sample_customer):
        response = client.get(f'/api/customers/{sample_customer.user_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user_id'] == sample_customer.user_id
        assert 'default_theatre_id' in data
    
    def test_get_customer_not_found(self, client):
        response = client.get('/api/customers/99999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_delete_customer_success(self, client, sample_customer):
        response = client.delete(f'/api/customers/{sample_customer.user_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Customer deleted successfully'
        
        response = client.get(f'/api/customers/{sample_customer.user_id}')
        assert response.status_code == 404
    
    def test_delete_customer_not_found(self, client):
        response = client.delete('/api/customers/99999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_update_default_theatre_success(self, client, app, sample_customer):
        with app.app_context():
            new_theatre = Theatres(name='New Cinema', address='456 Oak St', phone='5559999999', is_open=True)
            db.session.add(new_theatre)
            db.session.commit()
            theatre_id = new_theatre.id
        
        response = client.put(f'/api/customers/{sample_customer.user_id}/theatre', json={
            'theatre_id': theatre_id
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Default theatre updated'
        assert data['customer']['default_theatre_id'] == theatre_id
    
    def test_update_default_theatre_not_found(self, client, sample_customer):
        response = client.put(f'/api/customers/{sample_customer.user_id}/theatre', json={
            'theatre_id': 99999
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_add_payment_method_success(self, client, sample_customer):
        response = client.post(f'/api/customers/{sample_customer.user_id}/payment-methods', json={
            'card_number': '1234567812345678',
            'expiration_month': 12,
            'expiration_year': 2027,
            'billing_address': '789 Pine St',
            'balance': 100.00,
            'is_default': True
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Payment method added'
        assert 'payment_method_id' in data
    
    def test_add_payment_method_duplicate(self, client, sample_customer):
        client.post(f'/api/customers/{sample_customer.user_id}/payment-methods', json={
            'card_number': '1234567812345678',
            'expiration_month': 12,
            'expiration_year': 2027,
            'billing_address': '789 Pine St',
            'balance': 100.00,
            'is_default': True
        })

        response = client.post(f'/api/customers/{sample_customer.user_id}/payment-methods', json={
            'card_number': '1234567812345678',
            'expiration_month': 12,
            'expiration_year': 2027,
            'billing_address': 'Different Address',
            'balance': 50.00,
            'is_default': False
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_payment_methods_success(self, client, sample_customer):
        client.post(f'/api/customers/{sample_customer.user_id}/payment-methods', json={
            'card_number': '1111222233334444',
            'expiration_month': 6,
            'expiration_year': 2026,
            'billing_address': 'Address 1',
            'balance': 100.00,
            'is_default': True
        })
        
        client.post(f'/api/customers/{sample_customer.user_id}/payment-methods', json={
            'card_number': '5555666677778888',
            'expiration_month': 9,
            'expiration_year': 2028,
            'billing_address': 'Address 2',
            'balance': 200.00,
            'is_default': False
        })
        
        response = client.get(f'/api/customers/{sample_customer.user_id}/payment-methods')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'payment_methods' in data
        assert len(data['payment_methods']) == 2
    
    def test_get_payment_methods_none(self, client, sample_customer):
        response = client.get(f'/api/customers/{sample_customer.user_id}/payment-methods')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_delete_payment_method_success(self, client, sample_customer):
        add_response = client.post(f'/api/customers/{sample_customer.user_id}/payment-methods', json={
            'card_number': '1234567812345678',
            'expiration_month': 12,
            'expiration_year': 2027,
            'billing_address': '789 Pine St',
            'balance': 100.00,
            'is_default': True
        })
        pm_id = json.loads(add_response.data)['payment_method_id']
        
        response = client.delete(f'/api/payment-methods/{pm_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Payment method deleted'
    
    def test_delete_payment_method_not_found(self, client):
        response = client.delete('/api/payment-methods/99999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_add_funds_success(self, client, sample_customer):
        add_response = client.post(f'/api/customers/{sample_customer.user_id}/payment-methods', json={
            'card_number': '1234567812345678',
            'expiration_month': 12,
            'expiration_year': 2027,
            'billing_address': '789 Pine St',
            'balance': 100.00,
            'is_default': True
        })
        pm_id = json.loads(add_response.data)['payment_method_id']
        
        response = client.post(f'/api/payment-methods/{pm_id}/add-funds', json={
            'amount': 50.00
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Funds added successfully'
        assert data['new_balance'] == 150.00
    
    def test_add_funds_invalid_amount(self, client, sample_customer):
        add_response = client.post(f'/api/customers/{sample_customer.user_id}/payment-methods', json={
            'card_number': '1234567812345678',
            'expiration_month': 12,
            'expiration_year': 2027,
            'billing_address': '789 Pine St',
            'balance': 100.00,
            'is_default': True
        })
        pm_id = json.loads(add_response.data)['payment_method_id']
        
        response = client.post(f'/api/payment-methods/{pm_id}/add-funds', json={
            'amount': 0.00
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_add_to_cart_success(self, client, app, sample_customer):
        with app.app_context():
            from services.user_service import UserService
            user_service = UserService()
            supplier_user = user_service.create_user(
                name='Supplier',
                email='supplier@example.com',
                phone='5551112222',
                birthday='1980-01-01',
                password='password123',
                role='supplier'
            )
            
            supplier = Suppliers(
                user_id=supplier_user.id,
                company_name='Snacks Inc',
                company_address='123 Supply St',
                contact_phone='5553334444'
            )
            db.session.add(supplier)
            db.session.commit()
            
            product = Products(
                supplier_id=supplier.user_id,
                name='Popcorn',
                unit_price=5.99,
                inventory_quantity=100,
                category='snacks',
                is_available=True
            )
            db.session.add(product)
            db.session.commit()
            product_id = product.id
        
        response = client.post(f'/api/customers/{sample_customer.user_id}/cart', json={
            'product_id': product_id,
            'quantity': 2
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Item added to cart'
        assert 'cart_item_id' in data
    
    def test_add_to_cart_invalid_quantity(self, client, sample_customer):
        response = client.post(f'/api/customers/{sample_customer.user_id}/cart', json={
            'product_id': 1,
            'quantity': 0  
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_update_cart_item_success(self, client, app, sample_customer):
        with app.app_context():
            product = Products(
                supplier_id=1,
                name='Soda',
                unit_price=3.99,
                inventory_quantity=50,
                category='beverages',
                is_available=True
            )
            db.session.add(product)
            db.session.commit()
            product_id = product.id
        
        add_response = client.post(f'/api/customers/{sample_customer.user_id}/cart', json={
            'product_id': product_id,
            'quantity': 1
        })
        cart_item_id = json.loads(add_response.data)['cart_item_id']
        
        response = client.put(f'/api/cart/{cart_item_id}', json={
            'quantity': 3
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Cart item updated'
        assert data['new_quantity'] == 4  
    
    def test_update_cart_item_not_found(self, client):
        response = client.put('/api/cart/99999', json={
            'quantity': 1
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_delete_cart_item_success(self, client, app, sample_customer):
        with app.app_context():
            product = Products(
                supplier_id=1,
                name='Candy',
                unit_price=2.99,
                inventory_quantity=100,
                category='candy',
                is_available=True
            )
            db.session.add(product)
            db.session.commit()
            product_id = product.id
        
        add_response = client.post(f'/api/customers/{sample_customer.user_id}/cart', json={
            'product_id': product_id,
            'quantity': 2
        })
        cart_item_id = json.loads(add_response.data)['cart_item_id']
        
        response = client.delete(f'/api/cart/{cart_item_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Cart item deleted'
    
    def test_delete_cart_item_not_found(self, client):
        response = client.delete('/api/cart/99999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_create_customer_showing_success(self, client, app, sample_customer):
        with app.app_context():
            theatre = Theatres(name='Cinema', address='123 St', phone='5551111111', is_open=True)
            db.session.add(theatre)
            db.session.commit()
            
            auditorium = Auditoriums(theatre_id=theatre.id, number=1, capacity=100)
            db.session.add(auditorium)
            db.session.commit()
            
            seat = Seats(aisle='A', number=10, auditorium_id=auditorium.id)
            db.session.add(seat)
            db.session.commit()
            
            movie = Movies(
                title='Test Movie',
                genre='Action',
                length_mins=120,
                release_year=2024,
                keywords='test',
                rating=4.5
            )
            db.session.add(movie)
            db.session.commit()
            
            showing = MovieShowings(
                movie_id=movie.id,
                auditorium_id=auditorium.id,
                start_time='2025-12-01 19:00:00'
            )
            db.session.add(showing)
            db.session.commit()
            
            showing_id = showing.id
            seat_id = seat.id
        
        response = client.post(f'/api/customers/{sample_customer.user_id}/showings', json={
            'movie_showing_id': showing_id,
            'seat_id': seat_id
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Showing booked successfully'
        assert 'customer_showing_id' in data
    
    def test_create_customer_showing_invalid_showing(self, client, sample_customer):
        response = client.post(f'/api/customers/{sample_customer.user_id}/showings', json={
            'movie_showing_id': 99999,
            'seat_id': 1
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_delivery_insufficient_funds(self, client, app, sample_customer):       
        response = client.post('/api/deliveries', json={
            'driver_id': 1,
            'customer_showing_id': 1,
            'payment_method_id': 1,
            'staff_id': 1
        })
        
        assert response.status_code in [400, 402, 500]
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_complete_delivery_payment_not_found(self, client):
        response = client.post('/api/deliveries/99999/complete-payment')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_cancel_delivery_not_found(self, client):
        response = client.post('/api/deliveries/99999/cancel')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_customer_flow(self, client, app):
        with app.app_context():
            theatre = Theatres(name='Cinema', address='123 St', phone='5551111111', is_open=True)
            db.session.add(theatre)
            db.session.commit()
            
            from services.user_service import UserService
            user_service = UserService()
            user = user_service.create_user(
                name='Flow Customer',
                email='flow@example.com',
                phone='5554445555',
                birthday='1990-01-01',
                password='password123',
                role='customer'
            )
            user_id = user.id
            theatre_id = theatre.id
        
        response = client.post('/api/customers', json={
            'user_id': user_id,
            'default_theatre_id': theatre_id
        })
        assert response.status_code == 201
        
        response = client.post(f'/api/customers/{user_id}/payment-methods', json={
            'card_number': '1234567812345678',
            'expiration_month': 12,
            'expiration_year': 2027,
            'billing_address': '789 Pine St',
            'balance': 100.00,
            'is_default': True
        })
        assert response.status_code == 201
        
        response = client.get(f'/api/customers/{user_id}')
        assert response.status_code == 200
        
        response = client.delete(f'/api/customers/{user_id}')
        assert response.status_code == 200
