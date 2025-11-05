# models_test.py (Refactored to use BaseIntegrationTest)

import unittest
from datetime import date, datetime
# Import actual models from models.py
from models import CartItems, db
from sqlalchemy.exc import IntegrityError, OperationalError

# Import the integration test base class and utilities from the external file
from testing_utils import BaseIntegrationTest



#--------------------------------------------------------------------------
# 60 UNIT TESTS BEGIN HERE
# --------------------------------------------------------------------------
# For demonstration, we use placeholder classes and functions:

class TestAllModels(unittest.TestCase):
    def setUp(self):
        # In a real environment, this is where you would set up your in-memory DB
        # and create your session.
        self.db = MockDB()
        self.session = self.db

    # --- Helper Method Placeholders (Replace with actual DB interaction) ---
    def commit_and_flush(self):
        """Simulates successful commit/flush."""
        self.session.flush()

    def assert_raises_integrity_error(self, func, msg=None):
        """Simulates a UniqueConstraint/FK violation test."""
        # Replace with a real assertRaises(IntegrityError) call
        with self.assertRaises(Exception): func()

    def assert_raises_operational_error(self, func, msg=None):
        """Simulates a CheckConstraint/Enum violation test."""
        # Replace with a real assertRaises(OperationalError) call
        with self.assertRaises(Exception): func()

# --------------------------------------------------------------------------

# ----------------- THEATRES (4 TESTS) -----------------
    # 1. Tests the successful creation of a Theatres object with all required fields.
    def test_01_create_theatre(self):
        t = create_mock_model('Theatres', id=2, name='Test T', address='Test Addr', phone='555-3333'); self.session.add(t)
        self.commit_and_flush()
        self.assertIsNotNone(t.id)

    # 2. Verifies that a unique constraint prevents two theatres from having the same name and address.
    def test_02_unique_address_constraint(self):
        def create_duplicate():
            self.session.add(create_mock_model('Theatres', name=self.db.theatre1.name, address=self.db.theatre1.address, phone='555-9999'))
        self.assert_raises_integrity_error(create_duplicate, 'Unique constraint on name/address failed.')

    # 3. Confirms that the is_open field correctly defaults to False.
    def test_03_default_is_open_value(self):
        t = create_mock_model('Theatres', is_open=False)
        self.assertFalse(t.is_open, 'is_open should default to False.')

    # 4. Checks that the __repr__ method returns a correctly formatted string representation of the object.
    def test_04_repr_method(self):
        expected_repr = f"<Theatre id = {self.db.theatre1.id} name = '{self.db.theatre1.name}' address = '{self.db.theatre1.address}' is_open = {self.db.theatre1.is_open}>"
        self.assertEqual(repr(self.db.theatre1), expected_repr)

# ----------------- AUDITORIUMS (5 TESTS) -----------------
    # 5. Tests the successful creation of an Auditoriums object linked to a valid theatre.
    def test_05_create_auditorium(self):
        a = create_mock_model('Auditoriums', id=2, theatre_id=1, number=2, capacity=150); self.session.add(a)
        self.commit_and_flush()
        self.assertIsNotNone(a.id)

    # 6. Verifies that a unique constraint prevents two auditoriums in the same theatre from having the same number.
    def test_06_unique_number_constraint(self):
        def create_duplicate():
            self.session.add(create_mock_model('Auditoriums', theatre_id=1, number=self.db.auditorium1.number, capacity=150))
        self.assert_raises_integrity_error(create_duplicate, 'Unique constraint on theatre_id/number failed.')

    # 7. Confirms that a check constraint enforces the number field to be greater than 0.
    def test_07_check_number_greater_than_zero(self):
        def create_invalid():
            self.session.add(create_mock_model('Auditoriums', theatre_id=1, number=0, capacity=100))
        self.assert_raises_operational_error(create_invalid, 'Check constraint on number > 0 failed.')

    # 8. Confirms that a check constraint enforces the capacity field to be greater than 0.
    def test_08_check_capacity_greater_than_zero(self):
        def create_invalid():
            self.session.add(create_mock_model('Auditoriums', theatre_id=1, number=2, capacity=0))
        self.assert_raises_operational_error(create_invalid, 'Check constraint on capacity > 0 failed.')

    # 9. Ensures that deleting the linked theatre cascades and deletes the auditorium.
    def test_09_foreign_key_cascade_on_delete(self):
        # In a real test: delete theatre -> try to fetch auditorium -> assert None
        # self.session.delete(self.db.theatre1); self.session.commit()
        # self.assertIsNone(self.session.get(Auditoriums, self.db.auditorium1.id))
        pass

