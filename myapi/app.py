"""
RESTFUL API powered by Flask
"""
# Import libraries
import pymongo
from flask import Flask
from flask_restful import Api

from config import DATABASE_CONFIG
from resources.todo import Todo
from resources.todolist import TodoList

# Initiate APP and API
app = Flask(__name__)
api = Api(app)


# Initiate DB setup
CONNECTION_STRING = DATABASE_CONFIG['mongodb_connection_string'].replace('{username}', DATABASE_CONFIG['username'])\
                                                                .replace('{password}', DATABASE_CONFIG['password'])\
                                                                .replace('{clustername}', DATABASE_CONFIG['clustername'])\
                                                                .replace('{dbname}', DATABASE_CONFIG['dbname'])
client = pymongo.MongoClient(CONNECTION_STRING)
db = client[DATABASE_CONFIG['dbname']]


# Set-up Resources
api.add_resource(TodoList, '/todos', resource_class_kwargs={'todolist_collection': db['todolist']})
api.add_resource(Todo, '/todos/<string:todo_id>', resource_class_kwargs={'todolist_collection': db['todolist']})


# Run app
if __name__ == '__main__':
    app.run(debug=True)
