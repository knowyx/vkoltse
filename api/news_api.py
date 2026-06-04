"""This module contains api resources for working with news"""

from datetime import datetime

from flask import jsonify, request
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.db_session import create_session
from data.news import News
from config.cfg_handler import get_config_data


def abort_if_news_not_found(news_id):
    """function for checking if news exists"""
    session = db_session.create_session()
    news = session.get(News, news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")


def parse_date(
    value,
):
    """function for parsing date from string, expected format: YYYY-MM-DDTHH:MM:SS"""
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("Неверный формат даты, ожидается YYYY-MM-DDTHH:MM:SS") from exc


parser = (
    reqparse.RequestParser()
)  # parser for parsing request data for creating and updating news
parser.add_argument("title", required=True, type=str)
parser.add_argument("content", required=True, type=str)
parser.add_argument("date", required=True, type=parse_date)
parser.add_argument("user_id", required=True, type=int)


NEWS_API_VIEW_KEYS = get_config_data("api-keys")["news"]["view"]
NEWS_API_EDIT_KEYS = get_config_data("api-keys")["news"]["edit"]
NEWS_API_ENABLED = get_config_data("api-keys")["news"]["enabled"]


class NewsResource(Resource):
    """resource for working with news, supports GET, DELETE and PUT methods"""

    def get(self, news_id):
        """returns news with the specified id, represented as a dictionary with
        id, title, content, date and user information, if news with the specified
        id does not exist, returns 404 error"""
        if not NEWS_API_ENABLED:
            abort(403, message="This API is disabled right now.")

        key = request.args.get("key")
        if key is None:
            abort(403, message="Please provide an access key.")
        if key not in NEWS_API_VIEW_KEYS:
            abort(403, message="Invalid access key!")

        abort_if_news_not_found(news_id)
        session = create_session()
        news = session.get(News, news_id)
        return jsonify(
            {
                "news": news.to_dict(
                    only=("id", "title", "content", "date", "user.id", "user.login")
                )
            }
        )

    def delete(self, news_id):
        """deletes news with the specified id from the database, if news with
        the specified id does not exist, returns 404 error, otherwise returns
        success message"""
        if not NEWS_API_ENABLED:
            abort(403, message="This API is disabled right now.")

        key = request.args.get("key")
        if key is None:
            abort(403, message="Please provide an access key.")
        if key not in NEWS_API_EDIT_KEYS:
            abort(403, message="Invalid access key!")

        abort_if_news_not_found(news_id)
        session = create_session()
        news = session.get(News, news_id)
        session.delete(news)
        session.commit()
        return jsonify({"success": "Ok"})

    def put(self, news_id):
        """ "updates news with the specified id in the database, expects title,
        content, date and user_id in the request data, if news with the specified
        id does not exist, returns 404 error, otherwise returns success message"""
        if not NEWS_API_ENABLED:
            abort(403, message="This API is disabled right now.")

        key = request.args.get("key")
        if key is None:
            abort(403, message="Please provide an access key.")
        if key not in NEWS_API_EDIT_KEYS:
            abort(403, message="Invalid access key!")

        abort_if_news_not_found(news_id)
        session = create_session()
        news = session.get(News, news_id)

        args = parser.parse_args()
        news.title = args["title"]
        news.content = args["content"]
        news.date = args["date"]
        news.user_id = args["user_id"]

        session.commit()

        return jsonify({"success": "Ok"})


class NewsListResource(Resource):
    """resource for working with news list, supports GET and POST methods"""

    def get(self):
        """returns a list of all news in the database, each news is represented
        as a dictionary with id, title, content, date and user information"""
        if not NEWS_API_ENABLED:
            abort(403, message="This API is disabled right now.")

        key = request.args.get("key")
        if key is None:
            abort(403, message="Please provide an access key.")
        if key not in NEWS_API_VIEW_KEYS:
            abort(403, message="Invalid access key!")

        session = create_session()
        news = session.query(News).all()
        return jsonify(
            {
                "news": [
                    item.to_dict(
                        only=("id", "title", "content", "date", "user.id", "user.login")
                    )
                    for item in news
                ]
            }
        )

    def post(self):
        """creates a new news in the database, expects title, content, date
        and user_id in the request data, returns the id of the created news"""
        if not NEWS_API_ENABLED:
            abort(403, message="This API is disabled right now.")

        key = request.args.get("key")
        if key is None:
            abort(403, message="Please provide an access key.")
        if key not in NEWS_API_EDIT_KEYS:
            abort(403, message="Invalid access key!")

        args = parser.parse_args()
        session = create_session()
        news = News(
            title=args["title"],
            content=args["content"],
            date=args["date"],
            user_id=args["user_id"],
        )
        session.add(news)
        session.commit()
        return jsonify({"id": news.id})
