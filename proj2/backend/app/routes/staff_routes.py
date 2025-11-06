from flask import Blueprint, request, jsonify
from app.models import *
from app.app import db
from app.services.staff_service import StaffService

staff_bp = Blueprint("staff", __name__, url_prefix="/api")

def get_user_id():
    data = request.json
    return data.get('user_id')

@staff_bp.route('/staff', methods=['POST'])
def add_staff():
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
        return jsonify({'error': 'An error occurred'}), 500


@staff_bp.route('/staff/<int:staff_user_id>', methods=['DELETE'])
def remove_staff(staff_user_id):
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        service.remove_staff(staff_user_id)
        return jsonify({"message":"Staff successfully removed"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500


@staff_bp.route('/theatres', methods=['GET'])
def get_theatres():
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        theatres = service.get_theatres()
        return jsonify({"theatres": [{"id": t.id, "name": t.name, "address": t.address, "phone": t.phone, "is_open": t.is_open} for t in theatres]}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500


@staff_bp.route('/theatres', methods=['PUT'])
def set_theatre_status():
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
        return jsonify({'error': 'An error occurred'}), 500


@staff_bp.route('/movies', methods=['POST'])
def add_movie():
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
        return jsonify({'error': 'An error occurred'}), 500


@staff_bp.route('/movies/<int:movie_id>', methods=['PUT'])
def edit_movie(movie_id):
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
        return jsonify({'error': 'An error occurred'}), 500


@staff_bp.route('/movies/<int:movie_id>', methods=['DELETE'])
def remove_movie(movie_id):
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        service.remove_movie(movie_id)
        return jsonify({"message":"Movie successfully removed"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500


@staff_bp.route('/showings', methods=['POST'])
def add_showing():
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
            start_time=data['start_time']
        )
        return jsonify({"message":"Movie Showing created successfully", "showing_id": showing.id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500


@staff_bp.route('/showings/<int:showing_id>', methods=['PUT'])
def edit_showing(showing_id):
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
            start_time=data['start_time'],
        )
        return jsonify({"message":"Movie Showing details changed successfully", "showing_id": showing.id}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500


@staff_bp.route('/showings/<int:showing_id>', methods=['DELETE'])
def remove_showing(showing_id):
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        service.remove_showing(showing_id)
        return jsonify({"message":"Movie Showing successfully removed"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500


@staff_bp.route('/staff', methods=['PUT'])
def set_availability():
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
        return jsonify({'error': 'An error occurred'}), 500


@staff_bp.route('/deliveries/<int:delivery_id>/status', methods=['PUT'])
def update_delivery_status(delivery_id):
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        data = request.json
        if 'delivery_status' not in data:
            return jsonify({"error": "Missing delivery_status"}), 400
        delivery = service.update_delivery_status(delivery_id, data['delivery_status'])
        return jsonify({"message": f"Delivery status updated to {delivery.delivery_status}"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500


@staff_bp.route('/deliveries/<int:delivery_id>/accept', methods=['PUT'])
def accept_delivery(delivery_id):
    try:
        user_id = get_user_id()
        service = StaffService(user_id)
        delivery = service.accept_delivery(delivery_id)
        return jsonify({"message": "Delivery accepted successfully"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500
