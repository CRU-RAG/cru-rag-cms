"""A model representing user comments on content."""

from datetime import datetime
from uuid import uuid4
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from ..extensions import DB as db


# pylint: disable=too-few-public-methods
class Comment(db.Model):
    """Comment model representing user comments on content."""

    __tablename__ = "comments"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey("users.id"), nullable=False)
    content_id = db.Column(db.String(100), db.ForeignKey("contents.id"), nullable=False)
    comment_text = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, user_id, content_id, comment_text):
        """Initialize a comment."""
        self.id = str(uuid4())
        self.user_id = user_id
        self.content_id = content_id
        self.comment_text = comment_text

    def __repr__(self):
        return f"<Comment {self.id}>"


class CommentSchema(SQLAlchemyAutoSchema):
    """Schema for the Comment model."""

    content = fields.Nested("ContentSchema", exclude=("comments",))

    class Meta:
        """Meta class for the Comment schema."""

        model = Comment
        load_instance = True
        include_fk = True
