from datetime import datetime
from app.episodes.models import EpisodeModel
from flask.testing import FlaskClient

from ..test_app import client


def test_get_list(client: FlaskClient):
    """Get list of episodes."""
    # Setup
    episode = EpisodeModel("The ABC's of Beth", datetime(2017, 9, 24), "S03E09")
    episode.save_to_db()

    # Test
    response = client.get("/episodes/")
    json_data = response.get_json()
    assert json_data == {
        "count": 1,
        "objects": [episode.json(with_characters=True)],
        "page": 1,
        "per_page": 10,
        "total_objects": 1,
        "total_pages": 1,
    }
    assert response.status_code == 200
