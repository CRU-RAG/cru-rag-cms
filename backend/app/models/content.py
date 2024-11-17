"""Content Model"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import and_
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from ..extensions import DB as db
from ..models.comment import CommentSchema, Comment


class Content(db.Model):
    """Content Model"""

    __tablename__ = "content"

    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(5000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Add relationship to comments
    comments = db.relationship(
        "Comment",
        primaryjoin=and_(Comment.content_id == id, Comment.deleted_at is None),
        backref="content",
        lazy="dynamic",
    )

    def __init__(self, title, body):
        """Method to initialize a content"""
        self.id = str(uuid4())
        self.title = title
        self.body = body

    def to_dict(self):
        """Method to return a dictionary of the model"""
        short_content = (
            self.content[:50] + "..." if len(self.content) > 50 else self.content
        )
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "short_content": short_content,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }

    def __repr__(self):
        """Method to return a string representation of the model"""
        return f"\
            Item('{self.title}', '{self.body}'), '{self.created_at}',\
                  '{self.updated_at}', '{self.deleted_at}'"


# pylint: disable=too-few-public-methods
class ContentSchema(SQLAlchemyAutoSchema):
    """Content Schema"""

    # Include comments in serialization
    comments = fields.Nested(CommentSchema, many=True)

    class Meta:
        """Meta class for Content Schema"""

        model = Content
        load_instance = True
        include_fk = True
