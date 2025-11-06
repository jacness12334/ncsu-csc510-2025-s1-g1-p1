from app.models import *
from app.app import db
from app.services.user_service import UserService
from sqlalchemy.sql import expression
import datetime

class StaffService:

    # Initialize services
    def __init__(self, user_id):
        self.user_service = UserService()
        self.user_id = user_id

    # Check that user is admin
    def validate_admin(self):
        admin = Staff.query.filter_by(user_id=self.user_id).first()
        if not admin or admin.role != 'admin':
            raise ValueError("Unauthorized User - Not an admin")
        return admin

    # Retrieve the given staff user
    def validate_staff(self, user_id):
        staff = Staff.query.get(user_id)
        if not staff:
            raise ValueError(f"Staff member {user_id} not found")
        return staff

    # (ADMIN FUNCTIONALITY) Add staff member
    def add_staff(self, name, email, phone, birthday, password, theatre_id, staff_role):
        admin = self.validate_admin()

        if staff_role not in ['admin', 'runner']:
            raise ValueError("Staff role must be 'admin' or 'runner'")
        user = self.user_service.create_user(
            name=name, 
            email=email, 
            phone=phone, 
            birthday=birthday, 
            password=password, 
            role='staff'
        )
        staff = Staff(user_id=user.id, theatre_id=theatre_id, role=staff_role)
        db.session.flush()

        db.session.add(staff)
        db.session.commit()
        return staff

    # (ADMIN FUNCTIONALITY) Remove staff member
    def remove_staff(self, staff_user_id):
        admin = self.validate_admin()

        staff = self.validate_staff(staff_user_id)
        self.user_service.delete_user(staff.user_id)
        return True
    
    # (ADMIN FUNCTIONALITY) Close theatre
    def set_theatre_status(self, theatre_id, is_open):
        admin = self.validate_admin()
        
        theatre = Theatres.query.filter_by(id=theatre_id).first()
        if not theatre:
            raise ValueError(f"Theatre {theatre_id} not found")
        
        theatre.is_open = is_open
        db.session.commit()
        return theatre
    
    # (ADMIN FUNCTIONALITY) Add movie
    def add_movie(self, title, genre, length_mins, release_year, keywords, rating):
        admin = self.validate_admin()

        movie = Movies(title=title, genre=genre, length_mins=length_mins, release_year=release_year, keywords=keywords, rating=rating)
        db.session.add(movie)
        db.session.commit()
        return True
    
    # (ADMIN FUNCTIONALITY) Edit movie
    def edit_movie(self, movie_id, title, genre, length_mins, release_year, keywords, rating):
        admin = self.validate_admin()

        movie = Movies.query.get(movie_id)
        if not movie:
            raise ValueError(f"Movie {movie_id} not found")

        movie.title = title
        movie.genre = genre
        movie.length_mins = length_mins
        movie.release_year = release_year
        movie.keywords = keywords
        movie.rating = rating
        db.session.commit()
        return True

    # (ADMIN FUNCTIONALITY) Remove movie
    def remove_movie(self, movie_id):
        admin = self.validate_admin()

        movie = Movies.query.get(movie_id)
        if not movie:
            raise ValueError(f"Movie {movie_id} not found")
        db.session.delete(movie)
        db.session.commit()
        return True


    # (ADMIN FUNCTIONALITY) Create movie showing
    def add_showing(self, movie_id, auditorium_id, start_time):
        admin = self.validate_admin()

        movie = Movies.query.filter_by(id=movie_id).first()
        if not movie:
            raise ValueError(f"Movie {movie_id} not found")
        
        auditorium = Auditoriums.query.filter_by(id=auditorium_id).first()
        if not auditorium:
            raise ValueError(f"Auditorium {auditorium_id} not found")
        
        if not isinstance(start_time, datetime.date):
            raise ValueError(f"Movie start time must be in DateTime format")
        
        showing = MovieShowings(movie_id=movie_id, auditorium_id=auditorium_id, start_time=start_time)
        db.session.add(showing)
        db.session.commit()
        return showing
    

    # (ADMIN FUNCTIONALITY) Edit movie showing
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
            raise ValueError(f"Movie showing {showing_id} not found")
        
        if not isinstance(start_time, datetime.datetime):
            raise ValueError(f"Movie start time must be in DateTime format")
        
        showing.movie_id = movie_id
        showing.auditorium_id = auditorium_id
        showing.start_time = start_time
        db.session.commit()
        return showing
    

    # (ADMIN FUNCTIONALITY) Remove movie showing
    def remove_showing(self, showing_id):
        admin = self.validate_admin()

        showing = MovieShowings.query.filter_by(id=showing_id).first()
        if not showing:
            raise ValueError(f"Movie showing {showing_id} not found")
        db.session.delete(showing)
        db.session.commit()
        return showing

    # Set staff availability
    def set_availability(self, staff_id, availability):
        staff = self.validate_staff(staff_id)
        staff.is_available = availability
        db.session.commit()
        return staff

    # Fulfill delivery
    def fulfill_delivery(self, user_id, delivery_id):
        staff = self.validate_staff(user_id)
        delivery = Deliveries.query.filter_by(delivery_id=delivery_id).first()

        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        if delivery.delivery_status != 'delivered':
            raise ValueError("Delivery status must be 'delivered' to be fulfilled")

        delivery.delivery_status = 'fulfilled'
        self.set_availability(staff.user_id, True)
        db.session.commit()
        return delivery
    
    # Get available staff member
    def get_available_staff(self, theatre_id):
        staff = Staff.query.filter_by(theatre_id=theatre_id, is_available=True).all()
        if staff:
            staff = staff.order_by(Staff.last_updated.asc(), Staff.user_id.asc()).first()
        return staff
    
    # Assign available staff member
    def try_assign_staff(self, theatre_id, delivery):
        if not delivery:
            raise ValueError("Delivery not found")
        staff = self.get_available_staff(theatre_id=theatre_id)
        if not staff:
            return False
        delivery.staff_id = staff.user_id
        staff.is_available = self.set_availability(staff.user_id, False)
        db.session.commit()
        return True