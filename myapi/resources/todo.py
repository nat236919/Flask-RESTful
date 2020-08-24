"""
Resources - Todo
"""
# Import libs
import json
import time
from typing import Any, Dict, List

from flask import jsonify
from flask_restful import Resource, abort, reqparse

# Parser
parser = reqparse.RequestParser()
parser.add_argument('data', type=dict)


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def __init__(self, todolist_collection):
        self.todolist_collection = todolist_collection
        self.data_schema = {
            'task': '',
            'is_complete': False,
            'created_ts': ''
        }

    def get(self, todo_id: str) -> Dict[str, Any]:
        """ Get a single doc from its id """
        todo_id = self._transform_str_num_to_int(todo_id)
        res = self.todolist_collection.find_one({'_id': todo_id})
        if not res:
            return abort(404, message='not found')

        return res, 200

    def put(self, todo_id: str) -> Dict[str, Any]:
        """ Modify a single from its id
        scheme:
            'data': {
                'task': 'example',
                'is_complete': False,
            }
        """
        todo_id = self._transform_str_num_to_int(todo_id)
        res = self.get(todo_id)
        if not res:
            return abort(404, message='not found')

        args = parser.parse_args()
        if not args:
            return abort(400, message='data was not provided')

        # Modify the document
        data_schema = self.data_schema.copy()
        data_schema['task'] = args['data']['task']
        data_schema['is_complete'] = args['data']['is_complete']
        data_schema['created_ts'] = time.time()
        self.todolist_collection.update({'_id': todo_id}, data_schema.copy())

        return data_schema, 201

    def delete(self, todo_id: str) -> Dict[str, Any]:
        """ Delete a single document from its id """
        todo_id = self._transform_str_num_to_int(todo_id)
        res = self.get(todo_id)
        if not res:
            return abort(404, message='not found')

        # Remove a document
        try:
            self.todolist_collection.remove({'_id': todo_id})

        except Exception as e:
            return abort(400, message=e)

        return '', 204

    def _transform_str_num_to_int(self, arg: str) -> int:
        """ Transform a string to an integer """
        if isinstance(arg, int):
            return arg

        return int(arg) if arg.isdigit() else ''
