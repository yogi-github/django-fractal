from flask import Flask
from .config import Config
from .models import db
from .views import bp


def create_app(config_class=Config):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)
    flask_app.register_blueprint(bp)
    db.init_app(flask_app)

    return flask_app


main_app = create_app()