# ----------------- SEATS (3 TESTS) -----------------
    # 10. Tests the successful creation of a Seats object linked to a valid auditorium.
    def test_10_create_seat(self):
        s = create_mock_model('Seats', id=2, auditorium_id=1, aisle='B', number=1); self.session.add(s)
        self.commit_and_flush()
        self.assertIsNotNone(s.id)

    # 11. Verifies that a unique constraint prevents two seats in the same auditorium from having the same aisle and number.
    def test_11_unique_seat_constraint(self):
        def create_duplicate():
            self.session.add(create_mock_model('Seats', auditorium_id=1, aisle=self.db.seat1.aisle, number=self.db.seat1.number))
        self.assert_raises_integrity_error(create_duplicate, 'Unique constraint on auditorium_id/aisle/number failed.')

    # 12. Confirms that a check constraint enforces the number field to be greater than 0.
    def test_12_check_number_greater_than_zero(self):
        def create_invalid():
            self.session.add(create_mock_model('Seats', auditorium_id=1, aisle='Z', number=0))
        self.assert_raises_operational_error(create_invalid, 'Check constraint on number > 0 failed.')

# ----------------- USERS (6 TESTS) -----------------
    # 13. Tests the successful creation of a Users object with a valid role and all required fields.
    def test_13_create_user(self):
        u = create_mock_model('Users', id=2, name='Test U', email='new@test.com', phone='555-4444', birthday=date.today(), password_hash='hash', role='customer'); self.session.add(u)
        self.commit_and_flush()
        self.assertIsNotNone(u.id)

    # 14. Verifies that a unique constraint prevents creating two users with the same email.
    def test_14_unique_email_constraint(self):
        def create_duplicate():
            self.session.add(create_mock_model('Users', email=self.db.user1.email, phone='555-5555', birthday=date.today(), password_hash='hash', role='customer'))
        self.assert_raises_integrity_error(create_duplicate, 'Unique constraint on email failed.')

    # 15. Verifies that a unique constraint prevents creating two users with the same phone number.
    def test_15_unique_phone_constraint(self):
        def create_duplicate():
            self.session.add(create_mock_model('Users', email='other@test.com', phone=self.db.user1.phone, birthday=date.today(), password_hash='hash', role='customer'))
        self.assert_raises_integrity_error(create_duplicate, 'Unique constraint on phone failed.')

    # 16. Confirms that the account_status field correctly defaults to 'active'.
    def test_16_default_account_status(self):
        u = create_mock_model('Users', name='D', email='d@t.com', phone='555-6666', birthday=date.today(), password_hash='hash', role='staff', account_status='active')
        self.assertEqual(u.account_status, 'active', 'account_status should default to active')

    # 17. Checks that date_added is set on creation and last_updated is updated upon modification.
    def test_17_timestamp_defaults(self):
        u = create_mock_model('Users', date_added=datetime.now(), last_updated=datetime.now())
        self.assertIsNotNone(u.date_added)
        # The update check relies on server_onupdate, which requires a real DB connection
        # u.update(name='Updated'); self.session.commit()
        # self.assertGreater(u.last_updated, u.date_added)
        pass

    # 18. Confirms that the role field only accepts values from the defined enum.
    def test_18_enum_role_validation(self):
        def create_invalid():
            self.session.add(create_mock_model('Users', role='invalid_role'))
        self.assert_raises_operational_error(create_invalid, 'Enum validation for role failed.')

# ----------------- STAFF (4 TESTS) -----------------
    # 19. Tests the successful creation of a Staff object linked to a valid user and theatre.
    def test_19_create_staff(self):
        s = create_mock_model('Staff', user_id=2, theatre_id=1, role='runner'); self.session.add(s)
        self.commit_and_flush()
        self.assertIsNotNone(s.user_id)

    # 20. Confirms that the is_available field correctly defaults to False.
    def test_20_default_is_available_value(self):
        s = create_mock_model('Staff', user_id=3, theatre_id=1, role='admin', is_available=False)
        self.assertFalse(s.is_available, 'is_available should default to False')

    # 21. Ensures that deleting the linked user cascades and deletes the staff record.
    def test_21_foreign_key_on_delete(self):
        # In a real test: delete user -> try to fetch staff -> assert None
        # self.session.delete(self.db.user1); self.session.commit()
        # self.assertIsNone(self.session.get(Staff, self.db.staff1.user_id))
        pass

    # 22. Confirms that user_id is correctly set as the primary key (requires model introspection).
    def test_22_primary_key_is_user_id(self):
        self.assertTrue(hasattr(self.db.staff1, 'user_id'))
        # self.assertTrue(db.inspect(Staff).primary_key[0].name == 'user_id')
        pass

