"""Definition of resources for the content endpoints."""
from datetime import datetime
import json
from uuid import uuid4
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from ..models.user import AdminUser, EditorUser, User
from ..models.content import Content, ContentSchema
from ..extensions import DB as db
from ..services.producer import Producer
from ..utils.api_response import Response
from ..utils.decorators import roles_required

CONTENT_SCHEMA = ContentSchema()
CONTENTS_SCHEMA = ContentSchema(many=True)
PRODUCER = Producer()

class ContentListResource(Resource):
    """Resource to handle the content list."""
    @jwt_required()
    def get(self):
        """Method to get all contents."""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 15, type=int)
        pagination_object = Content.query.filter(
            Content.deleted_at.is_(None)
        ).paginate(page=page, per_page=per_page)
        contents = pagination_object.items
        pagination_info = {
            'total_items': pagination_object.total,
            'total_pages': pagination_object.pages,
            'current_page': pagination_object.page,
            'next_page': pagination_object.next_num,
            'prev_page': pagination_object.prev_num,
            'per_page': pagination_object.per_page
        }
        response = Response(
            payload=CONTENTS_SCHEMA.dump(contents),
            message='Contents retrieved successfully',
            status=200,
            pagination=pagination_info
        )
        return response.to_dict(), 200

    @jwt_required()
    @roles_required("admin", "editor")
    def post(self):
        """Method to create a new content."""
        data = request.get_json()
        data['id'] = str(uuid4())
        content = CONTENT_SCHEMA.load(data, session=db.session)
        db.session.add(content)
        db.session.commit()

        # Publish message to RabbitMQ
        message = {
            "op": "create",
            "id": content.id,
            "title": content.title,
            "content": content.content
        }
        PRODUCER.publish_message(json.dumps(message))
        response = Response(
            payload=CONTENT_SCHEMA.dump(content),
            message='Content created successfully',
            status=201
        )
        return response.to_dict(), 201

class ContentResource(Resource):
    """Resource to handle a single content."""
    @jwt_required()
    def get(self, id):
        """Method to get a single content."""
        content = Content.query.filter(Content.deleted_at.is_(None), Content.id == id).first()
        if content:
            response = Response(
                payload=CONTENT_SCHEMA.dump(content),
                message='Content retrieved successfully'
            )
            return response.to_dict(), 200
        response = Response(
            message='Unable to retrieve content',
            error='Content not found',
            status=404
        )
        return response.to_dict(), 404

    @jwt_required()
    @roles_required("admin", "editor")
    def put(self, id):
        """Method to update a single content."""
        content = Content.query.filter(Content.deleted_at.is_(None), Content.id == id).first()
        if not content:
            response = Response(
                message='Unable to edit content',
                error='Content not found',
                status=404
            )
            return response.to_dict(), 404
        data = request.get_json()
        content.updated_at = datetime.now()
        content = CONTENT_SCHEMA.load(data, instance=content, partial=True, session=db.session)
        db.session.commit()

        # Publish message to RabbitMQ
        message = {
            "op": "update",
            "id": content.id,
            "title": content.title,
            "content": content.content
        }
        PRODUCER.publish_message(json.dumps(message))
        response = Response(
            payload=CONTENT_SCHEMA.dump(content),
            message='Content updated successfully'
        )
        return response.to_dict(), 200

    @jwt_required()
    @roles_required("admin", "editor")
    def delete(self, id):
        """Method to delete a single content."""
        content = Content.query.filter(Content.deleted_at.is_(None), Content.id == id).first()
        if not content:
            response = Response(
                message='Unable to delete content',
                error='Content not found',
                status=404
            )
            return response.to_dict(), 404
        content.deleted_at = datetime.now()
        db.session.commit()

        # Publish message to RabbitMQ
        message = {
            "op": "delete",
            "id": content.id,
            "title": None,
            "content": None
        }
        PRODUCER.publish_message(json.dumps(message))
        response = Response(
            message='Content deleted successfully'
        )
        return response.to_dict(), 200
