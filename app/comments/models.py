from datetime import datetime
from typing import Any, Dict, Optional, Union

from ..characters.models import CharacterModel
from ..db import db
from ..episodes.models import EpisodeModel


class CommentModel(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    character = db.Column(db.Integer, db.ForeignKey("character.id"))
    episode = db.Column(db.Integer, db.ForeignKey("episode.id"))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(
        self,
        content: str,
        character: CharacterModel,
        episode: EpisodeModel,
        created_time: Optional[datetime] = None,
        _id: Optional[int] = None,
    ) -> None:
        if _id is not None:
            self.id = _id
        self.content = content
        self.character = character
        self.episode = episode
        if created_time:
            self.created_time = created_time

    def json(self) -> Dict[str, Union[str, Any]]:
        return {
            "id": self.id,
            "content": self.content,
            "character": self.character,
            "episode": self.episode,
            "created_time": self.created_time.strftime("%B %d, %Y"),
        }

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
