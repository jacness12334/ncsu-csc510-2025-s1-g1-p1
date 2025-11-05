from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from services.user_service import UserService

user_bp = Blueprint('user', __name__, url_prefix='/api/users')
user_service = UserService()

@user_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        user = user_service.create_user(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            birthday=data.get('birthday'),
            password=data.get('password'),
            role=data.get('role')
        )
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'User registration failed'}), 500
    
@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = user_service.validate_credentials(email, password)
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        login_user(user)
        
        return jsonify({
            'message': 'Logged in successfully',
            'user_id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500

@user_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@user_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    return jsonify({
        'user_id': current_user.id,
        'name': current_user.name,
        'email': current_user.email,
        'phone': current_user.phone,
        'birthday': str(current_user.birthday),
        'role': current_user.role
    }), 200
    
@user_bp.route('/me', methods=['PUT'])
@login_required
def update_profile():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        birthday = data.get('birthday')
        
        if not all([name, email, phone, birthday]):
            return jsonify({'error': 'All fields are required'}), 400
        
        user = user_service.update_user_profile(
            user_id=current_user.id,
            name=name,
            email=email,
            phone=phone,
            birthday=birthday
        )
        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'birthday': str(user.birthday)
            }
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Profile update failed'}), 500
    
@user_bp.route('/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    try:
        if current_user.id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        user_service.delete_user(user_id)
        
        logout_user()
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'User deletion failed'}), 500

@user_bp.route('/me/password', methods=['PUT'])
@login_required
def change_password():
    try:
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Current password and new password are required'}), 400
        
        user_service.change_password(
            user_id=current_user.id,
            current_password=current_password,
            new_password=new_password
        )
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Password change failed'}), 500