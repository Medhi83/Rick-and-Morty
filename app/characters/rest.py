from typing import Dict, List

from flask.views import MethodView
from flask_smorest import Blueprint

from .models import CharacterModel

blueprint_characters = Blueprint(
    "characters", "characters", url_prefix="/characters", description="Operations on characters"
)


@blueprint_characters.route("/")
class Characters(MethodView):
    def get(self) -> Dict[str, List]:
        characters = CharacterModel.query.all()
        return {"characters": [character.json() for character in characters]}
