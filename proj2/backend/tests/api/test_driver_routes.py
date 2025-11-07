import json
from datetime import datetime
from decimal import Decimal
import uuid # Used for generating unique identifiers for test data
from app.app import db
# Explicitly import all necessary models for test helpers
from app.models import Users, Drivers, Deliveries, Theatres, Staff, CustomerShowings, PaymentMethods, CartItems, Products, Movies, Auditoriums, Seats, MovieShowings, Customers, Suppliers

# Mock Hashed Password - This assumes 'password_hash' is the column name.
MOCK_PASSWORD_HASH = "mock-test-hash"

# Define valid ENUM status codes for testing helpers (from Drivers model)
STATUS_AVAILABLE = 'available'
STATUS_UNAVAILABLE = 'unavailable'
STATUS_ON_DELIVERY = 'on_delivery'


class TestDriverRoutes:

    def _create_test_driver(self, app, duty_status=STATUS_AVAILABLE, rating=5.0, deliveries=0, vehicle_color='Blue'):
        """Helper to create a fresh driver for testing."""
        unique_id = uuid.uuid4().hex[:8] 
        # Generate unique phone/email to prevent IntegrityError
        unique_phone = f'555111{unique_id[:4]}'
        unique_email = f'driver_{unique_id}@test.com'
        
        with app.app_context():
            user = Users(
                name='Test Driver',
                email=unique_email,
                phone=unique_phone, 
                birthday=datetime(1995, 5, 5),
                password_hash=MOCK_PASSWORD_HASH,
                role='driver',
            )
            db.session.add(user)
            db.session.flush() # Get user ID before commit
            
            driver = Drivers(
                user_id=user.id,
                license_plate='XYZ123',
                vehicle_type='car', 
                vehicle_color=vehicle_color,
                duty_status=duty_status, 
                rating=rating,
                total_deliveries=deliveries
            )
            db.session.add(driver)
            db.session.commit()
            return user.id, driver
    
    def _create_test_delivery(self, app, driver_id=None, delivery_status='pending'):
        """Helper to create a delivery with all necessary prerequisites."""
        
        # Use a short unique ID for elements that require uniqueness (names/emails/phones)
        unique_id = uuid.uuid4().hex[:6]
        
        with app.app_context():
            # 1. Theatre setup (Needed for Staff, Auditoriums, Customers)
            # Use unique names to prevent IntegrityError on unique_theatre_address
            theatre = Theatres(
                name=f'Test Cinema {unique_id}', 
                address=f'101 Delivery Ave {unique_id}', 
                phone=f'555000{unique_id[:4]}', 
                is_open=True
            )
            db.session.add(theatre)
            db.session.flush()

            # 2. Movie Showing / Seat Setup (REQUIRED to satisfy CustomerShowings FKs)
            movie = Movies(
                title=f'Test Movie {unique_id}',
                genre='Action',
                length_mins=120,
                release_year=2024,
                keywords='test',
                rating=Decimal('4.50')
            )
            db.session.add(movie)
            db.session.flush()

            auditorium = Auditoriums(
                theatre_id=theatre.id,
                number=1,
                capacity=100
            )
            db.session.add(auditorium)
            db.session.flush()

            seat = Seats(
                auditorium_id=auditorium.id,
                aisle='A',
                number=1
            )
            db.session.add(seat)
            db.session.flush()

            movie_showing = MovieShowings(
                movie_id=movie.id,
                auditorium_id=auditorium.id,
                start_time=datetime(2025, 12, 1, 19, 0, 0)
            )
            db.session.add(movie_showing)
            db.session.flush()

            # 3. Staff/Supplier setup (required for Delivery and Products)
            staff_user = Users(
                name='Test Staff',
                email=f'staff_{unique_id}@test.com',
                phone=f'555333{unique_id[:4]}', # Unique phone
                birthday=datetime(1990, 1, 1),
                password_hash=MOCK_PASSWORD_HASH,
                role='staff'
            )
            db.session.add(staff_user)
            db.session.flush()
            
            # Staff object
            staff = Staff(user_id=staff_user.id, theatre_id=theatre.id, role='runner', is_available=True)
            db.session.add(staff)
            
            # Create a Supplier object (needed for Products FK)
            supplier = Suppliers(
                user_id=staff_user.id,
                company_name=f'Test Snacks Inc. {unique_id}',
                company_address=f'456 Supply Road {unique_id}',
                contact_phone=f'555888{unique_id[:4]}', 
                is_open=True
            )
            db.session.add(supplier)
            
            # 4. Customer/Customer Showing setup (required for Delivery)
            customer_user = Users(
                name='Test Customer',
                email=f'customer_{unique_id}@test.com',
                phone=f'555555{unique_id[:4]}', # Unique phone
                birthday=datetime(2000, 1, 1),
                password_hash=MOCK_PASSWORD_HASH,
                role='customer'
            )
            db.session.add(customer_user)
            db.session.flush()

            customer = Customers(user_id=customer_user.id, default_theatre_id=theatre.id)
            db.session.add(customer)
            db.session.flush()


            # Create a placeholder CustomerShowing
            customer_showing = CustomerShowings(
                customer_id=customer_user.id, 
                movie_showing_id=movie_showing.id, 
                seat_id=seat.id, 
            )
            db.session.add(customer_showing)
            db.session.flush()

            # 5. Product and Cart setup
            product = Products(
                name=f'Test Snack {unique_id}',
                supplier_id=supplier.user_id, 
                unit_price=Decimal('10.00'),
                inventory_quantity=100,
                category='snacks'
            )
            db.session.add(product)
            db.session.flush()

            # CartItems uses customer_id/user_id
            cart_item = CartItems(
                customer_id=customer_user.id, 
                product_id=product.id,
                quantity=2
            )
            db.session.add(cart_item)
            db.session.flush()

            # 6. Payment Method setup
            payment_method = PaymentMethods(
                customer_id=customer_user.id, 
                card_number='1111222233334444', 
                expiration_month=12,
                expiration_year=2027,
                billing_address='123 Pay St',
                balance=Decimal('100.00'),
                is_default=True
            )
            db.session.add(payment_method)
            db.session.flush()

            # 7. Delivery setup
            delivery = Deliveries(
                driver_id=driver_id,
                customer_showing_id=customer_showing.id,
                payment_method_id=payment_method.id,
                staff_id=staff.user_id,
                total_price=Decimal('20.00'), # Mocking total price calculation result
                payment_status='completed', # Assuming payment passed for a test delivery
                delivery_status=delivery_status
            )
            db.session.add(delivery)
            db.session.commit()
            return delivery.id, driver_id, customer_user.id


    # --- Utility function to display server error response ---
    def _get_error_message(self, response):
        try:
            data = json.loads(response.data)
            return data.get('error', f"Unknown error (Status {response.status_code})")
        except:
            return f"Non-JSON response (Status {response.status_code})"


    # --- Admin/Staff Routes for Driver Management ---

    def test_create_driver_success(self, client, app):
        data = {
            'name': 'New Admin Driver',
            'email': f'newdriver_{uuid.uuid4().hex[:4]}@example.com',
            'phone': f'555111{uuid.uuid4().hex[:4]}',
            'birthday': '1985-06-15',
            'password': 'adminpass', 
            'role': 'driver',
            'license_plate': 'PQR789',
            'vehicle_type': 'car', 
            'vehicle_color': 'Red',
            'duty_status': STATUS_UNAVAILABLE, 
            'rating': 4.8,
            'total_deliveries': 100
        }
        
        response = client.post('/api/driver', json=data)
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Driver created successfully'
        assert 'user_id' in data

    def test_create_driver_missing_fields(self, client):
        response = client.post('/api/driver', json={
            'name': 'Missing Driver',
            'email': 'missing@example.com',
            'phone': '5551110000',
            'password': 'pass',
            # Missing required fields
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Missing required user or driver fields' in data['error']
        
    def test_delete_driver_success(self, client, app):
        user_id, _ = self._create_test_driver(app) 
        
        response = client.delete(f'/api/driver/{user_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == f'Driver {user_id} deleted successfully'
        
        # Verify the driver is marked as deleted/no longer accessible
        response = client.get(f'/api/driver/{user_id}')
        assert response.status_code == 404
    
    def test_delete_driver_not_found(self, client):
        response = client.delete('/api/driver/999999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data


    # --- Driver Information and Status Update ---
    
    def test_get_driver_info_success(self, client, app):
        user_id, driver = self._create_test_driver(app, duty_status=STATUS_ON_DELIVERY, rating=4.9, deliveries=50)

        response = client.get(f'/api/driver/{user_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)['driver']
        assert data['user_id'] == user_id
        assert data['duty_status'] == STATUS_ON_DELIVERY
        assert data['rating'] == 4.9
        assert data['total_deliveries'] == 50
    
    def test_get_driver_info_not_found(self, client):
        response = client.get('/api/driver/999999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_update_driver_details_success(self, client, app):
        user_id, _ = self._create_test_driver(app, vehicle_color='Blue') 
        
        response = client.put(f'/api/driver/{user_id}', json={
            'license_plate': 'NEWPLATE',
            'vehicle_type': 'bike', 
            'vehicle_color': 'Yellow'
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Driver details updated'
        
        # Verify update
        verify_response = client.get(f'/api/driver/{user_id}')
        verify_data = json.loads(verify_response.data)['driver']
        assert verify_data['vehicle_color'] == 'Yellow'
        assert verify_data['vehicle_type'] == 'bike'

    def test_update_driver_details_missing_fields(self, client, app):
        user_id, _ = self._create_test_driver(app)

        response = client.put(f'/api/driver/{user_id}', json={
            'vehicle_type': 'car',
            # Missing license_plate, vehicle_color
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Missing required fields' in data['error']

    def test_update_driver_status_success(self, client, app):
        user_id, _ = self._create_test_driver(app, duty_status=STATUS_UNAVAILABLE)

        response = client.put(f'/api/driver/{user_id}/status', json={
            'new_status': STATUS_AVAILABLE 
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'].startswith(f'Duty status updated to {STATUS_AVAILABLE}')
        assert data['duty_status'] == STATUS_AVAILABLE
        
    def test_update_driver_status_invalid_status(self, client, app):
        user_id, _ = self._create_test_driver(app, duty_status=STATUS_UNAVAILABLE)

        response = client.put(f'/api/driver/{user_id}/status', json={
            'new_status': 'driving_around' 
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_update_driver_status_missing_field(self, client, app):
        user_id, _ = self._create_test_driver(app, duty_status=STATUS_UNAVAILABLE)

        response = client.put(f'/api/driver/{user_id}/status', json={})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Missing new_status field' in data['error']

    # --- Delivery Assignment and Rating ---
    
    def test_assign_driver_success(self, client, app):
        driver_id, _ = self._create_test_driver(app, duty_status=STATUS_AVAILABLE)
        delivery_id, _, _ = self._create_test_delivery(app, driver_id=None, delivery_status='pending')
        
        response = client.put(f'/api/deliveries/assign/{delivery_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'].startswith(f'Delivery {delivery_id} successfully assigned')
        assert data['assigned_driver_id'] == driver_id
        assert data['delivery_status'] == 'accepted'

    def test_assign_driver_no_available_drivers(self, client, app):
        self._create_test_driver(app, duty_status=STATUS_UNAVAILABLE)
        delivery_id, _, _ = self._create_test_delivery(app, driver_id=None, delivery_status='pending')

        response = client.put(f'/api/deliveries/assign/{delivery_id}')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['message'] == 'No available drivers found.'
        
    def test_complete_delivery_success(self, client, app):
        driver_id, driver = self._create_test_driver(app, duty_status=STATUS_ON_DELIVERY, deliveries=5)
        delivery_id, _, _ = self._create_test_delivery(app, driver_id=driver_id, delivery_status='accepted') 
        
        response = client.put(f'/api/deliveries/{delivery_id}/complete')
        
        # Enhanced Assertion for debugging
        if response.status_code != 200:
            error_msg = self._get_error_message(response)
            assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Error: {error_msg}"

        data = json.loads(response.data)
        assert data['message'] == f'Delivery {delivery_id} marked as delivered/completed.'
        assert data['new_status'] == 'delivered'

    def test_complete_delivery_not_found(self, client):
        response = client.put('/api/deliveries/999999/complete')
        
        assert response.status_code == 400 
        data = json.loads(response.data)
        assert 'error' in data

    def test_rate_driver_success(self, client, app):
        driver_id, driver = self._create_test_driver(app, rating=4.0, deliveries=10)
        delivery_id, _, _ = self._create_test_delivery(app, driver_id=driver_id, delivery_status='fulfilled') 
        
        response = client.put(f'/api/deliveries/{delivery_id}/rate', json={'rating': 5})
        
        # Enhanced Assertion for debugging
        if response.status_code != 200:
            error_msg = self._get_error_message(response)
            assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Error: {error_msg}"

        data = json.loads(response.data)
        assert data['message'].startswith(f'Driver {driver_id} rated successfully.')
        # Expected new rating: (4.0 * 10 + 5) / (10 + 1) = 45 / 11 = 4.0909...
        assert round(data['new_rating'], 2) == 4.09

    def test_rate_driver_missing_rating(self, client, app):
        driver_id, _ = self._create_test_driver(app)
        delivery_id, _, _ = self._create_test_delivery(app, driver_id=driver_id, delivery_status='fulfilled') # Need fulfilled status to reach failure check

        response = client.put(f'/api/deliveries/{delivery_id}/rate', json={})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Missing rating field' in data['error']
        
    def test_rate_driver_delivery_not_completed(self, client, app):
        driver_id, _ = self._create_test_driver(app)
        # Test status: pending, which is not 'fulfilled'
        delivery_id, _, _ = self._create_test_delivery(app, driver_id=driver_id, delivery_status='pending')

        response = client.put(f'/api/deliveries/{delivery_id}/rate', json={'rating': 5})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Can only rate fulfilled deliveries' in data['error']


    # --- Driver Delivery Views ---
    
    def test_get_active_delivery_found(self, client, app):
        driver_id, _ = self._create_test_driver(app)
        delivery_id, _, _ = self._create_test_delivery(app, driver_id=driver_id, delivery_status='in_progress')
        
        response = client.get(f'/api/driver/{driver_id}/active-delivery')
        
        # Enhanced Assertion for debugging
        if response.status_code != 200:
            error_msg = self._get_error_message(response)
            assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Error: {error_msg}"

        data = json.loads(response.data)['active_delivery']
        assert data['id'] == delivery_id
        assert data['delivery_status'] == 'in_progress'

    def test_get_active_delivery_not_found(self, client, app):
        driver_id, _ = self._create_test_driver(app)
        self._create_test_delivery(app, driver_id=driver_id, delivery_status='fulfilled')

        response = client.get(f'/api/driver/{driver_id}/active-delivery')
        
        # FIX: Changed expected status from 200 to 404 based on driver_service implementation
        if response.status_code != 404:
            error_msg = self._get_error_message(response)
            assert response.status_code == 404, f"Expected 404 but got {response.status_code}. Error: {error_msg}"
        
        data = json.loads(response.data)
        assert 'error' in data

    def test_show_completed_deliveries_found(self, client, app):
        driver_id, _ = self._create_test_driver(app)
        d1_id, _, _ = self._create_test_delivery(app, driver_id=driver_id, delivery_status='fulfilled')
        d2_id, _, _ = self._create_test_delivery(app, driver_id=driver_id, delivery_status='fulfilled')
        
        # Create an incomplete one to ensure filter works
        self._create_test_delivery(app, driver_id=driver_id, delivery_status='accepted')

        response = client.get(f'/api/driver/{driver_id}/history')
        
        # Enhanced Assertion for debugging
        if response.status_code != 200:
            error_msg = self._get_error_message(response)
            assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Error: {error_msg}"

        data = json.loads(response.data)['history']
        assert len(data) == 2
        assert {d1_id, d2_id} == {d['id'] for d in data}
        assert all(d['delivery_status'] == 'fulfilled' for d in data)

    def test_show_completed_deliveries_none(self, client, app):
        driver_id, _ = self._create_test_driver(app)
        # Create an active delivery (not fulfilled)
        self._create_test_delivery(app, driver_id=driver_id, delivery_status='accepted')

        response = client.get(f'/api/driver/{driver_id}/history')
        
        if response.status_code != 404:
            error_msg = self._get_error_message(response)
            assert response.status_code == 404, f"Expected 404 but got {response.status_code}. Error: {error_msg}"

        data = json.loads(response.data)
        assert 'error' in data
        assert f'No previous deliveries found for driver {driver_id}' in data['error']
        
    def test_show_completed_deliveries_driver_not_found(self, client):
        response = client.get('/api/driver/999999/history')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data