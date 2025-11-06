from app.models import *
from app.app import db
from app.services.user_service import UserService

class StaffService:

    def __init__(self, user_id):
        self.user_id = user_id
        self.user_service = UserService()
    

    def validate_admin(self):
        admin = Staff.query.filter_by(user_id=self.user_id).first()
        if not admin or admin.role != 'admin':
            raise ValueError("Unauthorized User - Not an admin")
        return admin


    def validate_staff(self):
        staff = Staff.query.filter_by(user_id=self.user_id).first()
        if not staff:
            raise ValueError("Unauthorized User - Not a staff member")
        return staff
    

    # Admin functionality - add staff member
    def add_staff(self, name, email, phone, birthday, password, theatre_id, role):
        admin = self.validate_admin()
        
        if role not in ['admin', 'runner']:
            raise ValueError("Invalid role. Must be 'admin' or 'runner'.")
        
        user = self.user_service.create_user(name, email, phone, birthday, password, 'staff')
        db.session.flush()

        staff = Staff(user_id=user.id, theatre_id=theatre_id, role=role, is_available=True)
        db.session.add(staff)
        db.session.commit()
        return staff
        

    # Admin functionality - remove staff member
    def remove_staff(self, staff_user_id):
        admin = self.validate_admin()
        
        user = Users.query.filter_by(id=staff_user_id).first()
        staff = Staff.query.filter_by(user_id=staff_user_id).first()
        if not staff:
            raise ValueError(f"User {staff_user_id} not found")
        
        db.session.delete(staff)
        db.session.delete(user)
        db.session.commit()
    

    def get_theatres(self):
        theatres = Theatres.query.all()
        return theatres
    

    # Admin functionality - Set theatre status
    def set_theatre_status(self, theatre_id, is_open):
        admin = self.validate_admin()
        
        theatre = Theatres.query.filter_by(id=theatre_id).first()
        if not theatre:
            raise ValueError(f"Theatre {theatre_id} not found")
        
        theatre.is_open = is_open
        db.session.commit()
        return theatre
    

    # Admin functionality - add movie
    def add_movie(self, title, genre, length_mins, release_year, keywords, rating):
        admin = self.validate_admin()
        
        movie = Movies(title=title, genre=genre, length_mins=length_mins, release_year=release_year, keywords=keywords, rating=rating)
        db.session.add(movie)
        db.session.commit()
        return movie
    

    # Admin functionality - edit movie
    def edit_movie(self, movie_id, title, genre, length_mins, release_year, keywords, rating):
        admin = self.validate_admin()
        
        movie = Movies.query.filter_by(id=movie_id).first()
        if not movie:
            raise ValueError(f"Movie {movie_id} not found")

        movie.title = title
        movie.genre = genre
        movie.length_mins = length_mins
        movie.release_year = release_year
        movie.keywords = keywords
        movie.rating = rating
        db.session.commit()
        return movie
    

    # Admin functionality - remove movie
    def remove_movie(self, movie_id):
        admin = self.validate_admin()
        
        movie = Movies.query.filter_by(id=movie_id).first()
        if not movie:
            raise ValueError(f"Movie {movie_id} not found")
        
        db.session.delete(movie)
        db.session.commit()


    # Admin functionality - create movie showing
    def add_showing(self, movie_id, auditorium_id, start_time):
        admin = self.validate_admin()

        movie = Movies.query.filter_by(id=movie_id).first()
        if not movie:
            raise ValueError(f"Movie {movie_id} not found")
        auditorium = Auditoriums.query.filter_by(id=auditorium_id).first()
        if not auditorium:
            raise ValueError(f"Auditorium {auditorium_id} not found")
        
        showing = MovieShowings(movie_id=movie_id, auditorium_id=auditorium_id, start_time=start_time)
        db.session.add(showing)
        db.session.commit()
        return showing
    

    # Admin functionality - edit movie showing
    def edit_showing(self, showing_id, movie_id, auditorium_id, start_time):
        admin = self.validate_admin()

        movie = Movies.query.filter_by(id=movie_id).first()
        if not movie:
            raise ValueError(f"Movie {movie_id} not found")
        auditorium = Auditoriums.query.filter_by(id=auditorium_id).first()
        if not auditorium:
            raise ValueError(f"Auditorium {auditorium_id} not found")
        
        showing = MovieShowings.query.filter_by(id=showing_id).first()
        if not showing:
            raise ValueError(f"Movie Showing {showing_id} not found")
        
        showing.movie_id = movie_id
        showing.auditorium_id = auditorium_id
        showing.start_time = start_time
        db.session.commit()
        return showing
    

    # Admin functionality - remove movie
    def remove_showing(self, showing_id):
        admin = self.validate_admin()
        
        showing = MovieShowings.query.filter_by(id=showing_id).first()
        if not showing:
            raise ValueError(f"Movie Showing {showing_id} not found")
        
        db.session.delete(showing)
        db.session.commit()


    # Staff functionality - set availability
    def set_availability(self, is_available):
        staff = self.validate_staff()
        
        staff.is_available = is_available
        db.session.commit()
        return staff
    

    # Staff functionality - update delivery status
    def update_delivery_status(self, delivery_id, delivery_status):
        staff = self.validate_staff()

        valid = ['accepted', 'in_progress', 'ready_for_pickup', 'in_transit', 'delivered', 'fulfilled', 'cancelled']
        if delivery_status not in valid:
            raise ValueError("Invalid status")

        delivery = Deliveries.query.filter_by(id=delivery_id, staff_id=staff.id).first()
        if not delivery:
            raise ValueError("Delivery not found")

        delivery.delivery_status = delivery_status
        db.session.commit()
        return delivery
    

    # Staff functionality - accept delivery
    def accept_delivery(self, delivery_id):
        staff = self.validate_staff()

        delivery = Deliveries.query.get(delivery_id)
        if not delivery:
            raise ValueError("Delivery not found")

        if delivery.delivery_status != 'pending':
            raise ValueError("Delivery not available to accept")

        delivery.staff_id = staff.user_id
        delivery.delivery_status = 'accepted'
        db.session.commit()
        return delivery
