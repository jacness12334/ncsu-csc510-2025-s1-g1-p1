import json

class TestUserRoutes:
        
    def test_register_success(self, client):
        response = client.post('/api/users/register', json={
            'name': 'New User',
            'email': 'newuser@example.com',
            'phone': '1112223333',
            'birthday': '1993-06-10',
            'password': 'mypassword',
            'role': 'customer'
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'User registered successfully'
        assert data['name'] == 'New User'
        assert data['email'] == 'newuser@example.com'
        assert data['role'] == 'customer'
        assert 'user_id' in data
    
    def test_register_missing_fields(self, client):
        response = client.post('/api/users/register', json={
            'name': 'Incomplete User',
            'email': 'incomplete@example.com',
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_register_duplicate_email(self, client, sample_user):
        response = client.post('/api/users/register', json={
            'name': 'Duplicate User',
            'email': 'test@example.com',  
            'phone': '9998887777',
            'birthday': '1990-01-01',
            'password': 'password',
            'role': 'customer'
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_register_duplicate_phone(self, client, sample_user):
        response = client.post('/api/users/register', json={
            'name': 'Duplicate Phone User',
            'email': 'different@example.com',
            'phone': '1234567890',  
            'birthday': '1990-01-01',
            'password': 'password',
            'role': 'customer'
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_login_success(self, client, sample_user):
        response = client.post('/api/users/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Logged in successfully'
        assert data['email'] == 'test@example.com'
        assert data['name'] == 'Test User'
        assert data['role'] == 'customer'
        assert 'user_id' in data
    
    def test_login_wrong_password(self, client, sample_user):
        response = client.post('/api/users/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Invalid email or password' in data['error']
    
    def test_login_nonexistent_user(self, client):
        response = client.post('/api/users/login', json={
            'email': 'nobody@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Invalid email or password' in data['error']
    
    def test_login_missing_email(self, client):
        response = client.post('/api/users/login', json={
            'password': 'password123'
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Email and password are required' in data['error']
    
    def test_login_missing_password(self, client):
        response = client.post('/api/users/login', json={
            'email': 'test@example.com'
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Email and password are required' in data['error']
        
    def test_logout_success(self, authenticated_client):
        response = authenticated_client.post('/api/users/logout')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Logged out successfully'
        
        response = authenticated_client.get('/api/users/me')
        assert response.status_code == 401
    
    def test_logout_not_authenticated(self, client):
        response = client.post('/api/users/logout')
        assert response.status_code == 401  
        
    def test_get_current_user_authenticated(self, authenticated_client):
        response = authenticated_client.get('/api/users/me')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['email'] == 'test@example.com'
        assert data['name'] == 'Test User'
        assert data['role'] == 'customer'
        assert 'user_id' in data
        assert 'phone' in data
        assert 'birthday' in data
    
    def test_get_current_user_not_authenticated(self, client):
        response = client.get('/api/users/me')
        
        assert response.status_code == 401  

    def test_update_profile_success(self, authenticated_client):
        response = authenticated_client.put('/api/users/me', json={
            'name': 'Updated Name',
            'email': 'updated@example.com',
            'phone': '5554443333',
            'birthday': '1992-08-15'
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Profile updated successfully'
        assert data['user']['name'] == 'Updated Name'
        assert data['user']['email'] == 'updated@example.com'
        assert data['user']['phone'] == '5554443333'
        assert data['user']['birthday'] == '1992-08-15'
    
    def test_update_profile_missing_fields(self, authenticated_client):
        response = authenticated_client.put('/api/users/me', json={
            'name': 'Updated Name',
            'email': 'updated@example.com',
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'All fields are required' in data['error']
    
    def test_update_profile_not_authenticated(self, client):
        response = client.put('/api/users/me', json={
            'name': 'Updated Name',
            'email': 'updated@example.com',
            'phone': '5554443333',
            'birthday': '1992-08-15'
        })
        
        assert response.status_code == 401  
    
    def test_update_profile_duplicate_email(self, client, app):
        with app.app_context():
            from app.services.user_service import UserService
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
        
        client.post('/api/users/login', json={
            'email': 'user2@example.com',
            'password': 'password123'
        })
        
        response = client.put('/api/users/me', json={
            'name': 'User Two',
            'email': 'user1@example.com',  
            'phone': '2222222222',
            'birthday': '1990-01-01'
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        
    def test_delete_user_success(self, client, sample_user):
        client.post('/api/users/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        response = client.delete(f'/api/users/{sample_user}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'User deleted successfully'
        
        response = client.get('/api/users/me')
        assert response.status_code == 401
    
    def test_delete_user_not_authenticated(self, client, sample_user):
        response = client.delete(f'/api/users/{sample_user}')
        
        assert response.status_code == 401  
    
    def test_delete_user_unauthorized(self, client, app):
        with app.app_context():
            from app.services.user_service import UserService
            user_service = UserService()
            
            user1 = user_service.create_user(
                name='User One',
                email='user1@example.com',
                phone='1111111111',
                birthday='1990-01-01',
                password='password123',
                role='customer'
            )
            user1_id = user1.id
            
            user2 = user_service.create_user(
                name='User Two',
                email='user2@example.com',
                phone='2222222222',
                birthday='1990-01-01',
                password='password123',
                role='customer'
            )
            user2_id = user2.id
        
        client.post('/api/users/login', json={
            'email': 'user1@example.com',
            'password': 'password123'
        })
        
        response = client.delete(f'/api/users/{user2_id}')
        
        assert response.status_code == 403  
        data = json.loads(response.data)
        assert 'Unauthorized' in data['error']
        
    def test_change_password_success(self, authenticated_client):
        response = authenticated_client.put('/api/users/me/password', json={
            'current_password': 'password123',
            'new_password': 'newpassword456'
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Password changed successfully'
    
    def test_change_password_wrong_current(self, authenticated_client):
        response = authenticated_client.put('/api/users/me/password', json={
            'current_password': 'wrongpassword',
            'new_password': 'newpassword456'
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_change_password_missing_fields(self, authenticated_client):
        response = authenticated_client.put('/api/users/me/password', json={
            'current_password': 'password123'
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Current password and new password are required' in data['error']
    
    def test_change_password_not_authenticated(self, client):
        response = client.put('/api/users/me/password', json={
            'current_password': 'password123',
            'new_password': 'newpassword456'
        })
        
        assert response.status_code == 401  
        
    def test_complete_user_flow(self, client):
        response = client.post('/api/users/register', json={
            'name': 'Flow User',
            'email': 'flow@example.com',
            'phone': '5556667777',
            'birthday': '1995-03-15',
            'password': 'initialpass',
            'role': 'customer'
        })
        assert response.status_code == 201
        user_data = json.loads(response.data)
        user_id = user_data['user_id']
        
        response = client.post('/api/users/login', json={
            'email': 'flow@example.com',
            'password': 'initialpass'
        })
        assert response.status_code == 200
        
        response = client.get('/api/users/me')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Flow User'
        
        response = client.put('/api/users/me', json={
            'name': 'Flow User Updated',
            'email': 'flowupdated@example.com',
            'phone': '5556667777',
            'birthday': '1995-03-15'
        })
        assert response.status_code == 200
        
        response = client.put('/api/users/me/password', json={
            'current_password': 'initialpass',
            'new_password': 'newpass123'
        })
        assert response.status_code == 200
        
        response = client.delete(f'/api/users/{user_id}')
        assert response.status_code == 200
        
        response = client.post('/api/users/login', json={
            'email': 'flowupdated@example.com',
            'password': 'newpass123'
        })
        assert response.status_code == 401
