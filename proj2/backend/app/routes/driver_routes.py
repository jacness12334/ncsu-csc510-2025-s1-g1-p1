from flask import Blueprint, request, jsonify
from app.models import Users, Drivers, Deliveries
from app.app import db
from app.services.driver_service import DriverService
from datetime import datetime

driver_bp = Blueprint("driver", __name__, url_prefix="/api")

def get_user_id():
    data = request.json
    return data.get('user_id')

def delivery_to_dict(delivery):
    return {
        "id": delivery.id,
        "driver_id": delivery.driver_id,
        "customer_showing_id": delivery.customer_showing_id,
        "payment_method_id": delivery.payment_method_id,
        "staff_id": delivery.staff_id,
        "payment_status": delivery.payment_status,
        "total_price": float(delivery.total_price),
        "delivery_time": delivery.delivery_time.isoformat() if delivery.delivery_time else None,
        "delivery_status": delivery.delivery_status
    }


# --- Admin/Staff Routes for Driver Management ---
@driver_bp.route('/driver', methods=['POST'])
def create_driver():
    try:
        data = request.json
        service = DriverService()
        
        required_fields = ['name', 'email', 'phone', 'birthday', 'password', 'license_plate', 'vehicle_type', 'vehicle_color', 'duty_status', 'rating', 'total_deliveries']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required user or driver fields"}), 400
        
        driver = service.create_driver(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            birthday=data['birthday'],
            password=data['password'],
            role='driver',
            license_plate=data['license_plate'],
            vehicle_type=data['vehicle_type'],
            vehicle_color=data['vehicle_color'],
            duty_status=data['duty_status'],
            rating=data['rating'],
            total_deliveries=data['total_deliveries']
        )
        return jsonify({"message": "Driver created successfully", "user_id": driver.user_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

@driver_bp.route('/driver/<int:driver_user_id>', methods=['DELETE'])
def delete_driver(driver_user_id):
    try:
        service = DriverService()
        service.delete_driver(driver_user_id)
        return jsonify({"message": f"Driver {driver_user_id} deleted successfully"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500


# --- Driver Information and Status Update (By Driver or Admin) ---
@driver_bp.route('/driver/<int:driver_user_id>', methods=['GET'])
def get_driver_info(driver_user_id):
    try:
        service = DriverService()
        driver = service.validate_driver(driver_user_id)
        user = Users.query.get(driver.user_id)

        return jsonify({
            "driver": {
                "user_id": driver.user_id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "license_plate": driver.license_plate,
                "vehicle_type": driver.vehicle_type,
                "vehicle_color": driver.vehicle_color,
                "duty_status": driver.duty_status,
                "rating": float(driver.rating),
                "total_deliveries": driver.total_deliveries
            }
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

@driver_bp.route('/driver/<int:driver_user_id>', methods=['PUT'])
def update_driver_details(driver_user_id):
    try:
        data = request.json
        service = DriverService()
        required_fields = ['license_plate', 'vehicle_type', 'vehicle_color']
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields: license_plate, vehicle_type, vehicle_color"}), 400
        
        driver = service.update_driver_details(
            user_id=driver_user_id,
            license_plate=data['license_plate'],
            vehicle_type=data['vehicle_type'],
            vehicle_color=data['vehicle_color']
        )
        return jsonify({"message": "Driver details updated", "user_id": driver.user_id}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

@driver_bp.route('/driver/<int:driver_user_id>/status', methods=['PUT'])
def update_driver_status(driver_user_id):
    try:
        data = request.json
        service = DriverService()
        if 'new_status' not in data:
            return jsonify({"error": "Missing new_status field"}), 400
        
        driver = service.update_driver_status(driver_user_id, data['new_status'])
        return jsonify({
            "message": f"Duty status updated to {driver.duty_status}",
            "duty_status": driver.duty_status
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500


# --- Delivery Assignment and Rating ---
@driver_bp.route('/deliveries/assign/<int:delivery_id>', methods=['PUT'])
def assign_driver(delivery_id):
    try:
        service = DriverService()
        # Fetch delivery object (assuming it's checked by service for existence)
        delivery = Deliveries.query.get(delivery_id) 
        
        assigned = service.try_assign_driver(delivery)
        
        if not assigned:
            return jsonify({"message": "No available drivers found."}), 404
            
        driver = service.validate_driver(delivery.driver_id) # Fetch the newly assigned driver
        
        return jsonify({
            "message": f"Delivery {delivery_id} successfully assigned to driver {driver.user_id}.",
            "delivery_id": delivery.id,
            "assigned_driver_id": driver.user_id,
            "driver_duty_status": driver.duty_status,
            "delivery_status": delivery.delivery_status
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

@driver_bp.route('/deliveries/<int:delivery_id>/complete', methods=['PUT'])
def complete_delivery(delivery_id):
    try:
        service = DriverService()
        delivery = service.complete_delivery(delivery_id)
        
        return jsonify({
            "message": f"Delivery {delivery_id} marked as delivered/completed.",
            "delivery_id": delivery.id,
            "new_status": delivery.delivery_status
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

@driver_bp.route('/deliveries/<int:delivery_id>/rate', methods=['PUT'])
def rate_driver(delivery_id):
    try:
        data = request.json
        service = DriverService()
        if 'rating' not in data:
            return jsonify({"error": "Missing rating field"}), 400
            
        driver, delivery = service.rate_driver(delivery_id, data['rating'])
        
        return jsonify({
            "message": f"Driver {driver.user_id} rated successfully.",
            "delivery_id": delivery.id,
            "new_rating": float(driver.rating)
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500


# --- Driver Delivery Views ---
@driver_bp.route('/driver/<int:driver_id>/active-delivery', methods=['GET'])
def get_active_delivery(driver_id):
    try:
        service = DriverService()
        delivery = service.get_active_delivery(driver_id)
        return jsonify({"active_delivery": delivery_to_dict(delivery)}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

@driver_bp.route('/driver/<int:driver_id>/history', methods=['GET'])
def show_completed_deliveries(driver_id):
    try:
        service = DriverService()
        deliveries = service.show_completed_deliveries(driver_id)
        
        return jsonify({
            "history": [delivery_to_dict(d) for d in deliveries]
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500
  
