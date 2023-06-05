from flask_migrate import Migrate
from flask import request

from app import create_app, db

from app.models.user import Users
from app.models.api_key import ApiKeys

from functools import wraps

def authenticate(auth_type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if auth_type == 'internal':
                api_key = request.headers.get('X-API-KEY')
                if api_key == os.environ.get('API_KEY'):
                    return func(*args, **kwargs)
                    # api_key = ApiKeys.query.filter_by(api_key=api_key).first()
                    # if api_key:
                    #     return func(*args, **kwargs)
                return {
                    'status': 401,
                    'message': 'Unauthorized',
                }, 401
            else:
                return {
                    'status': 401,
                    'message': 'Unauthorized',
                }, 401
        return wrapper
    return decorator

import os

from app.utils import serialize

app = create_app()
migrate = Migrate(app, db)

@app.route('/')
def index():
    return {
        'pid': os.getpid(),
        'status': 200,
    }

@app.route('/users')
@authenticate('internal')
def users():
    return {
        'users': serialize(Users.query_active_users().all()),
        'status': 200,
    }
