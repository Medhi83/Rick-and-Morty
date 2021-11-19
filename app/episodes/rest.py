from typing import Dict, List

from flask.views import MethodView
from flask_smorest import Blueprint

from .models import EpisodeModel

blueprint_episodes = Blueprint("episodes", "episodes", url_prefix="/episodes", description="Operations on episodes")


@blueprint_episodes.route("/")
class Episodes(MethodView):
    def get(self) -> Dict[str, List]:
        episodes = EpisodeModel.query.all()
        return {"episodes": [episode.json() for episode in episodes]}
