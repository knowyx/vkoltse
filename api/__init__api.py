from flask_restful import Api
from .news_api import NewsResource


def init_api(app):
    api = Api(app)
    api.add_resource(NewsResource, '/api/users/<int:user_id>')