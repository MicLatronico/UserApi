import json
import boto3
from flask import Flask, request

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('users')

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = data['userId']
    name = data['name']
    table.put_item(Item={'userId': user_id, 'name': name})
    return json.dumps({'success': True}), 201

@app.route('/users/<userId>', methods=['GET'])
def get_user_by_id(userId):
    response = table.get_item(Key={'userId': userId})
    user = response.get('Item')
    if not user:
        return json.dumps({'error': 'User not found'}), 404
    return json.dumps(user), 200

