"""Definition of resources for the content endpoints."""
from datetime import datetime
import json
from uuid import uuid4
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User, UserRole
from ..models.content import Content, ContentSchema
from ..extensions import DB as db
from ..services.producer import Producer
from ..utils.api_response import SuccessResponse, ErrorResponse

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
        contents = Content.query.filter(
            Content.deleted_at.is_(None)
        ).paginate(page=page, per_page=per_page)
        return {
            'total': contents.total,
            'pages': contents.pages,
            'current_page': contents.page,
            'next_page': contents.next_num,
            'prev_page': contents.prev_num,
            'data': CONTENTS_SCHEMA.dump(contents.items)
        }, 200

    @jwt_required()
    def post(self):
        """Method to create a new content."""
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if current_user.role not in [UserRole.admin, UserRole.editor]:
            response = ErrorResponse(message='You do not have permission to create content')
            return response.to_dict(), 403
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
        response = SuccessResponse(data=CONTENT_SCHEMA.dump(content))
        return response.to_dict(), 201

class ContentResource(Resource):
    """Resource to handle a single content."""
    @jwt_required()
    def get(self, id):
        """Method to get a single content."""
        content = Content.query.filter(Content.deleted_at.is_(None), Content.id == id).first()
        if content:
            response = SuccessResponse(data=CONTENT_SCHEMA.dump(content))
            return response.to_dict(), 200
        response = ErrorResponse(message='Content not found')
        return response.to_dict(), 404

    @jwt_required()
    def put(self, id):
        """Method to update a single content."""
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if current_user.role not in [UserRole.admin, UserRole.editor]:
            response = ErrorResponse(message='You do not have permission to update content')
            return response.to_dict(), 403
        content = Content.query.filter(Content.deleted_at.is_(None), Content.id == id).first()
        if not content:
            response = ErrorResponse(message='Content not found')
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
        response = SuccessResponse(data=CONTENT_SCHEMA.dump(content))
        return response.to_dict(), 200

    @jwt_required()
    def delete(self, id):
        """Method to delete a single content."""
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if current_user.role not in [UserRole.admin, UserRole.editor]:
            response = ErrorResponse(message='You do not have permission to delete content')
            return response.to_dict(), 403
        content = Content.query.filter(Content.deleted_at.is_(None), Content.id == id).first()
        if not content:
            response = ErrorResponse(message='Content not found')
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
        response = SuccessResponse(message='Content deleted successfully')
        return response.to_dict(), 200
