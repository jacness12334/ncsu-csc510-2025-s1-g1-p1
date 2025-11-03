from models import *
from app import db, get_app

config_name = 'development'
app = get_app(config_name)

with app.app_context():
    pass

class StaffService:

    def __init__(self, user_id):
        self.user_id = user_id
    

    # Admin functionality - add staff member
    def add_staff(self, name, email, phone, birthday, password, theatre_id, role):
        admin = Staff.query.filter_by(user_id=self.user_id).first()
        if not admin or admin.role != 'admin':
            return {"error":"Unauthorized User - Not an admin"}, 403
        
        if Users.query.filter((Users.email == email) | (Users.phone == phone)).first():
            return {"error": "User already exists"}, 400
        
        if role not in ['admin', 'runner']:
            return {"error": "Invalid role. Must be 'admin' or 'runner'."}, 400
        
        # Hash password
        user = Users(name=name, email=email, phone=phone, birthday=birthday, password_hash=password, role='staff', account_status='active')
        db.session.add(user)
        db.session.flush()

        staff = Staff(user_id=user.id, theatre_id=theatre_id, role=role, is_available=True)
        db.session.add(staff)
        db.session.commit()
        return {"message": "Staff member created successfully", "user_id": user.id, "staff_role": staff.role}, 201
        

    # Admin functionality - remove staff member
    def remove_staff(self, staff_user_id):
        admin = Staff.query.filter_by(user_id=self.user_id).first()
        if not admin or admin.role != 'admin':
            return {"error":"Unauthorized User - Not an admin"}, 403
        
        staff = Staff.query.filter_by(user_id=staff_user_id).first()
        if not staff:
            return {"error":"User not found"}, 404
        
        db.session.delete(staff)
        # Maybe delete user too
        db.session.commit()
        return {"message":"Staff successfully removed"}, 200
    

    # Admin functionality - Set theatre status
    def set_theatre_status(self, theatre_id, is_open):
        admin = Staff.query.filter_by(user_id=self.user_id).first()
        if not admin or admin.role != 'admin':
            return {"error":"Unauthorized User - Not an admin"}, 403
        
        theatre = Theatres.query.filter_by(id=theatre_id).first()
        if not theatre:
            return {"error":"Theatre not found"}, 404
        
        theatre.is_open = is_open
        db.session.commit()
        return {"message":f"Theatre {'opened' if is_open else 'closed'}"}, 200
    

    # Admin functionality - add movie
    def add_movie(self, title, genre, length_mins, release_year, keywords, rating):
        admin = Staff.query.filter_by(user_id=self.user_id).first()
        if not admin or admin.role != 'admin':
            return {"error":"Unauthorized User - Not an admin"}, 403
        
        movie = Movies(title=title, genre=genre, length_mins=length_mins, release_year=release_year, keywords=keywords, rating=rating)
        db.session.add(movie)
        db.session.commit()
        return {"message":"Movie added successfully", "movie_id": movie.id}, 201
    

    # Admin functionality - edit movie
    def edit_movie(self, movie_id, title, genre, length_mins, release_year, keywords, rating):
        admin = Staff.query.filter_by(user_id=self.user_id).first()
        if not admin or admin.role != 'admin':
            return {"error":"Unauthorized User - Not an admin"}, 403
        
        movie = Movies.query.filter_by(id=movie_id).first()
        if not movie:
            return {"error":"Movie not found"}, 404

        movie.title = title
        movie.genre = genre
        movie.length_mins = length_mins
        movie.release_year = release_year
        movie.keywords = keywords
        movie.rating = rating
        db.session.commit()
        return {"message":"Movie details changed successfully", "movie_id": movie.id}, 200
    

    # Admin functionality - remove movie
    def remove_movie(self, movie_id):
        admin = Staff.query.filter_by(user_id=self.user_id).first()
        if not admin or admin.role != 'admin':
            return {"error":"Unauthorized User - Not an admin"}, 403
        
        movie = Movies.query.filter_by(id=movie_id).first()
        if not movie:
            return {"error":"Movie not found"}, 404
        
        db.session.delete(movie)
        db.session.commit()
        return {"message":"Movie successfully removed"}, 200


    # Admin functionality - create movie showing
    def add_showing(self, movie_id, auditorium_id, start_time):
        admin = Staff.query.filter_by(user_id=self.user_id).first()
        if not admin or admin.role != 'admin':
            return {"error":"Unauthorized User - Not an admin"}, 403

        movie = Movies.query.filter_by(id=movie_id).first()
        if not movie:
            return {"error":"Movie not found"}, 404
        auditorium = Auditoriums.query.filter_by(id=auditorium_id).first()
        if not auditorium:
            return {"error":"Auditorium not found"}, 404
        
        showing = MovieShowings(movie_id=movie_id, auditorium_id=auditorium_id, start_time=start_time)
        db.session.add(showing)
        db.session.commit()
        return {"message":"Movie Showing created successfully", "showing_id": showing.id}, 201
    

    # Admin functionality - edit movie showing
    def edit_showing(self, showing_id, movie_id, auditorium_id, start_time):
        admin = Staff.query.filter_by(user_id=self.user_id).first()
        if not admin or admin.role != 'admin':
            return {"error":"Unauthorized User - Not an admin"}, 403

        movie = Movies.query.filter_by(id=movie_id).first()
        if not movie:
            return {"error":"Movie not found"}, 404
        auditorium = Auditoriums.query.filter_by(id=auditorium_id).first()
        if not auditorium:
            return {"error":"Auditorium not found"}, 404
        
        showing = MovieShowings.query.filter_by(id=showing_id).first()
        if not showing:
            return {"error":"Movie Showing not found"}, 404
        
        showing.movie_id = movie_id
        showing.auditorium_id = auditorium_id
        showing.start_time = start_time
        db.session.commit()
        return {"message":"Movie Showing details changed successfully", "showing_id": showing.id}, 200
    

    # Admin functionality - remove movie
    def remove_showing(self, showing_id):
        admin = Staff.query.filter_by(user_id=self.user_id).first()
        if not admin or admin.role != 'admin':
            return {"error":"Unauthorized User - Not an admin"}, 403
        
        showing = MovieShowings.query.filter_by(id=showing_id).first()
        if not showing:
            return {"error":"Movie Showing not found"}, 404
        
        db.session.delete(showing)
        db.session.commit()
        return {"message":"Movie Showing successfully removed"}, 200


    # Staff functionality - set availability
    def set_availability(self, is_available):
        staff = Staff.query.filter_by(user_id=self.user_id).first()
        if not staff :
            return {"error":"Unauthorized User - Not a staff member"}, 403
        
        staff.is_available = is_available
        db.session.commit()
        return {"message":f"Availability set to {is_available}"}, 200
    

    # Staff functionality - update delivery status
    def update_delivery_status(self, delivery_id, delivery_status):
        staff = Staff.query.filter_by(user_id=self.user_id).first()
        if not staff :
            return {"error":"Unauthorized User - Not a staff member"}, 403

        valid = ['accepted', 'in_progress', 'ready_for_pickup', 'in_transit', 'delivered', 'fulfilled', 'cancelled']
        if delivery_status not in valid:
            return {"error": "Invalid status"}, 400

        delivery = Deliveries.query.filter_by(id=delivery_id, staff_id=staff.id).first()
        if not delivery:
            return {"error": "Delivery not found"}, 404

        delivery.delivery_status = delivery_status
        db.session.commit()
        return {"message": f"Delivery status updated to {delivery_status}"}, 200
    

    # Staff functionality - accept delivery
    def accept_delivery(self, delivery_id):
        staff = Staff.query.filter_by(user_id=self.user_id).first()
        if not staff :
            return {"error":"Unauthorized User - Not a staff member"}, 403

        delivery = Deliveries.query.get(delivery_id)
        if not delivery:
            return {"error": "Delivery not found"}, 404

        if delivery.delivery_status != 'pending':
            return {"error": "Delivery not available to accept"}, 400

        delivery.staff_id = staff.id
        delivery.delivery_status = 'accepted'
        db.session.commit()
        return {"message": "Delivery accepted successfully"}, 200
