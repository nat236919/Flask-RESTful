"""
RESTFUL API powered by Flask
"""
# Import libraries
from flask import Flask
from flask_restful import Api
from resources.todo import Todo
from resources.todolist import TodoList


# Initiate APP and API
app = Flask(__name__)
api = Api(app)


# Set-up Resources
api.add_resource(TodoList, '/todos')
# api.add_resource(Todo, '/todos/<string:todo_id>')


# Run app
if __name__ == '__main__':
    app.run(debug=True)
