import pytest
from app.services.staff_service import StaffService
from app.services.user_service import UserService
from app.models import *
from datetime import datetime

# Test class for staff_service.py
class TestStaffService:
    # Validate that an admin user is recognized as admin
    def test_validate_admin_success(self, app, sample_admin):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            admin = staff_service.validate_admin()
            assert admin is not None
            assert admin.user_id is not None
            assert admin.role == "admin"

    # Validate that a non-admin user triggers unauthorized error
    def test_validate_admin_unauthorized(self, app, sample_staff):
        with app.app_context():
            staff_service = StaffService(sample_staff)
            with pytest.raises(ValueError, match="Unauthorized User - Not an admin"):
                staff_service.validate_admin()

    # Validate that both admin and runner are recognized as staff
    def test_validate_staff_success(self, app, sample_admin, sample_staff):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            admin = staff_service.validate_staff()
            assert admin is not None
            assert admin.user_id is not None
            assert admin.role == "admin"

            staff_service = StaffService(sample_staff)
            runner = staff_service.validate_staff()
            assert runner is not None
            assert runner.user_id is not None
            assert runner.role == "runner"

    # Validate that a non-staff user triggers unauthorized error
    def test_validate_staff_unauthorized(self, app, sample_user):
        with app.app_context():
            staff_service = StaffService(sample_user)
            with pytest.raises(ValueError, match="Unauthorized User - Not a staff member"):
                staff_service.validate_staff()

    # Add a new staff member and verify role/ids
    def test_add_staff_success(self, app, sample_admin, sample_theatre):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            staff = staff_service.add_staff(
                name='Runner 2',
                email='runner_2@movie_munchers.com',
                phone='9000000003',
                birthday='2000-01-01',
                password='password',
                theatre_id=sample_theatre,
                role='runner'
            )
            assert staff is not None
            assert staff.user_id is not None
            assert staff.role == "runner"

    # Adding staff with an invalid role should raise
    def test_add_staff_invalid_role(self, app, sample_admin, sample_theatre):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            with pytest.raises(ValueError, match="Invalid role"):
                staff_service.add_staff(
                    name="X",
                    email="x@test.com",
                    phone="123",
                    birthday="2000-01-01",
                    password="pass",
                    theatre_id=sample_theatre,
                    role="invalid",
                )

    # Only admins can add staff; non-admin should raise
    def test_add_staff_unauthorized(self, app, sample_staff, sample_theatre):
        with app.app_context():
            staff_service = StaffService(sample_staff)
            with pytest.raises(ValueError):
                staff_service.add_staff(
                    name="Runner3",
                    email="runner3@movie_munchers.com",
                    phone="9000000004",
                    birthday="2000-01-01",
                    password="password",
                    theatre_id=sample_theatre,
                    role="runner",
                )

    # Remove an existing staff member and verify deletion
    def test_remove_staff_success(self, app, sample_admin, sample_staff):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            staff_service.remove_staff(sample_staff)
            assert Staff.query.filter_by(user_id=sample_staff).first() is None

    # Removing a non-existent staff member should raise
    def test_remove_staff_not_found(self, app, sample_admin):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            with pytest.raises(ValueError, match="not found"):
                staff_service.remove_staff(9999)

    # Only admins can remove staff; non-admin should raise
    def test_remove_staff_unauthorized(self, app, sample_staff):
        with app.app_context():
            staff_service = StaffService(sample_staff)
            with pytest.raises(ValueError):
                staff_service.remove_staff(sample_staff)

    # Get theatres should return a non-empty list
    def test_get_theatres_returns_list(self, app, sample_admin):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            theatres = staff_service.get_theatres()
            assert isinstance(theatres, list)
            assert len(theatres) > 0

    # Set theatre status and verify is_open flag
    def test_set_theatre_status_success(self, app, sample_admin, sample_theatre):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            theatre = staff_service.set_theatre_status(sample_theatre, False)
            assert theatre.is_open is False

    # Setting theatre status for a missing theatre should raise
    def test_set_theatre_status_not_found(self, app, sample_admin):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            with pytest.raises(ValueError, match="not found"):
                staff_service.set_theatre_status(9999, True)

    # Only admins can set theatre status; non-admin should raise
    def test_set_theatre_status_unauthorized(self, app, sample_staff, sample_theatre):
        with app.app_context():
            staff_service = StaffService(sample_staff)
            with pytest.raises(ValueError):
                staff_service.set_theatre_status(sample_theatre, False)

    # Add a movie and verify title
    def test_add_movie_success(self, app, sample_admin):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            movie = staff_service.add_movie("M2", "Drama", 120, 2024, "love", 4)
            assert movie.title == "M2"

    # Only admins can add movies; non-admin should raise
    def test_add_movie_unauthorized(self, app, sample_staff):
        with app.app_context():
            staff_service = StaffService(sample_staff)
            with pytest.raises(ValueError):
                staff_service.add_movie("M3", "Sci-Fi", 100, 2023, "space", 5)

    # Edit a movie and verify the updated title
    def test_edit_movie_success(self, app, sample_admin, sample_movie):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            movie = staff_service.edit_movie(sample_movie, "Edited", "Thriller", 100, 2024, "thrill", 5)
            assert movie.title == "Edited"

    # Editing a missing movie should raise
    def test_edit_movie_not_found(self, app, sample_admin):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            with pytest.raises(ValueError, match="not found"):
                staff_service.edit_movie(9999, "X", "Y", 10, 2020, "none", 2)

    # Remove a movie and ensure it no longer exists
    def test_remove_movie_success(self, app, sample_admin, sample_movie):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            staff_service.remove_movie(sample_movie)
            assert Movies.query.filter_by(id=sample_movie).first() is None

    # Removing a missing movie should raise
    def test_remove_movie_not_found(self, app, sample_admin):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            with pytest.raises(ValueError):
                staff_service.remove_movie(9999)

    # Add a showing with valid movie, auditorium, and datetime
    def test_add_showing_success(self, app, sample_admin, sample_movie, sample_auditorium):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            showing = staff_service.add_showing(sample_movie, sample_auditorium, datetime(2025, 1, 1, 9, 0, 0))
            assert showing.movie_id == sample_movie

    # Adding a showing with an invalid movie id should raise
    def test_add_showing_invalid_movie(self, app, sample_admin, sample_auditorium):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            with pytest.raises(ValueError):
                staff_service.add_showing(9999, sample_auditorium, datetime(2025, 1, 1, 8, 0, 0))

    # Adding a showing with an invalid auditorium id should raise
    def test_add_showing_invalid_auditorium(self, app, sample_admin, sample_movie):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            with pytest.raises(ValueError):
                staff_service.add_showing(sample_movie, 9999, datetime(2025, 1, 1, 8, 0, 0))

    # Adding a showing with a non-datetime start_time should raise
    def test_add_showing_invalid_start_time(self, app, sample_admin, sample_movie, sample_auditorium):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            with pytest.raises(ValueError):
                staff_service.add_showing(sample_movie, sample_auditorium, "today")

    # Edit an existing showing and verify fields updated
    def test_edit_showing_success(self, app, sample_admin, sample_showing, sample_movie, sample_auditorium):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            showing = staff_service.edit_showing(sample_showing, sample_movie, sample_auditorium, datetime(2025, 1, 1, 9, 0, 0))
            assert showing.id == sample_showing
            assert MovieShowings.query.filter_by(id=sample_showing).first().start_time == datetime(2025, 1, 1, 9, 0, 0)

    # Editing a showing with an invalid movie id should raise
    def test_edit_showing_invalid_movie(self, app, sample_admin, sample_showing, sample_auditorium):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            with pytest.raises(ValueError):
                staff_service.edit_showing(sample_showing, 9999, sample_auditorium, datetime(2025, 1, 1, 9, 0, 0))

    # Editing a showing with an invalid auditorium id should raise
    def test_edit_showing_invalid_auditorium(self, app, sample_admin, sample_showing, sample_movie):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            with pytest.raises(ValueError):
                staff_service.edit_showing(sample_showing, sample_movie, 9999, datetime(2025, 1, 1, 9, 0, 0))

    # Editing a missing showing id should raise
    def test_edit_showing_invalid_showing(self, app, sample_admin, sample_movie, sample_auditorium):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            with pytest.raises(ValueError):
                staff_service.edit_showing(9999, sample_movie, sample_auditorium, datetime(2025, 1, 1, 9, 0, 0))

    # Editing a showing with a non-datetime start_time should raise
    def test_edit_showing_invalid_start_time(self, app, sample_admin, sample_showing, sample_movie, sample_auditorium):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            with pytest.raises(ValueError):
                staff_service.edit_showing(sample_showing, sample_movie, sample_auditorium, "today")

    # Remove a showing and ensure it no longer exists
    def test_remove_showing_success(self, app, sample_admin, sample_showing):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            staff_service.remove_showing(sample_showing)
            assert MovieShowings.query.filter_by(id=sample_showing).first() is None

    # Removing a missing showing should raise
    def test_remove_showing_success(self, app, sample_admin):
        with app.app_context():
            staff_service = StaffService(sample_admin)
            with pytest.raises(ValueError):
                staff_service.remove_showing(9999)

    # Set staff availability and verify persisted value
    def test_set_availability_success(self, app, sample_staff):
        with app.app_context():
            staff_service = StaffService(sample_staff)
            staff = staff_service.set_availability(False)
            assert staff.is_available is False
            assert Staff.query.filter_by(user_id=sample_staff).first().is_available is False

    # Accept a pending delivery and verify staff status and delivery update
    def test_accept_delivery_success(self, app, sample_staff, sample_delivery):
        with app.app_context():
            staff_service = StaffService(sample_staff)
            staff = Staff.query.filter_by(user_id=sample_staff).first()
            assert staff.is_available is True
            delivery = staff_service.accept_delivery(sample_delivery)
            assert delivery.staff_id is not None
            assert delivery.delivery_status == "accepted"
            assert staff.is_available is False

    # Accepting a missing delivery should raise
    def test_accept_delivery_not_found(self, app, sample_staff):
        with app.app_context():
            staff_service = StaffService(sample_staff)
            with pytest.raises(ValueError, match="Delivery not found"):
                staff_service.accept_delivery(9999)

    # Accepting an already accepted delivery should raise
    def test_accept_delivery_already_taken(self, app, sample_staff, sample_delivery):
        with app.app_context():
            staff_service = StaffService(sample_staff)
            delivery = Deliveries.query.filter_by(id=sample_delivery).first()
            delivery.delivery_status = "accepted"
            with pytest.raises(ValueError, match="Delivery not available to accept"):
                staff_service.accept_delivery(sample_delivery)

    # Accepting a delivery while staff is unavailable should raise
    def test_accept_delivery_not_available(self, app, sample_staff, sample_delivery):
        with app.app_context():
            staff_service = StaffService(sample_staff)
            staff = Staff.query.filter_by(user_id=sample_staff).first()
            staff.is_available = False
            db.session.commit()
            with pytest.raises(ValueError, match="Staff not available"):
                staff_service.accept_delivery(sample_delivery)

    # Fulfill a delivered delivery and free up the staff
    def test_fulfill_delivery_success(self, app, sample_staff, sample_delivery):
        with app.app_context():
            staff_service = StaffService(sample_staff)
            staff = Staff.query.filter_by(user_id=sample_staff).first()
            staff_service.accept_delivery(sample_delivery)
            delivery = Deliveries.query.filter_by(id=sample_delivery).first()
            delivery.delivery_status = "delivered"
            db.session.commit()
            assert staff.is_available is False
            delivery = staff_service.fulfill_delivery(delivery.id)
            assert delivery.delivery_status == "fulfilled"
            assert staff.is_available is True

    # Fulfilling a missing delivery should raise
    def test_fulfill_delivery_not_found(self, app, sample_staff):
        with app.app_context():
            staff_service = StaffService(sample_staff)
            with pytest.raises(ValueError, match="not found"):
                staff_service.fulfill_delivery(9999)

    # Fulfilling a non-delivered delivery should raise
    def test_fulfill_delivery_not_delivered(self, app, sample_staff, sample_delivery):
        with app.app_context():
            staff_service = StaffService(sample_staff)
            with pytest.raises(ValueError, match="Delivery status must be 'delivered' to be fulfilled"):
                staff_service.fulfill_delivery(sample_delivery)

    # List staff for a theatre and verify items belong to that theatre
    def test_show_all_staff_success(self, app, sample_admin, sample_theatre):
        with app.app_context():
            u = UserService().create_user(
                name='Runner One',
                email='runner1@example.com',
                phone='5551237001',
                birthday='1995-01-01',
                password='password123',
                role='staff'
            )
            s = Staff(user_id=u.id, theatre_id=sample_theatre, role='runner', is_available=True)
            db.session.add(s)
            db.session.commit()
            svc = StaffService(user_id=sample_admin)
            staff_list = svc.show_all_staff(theatre_id=sample_theatre)
            assert len(staff_list) >= 1
            assert all(st.theatre_id == sample_theatre for st in staff_list)
            assert any(st.user_id == u.id for st in staff_list)

    # Verify filtering excludes staff from other theatres
    def test_show_all_staff_filters_other_theatre(self, app, sample_admin, sample_theatre):
        with app.app_context():
            other = Theatres(name='Other', address='999 Elsewhere', phone='5550000000', is_open=True)
            db.session.add(other)
            db.session.commit()
            u2 = UserService().create_user(
                name='Runner Two',
                email='runner2@example.com',
                phone='5551237002',
                birthday='1996-02-02',
                password='password123',
                role='staff'
            )
            s2 = Staff(user_id=u2.id, theatre_id=other.id, role='runner', is_available=True)
            db.session.add(s2)
            db.session.commit()
            svc = StaffService(user_id=sample_admin)
            staff_list = svc.show_all_staff(theatre_id=sample_theatre)
            assert all(st.theatre_id == sample_theatre for st in staff_list)
            assert all(st.user_id != u2.id for st in staff_list)

    # Only admins can list staff by theatre; non-admin should raise
    def test_show_all_staff_unauthorized(self, app, sample_staff, sample_theatre):
        with app.app_context():
            svc = StaffService(user_id=sample_staff)
            with pytest.raises(ValueError):
                svc.show_all_staff(theatre_id=sample_theatre)

    # Show all deliveries for a theatre returns a list with basic fields
    def test_show_all_deliveries_success_returns_list(self, app, sample_admin, sample_theatre):
        with app.app_context():
            svc = StaffService(sample_admin)
            deliveries = svc.show_all_deliveries(theatre_id=sample_theatre)
            assert isinstance(deliveries, list)
            for d in deliveries:
                assert hasattr(d, "id")
                assert hasattr(d, "delivery_status")

    # Show all deliveries should be empty for a theatre with no data
    def test_show_all_deliveries_empty_for_unused_theatre(self, app, sample_admin):
        with app.app_context():
            empty = Theatres(name='Empty Theatre', address='123 Nowhere', phone='5550009999', is_open=True)
            db.session.add(empty)
            db.session.commit()
            svc = StaffService(sample_admin)
            deliveries = svc.show_all_deliveries(theatre_id=empty.id)
            assert isinstance(deliveries, list)
            assert deliveries == []

    # Get a staff record by id and verify user_id
    def test_get_staff_success(self, app, sample_admin, sample_staff):
        with app.app_context():
            svc = StaffService(sample_admin)
            staff = svc.get_staff(sample_staff)
            assert staff.user_id == sample_staff

    # Non-staff trying to access get_staff should raise
    def test_get_staff_unauthorized(self, app, sample_customer):
        with app.app_context():
            svc = StaffService(sample_customer)
            with pytest.raises(ValueError, match="Unauthorized User - Not a staff member"):
                staff = svc.get_staff(sample_customer)
                assert staff is None
