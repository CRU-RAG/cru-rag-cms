"""API routes for CRUD operations"""
from datetime import datetime
import jwt
import redis
import json
import os
from uuid import uuid4
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager, get_jwt_identity
from flask_limiter import Limiter
import pika
from flask import request, jsonify
from dotenv import load_dotenv
from flask import current_app as app
from flask_limiter.util import get_remote_address
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.exc import SQLAlchemyError
from . import db
from .models.content import Content
from .models.user import User

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
        channel.basic_publish(exchange="", routing_key=os.environ.get("RABBIT_MQ_QUEUE"), body=(json.dumps({"data": data})))
    except pika.exceptions.AMQPError as e:
        app.logger.error(f"Error publishing message: {e}")
    finally:
        if connection and connection.is_open:
            connection.close()

def publish_message_async(data):
    """Function to publish messages asynchronously"""
    executor.submit(publish_message, data)

limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

@app.route('/register', methods=['POST'])
@limiter.limit(limit_value="5 per minute")  # Limit registration attempts
def register():
    """Register a new user"""
    username = request.json.get('username')
    password = request.json.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 400

    # Create new user and add to the database
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

# User login
@app.route('/login', methods=['POST'])
@limiter.limit(limit_value="10 per minute")  # Limit login attempts
def login():
    """Login an authenticated user"""
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Create access token
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token, "msg": "Logged In Successfully"}), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401

# Routes
@app.route("/create", methods=["POST"])
@jwt_required()
def create():
    """Create a new item"""
    try:
        data = request.get_json()
        id = str(uuid4())
        new_item = Content(id=id, title=data["title"], content=data["content"])
        db.session.add(new_item)
        db.session.commit()
        response = {
            "message": "Item created successfully",
            "result": new_item.to_dict()
        }
        publish_message_async({"op": "create", "id": id, "title": data["title"], "content": data["content"]})
        return jsonify(response), 201
    except (KeyError, TypeError) as e:
        app.logger.error(f"Invalid input: {e}")
        return jsonify({"error": "Invalid input"}), 400
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

@app.route("/getall", methods=["GET"])
@jwt_required()
def getall():
    """Get all items"""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = 15
        pagination = Content.query.filter(Content.deleted_at.is_(None)).paginate(page=page, per_page=per_page)
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
@jwt_required()
def read_one(id):
    """Get a single item"""
    try:
        item = Content.query.filter(Content.deleted_at.is_(None), Content.id == id).first()
        if item is None:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(item.to_dict()), 200
    except SQLAlchemyError as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500

@app.route("/update", methods=["PUT"])
@jwt_required()
def update():
    """Update an item"""
    try:
        data = request.get_json()
        item = Content.query.get(data["id"])
        if item is None:
            return jsonify({"error": "Item not found"}), 404
        item.title = data["title"]
        item.content = data["content"]
        item.updated_at = datetime.now()
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
@jwt_required()
def delete(id):
    """Soft delete an item by setting the deleted_at timestamp"""
    try:
        item = Content.query.get(id)
        if item is None or item.deleted_at is not None:
            return jsonify({"error": "Item not found"}), 404
        item.deleted_at = datetime.now()
        result = item.to_dict()
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
