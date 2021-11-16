from typing import Dict, List

from flask_restful import Resource

from .models import CharacterModel


class Characters(Resource):
    def get(self) -> Dict[str, List]:
        characters = CharacterModel.query.all()
        return {"characters": [character.json() for character in characters]}
