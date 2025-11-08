from flask import Blueprint, request, jsonify
from app.models import *
from app.app import db
from app.services.supplier_service import SupplierService


# Blueprint for supplier-related endpoints
supplier_bp = Blueprint("suppliers", __name__, url_prefix="/api")


# Helper function to get the current user's id
def get_user_id():
    data = request.json
    return data.get('user_id')


@supplier_bp.route('/suppliers/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    """
    Get Supplier Details
    ---
    tags: [Supplier Management]
    description: Retrieves company profile details for a supplier by user ID.
    parameters:
      - in: path
        name: supplier_id
        type: integer
        required: true
        description: The supplier's user ID.
    responses:
      200:
        description: Supplier details retrieved successfully
        schema:
          type: object
          properties:
            supplier: {$ref: '#/definitions/SupplierDetails'}
      404:
        description: Supplier not found
    """
    try:
        service = SupplierService(supplier_id)
        supplier = service.get_supplier()
        return jsonify({"supplier": {"user_id": supplier.user_id, "company_name": supplier.company_name, "company_address": supplier.company_address, "contact_phone": supplier.contact_phone, "is_open": supplier.is_open}}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@supplier_bp.route('/suppliers', methods=['PUT'])
def edit_supplier():
    """
    Update Supplier Profile
    ---
    tags: [Supplier Management]
    description: Updates the authenticated supplier's company name, address, phone, and open state. Requires user_id in the request body.
    parameters:
      - in: body
        name: supplier_update
        schema: {$ref: '#/definitions/SupplierEdit'}
    responses:
      200:
        description: Supplier details changed successfully
        schema:
          type: object
          properties:
            message: {type: string}
            supplier_id: {type: integer}
      400:
        description: Missing or invalid fields
      404:
        description: Supplier not found
    """
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
        return jsonify({'error': str(e)}), 500



@supplier_bp.route('/suppliers/status', methods=['PUT'])
def set_availability():
    """
    Set Supplier Availability
    ---
    tags: [Supplier Management]
    description: Sets the supplier's is_open status (open/closed). Requires user_id in the request body.
    parameters:
      - in: body
        name: status_update
        schema: {$ref: '#/definitions/SupplierStatusUpdate'}
    responses:
      200:
        description: Supplier status changed successfully
        schema:
          type: object
          properties:
            message: {type: string}
      400:
        description: Missing is_open field
      404:
        description: Supplier not found
    """
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
        return jsonify({'error': str(e)}), 500



@supplier_bp.route('/products/<int:supplier_id>', methods=['GET'])
def get_products(supplier_id):
    """
    List Supplier Products
    ---
    tags: [Product Management]
    description: Retrieves all products managed by the specified supplier.
    parameters:
      - in: path
        name: supplier_id
        type: integer
        required: true
        description: The supplier's user ID.
    responses:
      200:
        description: Products retrieved successfully
        schema:
          type: object
          properties:
            products:
              type: array
              items: {$ref: '#/definitions/Product'}
      404:
        description: Supplier not found
    """
    try:
        service = SupplierService(supplier_id)
        products = service.get_products()
        return jsonify({"products": [{"id": p.id, "supplier_id": p.supplier_id, "name": p.name, "unit_price": float(p.unit_price), "inventory_quantity": p.inventory_quantity, "size": p.size, "keywords": p.keywords, "category": p.category, "discount": p.discount, "is_available": p.is_available} for p in products]}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@supplier_bp.route('/products', methods=['POST'])
def add_product():
    """
    Add New Product
    ---
    tags: [Product Management]
    description: Creates a new product under the authenticated supplier. Requires user_id in the request body.
    parameters:
      - in: body
        name: product_details
        schema: {$ref: '#/definitions/ProductCreateEdit'}
    responses:
      201:
        description: Product added successfully
        schema:
          type: object
          properties:
            message: {type: string}
            product_id: {type: integer}
      400:
        description: Missing or invalid fields
      404:
        description: Supplier not found
    """
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
        return jsonify({'error': str(e)}), 500



@supplier_bp.route('/products/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    """
    Edit Existing Product
    ---
    tags: [Product Management]
    description: Updates fields for an existing product owned by the authenticated supplier. Requires user_id in the request body.
    parameters:
      - in: path
        name: product_id
        type: integer
        required: true
        description: The product ID to update.
      - in: body
        name: product_details
        schema: {$ref: '#/definitions/ProductCreateEdit'}
    responses:
      200:
        description: Product details changed successfully
        schema:
          type: object
          properties:
            message: {type: string}
            product_id: {type: integer}
      400:
        description: Missing or invalid fields
      404:
        description: Product or Supplier not found
    """
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
        return jsonify({'error': str(e)}), 500



@supplier_bp.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    """
    Remove Product
    ---
    tags: [Product Management]
    description: Deletes a product by ID for the authenticated supplier. Requires user_id in the request body.
    parameters:
      - in: path
        name: product_id
        type: integer
        required: true
        description: The product ID to remove.
      - in: body
        name: user_id
        schema: 
          type: object
          properties:
            user_id: {type: integer, description: 'The supplier user ID.'}
    responses:
      200:
        description: Product successfully removed
        schema:
          type: object
          properties:
            message: {type: string}
      404:
        description: Product or Supplier not found
    """
    try:
        user_id = get_user_id()
        service = SupplierService(user_id)
        service.remove_product(product_id)
        return jsonify({"message":"Product successfully removed"}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
       
    
@supplier_bp.route('/suppliers/all', methods=['GET'])
def list_open_suppliers():
    """
    List Open Suppliers
    ---
    tags: [Supplier Management]
    description: Retrieves all suppliers that are currently open (is_open = true).
    responses:
      200:
        description: Open suppliers retrieved successfully
        schema:
          type: object
          properties:
            suppliers:
              type: array
              items: {$ref: '#/definitions/SupplierDetails'}
    """
    try:
        service = SupplierService(Suppliers.query.first().user_id)  
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
