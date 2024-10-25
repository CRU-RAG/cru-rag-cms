from . import db

class KnowledgeBase(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        short_content = self.content[:50] + '...' if len(self.content) > 50 else self.content
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'short_content': short_content
        }

    def __repr__(self):
        return f"Item('{self.name}', '{self.description}')"