import os

from flask import Flask
from flask_restful import Api

from .characters.rest import Characters
from .db import db
from .episodes.rest import Episodes

app = Flask(__name__)
api = Api(app, prefix="/api")

api.add_resource(Characters, "/characters")
api.add_resource(Episodes, "/episodes")

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.before_first_request
def create_tables() -> None:
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