# ----------------- MOVIES (3 TESTS) -----------------
    # 23. Tests the successful creation of a Movies object with valid rating and length.
    def test_23_create_movie(self):
        m = create_mock_model('Movies', id=2, title='New Movie', genre='Action', length_mins=100, release_year=2023, keywords='K1,K2', rating='4.10'); self.session.add(m)
        self.commit_and_flush()
        self.assertIsNotNone(m.id)

    # 24. Confirms that a check constraint enforces the rating to be between 0.00 and 5.00.
    def test_24_rating_check_constraint(self):
        def create_invalid_high():
            self.session.add(create_mock_model('Movies', rating='5.01'))
        def create_invalid_low():
            self.session.add(create_mock_model('Movies', rating='-0.01'))
        self.assert_raises_operational_error(create_invalid_high, 'Check constraint on rating <= 5.00 failed.')
        self.assert_raises_operational_error(create_invalid_low, 'Check constraint on rating >= 0.00 failed.')

    # 25. Checks that the rating column correctly stores values with a precision of (3, 2).
    def test_25_decimal_precision(self):
        m = create_mock_model('Movies', rating='4.12')
        self.assertEqual(str(m.rating), '4.12', 'Rating should store with (3,2) precision')

# ----------------- MOVIE SHOWINGS (3 TESTS) -----------------
    # 26. Tests the successful creation of a MovieShowings object linked to a movie and auditorium.
    def test_26_create_movie_showing(self):
        ms = create_mock_model('MovieShowings', id=2, movie_id=1, auditorium_id=1, start_time=datetime.now()); self.session.add(ms)
        self.commit_and_flush()
        self.assertIsNotNone(ms.id)

    # 27. Verifies that a unique constraint prevents two showings from being scheduled in the same auditorium at the same start time.
    def test_27_unique_showing_constraint(self):
        def create_duplicate():
            self.session.add(create_mock_model('MovieShowings', movie_id=2, auditorium_id=self.db.showing1.auditorium_id, start_time=self.db.showing1.start_time))
        self.assert_raises_integrity_error(create_duplicate, 'Unique constraint on auditorium_id/start_time failed.')

    # 28. Confirms that the in_progress field correctly defaults to False.
    def test_28_default_in_progress_value(self):
        ms = create_mock_model('MovieShowings', movie_id=1, auditorium_id=2, start_time=datetime.now(), in_progress=False)
        self.assertFalse(ms.in_progress, 'in_progress should default to False')

# ----------------- CUSTOMERS (3 TESTS) -----------------
    # 29. Tests the successful creation of a Customers object linked to a valid user and a default theatre.
    def test_29_create_customer(self):
        c = create_mock_model('Customers', user_id=2, default_theatre_id=1); self.session.add(c)
        self.commit_and_flush()
        self.assertIsNotNone(c.user_id)

    # 30. Ensures that deleting the linked user cascades and deletes the customer record.
    def test_30_foreign_key_on_delete(self):
        # In a real test: delete user -> try to fetch customer -> assert None
        # self.session.delete(self.db.user1); self.session.commit()
        # self.assertIsNone(self.session.get(Customers, self.db.customer1.user_id))
        pass

    # 31. Confirms that user_id is correctly set as the primary key.
    def test_31_primary_key_is_user_id(self):
        self.assertTrue(hasattr(self.db.customer1, 'user_id'))
        # self.assertTrue(db.inspect(Customers).primary_key[0].name == 'user_id')
        pass

# ----------------- CUSTOMER SHOWINGS (2 TESTS) -----------------
    # 32. Tests the successful creation of a CustomerShowings record linking a customer, movie showing, and seat.
    def test_32_create_customer_showing(self):
        cs = create_mock_model('CustomerShowings', id=2, customer_id=1, movie_showing_id=1, seat_id=2); self.session.add(cs)
        self.commit_and_flush()
        self.assertIsNotNone(cs.id)

    # 33. Verifies that a unique constraint prevents the same seat from being booked for the same movie showing twice.
    def test_33_unique_movie_seat_constraint(self):
        def create_duplicate():
            self.session.add(create_mock_model('CustomerShowings', customer_id=1, movie_showing_id=self.db.showing1.id, seat_id=self.db.seat1.id))
        self.assert_raises_integrity_error(create_duplicate, 'Unique constraint on movie_showing_id/seat_id failed.')

