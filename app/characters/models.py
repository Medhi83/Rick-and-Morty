from typing import Any, Dict, List, Optional, Union

from ..db import db

episodes_table = db.Table(
    "episodes",
    db.Column("episode_id", db.Integer, db.ForeignKey("episode.id"), primary_key=True),
    db.Column("character_id", db.Integer, db.ForeignKey("character.id"), primary_key=True),
)


class CharacterModel(db.Model):
    __tablename__ = "character"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    status = db.Column(db.String(255))
    species = db.Column(db.String(255))
    type = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    episodes = db.relationship(
        "EpisodeModel", secondary=episodes_table, lazy="joined", backref=db.backref("characters", lazy="joined")
    )

    def __init__(
        self,
        name: str,
        status: str,
        species: str,
        _type: str,
        gender: str,
        episodes: Optional[List[int]] = None,
        _id: Optional[int] = None,
    ) -> None:
        if _id is not None:
            self.id = _id
        self.name = name
        self.status = status
        self.species = species
        self.type = _type
        self.gender = gender
        if episodes is not None:
            self.episodes = episodes

    def json(self) -> Dict[str, Union[str, Any]]:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "species": self.species,
            "type": self.type,
            "gender": self.gender,
            "episodes": [episode.json() for episode in self.episodes],
        }

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
