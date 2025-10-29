from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_app():
    app = Flask(__name__)
    password = ""
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{password}@localhost/movie_munchers'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app