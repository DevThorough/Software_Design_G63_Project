from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from pymongo import MongoClient
from flask_login import LoginManager
from .views import views
from .auth import auth
from .profile import profile
from .fuel_quote import fuelquote
from .fuel_quote_history import fq_history
from .pricing import pricing

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'group63'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db_m = client['se_G63']


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(profile, url_prefix='/')
    app.register_blueprint(fuelquote, url_prefix='/')
    app.register_blueprint(fq_history, url_prefix='/')
    app.register_blueprint(pricing, url_prefix='/')

    from .models import User

    with app.app_context():
        db.drop_all()
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app