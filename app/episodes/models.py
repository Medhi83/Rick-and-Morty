from datetime import datetime
from typing import Dict, Optional, Union

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

    def json(self) -> Dict[str, Union[str, int, datetime]]:
        return {
            "id": self.id,
            "name": self.name,
            "air_date": self.air_date.strftime("%B %d, %Y"),
            "episode": self.episode,
        }

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
