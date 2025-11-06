import json
from app.app import db
from app.models import Theatres, MovieShowings, Movies, Auditoriums, Seats


class TestCustomerRoutes:    
    
    def test_create_customer_success(self, client, app):
        with app.app_context():
            theatre = Theatres(name='Test Cinema', address='123 Main St', phone='5551234567', is_open=True)
            db.session.add(theatre)
            db.session.commit()
            theatre_id = theatre.id
        
        response = client.post('/api/customers', json={
            'name': 'New Customer',
            'email': 'newcustomer@example.com',
            'phone': '5559998888',
            'birthday': '1990-01-01',
            'password': 'password123',
            'role': 'customer',
            'default_theatre_id': theatre_id
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Customer created successfully'
        assert 'user_id' in data['customer']
        assert data['customer']['default_theatre_id'] == theatre_id
    
    def test_create_customer_missing_fields(self, client):
        response = client.post('/api/customers', json={
            'user_id': 1
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_customer_success(self, client, sample_customer):
        response = client.get(f'/api/customers/{sample_customer}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user_id'] == sample_customer
        assert 'default_theatre_id' in data
    
    def test_get_customer_not_found(self, client):
        response = client.get('/api/customers/99999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_delete_customer_success(self, client, sample_customer):
        response = client.delete(f'/api/customers/{sample_customer}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Customer deleted successfully'
        
        response = client.get(f'/api/customers/{sample_customer}')
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
        
        response = client.put(f'/api/customers/{sample_customer}/theatre', json={
            'theatre_id': theatre_id
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Default theatre updated'
        assert data['customer']['default_theatre_id'] == theatre_id
    
    def test_update_default_theatre_not_found(self, client, sample_customer):
        response = client.put(f'/api/customers/{sample_customer}/theatre', json={
            'theatre_id': 99999
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_add_payment_method_success(self, client, sample_customer):
        response = client.post(f'/api/customers/{sample_customer}/payment-methods', json={
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
        client.post(f'/api/customers/{sample_customer}/payment-methods', json={
            'card_number': '1234567812345678',
            'expiration_month': 12,
            'expiration_year': 2027,
            'billing_address': '789 Pine St',
            'balance': 100.00,
            'is_default': True
        })

        response = client.post(f'/api/customers/{sample_customer}/payment-methods', json={
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
        client.post(f'/api/customers/{sample_customer}/payment-methods', json={
            'card_number': '1111222233334444',
            'expiration_month': 6,
            'expiration_year': 2026,
            'billing_address': 'Address 1',
            'balance': 100.00,
            'is_default': True
        })
        
        client.post(f'/api/customers/{sample_customer}/payment-methods', json={
            'card_number': '5555666677778888',
            'expiration_month': 9,
            'expiration_year': 2028,
            'billing_address': 'Address 2',
            'balance': 200.00,
            'is_default': False
        })
        
        response = client.get(f'/api/customers/{sample_customer}/payment-methods')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'payment_methods' in data
        assert len(data['payment_methods']) == 2
    
    def test_get_payment_methods_none(self, client, sample_customer):
        response = client.get(f'/api/customers/{sample_customer}/payment-methods')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_delete_payment_method_success(self, client, sample_customer):
        add_response = client.post(f'/api/customers/{sample_customer}/payment-methods', json={
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
        add_response = client.post(f'/api/customers/{sample_customer}/payment-methods', json={
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
        add_response = client.post(f'/api/customers/{sample_customer}/payment-methods', json={
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
        
    def test_add_to_cart_success(self, client, app, sample_customer, sample_product):
        with app.app_context():                    
            response = client.post(f'/api/customers/{sample_customer}/cart', json={
                'product_id': sample_product,
                'quantity': 2
            })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Item added to cart'
        assert 'cart_item_id' in data
    
    def test_add_to_cart_invalid_quantity(self, client, sample_customer, sample_product):
        response = client.post(f'/api/customers/{sample_customer}/cart', json={
            'product_id': sample_product,
            'quantity': 0  
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_update_cart_item_success(self, client, sample_customer, sample_product_extra):
        add_response = client.post(f'/api/customers/{sample_customer}/cart', json={
            'product_id': sample_product_extra,
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
    
    def test_delete_cart_item_success(self, client, sample_customer, sample_product):
        add_response = client.post(f'/api/customers/{sample_customer}/cart', json={
            'product_id': sample_product,
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
            from app.services.customer_service import CustomerService
            customer_service = CustomerService()
            customer = customer_service.get_customer(sample_customer)
            theatre_id = customer.default_theatre_id
            
            auditorium = Auditoriums(theatre_id=theatre_id, number=1, capacity=100)
            db.session.add(auditorium)
            db.session.commit()
            
            seat = Seats(aisle='A', number=1, auditorium_id=auditorium.id)
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
        
        response = client.post(f'/api/customers/{sample_customer}/showings', json={
            'movie_showing_id': showing_id,
            'seat_id': seat_id
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Showing booked successfully'
        assert 'customer_showing_id' in data
    
    def test_create_customer_showing_invalid_showing(self, client, sample_customer):
        response = client.post(f'/api/customers/{sample_customer}/showings', json={
            'movie_showing_id': 99999,
            'seat_id': 1
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_delivery_insufficient_funds(self, client, app, sample_customer_showing, sample_driver, sample_product):    
        with app.app_context():
            from app.services.customer_service import CustomerService
            from app.services.user_service import UserService
            from app.models import Staff, CartItems, CustomerShowings
            customer_service = CustomerService()
            user_service = UserService()

            showing = CustomerShowings.query.get(sample_customer_showing)
            customer = customer_service.get_customer(showing.customer_id)

            payment_method = customer_service.add_payment_method(
                user_id=customer.user_id,
                card_number='4111111111111111',
                expiration_month=12,
                expiration_year=2027,
                billing_address='123 Payment St',
                balance=2.00,
                is_default=True
            )   
            staff_user = user_service.create_user(
                name='Test Staff',
                email='staff@example.com',
                phone='5554445555',
                birthday='1987-03-12',
                password='password123',
                role='staff'
            )

            staff = Staff(
                user_id=staff_user.id,
                theatre_id=customer.default_theatre_id,
                role='runner',          
                is_available=True
            )
            db.session.add(staff)
            db.session.commit()

            cart_item = CartItems(
                customer_id=customer.user_id,
                product_id=sample_product,
                quantity=1
            )
            db.session.add(cart_item)
            db.session.commit()

            payment_method_id = payment_method.id
            staff_id = staff.user_id
        response = client.post('/api/deliveries', json={
            'driver_id': sample_driver,
            'customer_showing_id': sample_customer_showing,
            'payment_method_id': payment_method_id,
            'staff_id': staff_id
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
            theatre_id = theatre.id
            
        response = client.post('/api/customers', json={
            'name': 'Flow Customer',
            'email': 'flow@example.com',
            'phone': '5554445555',
            'birthday': '1990-01-01',
            'password': 'password123',
            'role': 'customer',
            'default_theatre_id': theatre_id
        })
        assert response.status_code == 201

        user_id = json.loads(response.data)['customer']['user_id']
        
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
