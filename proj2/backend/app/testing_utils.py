# testing_utils.py

import unittest
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError, OperationalError
# Import the core components from your project files
from app import get_app, db 
import models # Assumes models.py imports 'db' from app

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
        """Inserts minimal, necessary data to satisfy Foreign Key constraints 
        (e.g., a customer and a product for CartItems tests)."""
        
        # NOTE: Using real models to insert data that tests will reference.
        # This data is rolled back after the test due to the tearDown() rollback.
        from models import Customers, Products 
        
        # Insert a Customer record
        customer = Customers(
            # Required fields must be set to pass validation/constraints
            user_id=1, name='Test Customer', email='test@example.com', 
            phone='555-1234', password_hash='hash', role='customer'
        )
        self.session.add(customer)
        
        # Insert a Product record
        product = Products(
            supplier_id=1, name='Test Product', unit_price=10.00, 
            inventory_quantity=10, is_available=True
        ) 
        self.session.add(product)
        self.commit_and_flush()

        class BaseRefs:
            customer1 = customer
            product1 = product
            
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