from flask import Blueprint, request, jsonify
from app.models import *
from app.app import db, get_app
from app.services.supplier_service import SupplierService

bp = Blueprint("suppliers", __name__, url_prefix="/api")

config_name = 'development'
app = get_app(config_name)

def get_user_id():
    data = request.json
    return data.get('user_id')

@bp.route('/suppliers', methods=['POST'])
def create_supplier():
    user_id = get_user_id()
    service = SupplierService(user_id)

    data = request.json
    required_fields = ['name', 'email', 'phone', 'birthday', 'password', 'company_name', 'company_address', 'contact_phone', 'is_open']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    response, status = service.add_supplier(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        birthday=data['birthday'],
        password=data['password'],
        company_name=data['company_name'],
        company_address=data['company_address'],
        contact_phone=data['contact_phone'],
        is_open=False
    )
    return jsonify(response), status


@bp.route('/suppliers', methods=['PUT'])
def edit_supplier():
    user_id = get_user_id()
    service = SupplierService(user_id)
    data = request.json
    required_fields = ['company_name', 'company_address', 'contact_phone', 'is_open']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    response, status = service.edit_supplier(
        company_name=data['company_name'],
        company_address=data['company_address'],
        contact_phone=data['contact_phone'],
        is_open=data['is_open']
    )
    return jsonify(response), status


@bp.route('/suppliers/status', methods=['PUT'])
def set_availability():
    user_id = get_user_id()
    service = SupplierService(user_id)
    data = request.json
    if 'is_open' not in data:
        return jsonify({"error": "Missing is_open field"}), 400
    response, status = service.set_is_open(data['is_open'])
    return jsonify(response), status


@bp.route('/products', methods=['POST'])
def add_product():
    user_id = get_user_id()
    service = SupplierService(user_id)
    data = request.json
    required_fields = ['name', 'unit_price', 'inventory_quantity', 'size', 'keywords', 'category', 'is_available']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    response, status = service.add_product(
        name=data['name'],
        unit_price=data['unit_price'],
        inventory_quantity=data['inventory_quantity'],
        size=data['size'],
        keywords=data['keywords'],
        category=data['category'],
        is_available=data['is_available']
    )
    return jsonify(response), status


@bp.route('/products/<int:product_id>', methods=['PUT'])
def edit_movie(product_id):
    user_id = get_user_id()
    service = SupplierService(user_id)
    data = request.json
    required_fields = ['name', 'unit_price', 'inventory_quantity', 'size', 'keywords', 'category', 'is_available']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    response, status = service.edit_product(
        product_id=product_id,
        name=data['name'],
        unit_price=data['unit_price'],
        inventory_quantity=data['inventory_quantity'],
        size=data['size'],
        keywords=data['keywords'],
        category=data['category'],
        is_available=data['is_available']
    )
    return jsonify(response), status


@bp.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    user_id = get_user_id()
    service = SupplierService(user_id)
    response, status = service.remove_product(product_id)
    return jsonify(response), status

app.register_blueprint(bp)
