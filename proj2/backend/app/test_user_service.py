import pytest
from services.user_service import UserService

class TestUserService:
    
    def test_create_user_success(self, app):
        with app.app_context():
            user_service = UserService()
            user = user_service.create_user(
                name='John Doe',
                email='john@example.com',
                phone='5551234567',
                birthday='1995-05-15',
                password='securepass',
                role='customer'
            )
            
            assert user is not None
            assert user.name == 'John Doe'
            assert user.email == 'john@example.com'
            assert user.phone == '5551234567'
            assert user.role == 'customer'
            assert user.password_hash is not None
            assert user.password_hash != 'securepass'  
    
    def test_create_user_missing_fields(self, app):
        with app.app_context():
            user_service = UserService()
            
            with pytest.raises(ValueError, match="Fields cannot be empty"):
                user_service.create_user(
                    name='',  
                    email='test@example.com',
                    phone='1234567890',
                    birthday='1990-01-01',
                    password='password',
                    role='customer'
                )
    
    def test_create_user_duplicate_email(self, app, sample_user):
        with app.app_context():
            user_service = UserService()
            
            with pytest.raises(ValueError, match="Email already in use"):
                user_service.create_user(
                    name='Another User',
                    email='test@example.com',  
                    phone='9876543210',
                    birthday='1992-03-20',
                    password='password456',
                    role='driver'
                )
    
    def test_create_user_duplicate_phone(self, app, sample_user):
        with app.app_context():
            user_service = UserService()
            
            with pytest.raises(ValueError, match="Phone already in use"):
                user_service.create_user(
                    name='Another User',
                    email='different@example.com',
                    phone='1234567890',  
                    birthday='1992-03-20',
                    password='password456',
                    role='driver'
                )
    
    def test_validate_credentials_success(self, app, sample_user):
        with app.app_context():
            user_service = UserService()
            user = user_service.validate_credentials('test@example.com', 'password123')
            
            assert user is not None
            assert user.email == 'test@example.com'
            assert user.name == 'Test User'
    
    def test_validate_credentials_wrong_password(self, app, sample_user):
        with app.app_context():
            user_service = UserService()
            user = user_service.validate_credentials('test@example.com', 'wrongpassword')
            
            assert user is None
    
    def test_validate_credentials_nonexistent_user(self, app):
        with app.app_context():
            user_service = UserService()
            user = user_service.validate_credentials('nobody@example.com', 'password')
            
            assert user is None
    
    def test_validate_credentials_empty_fields(self, app):
        with app.app_context():
            user_service = UserService()
            
            with pytest.raises(ValueError, match="Fields cannot be empty"):
                user_service.validate_credentials('', 'password')
            
            with pytest.raises(ValueError, match="Fields cannot be empty"):
                user_service.validate_credentials('test@example.com', '')
    
    def test_get_user_success(self, app, sample_user):
        with app.app_context():
            user_service = UserService()
            user = user_service.get_user(sample_user)
            
            assert user is not None
            assert user.id == sample_user
            assert user.email == 'test@example.com'
            assert user.name == 'Test User'
    
    def test_get_user_not_found(self, app):
        with app.app_context():
            user_service = UserService()
            user = user_service.get_user(99999)  
            
            assert user is None
    
    def test_update_user_profile_success(self, app, sample_user):
        with app.app_context():
            user_service = UserService()
            updated_user = user_service.update_user_profile(
                user_id=sample_user,
                name='Updated Name',
                email='newemail@example.com',
                phone='9998887777',
                birthday='1991-12-25'
            )
            
            assert updated_user.name == 'Updated Name'
            assert updated_user.email == 'newemail@example.com'
            assert updated_user.phone == '9998887777'
            assert str(updated_user.birthday) == '1991-12-25'
    
    def test_update_user_profile_missing_fields(self, app, sample_user):
        with app.app_context():
            user_service = UserService()
            
            with pytest.raises(ValueError, match="Fields cannot be empty"):
                user_service.update_user_profile(
                    user_id=sample_user,
                    name='',  
                    email='test@example.com',
                    phone='1234567890',
                    birthday='1990-01-01'
                )
    
    def test_update_user_profile_duplicate_email(self, app):
        with app.app_context():
            user_service = UserService()
            
            user1 = user_service.create_user(
                name='User One',
                email='user1@example.com',
                phone='1111111111',
                birthday='1990-01-01',
                password='password123',
                role='customer'
            )
            
            user2 = user_service.create_user(
                name='User Two',
                email='user2@example.com',
                phone='2222222222',
                birthday='1990-01-01',
                password='password123',
                role='customer'
            )
            
            with pytest.raises(ValueError, match="Email already in use"):
                user_service.update_user_profile(
                    user_id=user2.id,
                    name='User Two',
                    email='user1@example.com', 
                    phone='2222222222',
                    birthday='1990-01-01'
                )
    
    def test_update_user_profile_not_found(self, app):
        with app.app_context():
            user_service = UserService()
            
            with pytest.raises(ValueError, match="User not found"):
                user_service.update_user_profile(
                    user_id=99999,  
                    name='Test',
                    email='test@example.com',
                    phone='1234567890',
                    birthday='1990-01-01'
                )
    
    def test_change_password_success(self, app, sample_user):
        with app.app_context():
            user_service = UserService()
            
            user_service.change_password(
                user_id=sample_user,
                current_password='password123',
                new_password='newpassword456'
            )
            
            user = user_service.validate_credentials('test@example.com', 'newpassword456')
            assert user is not None
            
            user = user_service.validate_credentials('test@example.com', 'password123')
            assert user is None
    
    def test_change_password_wrong_current(self, app, sample_user):
        with app.app_context():
            user_service = UserService()
            
            with pytest.raises(ValueError, match="Invalid credentials"):
                user_service.change_password(
                    user_id=sample_user,
                    current_password='wrongpassword',
                    new_password='newpassword'
                )
    
    def test_change_password_user_not_found(self, app):
        with app.app_context():
            user_service = UserService()
            
            with pytest.raises(ValueError, match="User 99999 not found"):
                user_service.change_password(
                    user_id=99999, 
                    current_password='password',
                    new_password='newpassword'
                )
    
    def test_delete_user_success(self, app, sample_user):
        with app.app_context():
            user_service = UserService()
            user_id = sample_user
            
            result = user_service.delete_user(user_id)
            assert result is True
            
            user = user_service.get_user(user_id)
            assert user is None
    
    def test_delete_user_not_found(self, app):
        with app.app_context():
            user_service = UserService()
            
            with pytest.raises(ValueError, match="User 99999 not found"):
                user_service.delete_user(99999) 
    
    def test_generate_password_hash(self, app):
        with app.app_context():
            user_service = UserService()
            
            hash1 = user_service.generate_password_hash('password123')
            hash2 = user_service.generate_password_hash('password123')
            
            assert hash1 != hash2
            assert hash1 != 'password123'
            assert hash2 != 'password123'
    
    def test_check_password_hash_correct(self, app):
        with app.app_context():
            user_service = UserService()
            
            password_hash = user_service.generate_password_hash('mypassword')
            result = user_service.check_password_hash(password_hash, 'mypassword')
            
            assert result is True
    
    def test_check_password_hash_incorrect(self, app):
        with app.app_context():
            user_service = UserService()
            
            password_hash = user_service.generate_password_hash('mypassword')
            result = user_service.check_password_hash(password_hash, 'wrongpassword')
            
            assert result is False
