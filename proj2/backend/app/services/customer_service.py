from app.models import *
from app.app import db
from app.services.user_service import UserService
from app.services.staff_service import StaffService
from app.services.driver_service import DriverService
import decimal

class CustomerService:

    # Initialize services
    def __init__(self):
        self.user_service = UserService()   
        self.staff_service = StaffService()
        self.driver_service = DriverService()

    # Validate given user as customer
    def validate_customer(self, user_id):
        customer = Customers.query.get(user_id)
        if not customer:
            raise ValueError(f"Customer {user_id} not found")
        return customer
    
    # Retrieve the given customer
    def get_customer(self, user_id):
        customer = self.validate_customer(user_id=user_id)
        return customer
            
    # Create new customer user using given fields
    def create_customer(self, name, email, phone, birthday, password, role, default_theatre_id):
        if role != 'customer':
            raise ValueError("User role is not 'customer'")
        
        user = self.user_service.create_user(
            name=name, 
            email=email, 
            phone=phone, 
            birthday=birthday, 
            password=password, 
            role=role
        )
        
        theatre = Theatres.query.get(default_theatre_id)
        if not theatre:
            raise ValueError(f"Theatre {default_theatre_id} not found")
        
        customer = Customers(user_id=user.id, default_theatre_id=default_theatre_id)
        db.session.add(customer)
        db.session.commit()
        return customer
    
    # Delete the given customer
    def delete_customer(self, user_id):
        customer = self.get_customer(user_id=user_id)
        self.user_service.delete_user(user_id=customer.user_id)

    # Update customer's default theatre
    def update_default_theatre(self, user_id, new_theatre_id):
        customer = self.get_customer(user_id=user_id)
        theatre = Theatres.query.get(new_theatre_id)
        if not theatre:
            raise ValueError(f"Theatre {new_theatre_id} not found")
        
        customer.default_theatre_id = theatre.id
        db.session.commit()
        return customer
    
    # Add payment method for the given customer
    def add_payment_method(self, user_id, card_number, expiration_month, expiration_year, billing_address, balance, is_default):
        customer = self.get_customer(user_id=user_id)
        existing_payment_method = PaymentMethods.query.filter_by(customer_id=customer.user_id, card_number=card_number, expiration_month=expiration_month, expiration_year=expiration_year).first()
        if existing_payment_method:
            raise ValueError("Payment method already exists for this user")
        
        payment_method = PaymentMethods(customer_id=customer.user_id, card_number=card_number, expiration_month=expiration_month, expiration_year=expiration_year, billing_address=billing_address, balance=balance, is_default=is_default)
        db.session.add(payment_method)
        db.session.commit()
        return payment_method
    
    # Delete the given payment method
    def delete_payment_method(self, payment_method_id):
        payment_method = PaymentMethods.query.get(payment_method_id)
        if not payment_method:
            raise ValueError("Payment method not found")
        
        db.session.delete(payment_method)
        db.session.commit()
        return True
    
    # Add the given amount to the specified payment method
    def add_funds_to_payment_method(self, payment_method_id, amount):
        if amount <= 0.00:
            raise ValueError("Amount to add must be greater than zero")
        
        payment_method = PaymentMethods.query.get(payment_method_id)
        if not payment_method:
            raise ValueError("Payment method not found")
        
        payment_method.balance += decimal.Decimal(amount)
        db.session.commit()
        return payment_method
    
    # Retrieve all payment methods associated with the given customer
    def get_customer_payment_methods(self, customer_id):
        payment_methods = PaymentMethods.query.filter(PaymentMethods.customer_id == customer_id).all()
        return payment_methods

    # Create movie showing for the given customer
    def create_customer_showing(self, user_id, movie_showing_id, seat_id):
        customer = self.get_customer(user_id=user_id)
        movie_showing = MovieShowings.query.get(movie_showing_id)
        if not movie_showing:
            raise ValueError(f"Movie Showing {movie_showing_id} not found")
        
        seat = Seats.query.get(seat_id)
        if not seat:
            raise ValueError(f"Seat {seat_id} not found")
        
        existing_showing = CustomerShowings.query.filter_by(customer_id=customer.user_id, movie_showing_id=movie_showing.id, seat_id=seat.id).first()
        if existing_showing:
            raise ValueError(f"Identical customer showing found")
        
        customer_showing = CustomerShowings(customer_id=customer.user_id, movie_showing_id=movie_showing.id, seat_id=seat.id)
        db.session.add(customer_showing)
        db.session.commit()
        return customer_showing
    
    # Create cart item using the given product and customer
    def create_cart_item(self, customer_id, product_id, quantity):
        if quantity <= 0:
            raise ValueError("Quantity to add must be greater than zero")
        
        customer = self.get_customer(user_id=customer_id)
        product = Products.query.get(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")
        
        existing_item = CartItems.query.filter_by(customer_id=customer_id, product_id=product_id).first()
        if existing_item:
            existing_item.quantity += quantity
            db.session.commit()
            return existing_item
        
        cart_item = CartItems(customer_id=customer.user_id, product_id=product.id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()
        return cart_item

    # Update the given cart item's quantity
    def update_cart_item(self, cart_item_id, quantity):
        if quantity <= 0:
            raise ValueError("Quantity to add must be greater than zero")
        
        cart_item = CartItems.query.get(cart_item_id)
        if not cart_item:
            raise ValueError(f"Cart item {cart_item_id} not found")

        cart_item.quantity += quantity
        db.session.commit()
        return cart_item

    # Delete the given cart item
    def delete_cart_item(self, cart_item_id):
        cart_item = CartItems.query.get(cart_item_id)
        if not cart_item:
            raise ValueError(f"Cart item {cart_item_id} not found")

        db.session.delete(cart_item)
        db.session.commit()
        return
    
    # Retrieve all cart items for the given customer
    def get_cart_items(self, customer_id):
        cart_items = CartItems.query.filter_by(customer_id=customer_id).all()
        if not cart_items:
            return None
        return cart_items

    # Pay for the given cart items using the given payment method
    def charge_payment_method(self, payment_method_id, cart_items):
        payment_method = PaymentMethods.query.get(payment_method_id)
        if not payment_method:
            raise ValueError(f"Payment Method {payment_method_id} not found")
        
        self.validate_customer(payment_method.customer_id)
        
        if len(cart_items) == 0:
            raise ValueError(f"Cart for customer {payment_method.customer_id} is empty")
        
        total_price = self.calculate_total_price(cart_items=cart_items)
        if payment_method.balance < total_price:
            return False
        
        payment_method.balance -= total_price
        db.session.commit()
        return True

    # Create a delivery for the given customer_showing using the given payment method
    def create_delivery(self, customer_showing_id, payment_method_id):

        existing_delivery = Deliveries.query.filter(
            Deliveries.customer_showing_id == customer_showing_id,
            Deliveries.payment_method_id == payment_method_id
        ).first()
        if existing_delivery:
            raise ValueError(f"Delivery already exists for customer showing {customer_showing_id} and payment method {payment_method_id}")
        
        customer_showing = CustomerShowings.query.get(customer_showing_id)
        if not customer_showing:
            raise ValueError(f"Customer showing {customer_showing_id} not found")
        self.validate_customer(customer_showing.customer_id)

        payment_method = PaymentMethods.query.get(payment_method_id)
        if not payment_method:
            raise ValueError(f"Payment method {payment_method_id} not found")
        if payment_method.customer_id != customer_showing.customer_id:
            raise ValueError("Payment method does not belong to this customer")
        
        seat = Seats.query.get(customer_showing.seat_id)
        if not seat:
            raise ValueError(f"Seat {customer_showing.seat_id} not found")
        
        auditorium = Auditoriums.query.get(seat.auditorium_id)
        if not auditorium:
            raise ValueError(f"Auditorium {seat.auditorium_id} not found")
                        
        cart_items = self.get_cart_items(customer_id=customer_showing.customer_id)
        if not cart_items:
            raise ValueError(f"Cart for {customer_showing.customer_id} is empty")
        
        for item in cart_items:
            self.create_delivery_item(item.cart_item_id, delivery.id)
        total_price = self.charge_payment_method(payment_method_id=payment_method.id, cart_items=cart_items)
        
        delivery = Deliveries(
            driver_id=None, 
            customer_showing_id=customer_showing.id, 
            payment_method_id=payment_method.id, 
            staff_id=None,
            total_price=total_price
        )

        # Attempt to assign driver and staff member for delivery (will remain None if unavailable)
        self.driver_service.try_assign_driver(delivery=delivery)
        self.staff_service.try_assign_staff(theatre_id=auditorium.theatre_id, delivery=delivery)

        db.session.add(delivery)
        db.session.commit()
        return delivery
        
    # Calculate total price of cart items
    def calculate_total_price(self, cart_items):
        total_price = decimal.Decimal(0.00)
        for item in cart_items:
            if item:
                product = Products.query.get(item.product_id)
                if not product:
                    raise ValueError(f"Product {item.product_id} not found")
                total_price += (product.unit_price - product.discount) * item.quantity
            else:
                raise ValueError("Invalid cart item")
        return total_price
    
    # Create delivery item from given cart item and delivery
    def create_delivery_item(self, cart_item_id, delivery_id):
        cart_item = CartItems.query.get(cart_item_id)
        if not cart_item:
            raise ValueError(f"Cart item {cart_item_id} not found")
        
        delivery = Deliveries.query.get(delivery_id)
        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        
        if delivery.delivery_status != 'pending':
            raise ValueError(f"Delivery must be pending to create delivery items")
        
        existing_delivery_item = DeliveryItems.query.filter_by(cart_item_id=cart_item.id, delivery_id=delivery.id).first()
        if existing_delivery_item:
            raise ValueError(f"Delivery item {existing_delivery_item.id} already exists for cart item {cart_item.id}")
        
        delivery_item = DeliveryItems(cart_item.id, delivery.id)
        db.session.add(delivery_item)
        db.session.commit()
        return delivery_item
    
    # Complete payment for the given delivery
    def complete_delivery_payment(self, delivery_id):
        delivery = Deliveries.query.get(delivery_id)
        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        
        if delivery.delivery_status == 'cancelled':
            raise ValueError(f"Delivery {delivery_id} is cancelled")
        
        payment_method = PaymentMethods.query.get(delivery.payment_method_id)
        if not payment_method:
            raise ValueError(f"Payment method not found for {delivery.id}")
        
        was_charged = self.charge_payment_method(payment_method_id=payment_method.id)
        if not was_charged:
            raise ValueError(f"Payment method {payment_method.id} has insufficient funds")
        
        delivery.payment_status = 'completed'
        db.session.commit()
        return delivery
    
    # Cancel the given delivery
    def cancel_delivery(self, delivery_id):
        delivery = Deliveries.query.get(delivery_id)
        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        
        if delivery.delivery_status == 'cancelled':
            raise ValueError(f"Delivery {delivery.id} is already cancelled")

        payment_method = PaymentMethods.query.get(delivery.payment_method_id)
        if not payment_method:
            raise ValueError(f"Payment method not found for {delivery.id}")
        
        payment_method.balance += delivery.total_price
        self.driver_service.update_driver_status(user_id=delivery.driver_id, new_status='available')
        delivery.delivery_status = 'cancelled'
        db.session.commit()
        return delivery
        
    # Rate the given delivery
    def rate_delivery(self, delivery_id, rating):
        driver, delivery = self.driver_service.rate_driver(delivery_id=delivery_id, new_rating=rating)
        return delivery