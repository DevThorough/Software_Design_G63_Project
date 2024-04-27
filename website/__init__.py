from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'group63'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from website.views import views
    from website.auth import auth
    from website.profile import profile
    from website.fuel_quote import fuelquote
    from website.fuel_quote_history import fq_history
    from website.pricing import pricing

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(profile, url_prefix='/')
    app.register_blueprint(fuelquote, url_prefix='/')
    app.register_blueprint(fq_history, url_prefix='/')
    app.register_blueprint(pricing, url_prefix='/')

    from website.models import User

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