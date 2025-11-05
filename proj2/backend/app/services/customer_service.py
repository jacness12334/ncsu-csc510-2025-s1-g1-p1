from models import *
from app import db
from services.user_service import UserService

user_service = UserService()

class CustomerService:   

    def validate_customer(self, user_id):
        user = Customers.query.get(user_id)
        if not user:
            raise ValueError(f"Customer {user_id} not found")
        return user
            
    def create_customer(self, name, email, phone, birthday, password, role, default_theatre_id):
        if role != 'customer':
            raise ValueError("User role is not 'customer'")
        
        user = user_service.create_user(name=name, email=email, phone=phone, birthday=birthday, password=password, role=role)
        
        try:
            record_exists = self.get_customer(user_id=user.id)
            raise ValueError(f"Customer record already exists for user {record_exists.user.id}")
        except:
            customer = Customers(user_id=user.id, default_theatre_id=default_theatre_id)
            db.session.add(customer)
            db.session.commit()
            return customer
    
    def delete_customer(self, user_id):
        customer = self.get_customer(user_id=user_id)
        user_service.delete_user(user_id=customer.user_id)

    def get_customer(self, user_id):
        customer = self.validate_customer(user_id=user_id)
        return customer

    def update_default_theatre(self, user_id, new_theatre_id):
        customer = self.get_customer(user_id=user_id)
        theatre = Theatres.query.get(theatre_id=new_theatre_id)
        if not theatre:
            raise ValueError(f"Theatre {new_theatre_id} not found")
        
        customer.default_theatre_id = theatre.id
        db.session.commit()
        return customer
    
    def add_payment_method(self, user_id, card_number, expiration_month, expiration_year, billing_address, balance, is_default):
        customer = self.get_customer(user_id=user_id)
        existing_payment_method = PaymentMethods.query.filter_by(customer_id=customer.user_id, card_number=card_number, expiration_month=expiration_month, expiration_year=expiration_year).first()
        if existing_payment_method:
            raise ValueError("Payment method already exists for this user")
        
        payment_method = PaymentMethods(customer_id=customer.user_id, card_number=card_number, expiration_month=expiration_month, expiration_year=expiration_year, billing_address=billing_address, balance=balance, is_default=is_default)
        db.session.add(payment_method)
        db.session.commit()
        return payment_method
    
    def delete_payment_method(self, payment_method_id):
        payment_method = PaymentMethods.query.get(payment_method_id)
        if not payment_method:
            raise ValueError("Payment method not found")
        
        db.session.delete(payment_method)
        db.session.commit()
        return True
    
    def add_funds_to_payment_method(self, payment_method_id, amount):
        if amount <= 0.00:
            raise ValueError("Amount to add must be greater than zero")
        
        payment_method = PaymentMethods.query.get(payment_method_id)
        if not payment_method:
            raise ValueError("Payment method not found")
        
        payment_method.balance += amount
        db.session.commit()
        return payment_method
    
    def get_customer_payment_methods(self, customer_id):
        payment_methods = PaymentMethods.query.filter(PaymentMethods.customer_id == customer_id).all()
        if not payment_methods:
            raise ValueError(f"Payment methods for customer {customer_id} not found")
        
        return payment_methods

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
    
    def create_cart_item(self, customer_id, product_id, quantity):
        if quantity <= 0:
            raise ValueError("Quantity to add must be greater than zero")
        
        customer = self.get_customer(customer_id)
        product = Products.query.get(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")
        
        existing_item = CartItems.query.filter_by(customer_id=customer_id, product_id=product_id).first()
        if existing_item:
            existing_item.quantity += quantity
            return existing_item
        
        cart_item = CartItems(customer_id=customer.user_id, product_id=product.id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()
        return cart_item

    def update_cart_item(self, cart_item_id, quantity):
        if quantity <= 0:
            raise ValueError("Quantity to add must be greater than zero")
        
        cart_item = CartItems.query.get(cart_item_id)
        if not cart_item:
            raise ValueError(f"Cart item {cart_item_id} not found")

        cart_item.quantity += quantity
        db.session.commit()
        return cart_item

    def delete_cart_item(self, cart_item_id):
        cart_item = CartItems.query.get(cart_item_id)
        if not cart_item:
            raise ValueError(f"Cart item {cart_item_id} not found")

        db.session.delete(cart_item)
        db.session.commit()
        return

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

    def create_delivery(self, driver_id, customer_showing_id, payment_method_id, staff_id):
        driver = Drivers.query.get(driver_id)
        if not driver:
            raise ValueError(f"Driver {driver_id} not found")
        
        customer_showing = CustomerShowings.query.get(customer_showing_id)
        if not customer_showing:
            raise ValueError(f"Customer showing {customer_showing_id} not found")
        self.validate_customer(customer_showing.customer_id)

        payment_method = PaymentMethods.get(payment_method_id)
        if not payment_method:
            raise ValueError(f"Payment method {payment_method_id} not found")
        
        staff = Staff.query.get(staff_id)
        if not staff:
            raise ValueError(f"Staff member {staff_id} not found")
        
        existing_delivery = Deliveries.query.filter_by(driver_id, customer_showing_id).first()
        if existing_delivery:
            raise ValueError(f"Delivery already exists for driver {driver_id} and customer showing {customer_showing_id}")
        
        cart_items = CartItems.query.filter(CartItems.customer_id == customer_showing.customer_id).all()
        if not cart_items:
            raise ValueError(f"Cart for {customer_showing.customer_id} is empty")
        
        delivery = Deliveries(driver_id=driver.user_id, customer_showing_id=customer_showing.id, payment_method_id=payment_method.id, staff_id=staff.user_id, total_price=0.00)
        
        for item in cart_items:
            self.create_delivery_item(item.cart_item_id, delivery.id)

        total_price = self.charge_payment_method(payment_method.id)
        if not total_price:
            db.session.delete(delivery)
            db.session.commit()
            return None
        
        delivery.total_price = total_price
        db.session.add(delivery)
        db.session.commit()
        return delivery
            
    def calculate_total_price(self, cart_items):
        total_price = 0.00
        for item in cart_items:
            if item:
                product = Products.query.get(item.product_id)
                if not product:
                    raise ValueError(f"Product {item.product_id} not found")
                total_price += (product.unit_price - product.discount) * item.quantity
            else:
                raise ValueError("Invalid cart item")
        return total_price
    
    def create_delivery_item(self, cart_item_id, delivery_id):
        cart_item = CartItems.query.get(cart_item_id)
        if not cart_item:
            raise ValueError(f"Cart item {cart_item_id} not found")
        
        delivery = Deliveries.query.get(delivery_id)
        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        
        if delivery.delivery_status == 'cancelled':
            raise ValueError(f"Delivery {delivery.id} is cancelled")
        
        existing_delivery_item = DeliveryItems.query.filter_by(cart_item_id=cart_item.id, delivery_id=delivery.id).first()
        if existing_delivery_item:
            raise ValueError(f"Delivery item {existing_delivery_item.id} already exists for cart item {cart_item.id}")
        
        delivery_item = DeliveryItems(cart_item.id, delivery.id)
        db.session.add(delivery_item)
        db.session.commit()
        return delivery_item
    
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
    
    def cancel_delivery(self, delivery_id):
        delivery = Deliveries.query.get(delivery_id)
        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        
        if delivery.delivery_status == 'cancelled':
            raise ValueError(f"Delivery {delivery.id} is cancelled")

        payment_method = PaymentMethods.query.get(delivery.payment_method_id)
        if not payment_method:
            raise ValueError(f"Payment method not found for {delivery.id}")
        
        payment_method.balance += delivery.total_price
        delivery.delivery_status = 'cancelled'
        db.session.commit()
        return delivery


