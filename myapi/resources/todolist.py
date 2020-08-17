"""
Resources - TodoList
"""
# Import libs
from typing import List, Dict, Any
from flask_restful import Resource, reqparse

# Set-up constant variables
TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


# Parser
parser = reqparse.RequestParser()
parser.add_argument('task')


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self) -> Dict[str, Dict[str, Any]]:
        return TODOS

    def post(self) -> Dict[str, Any]:
        args = parser.parse_args()
        todo_id = self._get_current_id() + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201
    
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
        