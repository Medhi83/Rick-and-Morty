from typing import Any, Dict

import marshmallow as ma
from flask.views import MethodView
from flask_smorest import Blueprint

from .models import EpisodeModel
from .schemas import EpisodesPaginationSchema

blueprint_episodes = Blueprint("episodes", "episodes", url_prefix="/episodes", description="Operations on episodes")


@blueprint_episodes.route("/")
class Episodes(MethodView):
    @blueprint_episodes.response(200, EpisodesPaginationSchema())
    @blueprint_episodes.paginate()
    def get(self, pagination_parameters) -> Dict[str, Any]:
        pagination_results = EpisodeModel.query.paginate(
            page=pagination_parameters.page, per_page=pagination_parameters.page_size
        )
        pagination_parameters.item_count = len(pagination_results.items)
        return {
            "objects": [episode.json(with_characters=True) for episode in pagination_results.items],
            "page": pagination_results.page,
            "per_page": pagination_results.per_page,
            "total_pages": pagination_results.pages,
            "total_objects": pagination_results.total,
        }
