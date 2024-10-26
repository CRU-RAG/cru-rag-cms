"""Module to define the KnowledgeBase model"""
from . import db

class KnowledgeBase(db.Model):
    """KnowledgeBase Model"""
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(5000), nullable=False)

    def to_dict(self):
        """Method to return a dictionary of the model"""
        short_content = self.content[:50] + '...' if len(self.content) > 50 else self.content
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'short_content': short_content
        }

    def __repr__(self):
        """Method to return a string representation of the model"""
        return f"Item('{self.name}', '{self.description}')"
