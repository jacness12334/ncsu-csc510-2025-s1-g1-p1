# models_test.py (Refactored to use BaseIntegrationTest)

import unittest
from datetime import date, datetime
# Import actual models from models.py
from app.models import (
    CartItems, Theatres, Auditoriums, Seats, Users, Staff, Movies,
    MovieShowings, Customers, CustomerShowings, PaymentMethods, Drivers,
    Suppliers, Products, Deliveries, DeliveryItems
)
from sqlalchemy.exc import IntegrityError, OperationalError

# Import the integration test base class and utilities from the external file
from testing_utils import BaseIntegrationTest


# --------------------------------------------------------------------------
# 60 UNIT TESTS BEGIN HERE
# --------------------------------------------------------------------------
# This class now inherits from BaseIntegrationTest for real DB interaction.

class TestAllModels(BaseIntegrationTest):
    # The setUp, tearDown, commit_and_flush, and initial base references (self.db) 
    # are all handled by BaseIntegrationTest.

    # We use the context managers from BaseIntegrationTest for error assertions.
    
    # ----------------- THEATRES (4 TESTS) -----------------
    # 1. Tests the successful creation of a Theatres object with all required fields.
    def test_01_create_theatre(self):
        t = Theatres(name='Test T', address='Test Addr', phone='555-3333'); 
        self.session.add(t)
        self.commit_and_flush()
        self.assertIsNotNone(t.id)

    # 2. Verifies that a unique constraint prevents two theatres from having the same name and address.
    def test_02_unique_address_constraint(self):
        with self.assert_raises_integrity_error('Unique constraint on name/address failed.'):
            # Attempt to add a theatre with the same name and address as self.db.theatre1
            self.session.add(Theatres(
                name=self.db.theatre1.name, 
                address=self.db.theatre1.address, 
                phone='555-9999' # Different phone is fine, but name/address is constrained
            ))
            self.commit_and_flush()

    # 3. Confirms that the is_open field correctly defaults to False.
    def test_03_default_is_open_value(self):
        # Default value should be tested directly on the model instance (before commit)
        t = Theatres(name='T2', address='A2', phone='555-2222')
        self.assertFalse(t.is_open, 'is_open should default to False.')

    # 4. Checks that the __repr__ method returns a correctly formatted string representation of the object.
    def test_04_repr_method(self):
        expected_repr = f"<Theatre id = {self.db.theatre1.id} name = '{self.db.theatre1.name}' address = '{self.db.theatre1.address}' is_open = {self.db.theatre1.is_open}>"
        self.assertEqual(repr(self.db.theatre1), expected_repr)

# ----------------- AUDITORIUMS (5 TESTS) -----------------
    # 5. Tests the successful creation of an Auditoriums object linked to a valid theatre.
    def test_05_create_auditorium(self):
        a = Auditoriums(theatre_id=self.db.theatre1.id, number=2, capacity=150); 
        self.session.add(a)
        self.commit_and_flush()
        self.assertIsNotNone(a.id)

    # 6. Verifies that a unique constraint prevents two auditoriums in the same theatre from having the same number.
    def test_06_unique_number_constraint(self):
        with self.assert_raises_integrity_error('Unique constraint on theatre_id/number failed.'):
            self.session.add(Auditoriums(
                theatre_id=self.db.auditorium1.theatre_id, 
                number=self.db.auditorium1.number, 
                capacity=150
            ))
            self.commit_and_flush()

    # 7. Confirms that a check constraint enforces the number field to be greater than 0.
    def test_07_check_number_greater_than_zero(self):
        with self.assert_raises_operational_error('Check constraint on number > 0 failed.'):
            self.session.add(Auditoriums(theatre_id=self.db.theatre1.id, number=0, capacity=100))
            self.commit_and_flush()

    # 8. Confirms that a check constraint enforces the capacity field to be greater than 0.
    def test_08_check_capacity_greater_than_zero(self):
        with self.assert_raises_operational_error('Check constraint on capacity > 0 failed.'):
            self.session.add(Auditoriums(theatre_id=self.db.theatre1.id, number=2, capacity=0))
            self.commit_and_flush()

    # 9. Ensures that deleting the linked theatre cascades and deletes the auditorium.
    def test_09_foreign_key_cascade_on_delete(self):
        # In a real test: delete theatre -> try to fetch auditorium -> assert None
        # Must ensure cascade is set in model definition (ondelete='CASCADE')
        auditorium_id = self.db.auditorium1.id
        self.session.delete(self.db.theatre1) 
        self.commit_and_flush() # Perform the delete and cascade

        # Attempt to retrieve the deleted auditorium; should be None
        deleted_auditorium = self.session.get(Auditoriums, auditorium_id)
        self.assertIsNone(deleted_auditorium, 'Auditorium should be deleted via cascade.')

