from datetime import datetime
from typing import Any, Dict, Optional, Union

from ..characters.models import CharacterModel
from ..db import db
from ..episodes.models import EpisodeModel


class CommentException(Exception):
    """Exceptions Related to the comment model"""

    pass


class CharacterNotInEpisode(CommentException):
    """The character does not belong to the episode"""

    pass


class CommentModel(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
    episode_id = db.Column(db.Integer, db.ForeignKey("episode.id"))

    character = db.relationship("CharacterModel", lazy="joined")
    episode = db.relationship("EpisodeModel", lazy="joined")
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(
        self,
        content: str,
        character: Optional[CharacterModel] = None,
        episode: Optional[EpisodeModel] = None,
        _id: Optional[int] = None,
    ) -> None:
        if _id is not None:
            self.id = _id
        self.content = content
        self.character = character
        self.episode = episode

    def json(self) -> Dict[str, Union[str, Any]]:
        return {
            "id": self.id,
            "content": self.content,
            "character": self.character.json(),
            "episode": self.episode.json(),
            "created_time": self.created_time.strftime("%B %d, %Y"),
            "updated_time": self.updated_time.strftime("%B %d, %Y"),
        }

    def _validate_data(self):
        if self.episode and self.character and self.episode not in self.character.episodes:
            raise CharacterNotInEpisode()

    def save_to_db(self) -> None:
        self._validate_data()
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
