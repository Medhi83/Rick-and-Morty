from flask.views import MethodView
from flask_smorest import Blueprint
from flask_sqlalchemy import BaseQuery

from ..helpers import SQLCursorPage
from .models import EpisodeModel
from .schemas import EpisodeQueryArgsSchema, EpisodeSchema

blueprint_episodes = Blueprint("episodes", "episodes", url_prefix="/episodes", description="Operations on episodes")


@blueprint_episodes.route("/")
class EpisodesListResource(MethodView):
    @blueprint_episodes.arguments(EpisodeQueryArgsSchema, location="query")
    @blueprint_episodes.response(200, EpisodeSchema(many=True))
    @blueprint_episodes.paginate(SQLCursorPage)
    def get(self, query) -> BaseQuery:
        return EpisodeModel.query.filter_by(**query)
