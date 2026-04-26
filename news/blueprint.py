import flask

news_blueprint = flask.Blueprint(
    "news", __name__, template_folder="../html/news", static_folder="../static"
)
