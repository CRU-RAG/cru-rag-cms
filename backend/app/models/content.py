"""Content Model"""
from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..extensions import DB as db

class Content(db.Model):
    """Content Model"""
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(5000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        """Method to return a dictionary of the model"""
        short_content = self.content[:50] + '...' if len(self.content) > 50 else self.content
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'short_content': short_content,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }

    def __repr__(self):
        """Method to return a string representation of the model"""
        return f"\
            Item('{self.name}', '{self.description}'), '{self.created_at}',\
                  '{self.updated_at}', '{self.deleted_at}'"

class ContentSchema(SQLAlchemyAutoSchema):
    """Content Schema"""
    class Meta:
        """Meta class for Content Schema"""
        model = Content
        load_instance = True
