from models import Users
from app import db
from argon2 import PasswordHasher

class UserService:

    def __init__(self):
        self.ph = PasswordHasher()

    def generate_password_hash(self, password):
        password_hash = self.ph.hash(password)
        return password_hash

    def check_password_hash(self, password_hash, password):
        if self.ph.verify(password_hash, password):
            return True
        else:
            return False
        
    def validate_credentials(self, email, password):
        if not email or not password:
            raise ValueError("Fields cannot be empty")
        
        user = Users.query.filter_by(email=email).first()
        hash = user.password_hash
        if not self.check_password_hash(password_hash=hash, password=password):
            return None
        return user

    def create_user(self, name, email, phone, birthday, password, role):
        if not name or not email or not phone or not birthday or not password or not role:
            raise ValueError("Fields cannot be empty")

        user = Users.query.filer_by(email=email, phone=phone).first()
        if user:
            raise ValueError("Email or phone already exists")
        
        user = Users(
            name=name,
            email=email,
            phone=phone,
            birthday=birthday,
            password_hash=self.generate_password_hash(password),
            role = role
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    def delete_user(self, user_id):
        user = Users.query.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        db.session.delete(user)
        db.session.commit()
        return True
    
    def get_user(self, user_id):
        user = Users.query.get(user_id)
        if not user:
            return None
        return user
        
    def update_user_profile(self, user_id, name, email, phone, birthday):
        user = Users.query.get(user_id)
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
        user = Users.query.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        if not self.check_password_hash(user.password_hash, current_password):
            raise ValueError("Invalid credentials")
        
        user.password_hash = self.generate_password_hash(new_password)
        db.session.commit()
        return user
    


    