from app.models import *
from app.app import db
from app.services.user_service import UserService
from datetime import datetime

class StaffService:

    # Initialize services
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_service = UserService()
    

    # Check that user is admin
    def validate_admin(self):
        admin = Staff.query.filter_by(user_id=self.user_id).first()
        if not admin or admin.role != 'admin':
            raise ValueError("Unauthorized User - Not an admin")
        return admin


    # Retrieve the given staff user
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

                
        staff = Staff.query.filter_by(user_id=staff_user_id).first()
        if not staff:
            raise ValueError(f"User {staff_user_id} not found")
        
        self.user_service.delete_user(staff.user_id)
    

    # Returns a list of all theatres
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
        if not isinstance(start_time, datetime):
            raise ValueError(f"Movie start time must be in DateTime format")
        
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
        
        if not isinstance(start_time, datetime):
            raise ValueError(f"Movie start time must be in DateTime format")
        
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
    

    # Staff functionality - accept delivery
    def accept_delivery(self, delivery_id):
        staff = self.validate_staff()

        delivery = Deliveries.query.filter_by(id=delivery_id).first()

        if not staff.is_available:
            raise ValueError("Staff not available")
        if not delivery:
            raise ValueError("Delivery not found")
        if delivery.delivery_status != 'pending':
            raise ValueError("Delivery not available to accept")

        self.set_availability(False)
        delivery.staff_id = staff.user_id
        delivery.delivery_status = 'accepted'
        db.session.commit()
        return delivery
    

    # Fulfill delivery
    def fulfill_delivery(self, delivery_id):
        staff = self.validate_staff()
        delivery = Deliveries.query.filter_by(id=delivery_id).first()

        if not delivery:
            raise ValueError(f"Delivery {delivery_id} not found")
        if delivery.delivery_status != 'delivered':
            raise ValueError("Delivery status must be 'delivered' to be fulfilled")

        delivery.delivery_status = 'fulfilled'
        self.set_availability(True)
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
        staff.is_available = self.set_availability(False)
        db.session.commit()
        return True
    
    # Show all staff members 
    def show_all_staff(self, theatre_id):
        self.validate_admin()
        return Staff.query.filter(Staff.theatre_id == theatre_id).order_by(Staff.user_id.asc()).all()
    
    # Show all deliveries for the given theatre
    def show_all_deliveries(self, theatre_id):
        self.validate_staff()
        deliveries = (
            Deliveries.query
            .join(CustomerShowings, Deliveries.customer_showing_id == CustomerShowings.id)
            .join(Seats, CustomerShowings.seat_id == Seats.id)
            .join(Auditoriums, Seats.auditorium_id == Auditoriums.id)
            .filter(Auditoriums.theatre_id == theatre_id)
            .order_by(Deliveries.delivery_status.asc(), Deliveries.id.desc())
            .all()
        )
        return deliveries

    # # Show all showings
    # def show_all_showings(self, theatre_id):
    #     self.validate_admin()
    #     MovieShowings.query.join(Auditoriums, MovieShowings.auditorium_id == Auditoriums.id).filter(Auditoriums.theatre_id == theatre_id).all()

    # # Show all movies
    # def show_all_movies(self):
    #     return Movies.query.order_by(Movies.title.asc()).all()

    # Get staff member
    def get_staff(self, staff_id):
        self.validate_admin()
        staff = Staff.query.filter_by(user_id=staff_id).first()
        return {
            "user_id": staff.user_id,
            "theatre_id": staff.theatre_id,
            "role": staff.role,
            "is_available": staff.is_available,
        }

