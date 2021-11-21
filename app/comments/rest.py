from typing import Any, Dict

from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint

from .models import CharacterNotInEpisode, CommentModel
from .schemas import CommentCreateArgsSchema, CommentSchema, CommentsPaginationSchema

blueprint_comments = Blueprint("comments", "comments", url_prefix="/comments", description="Operations on comments")


@blueprint_comments.route("/")
class CommentListResource(MethodView):
    @blueprint_comments.response(200, CommentsPaginationSchema())
    @blueprint_comments.paginate()
    def get(self, pagination_parameters) -> Dict[str, Any]:
        """List comments"""
        pagination_results = CommentModel.query.paginate(
            page=pagination_parameters.page, per_page=pagination_parameters.page_size
        )
        pagination_parameters.item_count = len(pagination_results.items)
        return {
            "objects": [comment.json() for comment in pagination_results.items],
            "page": pagination_results.page,
            "per_page": pagination_results.per_page,
            "total_pages": pagination_results.pages,
            "total_objects": pagination_results.total,
        }

    @blueprint_comments.arguments(CommentCreateArgsSchema, required=True)
    @blueprint_comments.response(201, CommentSchema)
    def post(self, data):
        """Add a new comment"""
        try:
            comment = CommentModel(**data)
            comment.save_to_db()
        except CharacterNotInEpisode:
            abort(400, "The character is not in the episode.")

        return comment


@blueprint_comments.route("/<comment_id>")
class CommentResource(MethodView):
    @blueprint_comments.response(200, CommentSchema)
    def get(self, comment_id):
        """Get comment by ID"""
        comment: CommentModel = CommentModel.query.get_or_404(comment_id)
        return comment.json()

    @blueprint_comments.arguments(CommentCreateArgsSchema, required=True)
    @blueprint_comments.response(200, CommentSchema)
    def put(self, update_data, comment_id):
        """Update existing comment"""
        comment: CommentModel = CommentModel.query.get_or_404(comment_id)
        try:
            comment.content = update_data["content"]
            comment.episode = update_data.get("episode")
            comment.character = update_data.get("character")
            comment.save_to_db()
        except CharacterNotInEpisode:
            abort(400, "The character is not in the episode.")
        return comment.json()

    @blueprint_comments.response(204)
    def delete(self, comment_id):
        """Delete comment"""
        comment: CommentModel = CommentModel.query.get_or_404(comment_id)
        comment.delete_from_db()
