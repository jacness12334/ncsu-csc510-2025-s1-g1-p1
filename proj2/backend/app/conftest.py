import pytest
from app import create_app, db
from database import create_tables, drop_all_tables, get_database
from models import Theatres

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

@pytest.fixture
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

@pytest.fixture
def sample_customer(app, sample_user):
    from services.customer_service import CustomerService
    customer_service = CustomerService()
    with app.app_context():
        theatre = Theatres(name='Test Theatre', address='123 St', phone='5551111111', is_open=True)
        db.session.add(theatre)
        db.session.commit()

        customer = customer_service.create_customer(
            user_id=sample_user,  
            default_theatre_id=theatre.id
        )
        db.session.commit()
        customer_id = customer.user_id
    return customer_id


# TODO Add samples for driver, supplier, & staff

@pytest.fixture
def authenticated_client(client, app, sample_user):
    with app.app_context():
        client.post('/api/users/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
    return client