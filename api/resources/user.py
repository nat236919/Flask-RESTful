"""
Resources - User
"""
# Import libs
import time
from typing import Any, Dict, List

from flask import jsonify
from flask_restful import Resource, abort, reqparse

# Parser
parser = reqparse.RequestParser()
parser.add_argument('data', type=dict, required=True)


# User (admin)
class User(Resource):
    def __init__(self, user_collection):
        self.user_collection = user_collection
        self.data_schema = {
            '_id': '',
            'username': '',
            'password': '',
            'is_admin': False,
            'created_ts': ''
        }

    def get(self) -> List[Dict[str, Any]]:
        """ Get all users from the collection """
        res = self._get_all_docs()
        return jsonify(res)
    
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
