from models import *
from app import db, get_app

config_name = 'development'
app = get_app(config_name)

with app.app_context():
    pass

# Note: Try to implement Google Sign-Up with Flask
# Snack-Movie Linking   
