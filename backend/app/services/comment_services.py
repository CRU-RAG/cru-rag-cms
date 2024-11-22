"""Helper functions for comments."""

from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import abort
from app.models.comment import Comment


def get_comment_and_user(**kwargs):
    """Helper to retrieve the current user and comment."""
    verify_jwt_in_request()
    current_user_id = get_jwt_identity()
    comment_id = kwargs.get("comment_id")
    comment = Comment.query.filter_by(id=comment_id, deleted_at=None).first()
    if not comment:
        abort(404, description="Comment not found.")
    return current_user_id, comment