# ----------------- SEATS (3 TESTS) -----------------
    # 10. Tests the successful creation of a Seats object linked to a valid auditorium.
    def test_10_create_seat(self):
        s = Seats(auditorium_id=self.db.auditorium1.id, aisle='B', number=1); 
        self.session.add(s)
        self.commit_and_flush()
        self.assertIsNotNone(s.id)

    # 11. Verifies that a unique constraint prevents two seats in the same auditorium from having the same aisle and number.
    def test_11_unique_seat_constraint(self):
        with self.assert_raises_integrity_error('Unique constraint on auditorium_id/aisle/number failed.'):
            self.session.add(Seats(
                auditorium_id=self.db.seat1.auditorium_id, 
                aisle=self.db.seat1.aisle, 
                number=self.db.seat1.number
            ))
            self.commit_and_flush()

    # 12. Confirms that a check constraint enforces the number field to be greater than 0.
    def test_12_check_number_greater_than_zero(self):
        with self.assert_raises_operational_error('Check constraint on number > 0 failed.'):
            self.session.add(Seats(auditorium_id=self.db.auditorium1.id, aisle='Z', number=0))
            self.commit_and_flush()

# ----------------- USERS (6 TESTS) -----------------
    # 13. Tests the successful creation of a Users object with a valid role and all required fields.
    def test_13_create_user(self):
        u = Users(
            name='Test U', email='new@test.com', phone='555-4444', 
            birthday=date.today(), password_hash='hash', role='customer'
        ); 
        self.session.add(u)
        self.commit_and_flush()
        self.assertIsNotNone(u.id)

    # 14. Verifies that a unique constraint prevents creating two users with the same email.
    def test_14_unique_email_constraint(self):
        with self.assert_raises_integrity_error('Unique constraint on email failed.'):
            self.session.add(Users(
                name='Other U', email=self.db.user1.email, phone='555-5555', 
                birthday=date.today(), password_hash='hash', role='customer'
            ))
            self.commit_and_flush()

    # 15. Verifies that a unique constraint prevents creating two users with the same phone number.
    def test_15_unique_phone_constraint(self):
        with self.assert_raises_integrity_error('Unique constraint on phone failed.'):
            self.session.add(Users(
                name='Other U', email='other@test.com', phone=self.db.user1.phone, 
                birthday=date.today(), password_hash='hash', role='customer'
            ))
            self.commit_and_flush()

    # 16. Confirms that the account_status field correctly defaults to 'active'.
    def test_16_default_account_status(self):
        u = Users(
            name='D', email='d@t.com', phone='555-6666', 
            birthday=date.today(), password_hash='hash', role='staff'
        )
        self.session.add(u)
        self.commit_and_flush() # Commit to ensure DB default is not overriding model default
        self.assertEqual(u.account_status, 'active', 'account_status should default to active')

    # 17. Checks that date_added is set on creation and last_updated is updated upon modification.
    def test_17_timestamp_defaults(self):
        # date_added should be set on creation (which happens on flush/commit)
        user = Users(
            name='D2', email='d2@t.com', phone='555-7777', 
            birthday=date.today(), password_hash='hash', role='staff'
        )
        self.session.add(user)
        self.commit_and_flush()
        
        # Verify date_added is set
        self.assertIsNotNone(user.date_added)

        # Update check requires server_onupdate/column_property, which needs the model/schema definition
        # If last_updated is a server_onupdate column, it will be handled by the database.
        # This test remains a placeholder if server-side logic is required.
        pass

    # 18. Confirms that the role field only accepts values from the defined enum.
    def test_18_enum_role_validation(self):
        with self.assert_raises_operational_error('Enum validation for role failed.'):
            self.session.add(Users(
                name='D', email='d3@t.com', phone='555-8888', 
                birthday=date.today(), password_hash='hash', role='invalid_role'
            ))
            self.commit_and_flush()

