"""Definition of resources for the content endpoints."""

from datetime import datetime
import json
from flask import request
from flask_jwt_extended import jwt_required

from app.utils.pagination import get_pagination_info
from ..models.content import Content, ContentSchema
from ..extensions import DB as db
from ..services.producer import Producer
from .base_resource import BaseResource
from ..middlewares.is_admin_or_editor import is_admin_or_editor

CONTENT_SCHEMA = ContentSchema()
CONTENTS_SCHEMA = ContentSchema(many=True)
PRODUCER = Producer()


class ContentListResource(BaseResource):
    """Resource to handle the content list."""

    @jwt_required()
    def get(self):
        """Method to get all contents."""
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 15, type=int)
        pagination_object = Content.query.filter(Content.deleted_at.is_(None)).paginate(
            page=page, per_page=per_page
        )
        contents = pagination_object.items
        pagination_info = get_pagination_info(pagination_object)
        return self.make_response(
            payload=CONTENTS_SCHEMA.dump(contents),
            message="Contents retrieved successfully",
            status=200,
            pagination=pagination_info,
        )

    @jwt_required()
    @is_admin_or_editor
    def post(self):
        """Method to create a new content."""
        data = request.get_json()
        content = Content(title=data["title"], body=data["body"])
        db.session.add(content)
        db.session.commit()

        # Publish message to RabbitMQ
        message = {
            "op": "create",
            "id": content.id,
            "title": content.title,
            "body": content.body,
        }
        PRODUCER.publish_message(json.dumps(message))
        return self.make_response(
            payload=CONTENT_SCHEMA.dump(content),
            message="Content created successfully",
            status=201,
        )


class ContentResource(BaseResource):
    """Resource to handle a single content."""

    @jwt_required()
    def get(self, content_id):
        """Method to get a single content."""
        content = Content.query.filter(
            Content.deleted_at.is_(None), Content.id == content_id
        ).first()
        if content:
            return self.make_response(
                payload=CONTENT_SCHEMA.dump(content),
                message="Content retrieved successfully",
            )
        return self.make_response(
            message="Unable to retrieve content", error="Content not found", status=404
        )

    @jwt_required()
    @is_admin_or_editor
    def put(self, content_id):
        """Method to update a single content."""
        content = Content.query.filter(
            Content.deleted_at.is_(None), Content.id == content_id
        ).first()
        if not content:
            return self.make_response(
                message="Unable to edit content", error="Content not found", status=404
            )
        data = request.get_json()
        content.updated_at = datetime.now()
        content = CONTENT_SCHEMA.load(
            data, instance=content, partial=True, session=db.session
        )
        db.session.commit()

        # Publish message to RabbitMQ
        message = {
            "op": "update",
            "id": content.id,
            "title": content.title,
            "body": content.body,
        }
        PRODUCER.publish_message(json.dumps(message))
        return self.make_response(
            payload=CONTENT_SCHEMA.dump(content), message="Content updated successfully"
        )

    @jwt_required()
    @is_admin_or_editor
    def delete(self, content_id):
        """Method to delete a single content."""
        content = Content.query.filter(
            Content.deleted_at.is_(None), Content.id == content_id
        ).first()
        if not content:
            return self.make_response(
                message="Unable to delete content",
                error="Content not found",
                status=404,
            )
        content.deleted_at = datetime.now()
        db.session.commit()

        # Publish message to RabbitMQ
        message = {"op": "delete", "id": content.id, "title": None, "content": None}
        PRODUCER.publish_message(json.dumps(message))
        return self.make_response(message="Content deleted successfully")
