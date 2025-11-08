from flask import Blueprint, request, jsonify
from app.models import *
from app.services.staff_service import StaffService
from datetime import datetime


# Blueprint for staff-related endpoints
staff_bp = Blueprint("staff", __name__, url_prefix="/api")


# Helper function to retrieve the current user's id
def get_user_id():
    data = request.json
    return data.get('user_id')


@staff_bp.route('/staff', methods=['POST'])
def add_staff():
    """
    Add New Staff Member
    ---
    tags: [Staff Management]
    description: Adds a new staff member. Requires manager user_id in the request body for authorization.
    parameters:
      - in: body
        name: staff_registration
        schema: {$ref: '#/definitions/StaffRegistration'}
    responses:
      201:
        description: Staff member created successfully
        schema:
          type: object
          properties:
            message: {type: string}
            user_id: {type: integer}
            staff_role: {type: string}
      400:
        description: Missing or invalid fields
      404:
        description: Unauthorized (manager not admin) or theatre not found
    """
    try:
        user_id = get_user_id()
        service = StaffService(user_id)

        data = request.json
        required_fields = ['name', 'email', 'phone', 'birthday', 'password', 'theatre_id', 'role']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        staff = service.add_staff(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            birthday=data['birthday'],
            password=data['password'],
            theatre_id=data['theatre_id'],
            role=data['role']
        )
        return jsonify({"message": "Staff member created successfully", "user_id": staff.user_id, "staff_role": staff.role}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@staff_bp.route('/staff/<int:staff_user_id>', methods=['DELETE'])
def remove_staff(staff_user_id):
    """
    Remove Staff Member
    ---
    tags: [Staff Management]
    description: Removes a staff member. Requires manager user_id in the request body for authorization.
    parameters:
      - in: path
        name: staff_user_id
        type: integer
        required: true
        description: The user ID of the staff member to remove.
      - in: body
        name: manager_id
        schema:
          type: object
          properties:
            user_id: {type: integer, description: 'The staff manager user ID.'}
    responses:
      200:
        description: Staff successfully removed
        schema:
          type: object
          properties:
            message: {type: string}
      404:
        description: Staff member not found or unauthorized
    """
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        service.remove_staff(staff_user_id)
        return jsonify({"message":"Staff successfully removed"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@staff_bp.route('/theatres/<int:staff_user_id>', methods=['GET'])
def get_theatres(staff_user_id):
    """
    Get Theatres
    ---
    tags: [Theatre Operations]
    description: Retrieves a list of all theatres.
    parameters:
      - in: path
        name: staff_user_id
        type: integer
        required: true
        description: The staff user ID (context only).
    responses:
      200:
        description: Theatres retrieved successfully
        schema:
          type: object
          properties:
            theatres:
              type: array
              items: {$ref: '#/definitions/TheatreDetails'}
    """
    try:
        service = StaffService(staff_user_id)
        theatres = service.get_theatres()
        return jsonify({"theatres": [{"id": t.id, "name": t.name, "address": t.address, "phone": t.phone, "is_open": t.is_open} for t in theatres]}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@staff_bp.route('/theatres', methods=['GET'])
def get_all_theatres():
    """
    List All Theatres
    ---
    tags: [Theatre Operations]
    description: Retrieves all theatres without filtering or authorization.
    responses:
      200:
        description: Theatres retrieved successfully
        schema:
          type: object
          properties:
            theatres:
              type: array
              items: {$ref: '#/definitions/TheatreDetails'}
    """
    try:
        return jsonify({'theatres': [{"id": t.id, "name": t.name, "address": t.address, "phone": t.phone, "is_open": t.is_open} for t in Theatres.query.all()]}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@staff_bp.route('/theatres', methods=['PUT'])
def set_theatre_status():
    """
    Set Theatre Open/Close Status
    ---
    tags: [Theatre Operations]
    description: Opens or closes a theatre location. Requires staff user_id in the body for authorization (admin only).
    parameters:
      - in: body
        name: theatre_status_update
        schema: {$ref: '#/definitions/TheatreStatusUpdate'}
    responses:
      200:
        description: Theatre status updated successfully
        schema:
          type: object
          properties:
            message: {type: string}
      400:
        description: Missing theatre_id or is_open
      404:
        description: Theatre not found or unauthorized
    """
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        data = request.json
        if 'theatre_id' not in data or 'is_open' not in data:
            return jsonify({"error": "Missing theatre_id or is_open"}), 400
        theatre = service.set_theatre_status(data['theatre_id'], data['is_open'])
        return jsonify({"message":f"Theatre {'opened' if theatre.is_open else 'closed'}"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@staff_bp.route('/movies', methods=['POST'])
def add_movie():
    """
    Add New Movie
    ---
    tags: [Movie Management]
    description: Adds a new movie. Requires staff user_id in the body for authorization (admin only).
    parameters:
      - in: body
        name: new_movie
        schema: {$ref: '#/definitions/MovieCreateEdit'}
    responses:
      201:
        description: Movie added successfully
        schema:
          type: object
          properties:
            message: {type: string}
            movie_id: {type: integer}
      400:
        description: Missing or invalid fields
      404:
        description: Unauthorized
    """
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        data = request.json
        required_fields = ['title', 'genre', 'length_mins', 'release_year', 'keywords', 'rating']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        movie = service.add_movie(
            title=data['title'],
            genre=data['genre'],
            length_mins=data['length_mins'],
            release_year=data['release_year'],
            keywords=data['keywords'],
            rating=data['rating']
        )
        return jsonify({"message":"Movie added successfully", "movie_id": movie.id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@staff_bp.route('/movies/<int:movie_id>', methods=['PUT'])
def edit_movie(movie_id):
    """
    Edit Existing Movie
    ---
    tags: [Movie Management]
    description: Updates an existing movie. Requires staff user_id in the body for authorization (admin only).
    parameters:
      - in: path
        name: movie_id
        type: integer
        required: true
        description: The ID of the movie to update.
      - in: body
        name: movie_update
        schema: {$ref: '#/definitions/MovieCreateEdit'}
    responses:
      200:
        description: Movie details changed successfully
        schema:
          type: object
          properties:
            message: {type: string}
            movie_id: {type: integer}
      400:
        description: Missing or invalid fields
      404:
        description: Movie not found or unauthorized
    """
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        data = request.json
        required_fields = ['title', 'genre', 'length_mins', 'release_year', 'keywords', 'rating']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        movie = service.edit_movie(
            movie_id=movie_id,
            title=data['title'],
            genre=data['genre'],
            length_mins=data['length_mins'],
            release_year=data['release_year'],
            keywords=data['keywords'],
            rating=data['rating']
        )
        return jsonify({"message":"Movie details changed successfully", "movie_id": movie.id}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@staff_bp.route('/movies/<int:movie_id>', methods=['DELETE'])
def remove_movie(movie_id):
    """
    Remove Movie
    ---
    tags: [Movie Management]
    description: Removes a movie by ID. Requires staff user_id in the body for authorization (admin only).
    parameters:
      - in: path
        name: movie_id
        type: integer
        required: true
        description: The ID of the movie to remove.
      - in: body
        name: staff_id
        schema:
          type: object
          properties:
            user_id: {type: integer, description: 'The staff manager user ID.'}
    responses:
      200:
        description: Movie successfully removed
        schema:
          type: object
          properties:
            message: {type: string}
      404:
        description: Movie not found or unauthorized
    """
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        service.remove_movie(movie_id)
        return jsonify({"message":"Movie successfully removed"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@staff_bp.route('/showings', methods=['POST'])
def add_showing():
    """
    Add New Movie Showing
    ---
    tags: [Showings Scheduling]
    description: Schedules a new movie showing. Requires staff user_id in the body for authorization (admin only). Expects start_time as ISO 8601 string.
    parameters:
      - in: body
        name: new_showing
        schema: {$ref: '#/definitions/ShowingCreateEdit'}
    responses:
      201:
        description: Movie Showing created successfully
        schema:
          type: object
          properties:
            message: {type: string}
            showing_id: {type: integer}
      400:
        description: Missing fields or invalid start_time
      404:
        description: Movie/Auditorium not found or unauthorized
    """
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        data = request.json
        required_fields = ['movie_id', 'auditorium_id', 'start_time']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        showing = service.add_showing(
            movie_id=data['movie_id'],
            auditorium_id=data['auditorium_id'],
            start_time=datetime.fromisoformat(data['start_time'].replace("Z", "+00:00"))
        )
        return jsonify({"message":"Movie Showing created successfully", "showing_id": showing.id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@staff_bp.route('/showings/<int:showing_id>', methods=['PUT'])
def edit_showing(showing_id):
    """
    Edit Existing Showing
    ---
    tags: [Showings Scheduling]
    description: Updates an existing movie showing. Requires staff user_id in the body for authorization (admin only). Expects start_time as ISO 8601 string.
    parameters:
      - in: path
        name: showing_id
        type: integer
        required: true
        description: The ID of the showing to update.
      - in: body
        name: showing_update
        schema: {$ref: '#/definitions/ShowingCreateEdit'}
    responses:
      200:
        description: Movie Showing details changed successfully
        schema:
          type: object
          properties:
            message: {type: string}
            showing_id: {type: integer}
      400:
        description: Missing fields or invalid start_time
      404:
        description: Showing not found or unauthorized
    """
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        data = request.json
        required_fields = ['movie_id', 'auditorium_id', 'start_time']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        showing = service.edit_showing(
            showing_id=showing_id,
            movie_id=data['movie_id'],
            auditorium_id=data['auditorium_id'],
            start_time=datetime.fromisoformat(data['start_time'].replace("Z", "+00:00"))
        )
        return jsonify({"message":"Movie Showing details changed successfully", "showing_id": showing.id}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@staff_bp.route('/showings/<int:showing_id>', methods=['DELETE'])
def remove_showing(showing_id):
    """
    Remove Movie Showing
    ---
    tags: [Showings Scheduling]
    description: Removes a movie showing by ID. Requires staff user_id in the body for authorization (admin only).
    parameters:
      - in: path
        name: showing_id
        type: integer
        required: true
        description: The ID of the showing to remove.
      - in: body
        name: staff_id
        schema:
          type: object
          properties:
            user_id: {type: integer, description: 'The staff manager user ID.'}
    responses:
      200:
        description: Movie Showing successfully removed
        schema:
          type: object
          properties:
            message: {type: string}
      404:
        description: Showing not found or unauthorized
    """
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        service.remove_showing(showing_id)
        return jsonify({"message":"Movie Showing successfully removed"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@staff_bp.route('/staff', methods=['PUT'])
def set_availability():
    """
    Set Staff Availability
    ---
    tags: [Staff Management]
    description: Sets the staff member's availability status. Requires staff user_id in the body.
    parameters:
      - in: body
        name: availability_update
        schema: {$ref: '#/definitions/StaffAvailabilityUpdate'}
    responses:
      200:
        description: Availability set successfully
        schema:
          type: object
          properties:
            message: {type: string}
      400:
        description: Missing is_available field
      404:
        description: Staff member not found
    """
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        data = request.json
        if 'is_available' not in data:
            return jsonify({"error": "Missing is_available field"}), 400
        staff = service.set_availability(data['is_available'])
        return jsonify({"message":f"Availability set to {staff.is_available}"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@staff_bp.route('/deliveries/<int:delivery_id>/accept', methods=['PUT'])
def accept_delivery(delivery_id):
    """
    Accept Delivery Order
    ---
    tags: [Delivery Management]
    description: Staff member accepts a pending delivery for fulfillment. Requires staff user_id in the body.
    parameters:
      - in: path
        name: delivery_id
        type: integer
        required: true
        description: The ID of the delivery order to accept.
      - in: body
        name: staff_id
        schema:
          type: object
          properties:
            user_id: {type: integer, description: 'The staff member user ID.'}
    responses:
      200:
        description: Delivery accepted successfully
        schema:
          type: object
          properties:
            message: {type: string}
      400:
        description: Staff not available or delivery not pending
      404:
        description: Delivery or Staff not found
    """
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        delivery = service.accept_delivery(delivery_id)
        return jsonify({"message": "Delivery accepted successfully"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@staff_bp.route('/deliveries/<int:delivery_id>/fulfill', methods=['PUT'])
def fulfill_delivery(delivery_id):
    """
    Fulfill Delivery Order
    ---
    tags: [Delivery Management]
    description: Staff member marks a delivered order as fulfilled. Requires staff user_id in the body.
    parameters:
      - in: path
        name: delivery_id
        type: integer
        required: true
        description: The ID of the delivery order to fulfill.
      - in: body
        name: staff_id
        schema:
          type: object
          properties:
            user_id: {type: integer, description: 'The staff member user ID.'}
    responses:
      200:
        description: Delivery fulfilled successfully
        schema:
          type: object
          properties:
            message: {type: string}
      400:
        description: Delivery status is not 'delivered'
      404:
        description: Delivery or Staff not found
    """
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        data = request.json
        delivery = service.fulfill_delivery(delivery_id)
        return jsonify({"message": f"Delivery fulfilled"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@staff_bp.route('/staff/list/<int:theatre_id>', methods=['PUT'])
def list_staff_by_theatre(theatre_id):
    """
    List Staff by Theatre
    ---
    tags: [Staff Management]
    description: Retrieves staff working at a theatre. Requires staff user_id in the body for authorization.
    parameters:
      - in: path
        name: theatre_id
        type: integer
        required: true
        description: The ID of the theatre to list staff for.
      - in: body
        name: staff_id
        schema:
          type: object
          properties:
            user_id: {type: integer, description: 'The staff manager user ID.'}
    responses:
      200:
        description: List of staff retrieved successfully
        schema:
          type: object
          properties:
            staff:
              type: array
              items: {$ref: '#/definitions/StaffMemberDetails'}
      404:
        description: Theatre not found or unauthorized
    """
    try:
        user_id = get_user_id()  
        service = StaffService(user_id)
        staff = service.show_all_staff(theatre_id)
        return jsonify({
            "staff": [{
                "user_id": s.user_id,
                "theatre_id": s.theatre_id,
                "role": s.role,
                "is_available": s.is_available
            } for s in staff]
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@staff_bp.route('/deliveries/list/<int:theatre_id>', methods=['GET'])
def list_deliveries_by_theatre(theatre_id):
    """
    List Deliveries by Theatre
    ---
    tags: [Delivery Management]
    description: Retrieves deliveries associated with a theatre ID. Intended for staff views.
    parameters:
      - in: path
        name: theatre_id
        type: integer
        required: true
        description: The ID of the theatre to list deliveries for.
    responses:
      200:
        description: List of deliveries retrieved successfully
        schema:
          type: object
          properties:
            deliveries:
              type: array
              items: {$ref: '#/definitions/DeliveryDetails'}
      404:
        description: Theatre not found or unauthorized
    """
    try:
        service = StaffService(Staff.query.first().user_id)
        deliveries = service.show_all_deliveries(theatre_id)
        return jsonify({
            "deliveries": [{
                "id": d.id,
                "customer_showing_id": d.customer_showing_id,
                "payment_method_id": d.payment_method_id,
                "driver_id": d.driver_id,
                "staff_id": d.staff_id,
                "total_price": float(d.total_price),
                "payment_status": d.payment_status,
                "delivery_status": d.delivery_status
            } for d in deliveries]
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@staff_bp.route('/staff/<int:staff_user_id>', methods=['GET'])
def get_staff(staff_user_id):
    """
    Get Staff Profile
    ---
    summary: Get Staff Profile
    tags: [Staff Management]
    description: Retrieves staff profile details by staff user ID.
    parameters:
      - in: path
        name: staff_user_id
        type: integer
        required: true
        description: The ID of the staff user.
    responses:
      200:
        description: Staff profile retrieved
        schema:
          type: object
          properties:
            user_id: {type: integer}
            theatre_id: {type: integer}
            role: {type: string}
            is_available: {type: boolean}
      404:
        description: Staff member not found or unauthorized
    """
    try:
        service = StaffService(staff_user_id)
        data = service.get_staff(staff_id=staff_user_id)
        return jsonify({
            "user_id": data.user_id,
            "theatre_id": data.theatre_id,
            "role": data.role,
            "is_available": data.is_available
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
