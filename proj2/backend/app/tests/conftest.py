import pytest
from app import create_app, db
from database import create_tables, drop_all_tables, get_database
from models import Theatres, Suppliers, Products, Drivers, Staff, Movies, MovieShowings, Seats, Auditoriums

@pytest.fixture(scope='function')
def app():
    app = create_app('testing')
    with app.app_context():
        test_db = get_database('movie_munchers_test')
        drop_all_tables(test_db)
        create_tables(test_db)
        test_db.close()
        yield app
        db.session.remove()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def sample_user(app):
    from services.user_service import UserService
    user_service = UserService()
    with app.app_context():
        user = user_service.create_user(
            name='Test User',
            email='test@example.com',
            phone='1234567890',
            birthday='1990-01-01',
            password='password123',
            role='customer'
        )
        db.session.commit()
        user_id = user.id
    return user_id

@pytest.fixture(scope='function')
def sample_customer(app):
    from services.customer_service import CustomerService
    customer_service = CustomerService()

    with app.app_context():
        theatre = Theatres(
            name='Test Theatre', 
            address='123 St', 
            phone='5551111111', 
            is_open=True
        )
        db.session.add(theatre)
        db.session.commit()

        customer = customer_service.create_customer(
            name='Test User',
            email='test@example.com',
            phone='1234567890',
            birthday='1990-01-01',
            password='password123',
            role='customer',
            default_theatre_id=theatre.id
        )
        customer_id = customer.user_id
    return customer_id

@pytest.fixture(scope='function')
def sample_supplier(app):
    from services.user_service import UserService
    user_service = UserService()
    with app.app_context():
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
        supplier_id = supplier.user_id
    return supplier_id


@pytest.fixture(scope='function')
def sample_product(app, sample_supplier):
    with app.app_context():
        product = Products(
            supplier_id=sample_supplier,
            name='Popcorn',
            unit_price=5.99,
            inventory_quantity=100,
            category='snacks',
            is_available=True
        )
        db.session.add(product)
        db.session.commit()
        product_id = product.id
    return product_id

@pytest.fixture(scope='function')
def sample_product_extra(app, sample_supplier):
    with app.app_context():
        product = Products(
            supplier_id=sample_supplier,
            name='Soda',
            unit_price=2.99,
            inventory_quantity=50,
            category='beverages',
            is_available=True
        )
        db.session.add(product)
        db.session.commit()
        product_id = product.id
    return product_id

@pytest.fixture(scope='function')
def sample_driver(app):
    from services.user_service import UserService
    user_service = UserService()
    with app.app_context():
        driver_user = user_service.create_user(
            name='Driver',
            email='driver@example.com',
            phone='5556667777',
            birthday='1980-01-01',
            password='password123',
            role='driver'
        )
        driver = Drivers(
            user_id=driver_user.id,
            license_plate='XYZ1234',
            vehicle_type='car',
            vehicle_color='blue',
            duty_status='available',
            rating=4.7,
            total_deliveries=10
        )
        db.session.add(driver)
        db.session.commit()
        driver_id = driver.user_id
    return driver_id

@pytest.fixture(scope='function')
def sample_staff(app):
    from services.user_service import UserService
    user_service = UserService()

    with app.app_context():
        
        theatre = Theatres(
                name='Test Theatre', 
                address='123 St', 
                phone='5551111111', 
                is_open=True
            )
        db.session.add(theatre)
        db.session.commit()
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
            theatre_id=theatre.id,
            role='runner',          
            is_available=True
        )
        db.session.add(staff)
        db.session.commit()
        staff_id = staff_user.id 
    return staff_id

@pytest.fixture(scope='function')
def sample_customer_showing(app, sample_customer):
    from services.customer_service import CustomerService
    customer_service = CustomerService()
    with app.app_context():
        customer = customer_service.get_customer(sample_customer)

        auditorium = Auditoriums(theatre_id=customer.default_theatre_id, number=1, capacity=100)
        db.session.add(auditorium)
        db.session.commit()

        seat = Seats(aisle='A', number=1, auditorium_id=auditorium.id)
        db.session.add(seat)
        db.session.commit()
        
        movie = Movies(title='Test Movie', genre='Action', length_mins=120, release_year=2024, keywords='test', rating=4.5)
        db.session.add(movie)
        db.session.commit()

        showing = MovieShowings(movie_id=movie.id, auditorium_id=auditorium.id, start_time='2025-12-01 19:00:00')
        db.session.add(showing)
        db.session.commit()

        customer_showing = customer_service.create_customer_showing(
            user_id=sample_customer,
            movie_showing_id=showing.id,
            seat_id=seat.id
        )
        customer_showing_id = customer_showing.id
    return customer_showing_id
    
@pytest.fixture(scope='function')
def authenticated_client(client, app, sample_user):
    with app.app_context():
        client.post('/api/users/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
    return client