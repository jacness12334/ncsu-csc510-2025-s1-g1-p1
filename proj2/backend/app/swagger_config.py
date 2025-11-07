swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Movie Munchers API",
        "description": "API documentation for the Movie Munchers application.",
        "contact": {
            "responsibleOrganization": "NCSU",
            "responsibleDeveloper": "Your Team",
            "url": "http://www.example.com",
        },
        "version": "1.0.0"
    },
    "schemes": [
        "http",
        "https"
    ],
    # --- GLOBAL DEFINITIONS FOR REFERENCES ---
    "definitions": {
        'UserRegistration': {
            'type': 'object',
            'required': ['name', 'email', 'phone', 'birthday', 'password'],
            'properties': {
                'name': {'type': 'string', 'description': 'The full name of the user.'},
                'email': {'type': 'string', 'description': 'The unique email address.'},
                'phone': {'type': 'string', 'description': "The user's phone number."},
                'birthday': {'type': 'string', 'format': 'date', 'description': "The user's date of birth (YYYY-MM-DD)."},
                'password': {'type': 'string', 'description': "The user's password."},
                'role': {'type': 'string', 'description': "The user's role (Optional)."}
            }
        },
        'UserLogin': {
            'type': 'object',
            'required': ['email', 'password'],
            'properties': {
                'email': {'type': 'string', 'description': "The user's email address."},
                'password': {'type': 'string', 'description': "The user's password."},
            }
        },
        'UserUpdate': {
            'type': 'object',
            'required': ['name', 'email', 'phone', 'birthday'],
            'properties': {
                'name': {'type': 'string', 'description': 'The updated full name of the user.'},
                'email': {'type': 'string', 'description': 'The updated email address.'},
                'phone': {'type': 'string', 'description': 'The updated phone number.'},
                'birthday': {'type': 'string', 'format': 'date', 'description': 'The updated date of birth (YYYY-MM-DD).'},
            }
        },
        'PasswordChange': {
            'type': 'object',
            'required': ['current_password', 'new_password'],
            'properties': {
                'current_password': {'type': 'string', 'description': 'The current password for verification.'},
                'new_password': {'type': 'string', 'description': 'The new password.'},
            }
        },
        'UserResponse': {
            'type': 'object',
            'properties': {
                'message': {'type': 'string', 'description': 'A success message.'},
                'user_id': {'type': 'integer'},
                'name': {'type': 'string'},
                'email': {'type': 'string'},
                'role': {'type': 'string'},
            }
        },
        'UserProfile': {
            'type': 'object',
            'properties': {
                'user_id': {'type': 'integer'},
                'name': {'type': 'string'},
                'email': {'type': 'string'},
                'phone': {'type': 'string'},
                'birthday': {'type': 'string', 'format': 'date'},
                'role': {'type': 'string'},
            }
        },
        'SupplierDetails': {
            'type': 'object',
            'properties': {
                'user_id': {'type': 'integer', 'description': 'The User ID associated with the supplier.'},
                'company_name': {'type': 'string', 'description': 'The official name of the supplier company.'},
                'company_address': {'type': 'string', 'description': 'The physical address of the company.'},
                'contact_phone': {'type': 'string', 'description': 'The main contact phone number.'},
                'is_open': {'type': 'boolean', 'description': 'Current availability status (True if open for business).'}
            }
        },
        'SupplierEdit': {
            'type': 'object',
            'required': ['user_id', 'company_name', 'company_address', 'contact_phone', 'is_open'],
            'properties': {
                'user_id': {'type': 'integer', 'description': 'The ID of the supplier user (must be sent in the request body).'},
                'company_name': {'type': 'string'},
                'company_address': {'type': 'string'},
                'contact_phone': {'type': 'string'},
                'is_open': {'type': 'boolean'}
            }
        },
        'SupplierStatusUpdate': {
            'type': 'object',
            'required': ['user_id', 'is_open'],
            'properties': {
                'user_id': {'type': 'integer', 'description': 'The ID of the supplier user (must be sent in the request body).'},
                'is_open': {'type': 'boolean', 'description': 'The new availability status (True or False).'}
            }
        },
        'Product': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer', 'description': 'The unique ID of the product.'},
                'supplier_id': {'type': 'integer', 'description': 'The ID of the supplying user.'},
                'name': {'type': 'string', 'description': 'Name of the product.'},
                'unit_price': {'type': 'number', 'format': 'float', 'description': 'Price per unit.'},
                'inventory_quantity': {'type': 'integer', 'description': 'Stock quantity.'},
                'size': {'type': 'string', 'description': 'Product size (e.g., Small, 12oz).'},
                'keywords': {'type': 'string', 'description': 'Comma-separated keywords for search.'},
                'category': {'type': 'string', 'description': 'Product category (e.g., Snack, Drink).'},
                'discount': {'type': 'number', 'format': 'float', 'description': 'Discount percentage (0.0 to 1.0).'},
                'is_available': {'type': 'boolean', 'description': 'Availability status.'}
            }
        },
        'ProductCreateEdit': {
            'type': 'object',
            'required': ['user_id', 'name', 'unit_price', 'inventory_quantity', 'size', 'keywords', 'category', 'discount', 'is_available'],
            'properties': {
                'user_id': {'type': 'integer', 'description': 'The ID of the supplier user (must be sent in the request body).'},
                'name': {'type': 'string'},
                'unit_price': {'type': 'number', 'format': 'float'},
                'inventory_quantity': {'type': 'integer'},
                'size': {'type': 'string'},
                'keywords': {'type': 'string'},
                'category': {'type': 'string'},
                'discount': {'type': 'number', 'format': 'float'},
                'is_available': {'type': 'boolean'}
            }
        },
        'StaffRegistration': {
            'type': 'object',
            'required': ['name', 'email', 'phone', 'birthday', 'password', 'theatre_id', 'role'],
            'properties': {
                'user_id': {'type': 'integer', 'description': 'The staff manager/admin ID for authorization (must be in body).'},
                'name': {'type': 'string'},
                'email': {'type': 'string'},
                'phone': {'type': 'string'},
                'birthday': {'type': 'string', 'format': 'date'},
                'password': {'type': 'string'},
                'theatre_id': {'type': 'integer', 'description': 'The ID of the theatre the staff member works at.'},
                'role': {'type': 'string', 'description': 'The role of the staff member (e.g., attendant, manager).'}
            }
        },
        'StaffAvailabilityUpdate': {
            'type': 'object',
            'required': ['user_id', 'is_available'],
            'properties': {
                'user_id': {'type': 'integer', 'description': 'The staff member ID (must be in body).'},
                'is_available': {'type': 'boolean', 'description': 'The new availability status (True/False).'}
            }
        },
        'TheatreDetails': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'name': {'type': 'string'},
                'address': {'type': 'string'},
                'phone': {'type': 'string'},
                'is_open': {'type': 'boolean'}
            }
        },
        'TheatreStatusUpdate': {
            'type': 'object',
            'required': ['user_id', 'theatre_id', 'is_open'],
            'properties': {
                'user_id': {'type': 'integer', 'description': 'The staff member ID for authorization.'},
                'theatre_id': {'type': 'integer', 'description': 'The ID of the theatre to update.'},
                'is_open': {'type': 'boolean', 'description': 'The new status of the theatre.'}
            }
        },
        'MovieCreateEdit': {
            'type': 'object',
            'required': ['title', 'genre', 'length_mins', 'release_year', 'keywords', 'rating'],
            'properties': {
                'user_id': {'type': 'integer', 'description': 'The staff member ID for authorization (must be in body).'},
                'title': {'type': 'string'},
                'genre': {'type': 'string'},
                'length_mins': {'type': 'integer'},
                'release_year': {'type': 'integer'},
                'keywords': {'type': 'string'},
                'rating': {'type': 'string'}
            }
        },
        'ShowingCreateEdit': {
            'type': 'object',
            'required': ['movie_id', 'auditorium_id', 'start_time'],
            'properties': {
                'user_id': {'type': 'integer', 'description': 'The staff member ID for authorization (must be in body).'},
                'movie_id': {'type': 'integer'},
                'auditorium_id': {'type': 'integer'},
                'start_time': {'type': 'string', 'format': 'date-time', 'description': 'Start time in ISO format (e.g., 2025-01-01T19:00:00Z).'}
            }
        },
        'StaffMemberDetails': {
            'type': 'object',
            'properties': {
                'user_id': {'type': 'integer'},
                'theatre_id': {'type': 'integer'},
                'role': {'type': 'string'},
                'is_available': {'type': 'boolean'}
            }
        },
        'DeliveryDetails': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'customer_showing_id': {'type': 'integer'},
                'payment_method_id': {'type': 'integer'},
                'driver_id': {'type': 'integer', 'description': 'ID of the assigned delivery driver.'},
                'staff_id': {'type': 'integer', 'description': 'ID of the staff member managing the delivery.'},
                'total_price': {'type': 'number', 'format': 'float'},
                'payment_status': {'type': 'string'},
                'delivery_status': {'type': 'string'}
            }
        },
        # --- ADD THESE TO THE 'definitions' BLOCK IN swagger_config.py ---

        'DriverRegistration': {
            'type': 'object',
            'required': ['name', 'email', 'phone', 'birthday', 'password', 'license_plate', 'vehicle_type', 'vehicle_color', 'duty_status'],
            'properties': {
                'name': {'type': 'string'},
                'email': {'type': 'string'},
                'phone': {'type': 'string'},
                'birthday': {'type': 'string', 'format': 'date'},
                'password': {'type': 'string'},
                'license_plate': {'type': 'string'},
                'vehicle_type': {'type': 'string'},
                'vehicle_color': {'type': 'string'},
                'duty_status': {'type': 'string', 'description': 'The driver\'s current work status (e.g., "on_duty", "off_duty").'},
                'rating': {'type': 'number', 'format': 'float', 'description': 'Initial rating (Optional, often 0.0 or 5.0).'},
                'total_deliveries': {'type': 'integer', 'description': 'Initial delivery count (Optional, usually 0).'}
            }
        },
        'DriverProfile': {
            'type': 'object',
            'properties': {
                'user_id': {'type': 'integer'},
                'name': {'type': 'string'},
                'email': {'type': 'string'},
                'phone': {'type': 'string'},
                'license_plate': {'type': 'string'},
                'vehicle_type': {'type': 'string'},
                'vehicle_color': {'type': 'string'},
                'duty_status': {'type': 'string'},
                'rating': {'type': 'number', 'format': 'float'},
                'total_deliveries': {'type': 'integer'}
            }
        },
        'DriverUpdate': {
            'type': 'object',
            'required': ['license_plate', 'vehicle_type', 'vehicle_color'],
            'properties': {
                'license_plate': {'type': 'string'},
                'vehicle_type': {'type': 'string'},
                'vehicle_color': {'type': 'string'}
            }
        },
        'DriverStatusUpdate': {
            'type': 'object',
            'required': ['new_status'],
            'properties': {
                'new_status': {'type': 'string', 'description': 'The new duty status (e.g., "on_duty", "delivering", "off_duty").'}
            }
        },
        'DeliveryRate': {
            'type': 'object',
            'required': ['rating'],
            'properties': {
                'rating': {'type': 'number', 'format': 'float', 'description': 'The rating given to the driver (e.g., 1.0 to 5.0).'}
            }
        },
        'DeliveryHistoryItem': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'driver_id': {'type': 'integer'},
                'customer_showing_id': {'type': 'integer'},
                'payment_method_id': {'type': 'integer'},
                'staff_id': {'type': 'integer'},
                'payment_status': {'type': 'string'},
                'total_price': {'type': 'number', 'format': 'float'},
                'delivery_time': {'type': 'string', 'format': 'date-time'},
                'delivery_status': {'type': 'string'}
            }
        },
        'CustomerRegistration': {
            'type': 'object',
            'required': ['name', 'email', 'phone', 'birthday', 'password'],
            'properties': {
                'name': {'type': 'string'},
                'email': {'type': 'string'},
                'phone': {'type': 'string'},
                'birthday': {'type': 'string', 'format': 'date'},
                'password': {'type': 'string'},
                'role': {'type': 'string', 'description': 'Defaults to "customer". (Optional)'},
                'default_theatre_id': {'type': 'integer', 'description': 'The customer\'s preferred theatre ID. (Optional)'}
            }
        },
        'CustomerProfile': {
            'type': 'object',
            'properties': {
                'user_id': {'type': 'integer'},
                'default_theatre_id': {'type': 'integer', 'nullable': True}
            }
        },
        'TheatreUpdate': {
            'type': 'object',
            'required': ['theatre_id'],
            'properties': {
                'theatre_id': {'type': 'integer', 'description': 'The new default theatre ID.'}
            }
        },
        'PaymentMethodCreate': {
            'type': 'object',
            'required': ['card_number', 'expiration_month', 'expiration_year', 'billing_address'],
            'properties': {
                'card_number': {'type': 'string'},
                'expiration_month': {'type': 'integer'},
                'expiration_year': {'type': 'integer'},
                'billing_address': {'type': 'string'},
                'balance': {'type': 'number', 'format': 'float', 'description': 'Initial balance (default 0.00). (Optional)'},
                'is_default': {'type': 'boolean', 'description': 'Set as default payment method. (Optional)'}
            }
        },
        'PaymentMethodDetails': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'card_number': {'type': 'string'},
                'expiration_month': {'type': 'integer'},
                'expiration_year': {'type': 'integer'},
                'billing_address': {'type': 'string'},
                'balance': {'type': 'number', 'format': 'float'},
                'is_default': {'type': 'boolean'}
            }
        },
        'FundAddition': {
            'type': 'object',
            'required': ['amount'],
            'properties': {
                'amount': {'type': 'number', 'format': 'float', 'description': 'The amount of funds to add.'}
            }
        },
        'CartItemCreate': {
            'type': 'object',
            'required': ['product_id'],
            'properties': {
                'product_id': {'type': 'integer'},
                'quantity': {'type': 'integer', 'description': 'Defaults to 1. (Optional)'}
            }
        },
        'CartItemUpdate': {
            'type': 'object',
            'required': ['quantity'],
            'properties': {
                'quantity': {'type': 'integer', 'description': 'The new quantity for the cart item.'}
            }
        },
        'CartItemDetails': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'product_id': {'type': 'integer'},
                'quantity': {'type': 'integer'}
            }
        },
        'CustomerShowingCreate': {
            'type': 'object',
            'required': ['movie_showing_id', 'seat_id'],
            'properties': {
                'movie_showing_id': {'type': 'integer'},
                'seat_id': {'type': 'integer'}
            }
        },
        'DeliveryCreate': {
            'type': 'object',
            'required': ['customer_showing_id', 'payment_method_id'],
            'properties': {
                'customer_showing_id': {'type': 'integer', 'description': 'The ID of the booked showing.'},
                'payment_method_id': {'type': 'integer', 'description': 'The payment method ID to use for the order.'}
            }
        },
        'DeliveryRateCustomer': {
            'type': 'object',
            'required': ['rating'],
            'properties': {
                'rating': {'type': 'number', 'format': 'float', 'description': 'The rating given to the entire delivery (e.g., 1.0 to 5.0).'}
            }
        },
        'ProductMenu': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'supplier_id': {'type': 'integer'},
                'name': {'type': 'string'},
                'unit_price': {'type': 'number', 'format': 'float'},
                'inventory_quantity': {'type': 'integer'},
                'category': {'type': 'string'},
                'is_available': {'type': 'boolean'}
            }
        }
    }
}