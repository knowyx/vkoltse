import flask

story_blueprint = flask.Blueprint(
    'stories_handlers',
    __name__,
    template_folder='../html/story',
    static_folder='../static'
)

from . import route_storylist
from . import route_storysubmit