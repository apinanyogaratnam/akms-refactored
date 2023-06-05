from sqlalchemy.ext.declarative import DeclarativeMeta
import json

from flask import Response as FlaskResponse


class AlchemyEncoder(json.JSONEncoder):

    @staticmethod
    def clean_keys(response):
        ignore_keys = {'query', 'query_class', 'registry', 'query_active_users'}
        for key in ignore_keys:
            if key in response:
                del response[key]

        return response

    def default(self, obj):
        if not isinstance(obj.__class__, DeclarativeMeta):
            response = json.JSONEncoder.default(self, obj)

            return self.clean_keys(response)

        # an SQLAlchemy class
        fields = {}
        for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
            data = obj.__getattribute__(field)
            try:
                json.dumps(data) # this will fail on non-encodable values, like other classes
                fields[field] = data
            except TypeError:
                fields[field] = None
        # a json-encodable dict
        return self.clean_keys(fields)


class Response:
    """Response object wrapper of flask Response object"""
    def __new__(cls, response_data, status_code):
        """Constructor for Response class
        Args:
            response_data (object): response data
            status_code (int): status code
        Returns:
            Response: Flask Response object
        """
        return FlaskResponse(json.dumps(response_data), status=status_code, mimetype='application/json')


def serialize(model):
    return json.loads(json.dumps(model, cls=AlchemyEncoder))
