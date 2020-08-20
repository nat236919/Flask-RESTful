"""
Resources - TodoList
"""
# Import libs
import time
import pymongo
from config import DATABASE_CONFIG
from typing import List, Dict, Any
from flask import jsonify
from flask_restful import Resource, reqparse, abort

# Set MongoDB connection
CONNECTION_STRING = DATABASE_CONFIG['mongodb_connection_string'].replace('{username}', DATABASE_CONFIG['username'])\
                                                                .replace('{password}', DATABASE_CONFIG['password'])\
                                                                .replace('{clustername}', DATABASE_CONFIG['clustername'])\
                                                                .replace('{dbname}', DATABASE_CONFIG['dbname'])

# Parser
parser = reqparse.RequestParser()
parser.add_argument('task')


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def __init__(self):
        self.client = pymongo.MongoClient(CONNECTION_STRING)
        self.db = self.client[DATABASE_CONFIG['dbname']]
        self.todolist_collection = self.db['todolist']
        self.data_schema = {
            '_id': '',
            'task': '',
            'is_complete': False,
            'created_ts': ''
        }

    def get(self) -> List[Dict[str, Any]]:
        """ Get all the documents from the collection """
        res = self.todolist_collection.find({})
        return jsonify([doc for doc in res])

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
    
        all_docs = [doc for doc in self.todolist_collection.find({})]
        cur_id = max(all_docs, key=lambda doc: doc['_id'])['_id'] # Get current document id
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
        todo_id = self._get_current_id()
        todo_id = 'todo%i' % todo_id
        TODOS.pop(todo_id)
        return '', 204
    
    def _get_current_id(self) -> int:
        """ Get the current id (max) from TODOS """
        if not TODOS:
            return 0
        return int(max(TODOS.keys()).lstrip('todo'))
        