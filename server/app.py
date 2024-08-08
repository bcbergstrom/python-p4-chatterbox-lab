from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['POST', 'GET'])
def messages():
    if request.method == 'GET':
        return_arr = []
        for each in Message.query.all():
            return_arr.append({
                'id': each.id,
                'body': each.body,
                'username': each.username,
                'created_at': each.created_at,
                'updated_at': each.updated_at
            })
        return_arr.sort(key=lambda x: x['created_at'])
        return make_response(jsonify(return_arr), 200)
    elif request.method == 'POST':
        body = request.json['body']
        username = request.json['username']
        new_message = Message(body=body, username=username)
        db.session.add(new_message)
        return make_response(jsonify(new_message.to_dict()), 201)
        
@app.route('/messages/<int:id>', methods=['DELETE', 'PATCH'])
def messages_by_id(id):
    if request.method == 'DELETE':
        message = Message.query.get(id)
        db.session.delete(message)
        db.session.commit()
        return make_response('', 204)
    elif request.method == 'PATCH':
        message = Message.query.get(id)
        message.body = request.json['body']
        db.session.add(message)
        db.session.commit()
        return make_response(jsonify(message.to_dict()), 200)

if __name__ == '__main__':
    app.run(port=5555)
