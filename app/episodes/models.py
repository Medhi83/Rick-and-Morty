from datetime import datetime
from typing import Any, Dict, Generator, Optional, Union

from ..characters.models import CharacterModel
from ..db import db


class EpisodeModel(db.Model):
    __tablename__ = "episode"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    air_date = db.Column(db.DateTime)
    episode = db.Column(db.String(255))

    def __init__(
        self,
        name: str,
        air_date: datetime,
        episode: str,
        _id: Optional[int] = None,
    ) -> None:
        if _id is not None:
            self.id = _id
        self.name = name
        self.air_date = air_date
        self.episode = episode

    def json(self, with_characters: bool = False) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "name": self.name,
            "air_date": self.air_date.strftime("%B %d, %Y"),
            "episode": self.episode,
        }
        if with_characters:
            data.update({"characters": [character_json for character_json in self.get_characters_to_json()]})
        return data

    def get_characters_to_json(self) -> Generator[Dict, None, None]:
        for character in CharacterModel.query.with_parent(self):
            yield character.json()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
