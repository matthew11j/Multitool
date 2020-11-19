from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from multitool.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)

    from multitool.users.routes import users
    from multitool.main.routes import main
    from multitool.golf.routes import golf
    from multitool.music.routes import music
    from multitool.weather.routes import weather
    from multitool.mp3converter.routes import mp3converter
    from multitool.nutrimeal.routes import nutrimeal
    from multitool.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(golf)
    app.register_blueprint(music)
    app.register_blueprint(weather)
    app.register_blueprint(mp3converter)
    app.register_blueprint(nutrimeal)
    app.register_blueprint(errors)

    return app
