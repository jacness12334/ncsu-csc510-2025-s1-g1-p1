import mysql.connector

tables = ['theatres', 'auditoriums', 'seats', 'users', 'staff', 'movies', 'movie_showings',
          'customers', 'customer_showings', 'payment_methods', 'drivers', 'suppliers',
          'products', 'deliveries', 'delivery_items']

def drop_table(database, table):
    cursor = database.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute(f'DROP TABLE IF EXISTS {table}')
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    cursor.close()

def drop_all_tables(database):
    for table in tables:
        drop_table(database, table)
    
def get_database(db_name):
    my_host = 'localhost'
    my_user = 'root'
    my_password = ''

    root = mysql.connector.connect(
        host=my_host,
        user=my_user,
        password=my_password
    )
    temp_cursor = root.cursor()
    temp_cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db_name}')
    temp_cursor.close()
    root.close()
    connection = mysql.connector.connect(
        host=my_host,
        user=my_user,
        password=my_password,
        database = db_name
    )
    return connection    

def create_tables(db):
    cursor_object = db.cursor()
    theatres = """CREATE TABLE IF NOT EXISTS theatres (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(128) NOT NULL,
                address VARCHAR(256) NOT NULL,
                phone VARCHAR(32) NOT NULL,
                is_open BOOLEAN NOT NULL DEFAULT FALSE,
                CONSTRAINT unique_theatre_address UNIQUE(name, address)
                )"""

    auditoriums = """CREATE TABLE IF NOT EXISTS auditoriums (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    theatre_id BIGINT NOT NULL,
                    number INT UNSIGNED NOT NULL,
                    capacity INT UNSIGNED NOT NULL,
                    FOREIGN KEY (theatre_id) REFERENCES theatres(id),
                    CONSTRAINT unique_theatre_number UNIQUE(theatre_id, number),
                    CONSTRAINT check_auditorium_number CHECK (number > 0),
                    CONSTRAINT check_auditorium_capacity CHECK (capacity > 0)
                    )"""

    seats = """CREATE TABLE IF NOT EXISTS seats (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            aisle CHAR(1) NOT NULL,
            number INT UNSIGNED NOT NULL,
            auditorium_id BIGINT NOT NULL,
            FOREIGN KEY (auditorium_id) REFERENCES auditoriums(id),
            CONSTRAINT unique_auditorium_seat UNIQUE (auditorium_id, aisle, number),
            CONSTRAINT check_seat_number CHECK (number > 0)
            )"""

    users = """CREATE TABLE IF NOT EXISTS users (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(128) NOT NULL,
            email VARCHAR(128) NOT NULL UNIQUE,
            phone VARCHAR(32) NOT NULL UNIQUE,
            birthday DATE NOT NULL,
            password_hash VARCHAR(256) NOT NULL,
            role ENUM('customer', 'staff', 'driver', 'supplier') NOT NULL,
            account_status ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
            date_added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )"""

    staff = """CREATE TABLE IF NOT EXISTS staff (
            user_id BIGINT PRIMARY KEY,
            theatre_id BIGINT NOT NULL,
            role ENUM('admin', 'runner') NOT NULL,
            is_available BOOLEAN NOT NULL DEFAULT FALSE,
            date_added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (theatre_id) REFERENCES theatres(id)
            )"""

    movies = """CREATE TABLE IF NOT EXISTS movies (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(128) NOT NULL,
            genre VARCHAR(64) NOT NULL,
            length_mins SMALLINT UNSIGNED NOT NULL,
            release_year SMALLINT UNSIGNED NOT NULL,
            keywords VARCHAR(256) NOT NULL,
            rating DECIMAL(3,2) NOT NULL,
            CONSTRAINT check_movie_rating CHECK(0.00 <= rating AND 5.00 >= rating)
            )"""

    movie_showings = """CREATE TABLE IF NOT EXISTS movie_showings (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    movie_id BIGINT NOT NULL,
                    auditorium_id BIGINT NOT NULL,
                    start_time DATETIME NOT NULL,
                    in_progress BOOLEAN DEFAULT FALSE,
                    date_added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (movie_id) REFERENCES movies(id),
                    FOREIGN KEY (auditorium_id) REFERENCES auditoriums(id),
                    CONSTRAINT unique_auditorium_showing UNIQUE(auditorium_id, start_time)
                    )"""

    customers = """CREATE TABLE IF NOT EXISTS customers (
                user_id BIGINT PRIMARY KEY,
                default_theatre_id BIGINT NOT NULL,
                date_added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (default_theatre_id) REFERENCES theatres(id)
                )"""

    customer_showings = """CREATE TABLE IF NOT EXISTS customer_showings (
                        id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        customer_id BIGINT NOT NULL,
                        movie_showing_id BIGINT NOT NULL,
                        seat_id BIGINT NOT NULL,
                        date_added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        FOREIGN KEY (customer_id) REFERENCES customers(user_id),
                        FOREIGN KEY (movie_showing_id) REFERENCES movie_showings(id),
                        FOREIGN KEY (seat_id) REFERENCES seats(id),
                        CONSTRAINT unique_movie_seat UNIQUE(movie_showing_id, seat_id)
                        )"""

    payment_methods = """CREATE TABLE IF NOT EXISTS payment_methods (
                        id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        customer_id BIGINT NOT NULL,
                        card_number CHAR(16) NOT NULL,
                        expiration_month TINYINT UNSIGNED NOT NULL,
                        expiration_year SMALLINT UNSIGNED NOT NULL,
                        billing_address VARCHAR(256) NOT NULL,
                        balance DECIMAL(10,2) NOT NULL DEFAULT 100.00,
                        is_default BOOLEAN NOT NULL DEFAULT FALSE,
                        date_added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        FOREIGN KEY (customer_id) REFERENCES customers(user_id),
                        CONSTRAINT check_expiration_month CHECK (expiration_month BETWEEN 1 AND 12),
                        CONSTRAINT check_expiration_year CHECK (expiration_year >= 2025),
                        CONSTRAINT check_balance CHECK (balance >= 0)
                        )"""

    drivers = """CREATE TABLE IF NOT EXISTS drivers (
                user_id BIGINT PRIMARY KEY,
                license_plate VARCHAR(16) NULL,
                vehicle_type ENUM('car', 'bike', 'scooter', 'other') NOT NULL,
                vehicle_color VARCHAR(16) NOT NULL,
                duty_status ENUM('unavailable', 'available', 'on_delivery') NOT NULL DEFAULT 'unavailable',
                rating DECIMAL(3,2) NOT NULL DEFAULT 5.00,
                total_deliveries INT NOT NULL DEFAULT 0,
                date_added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                CONSTRAINT check_driver_rating CHECK (rating >= 0.00 AND rating <= 5.00)
                )"""

    suppliers = """CREATE TABLE IF NOT EXISTS suppliers (
                user_id BIGINT PRIMARY KEY,
                company_name VARCHAR(64) NOT NULL,
                company_address VARCHAR(256) NOT NULL,
                contact_phone VARCHAR(32) NOT NULL,
                is_open BOOLEAN NOT NULL DEFAULT FALSE,
                date_added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
                )"""

    products = """CREATE TABLE IF NOT EXISTS products (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                supplier_id BIGINT NOT NULL,
                name VARCHAR(128) NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                inventory_quantity INT UNSIGNED DEFAULT 0 NOT NULL,
                size ENUM('small', 'medium', 'large') DEFAULT NULL,
                keywords VARCHAR(256),
                category ENUM('beverages', 'snacks', 'candy', 'food') NOT NULL,
                is_available BOOLEAN NOT NULL DEFAULT FALSE,
                date_added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (supplier_id) REFERENCES suppliers(user_id),
                CONSTRAINT check_product_price CHECK (unit_price >= 0.00),
                CONSTRAINT check_product_inventory CHECK (inventory_quantity >= 0),
                CONSTRAINT unique_supplier_product UNIQUE(supplier_id, name)
                )"""

    deliveries = """CREATE TABLE IF NOT EXISTS deliveries (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            driver_id BIGINT NOT NULL,
            customer_showing_id BIGINT NOT NULL,
            payment_method_id BIGINT NOT NULL,
            staff_id BIGINT NOT NULL,
            payment_status ENUM('pending', 'completed', 'failed') NOT NULL,
            total_price DECIMAL(12,2) NOT NULL,
            delivery_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            delivery_status ENUM('pending', 'accepted', 'in_progress', 'ready_for_pickup', 'in_transit', 
                        'delivered', 'fulfilled', 'cancelled') DEFAULT 'pending' NOT NULL,
            date_added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (driver_id) REFERENCES drivers(user_id),
            FOREIGN KEY (customer_showing_id) REFERENCES customer_showings(id),
            FOREIGN KEY (payment_method_id) REFERENCES payment_methods(id),
            FOREIGN KEY (staff_id) REFERENCES staff(user_id),
            CONSTRAINT check_total_price CHECK (total_price >= 0.00)
            )"""

    delivery_items = """CREATE TABLE IF NOT EXISTS delivery_items (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    product_id BIGINT NOT NULL,
                    delivery_id BIGINT NOT NULL,
                    quantity INT UNSIGNED NOT NULL DEFAULT 1,
                    discount DECIMAL(10,2) DEFAULT 0.00 NOT NULL,
                    FOREIGN KEY (product_id) REFERENCES products(id),
                    FOREIGN KEY (delivery_id) REFERENCES deliveries(id) ON DELETE CASCADE,
                    CONSTRAINT unique_delivery_product UNIQUE (delivery_id, product_id),
                    CONSTRAINT check_item_quantity CHECK (quantity > 0),
                    CONSTRAINT check_discount_value CHECK (discount >= 0.00)
                    )"""

    cursor_object.execute(theatres)
    cursor_object.execute(auditoriums)
    cursor_object.execute(seats)
    cursor_object.execute(users)
    cursor_object.execute(staff)
    cursor_object.execute(movies)
    cursor_object.execute(movie_showings)
    cursor_object.execute(customers)
    cursor_object.execute(customer_showings)
    cursor_object.execute(payment_methods)
    cursor_object.execute(drivers)
    cursor_object.execute(suppliers)
    cursor_object.execute(products)
    cursor_object.execute(deliveries)
    cursor_object.execute(delivery_items)

    cursor_object.close()
    db.close()

prod_database = get_database("movie_munchers_prod")
# drop_all_tables(prod_database)
create_tables(prod_database)

dev_database = get_database("movie_munchers_dev")
# drop_all_tables(dev_database)
create_tables(dev_database)

test_database = get_database("movie_munchers_test")
# drop_all_tables(test_database)
create_tables(test_database)
