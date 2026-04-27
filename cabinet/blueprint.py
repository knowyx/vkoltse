"""This module initializes cabinet blueprint"""

import flask

cabinet_blueprint = flask.Blueprint(
    "cabinet", __name__, template_folder="../html/cabinet", static_folder="../static"
)
