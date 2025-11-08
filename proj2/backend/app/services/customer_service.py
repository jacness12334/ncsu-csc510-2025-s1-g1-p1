from app.models import *
from app.app import db
from app.services.user_service import UserService
from app.services.staff_service import StaffService
from app.services.driver_service import DriverService
import decimal

class CustomerService:
    """Customer service layer for accounts, payment methods, carts, showings, products, and deliveries.

    This module centralizes customer-facing business logic on top of SQLAlchemy models,
    and coordinates with user, staff, and driver services.
    """

    def __init__(self):
        """Initialize dependent services used by customer operations."""
        self.user_service = UserService()
        self.staff_service = StaffService(0)
        self.driver_service = DriverService()

    def validate_customer(self, user_id):
        """Ensure the given user_id belongs to a customer.

        Args:
            user_id: The user id to validate.

        Returns:
            Customers: The customer record associated with user_id.

        Raises:
            ValueError: If no customer exists for the given user_id.
        """
        customer = Customers.query.filter_by(user_id=user_id).first()
        if not customer:
            raise ValueError(f"Customer {user_id} not found")
        return customer

    def get_customer(self, user_id):
        """Fetch the customer record for a given user id.

        Args:
            user_id: The user id to look up.

        Returns:
            Customers: The customer record.
        """
        customer = self.validate_customer(user_id=user_id)
        return customer

    def create_customer(self, name, email, phone, birthday, password, role, default_theatre_id):
        """Create a user with the customer role and a matching customer profile.

        Args:
            name: Customer full name.
            email: Unique email address.
            phone: Unique phone number.
            birthday: Date of birth (YYYY-MM-DD or date).
            password: Plaintext password to hash and store.
            role: Must be 'customer'.
            default_theatre_id: Theatre id to set as the customer's default.

        Returns:
            Customers: The newly created customer profile.

        Raises:
            ValueError: If role is not 'customer' or the theatre id is invalid.
        """
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

    def delete_customer(self, user_id):
        """Delete a customer by removing the underlying user.

        Args:
            user_id: Customer's user id.

        Returns:
            None

        Raises:
            ValueError: If the customer does not exist.
        """
        customer = self.get_customer(user_id=user_id)
        self.user_service.delete_user(user_id=customer.user_id)

    def update_default_theatre(self, user_id, new_theatre_id):
        """Set a customer's default theatre.

        Args:
            user_id: Customer's user id.
            new_theatre_id: Theatre id to set as default.

        Returns:
            Customers: The updated customer record.

        Raises:
            ValueError: If customer or theatre is not found.
        """
        customer = self.get_customer(user_id=user_id)
        theatre = Theatres.query.filter_by(id=new_theatre_id).first()
        if not theatre:
            raise ValueError(f"Theatre {new_theatre_id} not found")

        customer.default_theatre_id = theatre.id
        db.session.commit()
        return customer

    def add_payment_method(self, user_id, card_number, expiration_month, expiration_year, billing_address, balance, is_default):
        """Add a new payment method for a customer.

        Args:
            user_id: Customer's user id.
            card_number: 16-character card number string.
            expiration_month: Integer month 1–12.
            expiration_year: Four-digit expiration year.
            billing_address: Billing address string.
            balance: Initial stored balance for testing/demo.
            is_default: Whether this card is the default.

        Returns:
            PaymentMethods: The created payment method.

        Raises:
            ValueError: If a duplicate payment method exists for the same card and expiry.
        """
        customer = self.get_customer(user_id=user_id)
        existing_payment_method = PaymentMethods.query.filter_by(
            customer_id=customer.user_id,
            card_number=card_number,
            expiration_month=expiration_month,
            expiration_year=expiration_year
        ).first()
        if existing_payment_method:
            raise ValueError("Payment method already exists for this user")

        payment_method = PaymentMethods(
            customer_id=customer.user_id,
            card_number=card_number,
            expiration_month=expiration_month,
            expiration_year=expiration_year,
            billing_address=billing_address,
            balance=balance,
            is_default=is_default
        )
        db.session.add(payment_method)
        db.session.commit()
        return payment_method

    def delete_payment_method(self, payment_method_id):
        """Remove a payment method by id.

        Args:
            payment_method_id: Payment method primary key.

        Returns:
            bool: True if deleted.

        Raises:
            ValueError: If the payment method does not exist.
        """
        payment_method = PaymentMethods.query.filter_by(id=payment_method_id).first()
        if not payment_method:
            raise ValueError("Payment method not found")

        db.session.delete(payment_method)
        db.session.commit()
        return True

    def add_funds_to_payment_method(self, payment_method_id, amount):
        """Increase a payment method's balance.

        Args:
            payment_method_id: Payment method id.
            amount: Positive decimal amount to add.

        Returns:
            PaymentMethods: The updated payment method.

        Raises:
            ValueError: If amount is not greater than zero or method not found.
        """
        if amount <= 0.00:
            raise ValueError("Amount to add must be greater than zero")

        payment_method = PaymentMethods.query.filter_by(id=payment_method_id).first()
        if not payment_method:
            raise ValueError("Payment method not found")

        payment_method.balance += decimal.Decimal(amount)
        db.session.commit()
        return payment_method

    def get_customer_payment_methods(self, customer_id):
        """List all payment methods for a customer.

        Args:
            customer_id: Customer's user id.

        Returns:
            list[PaymentMethods]: All payment methods for the customer (possibly empty).
        """
        payment_methods = PaymentMethods.query.filter(PaymentMethods.customer_id == customer_id).all()
        return payment_methods

    def create_customer_showing(self, user_id, movie_showing_id, seat_id):
        """Book a seat for a specific movie showing for a customer.

        Args:
            user_id: Customer's user id.
            movie_showing_id: Target MovieShowings id.
            seat_id: Target seat id in the showing's auditorium.

        Returns:
            CustomerShowings: The created booking record.

        Raises:
            ValueError: If customer, showing, seat is missing, or a duplicate booking exists.
        """
        customer = self.get_customer(user_id=user_id)
        movie_showing = MovieShowings.query.filter_by(id=movie_showing_id).first()
        if not movie_showing:
            raise ValueError(f"Movie Showing {movie_showing_id} not found")

        seat = Seats.query.filter_by(id=seat_id).first()
        if not seat:
            raise ValueError(f"Seat {seat_id} not found")

        existing_showing = CustomerShowings.query.filter_by(
            customer_id=customer.user_id,
            movie_showing_id=movie_showing.id,
            seat_id=seat.id
        ).first()
        if existing_showing:
            raise ValueError(f"Identical customer showing found")

        customer_showing = CustomerShowings(
            customer_id=customer.user_id,
            movie_showing_id=movie_showing.id,
            seat_id=seat.id
        )
        db.session.add(customer_showing)
        db.session.commit()
        return customer_showing

    def create_cart_item(self, customer_id, product_id, quantity):
        """Add a product to the cart or increment quantity if it already exists.

        Args:
            customer_id: Customer's user id.
            product_id: Product id to add.
            quantity: Positive integer quantity to add.

        Returns:
            CartItems: The created or updated cart item.

        Raises:
            ValueError: If quantity is invalid, product is not found, or insufficient inventory.
        """
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

    def update_cart_item(self, cart_item_id, quantity):
        """Set a cart item's quantity to a new positive value.

        Args:
            cart_item_id: Cart item primary key.
            quantity: Positive integer quantity to set.

        Returns:
            CartItems: The updated cart item.

        Raises:
            ValueError: If quantity is invalid or cart item is not found.
        """
        if quantity <= 0:
            raise ValueError("Quantity to add must be greater than zero")

        cart_item = CartItems.query.filter_by(id=cart_item_id).first()
        if not cart_item:
            raise ValueError(f"Cart item {cart_item_id} not found")

        cart_item.quantity = quantity
        db.session.commit()
        return cart_item

    def delete_cart_item(self, cart_item_id):
        """Remove a cart item by id.

        Args:
            cart_item_id: Cart item id.

        Returns:
            None

        Raises:
            ValueError: If the cart item is not found.
        """
        cart_item = CartItems.query.filter_by(id=cart_item_id).first()
        if not cart_item:
            raise ValueError(f"Cart item {cart_item_id} not found")

        db.session.delete(cart_item)
        db.session.commit()
        return

    def get_cart_items(self, customer_id):
        """Return all cart items for a customer or None if empty.

        Args:
            customer_id: Customer's user id.

        Returns:
            list[CartItems] | None: List of items if any, else None.
        """
        cart_items = CartItems.query.filter_by(customer_id=customer_id).all()
        if not cart_items:
            return None
        return cart_items

    def charge_payment_method(self, payment_method_id, total_price):
        """Charge a payment method for the given amount if sufficient funds exist.

        Args:
            payment_method_id: Payment method id to charge.
            total_price: Decimal total amount to charge.

        Returns:
            bool: True if charged; False if insufficient funds.

        Raises:
            ValueError: If the payment method is not found.
        """
        payment_method = PaymentMethods.query.filter_by(id=payment_method_id).first()
        if not payment_method:
            raise ValueError(f"Payment Method {payment_method_id} not found")

        self.validate_customer(payment_method.customer_id)

        if payment_method.balance < total_price:
            return False

        payment_method.balance -= total_price
        db.session.commit()
        return True

    def create_delivery(self, customer_showing_id, payment_method_id):
        """Create a delivery for a booked showing after validating ownership and charging.

        This links the delivery to the customer's showing, verifies the payment method
        belongs to the same customer, creates delivery items from the cart, charges the
        payment method, decrements inventory, and attempts to assign a driver and staff.

        Args:
            customer_showing_id: CustomerShowings id for the booking.
            payment_method_id: PaymentMethods id to charge.

        Returns:
            Deliveries: The created delivery.

        Raises:
            ValueError: If duplicates exist, any referenced record is missing,
                the cart is empty, or funds are insufficient.
        """
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

        # Attempt to assign driver and staff member (no-op if none available)
        self.driver_service.try_assign_driver(delivery=delivery)
        self.staff_service.try_assign_staff(theatre_id=auditorium.theatre_id, delivery=delivery)

        db.session.commit()
        return delivery

    def calculate_total_price(self, cart_items):
        """Compute the total price for a list of cart items.

        Total is computed as sum of (unit_price - discount) * quantity for each item.

        Args:
            cart_items: Iterable of CartItems to price.

        Returns:
            Decimal: The total price as a Decimal.

        Raises:
            ValueError: If a cart item is invalid or references a missing product.
        """
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

    def create_delivery_item(self, cart_item_id, delivery_id):
        """Create a DeliveryItems entry from a cart item for a pending delivery.

        Args:
            cart_item_id: Source cart item id.
            delivery_id: Target delivery id (must be pending).

        Returns:
            DeliveryItems: The created delivery-item record.

        Raises:
            ValueError: If cart item or delivery is missing, delivery not pending,
                or an identical delivery-item already exists.
        """
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

    def cancel_delivery(self, delivery_id):
        """Cancel a delivery, set driver availability, and refund the balance.

        Args:
            delivery_id: Delivery id to cancel.

        Returns:
            Deliveries: The cancelled delivery.

        Raises:
            ValueError: If the delivery is missing or already cancelled, or payment method cannot be found.
        """
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

    def rate_delivery(self, delivery_id, rating):
        """Rate a fulfilled delivery and update the driver's average rating.

        Args:
            delivery_id: Delivery id to rate.
            rating: New rating value for the driver.

        Returns:
            Deliveries: The rated delivery (unchanged id and status; rating stored on driver).

        Raises:
            ValueError: If the underlying driver service rejects the rating.
        """
        driver, delivery = self.driver_service.rate_driver(delivery_id=delivery_id, new_rating=rating)
        return delivery

    def show_all_products(self):
        """List all available products across open suppliers, sorted by supplier and name.

        Returns:
            list[Products]: All available products ordered by supplier name and product name.
        """
        products = Products.query.join(Suppliers, Products.supplier_id == Suppliers.user_id).filter(
            Products.is_available.is_(True)
        ).order_by(Suppliers.company_name.asc(), Products.name.asc()).all()
        return products

    def get_all_deliveries(self, user_id):
        """List all deliveries for a customer (newest first).

        Args:
            user_id: Customer's user id.

        Returns:
            list[Deliveries]: Deliveries linked to the customer's showings.
        """
        self.validate_customer(user_id=user_id)
        deliveries = Deliveries.query.join(
            CustomerShowings, Deliveries.customer_showing_id == CustomerShowings.id
        ).filter(
            CustomerShowings.customer_id == user_id
        ).order_by(
            Deliveries.id.desc()
        ).all()
        return deliveries

    def get_all_showings(self, user_id):
        """Return showings booked by a customer with basic presentation details.

        Each result includes movie title, seat, ISO start time, auditorium label, and theatre name.

        Args:
            user_id: Customer's user id.

        Returns:
            list[dict]: Presentation dictionaries for each showing.
        """
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

    def get_delivery_details(self, delivery_id):
        """Return expanded delivery details including items and associated theatre/movie.

        Args:
            delivery_id: Delivery id to expand.

        Returns:
            dict: A mapping containing ids, totals, timestamps, status, items, and venue/movie details.

        Raises:
            ValueError: If the delivery id is not found.
        """
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

    def get_customer_showing_id(self, user_id):
        """
        Return the first customer showing id for a given customer.

        Looks up the first CustomerShowings record for the provided customer user_id
        and returns a minimal payload containing its id. Prints the id to stdout as
        a side effect.

        Args:
            user_id (int): The customer user's id to search by.

        Returns:
            dict: A dictionary with the key "id" mapped to the showing's integer id.

        Raises:
            AttributeError: If no CustomerShowings record exists for the given user_id.
        """
        customer_showing = CustomerShowings.query.filter_by(customer_id=user_id).first()
        print(customer_showing.id)
        return {
            "id": customer_showing.id,
        }