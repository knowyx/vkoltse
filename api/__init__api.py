# This file initializes the API for the application, defining the endpoints and their corresponding resources.
from flask_restful import Api
from .news_api import NewsResource, NewsListResource
from .users_api import UsersResource, UserListResource
from .stories_api import StoriesResource, StoriesListResource

def init_api(app):
    api = Api(app)
    api.add_resource(UsersResource, "/api/users/<int:user_id>")
    api.add_resource(UserListResource, "/api/users")
    api.add_resource(NewsResource, '/api/news/<int:news_id>')
    api.add_resource(NewsListResource, '/api/news')
    api.add_resource(StoriesResource, "/api/stories/<int:story_id>")
    api.add_resource(StoriesListResource, '/api/stories')