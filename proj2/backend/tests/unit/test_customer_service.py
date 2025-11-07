import pytest
from app.services.customer_service import CustomerService
from app.models import Theatres, PaymentMethods, CartItems, Seats
from app.app import db
from decimal import Decimal


class TestCustomerService:
        
    def test_create_customer_success(self, app, sample_theatre):
        with app.app_context():
            customer_service = CustomerService()            
            customer = customer_service.create_customer(
                name='Customer',
                email='customer@example.com',
                phone='5555555555',
                birthday='1990-05-05',
                password='password123',
                role='customer',
                default_theatre_id=sample_theatre
            )
            
            assert customer is not None
            assert customer.user_id is not None
            assert customer.default_theatre_id == sample_theatre
    
    def test_create_customer_wrong_role(self, app, sample_theatre):
        with app.app_context():
            svc = CustomerService()
            with pytest.raises(ValueError, match="User role is not 'customer'"):
                svc.create_customer(
                    name='Wrong Role',
                    email='wrong@example.com',
                    phone='5551111111',
                    birthday='1990-01-01',
                    password='password123',
                    role='driver',
                    default_theatre_id=sample_theatre
                )
    
    def test_create_customer_duplicate_email(self, app, sample_customer, sample_theatre):
        with app.app_context():
            svc = CustomerService()
            with pytest.raises(ValueError, match="Email already in use"):
                svc.create_customer(
                    name='Test User',
                    email='test@example.com',
                    phone='5551231234',
                    birthday='1990-01-01',
                    password='password123',
                    role='customer',
                    default_theatre_id=sample_theatre
                )

    def test_create_customer_duplicate_phone(self, app, sample_customer, sample_theatre):
        with app.app_context():
            svc = CustomerService()
            with pytest.raises(ValueError, match="Phone already in use"):
                svc.create_customer(
                    name='Test User',
                    email='new_test@example.com',
                    phone='1234567890',
                    birthday='1990-01-01',
                    password='password123',
                    role='customer',
                    default_theatre_id=sample_theatre
                )

    def test_get_customer_success(self, app, sample_customer):
        with app.app_context():
            svc = CustomerService()
            customer = svc.get_customer(sample_customer)
            assert customer is not None
            assert customer.user_id == sample_customer
    
    def test_get_customer_not_found(self, app):
        with app.app_context():
            svc = CustomerService()
            with pytest.raises(ValueError, match="Customer .* not found"):
                svc.get_customer(99999)
    
    def test_delete_customer_success(self, app, sample_customer):
        with app.app_context():
            svc = CustomerService()
            user_id = sample_customer
            svc.delete_customer(user_id)
            with pytest.raises(ValueError, match="Customer .* not found"):
                svc.get_customer(user_id)
    
    def test_update_default_theatre_success(self, app, sample_customer, sample_theatre):
        with app.app_context():
            svc = CustomerService()
            new_theatre = Theatres(name='New Cinema', address='456 Oak St', phone='5559999999', is_open=True)
            db.session.add(new_theatre)
            db.session.commit()
            updated = svc.update_default_theatre(
                user_id=sample_customer,
                new_theatre_id=new_theatre.id
            )
            assert updated.default_theatre_id == new_theatre.id
    
    def test_update_default_theatre_not_found(self, app, sample_customer):
        with app.app_context():
            svc = CustomerService()
            with pytest.raises(ValueError, match="Theatre .* not found"):
                svc.update_default_theatre(
                    user_id=sample_customer,
                    new_theatre_id=99999
                )
        
    def test_add_payment_method_success(self, app, sample_customer):
        with app.app_context():
            svc = CustomerService()
            pm = svc.add_payment_method(
                user_id=sample_customer,
                card_number='1234567812345678',
                expiration_month=12,
                expiration_year=2027,
                billing_address='789 Pine St',
                balance=100.00,
                is_default=True
            )
            assert pm is not None
            assert pm.customer_id == sample_customer
            assert pm.card_number == '1234567812345678'
            assert float(pm.balance) == 100.00
    
    def test_add_payment_method_duplicate(self, app, sample_customer):
        with app.app_context():
            svc = CustomerService()
            svc.add_payment_method(
                user_id=sample_customer,
                card_number='1234567812345678',
                expiration_month=12,
                expiration_year=2027,
                billing_address='789 Pine St',
                balance=100.00,
                is_default=True
            )
            with pytest.raises(ValueError, match="Payment method already exists for this user"):
                svc.add_payment_method(
                    user_id=sample_customer,
                    card_number='1234567812345678',
                    expiration_month=12,
                    expiration_year=2027,
                    billing_address='Different Address',
                    balance=50.00,
                    is_default=False
                )
    
    def test_get_customer_payment_methods_success(self, app, sample_customer):
        with app.app_context():
            svc = CustomerService()
            svc.add_payment_method(
                user_id=sample_customer,
                card_number='1111222233334444',
                expiration_month=6,
                expiration_year=2026,
                billing_address='Address 1',
                balance=100.00,
                is_default=True
            )
            svc.add_payment_method(
                user_id=sample_customer,
                card_number='5555666677778888',
                expiration_month=9,
                expiration_year=2028,
                billing_address='Address 2',
                balance=200.00,
                is_default=False
            )
            methods = svc.get_customer_payment_methods(sample_customer)
            assert isinstance(methods, list)
            assert len(methods) == 2
    
    def test_get_customer_payment_methods_none_returns_empty(self, app, sample_customer):
        with app.app_context():
            svc = CustomerService()
            methods = svc.get_customer_payment_methods(sample_customer)
            assert isinstance(methods, list)
            assert len(methods) == 0
    
    def test_delete_payment_method_success(self, app, sample_customer):
        with app.app_context():
            svc = CustomerService()
            pm = svc.add_payment_method(
                user_id=sample_customer,
                card_number='1234567812345678',
                expiration_month=12,
                expiration_year=2027,
                billing_address='789 Pine St',
                balance=100.00,
                is_default=True
            )
            result = svc.delete_payment_method(pm.id)
            assert result is True
            remaining = svc.get_customer_payment_methods(sample_customer)
            assert remaining == []
    
    def test_delete_payment_method_not_found(self, app):
        with app.app_context():
            svc = CustomerService()
            with pytest.raises(ValueError, match="Payment method not found"):
                svc.delete_payment_method(99999)
    
    def test_add_funds_to_payment_method_success(self, app, sample_customer):
        with app.app_context():
            svc = CustomerService()
            pm = svc.add_payment_method(
                user_id=sample_customer,
                card_number='1234567812345678',
                expiration_month=12,
                expiration_year=2027,
                billing_address='789 Pine St',
                balance=100.00,
                is_default=True
            )
            updated_pm = svc.add_funds_to_payment_method(pm.id, 50.00)
            assert float(updated_pm.balance) == 150.00
    
    def test_add_funds_invalid_amount(self, app, sample_customer):
        with app.app_context():
            svc = CustomerService()
            pm = svc.add_payment_method(
                user_id=sample_customer,
                card_number='1234567812345678',
                expiration_month=12,
                expiration_year=2027,
                billing_address='789 Pine St',
                balance=100.00,
                is_default=True
            )
            with pytest.raises(ValueError, match="Amount to add must be greater than zero"):
                svc.add_funds_to_payment_method(pm.id, 0.00)
            with pytest.raises(ValueError, match="Amount to add must be greater than zero"):
                svc.add_funds_to_payment_method(pm.id, -10.00)
        
    def test_create_cart_item_success(self, app, sample_customer, sample_product):
        with app.app_context():
            svc = CustomerService()
            item = svc.create_cart_item(
                customer_id=sample_customer,
                product_id=sample_product,
                quantity=2
            )
            assert item is not None
            assert item.customer_id == sample_customer
            assert item.product_id == sample_product
            assert item.quantity == 2
    
    def test_create_cart_item_existing_increases_quantity(self, app, sample_customer, sample_product):
        with app.app_context():
            svc = CustomerService()
            i1 = svc.create_cart_item(
                customer_id=sample_customer,
                product_id=sample_product,
                quantity=1
            )
            i2 = svc.create_cart_item(
                customer_id=sample_customer,
                product_id=sample_product,
                quantity=2
            )
            assert i1.id == i2.id
            assert i2.quantity == 3
    
    def test_create_cart_item_invalid_quantity(self, app, sample_customer, sample_product):
        with app.app_context():
            svc = CustomerService()
            with pytest.raises(ValueError, match="Quantity to add must be greater than zero"):
                svc.create_cart_item(
                    customer_id=sample_customer,
                    product_id=sample_product,
                    quantity=0
                )

    def test_update_cart_item_success(self, app, sample_customer, sample_product):
        with app.app_context():
            svc = CustomerService()
            item = svc.create_cart_item(
                customer_id=sample_customer,
                product_id=sample_product,
                quantity=1
            )
            updated = svc.update_cart_item(item.id, 3)
            assert updated.quantity == 4  

    def test_update_cart_item_invalid_quantity(self, app, sample_customer, sample_product):
        with app.app_context():
            svc = CustomerService()
            item = svc.create_cart_item(
                customer_id=sample_customer,
                product_id=sample_product,
                quantity=1
            )
            with pytest.raises(ValueError, match="Quantity to add must be greater than zero"):
                svc.update_cart_item(item.id, 0)
    
    def test_delete_cart_item_success(self, app, sample_customer, sample_product):
        with app.app_context():
            svc = CustomerService()
            item = svc.create_cart_item(
                customer_id=sample_customer,
                product_id=sample_product,
                quantity=1
            )
            svc.delete_cart_item(item.id)
            deleted = CartItems.query.filter_by(id=item.id).first()
            assert deleted is None

    def test_get_cart_items_empty_returns_none(self, app, sample_customer):
        with app.app_context():
            svc = CustomerService()
            items = svc.get_cart_items(sample_customer)
            assert items is None
        
    def test_calculate_total_price_success(self, app, sample_customer, sample_product, sample_product_extra):
        with app.app_context():
            svc = CustomerService()    
            svc.create_cart_item(
                customer_id=sample_customer,
                product_id=sample_product,
                quantity=2
            )
            svc.create_cart_item(
                customer_id=sample_customer,
                product_id=sample_product_extra,
                quantity=3
            )
            cart_items = svc.get_cart_items(sample_customer)
            total = svc.calculate_total_price(cart_items)
            assert float(total) == 20.95
        
    def test_create_customer_showing_success(self, app, sample_customer, sample_auditorium, sample_showing):
        with app.app_context():
            svc = CustomerService()
            seat = Seats(aisle='A', number=1, auditorium_id=sample_auditorium)
            db.session.add(seat)
            db.session.commit()
            cs = svc.create_customer_showing(
                user_id=sample_customer,
                movie_showing_id=sample_showing,
                seat_id=seat.id
            )
            assert cs is not None
            assert cs.customer_id == sample_customer
            assert cs.movie_showing_id == sample_showing
            assert cs.seat_id == seat.id
    
    def test_charge_payment_method_success(self, app, sample_customer, sample_product, sample_payment_method):
        with app.app_context():
            svc = CustomerService()
            cart_item = CartItems(customer_id=sample_customer, product_id=sample_product, quantity=2)
            db.session.add(cart_item)
            db.session.commit()
            total = svc.calculate_total_price([cart_item])
            result = svc.charge_payment_method(sample_payment_method, total)
            assert result is True
            pm = PaymentMethods.query.filter_by(id=sample_payment_method).first()
            assert float(pm.balance) == 100.00 - float(total)
    
    def test_charge_payment_method_insufficient_funds(self, app, sample_customer, sample_product, sample_payment_method_low_balance):
        with app.app_context():
            svc = CustomerService()
            cart_item = CartItems(customer_id=sample_customer, product_id=sample_product, quantity=1)
            db.session.add(cart_item)
            db.session.commit()
            total = svc.calculate_total_price([cart_item])
            result = svc.charge_payment_method(sample_payment_method_low_balance, total)
            assert result is False

    def test_rate_delivery_success(self, app, sample_fulfilled_delivery):
        with app.app_context():
            svc = CustomerService()
            delivery = svc.rate_delivery(delivery_id=sample_fulfilled_delivery, rating=5)
            assert delivery.id == sample_fulfilled_delivery

    def test_cancel_delivery_success_refunds_and_cancels(self, app, sample_delivery):
        with app.app_context():
            from app.models import Deliveries
            svc = CustomerService()
            delivery_before = Deliveries.query.filter_by(id=sample_delivery).first()
            pm_before = PaymentMethods.query.filter_by(id=delivery_before.payment_method_id).first()
            old_balance = float(pm_before.balance)
            refunded_delivery = svc.cancel_delivery(sample_delivery)
            assert refunded_delivery.delivery_status == 'cancelled'
            pm_after = PaymentMethods.query.filter_by(id=refunded_delivery.payment_method_id).first()
            assert float(pm_after.balance) == old_balance + float(refunded_delivery.total_price)

    def test_get_customer_showings_success(self, app, sample_customer, sample_customer_showing):
        from app.models import CustomerShowings
        with app.app_context():
            svc = CustomerService()
            showings = svc.get_all_showings(sample_customer)

            assert isinstance(showings, list)
            assert len(showings) == 1
            showing = showings[0]

            assert "movie_title" in showing
            assert "start_time" in showing
            assert "auditorium" in showing
            assert "seat" in showing
            assert 'theatre_name' in showing
            sample_showing = CustomerShowings.query.filter_by(id=sample_customer_showing).first()
            assert showing["id"] == sample_customer_showing
    
    def test_get_delivery_details_valid(self, app, sample_delivery):
        with app.app_context():
            svc = CustomerService()
            details = svc.get_delivery_details(sample_delivery)
            assert isinstance(details, dict)
            assert len(details) == 9
            assert "id" in details
            assert "driver_id" in details
            assert "total_price" in details
            assert "delivery_time" in details
            assert "delivery_status" in details
            assert "items" in details
            assert "theatre_name" in details
            assert "theatre_address" in details
            assert "movie_title" in details
            assert details["id"] == sample_delivery

    def test_get_delivery_details_invalid(self, app):
        from app.models import Deliveries
        with app.app_context():
            svc = CustomerService()
            delivery = Deliveries(
                customer_showing_id=123,   
                payment_method_id=456,    
                driver_id=None,
                staff_id=None,
                total_price=Decimal("19.99"),
                payment_status="pending",
                delivery_status="pending",
            )
            with pytest.raises(ValueError, match=f"Delivery {delivery.id} not found"):
                details = svc.get_delivery_details(delivery.id)
