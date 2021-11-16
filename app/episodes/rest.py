from typing import Dict, List

from flask_restful import Resource

from .models import EpisodeModel


class Episodes(Resource):
    def get(self) -> Dict[str, List]:
        episodes = EpisodeModel.query.all()
        return {"episodes": [episode.json() for episode in episodes]}
