"""Module to define the resources for the comments."""

from datetime import datetime
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.middlewares.is_own_comment import is_own_comment
from app.middlewares.is_own_comment_or_accessed_by_admin import (
    is_own_comment_or_accessed_by_admin,
)

from ..models.comment import Comment, CommentSchema
from ..extensions import DB as db
from .base_resource import BaseResource

COMMENT_SCHEMA = CommentSchema()
COMMENTS_SCHEMA = CommentSchema(many=True)


class CommentListResource(BaseResource):
    """Resource to handle the list of comments."""

    @jwt_required()
    def post(self):
        """Create a new comment."""
        data = request.get_json()
        current_user_id = get_jwt_identity()
        data["user_id"] = current_user_id
        comment = Comment(**data)
        db.session.add(comment)
        db.session.commit()
        return self.make_response(
            payload=COMMENT_SCHEMA.dump(comment),
            message="Comment created successfully",
            status=201,
        )


class CommentResource(BaseResource):
    """Resource to handle a single comment."""

    @jwt_required()
    @is_own_comment
    def put(self, comment_id):
        """Update a comment."""
        comment = Comment.query.filter_by(id=comment_id, deleted_at=None).first()
        if not comment:
            return self.make_response(
                message="Unable to update comment",
                error="Comment not found",
                status=404,
            )
        data = request.get_json()
        comment.comment_text = data.get("comment_text", comment.comment_text)
        comment.updated_at = datetime.now()
        db.session.commit()
        return self.make_response(
            payload=COMMENT_SCHEMA.dump(comment),
            message="Comment updated successfully",
        )

    @jwt_required()
    @is_own_comment_or_accessed_by_admin
    def delete(self, comment_id):
        """Delete a comment."""
        comment = Comment.query.filter_by(id=comment_id, deleted_at=None).first()
        if not comment:
            return self.make_response(
                message="Unable to delete comment",
                error="Comment not found",
                status=404,
            )
        comment.deleted_at = datetime.now()
        db.session.commit()
        return self.make_response(
            message="Comment deleted successfully",
        )
