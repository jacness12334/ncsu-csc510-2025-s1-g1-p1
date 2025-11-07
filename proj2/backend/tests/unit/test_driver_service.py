import pytest
import json
from datetime import datetime
from decimal import Decimal
import uuid
from app.app import db
from app.models import Users, Drivers, Deliveries, Theatres, Staff, CustomerShowings, PaymentMethods, CartItems, Products, Movies, Auditoriums, Seats, MovieShowings, Customers, Suppliers
from app.services.driver_service import DriverService

# Mock Hashed Password
MOCK_PASSWORD_HASH = "mock-test-hash"

# Define valid ENUM status codes
STATUS_AVAILABLE = 'available'
STATUS_UNAVAILABLE = 'unavailable'
STATUS_ON_DELIVERY = 'on_delivery'


@pytest.fixture
def driver_service():
    """Fixture to instantiate the DriverService."""
    return DriverService()

def _create_test_driver(app, duty_status=STATUS_AVAILABLE, rating=Decimal('5.0'), deliveries=0, vehicle_color='Blue'):
    """Helper to create a fresh driver for testing."""
    unique_id = uuid.uuid4().hex[:8] 
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
        db.session.flush() 
        
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

def _create_delivery(app, driver_id, showing_id, payment_id, status, is_rated=False):
    """Internal helper to quickly create a delivery record."""
    with app.app_context():
        delivery = Deliveries(
            driver_id=driver_id,
            customer_showing_id=showing_id,
            payment_method_id=payment_id,
            staff_id=None,
            total_price=Decimal('10.00'),
            delivery_status=status,
            payment_status='completed',
            is_rated=is_rated
        )
        db.session.add(delivery)
        db.session.commit()
        return delivery.id

@pytest.fixture
def setup_prerequisites(app):
    """Helper fixture to create all dependencies required for DriverService
    logic."""
    unique_id = uuid.uuid4().hex[:6]
    with app.app_context():
        # 1. Theatre Setup
        theatre = Theatres(
            name=f'Test Cinema {unique_id}', 
            address=f'101 Delivery Ave {unique_id}', 
            phone=f'555000{unique_id[:4]}', 
            is_open=True
        )
        db.session.add(theatre)
        db.session.flush()

        # 2. Movie/Seat Setup
        movie = Movies(
            title=f'Test Movie {unique_id}', genre='Action', length_mins=120, release_year=2024,
            keywords='test', rating=Decimal('4.50')
        )
        db.session.add(movie)
        auditorium = Auditoriums(theatre_id=theatre.id, number=1, capacity=100)
        db.session.add(auditorium)
        db.session.flush()
        seat = Seats(auditorium_id=auditorium.id, aisle='A', number=1)
        db.session.add(seat)
        movie_showing = MovieShowings(movie_id=movie.id, auditorium_id=auditorium.id, start_time=datetime(2025, 12, 1, 19, 0, 0))
        db.session.add(movie_showing)
        db.session.flush()

        # 3. Customer/Payment Method Setup
        customer_user = Users(
            name='Test Customer', email=f'customer_{unique_id}@test.com', phone=f'555555{unique_id[:4]}',
            birthday=datetime(2000, 1, 1), password_hash=MOCK_PASSWORD_HASH, role='customer'
        )
        db.session.add(customer_user)
        db.session.flush()
        customer = Customers(user_id=customer_user.id, default_theatre_id=theatre.id)
        db.session.add(customer)
        db.session.flush()

        payment_method = PaymentMethods(
            customer_id=customer_user.id, card_number='1111222233334444', expiration_month=12,
            expiration_year=2027, billing_address='123 Pay St', balance=Decimal('100.00'), is_default=True
        )
        db.session.add(payment_method)
        db.session.flush()

        customer_showing = CustomerShowings(
            customer_id=customer_user.id, movie_showing_id=movie_showing.id, seat_id=seat.id
        )
        db.session.add(customer_showing)
        db.session.flush()
        
        # 4. Supplier/Product/Cart setup (Needed for total_price logic)
        supplier_user = Users(name='Test Supplier', email=f'supplier_{unique_id}@test.com', phone=f'555444{unique_id[:4]}', birthday=datetime(1990, 1, 1), password_hash=MOCK_PASSWORD_HASH, role='supplier')
        db.session.add(supplier_user)
        db.session.flush()
        supplier = Suppliers(user_id=supplier_user.id, company_name=f'Test Inc. {unique_id}', company_address='789 Supply', contact_phone='5557778888')
        db.session.add(supplier)
        db.session.commit() 

        product = Products(name=f'Soda {unique_id}', supplier_id=supplier.user_id, unit_price=Decimal('5.00'), inventory_quantity=10, category='beverages', size='small')
        db.session.add(product)
        db.session.flush()
        
        cart_item = CartItems(customer_id=customer_user.id, product_id=product.id, quantity=1)
        db.session.add(cart_item)
        db.session.commit()

        return {
            'customer_user_id': customer_user.id,
            'customer_showing_id': customer_showing.id,
            'payment_method_id': payment_method.id,
            'product_id': product.id,
            'supplier_id': supplier.user_id,
            'initial_price': Decimal('5.00')
        }


