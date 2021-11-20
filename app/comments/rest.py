from typing import Any, Dict

from flask.views import MethodView
from flask_smorest import Blueprint

from .models import CommentModel

blueprint_comments = Blueprint(
    "comments", "comments", url_prefix="/comments", description="Operations on comments"
)


@blueprint_comments.route("/")
class Comments(MethodView):
    @blueprint_comments.paginate()
    def get(self, pagination_parameters) -> Dict[str, Any]:
        pagination_results = CommentModel.query.paginate(
            page=pagination_parameters.page, per_page=pagination_parameters.page_size
        )
        pagination_parameters.item_count = len(pagination_results.items)
        return {
            "objects": [comment.json() for comment in pagination_results.items],
            "page": pagination_results.page,
            "per_page": pagination_results.per_page,
            "count": pagination_parameters.item_count,
            "total_pages": pagination_results.pages,
            "total_objects": pagination_results.total,
        }
    
    