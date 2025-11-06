from app.models import *
from app.app import db
from sqlalchemy import or_

config_name = 'development'
app = get_app(config_name)

with app.app_context():
    pass

class DriverService:

    def __init__(self, user_id):
        self.user_id = user_id
    
    def validate_driver(self):
        driver = Drivers.query.filter_by(user_id=self.user_id).first()
        if not driver:
            raise ValueError(f"Driver {self.user_id} not found")
        return driver
    
    def get_driver(self):
        driver = self.validate_driver()
        return driver

    def update_driver_info(self, license_plate, vehicle_type, vehicle_color):
        driver = self.validate_driver()
        
        valid_vehicle_types = ['car', 'bike', 'scooter', 'other']
        if vehicle_type not in valid_vehicle_types:
            raise ValueError(f"Invalid vehicle type. Must be one of: {', '.join(valid_vehicle_types)}")

        driver.license_plate = license_plate
        driver.vehicle_type = vehicle_type
        driver.vehicle_color = vehicle_color
        db.session.commit()
        return driver

    def set_duty_status(self, duty_status):
        driver = self.validate_driver()
        
        valid_statuses = ['unavailable', 'available', 'on_delivery']
        if duty_status not in valid_statuses:
            raise ValueError(f"Invalid duty status. Must be one of: {', '.join(valid_statuses)}")

        driver.duty_status = duty_status
        db.session.commit()
        return driver
    
    def get_assigned_deliveries(self):
        driver = self.validate_driver()
        
        active_statuses = ['accepted', 'ready_for_pickup', 'in_transit', 'delivered']
        
        deliveries = Deliveries.query.filter(
            Deliveries.driver_id == driver.user_id,
            Deliveries.delivery_status.in_(active_statuses)
        ).all()

        return deliveries

    def get_delivery_history(self):
        driver = self.validate_driver()

        history_statuses = ['fulfilled', 'cancelled']

        deliveries = Deliveries.query.filter(
            Deliveries.driver_id == driver.user_id,
            Deliveries.delivery_status.in_(history_statuses)
        ).order_by(Deliveries.delivery_time.desc()).all()

        return deliveries

    def update_delivery_status(self, delivery_id, delivery_status):
        driver = self.validate_driver()
        
        delivery = Deliveries.query.filter_by(id=delivery_id, driver_id=driver.user_id).first()
        
        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found or not assigned to driver {driver.user_id}")
        
        current_status = delivery.delivery_status
        
        if delivery_status == 'in_transit':
            if current_status != 'ready_for_pickup':
                raise ValueError(f"Cannot transition from '{current_status}' to 'in_transit'. Delivery must be 'ready_for_pickup'.")
            
            if driver.duty_status != 'on_delivery':
                driver.duty_status = 'on_delivery'

        elif delivery_status == 'delivered':
            if current_status != 'in_transit':
                raise ValueError(f"Cannot transition from '{current_status}' to 'delivered'. Delivery must be 'in_transit'.")
                
            active_deliveries_count = Deliveries.query.filter(
                Deliveries.driver_id == driver.user_id,
                Deliveries.delivery_status.in_(['ready_for_pickup', 'in_transit']) 
            ).count()

            if active_deliveries_count == 1:
                 driver.duty_status = 'available'
        
        else:
            valid_driver_statuses = ['in_transit', 'delivered']
            raise ValueError(f"Invalid delivery status transition. Driver can only set status to: {', '.join(valid_driver_statuses)}.")
            
        delivery.delivery_status = delivery_status
        db.session.commit()
        return delivery
    
    def assign_delivery_to_driver(self, delivery_id):
        delivery = Deliveries.query.get(delivery_id)

        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        
        if delivery.delivery_status != 'pending' and delivery.delivery_status != 'accepted':
            raise ValueError(f"Delivery is already in status '{delivery.delivery_status}' and cannot be auto-assigned.")
        
        best_driver = Drivers.query.filter(
            Drivers.duty_status == 'available'
        ).order_by(
            Drivers.rating.desc()
        ).first()

        if not best_driver:
            raise ValueError("No available drivers found to assign the delivery")

        delivery.driver_id = best_driver.user_id
        delivery.delivery_status = 'accepted'
        
        best_driver.duty_status = 'on_delivery'

        db.session.commit()
        return best_driver, delivery
    
    def update_driver_rating(self, driver_user_id, new_score):
        driver = Drivers.query.filter_by(user_id=driver_user_id).first()
        if not driver:
            raise ValueError(f"Driver {driver_user_id} not found")
        
        try:
            new_score = float(new_score)
        except ValueError:
            raise ValueError("New score must be a number")
        
        if not (0.00 <= new_score <= 5.00):
            raise ValueError("Rating must be between 0.00 and 5.00")

        current_rating = float(driver.rating)
        total_ratings = driver.total_deliveries

        if total_ratings == 0:
            new_average = new_score
        else:
            total_points = current_rating * total_ratings
            new_average = (total_points + new_score) / (total_ratings + 1)

        driver.rating = round(new_average, 2)
        driver.total_deliveries += 1
        db.session.commit()
        return driver

