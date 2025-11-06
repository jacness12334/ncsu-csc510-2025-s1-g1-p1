from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routes.staff_routes import staff_bp
from app.routes.supplier_routes import supplier_bp
from app.routes.driver_routes import bp as driver_bp 

db = SQLAlchemy()

def get_app(config_name):
    app = Flask(__name__)
    app.register_blueprint(staff_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(driver_bp)

    user = 'root'
    password = ''
    host = 'localhost'

    if config_name == 'production':
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@{host}/movie_munchers_prod'
    elif config_name == 'development':
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@{host}/movie_munchers_dev'
    elif config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@{host}/movie_munchers_test'
        app.config['TESTING'] = True

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app
