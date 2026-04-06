import flask

story_blueprint = flask.Blueprint('stories_handlers', __name__, template_folder='../html', static_folder='../static')

from . import route_storylist, route_storysubmit