from app.models import Users
from app.app import db
from argon2 import PasswordHasher

class UserService:
    """Service for managing users: creation, retrieval, authentication, and updates.
    
    This module encapsulates user-related operations and password handling using Argon2.
    """

    def __init__(self):
        """Initialize dependencies (password hasher)."""
        self.ph = PasswordHasher()

    def generate_password_hash(self, password):
        """Generate a secure Argon2 hash for a plaintext password.

        Args:
            password: Plaintext password.

        Returns:
            str: Encoded Argon2 hash string.
        """
        password_hash = self.ph.hash(password)
        return password_hash

    def check_password_hash(self, password_hash, password):
        """Verify a plaintext password against a stored Argon2 hash.

        Args:
            password_hash: Stored Argon2 hash.
            password: Plaintext password to verify.

        Returns:
            bool: True if the password matches the hash; otherwise False.
        """
        try:
            self.ph.verify(password_hash, password)
            return True
        except:
            return False
        
    def validate_credentials(self, email, password):
        """Validate user credentials and return the user if valid.

        Args:
            email: User email address.
            password: Plaintext password.

        Returns:
            Users | None: The user object if credentials are correct; otherwise None.

        Raises:
            ValueError: If email or password is empty.
        """
        if not email or not password:
            raise ValueError("Fields cannot be empty")
        
        user = Users.query.filter_by(email=email).first()
        if not user: return None

        if not self.check_password_hash(password_hash=user.password_hash, password=password):
            return None
        return user

    def create_user(self, name, email, phone, birthday, password, role):
        """Create a new user with uniqueness and role validation.

        Args:
            name: Full name.
            email: Unique email address.
            phone: Unique phone number.
            birthday: Date of birth (YYYY-MM-DD or date).
            password: Plaintext password (will be hashed).
            role: One of 'customer', 'driver', 'staff', 'supplier'.

        Returns:
            Users: The created user record.

        Raises:
            ValueError: If any field is empty, email/phone already used, or role invalid.
        """
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
        
        password_hash = self.generate_password_hash(password)
        user = Users(
            name=name,
            email=email,
            phone=phone,
            birthday=birthday,
            password_hash=password_hash,
            role=role
        )

        db.session.add(user)
        db.session.commit()
        return user
    
    def delete_user(self, user_id):
        """Delete a user by id.

        Args:
            user_id: The user's primary key.

        Returns:
            bool: True if the user was deleted.

        Raises:
            ValueError: If the user is not found.
        """
        user = self.get_user(user_id=user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        db.session.delete(user)
        db.session.commit()
        return True
    
    def get_user(self, user_id):
        """Retrieve a user by id.

        Args:
            user_id: The user's primary key.

        Returns:
            Users | None: The user if found; otherwise None.
        """
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return None
        return user
        
    def update_user_profile(self, user_id, name, email, phone, birthday):
        """Update user profile fields with non-empty and uniqueness checks.

        Args:
            user_id: The user's primary key.
            name: New name.
            email: New email (must be unique).
            phone: New phone (must be unique).
            birthday: New birthday.

        Returns:
            Users: The updated user record.

        Raises:
            ValueError: If the user is missing, any field is empty, or email/phone duplicates another user.
        """
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
    
    def change_password(self, user_id, current_password, new_password):
        """Change a user's password after verifying the current password.

        Args:
            user_id: The user's primary key.
            current_password: Current plaintext password.
            new_password: New plaintext password to set.

        Returns:
            Users: The user record with updated password hash.

        Raises:
            ValueError: If the user is missing or current password is invalid.
        """
        user = self.get_user(user_id=user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        if not self.check_password_hash(user.password_hash, current_password):
            raise ValueError("Invalid credentials")
        
        user.password_hash = self.generate_password_hash(new_password)
        db.session.commit()
        return user
