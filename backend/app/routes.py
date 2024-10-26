"""API routes for CRUD operations"""
import json
import os
from uuid import uuid4
import pika
from flask import request, jsonify
from dotenv import load_dotenv
from flask import current_app as app
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.exc import SQLAlchemyError
from . import db
from .models import KnowledgeBase

executor = ThreadPoolExecutor(max_workers=2)
load_dotenv(override=True)

def publish_message(data):
    """Function to publish messages to the RabbitMQ server"""
    try:
        credentials = pika.PlainCredentials(
            os.environ.get("RABBIT_MQ_USERNAME"), os.environ.get("RABBIT_MQ_PASSWORD")
        )
        parameters = pika.ConnectionParameters(
            os.environ.get("RABBIT_MQ_HOST"),
            os.environ.get("RABBIT_MQ_PORT"),
            os.environ.get("RABBIT_MQ_VHOST"),
            credentials,
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.basic_qos(prefetch_count=5)
        channel.queue_declare(queue=os.environ.get("RABBIT_MQ_QUEUE"))
        channel.basic_publish(exchange="", routing_key=os.environ.get("RABBIT_MQ_QUEUE"), body=jsonify({"data": data}))
    except pika.exceptions.AMQPError as e:
        app.logger.error(f"Error publishing message: {e}")
    finally:
        if connection and connection.is_open:
            connection.close()

def publish_message_async(data):
    """Function to publish messages asynchronously"""
    executor.submit(publish_message, data)

# Routes
@app.route("/create", methods=["POST"])
def create():
    """Create a new item"""
    try:
        data = request.get_json()
        id = str(uuid4())
        new_item = KnowledgeBase(id=id, title=data["title"], content=data["content"])
        db.session.add(new_item)
        db.session.commit()
        response = {
            "message": "Item created successfully",
            "result": new_item.to_dict()
        }
        # publish_message_async({"op": "create", "id": id, "title": data["title"], "content": data["content"]})
        credentials = pika.PlainCredentials(
            os.environ.get("RABBIT_MQ_USERNAME"), os.environ.get("RABBIT_MQ_PASSWORD")
        )
        parameters = pika.ConnectionParameters(
            os.environ.get("RABBIT_MQ_HOST"),
            os.environ.get("RABBIT_MQ_PORT"),
            os.environ.get("RABBIT_MQ_VHOST"),
            credentials,
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.basic_qos(prefetch_count=5)
        channel.queue_declare(queue=os.environ.get("RABBIT_MQ_QUEUE"))
        channel.basic_publish(exchange="", routing_key=os.environ.get("RABBIT_MQ_QUEUE"), body=({"data": data}))
        return jsonify(response), 201
    except (KeyError, TypeError) as e:
        app.logger.error(f"Invalid input: {e}")
        return jsonify({"error": "Invalid input"}), 400
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

@app.route("/getall", methods=["GET"])
def getall():
    """Get all items"""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = 15
        pagination = KnowledgeBase.query.paginate(page=page, per_page=per_page)
        items = pagination.items
        return jsonify({
            "items": [item.to_dict() for item in items],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page
        }), 200
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500

@app.route("/get/<id>", methods=["GET"])
def read_one(id):
    """Get a single item"""
    try:
        item = KnowledgeBase.query.get(id)
        if item is None:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(item.to_dict()), 200
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500

@app.route("/update", methods=["PUT"])
def update():
    """Update an item"""
    try:
        data = request.get_json()
        item = KnowledgeBase.query.get(data["id"])
        if item is None:
            return jsonify({"error": "Item not found"}), 404
        item.title = data["title"]
        item.content = data["content"]
        db.session.commit()
        publish_message_async({"op": "update", "id": data["id"], "title": data["title"], "content": data["content"]})
        return jsonify({
            "message": "Item updated successfully",
            "result": item.to_dict()
        }), 200
    except (KeyError, TypeError) as e:
        app.logger.error(f"Invalid input: {e}")
        return jsonify({"error": "Invalid input"}), 400
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

@app.route("/delete/<id>", methods=["DELETE"])
def delete(id):
    """Delete an item"""
    try:
        item = KnowledgeBase.query.get(id)
        if item is None:
            return jsonify({"error": "Item not found"}), 404
        result = item.to_dict()
        db.session.delete(item)
        db.session.commit()
        publish_message_async({"op": "delete", "id": id, "title": None, "content": None})
        return jsonify({
            "result": result,
            "message": "Item deleted successfully"
        }), 200
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500
