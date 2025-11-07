from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from datetime import timedelta

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins=["http://localhost:3000", "https://localhost:3000"])

    app.config['SECRET_KEY'] = 'faedda1dcedc8a54042c86aaa6caf6b8'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=1)

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
    login_manager.init_app(app)
    login_manager.login_view = None 
    login_manager.session_protection = None

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import Users
        return Users.query.filter_by(id=int(user_id)).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({'error': 'Unauthorized - login required'}), 401
    
    from app.routes.customer_routes import customer_bp
    from app.routes.user_routes import user_bp
    from app.routes.staff_routes import staff_bp
    from app.routes.supplier_routes import supplier_bp
    from app.routes.driver_routes import driver_bp

    app.register_blueprint(customer_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(driver_bp)

    return app
