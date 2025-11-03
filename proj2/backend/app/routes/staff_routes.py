from flask import Blueprint, request, jsonify
from models import *
from app import db, get_app
from app.services.staff_service import StaffService

bp = Blueprint("staff", __name__, url_prefix="/api")

config_name = 'development'
app = get_app(config_name)

def get_user_id():
    data = request.json
    return data.get('user_id')

@bp.route('/staff', methods=['POST'])
def add_staff():
    user_id = get_user_id()
    service = StaffService(user_id)

    data = request.json
    required_fields = ['name', 'email', 'phone', 'birthday', 'password', 'theatre_id', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    response, status = service.add_staff(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        birthday=data['birthday'],
        password=data['password'],
        theatre_id=data['theatre_id'],
        role=data['role']
    )
    return jsonify(response), status


@bp.route('/staff/<int:staff_user_id>', methods=['DELETE'])
def remove_staff(staff_user_id):
    user_id = get_user_id()
    service = StaffService(user_id)
    response, status = service.remove_staff(staff_user_id)
    return jsonify(response), status


@bp.route('/theatre', methods=['PUT'])
def set_theatre_status():
    user_id = get_user_id()
    service = StaffService(user_id)
    data = request.json
    if 'theatre_id' not in data or 'is_open' not in data:
        return jsonify({"error": "Missing theatre_id or is_open"}), 400
    response, status = service.set_theatre_status(data['theatre_id'], data['is_open'])
    return jsonify(response), status


@bp.route('/movie', methods=['POST'])
def add_movie():
    user_id = get_user_id()
    service = StaffService(user_id)
    data = request.json
    required_fields = ['title', 'genre', 'length_mins', 'release_year', 'keywords', 'rating']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    response, status = service.add_movie(
        title=data['title'],
        genre=data['genre'],
        length_mins=data['length_mins'],
        release_year=data['release_year'],
        keywords=data['keywords'],
        rating=data['rating']
    )
    return jsonify(response), status


@bp.route('/movie/<int:movie_id>', methods=['PUT'])
def edit_movie(movie_id):
    user_id = get_user_id()
    service = StaffService(user_id)
    data = request.json
    required_fields = ['title', 'genre', 'length_mins', 'release_year', 'keywords', 'rating']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    response, status = service.edit_movie(
        movie_id=movie_id,
        title=data['title'],
        genre=data['genre'],
        length_mins=data['length_mins'],
        release_year=data['release_year'],
        keywords=data['keywords'],
        rating=data['rating']
    )
    return jsonify(response), status


@bp.route('/movie/<int:movie_id>', methods=['DELETE'])
def remove_movie(movie_id):
    user_id = get_user_id()
    service = StaffService(user_id)
    response, status = service.remove_movie(movie_id)
    return jsonify(response), status


@bp.route('/showing', methods=['POST'])
def add_showing():
    user_id = get_user_id()
    service = StaffService(user_id)
    data = request.json
    required_fields = ['movie_id', 'auditorium_id', 'start_time']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    response, status = service.add_showing(
        movie_id=data['movie_id'],
        auditorium_id=data['auditorium_id'],
        start_time=data['start_time']
    )
    return jsonify(response), status


@bp.route('/showing/<int:showing_id>', methods=['PUT'])
def edit_showing(showing_id):
    user_id = get_user_id()
    service = StaffService(user_id)
    data = request.json
    required_fields = ['movie_id', 'auditorium_id', 'start_time']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    response, status = service.edit_showing(
        showing_id=showing_id,
        movie_id=data['movie_id'],
        auditorium_id=data['auditorium_id'],
        start_time=data['start_time'],
    )
    return jsonify(response), status


@bp.route('/showing/<int:showing_id>', methods=['DELETE'])
def remove_showing(showing_id):
    user_id = get_user_id()
    service = StaffService(user_id)
    response, status = service.remove_showing(showing_id)
    return jsonify(response), status


@bp.route('/staff', methods=['PUT'])
def set_availability():
    user_id = get_user_id()
    service = StaffService(user_id)
    data = request.json
    if 'is_available' not in data:
        return jsonify({"error": "Missing is_available field"}), 400
    response, status = service.set_availability(data['is_available'])
    return jsonify(response), status


@bp.route('/delivery/<int:delivery_id>/status', methods=['PUT'])
def update_delivery_status(delivery_id):
    user_id = get_user_id()
    service = StaffService(user_id)
    data = request.json
    if 'delivery_status' not in data:
        return jsonify({"error": "Missing delivery_status"}), 400
    response, status = service.update_delivery_status(delivery_id, data['delivery_status'])
    return jsonify(response), status


@bp.route('/delivery/<int:delivery_id>/accept', methods=['PUT'])
def accept_delivery(delivery_id):
    user_id = get_user_id()
    service = StaffService(user_id)
    response, status = service.accept_delivery(delivery_id)
    return jsonify(response), status


app.register_blueprint(bp)