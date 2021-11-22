from app.characters.models import CharacterModel
from flask.testing import FlaskClient

from ..test_app import client


def test_get_list(client: FlaskClient):
    """Get list of characters."""
    # Setup
    rick = CharacterModel("Rick Sanchez", "Alive", "Human", "", "Male")
    rick.save_to_db()

    # Test
    response = client.get("/characters/")
    json_data = response.get_json()
    assert json_data == [rick.json(with_episodes=True)]
    assert response.status_code == 200
