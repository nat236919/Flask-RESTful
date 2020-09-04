"""
RESTFUL API powered by Flask
"""
# Import libraries
import pymongo
from flask import Flask
from flask_restful import Api

from config import APP_CONFIG, DATABASE_CONFIG
from resources.todo import Todo
from resources.todolist import TodoList
from resources.user import User
from resources.register import Register
from resources.login import Login

# Initiate APP and API
app = Flask(__name__)
app.config['SECRET_KEY'] = APP_CONFIG['secret_key']
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

api.add_resource(User, '/users', resource_class_kwargs={'user_collection': db['users']})
api.add_resource(Register, '/users/register', resource_class_kwargs={'user_collection': db['users']})
api.add_resource(Login, '/users/login', resource_class_kwargs={'user_collection': db['users']})


# Run app
if __name__ == '__main__':
    app.run(debug=True)
