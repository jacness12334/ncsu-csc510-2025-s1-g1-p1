from app.models import *
from app.app import db
from app.services.user_service import UserService
import decimal

class DriverService:

    def __init__(self):
        self.user_service = UserService()   
    
    def validate_driver(self, user_id):
        driver = Drivers.query.get(user_id)
        if not driver:
            raise ValueError(f"Driver {user_id} not found")
        return driver
    
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
    
    def validate_vehicle_type(self, vehicle_type):
        try:
            str(vehicle_type)
            if vehicle_type not in ['car', 'bike', 'scooter', 'other']:
                raise ValueError("Vehicle type must be 'car', 'bike', 'scooter', or 'other")
            return vehicle_type
        except:
            raise ValueError("Vehicle type must be a string")

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
        
    def validate_duty_status(self, duty_status):
        try:
            str(duty_status)
            if duty_status not in ['unavailable', 'available', 'on_delivery']:
                raise ValueError("Duty status must be 'unavailable', 'available', or 'on_delivery'")
            return duty_status
        except:
            raise ValueError("Duty status must be a string")
    
    def validate_rating(self, rating):
        try:
            rating = decimal.Decimal(str(rating))
            if rating < decimal.Decimal('0.00') or rating > decimal.Decimal('5.00'):
                raise ValueError("Rating must be between 0.00 and 5.00")
            return rating
        except:
            raise ValueError("Rating must be a valid decimal number")
    
    def validate_total_deliveries(self, total_deliveries):
        try:
            total_deliveries = int(total_deliveries)
            if total_deliveries < 0:
                raise ValueError("Total deliveries cannot be negative")
            return total_deliveries
        except:
            raise ValueError("Total deliveries must be an integer")

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
    
    def update_driver_details(self, user_id, license_plate, vehicle_type, vehicle_color):
        driver = self.validate_driver(user_id=user_id)
        driver.license_plate = self.validate_license_plate(license_plate=license_plate)
        driver.vehicle_type = self.validate_vehicle_type(vehicle_type=vehicle_type)
        driver.vehicle_color = self.validate_vehicle_color(vehicle_color=vehicle_color)
        db.session.commit()
        return driver
    
    def update_driver_status(self, user_id, new_status):
        driver = self.validate_driver(user_id=user_id)
        driver.duty_status = self.validate_duty_status(duty_status=new_status)
        db.session.commit()
        return driver
    
    def get_available_drivers(self):
        return Drivers.query.filter(Drivers.duty_status == 'available').all()
    
    def get_best_available_driver(self):
        best_driver = Drivers.query.filter_by(duty_status='available').order_by(Drivers.rating.desc()).first()
        if not best_driver:
            raise ValueError("No available drivers at this time")
    
        return best_driver
    
    def try_assign_driver(self, delivery):
        try:
            driver = self.get_best_available_driver()
        except ValueError:
            return False
        delivery.driver_id = driver.user_id
        delivery.delivery_status = 'accepted'
        self.update_driver_status(user_id=delivery.driver_id, new_status='on_delivery')
        db.session.commit()
        return True
    
    def delete_driver(self, user_id):
        driver = self.validate_driver(user_id=user_id)
        db.session.delete(driver)
        db.session.commit()
        return True
    
    def complete_delivery(self, delivery_id):
        delivery = Deliveries.query.get(delivery_id)
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
    
    def rate_driver(self, delivery_id, new_rating):
        delivery = Deliveries.query.get(delivery_id)
        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        
        if delivery.delivery_status is not 'fulfilled':
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
        
    def show_completed_deliveries(self, driver_id):
        driver = self.validate_driver(driver_id)
        deliveries = Deliveries.query.filter(Deliveries.driver_id == driver.id, Deliveries.delivery_status == 'fulfilled').all()
        if not deliveries:
            raise ValueError(f"No previous deliveries found for driver {driver.id}")
        return deliveries
    
    def get_active_delivery(self, driver_id):
        driver = self.validate_driver(driver_id)
        delivery = Deliveries.query.filter_by(driver_id=driver.id).first()
        if not delivery:
            raise ValueError(f"No active delivery found for driver {driver.id}")
        return delivery

