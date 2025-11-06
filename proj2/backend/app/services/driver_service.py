from app.models import *
from app.app import db, get_app

config_name = 'development'
app = get_app(config_name)

with app.app_context():
    pass