class TestDriverService:
    
    _create_test_driver = staticmethod(_create_test_driver) 
    
    # --- Test Driver Validation Methods ---
    
    @pytest.mark.parametrize("plate, expected_error", [
        ("ABC12345678901234567", "License plate must be a string"),
        ("", "License plate must be a string"),
        (12345, "License plate must be a string")
    ])
    def test_validate_license_plate_invalid(self, driver_service, plate, expected_error):
        with pytest.raises(ValueError, match=expected_error):
            driver_service.validate_license_plate(plate)

    def test_validate_license_plate_valid(self, driver_service):
        assert driver_service.validate_license_plate("XYZ789") == "XYZ789"
    
    @pytest.mark.parametrize("v_type, expected_error", [
        ("truck", "Vehicle type must be a string"),
        (123, "Vehicle type must be a string")
    ])
    def test_validate_vehicle_type_invalid(self, driver_service, v_type, expected_error):
        with pytest.raises(ValueError, match=expected_error):
            driver_service.validate_vehicle_type(v_type)

    def test_validate_vehicle_type_valid(self, driver_service):
        assert driver_service.validate_vehicle_type("bike") == "bike"
        assert driver_service.validate_vehicle_type("other") == "other"

    @pytest.mark.parametrize("color, expected_error", [
        ("SuperLongAndInvalidColorName", "Vehicle color must be a string"),
        ("", "Vehicle color must be a string"),
        (100, "Vehicle color must be a string")
    ])
    def test_validate_vehicle_color_invalid(self, driver_service, color, expected_error):
        with pytest.raises(ValueError, match=expected_error):
            driver_service.validate_vehicle_color(color)

    def test_validate_vehicle_color_valid(self, driver_service):
        assert driver_service.validate_vehicle_color("Red") == "Red"

    @pytest.mark.parametrize("status, expected_error", [
        ("on_break", "Duty status must be a string"),
        (1, "Duty status must be a string")
    ])
    def test_validate_duty_status_invalid(self, driver_service, status, expected_error):
        with pytest.raises(ValueError, match=expected_error):
            driver_service.validate_duty_status(status)

    def test_validate_duty_status_valid(self, driver_service):
        assert driver_service.validate_duty_status(STATUS_AVAILABLE) == STATUS_AVAILABLE

    @pytest.mark.parametrize("rating, expected_error", [
        (Decimal('5.1'), "Rating must be a valid decimal number"),
        (Decimal('-0.1'), "Rating must be a valid decimal number"),
        ("abc", "Rating must be a valid decimal number")
    ])
    def test_validate_rating_invalid(self, driver_service, rating, expected_error):
        with pytest.raises(ValueError, match=expected_error):
            driver_service.validate_rating(rating)

    def test_validate_rating_valid(self, driver_service):
        assert driver_service.validate_rating(4.5) == Decimal('4.5')

    @pytest.mark.parametrize("deliveries, expected_error", [
        (-1, "Total deliveries must be an integer"),
        ("a", "Total deliveries must be an integer")
    ])
    def test_validate_total_deliveries_invalid(self, driver_service, deliveries, expected_error):
        with pytest.raises(ValueError, match=expected_error):
            driver_service.validate_total_deliveries(deliveries)

    def test_validate_total_deliveries_valid(self, driver_service):
        assert driver_service.validate_total_deliveries(10) == 10
        
    # --- Test Driver CRUD ---
    
    def test_create_driver_success(self, app, driver_service):
        unique_id = uuid.uuid4().hex[:8]
        with app.app_context():
            driver = driver_service.create_driver(
                name='New Driver',
                email=f'new_{unique_id}@test.com',
                phone=f'555000{unique_id[:4]}',
                birthday=datetime(2000, 1, 1),
                password='testpass',
                role='driver',
                license_plate='TEST111',
                vehicle_type='car',
                vehicle_color='Black',
                duty_status=STATUS_AVAILABLE,
                rating=Decimal('4.0'),
                total_deliveries=5
            )
            assert driver.user_id is not None
            assert driver.license_plate == 'TEST111'
            assert driver.duty_status == STATUS_AVAILABLE
            
    def test_create_driver_invalid_role(self, driver_service):
        with pytest.raises(ValueError, match="User role must be 'driver'"):
            driver_service.create_driver(
                name='New Driver',
                email='wrong@test.com',
                phone='5550000000',
                birthday=datetime(2000, 1, 1),
                password='testpass',
                role='customer', # Invalid role
                license_plate='TEST111',
                vehicle_type='car',
                vehicle_color='Black',
                duty_status=STATUS_AVAILABLE,
                rating=Decimal('4.0'),
                total_deliveries=5
            )

    def test_update_driver_details_success(self, app, driver_service):
        user_id, driver = self._create_test_driver(app)
        with app.app_context():
            updated_driver = driver_service.update_driver_details(
                user_id=user_id,
                license_plate='NEWPLATE',
                vehicle_type='bike',
                vehicle_color='Yellow'
            )
            assert updated_driver.vehicle_type == 'bike'
            assert updated_driver.license_plate == 'NEWPLATE'
            assert updated_driver.vehicle_color == 'Yellow'
    
    def test_update_driver_details_not_found(self, app, driver_service):
        with app.app_context():
            with pytest.raises(ValueError, match="Driver 999999 not found"):
                driver_service.update_driver_details(
                    user_id=999999,
                    license_plate='NEWPLATE',
                    vehicle_type='bike',
                    vehicle_color='Yellow'
                )

    def test_update_driver_status_success(self, app, driver_service):
        user_id, driver = self._create_test_driver(app, duty_status=STATUS_UNAVAILABLE)
        with app.app_context():
            updated_driver = driver_service.update_driver_status(user_id=user_id, new_status=STATUS_ON_DELIVERY)
            assert updated_driver.duty_status == STATUS_ON_DELIVERY

    def test_delete_driver_success(self, app, driver_service):
        user_id, driver = self._create_test_driver(app)
        with app.app_context():
            assert driver_service.delete_driver(user_id) is True
            assert Users.query.filter_by(id=user_id).first() is None
    
    # --- Test Availability & Assignment Logic ---

    def test_get_available_drivers(self, app, driver_service):
        # Create 1 available driver
        d1_id, _ = self._create_test_driver(app, duty_status=STATUS_AVAILABLE, rating=Decimal('4.5'))
        # Create 1 unavailable driver
        self._create_test_driver(app, duty_status=STATUS_UNAVAILABLE, rating=Decimal('5.0'))
        
        with app.app_context():
            available_drivers = driver_service.get_available_drivers()
            assert len(available_drivers) == 1
            assert available_drivers[0].user_id == d1_id

    def test_get_best_available_driver(self, app, driver_service):
        # Create lower rated available driver
        self._create_test_driver(app, duty_status=STATUS_AVAILABLE, rating=Decimal('4.0'), deliveries=10, vehicle_color='Green')
        # Create best available driver (highest rating)
        d2_id, _ = self._create_test_driver(app, duty_status=STATUS_AVAILABLE, rating=Decimal('4.8'), deliveries=5)
        # Create unavailable driver
        self._create_test_driver(app, duty_status=STATUS_UNAVAILABLE, rating=Decimal('5.0'))
        
        with app.app_context():
            best_driver = driver_service.get_best_available_driver()
            assert best_driver.user_id == d2_id
            
    def test_try_assign_driver_success(self, app, driver_service, setup_prerequisites):
        driver_id, _ = self._create_test_driver(app, duty_status=STATUS_AVAILABLE)
        delivery_id = _create_delivery(app, driver_id=None, showing_id=setup_prerequisites['customer_showing_id'], payment_id=setup_prerequisites['payment_method_id'], status='pending')
        
        with app.app_context():
            delivery = Deliveries.query.filter_by(id=delivery_id).first()
            assert driver_service.try_assign_driver(delivery) is True
            
            # Verify updates
            updated_driver = Drivers.query.filter_by(user_id=driver_id).first()
            assert delivery.driver_id == driver_id
            assert delivery.delivery_status == 'accepted'
            assert updated_driver.duty_status == STATUS_ON_DELIVERY

    def test_try_assign_driver_no_available_driver(self, app, driver_service, setup_prerequisites):
        # Create a driver but set status to unavailable
        self._create_test_driver(app, duty_status=STATUS_UNAVAILABLE)
        delivery_id = _create_delivery(app, driver_id=None, showing_id=setup_prerequisites['customer_showing_id'], payment_id=setup_prerequisites['payment_method_id'], status='pending')
        
        with app.app_context():
            delivery = Deliveries.query.filter_by(id=delivery_id).first()
            assert driver_service.try_assign_driver(delivery) is False
            assert delivery.driver_id is None
    
    def test_try_assign_driver_delivery_not_found(self, driver_service):
        with pytest.raises(ValueError, match="Delievry not found"):
            driver_service.try_assign_driver(None)

    # --- Test Delivery Completion Logic ---

    def test_complete_delivery_success(self, app, driver_service, setup_prerequisites):
        driver_id, driver = self._create_test_driver(app, duty_status=STATUS_ON_DELIVERY, deliveries=5)
        delivery_id = _create_delivery(app, driver_id=driver_id, showing_id=setup_prerequisites['customer_showing_id'], payment_id=setup_prerequisites['payment_method_id'], status='accepted')
        
        with app.app_context():
            completed_delivery = driver_service.complete_delivery(delivery_id)
            
            # Verify delivery status change
            assert completed_delivery.delivery_status == 'delivered'
            
            # Verify driver updates
            updated_driver = Drivers.query.filter_by(user_id=driver_id).first()
            assert updated_driver.duty_status == STATUS_AVAILABLE
            assert updated_driver.total_deliveries == 6 # 5 + 1

    def test_complete_delivery_not_found(self, app, driver_service):
        with app.app_context():
            with pytest.raises(ValueError, match="Delivery 999999 not found"):
                driver_service.complete_delivery(999999)
            
    def test_complete_delivery_wrong_status(self, app, driver_service, setup_prerequisites):
        driver_id, _ = self._create_test_driver(app, duty_status=STATUS_ON_DELIVERY, deliveries=5)
        delivery_id = _create_delivery(app, driver_id=driver_id, showing_id=setup_prerequisites['customer_showing_id'], payment_id=setup_prerequisites['payment_method_id'], status='pending') # Wrong status
        
        with app.app_context():
            with pytest.raises(ValueError, match="Delivery must be accepted to be completed"):
                driver_service.complete_delivery(delivery_id)

    # --- Test Rating Logic ---
    
    def test_rate_driver_success_new_average(self, app, driver_service, setup_prerequisites):
        driver_id, driver = self._create_test_driver(app, rating=Decimal('4.00'), deliveries=10)
        delivery_id = _create_delivery(app, driver_id=driver_id, showing_id=setup_prerequisites['customer_showing_id'], payment_id=setup_prerequisites['payment_method_id'], status='fulfilled', is_rated=False)

        with app.app_context():
            rated_driver, delivery = driver_service.rate_driver(delivery_id, 5.0)
            
            assert round(rated_driver.rating, 2) == Decimal('4.09')
            assert delivery.is_rated is True

    def test_rate_driver_success_first_rating(self, app, driver_service, setup_prerequisites):
        driver_id, driver = self._create_test_driver(app, rating=Decimal('5.00'), deliveries=0)
        delivery_id = _create_delivery(app, driver_id=driver_id, showing_id=setup_prerequisites['customer_showing_id'], payment_id=setup_prerequisites['payment_method_id'], status='fulfilled', is_rated=False)

        with app.app_context():
            rated_driver, delivery = driver_service.rate_driver(delivery_id, 3.5)
            
            assert rated_driver.rating == Decimal('3.5')
            assert delivery.is_rated is True

    def test_rate_driver_already_rated(self, app, driver_service, setup_prerequisites):
        driver_id, driver = self._create_test_driver(app, rating=Decimal('4.00'), deliveries=10)
        delivery_id = _create_delivery(app, driver_id=driver_id, showing_id=setup_prerequisites['customer_showing_id'], payment_id=setup_prerequisites['payment_method_id'], status='fulfilled', is_rated=True)

        with app.app_context():
            with pytest.raises(ValueError, match="Delivery .* has already been rated"):
                driver_service.rate_driver(delivery_id, 5.0)
    
    def test_rate_driver_wrong_status(self, app, driver_service, setup_prerequisites):
        driver_id, driver = self._create_test_driver(app, rating=Decimal('4.00'), deliveries=10)
        delivery_id = _create_delivery(app, driver_id=driver_id, showing_id=setup_prerequisites['customer_showing_id'], payment_id=setup_prerequisites['payment_method_id'], status='delivered', is_rated=False) # Wrong status
        
        with app.app_context():
            with pytest.raises(ValueError, match="Can only rate fulfilled deliveries"):
                driver_service.rate_driver(delivery_id, 5.0)

    # --- Test Retrieval Methods ---
    
    def test_show_completed_deliveries_found(self, app, driver_service, setup_prerequisites):
        driver_id, _ = self._create_test_driver(app)
        d1_id = _create_delivery(app, driver_id, setup_prerequisites['customer_showing_id'], setup_prerequisites['payment_method_id'], 'fulfilled')
        d2_id = _create_delivery(app, driver_id, setup_prerequisites['customer_showing_id'], setup_prerequisites['payment_method_id'], 'fulfilled')
        _create_delivery(app, driver_id, setup_prerequisites['customer_showing_id'], setup_prerequisites['payment_method_id'], 'pending') # Exclude incomplete
        
        with app.app_context():
            deliveries = driver_service.show_completed_deliveries(driver_id)
            assert len(deliveries) == 2
            assert all(d.delivery_status == 'fulfilled' for d in deliveries)
            assert {d1_id, d2_id} == {d.id for d in deliveries}

    def test_show_completed_deliveries_not_found(self, app, driver_service, setup_prerequisites):
        driver_id, _ = self._create_test_driver(app)
        _create_delivery(app, driver_id, setup_prerequisites['customer_showing_id'], setup_prerequisites['payment_method_id'], 'accepted') # Active, not completed
        
        with app.app_context():
            with pytest.raises(ValueError, match=f"No previous deliveries found for driver {driver_id}"):
                driver_service.show_completed_deliveries(driver_id)

    def test_get_active_delivery_found(self, app, driver_service, setup_prerequisites):
        driver_id, _ = self._create_test_driver(app)
        _create_delivery(app, driver_id, setup_prerequisites['customer_showing_id'], setup_prerequisites['payment_method_id'], 'fulfilled') # Completed, exclude
        active_id = _create_delivery(app, driver_id, setup_prerequisites['customer_showing_id'], setup_prerequisites['payment_method_id'], 'in_transit') # Active
        
        with app.app_context():
            delivery = driver_service.get_active_delivery(driver_id)
            assert delivery.id == active_id
            assert delivery.delivery_status == 'in_transit'

    def test_get_active_delivery_not_found(self, app, driver_service, setup_prerequisites):
        driver_id, _ = self._create_test_driver(app)
        _create_delivery(app, driver_id, setup_prerequisites['customer_showing_id'], setup_prerequisites['payment_method_id'], 'fulfilled') # Completed
        
        with app.app_context():
            with pytest.raises(ValueError, match=f"No active delivery found for driver {driver_id}"):
                driver_service.get_active_delivery(driver_id)
