from flask import Blueprint, request, jsonify
from services.customer_service import CustomerService

customer_bp = Blueprint('customer', __name__, url_prefix='/api')
customer_service = CustomerService()

@customer_bp.route('/customers', methods=['POST'])
def create_customer():
    try:
        data = request.get_json()
        customer = customer_service.create_customer(
            name=data.get('name'), 
            email=data.get('email'),
            phone=data.get('phone'),
            birthday=data.get('birthday'),
            password=data.get('password'),
            role=data.get('role', 'customer'),
            default_theatre_id=data.get('default_theatre_id')
        )
        return jsonify({
            'message': 'Customer created successfully',
            'customer': {
                'user_id': customer.user_id,
                'default_theatre_id': customer.default_theatre_id
            }
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500
    
@customer_bp.route('/customers/<int:user_id>', methods=['GET'])
def get_customer(user_id):
    try:
        customer = customer_service.get_customer(user_id=user_id)
        return jsonify({
            'user_id': customer.user_id,
            'default_theatre_id': customer.default_theatre_id
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500
    
@customer_bp.route('/customers/<int:user_id>', methods=['DELETE'])
def delete_customer(user_id):
    try:
        customer_service.delete_customer(user_id)
        return jsonify({'message': 'Customer deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500
    
@customer_bp.route('/customers/<int:user_id>/theatre', methods=['PUT'])
def update_default_theatre(user_id):
    try:
        data = request.get_json()
        new_theatre_id = data.get('theatre_id')
        customer = customer_service.update_default_theatre(user_id=user_id, new_theatre_id=new_theatre_id)
        return jsonify({
            'message': 'Default theatre updated',
            'customer': {
                'user_id': customer.user_id,
                'default_theatre_id': customer.default_theatre_id
            }
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500
    
@customer_bp.route('/customers/<int:user_id>/payment-methods', methods=['POST'])
def add_payment_method(user_id):
    try:
        data = request.get_json()
        payment_method = customer_service.add_payment_method(
            user_id=user_id,
            card_number=data.get('card_number'),
            expiration_month=data.get('expiration_month'),
            expiration_year=data.get('expiration_year'),
            billing_address=data.get('billing_address'),
            balance=data.get('balance', 0.00),
            is_default=data.get('is_default', False)
        )
        return jsonify({
            'message': 'Payment method added',
            'payment_method_id': payment_method.id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500
    
@customer_bp.route('/customers/<int:customer_id>/payment-methods', methods=['GET'])
def get_payment_methods(customer_id):
    try:
        payment_methods = customer_service.get_customer_payment_methods(customer_id=customer_id)
        return jsonify({
            'payment_methods': [{
                'id': pm.id,
                'card_number': pm.card_number,
                'expiration_month': pm.expiration_month,
                'expiration_year': pm.expiration_year,
                'balance': float(pm.balance),
                'is_default': pm.is_default
            } for pm in payment_methods]
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500
    
@customer_bp.route('/payment-methods/<int:payment_method_id>', methods=['DELETE'])
def delete_payment_method(payment_method_id):
    try:
        customer_service.delete_payment_method(payment_method_id)
        return jsonify({'message': 'Payment method deleted'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500

@customer_bp.route('/payment-methods/<int:payment_method_id>/add-funds', methods=['POST'])
def add_funds(payment_method_id):
    try:
        data = request.get_json()
        amount = data.get('amount')
        
        payment_method = customer_service.add_funds_to_payment_method(payment_method_id, amount)
        return jsonify({
            'message': 'Funds added successfully',
            'new_balance': float(payment_method.balance)
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500

@customer_bp.route('/customers/<int:customer_id>/cart', methods=['POST'])
def add_to_cart(customer_id):
    try:
        data = request.get_json()
        cart_item = customer_service.create_cart_item(
            customer_id=customer_id,
            product_id=data.get('product_id'),
            quantity=data.get('quantity', 1)
        )
        return jsonify({
            'message': 'Item added to cart',
            'cart_item_id': cart_item.id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500
    
@customer_bp.route('/cart/<int:cart_item_id>', methods=['PUT'])
def update_cart_item(cart_item_id):
    try:
        data = request.get_json()
        quantity = data.get('quantity')
        
        cart_item = customer_service.update_cart_item(cart_item_id, quantity)
        return jsonify({
            'message': 'Cart item updated',
            'cart_item_id': cart_item.id,
            'new_quantity': cart_item.quantity
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500
    
@customer_bp.route('/cart/<int:cart_item_id>', methods=['DELETE'])
def delete_cart_item(cart_item_id):
    try:
        customer_service.delete_cart_item(cart_item_id)
        return jsonify({'message': 'Cart item deleted'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500
    
@customer_bp.route('/customers/<int:user_id>/showings', methods=['POST'])
def create_customer_showing(user_id):
    try:
        data = request.get_json()
        customer_showing = customer_service.create_customer_showing(
            user_id=user_id,
            movie_showing_id=data.get('movie_showing_id'),
            seat_id=data.get('seat_id')
        )
        return jsonify({
            'message': 'Showing booked successfully',
            'customer_showing_id': customer_showing.id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500
    
@customer_bp.route('/deliveries', methods=['POST'])
def create_delivery():
    try:
        data = request.get_json()
        delivery = customer_service.create_delivery(
            driver_id=data.get('driver_id'),
            customer_showing_id=data.get('customer_showing_id'),
            payment_method_id=data.get('payment_method_id'),
            staff_id=data.get('staff_id')
        )
        
        if not delivery:
            return jsonify({'error': 'Insufficient funds'}), 402
        
        return jsonify({
            'message': 'Delivery created successfully',
            'delivery_id': delivery.id,
            'total_price': float(delivery.total_price)
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500
    
@customer_bp.route('/deliveries/<int:delivery_id>/complete-payment', methods=['POST'])
def complete_delivery_payment(delivery_id):
    try:
        delivery = customer_service.complete_delivery_payment(delivery_id)
        return jsonify({
            'message': 'Payment completed',
            'delivery_id': delivery.id,
            'payment_status': delivery.payment_status
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500

@customer_bp.route('/deliveries/<int:delivery_id>/cancel', methods=['POST'])
def cancel_delivery(delivery_id):
    try:
        delivery = customer_service.cancel_delivery(delivery_id)
        return jsonify({
            'message': 'Delivery cancelled',
            'delivery_id': delivery.id,
            'delivery_status': delivery.delivery_status
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500