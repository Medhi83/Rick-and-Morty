from datetime import datetime
from typing import Any, Dict

from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_sqlalchemy import BaseQuery

from ..helpers import SQLCursorPage
from .models import CharacterNotInEpisode, CommentModel
from .schemas import CommentCreateArgsSchema, CommentQueryArgsSchema, CommentSchema

blp_comments = Blueprint("comments", "comments", url_prefix="/comments", description="Operations on comments")


@blp_comments.route("/")
class CommentsListResource(MethodView):
    @blp_comments.arguments(CommentQueryArgsSchema, location="query")
    @blp_comments.response(200, CommentSchema(many=True))
    @blp_comments.paginate(SQLCursorPage)
    def get(self, query) -> BaseQuery:
        """List comments"""
        return CommentModel.query.filter_by(**query)

    @blp_comments.arguments(CommentCreateArgsSchema, required=True)
    @blp_comments.response(201, CommentSchema)
    def post(self, data) -> CommentModel:
        """Add a new comment"""
        try:
            comment = CommentModel(**data)
            comment.save_to_db()
        except CharacterNotInEpisode:
            abort(400, "The character is not in the episode.")

        return comment


@blp_comments.route("/<comment_id>")
class CommentResource(MethodView):
    @blp_comments.response(200, CommentSchema)
    def get(self, comment_id) -> CommentModel:
        """Get comment by ID"""
        return CommentModel.query.get_or_404(comment_id)

    @blp_comments.arguments(CommentCreateArgsSchema, required=True)
    @blp_comments.response(200, CommentSchema)
    def put(self, update_data, comment_id) -> CommentModel:
        """Update existing comment"""
        comment: CommentModel = CommentModel.query.get_or_404(comment_id)
        try:
            comment.content = update_data["content"]
            comment.episode = update_data.get("episode")
            comment.character = update_data.get("character")
            comment.updated_time = datetime.utcnow()
            comment.save_to_db()
        except CharacterNotInEpisode:
            abort(400, "The character is not in the episode.")
        return comment

    @blp_comments.response(204)
    def delete(self, comment_id) -> None:
        """Delete comment"""
        comment: CommentModel = CommentModel.query.get_or_404(comment_id)
        comment.delete_from_db()
