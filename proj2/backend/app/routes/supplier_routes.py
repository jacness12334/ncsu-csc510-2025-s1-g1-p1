from flask import Blueprint, request, jsonify
from app.models import *
from app.app import db
from app.services.supplier_service import SupplierService

supplier_bp = Blueprint("suppliers", __name__, url_prefix="/api")

def get_user_id():
    data = request.json
    return data.get('user_id')


@supplier_bp.route('/suppliers', methods=['GET'])
def get_supplier():
    try:
        user_id = get_user_id()
        service = SupplierService(user_id)
        supplier = service.get_supplier()
        return jsonify({"supplier": {"user_id": supplier.user_id, "company_name": supplier.company_name, "company_address": supplier.company_address, "contact_phone": supplier.contact_phone, "is_open": supplier.is_open}}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500


@supplier_bp.route('/suppliers', methods=['PUT'])
def edit_supplier():
    try:
        user_id = get_user_id()
        service = SupplierService(user_id)
        data = request.json
        required_fields = ['company_name', 'company_address', 'contact_phone', 'is_open']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        supplier = service.edit_supplier(
            company_name=data['company_name'],
            company_address=data['company_address'],
            contact_phone=data['contact_phone'],
            is_open=data['is_open']
        )
        return jsonify({"message":"Supplier details changed successfully", "supplier_id": supplier.user_id}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500


@supplier_bp.route('/suppliers/status', methods=['PUT'])
def set_availability():
    try:
        user_id = get_user_id()
        service = SupplierService(user_id)
        data = request.json
        if 'is_open' not in data:
            return jsonify({"error": "Missing is_open field"}), 400
        supplier = service.set_is_open(data['is_open'])
        return jsonify({"message":f"Supplier set to {supplier.is_open}"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500


@supplier_bp.route('/products', methods=['GET'])
def get_products():
    try:
        user_id = get_user_id()
        service = SupplierService(user_id)
        products = service.get_products()
        return jsonify({"products": [{"id": p.id, "supplier_id": p.supplier_id, "name": p.name, "unit_price": float(p.unit_price), "inventory_quantity": p.inventory_quantity, "size": p.size, "keywords": p.keywords, "category": p.category, "discount": p.discount, "is_available": p.is_available} for p in products]}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500


@supplier_bp.route('/products', methods=['POST'])
def add_product():
    try:
        user_id = get_user_id()
        service = SupplierService(user_id)
        data = request.json
        required_fields = ['name', 'unit_price', 'inventory_quantity', 'size', 'keywords', 'category', 'discount', 'is_available']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        product = service.add_product(
            name=data['name'],
            unit_price=data['unit_price'],
            inventory_quantity=data['inventory_quantity'],
            size=data['size'],
            keywords=data['keywords'],
            category=data['category'],
            discount=data['discount'],
            is_available=data['is_available']
        )
        return jsonify({"message":"Product added successfully", "product_id": product.id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500


@supplier_bp.route('/products/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    try:
        user_id = get_user_id()
        service = SupplierService(user_id)
        data = request.json
        required_fields = ['name', 'unit_price', 'inventory_quantity', 'size', 'keywords', 'category', 'discount', 'is_available']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        product = service.edit_product(
            product_id=product_id,
            name=data['name'],
            unit_price=data['unit_price'],
            inventory_quantity=data['inventory_quantity'],
            size=data['size'],
            keywords=data['keywords'],
            category=data['category'],
            discount=data['discount'],
            is_available=data['is_available']
        )
        return jsonify({"message":"Product details changed successfully", "product_id": product.id}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500


@supplier_bp.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    try:
        user_id = get_user_id()
        service = SupplierService(user_id)
        service.remove_product(product_id)
        return jsonify({"message":"Product successfully removed"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500 
       
    
@supplier_bp.route('/suppliers/all', methods=['GET'])
def list_open_suppliers():
    try:
        service = SupplierService()  
        suppliers = service.get_all_suppliers()

        return jsonify({
            "suppliers": [
                {
                    "user_id": s.user_id,
                    "company_name": s.company_name,
                    "company_address": s.company_address,
                    "contact_phone": s.contact_phone,
                    "is_open": s.is_open
                } for s in suppliers
            ]
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500
