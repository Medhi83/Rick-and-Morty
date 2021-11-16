from datetime import datetime
from typing import Dict, Union

from ..db import db


class EpisodeModel(db.Model):
    __tablename__ = "episode"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    air_date = db.Column(db.DateTime)
    episode = db.Column(db.String(255))

    def __init__(self, name: str, air_date: datetime, episode: str) -> None:
        self.name = name
        self.air_date = air_date
        self.episode = episode

    def json(self) -> Dict[str, Union[str, int, datetime]]:
        return {"id": self.id, "name": self.name, "air_date": self.air_date, "episode": self.episode}

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
