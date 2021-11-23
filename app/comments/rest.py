import csv
import io
from datetime import datetime
from typing import Any, Dict

from flask import abort, make_response
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


@blp_comments.route("/export")
class CommentsExportResource(MethodView):
    @blp_comments.arguments(CommentQueryArgsSchema, location="query")
    @blp_comments.response(
        200,
        description="csv file",
        headers={
            "content-disposition": {"description": "attachment; filename=export.csv", "type": "string"},
            "content-type": {"description": "text/csv", "type": "string"},
        },
    )
    def get(self, query) -> BaseQuery:
        """Export comments as csv file"""

        def _get_csv_fields(comment: CommentModel) -> Dict[str, Any]:
            data = comment.json()
            added_data = {
                "character_id": None,
                "character_name": None,
                "episode_id": None,
                "episode_name": None,
            }
            if comment.character:
                added_data["character_id"] = comment.character.id
                added_data["character_name"] = comment.character.name
            if comment.episode:
                added_data["episode_id"] = comment.episode.id
                added_data["episode_name"] = comment.episode.name

            del data["character"]
            del data["episode"]
            data.update(added_data)

            return data

        fieldnames = [
            "id",
            "content",
            "character_id",
            "episode_id",
            "character_name",
            "episode_name",
            "created_time",
            "updated_time",
        ]

        comments = CommentModel.query.filter_by(**query)
        csv_rows = (_get_csv_fields(comment) for comment in comments)

        si = io.StringIO()
        writer = csv.DictWriter(si, fieldnames=fieldnames, dialect="excel")
        writer.writeheader()
        writer.writerows(csv_rows)

        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output
