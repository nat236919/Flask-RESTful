"""
Resources - Login
passlib: https://passlib.readthedocs.io/en/stable/lib/passlib.hash.sha256_crypt.html
"""
# Import libs
import datetime
from typing import Any, Dict, List

import jwt
from flask import jsonify
from flask_restful import Resource, abort, reqparse
from passlib.hash import sha256_crypt

from config import APP_CONFIG

# Parser
parser = reqparse.RequestParser()
parser.add_argument('data', type=dict, required=True)


# Login
class Login(Resource):
    def __init__(self, user_collection):
        self.user_collection = user_collection
        self.payload = {
            'user_id': '',
            'username': '',
            'is_admin': '',
            'exp': ''
        }
        self.data_schema = {
            'result': 'failed',
            'data': ''
        }
    
    def post(self) -> str:
        """ Login with a username and password
            data: {
                'username': str,
                'password': str
            }
        """
        args = parser.parse_args()
        if not args:
            return abort(400, message='data was not provided')
        
        # Check username
        username = args['data'].get('username')
        password = args['data'].get('password')
        existing_user = [doc for doc in self.user_collection.find({'username': username})]
        if not existing_user:
            return abort(401, message='username or password is incorrect')
        
        # Validate password
        existing_user = existing_user[0]
        existing_user_password = existing_user.get('password', '')
        if not sha256_crypt.verify(password, existing_user_password):
            return abort(401, message='username or password is incorrect')
        
        # Generate JWT
        payload = self.payload.copy()
        payload['user_id'] = existing_user.get('_id')
        payload['username'] = existing_user.get('username')
        payload['is_admin'] = existing_user.get('is_admin')
        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=180)
        encoded = jwt.encode(payload, APP_CONFIG['secret_key'], algorithm='HS256')

        # Wrap response data
        data_schema = self.data_schema.copy()
        data_schema['result'] = 'success'
        data_schema['data'] = encoded.decode('utf-8')

        return data_schema
