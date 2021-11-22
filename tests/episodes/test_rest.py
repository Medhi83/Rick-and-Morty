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
    assert json_data == [episode.json(with_characters=True)]
    assert response.status_code == 200
