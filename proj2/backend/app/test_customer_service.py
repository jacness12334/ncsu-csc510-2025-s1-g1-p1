import pytest
from services.customer_service import CustomerService
from services.user_service import UserService
from models import Theatres, PaymentMethods, Products, CartItems, MovieShowings, Seats
from app import db


class TestCustomerService:
        
    def test_create_customer_success(self, app):
        with app.app_context():
            customer_service = CustomerService()
            
            theatre = Theatres(name='Test Cinema', address='123 Main St', phone='5551234567', is_open=True)
            db.session.add(theatre)
            db.session.commit()
            
            customer = customer_service.create_customer(
                name='John Customer',
                email='customer@example.com',
                phone='5559876543',
                birthday='1990-05-15',
                password='password123',
                role='customer',
                default_theatre_id=theatre.id
            )
            
            assert customer is not None
            assert customer.user_id is not None
            assert customer.default_theatre_id == theatre.id
    
    def test_create_customer_wrong_role(self, app):
        with app.app_context():
            customer_service = CustomerService()
            
            with pytest.raises(ValueError, match="User role is not 'customer'"):
                customer_service.create_customer(
                    name='Wrong Role',
                    email='wrong@example.com',
                    phone='5551111111',
                    birthday='1990-01-01',
                    password='password123',
                    role='driver',  
                    default_theatre_id=1
                )
    
    def test_create_customer_duplicate(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            with pytest.raises(ValueError, match="Customer record already exists"):
                customer_service.create_customer(
                    name='Test User',
                    email='test@example.com',
                    phone='1234567890',
                    birthday='1990-01-01',
                    password='password123',
                    role='customer',
                    default_theatre_id=1
                )
    
    def test_get_customer_success(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            customer = customer_service.get_customer(sample_customer.user_id)
            
            assert customer is not None
            assert customer.user_id == sample_customer.user_id
    
    def test_get_customer_not_found(self, app):
        with app.app_context():
            customer_service = CustomerService()
            
            with pytest.raises(ValueError, match="Customer .* not found"):
                customer_service.get_customer(99999)
    
    def test_delete_customer_success(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            user_id = sample_customer.user_id
            
            customer_service.delete_customer(user_id)
            
            with pytest.raises(ValueError, match="Customer .* not found"):
                customer_service.get_customer(user_id)
    
    def test_update_default_theatre_success(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            new_theatre = Theatres(name='New Cinema', address='456 Oak St', phone='5559999999', is_open=True)
            db.session.add(new_theatre)
            db.session.commit()
            
            updated_customer = customer_service.update_default_theatre(
                user_id=sample_customer.user_id,
                new_theatre_id=new_theatre.id
            )
            
            assert updated_customer.default_theatre_id == new_theatre.id
    
    def test_update_default_theatre_not_found(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            with pytest.raises(ValueError, match="Theatre .* not found"):
                customer_service.update_default_theatre(
                    user_id=sample_customer.user_id,
                    new_theatre_id=99999
                )
        
    def test_add_payment_method_success(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            payment_method = customer_service.add_payment_method(
                user_id=sample_customer.user_id,
                card_number='1234567812345678',
                expiration_month=12,
                expiration_year=2027,
                billing_address='789 Pine St',
                balance=100.00,
                is_default=True
            )
            
            assert payment_method is not None
            assert payment_method.customer_id == sample_customer.user_id
            assert payment_method.card_number == '1234567812345678'
            assert payment_method.balance == 100.00
    
    def test_add_payment_method_duplicate(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            customer_service.add_payment_method(
                user_id=sample_customer.user_id,
                card_number='1234567812345678',
                expiration_month=12,
                expiration_year=2027,
                billing_address='789 Pine St',
                balance=100.00,
                is_default=True
            )
            
            with pytest.raises(ValueError, match="Payment method already exists"):
                customer_service.add_payment_method(
                    user_id=sample_customer.user_id,
                    card_number='1234567812345678',  
                    expiration_month=12,
                    expiration_year=2027,
                    billing_address='Different Address',
                    balance=50.00,
                    is_default=False
                )
    
    def test_get_customer_payment_methods_success(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            customer_service.add_payment_method(
                user_id=sample_customer.user_id,
                card_number='1111222233334444',
                expiration_month=6,
                expiration_year=2026,
                billing_address='Address 1',
                balance=100.00,
                is_default=True
            )
            
            customer_service.add_payment_method(
                user_id=sample_customer.user_id,
                card_number='5555666677778888',
                expiration_month=9,
                expiration_year=2028,
                billing_address='Address 2',
                balance=200.00,
                is_default=False
            )
            
            payment_methods = customer_service.get_customer_payment_methods(sample_customer.user_id)
            
            assert len(payment_methods) == 2
    
    def test_get_customer_payment_methods_none(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            with pytest.raises(ValueError, match="Payment methods for customer .* not found"):
                customer_service.get_customer_payment_methods(sample_customer.user_id)
    
    def test_delete_payment_method_success(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            payment_method = customer_service.add_payment_method(
                user_id=sample_customer.user_id,
                card_number='1234567812345678',
                expiration_month=12,
                expiration_year=2027,
                billing_address='789 Pine St',
                balance=100.00,
                is_default=True
            )
            
            result = customer_service.delete_payment_method(payment_method.id)
            assert result is True
            
            with pytest.raises(ValueError, match="Payment methods for customer .* not found"):
                customer_service.get_customer_payment_methods(sample_customer.user_id)
    
    def test_delete_payment_method_not_found(self, app):
        with app.app_context():
            customer_service = CustomerService()
            
            with pytest.raises(ValueError, match="Payment method not found"):
                customer_service.delete_payment_method(99999)
    
    def test_add_funds_to_payment_method_success(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            payment_method = customer_service.add_payment_method(
                user_id=sample_customer.user_id,
                card_number='1234567812345678',
                expiration_month=12,
                expiration_year=2027,
                billing_address='789 Pine St',
                balance=100.00,
                is_default=True
            )
            
            updated_pm = customer_service.add_funds_to_payment_method(payment_method.id, 50.00)
            
            assert updated_pm.balance == 150.00
    
    def test_add_funds_invalid_amount(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            payment_method = customer_service.add_payment_method(
                user_id=sample_customer.user_id,
                card_number='1234567812345678',
                expiration_month=12,
                expiration_year=2027,
                billing_address='789 Pine St',
                balance=100.00,
                is_default=True
            )
            
            with pytest.raises(ValueError, match="Amount to add must be greater than zero"):
                customer_service.add_funds_to_payment_method(payment_method.id, 0.00)
            
            with pytest.raises(ValueError, match="Amount to add must be greater than zero"):
                customer_service.add_funds_to_payment_method(payment_method.id, -10.00)
        
    def test_create_cart_item_success(self, app, sample_customer):
        with app.app_context():
            user_service = UserService()
            customer_service = CustomerService()
            
            from models import Suppliers
            supplier_user = user_service.create_user(
                name='Supplier',
                email='supplier@example.com',
                phone='5551112222',
                birthday='1980-01-01',
                password='password123',
                role='supplier'
            )
            supplier = Suppliers(user_id=supplier_user.id, company_name='Snacks Inc', company_address='123 Supply St', contact_phone='5553334444')
            db.session.add(supplier)
            db.session.commit()
            
            product = Products(
                supplier_id=supplier.user_id,
                name='Popcorn',
                unit_price=5.99,
                inventory_quantity=100,
                category='snacks',
                is_available=True
            )
            db.session.add(product)
            db.session.commit()
            
            cart_item = customer_service.create_cart_item(
                customer_id=sample_customer.user_id,
                product_id=product.id,
                quantity=2
            )
            
            assert cart_item is not None
            assert cart_item.customer_id == sample_customer.user_id
            assert cart_item.product_id == product.id
            assert cart_item.quantity == 2
    
    def test_create_cart_item_existing_increases_quantity(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            product = Products(
                supplier_id=1,  
                name='Soda',
                unit_price=3.99,
                inventory_quantity=50,
                category='beverages',
                is_available=True
            )
            db.session.add(product)
            db.session.commit()
            
            cart_item1 = customer_service.create_cart_item(
                customer_id=sample_customer.user_id,
                product_id=product.id,
                quantity=1
            )
            
            cart_item2 = customer_service.create_cart_item(
                customer_id=sample_customer.user_id,
                product_id=product.id,
                quantity=2
            )
            
            assert cart_item1.id == cart_item2.id
            assert cart_item2.quantity == 3
    
    def test_create_cart_item_invalid_quantity(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            with pytest.raises(ValueError, match="Quantity to add must be greater than zero"):
                customer_service.create_cart_item(
                    customer_id=sample_customer.user_id,
                    product_id=1,
                    quantity=0
                )
    
    def test_update_cart_item_success(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            product = Products(
                supplier_id=1,
                name='Candy',
                unit_price=2.99,
                inventory_quantity=100,
                category='candy',
                is_available=True
            )
            db.session.add(product)
            db.session.commit()
            
            cart_item = customer_service.create_cart_item(
                customer_id=sample_customer.user_id,
                product_id=product.id,
                quantity=1
            )
            
            updated_item = customer_service.update_cart_item(cart_item.id, 3)
            
            assert updated_item.quantity == 4  
    
    def test_delete_cart_item_success(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            product = Products(
                supplier_id=1,
                name='Nachos',
                unit_price=6.99,
                inventory_quantity=50,
                category='food',
                is_available=True
            )
            db.session.add(product)
            db.session.commit()
            
            cart_item = customer_service.create_cart_item(
                customer_id=sample_customer.user_id,
                product_id=product.id,
                quantity=1
            )
            
            customer_service.delete_cart_item(cart_item.id)
            
            deleted_item = CartItems.query.get(cart_item.id)
            assert deleted_item is None
        
    def test_calculate_total_price_success(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            product1 = Products(supplier_id=1, name='Item1', unit_price=10.00, discount=1.00, inventory_quantity=10, category='snacks', is_available=True)
            product2 = Products(supplier_id=1, name='Item2', unit_price=5.00, discount=0.50, inventory_quantity=10, category='beverages', is_available=True)
            db.session.add_all([product1, product2])
            db.session.commit()
            
            cart_item1 = CartItems(customer_id=sample_customer.user_id, product_id=product1.id, quantity=2)
            cart_item2 = CartItems(customer_id=sample_customer.user_id, product_id=product2.id, quantity=3)
            db.session.add_all([cart_item1, cart_item2])
            db.session.commit()
            
            cart_items = [cart_item1, cart_item2]
            
            total = customer_service.calculate_total_price(cart_items)
            
            assert total == 31.50
        
    def test_create_customer_showing_success(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            theatre = Theatres(name='Cinema', address='123 St', phone='5551111111', is_open=True)
            db.session.add(theatre)
            db.session.commit()
            
            from models import Auditoriums, Movies
            auditorium = Auditoriums(theatre_id=theatre.id, number=1, capacity=100)
            db.session.add(auditorium)
            db.session.commit()
            
            seat = Seats(aisle='A', number=10, auditorium_id=auditorium.id)
            db.session.add(seat)
            db.session.commit()
            
            movie = Movies(title='Test Movie', genre='Action', length_mins=120, release_year=2024, keywords='test', rating=4.5)
            db.session.add(movie)
            db.session.commit()
            
            showing = MovieShowings(movie_id=movie.id, auditorium_id=auditorium.id, start_time='2025-12-01 19:00:00')
            db.session.add(showing)
            db.session.commit()
            
            customer_showing = customer_service.create_customer_showing(
                user_id=sample_customer.user_id,
                movie_showing_id=showing.id,
                seat_id=seat.id
            )
            
            assert customer_showing is not None
            assert customer_showing.customer_id == sample_customer.user_id
            assert customer_showing.movie_showing_id == showing.id
            assert customer_showing.seat_id == seat.id
    
    def test_charge_payment_method_success(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            payment_method = customer_service.add_payment_method(
                user_id=sample_customer.user_id,
                card_number='1234567812345678',
                expiration_month=12,
                expiration_year=2027,
                billing_address='789 Pine St',
                balance=100.00,
                is_default=True
            )
            
            product = Products(supplier_id=1, name='Snack', unit_price=10.00, discount=0.00, inventory_quantity=10, category='snacks', is_available=True)
            db.session.add(product)
            db.session.commit()
            
            cart_item = CartItems(customer_id=sample_customer.user_id, product_id=product.id, quantity=2)
            db.session.add(cart_item)
            db.session.commit()
            
            result = customer_service.charge_payment_method(payment_method.id, [cart_item])
            
            assert result is True
            
            updated_pm = PaymentMethods.query.get(payment_method.id)
            assert updated_pm.balance == 80.00  
    
    def test_charge_payment_method_insufficient_funds(self, app, sample_customer):
        with app.app_context():
            customer_service = CustomerService()
            
            payment_method = customer_service.add_payment_method(
                user_id=sample_customer.user_id,
                card_number='1234567812345678',
                expiration_month=12,
                expiration_year=2027,
                billing_address='789 Pine St',
                balance=5.00,  
                is_default=True
            )
            
            product = Products(supplier_id=1, name='Expensive', unit_price=50.00, discount=0.00, inventory_quantity=10, category='snacks', is_available=True)
            db.session.add(product)
            db.session.commit()
            
            cart_item = CartItems(customer_id=sample_customer.user_id, product_id=product.id, quantity=1)
            db.session.add(cart_item)
            db.session.commit()
            
            result = customer_service.charge_payment_method(payment_method.id, [cart_item])
            
            assert result is False