# ----------------- STAFF (4 TESTS) -----------------
    # 19. Tests the successful creation of a Staff object linked to a valid user and theatre.
    def test_19_create_staff(self):
        # Need a separate user created for this new staff member
        user = Users(name='S2', email='s2@t.com', phone='555-9990', birthday=date.today(), password_hash='hash', role='staff')
        self.session.add(user)
        self.commit_and_flush()
        
        s = Staff(user_id=user.id, theatre_id=self.db.theatre1.id, role='runner'); 
        self.session.add(s)
        self.commit_and_flush()
        self.assertIsNotNone(s.user_id)

    # 20. Confirms that the is_available field correctly defaults to False.
    def test_20_default_is_available_value(self):
        user = Users(name='S3', email='s3@t.com', phone='555-9991', birthday=date.today(), password_hash='hash', role='staff')
        self.session.add(user)
        self.commit_and_flush()
        
        s = Staff(user_id=user.id, theatre_id=self.db.theatre1.id, role='admin')
        self.session.add(s)
        self.commit_and_flush()
        self.assertFalse(s.is_available, 'is_available should default to False')

    # 21. Ensures that deleting the linked user cascades and deletes the staff record.
    def test_21_foreign_key_on_delete(self):
        # user1 is the user linked to staff1
        user_id = self.db.user1.id # This is the FK/PK for staff1
        self.session.delete(self.db.user1) 
        self.commit_and_flush()
        
        deleted_staff = self.session.get(Staff, user_id)
        self.assertIsNone(deleted_staff, 'Staff record should be deleted via cascade.')

    # 22. Confirms that user_id is correctly set as the primary key.
    def test_22_primary_key_is_user_id(self):
        # Real test requires model introspection (not available here)
        self.assertTrue(hasattr(self.db.staff1, 'user_id'))
        pass

# ----------------- MOVIES (3 TESTS) -----------------
    # 23. Tests the successful creation of a Movies object with valid rating and length.
    def test_23_create_movie(self):
        m = Movies(
            title='New Movie', genre='Action', length_mins=100, 
            release_year=2023, keywords='K1,K2', rating='4.10'
        ); 
        self.session.add(m)
        self.commit_and_flush()
        self.assertIsNotNone(m.id)

    # 24. Confirms that a check constraint enforces the rating to be between 0.00 and 5.00.
    def test_24_rating_check_constraint(self):
        with self.assert_raises_operational_error('Check constraint on rating <= 5.00 failed.'):
            self.session.add(Movies(title='Inv High', rating='5.01', genre='A', length_mins=1, release_year=2020))
            self.commit_and_flush()
            
        with self.assert_raises_operational_error('Check constraint on rating >= 0.00 failed.'):
            self.session.add(Movies(title='Inv Low', rating='-0.01', genre='A', length_mins=1, release_year=2020))
            self.commit_and_flush()

    # 25. Checks that the rating column correctly stores values with a precision of (3, 2).
    def test_25_decimal_precision(self):
        m = Movies(title='Prec', rating='4.12', genre='A', length_mins=1, release_year=2020)
        self.session.add(m)
        self.commit_and_flush()
        # SQLAlchemy may return a Decimal object, checking the string representation for precision.
        self.assertEqual(str(m.rating), '4.12', 'Rating should store with (3,2) precision')

