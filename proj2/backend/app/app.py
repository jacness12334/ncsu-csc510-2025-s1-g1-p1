from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def get_app(config_name):
    app = Flask(__name__)
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

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from models import Users
        return Users.query.get(int(user_id))
    
    from routes.customer_routes import customer_bp
    # from routes.user_routes import user_bp

    app.register_blueprint(customer_bp)
    # app.register_blueprint(user_bp)

    return app
