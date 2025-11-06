from flask import Blueprint, request, jsonify
from app.models import *
from app.app import db
from app.services.driver_service import DriverService

bp = Blueprint("driver", __name__, url_prefix="/api")

def get_user_id():
    data = request.json
    return data.get('user_id')

def delivery_to_dict(delivery):
    return {
        "id": delivery.id,
        "customer_showing_id": delivery.customer_showing_id,
        "payment_method_id": delivery.payment_method_id,
        "staff_id": delivery.staff_id,
        "payment_status": delivery.payment_status,
        "total_price": float(delivery.total_price),
        "delivery_time": delivery.delivery_time.isoformat() if delivery.delivery_time else None,
        "delivery_status": delivery.delivery_status
    }

@bp.route('/drivers', methods=['GET'])
def get_driver_info():
    try:
        user_id = get_user_id()
        service = DriverService(user_id)
        driver = service.get_driver()

        user = Users.query.get(driver.user_id)
        if not user:
             return jsonify({'error': 'User data not found for driver'}), 404

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
        print(f"Error fetching driver info: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500


@bp.route('/drivers', methods=['PUT'])
def update_driver_info():
    try:
        user_id = get_user_id()
        service = DriverService(user_id)
        data = request.json
        required_fields = ['license_plate', 'vehicle_type', 'vehicle_color']
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields: license_plate, vehicle_type, vehicle_color"}), 400
        
        driver = service.update_driver_info(
            license_plate=data['license_plate'],
            vehicle_type=data['vehicle_type'],
            vehicle_color=data['vehicle_color']
        )
        return jsonify({
            "message": "Driver information updated successfully", 
            "user_id": driver.user_id,
            "license_plate": driver.license_plate,
            "vehicle_type": driver.vehicle_type
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400 
    except Exception as e:
        print(f"Error updating driver info: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500


@bp.route('/drivers/status', methods=['PUT'])
def set_duty_status():
    try:
        user_id = get_user_id()
        service = DriverService(user_id)
        data = request.json
        
        if 'duty_status' not in data:
            return jsonify({"error": "Missing duty_status field"}), 400
        
        driver = service.set_duty_status(data['duty_status'])
        return jsonify({
            "message": f"Duty status set to {driver.duty_status}",
            "duty_status": driver.duty_status
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400 
    except Exception as e:
        print(f"Error setting duty status: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500


@bp.route('/drivers/deliveries', methods=['GET'])
def get_assigned_deliveries():
    try:
        user_id = get_user_id()
        service = DriverService(user_id)
        deliveries = service.get_assigned_deliveries()
        
        return jsonify({
            "deliveries": [delivery_to_dict(d) for d in deliveries]
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        print(f"Error fetching assigned deliveries: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500


@bp.route('/drivers/history', methods=['GET'])
def get_delivery_history():
    try:
        user_id = get_user_id()
        service = DriverService(user_id)
        deliveries = service.get_delivery_history()

        return jsonify({
            "history": [delivery_to_dict(d) for d in deliveries]
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        print(f"Error fetching delivery history: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500


@bp.route('/deliveries/<int:delivery_id>/status', methods=['PUT'])
def update_delivery_status_by_driver(delivery_id):
    try:
        user_id = get_user_id()
        service = DriverService(user_id)
        data = request.json
        
        if 'delivery_status' not in data:
            return jsonify({"error": "Missing delivery_status field"}), 400
        
        delivery = service.update_delivery_status(delivery_id, data['delivery_status'])
        
        return jsonify({
            "message": f"Delivery {delivery_id} status updated to {delivery.delivery_status}",
            "delivery_id": delivery.id,
            "new_status": delivery.delivery_status
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400 
    except Exception as e:
        print(f"Error updating delivery status by driver: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500
    
@bp.route('/deliveries/<int:delivery_id>/assign_driver', methods=['PUT'])
def assign_delivery_to_driver(delivery_id):
    try:
        user_id = get_user_id()
        service = DriverService(user_id)
        best_driver, delivery = service.assign_delivery_to_driver(delivery_id)
        
        return jsonify({
            "message": f"Delivery {delivery_id} successfully assigned to driver {best_driver.user_id} ({best_driver.rating} rating).",
            "delivery_id": delivery.id,
            "assigned_driver_id": best_driver.user_id,
            "new_delivery_status": delivery.delivery_status
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error auto-assigning delivery: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@bp.route('/drivers/<int:driver_user_id>/rating', methods=['PUT'])
def update_driver_rating(driver_user_id):
    try:
        user_id = get_user_id()
        service = DriverService(user_id)
        data = request.json

        if 'rating' not in data:
            return jsonify({"error": "Missing rating field"}), 400
        
        driver = service.update_driver_rating(driver_user_id, data['rating'])
        
        return jsonify({
            "message": f"Driver {driver_user_id} rating updated successfully.",
            "driver_id": driver.user_id,
            "new_rating": float(driver.rating)
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error updating driver rating: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500
    
