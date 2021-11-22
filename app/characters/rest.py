from flask.views import MethodView
from flask_smorest import Blueprint
from flask_sqlalchemy import BaseQuery

from ..helpers import SQLCursorPage
from .models import CharacterModel
from .schemas import CharacterSchema, CharacterQueryArgsSchema

blp_characters = Blueprint(
    "characters", "characters", url_prefix="/characters", description="Operations on characters"
)


@blp_characters.route("/")
class CharactersListResource(MethodView):
    @blp_characters.arguments(CharacterQueryArgsSchema, location="query")
    @blp_characters.response(200, CharacterSchema(many=True))
    @blp_characters.paginate(SQLCursorPage)
    def get(self, query) -> BaseQuery:
        return CharacterModel.query.filter_by(**query)
