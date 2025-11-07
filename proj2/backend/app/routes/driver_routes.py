from flask import Blueprint, request, jsonify
from app.models import *
from app.services.driver_service import DriverService

# Blueprint for driver-related endpoints
driver_bp = Blueprint("driver", __name__, url_prefix="/api")

# Helper function to retrieve the current user
def get_user_id():
    data = request.json
    return data.get('user_id')

# Helper function to convert delivery fields into dictionary
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
        "delivery_status": delivery.delivery_status,
    }

# --- Admin/Staff Routes for Driver Management ---
@driver_bp.route('/driver', methods=['POST'])
def create_driver():
    """
    Create New Driver Account
    ---
    tags: [Driver Management (Admin)]
    description: Creates a new driver account with vehicle details.
    parameters:
      - in: body
        name: driver_registration
        schema: {$ref: '#/definitions/DriverRegistration'}
    responses:
      201:
        description: Driver created successfully
        schema:
          type: object
          properties:
            message: {type: string}
            user_id: {type: integer}
      400: {description: Missing required fields}
    """
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
    """
    Delete Driver Account
    ---
    tags: [Driver Management (Admin)]
    description: Deletes a driver account by user ID.
    parameters:
      - in: path
        name: driver_user_id
        type: integer
        required: true
        description: The ID of the driver's user account to delete.
    responses:
      200:
        description: Driver deleted successfully
        schema:
          type: object
          properties:
            message: {type: string}
      404: {description: Driver not found}
    """
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
    """
    Get Driver Profile
    ---
    tags: [Driver Profile]
    description: Retrieves detailed profile and vehicle information for a driver.
    parameters:
      - in: path
        name: driver_user_id
        type: integer
        required: true
        description: The ID of the driver's user account.
    responses:
      200:
        description: Driver profile retrieved successfully
        schema:
          type: object
          properties:
            driver: {$ref: '#/definitions/DriverProfile'}
      404: {description: Driver not found}
    """
    try:
        service = DriverService()
        driver = service.validate_driver(driver_user_id)
        user = Users.query.filter_by(id=driver.user_id).first()

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
    """
    Update Driver Vehicle Details
    ---
    tags: [Driver Profile]
    description: Updates the vehicle-specific details (plate, type, color) for a driver.
    parameters:
      - in: path
        name: driver_user_id
        type: integer
        required: true
        description: The ID of the driver's user account.
      - in: body
        name: vehicle_update
        schema: {$ref: '#/definitions/DriverUpdate'}
    responses:
      200:
        description: Driver details updated successfully
        schema:
          type: object
          properties:
            message: {type: string}
            user_id: {type: integer}
      400: {description: Missing required fields or invalid input}
      404: {description: Driver not found}
    """
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
    """
    Update Driver Duty Status
    ---
    tags: [Driver Profile]
    description: Updates the driver's duty status (e.g., on_duty, off_duty, delivering).
    parameters:
      - in: path
        name: driver_user_id
        type: integer
        required: true
        description: The ID of the driver's user account.
      - in: body
        name: status_update
        schema: {$ref: '#/definitions/DriverStatusUpdate'}
    responses:
      200:
        description: Duty status updated successfully
        schema:
          type: object
          properties:
            message: {type: string}
            duty_status: {type: string}
      400: {description: Missing new_status field}
      404: {description: Driver not found}
    """
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
    """
    Assign Driver to Delivery
    ---
    tags: [Delivery Operations]
    description: Attempts to find and assign an available driver to a specific delivery order.
    parameters:
      - in: path
        name: delivery_id
        type: integer
        required: true
        description: The ID of the delivery order to assign.
    responses:
      200:
        description: Delivery successfully assigned to a driver
        schema:
          type: object
          properties:
            message: {type: string}
            delivery_id: {type: integer}
            assigned_driver_id: {type: integer}
            driver_duty_status: {type: string}
            delivery_status: {type: string}
      404: {description: No available drivers found or Delivery not found}
    """
    try:
        service = DriverService()
        # Fetch delivery object (assuming it's checked by service for existence)
        delivery = Deliveries.query.filter_by(id=delivery_id).first()
        
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
    """
    Complete Delivery Order
    ---
    tags: [Delivery Operations]
    description: Marks the delivery order as completed by the driver.
    parameters:
      - in: path
        name: delivery_id
        type: integer
        required: true
        description: The ID of the delivery order to mark as complete.
    responses:
      200:
        description: Delivery marked as completed
        schema:
          type: object
          properties:
            message: {type: string}
            delivery_id: {type: integer}
            new_status: {type: string}
      400: {description: Invalid delivery status transition}
      404: {description: Delivery not found}
    """
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
    """
    Rate Driver
    ---
    tags: [Delivery Operations]
    description: Allows a customer to rate the driver after the delivery is complete.
    parameters:
      - in: path
        name: delivery_id
        type: integer
        required: true
        description: The ID of the delivery order being rated.
      - in: body
        name: rating_value
        schema: {$ref: '#/definitions/DeliveryRate'}
    responses:
      200:
        description: Driver rated successfully
        schema:
          type: object
          properties:
            message: {type: string}
            delivery_id: {type: integer}
            new_rating: {type: number, format: float}
      400: {description: Missing rating field or invalid value}
      404: {description: Delivery or Driver not found}
    """
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
    """
    Get Active Delivery
    ---
    tags: [Driver Views]
    description: Retrieves the single delivery currently assigned to and being worked on by the driver.
    parameters:
      - in: path
        name: driver_id
        type: integer
        required: true
        description: The ID of the driver's user account.
    responses:
      200:
        description: Active delivery retrieved successfully
        schema:
          type: object
          properties:
            active_delivery: {$ref: '#/definitions/DeliveryHistoryItem'}
      404: {description: Driver not found or no active delivery}
    """
    try:
        service = DriverService()
        delivery = service.get_active_delivery(driver_id)
        delivery_items = DeliveryItems.query.filter_by(delivery_id=delivery.id).all()
        cart_items = [CartItems.query.filter_by(id=item.cart_item_id).first() for item in delivery_items]
        items = [{"name": Products.query.filter_by(id=item.product_id).first().name, "quantity": item.quantity} for item in cart_items]
        customer_showing = CustomerShowings.query.filter_by(id=delivery.customer_showing_id).first()
        showing = MovieShowings.query.filter_by(id=customer_showing.movie_showing_id).first()
        auditorium = Auditoriums.query.filter_by(id=showing.auditorium_id).first()
        theatre = Theatres.query.filter_by(id=auditorium.theatre_id).first()
        return jsonify({"active_delivery": {
        "id": delivery.id,
        "driver_id": delivery.driver_id,
        "customer_showing_id": delivery.customer_showing_id,
        "payment_method_id": delivery.payment_method_id,
        "staff_id": delivery.staff_id,
        "payment_status": delivery.payment_status,
        "total_price": float(delivery.total_price),
        "delivery_time": delivery.delivery_time.isoformat() if delivery.delivery_time else None,
        "delivery_status": delivery.delivery_status,
        "address": theatre.address,
        "items": items
    }}), 200
    except ValueError as e:
        if "No active delivery found for driver" in str(e):
            return jsonify({"message": "No active delivery"}), 200
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

@driver_bp.route('/driver/<int:driver_id>/history', methods=['GET'])
def show_completed_deliveries(driver_id):
    """
    Get Delivery History
    ---
    tags: [Driver Views]
    description: Retrieves a history of all completed delivery orders for a specific driver.
    parameters:
      - in: path
        name: driver_id
        type: integer
        required: true
        description: The ID of the driver's user account.
    responses:
      200:
        description: Delivery history retrieved successfully
        schema:
          type: object
          properties:
            history:
              type: array
              items: {$ref: '#/definitions/DeliveryHistoryItem'}
      404: {description: Driver not found}
    """
    try:
        service = DriverService()
        deliveries = service.show_completed_deliveries(driver_id)
        
        return jsonify({
            "history": [delivery_to_dict(d) for d in deliveries]
        }), 200
    except ValueError as e:
        if "No previous deliveries found for driver" in str(e):
            return jsonify({"message": "No previous deliveries found"}), 200
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500
