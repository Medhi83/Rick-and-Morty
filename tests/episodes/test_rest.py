from flask.testing import FlaskClient

from ..test_app import client


def test_get_list(client: FlaskClient):
    """Get list of episodes"""
    response = client.get("/episodes/")
    assert response.status_code == 200