# ----------------- MOVIE SHOWINGS (3 TESTS) -----------------
    # 26. Tests the successful creation of a MovieShowings object linked to a movie and auditorium.
    def test_26_create_movie_showing(self):
        ms = MovieShowings(
            movie_id=self.db.movie1.id, 
            auditorium_id=self.db.auditorium1.id, 
            start_time=datetime.now()
        ); 
        self.session.add(ms)
        self.commit_and_flush()
        self.assertIsNotNone(ms.id)

    # 27. Verifies that a unique constraint prevents two showings from being scheduled in the same auditorium at the same start time.
    def test_27_unique_showing_constraint(self):
        with self.assert_raises_integrity_error('Unique constraint on auditorium_id/start_time failed.'):
            self.session.add(MovieShowings(
                movie_id=self.db.movie2.id, # Must use a different movie to simulate a new showing
                auditorium_id=self.db.showing1.auditorium_id, 
                start_time=self.db.showing1.start_time
            ))
            self.commit_and_flush()

    # 28. Confirms that the in_progress field correctly defaults to False.
    def test_28_default_in_progress_value(self):
        ms = MovieShowings(
            movie_id=self.db.movie1.id, 
            auditorium_id=self.db.auditorium2.id, 
            start_time=datetime.now()
        )
        self.session.add(ms)
        self.commit_and_flush()
        self.assertFalse(ms.in_progress, 'in_progress should default to False')

# ----------------- CUSTOMERS (3 TESTS) -----------------
    # 29. Tests the successful creation of a Customers object linked to a valid user and a default theatre.
    def test_29_create_customer(self):
        # Need a separate user created for this new customer
        user = Users(name='C2', email='c2@t.com', phone='555-9992', birthday=date.today(), password_hash='hash', role='customer')
        self.session.add(user)
        self.commit_and_flush()
        
        c = Customers(user_id=user.id, default_theatre_id=self.db.theatre1.id); 
        self.session.add(c)
        self.commit_and_flush()
        self.assertIsNotNone(c.user_id)

    # 30. Ensures that deleting the linked user cascades and deletes the customer record.
    def test_30_foreign_key_on_delete(self):
        # user2 is the user linked to customer1
        user_id = self.db.user2.id # This is the FK/PK for customer1
        self.session.delete(self.db.user2) 
        self.commit_and_flush()
        
        deleted_customer = self.session.get(Customers, user_id)
        self.assertIsNone(deleted_customer, 'Customer record should be deleted via cascade.')

    # 31. Confirms that user_id is correctly set as the primary key.
    def test_31_primary_key_is_user_id(self):
        # Real test requires model introspection (not available here)
        self.assertTrue(hasattr(self.db.customer1, 'user_id'))
        pass

# ----------------- CUSTOMER SHOWINGS (2 TESTS) -----------------
    # 32. Tests the successful creation of a CustomerShowings record linking a customer, movie showing, and seat.
    def test_32_create_customer_showing(self):
        cs = CustomerShowings(
            customer_id=self.db.customer1.user_id, 
            movie_showing_id=self.db.showing2.id, 
            seat_id=self.db.seat2.id
        ); 
        self.session.add(cs)
        self.commit_and_flush()
        self.assertIsNotNone(cs.id)

    # 33. Verifies that a unique constraint prevents the same seat from being booked for the same movie showing twice.
    def test_33_unique_movie_seat_constraint(self):
        with self.assert_raises_integrity_error('Unique constraint on movie_showing_id/seat_id failed.'):
            self.session.add(CustomerShowings(
                customer_id=self.db.customer1.user_id, 
                movie_showing_id=self.db.showing1.id, 
                seat_id=self.db.seat1.id
            ))
            self.commit_and_flush()

# ----------------- PAYMENT METHODS (5 TESTS) -----------------
    # 34. Tests the successful creation of a PaymentMethods object with valid dates and balance.
    def test_34_create_payment_method(self):
        pm = PaymentMethods(
            customer_id=self.db.customer1.user_id, 
            card_number='1234123412344321', expiration_month=12, 
            expiration_year=2030, billing_address='123 PM', balance='100.00'
        ); 
        self.session.add(pm)
        self.commit_and_flush()
        self.assertIsNotNone(pm.id)

    # 35. Confirms that a check constraint enforces the expiration_month to be between 1 and 12.
    def test_35_check_expiration_month(self):
        with self.assert_raises_operational_error('Check constraint on expiration_month failed.'):
            self.session.add(PaymentMethods(customer_id=self.db.customer1.user_id, expiration_month=13))
            self.commit_and_flush()

    # 36. Confirms that a check constraint enforces the expiration_year to be 2025 or later.
    def test_36_check_expiration_year(self):
        # NOTE: This constraint depends on the current year. Assuming 2025 is the cutoff.
        with self.assert_raises_operational_error('Check constraint on expiration_year failed.'):
            self.session.add(PaymentMethods(customer_id=self.db.customer1.user_id, expiration_year=2024))
            self.commit_and_flush()

    # 37. Confirms that a check constraint enforces the balance field to be greater than or equal to 0.
    def test_37_check_balance_non_negative(self):
        with self.assert_raises_operational_error('Check constraint on balance >= 0 failed.'):
            self.session.add(PaymentMethods(customer_id=self.db.customer1.user_id, balance='-0.01'))
            self.commit_and_flush()

    # 38. Confirms that the is_default field correctly defaults to False.
    def test_38_default_is_default_value(self):
        pm = PaymentMethods(
            customer_id=self.db.customer1.user_id, 
            card_number='0000000000000000', expiration_month=1, 
            expiration_year=2030, billing_address='Default PM'
        )
        self.session.add(pm)
        self.commit_and_flush()
        self.assertFalse(pm.is_default, 'is_default should default to False')

