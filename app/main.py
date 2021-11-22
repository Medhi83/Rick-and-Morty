import os

from flask import Flask
from flask_smorest import Api

from .characters.rest import blp_characters
from .comments.rest import blp_comments
from .db import db
from .episodes.rest import blueprint_episodes

class Config:
    API_TITLE = "Rick and Morty API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/api"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_VERSION = "3.24.2"
    OPENAPI_SWAGGER_UI_URL = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"
    OPENAPI_REDOC_PATH = "redoc"

def init_db(app: Flask):
    """Setup database."""
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    @app.before_first_request
    def create_tables() -> None:
        db.create_all()


def create_app() -> Flask:
    """Create Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    api = Api(app)
    api.register_blueprint(blp_characters)
    api.register_blueprint(blueprint_episodes)
    api.register_blueprint(blp_comments)

    init_db(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
