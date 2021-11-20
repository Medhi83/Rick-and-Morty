from app.comments.models import CommentModel
from app.characters.models import CharacterModel
from app.episodes.models import EpisodeModel
from flask.testing import FlaskClient
from datetime import datetime

from ..test_app import client


def test_get_list(client: FlaskClient):
    """Get list of comments."""
    # Setup
    rick = CharacterModel("Rick Sanchez", "Alive", "Human", "", "Male")
    rick.save_to_db()

    episode = EpisodeModel("The ABC's of Beth", datetime(2017, 9, 24), "S03E09")
    episode.save_to_db()

    comment = CommentModel("Hello World, "*1000, rick.id, episode.id)
    comment.save_to_db()

    # Test
    response = client.get("/comments/")
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data == {
        "count": 1,
        "objects": [comment.json()],
        "page": 1,
        "per_page": 10,
        "total_objects": 1,
        "total_pages": 1,
    }
