import os

from flask import Flask
from flask_smorest import Api


from .characters.rest import blueprint_characters
from .db import db
from .episodes.rest import blueprint_episodes

app = Flask(__name__)
app.config["API_TITLE"] = "Rick and Morty API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.1.0"

api = Api(app)
api.register_blueprint(blueprint_characters)
api.register_blueprint(blueprint_episodes)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.before_first_request
def create_tables() -> None:
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