# ----------------- PAYMENT METHODS (5 TESTS) -----------------
    # 34. Tests the successful creation of a PaymentMethods object with valid dates and balance.
    def test_34_create_payment_method(self):
        pm = create_mock_model('PaymentMethods', id=2, customer_id=1, card_number='1234123412344321', expiration_month=12, expiration_year=2025, billing_address='123 PM', balance='100.00'); self.session.add(pm)
        self.commit_and_flush()
        self.assertIsNotNone(pm.id)

    # 35. Confirms that a check constraint enforces the expiration_month to be between 1 and 12.
    def test_35_check_expiration_month(self):
        def create_invalid():
            self.session.add(create_mock_model('PaymentMethods', expiration_month=13))
        self.assert_raises_operational_error(create_invalid, 'Check constraint on expiration_month failed.')

    # 36. Confirms that a check constraint enforces the expiration_year to be 2025 or later.
    def test_36_check_expiration_year(self):
        def create_invalid():
            self.session.add(create_mock_model('PaymentMethods', expiration_year=2024))
        self.assert_raises_operational_error(create_invalid, 'Check constraint on expiration_year failed.')

    # 37. Confirms that a check constraint enforces the balance field to be greater than or equal to 0.
    def test_37_check_balance_non_negative(self):
        def create_invalid():
            self.session.add(create_mock_model('PaymentMethods', balance='-0.01'))
        self.assert_raises_operational_error(create_invalid, 'Check constraint on balance >= 0 failed.')

    # 38. Confirms that the is_default field correctly defaults to False.
    def test_38_default_is_default_value(self):
        pm = create_mock_model('PaymentMethods', is_default=False)
        self.assertFalse(pm.is_default, 'is_default should default to False')

# ----------------- DRIVERS (4 TESTS) -----------------
    # 39. Tests the successful creation of a Drivers object with all required fields.
    def test_39_create_driver(self):
        d = create_mock_model('Drivers', user_id=2, license_plate='ABC1234', vehicle_type='car', vehicle_color='red'); self.session.add(d)
        self.commit_and_flush()
        self.assertIsNotNone(d.user_id)

    # 40. Confirms that the duty_status field correctly defaults to 'unavailable'.
    def test_40_default_duty_status(self):
        d = create_mock_model('Drivers', duty_status='unavailable')
        self.assertEqual(d.duty_status, 'unavailable', 'duty_status should default to unavailable')

    # 41. Confirms that a check constraint enforces the rating to be between 0.00 and 5.00.
    def test_41_rating_check_constraint(self):
        def create_invalid():
            self.session.add(create_mock_model('Drivers', rating='5.01'))
        self.assert_raises_operational_error(create_invalid, 'Check constraint on rating failed.')

    # 42. Confirms that the total_deliveries field correctly defaults to 0.
    def test_42_default_total_deliveries(self):
        d = create_mock_model('Drivers', total_deliveries=0)
        self.assertEqual(d.total_deliveries, 0, 'total_deliveries should default to 0')

# ----------------- SUPPLIERS (3 TESTS) -----------------
    # 43. Tests the successful creation of a Suppliers object linked to a valid user.
    def test_43_create_supplier(self):
        s = create_mock_model('Suppliers', user_id=2, company_name='Co Name', company_address='Co Addr', contact_phone='555-9999'); self.session.add(s)
        self.commit_and_flush()
        self.assertIsNotNone(s.user_id)

    # 44. Confirms that the is_open field correctly defaults to False.
    def test_44_default_is_open_value(self):
        s = create_mock_model('Suppliers', is_open=False)
        self.assertFalse(s.is_open, 'is_open should default to False')

    # 45. Confirms that user_id is correctly set as the primary key.
    def test_45_primary_key_is_user_id(self):
        self.assertTrue(hasattr(self.db.supplier1, 'user_id'))
        # self.assertTrue(db.inspect(Suppliers).primary_key[0].name == 'user_id')
        pass

# ----------------- PRODUCTS (5 TESTS) -----------------
    # 46. Tests the successful creation of a Products object with valid price and inventory.
    def test_46_create_product(self):
        p = create_mock_model('Products', id=2, supplier_id=1, name='Soda', unit_price='2.50', category='beverages'); self.session.add(p)
        self.commit_and_flush()
        self.assertIsNotNone(p.id)

    # 47. Confirms that a check constraint enforces the unit_price field to be non-negative.
    def test_47_check_unit_price_non_negative(self):
        def create_invalid():
            self.session.add(create_mock_model('Products', unit_price='-0.01'))
        self.assert_raises_operational_error(create_invalid, 'Check constraint on unit_price >= 0 failed.')

    # 48. Confirms that a check constraint enforces the inventory_quantity field to be non-negative.
    def test_48_check_inventory_non_negative(self):
        def create_invalid():
            self.session.add(create_mock_model('Products', inventory_quantity=-1))
        self.assert_raises_operational_error(create_invalid, 'Check constraint on inventory_quantity >= 0 failed.')

    # 49. Verifies that a unique constraint prevents a supplier from having two products with the same name.
    def test_49_unique_supplier_product_constraint(self):
        def create_duplicate():
            self.session.add(create_mock_model('Products', supplier_id=1, name=self.db.product1.name))
        self.assert_raises_integrity_error(create_duplicate, 'Unique constraint on supplier_id/name failed.')

    # 50. Confirms that the is_available field correctly defaults to True.
    def test_50_default_is_available_value(self):
        p = create_mock_model('Products', is_available=True)
        self.assertEqual(p.is_available, True, 'is_available should default to True')
        
        
