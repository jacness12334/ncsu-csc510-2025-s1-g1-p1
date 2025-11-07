from app.models import *
from app.app import db
from app.services.user_service import UserService
import decimal

class DriverService:

    # Initialize services
    def __init__(self):
        self.user_service = UserService()   
    
    # Validate the given user as a driver
    def validate_driver(self, user_id):
        driver = Drivers.query.filter_by(user_id=user_id).first()
        if not driver:
            raise ValueError(f"Driver {user_id} not found")
        return driver
    
    # Validate the given license plate
    def validate_license_plate(self, license_plate):
        try:
            str(license_plate)
            if not license_plate.strip():
                raise ValueError("License plate is required")
            if len(license_plate) > 16:
                raise ValueError("License plate must be 16 characters or less")
            return license_plate.strip()
        except:
            raise ValueError("License plate must be a string")
    
    # Validate the given vehicle type
    def validate_vehicle_type(self, vehicle_type):
        try:
            str(vehicle_type)
            if vehicle_type not in ['car', 'bike', 'scooter', 'other']:
                raise ValueError("Vehicle type must be 'car', 'bike', 'scooter', or 'other")
            return vehicle_type
        except:
            raise ValueError("Vehicle type must be a string")

    # Validate the given vehicle color
    def validate_vehicle_color(self, vehicle_color):
        try:
            str(vehicle_color)
            if not vehicle_color.strip():
                raise ValueError("Vehicle color is required")
            if len(vehicle_color) > 16:
                raise ValueError("Vehicle color must be 16 characters or less")
            return vehicle_color.strip()
        except:
            raise ValueError("Vehicle color must be a string")
        
    # Validate the given duty status
    def validate_duty_status(self, duty_status):
        try:
            str(duty_status)
            if duty_status not in ['unavailable', 'available', 'on_delivery']:
                raise ValueError("Duty status must be 'unavailable', 'available', or 'on_delivery'")
            return duty_status
        except:
            raise ValueError("Duty status must be a string")
    
    # Validate the given rating
    def validate_rating(self, rating):
        try:
            rating = decimal.Decimal(str(rating))
            if rating < decimal.Decimal('0.00') or rating > decimal.Decimal('5.00'):
                raise ValueError("Rating must be between 0.00 and 5.00")
            return rating
        except:
            raise ValueError("Rating must be a valid decimal number")
    
    # Validate the given number of total deliveries
    def validate_total_deliveries(self, total_deliveries):
        try:
            total_deliveries = int(total_deliveries)
            if total_deliveries < 0:
                raise ValueError("Total deliveries cannot be negative")
            return total_deliveries
        except:
            raise ValueError("Total deliveries must be an integer")

    # Create driver user using given fields
    def create_driver(self, name, email, phone, birthday, password, role, license_plate, vehicle_type, vehicle_color, duty_status, rating, total_deliveries):
        if role != 'driver':
            raise ValueError("User role must be 'driver'")
        
        license_plate = self.validate_license_plate(license_plate=license_plate)
        vehicle_type = self.validate_vehicle_type(vehicle_type=vehicle_type)
        vehicle_color = self.validate_vehicle_color(vehicle_color=vehicle_color)
        duty_status = self.validate_duty_status(duty_status=duty_status)
        rating = self.validate_rating(rating=rating)
        total_deliveries = self.validate_total_deliveries(total_deliveries=total_deliveries)

        user = self.user_service.create_user(
            name=name, 
            email=email, 
            phone=phone, 
            birthday=birthday, 
            password=password, 
            role=role
        )
        
        driver = Drivers(
            user_id=user.id, 
            license_plate=license_plate, 
            vehicle_type=vehicle_type, 
            vehicle_color=vehicle_color, 
            duty_status=duty_status, 
            rating=rating, 
            total_deliveries=total_deliveries
        )

        db.session.add(driver)
        db.session.commit()

        return driver
    
    # Update the given driver using the given fields
    def update_driver_details(self, user_id, license_plate, vehicle_type, vehicle_color):
        driver = self.validate_driver(user_id=user_id)
        # Make sure plate is unique
        driver.license_plate = self.validate_license_plate(license_plate=license_plate)
        driver.vehicle_type = self.validate_vehicle_type(vehicle_type=vehicle_type)
        driver.vehicle_color = self.validate_vehicle_color(vehicle_color=vehicle_color)
        db.session.commit()
        return driver
    
    # Update the duty status of the given driver
    def update_driver_status(self, user_id, new_status):
        driver = self.validate_driver(user_id=user_id)
        driver.duty_status = self.validate_duty_status(duty_status=new_status)
        db.session.commit()
        return driver
    
    # Retrieve list of available drivers
    def get_available_drivers(self):
        return Drivers.query.filter(Drivers.duty_status == 'available').all()
    
    # Retrieve the best available driver
    def get_best_available_driver(self):
        best_driver = Drivers.query.filter_by(duty_status='available').order_by(Drivers.rating.desc()).first()
        return best_driver
    
    # Attempt to assign a driver to the given delivery
    def try_assign_driver(self, delivery):
        if not delivery:
            raise ValueError("Delievry not found")
        driver = self.get_best_available_driver()
        if not driver:
            return False
        delivery.driver_id = driver.user_id
        delivery.delivery_status = 'accepted'
        self.update_driver_status(user_id=delivery.driver_id, new_status='on_delivery')
        return True
    
    # Delete the given driver
    def delete_driver(self, user_id):
        driver = self.validate_driver(user_id=user_id)
        self.user_service.delete_user(driver.user_id)
        return True
    
    # Mark the given delivery as completed
    def complete_delivery(self, delivery_id):
        delivery = Deliveries.query.filter_by(id=delivery_id).first()
        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        
        if delivery.delivery_status != 'accepted':
            raise ValueError("Delivery must be accepted to be completed")
        
        driver = self.validate_driver(user_id=delivery.driver_id)
        if not driver:
            raise ValueError("Driver not found for this delivery")
        
        if driver.duty_status != 'on_delivery':
            raise ValueError("Driver is not currently on a delivery")
        
        driver.total_deliveries += 1
        delivery.delivery_status = 'delivered'
        driver.duty_status = 'available'
        db.session.commit()
        return delivery
    
    # Rate the driver of the diven delivery
    def rate_driver(self, delivery_id, new_rating):
        delivery = Deliveries.query.filter_by(id=delivery_id).first()
        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        
        if delivery.delivery_status != 'fulfilled':
            raise ValueError("Can only rate fulfilled deliveries")
        
        if delivery.is_rated:
            raise ValueError(f"Delivery {delivery_id} has already been rated")
        
        driver = self.validate_driver(user_id=delivery.driver_id)
        if not driver:
            raise ValueError("Driver not found for this delivery")
        
        new_rating = self.validate_rating(new_rating)

        if driver.total_deliveries == 0:
            driver.rating = new_rating
        else:
            total_rating = driver.rating * driver.total_deliveries + new_rating
            driver.rating = total_rating / (driver.total_deliveries + 1)
        
        delivery.is_rated = True
        db.session.commit()
        return driver, delivery
        
    # Show past deliveries for the given driver
    def show_completed_deliveries(self, driver_id):
        driver = self.validate_driver(driver_id)
        deliveries = Deliveries.query.filter(Deliveries.driver_id == driver.id, Deliveries.delivery_status == 'fulfilled').all()
        if not deliveries:
            raise ValueError(f"No previous deliveries found for driver {driver.id}")
        return deliveries
    
    # Get the given driver's active delivery
    def get_active_delivery(self, driver_id):
        driver = self.validate_driver(driver_id)
        delivery = Deliveries.query.filter_by(driver_id=driver.id).first()
        if not delivery:
            raise ValueError(f"No active delivery found for driver {driver.id}")
        return delivery

