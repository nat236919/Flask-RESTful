"""
Resource - User
"""
# Import libs
import jwt
import time
import datetime
from typing import Any, Dict, List

from flask import jsonify
from flask_restful import Resource, abort, reqparse
from passlib.hash import sha256_crypt

from config import APP_CONFIG

# Setup Parser
parser = reqparse.RequestParser()
parser.add_argument('data', type=dict, required=True)


# User - Base
class UserBase():
    def __init__(self):
        self.data_schema = {
            '_id': '',
            'username': '',
            'password': '',
            'is_admin': False,
            'created_ts': ''
        }
    
    def _get_all_docs(self) -> List[Dict[str, Any]]:
        """ Get all documents in the collection """
        return [doc for doc in self.user_collection.find({})]

    def _get_current_id(self) -> int:
        """ Get the current id (max) from TODOS """
        all_docs = self._get_all_docs()
        if not all_docs:
            return 0
        # Get current document id
        cur_id = int(max(all_docs, key=lambda doc: doc['_id'])['_id'])
        return cur_id


# User - Admin
class UserAdmin(Resource, UserBase):
    def __init__(self, user_collection):
        self.user_collection = user_collection

    def get(self) -> List[Dict[str, Any]]:
        """ Get all users from the collection """
        res = self._get_all_docs()
        return jsonify(res)


# User Registration
class UserRegister(Resource, UserBase):
    def __init__(self, user_collection):
        self.user_collection = user_collection
        self.data_schema = {
            '_id': '',
            'username': '',
            'password': '',
            'is_admin': False,
            'created_ts': ''
        }
    
    def post(self) -> Dict[str, Any]:
        """ Register a user to a database
            data: {
                'username': str,
                'password': sha256_crypt.hash("password"),
                'is_admin': bool
            }
        """
        args = parser.parse_args()
        if not args:
            return abort(400, message='data was not provided')
        
        # Check existing username
        all_usernames = [data.get('username') for data in self._get_all_docs()]
        if args['data'].get('username') in all_usernames:
            return abort(409, message='username already exists') 

        # Register a new username
        cur_id = self._get_current_id()
        try:
            data_schema = self.data_schema.copy()
            data_schema['_id'] = cur_id + 1
            data_schema['username'] = args['data']['username']
            data_schema['password'] = sha256_crypt.hash(args['data']['password'])
            data_schema['is_admin'] = args['data']['is_admin']
            data_schema['created_ts'] = time.time()
            self.user_collection.insert_one(data_schema.copy())
        
        except Exception as e:
            return abort(400, message=e)

        return data_schema, 201


# User - Login
class UserLogin(Resource, UserBase):
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
