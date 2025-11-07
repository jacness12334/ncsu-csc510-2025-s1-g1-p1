from app.models import Users
from app.app import db
from argon2 import PasswordHasher


# Service for managing users: creation, retrieval, authentication, and updates
class UserService:

    # Initialize password hasher dependency
    def __init__(self):
        self.ph = PasswordHasher()

    # Generate a secure hash for a plaintext password
    def generate_password_hash(self, password):
        password_hash = self.ph.hash(password)
        return password_hash

    # Verify a plaintext password against a stored hash
    def check_password_hash(self, password_hash, password):
        try:
            self.ph.verify(password_hash, password)
            return True
        except:
            return False
        
    # Validate credentials and return the user if valid; None if invalid
    def validate_credentials(self, email, password):
        if not email or not password:
            raise ValueError("Fields cannot be empty")
        
        user = Users.query.filter_by(email=email).first()
        if not user: return None

        if not self.check_password_hash(password_hash=user.password_hash, password=password):
            return None
        return user

    # Create a new user after validating fields, role, and uniqueness
    def create_user(self, name, email, phone, birthday, password, role):
        if not all([name, email, phone, birthday, password, role]):
            raise ValueError("Fields cannot be empty")
        
        existing_email = Users.query.filter_by(email=email).first()
        if existing_email:
            raise ValueError("Email already in use")
        
        existing_phone = Users.query.filter_by(phone=phone).first()
        if existing_phone:
            raise ValueError("Phone already in use")
        
        if role not in ['customer', 'driver', 'staff', 'supplier']:
            raise ValueError("Role must be customer, driver, staff, or supplier")
        
        password_hash=self.generate_password_hash(password)
        user = Users(
            name=name,
            email=email,
            phone=phone,
            birthday=birthday,
            password_hash=password_hash,
            role = role
        )

        db.session.add(user)
        db.session.commit()
        return user
    
    # Delete a user by id
    def delete_user(self, user_id):
        user = self.get_user(user_id=user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        db.session.delete(user)
        db.session.commit()
        return True
    
    # Retrieve a user by id or None if missing
    def get_user(self, user_id):
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return None
        return user
        
    # Update user profile fields with empty/uniqueness checks
    def update_user_profile(self, user_id, name, email, phone, birthday):
        user = self.get_user(user_id=user_id)
        if not user:
            raise ValueError("User not found")
        
        if not name or not email or not phone or not birthday:
            raise ValueError("Fields cannot be empty")
        
        if Users.query.filter(Users.email == email, Users.id != user_id).first():
            raise ValueError("Email already in use")
        user.email = email

        if Users.query.filter(Users.phone == phone, Users.id != user_id).first():
            raise ValueError("Phone number already in use")
        user.phone = phone
        user.name = name
        user.birthday = birthday

        db.session.commit()
        return user
    
    # Change password after verifying the current password
    def change_password(self, user_id, current_password, new_password):
        user = self.get_user(user_id=user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        if not self.check_password_hash(user.password_hash, current_password):
            raise ValueError("Invalid credentials")
        
        user.password_hash = self.generate_password_hash(new_password)
        db.session.commit()
        return user
