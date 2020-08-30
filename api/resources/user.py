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
