"""
Resources - Register
passlib: https://passlib.readthedocs.io/en/stable/lib/passlib.hash.sha256_crypt.html
"""
# Import libs
import time
from typing import Any, Dict, List

from flask import jsonify
from flask_restful import Resource, abort, reqparse
from passlib.hash import sha256_crypt

# Parser
parser = reqparse.RequestParser()
parser.add_argument('data', type=dict, required=True)


# User Registration
class Register(Resource):
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
            Schema: {
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

    def _get_all_docs(self) -> List[Dict[str, Any]]:
        """ Get all documents in the collection """
        return [doc for doc in self.user_collection.find({})]

    def _get_current_id(self) -> int:
        """ Get the current id (max) from TODOS """
        all_docs = self._get_all_docs()
        if not all_docs:
            return 0

        cur_id = int(max(all_docs, key=lambda doc: doc['_id'])['_id']) # Get current document id
        return cur_id
