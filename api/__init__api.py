from flask_restful import Api
from .news_api import NewsResource, NewsListResource


def init_api(app):
    api = Api(app)
    api.add_resource(NewsResource, '/api/news/<int:news_id>')
    api.add_resource(NewsListResource, '/api/news')