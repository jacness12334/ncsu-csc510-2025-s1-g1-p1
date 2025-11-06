# testing_utils.py

import unittest
from contextlib import contextmanager
from datetime import date, datetime
from sqlalchemy.exc import IntegrityError, OperationalError
# Import the core components from your project files
from app import get_app, db 
import models # Assumes models.py imports 'db' from app
import database
import load_database

class BaseIntegrationTest(unittest.TestCase):
    """
    Base test class that connects to the real 'movie_munchers_test' database,
    manages the Flask application context, and ensures transaction isolation.
    """
    
    @classmethod
    def setUpClass(cls):
        """Setup the Flask application and create all tables once."""
        cls.app = get_app('testing')
        # Push context to make models.py accessible via query methods (e.g., .query)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        
        # Create all tables on the 'movie_munchers_test' database
        # This uses the connection configured by get_app('testing')
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Drop all tables after all tests in the class are finished."""
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        """Starts a transaction for isolation before each test."""
        # Bind the session to a connection and begin a transaction
        self.connection = db.engine.connect()
        self.transaction = self.connection.begin()
        # Use the session bound to the transaction
        db.session.close() # Close session from previous test
        db.session = db.create_scoped_session({'bind': self.connection, 'autocommit': False, 'autoflush': True})
        self.session = db.session
        
        # Setup base objects for Foreign Key constraints
        self.db = self._setup_base_references()

    def tearDown(self):
        """Rollback the transaction to discard changes and clean up after each test."""
        # Rollback the transaction to revert all changes made by the test
        self.session.rollback()
        self.connection.close()

    def commit_and_flush(self):
        """Flushes session changes to the database (within the active transaction)."""
        self.session.flush()

    def _setup_base_references(self):
        """
        Inserts minimal, necessary data to satisfy Foreign Key constraints 
        for all models tested in models_test.py.
        """
        
        from models import (
            Users, Theatres, Auditoriums, Seats, Staff, Customers, 
            Movies, MovieShowings, PaymentMethods, Drivers, Suppliers, 
            Products, CustomerShowings, Deliveries, CartItems
        ) 
        
        # --- USERS ---
        user1_staff = Users(user_id=10, name='Staff User', email='staff@test.com', phone='555-1111', birthday=date.today(), password_hash='hash', role='staff')
        user2_customer = Users(user_id=11, name='Test Customer', email='customer@test.com', phone='555-1234', birthday=date.today(), password_hash='hash', role='customer')
        user3_driver = Users(user_id=12, name='Test Driver', email='driver@test.com', phone='555-2222', birthday=date.today(), password_hash='hash', role='driver')
        user4_supplier = Users(user_id=13, name='Test Supplier', email='supplier@test.com', phone='555-3333', birthday=date.today(), password_hash='hash', role='supplier')
        self.session.add_all([user1_staff, user2_customer, user3_driver, user4_supplier])
        
        # --- THEATRE & AUDITORIUMS ---
        theatre1 = Theatres(id=1, name='Main Theatre', address='123 Main St', phone='555-0000', is_open=True)
        auditorium1 = Auditoriums(id=1, theatre_id=theatre1.id, number=1, capacity=200)
        auditorium2 = Auditoriums(id=2, theatre_id=theatre1.id, number=2, capacity=100) # For test 28
        self.session.add_all([theatre1, auditorium1, auditorium2])

        # --- SEATS ---
        seat1 = Seats(id=1, auditorium_id=auditorium1.id, aisle='A', number=1)
        seat2 = Seats(id=2, auditorium_id=auditorium1.id, aisle='A', number=2) # For test 32
        seat3 = Seats(id=3, auditorium_id=auditorium1.id, aisle='A', number=3) # For test 51
        self.session.add_all([seat1, seat2, seat3])
        
        # --- STAFF / CUSTOMERS / DRIVERS / SUPPLIERS (FK on Users) ---
        staff1 = Staff(user_id=user1_staff.id, theatre_id=theatre1.id, role='manager', is_available=True)
        customer1 = Customers(user_id=user2_customer.id, default_theatre_id=theatre1.id)
        driver1 = Drivers(user_id=user3_driver.id, license_plate='TEST1234', vehicle_type='car', vehicle_color='black', rating='4.50')
        supplier1 = Suppliers(user_id=user4_supplier.id, company_name='Concessions Co', company_address='456 Supply Ln', contact_phone='555-4444')
        self.session.add_all([staff1, customer1, driver1, supplier1])

        # --- MOVIES & SHOWINGS ---
        movie1 = Movies(id=1, title='Test Movie 1', genre='Drama', length_mins=120, release_year=2024, rating='4.25')
        movie2 = Movies(id=2, title='Test Movie 2', genre='Comedy', length_mins=90, release_year=2023, rating='3.90')
        showing1_time = datetime.now()
        showing2_time = datetime.now().replace(hour=showing1_time.hour + 2, minute=showing1_time.minute, second=0, microsecond=0)
        showing1 = MovieShowings(id=1, movie_id=movie1.id, auditorium_id=auditorium1.id, start_time=showing1_time)
        showing2 = MovieShowings(id=2, movie_id=movie2.id, auditorium_id=auditorium1.id, start_time=showing2_time)
        self.session.add_all([movie1, movie2, showing1, showing2])
        
        # --- PAYMENT METHODS ---
        payment_method1 = PaymentMethods(id=1, customer_id=customer1.user_id, card_number='1111222233334444', expiration_month=1, expiration_year=2030, billing_address='Cust Addr', balance='50.00', is_default=True)
        self.session.add(payment_method1)
        
        # --- PRODUCTS ---
        product1 = Products(id=1, supplier_id=supplier1.user_id, name='Popcorn', unit_price='5.50', inventory_quantity=10, is_available=True)
        product2 = Products(id=2, supplier_id=supplier1.user_id, name='Water', unit_price='2.00', inventory_quantity=20, is_available=True)
        self.session.add_all([product1, product2])

        # --- CUSTOMER SHOWINGS (Seat Booking) ---
        customer_showing1 = CustomerShowings(id=1, customer_id=customer1.user_id, movie_showing_id=showing1.id, seat_id=seat1.id)
        self.session.add(customer_showing1)

        # --- DELIVERIES ---
        delivery1 = Deliveries(id=1, driver_id=driver1.user_id, customer_showing_id=customer_showing1.id, payment_method_id=payment_method1.id, staff_id=staff1.user_id, total_price='10.00')
        self.session.add(delivery1)

        # --- CART ITEMS ---
        cart_item1 = CartItems(id=1, customer_id=customer1.user_id, product_id=product1.id, quantity=2)
        self.session.add(cart_item1)

        # --- DELIVERY ITEMS ---
        delivery_item1 = DeliveryItems(id=1, cart_item_id=cart_item1.id, delivery_id=delivery1.id)
        self.session.add(delivery_item1)
        
        self.commit_and_flush()

        class BaseRefs:
            # Users/FKs
            user1 = user1_staff
            user2 = user2_customer
            driver1 = driver1
            staff1 = staff1
            customer1 = customer1
            supplier1 = supplier1
            payment_method1 = payment_method1
            
            # Theatre/Auditoriums/Seats
            theatre1 = theatre1
            auditorium1 = auditorium1
            auditorium2 = auditorium2
            seat1 = seat1
            seat2 = seat2
            seat3 = seat3
            
            # Movies/Showings
            movie1 = movie1
            movie2 = movie2
            showing1 = showing1
            showing2 = showing2
            
            # Products
            product1 = product1
            product2 = product2
            
            # Delivery Chain
            customer_showing1 = customer_showing1
            delivery1 = delivery1
            cart_item1 = cart_item1
            delivery_item1 = delivery_item1
            
        return BaseRefs()

    # Assertion Helpers (using context managers for clean test code)
    @contextmanager
    def assert_raises_integrity_error(self, message=None):
        """Checks if the following code block raises a SQLAlchemy IntegrityError."""
        with self.assertRaises(IntegrityError, msg=message):
            try:
                yield
                self.session.flush() # Try to flush to trigger constraint errors
            except:
                self.session.rollback() # Rollback the session if an error occurs
                raise
             
    @contextmanager
    def assert_raises_operational_error(self, message=None):
        """Checks if the following code block raises a SQLAlchemy OperationalError (e.g., Check constraint)."""
        with self.assertRaises(OperationalError, msg=message):
            try:
                yield
                self.session.flush() # Try to flush to trigger constraint errors
            except:
                self.session.rollback() # Rollback the session if an error occurs
                raise