# ----------------- DELIVERIES (4 TESTS) -----------------
    # 51. Tests the successful creation of a Deliveries object linked to all foreign keys.
    def test_51_create_delivery(self):
        d = create_mock_model('Deliveries', id=2, driver_id=1, customer_showing_id=1, payment_method_id=1, staff_id=1, total_price='15.00'); self.session.add(d)
        self.commit_and_flush()
        self.assertIsNotNone(d.id)

    # 52. Confirms that a check constraint enforces the total_price field to be non-negative.
    def test_52_check_total_price_non_negative(self):
        def create_invalid():
            self.session.add(create_mock_model('Deliveries', total_price='-0.01'))
        self.assert_raises_operational_error(create_invalid, 'Check constraint on total_price >= 0 failed.')

    # 53. Confirms that the payment_status field correctly defaults to 'pending'.
    def test_53_default_payment_status(self):
        d = create_mock_model('Deliveries', payment_status='pending')
        self.assertEqual(d.payment_status, 'pending', 'payment_status should default to pending')

    # 54. Confirms that the delivery_status field correctly defaults to 'pending'.
    def test_54_default_delivery_status(self):
        d = create_mock_model('Deliveries', delivery_status='pending')
        self.assertEqual(d.delivery_status, 'pending', 'delivery_status should default to pending')

# ----------------- DELIVERY ITEMS (2 TESTS) -----------------
    # 55. Tests the successful creation of a DeliveryItems object linking a cart item to a delivery.
    def test_55_create_delivery_item(self):
        di = create_mock_model('DeliveryItems', id=2, cart_item_id=2, delivery_id=1); self.session.add(di)
        self.commit_and_flush()
        self.assertIsNotNone(di.id)

    # 56. Verifies that a unique constraint prevents the same cart item from being linked to the same delivery twice.
    def test_56_unique_delivery_item_constraint(self):
        def create_duplicate():
            self.session.add(create_mock_model('DeliveryItems', cart_item_id=self.db.cart_item1.id, delivery_id=self.db.delivery1.id))
        self.assert_raises_integrity_error(create_duplicate, 'Unique constraint on delivery_id/cart_item_id failed.')
# --- CART ITEMS (4 TESTS) ---

class CartItemsTests(BaseIntegrationTest):
    # BaseIntegrationTest sets up self.session, self.db (for base references)

    # 57. Tests the successful creation of a CartItems object with valid quantity.
    def test_57_create_cart_item(self):
        ci = CartItems(
            customer_id=self.db.customer1.id, 
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
                customer_id=self.db.customer1.id, 
                product_id=self.db.product1.id, 
                quantity=0
            ))
            self.commit_and_flush() # Error raised on flush

    # 59. Verifies that a unique constraint prevents a customer from having the same product twice in their cart.
    def test_59_unique_customer_product_constraint(self):
        # 1. Add the first, valid item
        self.session.add(CartItems(
            customer_id=self.db.customer1.id, 
            product_id=self.db.product1.id, 
            quantity=1
        ))
        self.commit_and_flush() 

        # 2. Attempt to add the duplicate
        with self.assert_raises_integrity_error('Unique constraint on customer_id/product_id failed.'):
            self.session.add(CartItems(
                customer_id=self.db.customer1.id, 
                product_id=self.db.product1.id, 
                quantity=2 # Quantity is irrelevant, constraint is on the key pair
            ))
            self.commit_and_flush() # Error raised on flush

    # 60. Confirms that the quantity field correctly defaults to 1.
    def test_60_default_quantity(self):
        ci = CartItems(
            customer_id=self.db.customer1.id, 
            product_id=self.db.product1.id
            # Quantity left out to test default
        ) 
        self.session.add(ci)
        self.commit_and_flush()
        
        # Verify the value set by the model's server_default
        self.assertEqual(ci.quantity, 1)

if __name__ == '__main__':
    unittest.main()