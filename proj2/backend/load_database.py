from database import get_database

db_name = "movie_munchers_dev"
database = get_database(db_name)
cursor_object = database.cursor()

# HELPER FUNCTION FOR EXECUTING SQL QUERIES
def insert(query, values):
    cursor_object.executemany(query, values)
    database.commit()

def populate_db():
   # theatres
   insert("""INSERT INTO theatres (name, address, phone, is_open) VALUES (%s, %s, %s, %s)""",
         [('Theatre A', '123 A St', '555-0001', True),
            ('Theatre B', '123 B St', '555-0002', True)])

   # auditoriums
   insert("""INSERT INTO auditoriums (theatre_id, number, capacity) VALUES (%s, %s, %s)""",
         [(1, 1, 4),
            (2, 1, 4)])

   # seats
   insert("""INSERT INTO seats (aisle, number, auditorium_id) VALUES (%s, %s, %s)""",
         [('A', 1, 1),
            ('A', 1, 2),
            ('B', 1, 1),
            ('B', 1, 2),
            ('C', 1, 1),
            ('C', 1, 2),
            ('D', 1, 1),
            ('D', 1, 2)])

   # users
   insert("""INSERT INTO users (name, email, phone, birthday, password_hash, role) VALUES (%s, %s, %s, %s, %s, %s)""",
         [('Alice', 'alice@ncsu.edu', '555-1000', '1990-01-01', 'hash1', 'staff'),
            ('Bob', 'bob@ncsu.edu', '555-2000', '1990-01-02', 'hash2', 'staff'),
            ('Charles', 'charles@ncsu.edu', '555-3000', '1990-01-03', 'hash3', 'staff'),
            ('Daisy', 'daisy@ncsu.edu', '555-4000', '1990-01-04', 'hash4', 'staff'),
            ('Evelyn', 'evelyn@ncsu.edu', '555-5000', '1990-01-04', 'hash5', 'customer'),
            ('Fergus', 'fergus@ncsu.edu', '555-6000', '1990-01-06', 'hash6', 'customer'),
            ('Grace', 'grace@ncsu.edu', '555-7000', '1990-01-07', 'hash7', 'customer' ),
            ('Hunter', 'hunter@ncsu.edu', '555-8000', '1990-01-08', 'hash8', 'customer'),
            ('Ingrid', 'ingrid@ncsu.edu', '555-9000', '1990-01-09', 'hash9', 'driver'),
            ('Jack', 'jack@ncsu.edu', '555-0100', '1990-01-10', 'hash10', 'driver'),
            ('Kyle', 'kyle@ncsu.edu', '555-0200', '1990-01-11', 'hash11', 'driver' ),
            ('Linda', 'linda@ncsu.edu', '555-0300', '1990-01-12', 'hash12', 'driver'),
            ('Molly', 'molly@ncsu.edu', '555-0400', '1990-01-13', 'hash13', 'supplier'),
            ('Nick', 'nick@ncsu.edu', '555-0500', '1990-01-14', 'hash14', 'supplier'),
            ('Oscar', 'oscar@ncsu.edu', '555-0600', '1990-01-15', 'hash15', 'supplier' ),
            ('Patricia', 'patricia@ncsu.edu', '555-0700', '1990-01-16', 'hash16', 'supplier')])
   # staff
   insert("""INSERT INTO staff (user_id, theatre_id, role, is_available) VALUES (%s, %s, %s, %s)""",
         [(1, 1, 'runner', True),
            (2, 2, 'admin', False),
            (3, 1, 'runner', True),
            (4, 2, 'admin', False)])
   # movies
   insert("""INSERT INTO movies (title, genre, length_mins, release_year, keywords, rating) VALUES (%s, %s, %s, %s, %s, %s)""", 
         [('Interstellar', 'Sci-Fi', 169, 2014, 'space, time, drama, intense, sweet', 4.8),
            ('The Dark Knight', 'Action', 152, 2008, 'action, intense, classic, hero, energy', 4.9)])

   # movie_showings
   insert("""INSERT INTO movie_showings (movie_id, auditorium_id, start_time, in_progress) VALUES (%s, %s, %s, %s)""",
         [(1, 1, '2025-11-04 19:30:00', False),
            (2, 2, '2025-10-31 20:00:00', False)])

   # customers
   insert("""INSERT INTO customers (user_id, default_theatre_id) VALUES (%s, %s)""",
         [(5, 1),
            (6, 2),
            (7, 1),
            (8, 2)])

   # customer_showings
   insert("""INSERT INTO customer_showings (customer_id, movie_showing_id, seat_id) VALUES (%s, %s, %s)""",
         [(5, 1, 1),
            (6, 2, 2)])

   # payment_methods
   insert("""INSERT INTO payment_methods (customer_id, card_number, expiration_month, expiration_year, billing_address, balance, is_default) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
         [(5, '1234567812345678', 11, 2028, '123 Suburb Rd', 200, True),
            (6, '1111222233334444', 1, 2026, '456 Suburb Rd', 5, False)])

   # drivers
   insert("""INSERT INTO drivers (user_id, license_plate, vehicle_type, vehicle_color, duty_status, rating, total_deliveries) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
         [(9, 'ABCD123', 'car', 'red', 'available', 5.00, 10),
            (10, None, 'bike', 'blue', 'available', 5.00, 20),
            (11, None, 'scooter', 'green', 'unavailable', 4.25, 30),
            (12, 'WXYZ789', 'car', 'silver', 'on_delivery', 4.95, 15)])

   # suppliers
   insert("""INSERT INTO suppliers (user_id, company_name, company_address, contact_phone, is_open) VALUES (%s, %s, %s, %s, %s)""",
         [(13, 'Company A', '123 Company Way', '555-0010', True),
            (14, 'Company B', '456 Company Way', '555-0020', False),
            (15, 'Company C', '789 Company Way', '555-0030', True),
            (16, 'Company D', '223 Company Way', '555-0040', False)])

   # products
   insert("""INSERT INTO products (supplier_id, name, unit_price, inventory_quantity, size, keywords, category, is_available) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
         [(13, 'Pepsi', 3.00, 10, 'medium', 'sweet, refreshing, cold, quick, energy', 'beverages', True),
            (14, 'Chips', 4.00, 20, None, 'crispy, salty, bold, quick, shareable', 'snacks', True),
            (15, 'Skittles', 5.00, 5, None, 'fun, colorful, tangy, sweet, fruity', 'candy', False),
            (16, 'Hot Dog', 7.00, 8, None, 'savory, filling, classic, flavorful', 'food', True)])

   # deliveries 
   insert("""INSERT INTO deliveries (driver_id, customer_showing_id, payment_method_id, staff_id, payment_status, total_price) VALUES (%s, %s, %s, %s, %s, %s)""",
         [(9, 1, 1, 1, 'completed', 9.00),
            (10, 2, 2, 1, 'completed', 5.00)])

   # delivery_items
   insert("""INSERT INTO delivery_items (product_id, delivery_id, quantity, discount) VALUES (%s, %s, %s, %s)""",
         [(1, 1, 3, 0.00),
            (3, 2, 1, 0.00)])

populate_db()
