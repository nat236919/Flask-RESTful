"""
Common - Util
"""
# import libs
import jwt
from functools import wraps
from typing import Any, Dict, List

from flask import request
from flask_restful import abort

from config import APP_CONFIG


class JWTAuthentication:
    """
    This is a class containing all methods to validate JWT
    1. check admin
    2. check user
    """

    def _get_JWT_from_header(self) -> Dict[str, Any]:
        """ Get JWT from Header
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6ImFkbWluIiwiaXNfYWRtaW4iOnRydWUsImV4cCI6MTYwMTAyMDc5Mn0.0RAeH0kqHC5kqqEAFF08cgFdTyRQnZQ0nTaJMvevOZ0'
        """
        res_data = {'result': '', 'data': {}}
        try:
            if 'Authorization' not in request.headers:
                raise Exception('Authorization not found')

            auth_header = request.headers['Authorization'].split(' ')
            if not len(auth_header) > 1:
                raise Exception('Authorization not found')

            encoded = auth_header[-1]
            decoded = jwt.decode(
                encoded, APP_CONFIG['secret_key'], algorithms='HS256')
            res_data['result'] = 'success'
            res_data['data'] = decoded

        except Exception as e:
            res_data['result'] = e

        finally:
            return res_data

    def is_JWT_valid(self) -> bool:
        res_data = self._get_jwt_from_header()
        if res_data['result'] in ['success']:
            return True
        return False

    def is_admin(self) -> bool:
        """ Check admin status from valid JWT """
        res_data = self._get_JWT_from_header()
        if res_data['result'] in ['success'] and res_data['data'].get('is_admin'):
            return True
        return False
