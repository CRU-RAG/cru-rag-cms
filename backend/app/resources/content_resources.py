from datetime import datetime
import json
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from uuid import uuid4
from ..models.content import Content, db
from ..models.content import ContentSchema
from ..services.producer import Producer

content_schema = ContentSchema()
contents_schema = ContentSchema(many=True)
producer = Producer()

class ContentListResource(Resource):
    @jwt_required()
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 15, type=int)
        contents = Content.query.filter(Content.deleted_at.is_(None)).paginate(page=page, per_page=per_page)
        return {
            'total': contents.total,
            'pages': contents.pages,
            'current_page': contents.page,
            'next_page': contents.next_num,
            'prev_page': contents.prev_num,
            'data': contents_schema.dump(contents.items)
        }, 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        data['id'] = str(uuid4())
        content = content_schema.load(data, session=db.session)
        db.session.add(content)
        db.session.commit()

        # Publish message to RabbitMQ
        message = {
            "op": "create",
            "id": content.id,
            "title": content.title,
            "content": content.content
        }
        producer.publish_message(json.dumps(message))

        return content_schema.dump(content), 201
    
class ContentResource(Resource):
    @jwt_required()
    def get(self, id):
        content = Content.query.filter(Content.deleted_at.is_(None), Content.id == id).first()
        if content:
            return content_schema.dump(content), 200
        return {'message': 'Content not found'}, 404

    @jwt_required()
    def put(self, id):
        content = Content.query.get_or_404(id)
        data = request.get_json()
        content.updated_at = datetime.now()
        content = content_schema.load(data, instance=content, partial=True, session=db.session)
        db.session.commit()

        # Publish message to RabbitMQ
        message = {
            "op": "update",
            "id": content.id,
            "title": content.title,
            "content": content.content
        }
        producer.publish_message(json.dumps(message))

        return content_schema.dump(content), 200

    @jwt_required()
    def delete(self, id):
        content = Content.query.get_or_404(id)
        data = request.get_json()
        content.deleted_at = datetime.now()
        content = content_schema.load(data, instance=content, partial=True, session=db.session)
        db.session.commit()

        # Publish message to RabbitMQ
        message = {
            "op": "delete",
            "id": content.id,
            "title": None,
            "content": None
        }
        producer.publish_message(json.dumps(message))
        
        return content_schema.dump(content), 204