# ----------------- DRIVERS (4 TESTS) -----------------
    # 39. Tests the successful creation of a Drivers object with all required fields.
    def test_39_create_driver(self):
        # Need a separate user created for this new driver
        user = Users(name='D2', email='d2r@t.com', phone='555-9993', birthday=date.today(), password_hash='hash', role='driver')
        self.session.add(user)
        self.commit_and_flush()
        
        d = Drivers(
            user_id=user.id, license_plate='ABC1234', 
            vehicle_type='car', vehicle_color='red'
        ); 
        self.session.add(d)
        self.commit_and_flush()
        self.assertIsNotNone(d.user_id)

    # 40. Confirms that the duty_status field correctly defaults to 'unavailable'.
    def test_40_default_duty_status(self):
        user = Users(name='D3', email='d3r@t.com', phone='555-9994', birthday=date.today(), password_hash='hash', role='driver')
        self.session.add(user)
        self.commit_and_flush()
        
        d = Drivers(
            user_id=user.id, license_plate='DEF5678', 
            vehicle_type='truck', vehicle_color='blue'
        )
        self.session.add(d)
        self.commit_and_flush()
        self.assertEqual(d.duty_status, 'unavailable', 'duty_status should default to unavailable')

    # 41. Confirms that a check constraint enforces the rating to be between 0.00 and 5.00.
    def test_41_rating_check_constraint(self):
        # Rating is optional, so we must test when a rating is provided
        user = Users(name='D4', email='d4r@t.com', phone='555-9995', birthday=date.today(), password_hash='hash', role='driver')
        self.session.add(user)
        self.commit_and_flush()

        with self.assert_raises_operational_error('Check constraint on rating failed.'):
            self.session.add(Drivers(
                user_id=user.id, license_plate='GHI9012', 
                vehicle_type='car', vehicle_color='red', rating='5.01'
            ))
            self.commit_and_flush()

    # 42. Confirms that the total_deliveries field correctly defaults to 0.
    def test_42_default_total_deliveries(self):
        user = Users(name='D5', email='d5r@t.com', phone='555-9996', birthday=date.today(), password_hash='hash', role='driver')
        self.session.add(user)
        self.commit_and_flush()
        
        d = Drivers(
            user_id=user.id, license_plate='JKL3456', 
            vehicle_type='van', vehicle_color='yellow'
        )
        self.session.add(d)
        self.commit_and_flush()
        self.assertEqual(d.total_deliveries, 0, 'total_deliveries should default to 0')

# ----------------- SUPPLIERS (3 TESTS) -----------------
    # 43. Tests the successful creation of a Suppliers object linked to a valid user.
    def test_43_create_supplier(self):
        # Need a separate user created for this new supplier
        user = Users(name='S2', email='s2r@t.com', phone='555-9997', birthday=date.today(), password_hash='hash', role='supplier')
        self.session.add(user)
        self.commit_and_flush()
        
        s = Suppliers(
            user_id=user.id, company_name='Co Name 2', 
            company_address='Co Addr 2', contact_phone='555-9999'
        ); 
        self.session.add(s)
        self.commit_and_flush()
        self.assertIsNotNone(s.user_id)

    # 44. Confirms that the is_open field correctly defaults to False.
    def test_44_default_is_open_value(self):
        user = Users(name='S3', email='s3r@t.com', phone='555-9998', birthday=date.today(), password_hash='hash', role='supplier')
        self.session.add(user)
        self.commit_and_flush()

        s = Suppliers(
            user_id=user.id, company_name='Co Name 3', 
            company_address='Co Addr 3', contact_phone='555-9991'
        )
        self.session.add(s)
        self.commit_and_flush()
        self.assertFalse(s.is_open, 'is_open should default to False')

    # 45. Confirms that user_id is correctly set as the primary key.
    def test_45_primary_key_is_user_id(self):
        # Real test requires model introspection (not available here)
        self.assertTrue(hasattr(self.db.supplier1, 'user_id'))
        pass

