from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from os import path
import os

db = SQLAlchemy()
DB_NAME = "database.db"

moment = Moment()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(12).hex()
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .routes import routes
    from .auth import auth

    app.register_blueprint(routes, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Todo, Completed_Todo

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access that page."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    moment.init_app(app)

    return app

def create_database(app):
    if not path.exists(f"website/{DB_NAME}") and not os.environ.get("DATABASE_URL"):
        db.create_all(app=app)
        print("Initialized Database")
