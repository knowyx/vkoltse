"""This file initializes the API for the application, defining the endpoints and their
corresponding resources."""

from flask_restful import Api

from api.news_api import NewsListResource, NewsResource
from api.stories_api import StoriesListResource, StoriesResource
from api.users_api import UserListResource, UsersResource


def init_api(app):
    """Initialize the API and add resources for users, news, and stories"""
    api = Api(app)
    api.add_resource(UsersResource, "/api/users/<int:user_id>")
    api.add_resource(UserListResource, "/api/users")
    api.add_resource(NewsResource, "/api/news/<int:news_id>")
    api.add_resource(NewsListResource, "/api/news")
    api.add_resource(StoriesResource, "/api/stories/<int:story_id>")
    api.add_resource(StoriesListResource, "/api/stories")
