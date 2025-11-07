import json
from app.app import db
from app.models import *

class TestStaffRoutes:

    def test_add_staff_success(self, client, sample_theatre, sample_admin):
        response = client.post('/api/staff', json={
            'user_id': sample_admin,
            'name': 'Test Staff',
            'email': 'staff@example.com',
            'phone': '5559998888',
            'birthday': '1985-05-15',
            'password': 'password123',
            'role': 'runner',
            'theatre_id': sample_theatre
        })

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Staff member created successfully'
        assert data['user_id'] is not None
        assert data['staff_role'] == "runner"

    def test_add_staff_missing_fields(self, client, sample_admin):
        # Test missing required fields for staff creation
        response = client.post('/api/staff', json={
            'user_id': sample_admin,
            'name': 'Incomplete Staff'
        })

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == "Missing required fields"

    def test_add_staff_invalid_role(self, client, sample_admin, sample_theatre):
        response = client.post('/api/staff', json={
            'user_id': sample_admin,
            'name': 'Invalid Role Staff',
            'email': 'invalid@example.com',
            'phone': '5558887777',
            'birthday': '1990-05-15',
            'password': 'password123',
            'role': 'customer',
            'theatre_id': sample_theatre
        })

        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['error'] == "Invalid role. Must be 'admin' or 'runner'."
    
    def test_create_staff_unauthorized(self, client, sample_staff, sample_theatre):
        response = client.post('/api/staff', json={
            'user_id': sample_staff,
            'name': 'Unauthorized Staff',
            'email': 'unauth@example.com',
            'phone': '5550001111',
            'birthday': '1992-08-25',
            'password': 'password123',
            'role': 'runner',
            'theatre_id': sample_theatre
        })

        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['error'] == "Unauthorized User - Not an admin"

    def test_remove_staff_success(self, client, sample_admin, sample_staff):
        response = client.delete(f'/api/staff/{sample_staff}', json={
            'user_id': sample_admin
        })

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Staff successfully removed'

    def test_remove_staff_not_found(self, client, sample_admin):
        response = client.delete('/api/staff/9999', json={
            'user_id': sample_admin
        })

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'not found' in data['error'] 

    def test_get_theatres_success(self, client, sample_admin, sample_theatre):
        response = client.get(f'/api/theatres/{sample_admin}')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['theatres']) > 0
        assert data['theatres'][0]['id'] == sample_theatre

    def test_set_theatre_status_success(self, client, sample_admin, sample_theatre):
        response = client.put('/api/theatres', json={
            'user_id': sample_admin,
            'theatre_id': sample_theatre,
            'is_open': False
        })

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Theatre closed'

    def test_set_theatre_status_missing_fields(self, client, sample_admin):
        response = client.put('/api/theatres', json={
            'user_id': sample_admin
        })

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == "Missing theatre_id or is_open"
    
    def test_set_theatre_status_invalid_theatre(self, client, sample_admin):
        response = client.put('/api/theatres', json={
            'user_id': sample_admin,
            'theatre_id': 9999,
            'is_open': False
        })

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'not found' in data['error']

    def test_add_movie_success(self, client, sample_admin):
        response = client.post('/api/movies', json={
            'user_id': sample_admin,
            'title': 'Test Movie',
            'genre': 'Action',
            'length_mins': 120,
            'release_year': 2024,
            'keywords': 'test',
            'rating': 4.5
        })

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Movie added successfully'
        assert data['movie_id'] is not None

    def test_add_movie_missing_fields(self, client, sample_admin):
        response = client.post('/api/movies', json={
            'user_id': sample_admin,
            'genre': 'Action',
            'length_mins': 120,
            'release_year': 2024,
            'keywords': 'test',
            'rating': 4.5
        })

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Missing required fields'

    def test_edit_movie_success(self, client, sample_admin, sample_movie):
        response = client.put(f'/api/movies/{sample_movie}', json={
            'user_id': sample_admin,
            'title': 'Updated Test Movie',
            'genre': 'Action',
            'length_mins': 130,
            'release_year': 2025,
            'keywords': 'updated',
            'rating': 4.8
        })

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Movie details changed successfully'
        assert data['movie_id'] == sample_movie

    def test_edit_movie_missing_fields(self, client, sample_admin, sample_movie):
        response = client.put(f'/api/movies/{sample_movie}', json={
            'user_id': sample_admin,
            'title': 'Updated Test Movie',
            'genre': 'Action',
            'length_mins': 130,
            'release_year': 2025,
            'keywords': 'updated'
        })

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Missing required fields'

    def test_edit_movie_invalid_movie(self, client, sample_admin):
        response = client.put(f'/api/movies/{9999}', json={
            'user_id': sample_admin,
            'title': 'Updated Test Movie',
            'genre': 'Action',
            'length_mins': 130,
            'release_year': 2025,
            'keywords': 'updated',
            'rating': 5
        })

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'not found' in data['error']

    def test_remove_movie_success(self, client, sample_admin, sample_movie):
        response = client.delete(f'/api/movies/{sample_movie}', json={
            'user_id': sample_admin
        })

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Movie successfully removed'
    
    def test_remove_movie_invalid_movie(self, client, sample_admin):
        response = client.delete(f'/api/movies/{9999}', json={
            'user_id': sample_admin
        })

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'not found' in data['error']

    def test_add_showing_success(self, client, sample_admin, sample_movie, sample_auditorium):
        response = client.post(f'/api/showings', json={
            'user_id': sample_admin,
            'movie_id': sample_movie,
            'auditorium_id': sample_auditorium,
            'start_time': "2025-01-01T08:00:00.000Z"
        })

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Movie Showing created successfully'
    
    def test_edit_showing_success(self, client, sample_admin, sample_showing, sample_movie, sample_auditorium):
        response = client.put(f'/api/showings/{sample_showing}', json={
            'user_id': sample_admin,
            'movie_id': sample_movie,
            'auditorium_id': sample_auditorium,
            'start_time': "2025-01-01T08:00:00.000Z"
        })

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Movie Showing details changed successfully'

    def test_remove_showing_success(self, client, sample_admin, sample_showing):
        response = client.delete(f'/api/showings/{sample_showing}', json={
            'user_id': sample_admin
        })

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Movie Showing successfully removed'

    def test_set_availability_success(self, client, sample_staff):
        response = client.put(f'/api/staff', json={
            "user_id": sample_staff,
            'is_available': False
        })

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Availability set to False'

    def test_accept_delivery_success(self, client, sample_staff, sample_delivery):
        response = client.put(f'/api/deliveries/{sample_delivery}/accept', json={
            'user_id': sample_staff
        })

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Delivery accepted successfully'
        assert Staff.query.filter_by(user_id=sample_staff).first().is_available is False
        assert Deliveries.query.filter_by(id=sample_delivery).first().delivery_status == 'accepted'
    
    def test_fulfill_delivery_success(self, client, sample_staff, sample_delivery):
        delivery = Deliveries.query.filter_by(id=sample_delivery).first()
        delivery.delivery_status = 'delivered'
        db.session.commit()
        response = client.put(f'/api/deliveries/{sample_delivery}/fulfill', json={
            'user_id': sample_staff
        })

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Delivery fulfilled'
        assert Staff.query.filter_by(user_id=sample_staff).first().is_available is True
        assert Deliveries.query.filter_by(id=sample_delivery).first().delivery_status == 'fulfilled'

    def test_list_staff_by_theatre_success(self, client, sample_admin, sample_theatre, sample_staff):
        response = client.put(f'/api/staff/list/{sample_theatre}', json={
            'user_id': sample_admin,
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'staff' in data
        assert all(s['theatre_id'] == sample_theatre for s in data['staff'])
        assert any(s['user_id'] == sample_staff for s in data['staff'])

    def test_list_staff_by_theatre_unauthorized(self, client, sample_staff, sample_theatre):
        response = client.put(f'/api/staff/list/{sample_theatre}', json={
            'user_id': sample_staff,
        })
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_list_staff_by_theatre_empty(self, client, sample_admin):
        response = client.put(f'/api/staff/list/{9999}', json={
            'user_id': sample_admin,
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'staff' in data
        assert data['staff'] == []

    def test_list_deliveries_by_theatre_success(self, client, sample_admin, sample_theatre):
        response = client.get(f'/api/deliveries/list/{sample_theatre}', json={
            'user_id': sample_admin
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'deliveries' in data
        assert isinstance(data['deliveries'], list)

    def test_list_deliveries_by_theatre_unauthorized(self, client, sample_staff, sample_theatre):
        response = client.get(f'/api/deliveries/list/{sample_theatre}', json={
            'user_id': sample_staff
        })
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_list_deliveries_by_theatre_empty(self, client, sample_admin):
        response = client.get('/api/deliveries/list/999999', json={
            'user_id': sample_admin
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'deliveries' in data
        assert data['deliveries'] == []