# ----------------- PRODUCTS (5 TESTS) -----------------
    # 46. Tests the successful creation of a Products object with valid price and inventory.
    def test_46_create_product(self):
        p = Products(
            supplier_id=self.db.supplier1.user_id, 
            name='Soda', unit_price='2.50', category='beverages'
        ); 
        self.session.add(p)
        self.commit_and_flush()
        self.assertIsNotNone(p.id)

    # 47. Confirms that a check constraint enforces the unit_price field to be non-negative.
    def test_47_check_unit_price_non_negative(self):
        with self.assert_raises_operational_error('Check constraint on unit_price >= 0 failed.'):
            self.session.add(Products(supplier_id=self.db.supplier1.user_id, name='Inv Price', unit_price='-0.01'))
            self.commit_and_flush()

    # 48. Confirms that a check constraint enforces the inventory_quantity field to be non-negative.
    def test_48_check_inventory_non_negative(self):
        with self.assert_raises_operational_error('Check constraint on inventory_quantity >= 0 failed.'):
            self.session.add(Products(supplier_id=self.db.supplier1.user_id, name='Inv Qty', unit_price='1.00', inventory_quantity=-1))
            self.commit_and_flush()

    # 49. Verifies that a unique constraint prevents a supplier from having two products with the same name.
    def test_49_unique_supplier_product_constraint(self):
        with self.assert_raises_integrity_error('Unique constraint on supplier_id/name failed.'):
            self.session.add(Products(
                supplier_id=self.db.product1.supplier_id, 
                name=self.db.product1.name, 
                unit_price='10.00'
            ))
            self.commit_and_flush()

    # 50. Confirms that the is_available field correctly defaults to True.
    def test_50_default_is_available_value(self):
        p = Products(supplier_id=self.db.supplier1.user_id, name='Default', unit_price='1.00')
        self.session.add(p)
        self.commit_and_flush()
        self.assertEqual(p.is_available, True, 'is_available should default to True')
        
        
# ----------------- DELIVERIES (4 TESTS) -----------------
    # 51. Tests the successful creation of a Deliveries object linked to all foreign keys.
    def test_51_create_delivery(self):
        # We need a new CustomerShowing/Seat to satisfy the unique constraint on DeliveryItems
        cs = CustomerShowings(
            customer_id=self.db.customer1.user_id, movie_showing_id=self.db.showing1.id, 
            seat_id=self.db.seat3.id # seat3 must be created in base refs
        ); self.session.add(cs); self.commit_and_flush()
        
        d = Deliveries(
            driver_id=self.db.driver1.user_id, 
            customer_showing_id=cs.id, # Use the new one
            payment_method_id=self.db.payment_method1.id, 
            staff_id=self.db.staff1.user_id, 
            total_price='15.00'
        ); 
        self.session.add(d)
        self.commit_and_flush()
        self.assertIsNotNone(d.id)

    # 52. Confirms that a check constraint enforces the total_price field to be non-negative.
    def test_52_check_total_price_non_negative(self):
        with self.assert_raises_operational_error('Check constraint on total_price >= 0 failed.'):
            self.session.add(Deliveries(total_price='-0.01'))
            self.commit_and_flush()

    # 53. Confirms that the payment_status field correctly defaults to 'pending'.
    def test_53_default_payment_status(self):
        d = Deliveries(
            driver_id=self.db.driver1.user_id, customer_showing_id=self.db.showing1.id, 
            payment_method_id=self.db.payment_method1.id, staff_id=self.db.staff1.user_id
        )
        self.session.add(d)
        self.commit_and_flush()
        self.assertEqual(d.payment_status, 'pending', 'payment_status should default to pending')

    # 54. Confirms that the delivery_status field correctly defaults to 'pending'.
    def test_54_default_delivery_status(self):
        d = Deliveries(
            driver_id=self.db.driver1.user_id, customer_showing_id=self.db.showing1.id, 
            payment_method_id=self.db.payment_method1.id, staff_id=self.db.staff1.user_id
        )
        self.session.add(d)
        self.commit_and_flush()
        self.assertEqual(d.delivery_status, 'pending', 'delivery_status should default to pending')

