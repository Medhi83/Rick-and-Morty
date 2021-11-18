import sys

sys.path.append("..")

import json
from datetime import datetime
from typing import Dict, List

from app.characters.models import CharacterModel, episodes_table
from app.db import db
from app.episodes.models import EpisodeModel
from app.main import app

DATABASE_URI = "mysql+pymysql://root:test@localhost/rick_n_morty"
JSON_CHARACTERS_FILE = "./json_data/rick_morty-characters_v1.json"
JSON_EPISODES_FILE = "./json_data/rick_morty-episodes_v1.json"


class ImportData:
    def __init__(self) -> None:
        self.relationships: Dict[int, List[int]] = {}

    def run(self) -> None:
        episodes_data = self.get_data(JSON_EPISODES_FILE)
        characters_data = self.get_data(JSON_CHARACTERS_FILE)

        db.create_all()  # create tables
        self.import_episodes(episodes_data)
        self.import_characters(characters_data)
        db.session.commit()
        self.import_relationships()
        db.session.commit()

    @staticmethod
    def get_data(file_path: str) -> Dict:
        """Transform json data from a file to a dictionnary"""
        f = open(file_path)
        return json.load(f)

    def _add_relationship(self, episode_id: int, character_id: int) -> None:
        if episode_id not in self.relationships:
            self.relationships[episode_id] = []
        if character_id not in self.relationships[episode_id]:
            self.relationships[episode_id].append(character_id)

    def import_relationships(self) -> None:
        for episode_id in self.relationships:
            for character_id in self.relationships[episode_id]:
                statement = episodes_table.insert().values(episode_id=episode_id, character_id=character_id)
                db.session.execute(statement)

    def import_episodes(self, data: Dict) -> None:
        for episode in data:
            episode["_id"] = episode["id"]
            del episode["id"]

            for character_id in episode["characters"]:
                self._add_relationship(episode["_id"], character_id)

            del episode["characters"]
            episode["air_date"] = datetime.strptime(episode["air_date"], "%B %d, %Y")
            model = EpisodeModel(**episode)
            db.session.add(model)

    def import_characters(self, data: Dict) -> None:
        for character in data:
            character["_id"] = character["id"]
            character["_type"] = character["type"]

            for episode_id in character["episode"]:
                self._add_relationship(episode_id, character["_id"])

            del character["id"]
            del character["type"]
            del character["episode"]
            model = CharacterModel(**character)
            db.session.add(model)


if __name__ == "__main__":
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    with app.app_context():
        ImportData().run()
