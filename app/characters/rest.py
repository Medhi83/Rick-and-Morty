from typing import Any, Dict

from flask.views import MethodView
from flask_smorest import Blueprint

from .models import CharacterModel

blueprint_characters = Blueprint(
    "characters", "characters", url_prefix="/characters", description="Operations on characters"
)


@blueprint_characters.route("/")
class Characters(MethodView):
    @blueprint_characters.paginate()
    def get(self, pagination_parameters) -> Dict[str, Any]:
        pagination_results = CharacterModel.query.paginate(
            page=pagination_parameters.page, per_page=pagination_parameters.page_size
        )
        pagination_parameters.item_count = len(pagination_results.items)
        return {
            "objects": [character.json(with_episodes=True) for character in pagination_results.items],
            "page": pagination_results.page,
            "per_page": pagination_results.per_page,
            "count": pagination_parameters.item_count,
            "total_pages": pagination_results.pages,
            "total_objects": pagination_results.total,
        }
