from app.models import *
from app.app import db
from app.services.user_service import UserService
from datetime import datetime

class StaffService:
    
    """Service layer for staff profiles, authorization checks, theatre/movie management,
    and delivery maintenance operations.
    """

    def __init__(self, user_id):
        """Initialize the staff service with the acting user context.

        Args:
            user_id: The id of the user performing actions (authorization context).
        """
        self.user_id = user_id
        self.user_service = UserService()

    def validate_admin(self):
        """Ensure the current user is a staff admin.

        Returns:
            Staff: The admin staff record.

        Raises:
            ValueError: If the user is not a staff admin.
        """
        admin = Staff.query.filter_by(user_id=self.user_id).first()
        if not admin or admin.role != 'admin':
            raise ValueError("Unauthorized User - Not an admin")
        return admin

    def validate_staff(self):
        """Ensure the current user is a staff member (any role).

        Returns:
            Staff: The staff record.

        Raises:
            ValueError: If the user is not a staff member.
        """
        staff = Staff.query.filter_by(user_id=self.user_id).first()
        if not staff:
            raise ValueError("Unauthorized User - Not a staff member")
        return staff

    def add_staff(self, name, email, phone, birthday, password, theatre_id, role):
        """Create a new staff user and staff record (admin only).

        Args:
            name: Staff member name.
            email: Unique email for the new staff user.
            phone: Unique phone for the new staff user.
            birthday: Date of birth (YYYY-MM-DD or date).
            password: Plaintext password to hash.
            theatre_id: Theatre id for the staff assignment.
            role: 'admin' or 'runner'.

        Returns:
            Staff: The created staff record.

        Raises:
            ValueError: If the acting user is not admin or role is invalid.
        """
        admin = self.validate_admin()
        
        if role not in ['admin', 'runner']:
            raise ValueError("Invalid role. Must be 'admin' or 'runner'.")
        
        user = self.user_service.create_user(name, email, phone, birthday, password, 'staff')
        db.session.flush()

        staff = Staff(user_id=user.id, theatre_id=theatre_id, role=role, is_available=True)
        db.session.add(staff)
        db.session.commit()
        return staff

    def remove_staff(self, staff_user_id):
        """Remove a staff user and associated staff record (admin only).

        Args:
            staff_user_id: The user id of the staff member to remove.

        Returns:
            None

        Raises:
            ValueError: If the acting user is not admin or the staff user is not found.
        """
        admin = self.validate_admin()

        staff = Staff.query.filter_by(user_id=staff_user_id).first()
        if not staff:
            raise ValueError(f"User {staff_user_id} not found")
        
        self.user_service.delete_user(staff.user_id)

    def get_theatres(self):
        """Return all theatres.

        Returns:
            list[Theatres]: All theatres in the system.
        """
        theatres = Theatres.query.all()
        return theatres

    def set_theatre_status(self, theatre_id, is_open):
        """Set open/closed status for a theatre (admin only).

        Args:
            theatre_id: Target theatre id.
            is_open: Boolean open flag to set.

        Returns:
            Theatres: The updated theatre.

        Raises:
            ValueError: If acting user is not admin or the theatre id is invalid.
        """
        admin = self.validate_admin()
        
        theatre = Theatres.query.filter_by(id=theatre_id).first()
        if not theatre:
            raise ValueError(f"Theatre {theatre_id} not found")
        
        theatre.is_open = is_open
        db.session.commit()
        return theatre

    def add_movie(self, title, genre, length_mins, release_year, keywords, rating):
        """Create a movie (admin only).

        Args:
            title: Movie title.
            genre: Movie genre.
            length_mins: Duration in minutes.
            release_year: Year of release.
            keywords: Search keywords.
            rating: Decimal or float rating in model-defined bounds.

        Returns:
            Movies: The created movie.

        Raises:
            ValueError: If acting user is not admin.
        """
        admin = self.validate_admin()
        
        movie = Movies(title=title, genre=genre, length_mins=length_mins, release_year=release_year, keywords=keywords, rating=rating)
        db.session.add(movie)
        db.session.commit()
        return movie

    def edit_movie(self, movie_id, title, genre, length_mins, release_year, keywords, rating):
        """Edit a movie by id (admin only).

        Args:
            movie_id: Movie primary key.
            title: New title.
            genre: New genre.
            length_mins: New duration in minutes.
            release_year: New release year.
            keywords: New keywords.
            rating: New rating.

        Returns:
            Movies: The updated movie.

        Raises:
            ValueError: If acting user is not admin or movie not found.
        """
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

    def remove_movie(self, movie_id):
        """Delete a movie by id (admin only).

        Args:
            movie_id: Movie primary key.

        Returns:
            None

        Raises:
            ValueError: If acting user is not admin or movie not found.
        """
        admin = self.validate_admin()
        
        movie = Movies.query.filter_by(id=movie_id).first()
        if not movie:
            raise ValueError(f"Movie {movie_id} not found")
        
        db.session.delete(movie)
        db.session.commit()

    def add_showing(self, movie_id, auditorium_id, start_time):
        """Create a movie showing (admin only).

        Args:
            movie_id: Movie id to show.
            auditorium_id: Auditorium id where it screens.
            start_time: datetime start time.

        Returns:
            MovieShowings: The created showing.

        Raises:
            ValueError: If acting user is not admin, movie/auditorium missing,
                or start_time is not a datetime.
        """
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

    def edit_showing(self, showing_id, movie_id, auditorium_id, start_time):
        """Edit a movie showing (admin only).

        Args:
            showing_id: Showing primary key.
            movie_id: New movie id.
            auditorium_id: New auditorium id.
            start_time: New datetime start time.

        Returns:
            MovieShowings: The updated showing.

        Raises:
            ValueError: If acting user is not admin, any id not found,
                or start_time is not a datetime.
        """
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

    def remove_showing(self, showing_id):
        """Delete a movie showing by id (admin only).

        Args:
            showing_id: Showing primary key.

        Returns:
            None

        Raises:
            ValueError: If acting user is not admin or showing not found.
        """
        admin = self.validate_admin()
        
        showing = MovieShowings.query.filter_by(id=showing_id).first()
        if not showing:
            raise ValueError(f"Movie Showing {showing_id} not found")
        
        db.session.delete(showing)
        db.session.commit()

    def set_availability(self, is_available):
        """Set the current staff member's availability.

        Args:
            is_available: Boolean availability flag.

        Returns:
            Staff: The updated staff record.

        Raises:
            ValueError: If the user is not a staff member.
        """
        staff = self.validate_staff()
        
        staff.is_available = is_available
        db.session.commit()
        return staff

    def accept_delivery(self, delivery_id):
        """Accept a pending delivery for the current staff member.

        Sets the delivery staff_id, moves status to 'accepted', and marks
        the staff member unavailable.

        Args:
            delivery_id: Delivery primary key.

        Returns:
            Deliveries: The updated delivery.

        Raises:
            ValueError: If staff not available, delivery missing, or not pending.
        """
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

    def fulfill_delivery(self, delivery_id):
        """Mark a delivered order as fulfilled and free up the staff member.

        Args:
            delivery_id: Delivery primary key.

        Returns:
            Deliveries: The updated delivery.

        Raises:
            ValueError: If delivery missing or status is not 'delivered'.
        """
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
    
    def get_available_staff(self, theatre_id):
        """Return the next available staff member at a theatre (oldest update first).

        Args:
            theatre_id: Theatre identifier.

        Returns:
            Staff | None: The selected staff member or None if none available.
        """
        staff = Staff.query.filter_by(theatre_id=theatre_id, is_available=True).order_by(Staff.last_updated.asc(), Staff.user_id.asc()).all()
        if staff:
            staff = staff[0]
        return staff
    
    def try_assign_staff(self, theatre_id, delivery):
        """Assign an available staff member to a delivery if possible.

        Args:
            theatre_id: Theatre to search at.
            delivery: Delivery instance to assign.

        Returns:
            bool: True if an assignment occurred, else False.

        Raises:
            ValueError: If the delivery reference is missing.
        """
        if not delivery:
            raise ValueError("Delivery not found")
        staff = self.get_available_staff(theatre_id=theatre_id)
        print(staff)
        if not staff:
            return False
        delivery.staff_id = staff.user_id
        ss = StaffService(staff.user_id)
        ss.set_availability(False)
        db.session.commit()
        return True
    
    def show_all_staff(self, theatre_id):
        """List all staff at a theatre (admin only).

        Args:
            theatre_id: Theatre identifier.

        Returns:
            list[Staff]: Staff ordered by user id.

        Raises:
            ValueError: If the acting user is not admin.
        """
        self.validate_admin()
        return Staff.query.filter(Staff.theatre_id == theatre_id).order_by(Staff.user_id.asc()).all()
    
    def show_all_deliveries(self, theatre_id):
        """List all deliveries related to a theatre (staff only).

        Orders by delivery status then id descending.

        Args:
            theatre_id: Theatre identifier.

        Returns:
            list[Deliveries]: Matching deliveries.

        Raises:
            ValueError: If the acting user is not staff.
        """
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

    def get_staff(self, staff_id):
        """Return a staff record by user id (staff only).

        Args:
            staff_id: Staff user id to fetch.

        Returns:
            Staff | None: The staff record or None if not found.

        Raises:
            ValueError: If the acting user is not staff.
        """
        self.validate_staff()
        staff = Staff.query.filter_by(user_id=staff_id).first()
        return staff