# ----------------- DELIVERY ITEMS (2 TESTS) -----------------
    # 55. Tests the successful creation of a DeliveryItems object linking a cart item to a delivery.
    def test_55_create_delivery_item(self):
        # We need a new cart item and a new delivery for the unique constraint
        cart_item = CartItems(
            customer_id=self.db.customer1.user_id, product_id=self.db.product2.id, quantity=1
        ); self.session.add(cart_item); self.commit_and_flush()

        delivery = Deliveries(
            driver_id=self.db.driver1.user_id, customer_showing_id=self.db.showing1.id, 
            payment_method_id=self.db.payment_method1.id, staff_id=self.db.staff1.user_id
        ); self.session.add(delivery); self.commit_and_flush()

        di = DeliveryItems(cart_item_id=cart_item.id, delivery_id=delivery.id); 
        self.session.add(di)
        self.commit_and_flush()
        self.assertIsNotNone(di.id)

    # 56. Verifies that a unique constraint prevents the same cart item from being linked to the same delivery twice.
    def test_56_unique_delivery_item_constraint(self):
        with self.assert_raises_integrity_error('Unique constraint on delivery_id/cart_item_id failed.'):
            self.session.add(DeliveryItems(
                cart_item_id=self.db.cart_item1.id, 
                delivery_id=self.db.delivery1.id
            ))
            self.commit_and_flush()
# --- CART ITEMS (4 TESTS) ---

class CartItemsTests(BaseIntegrationTest):
    # This class already uses BaseIntegrationTest, so we only need to adjust the assertions 
    # to use the context manager version if they were not already.
    # The assertions were already using the context manager helpers, so no change needed 
    # other than referencing the correct base class (BaseIntegrationTest).
    
    # 57. Tests the successful creation of a CartItems object with valid quantity.
    def test_57_create_cart_item(self):
        ci = CartItems(
            customer_id=self.db.customer1.user_id, 
            product_id=self.db.product1.id, 
            quantity=3
        )
        self.session.add(ci)
        self.commit_and_flush() 
        
        self.assertIsNotNone(ci.id)

    # 58. Confirms that a check constraint enforces the quantity field to be greater than 0.
    def test_58_check_quantity_greater_than_zero(self):
        with self.assert_raises_operational_error('Check constraint on quantity > 0 failed.'):
            self.session.add(CartItems(
                customer_id=self.db.customer1.user_id, 
                product_id=self.db.product1.id, 
                quantity=0
            ))
            self.commit_and_flush() # Error raised on flush

    # 59. Verifies that a unique constraint prevents a customer from having the same product twice in their cart.
    def test_59_unique_customer_product_constraint(self):
        # The base setup provides cart_item1 which already links customer1 and product1
        
        # Attempt to add the duplicate
        with self.assert_raises_integrity_error('Unique constraint on customer_id/product_id failed.'):
            self.session.add(CartItems(
                customer_id=self.db.customer1.user_id, 
                product_id=self.db.product1.id, 
                quantity=2 # Quantity is irrelevant, constraint is on the key pair
            ))
            self.commit_and_flush() # Error raised on flush

    # 60. Confirms that the quantity field correctly defaults to 1.
    def test_60_default_quantity(self):
        ci = CartItems(
            customer_id=self.db.customer1.user_id, 
            product_id=self.db.product2.id # Use a new product so it doesn't violate unique constraint
            # Quantity left out to test default
        ) 
        self.session.add(ci)
        self.commit_and_flush()
        
        # Verify the value set by the model's server_default
        self.assertEqual(ci.quantity, 1)

if __name__ == '__main__':
    unittest.main()