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
    assert json_data == {
        "count": 1,
        "objects": [rick.json(with_episodes=True)],
        "page": 1,
        "per_page": 10,
        "total_objects": 1,
        "total_pages": 1,
    }
    assert response.status_code == 200
