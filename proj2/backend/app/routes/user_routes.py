from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.services.user_service import UserService
from datetime import timedelta


# Blueprint for user-related API routes 
user_bp = Blueprint('user', __name__, url_prefix='/api/users')
user_service = UserService()


# Register a new user account
@user_bp.route('/register', methods=['POST'])
def register():
    """
    Register User
    ---
    tags: [User Management]
    description: Registers a new user account.
    parameters:
      - in: body
        name: registration_data
        schema: {$ref: '#/definitions/UserRegistration'}
    responses:
      201:
        description: User registered successfully
        schema: {$ref: '#/definitions/UserResponse'}
      400: {description: Invalid input}
    """
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
        return jsonify({'error': 'User registration failed: ' + str(e)}), 500


# Log in a user and create a session
@user_bp.route('/login', methods=['POST'])
def login():
    """
    Log In User
    ---
    tags: [User Management]
    description: Authenticates a user and starts a session.
    parameters:
      - in: body
        name: login_credentials
        schema: {$ref: '#/definitions/UserLogin'}
    responses:
      200:
        description: Logged in successfully
        schema: {$ref: '#/definitions/UserResponse'}
      401: {description: Invalid email or password}
    """
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = user_service.validate_credentials(email, password)
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        login_user(user, remember=True, duration=timedelta(days=1))
        
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


# Log out the current user
@user_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Log Out User
    ---
    tags: [User Management]
    description: Logs out the current authenticated user.
    responses:
      200:
        description: Logged out successfully
        schema:
          properties:
            message: {type: string}
    """
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200


# Get the current authenticated user's profile
@user_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """
    Get Current User Profile
    ---
    tags: [User Management]
    description: Retrieves the profile details of the current authenticated user.
    responses:
      200:
        description: User profile retrieved successfully
        schema: {$ref: '#/definitions/UserProfile'}
      401: {description: Unauthorized - Login required}
    """
    return jsonify({
        'user_id': current_user.id,
        'name': current_user.name,
        'email': current_user.email,
        'phone': current_user.phone,
        'birthday': str(current_user.birthday),
        'role': current_user.role
    }), 200

# Get user from given id
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    return jsonify({
        'user_id': user.id,
        'name': user.name,
        'email': user.email,
        'phone': user.phone,
        'birthday': str(user.birthday),
        'role': user.role
    }), 200


# Update the current authenticated user's profile
@user_bp.route('/me', methods=['PUT'])
@login_required
def update_profile():
    """
    Update User Profile
    ---
    tags: [User Management]
    description: Updates the profile information for the current authenticated user.
    parameters:
      - in: body
        name: profile_update
        schema: {$ref: '#/definitions/UserUpdate'}
    responses:
      200:
        description: Profile updated successfully
        schema:
          properties:
            message: {type: string}
            user: {$ref: '#/definitions/UserProfile'}
      400: {description: Invalid input}
    """
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


# Delete the current authenticated user's account
@user_bp.route('/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    """
    Delete User Account
    ---
    tags: [User Management]
    description: Deletes the current authenticated user's account (only self-deletion allowed).
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: The ID of the user account to delete.
    responses:
      200:
        description: User deleted successfully
        schema:
          properties:
            message: {type: string}
      403: {description: Unauthorized}
      404: {description: User not found}
    """
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


# Change the current authenticated user's password
@user_bp.route('/me/password', methods=['PUT'])
@login_required
def change_password():
    """
    Change User Password
    ---
    tags: [User Management]
    description: Changes the password for the current authenticated user.
    parameters:
      - in: body
        name: password_change
        schema: {$ref: '#/definitions/PasswordChange'}
    responses:
      200:
        description: Password changed successfully
        schema:
          properties:
            message: {type: string}
      400: {description: Invalid input or current password incorrect}
    """
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
  
