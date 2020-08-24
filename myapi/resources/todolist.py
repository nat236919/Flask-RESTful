"""
Resources - TodoList
"""
# Import libs
import time
from typing import Any, Dict, List

from flask import jsonify
from flask_restful import Resource, abort, reqparse

# Parser
parser = reqparse.RequestParser()
parser.add_argument('task')


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def __init__(self, todolist_collection):
        self.todolist_collection = todolist_collection
        self.data_schema = {
            '_id': '',
            'task': '',
            'is_complete': False,
            'created_ts': ''
        }

    def get(self) -> List[Dict[str, Any]]:
        """ Get all the documents from the collection """
        res = self._get_all_docs()
        return jsonify(res)

    def post(self) -> Dict[str, Any]:
        """ Add a document onto the collection
            Schema:
                {
                    "task": "example task"
                }
        """
        args = parser.parse_args()
        if not args:
            return abort(400, message='data was not provided')

        cur_id = self._get_current_id()
        try:
            data_schema = self.data_schema.copy()
            data_schema['_id'] = cur_id + 1
            data_schema['task'] = args['task']
            data_schema['created_ts'] = time.time()
            self.todolist_collection.insert_one(data_schema.copy())

        except Exception as e:
            return abort(400, message=e)

        return data_schema, 201

    def delete(self) -> None:
        """ Pop out the latest data """
        cur_id = self._get_current_id()
        if not cur_id:
            return abort(400, message='no documents found')

        try:
            self.todolist_collection.delete_one({'_id': cur_id})

        except Exception as e:
            return abort(400, message=e)

        return '', 204

    def _get_all_docs(self) -> List[Dict[str, Any]]:
        """ Get all documents in the collection """
        return [doc for doc in self.todolist_collection.find({})]

    def _get_current_id(self) -> int:
        """ Get the current id (max) from TODOS """
        all_docs = self._get_all_docs()
        if not all_docs:
            return 0

        # Get current document id
        cur_id = int(max(all_docs, key=lambda doc: doc['_id'])['_id'])

        return cur_id
