import pika
from uuid import uuid4
from flask import request
from . import db
from .models import KnowledgeBase
from flask import current_app as app

def publish_message(operation, data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='crud_operations')
    message = {'operation': operation, 'data': data}

    channel.basic_publish(exchange='', routing_key='crud_operations', body=str(message))
    connection.close()

@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    id = str(uuid4())
    new_item = KnowledgeBase(id=id, title=data['title'], content=data['content'])
    db.session.add(new_item)
    db.session.commit()
    response = {
       'message': 'Item created successfully',
       'result': new_item.to_dict()
    }
    publish_message('create', {'id': id, 'title': data['title'], 'content': data['content']})
    return response

@app.route('/getall', methods=['GET'])
def getall():
    page = request.args.get('page', 1, type=int)
    per_page = 15
    pagination = KnowledgeBase.query.paginate(page=page, per_page=per_page)
    items = pagination.items
    return {
        'items': [item.to_dict() for item in items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }

@app.route('/get/<id>', methods=['GET'])
def read_one(id):
    item = KnowledgeBase.query.get(id)
    return item.to_dict()

@app.route('/update', methods=['PUT'])
def update():
    data = request.get_json()
    item = KnowledgeBase.query.get(data['id'])
    item.title = data['title']
    item.content = data['content']
    db.session.commit()
    publish_message('update', {'id': data['id'], 'title': data['title'], 'content': data['content']})
    return {
        'message': 'Item updated successfully',
        'result': item.to_dict()
    }

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    item = KnowledgeBase.query.get(id)
    result = item.to_dict()
    db.session.delete(item)
    db.session.commit()
    publish_message('delete', {'id': id})
    return {
        'result': result,
        'message': 'Item deleted successfully'
    }
