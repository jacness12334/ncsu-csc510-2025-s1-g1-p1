from app.models import *
from app.app import db
from app.services.user_service import UserService
from app.services.staff_service import StaffService
from app.services.driver_service import DriverService
import decimal

# Business logic for customer profiles, payment methods, carts, showings, products, and deliveries.
class CustomerService:

    # Initialize services
    def __init__(self):
        self.user_service = UserService()   
        self.staff_service = StaffService(0)
        self.driver_service = DriverService()

    # Validate given user as customer
    def validate_customer(self, user_id):
        customer = Customers.query.filter_by(user_id=user_id).first()
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
        
        theatre = Theatres.query.filter_by(id=default_theatre_id).first()
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
        theatre = Theatres.query.filter_by(id=new_theatre_id).first()
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
        payment_method = PaymentMethods.query.filter_by(id=payment_method_id).first()
        if not payment_method:
            raise ValueError("Payment method not found")
        
        db.session.delete(payment_method)
        db.session.commit()
        return True
    
    # Add the given amount to the specified payment method
    def add_funds_to_payment_method(self, payment_method_id, amount):
        if amount <= 0.00:
            raise ValueError("Amount to add must be greater than zero")
        
        payment_method = PaymentMethods.query.filter_by(id=payment_method_id).first()
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
        movie_showing = MovieShowings.query.filter_by(id=movie_showing_id).first()
        if not movie_showing:
            raise ValueError(f"Movie Showing {movie_showing_id} not found")
        
        seat = Seats.query.filter_by(id=seat_id).first()
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
        product = Products.query.filter_by(id=product_id).first()
        if not product:
            raise ValueError(f"Product {product_id} not found")

        if product.inventory_quantity - quantity <= 0:
            raise ValueError(f"Product inventory is insufficient")
        
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
        
        cart_item = CartItems.query.filter_by(id=cart_item_id).first()
        if not cart_item:
            raise ValueError(f"Cart item {cart_item_id} not found")

        cart_item.quantity += quantity
        db.session.commit()
        return cart_item

    # Delete the given cart item
    def delete_cart_item(self, cart_item_id):
        cart_item = CartItems.query.filter_by(id=cart_item_id).first()
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
    def charge_payment_method(self, payment_method_id, total_price):
        payment_method = PaymentMethods.query.filter_by(id=payment_method_id).first()
        if not payment_method:
            raise ValueError(f"Payment Method {payment_method_id} not found")
        
        self.validate_customer(payment_method.customer_id)
        
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
        
        customer_showing = CustomerShowings.query.filter_by(id=customer_showing_id).first()
        if not customer_showing:
            raise ValueError(f"Customer showing {customer_showing_id} not found")
        self.validate_customer(customer_showing.customer_id)

        payment_method = PaymentMethods.query.filter_by(id=payment_method_id).first()
        if not payment_method:
            raise ValueError(f"Payment method {payment_method_id} not found")
        if payment_method.customer_id != customer_showing.customer_id:
            raise ValueError("Payment method does not belong to this customer")
        
        seat = Seats.query.filter_by(id=customer_showing.seat_id).first()
        if not seat:
            raise ValueError(f"Seat {customer_showing.seat_id} not found")
        
        auditorium = Auditoriums.query.filter_by(id=seat.auditorium_id).first()
        if not auditorium:
            raise ValueError(f"Auditorium {seat.auditorium_id} not found")
                        
        cart_items = self.get_cart_items(customer_id=customer_showing.customer_id)
        if not cart_items:
            raise ValueError(f"Cart for {customer_showing.customer_id} is empty")
        
        total_price = self.calculate_total_price(cart_items=cart_items)
        
        delivery = Deliveries(
            driver_id=None, 
            customer_showing_id=customer_showing.id, 
            payment_method_id=payment_method.id, 
            staff_id=None,
            total_price=total_price
        )
        db.session.add(delivery)
        db.session.flush()

        for item in cart_items:
            self.create_delivery_item(cart_item_id=item.id, delivery_id=delivery.id)

        was_charged = self.charge_payment_method(payment_method_id=payment_method.id, total_price=total_price)
        if not was_charged:
            db.session.rollback()
            raise ValueError("Insufficient funds")

        delivery.payment_status = 'completed'

        for item in cart_items:
            product = Products.query.filter_by(id=item.product_id).first()
            product.inventory_quantity -= item.quantity

        # Attempt to assign driver and staff member for delivery (will remain None if unavailable)
        self.driver_service.try_assign_driver(delivery=delivery)
        self.staff_service.try_assign_staff(theatre_id=auditorium.theatre_id, delivery=delivery)
        
        db.session.commit()
        return delivery
        
    # Calculate total price of cart items
    def calculate_total_price(self, cart_items):
        total_price = decimal.Decimal(0.00)
        for item in cart_items:
            if item:
                product = Products.query.filter_by(id=item.product_id).first()
                if not product:
                    raise ValueError(f"Product {item.product_id} not found")
                total_price += (product.unit_price - product.discount) * item.quantity
            else:
                raise ValueError("Invalid cart item")
        return total_price
    
    # Create delivery item from given cart item and delivery
    def create_delivery_item(self, cart_item_id, delivery_id):
        cart_item = CartItems.query.filter_by(id=cart_item_id).first()
        if not cart_item:
            raise ValueError(f"Cart item {cart_item_id} not found")
        
        delivery = Deliveries.query.filter_by(id=delivery_id).first()
        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        
        if delivery.delivery_status != 'pending':
            raise ValueError(f"Delivery must be pending to create delivery items")
        
        existing_delivery_item = DeliveryItems.query.filter_by(cart_item_id=cart_item.id, delivery_id=delivery.id).first()
        if existing_delivery_item:
            raise ValueError(f"Delivery item {existing_delivery_item.id} already exists for cart item {cart_item.id}")
        
        delivery_item = DeliveryItems(cart_item_id=cart_item.id, delivery_id=delivery.id)
        db.session.add(delivery_item)
        db.session.commit()
        return delivery_item
    
    # Cancel the given delivery
    def cancel_delivery(self, delivery_id):
        delivery = Deliveries.query.filter_by(id=delivery_id).first()
        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        
        if delivery.delivery_status == 'cancelled':
            raise ValueError(f"Delivery {delivery.id} is already cancelled")

        payment_method = PaymentMethods.query.filter_by(id=delivery.payment_method_id).first()
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
    
    # Show all active products
    def show_all_products(self):
        products = Products.query.join(Suppliers, Products.supplier_id == Suppliers.user_id).filter(Products.is_available.is_(True)).order_by(Suppliers.company_name.asc(), Products.name.asc()).all()
        return products
    
    # Get all deliveries for the given customer
    def get_all_deliveries(self, user_id):
        self.validate_customer(user_id=user_id)
        deliveries = Deliveries.query.join(CustomerShowings, Deliveries.customer_showing_id == CustomerShowings.id).filter(CustomerShowings.customer_id == user_id).order_by(Deliveries.id.desc()).all()
        return deliveries
    
    # Get all showings associated with the given customer (movie name, seat, start time, auditorium)
    def get_all_showings(self, user_id):
        self.validate_customer(user_id=user_id)
        showings = CustomerShowings.query.filter(CustomerShowings.customer_id == user_id).all()
        result = []
        for showing in showings:
            movie_showing = MovieShowings.query.filter_by(id=showing.movie_showing_id).first()
            movie = Movies.query.filter_by(id=movie_showing.movie_id).first() 
            seat = Seats.query.filter_by(id=showing.seat_id).first()
            auditorium = (
                Auditoriums.query.filter_by(id=movie_showing.auditorium_id).first()
            )
            theatre = Theatres.query.filter_by(id=auditorium.theatre_id).first()
            start_time = None
            if movie_showing and getattr(movie_showing.start_time, "isoformat", None):
                start_time = movie_showing.start_time.isoformat()
            elif movie_showing:
                start_time = str(movie_showing.start_time)
            else:
                start_time = None

            result.append({
                "id": showing.id,
                "movie_title": movie.title if movie else None,
                "seat": f"{seat.aisle} {seat.number}",
                "start_time": start_time,
                "auditorium": f"Auditorium {auditorium.number}" if auditorium else None,
                "theatre_name": theatre.name
            })
        return result
    
    # Get delivery details for given delivery
    def get_delivery_details(self, delivery_id):
        delivery = Deliveries.query.filter_by(id=delivery_id).first()
        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        delivery_items = DeliveryItems.query.filter_by(delivery_id=delivery.id).all()
        cart_items = [CartItems.query.filter_by(id=item.cart_item_id).first() for item in delivery_items]
        items = [{"name": Products.query.filter_by(id=item.product_id).first().name, "quantity": item.quantity} for item in cart_items]
        customer_showing = CustomerShowings.query.filter_by(id=delivery.customer_showing_id).first()
        showing = MovieShowings.query.filter_by(id=customer_showing.movie_showing_id).first()
        movie = Movies.query.filter_by(id=showing.movie_id).first()
        auditorium = Auditoriums.query.filter_by(id=showing.auditorium_id).first()
        theatre = Theatres.query.filter_by(id=auditorium.theatre_id).first()
        return {
            "id": delivery.id,
            "driver_id": delivery.driver_id,
            "total_price": float(delivery.total_price),
            "delivery_time": delivery.delivery_time.isoformat() if delivery.delivery_time else None,
            "delivery_status": delivery.delivery_status,
            "items": items,
            "theatre_name": theatre.name,
            "theatre_address": theatre.address,
            "movie_title": movie.title,
        }
