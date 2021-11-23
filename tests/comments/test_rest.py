from datetime import datetime
from typing import Tuple

from app.characters.models import CharacterModel
from app.comments.models import CommentModel
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
    assert json_data == [comment.json()]


def test_get_list_with_query_arguments(client: FlaskClient) -> None:
    """Should get a list of comments filter by character_id."""
    # Setup
    _, _, comment = add_comment_in_db()

    # Test
    response = client.get(RESOURCE_COMMENTS, data={"character_id": 1})
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data == [comment.json()]


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
    assert comment.content == new_content


def test_delete(client: FlaskClient) -> None:
    """Should remove an existing comment"""
    # Setup
    _, _, comment = add_comment_in_db()

    # Test
    response = client.delete(RESOURCE_COMMENTS + str(comment.id))
    assert response.status_code == 204
    assert CommentModel.query.get(comment.id) is None


def test_export(client: FlaskClient) -> None:
    """Should export comments as csv file"""
    # Setup
    add_comment_in_db()

    # Test
    response = client.get(RESOURCE_COMMENTS + "export")
    assert response.status_code == 200
    assert response.headers.get("Content-Disposition") == "attachment; filename=export.csv"
    assert response.headers.get("Content-type") == "text/csv"
    assert (
        response.data == b"id,content,character_id,episode_id,character_name,episode_name,created_time,updated_time\r\n"
        b'1,Hello World,1,1,Rick Sanchez,The ABC\'s of Beth,"November 23, 2021","November 23, 2021"\r\n'
    )
