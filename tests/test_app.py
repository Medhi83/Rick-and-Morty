from typing import Generator

import pytest
from app.db import db
from app.main import create_app
from flask import Flask
from flask.testing import FlaskClient

TEST_DATABASE_URI = "sqlite:///test_data.db"


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    """Setup Flask client and database for tests."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = TEST_DATABASE_URI

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    _tearsdown(app)


def _tearsdown(app: Flask) -> None:
    with app.app_context():
        db.drop_all()
