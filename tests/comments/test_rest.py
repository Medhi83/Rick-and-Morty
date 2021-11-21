from datetime import datetime
from typing import Tuple

from app.characters.models import CharacterModel
from app.comments.models import CommentModel
from app.db import db
from app.episodes.models import EpisodeModel
from flask.testing import FlaskClient

from ..test_app import client

RESOURCE_COMMENTS = "/comments/"


def add_episode_with_character() -> Tuple[CharacterModel, EpisodeModel]:
    episode = EpisodeModel("The ABC's of Beth", datetime(2017, 9, 24), "S03E09")
    episode.save_to_db()
    rick = CharacterModel("Rick Sanchez", "Alive", "Human", "", "Male")
    rick.episodes.append(episode)
    rick.save_to_db()

    return rick, episode


def add_comment_in_db() -> Tuple[CharacterModel, EpisodeModel, CommentModel]:
    rick, episode = add_episode_with_character()
    comment = CommentModel("Hello World", rick, episode)
    comment.save_to_db()
    return rick, episode, comment


def test_get_list(client: FlaskClient) -> None:
    """Should get a list of comments."""
    # Setup
    _, _, comment = add_comment_in_db()

    # Test
    response = client.get(RESOURCE_COMMENTS)
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data == {
        "objects": [comment.json()],
        "page": 1,
        "per_page": 10,
        "total_objects": 1,
        "total_pages": 1,
    }


def test_get(client: FlaskClient) -> None:
    """Should get an existing comment"""
    # Setup
    _, _, comment = add_comment_in_db()

    # Test
    response = client.get(RESOURCE_COMMENTS + str(comment.id))
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data == comment.json()


def test_post(client: FlaskClient) -> None:
    """Should add a new comment on a character in an episode"""
    # Setup
    rick, episode = add_episode_with_character()

    # Test
    response = client.post(
        RESOURCE_COMMENTS, json={"content": "Hello World", "character_id": rick.id, "episode_id": episode.id}
    )
    assert response.status_code == 201


def test_put(client: FlaskClient) -> None:
    """Should update an existing comment"""
    # Setup
    rick, episode, comment = add_comment_in_db()

    # Test
    new_content = "This is another message!"
    response = client.put(
        RESOURCE_COMMENTS + str(comment.id),
        json={"content": new_content, "character_id": rick.id, "episode_id": episode.id},
    )
    assert response.status_code == 200
    db.session.refresh(comment)
    assert comment.content == new_content


def test_delete(client: FlaskClient) -> None:
    """Should remove an existing comment"""
    # Setup
    _, _, comment = add_comment_in_db()

    # Test
    response = client.delete(RESOURCE_COMMENTS + str(comment.id))
    assert response.status_code == 204
    assert CommentModel.query.get(comment.id) is None
