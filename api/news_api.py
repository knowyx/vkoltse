from flask_restful import Resource, abort, reqparse
from flask import jsonify
from data.db_session import create_session
from data.news import News
from data import db_session
from datetime import datetime


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.get(News, news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")


def parse_date(value):
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise ValueError("Неверный формат даты, ожидается YYYY-MM-DDTHH:MM:SS")


parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)
parser.add_argument('content', required=True, type=str)
parser.add_argument('date', required=True, type=parse_date)
parser.add_argument('user_id', required=True, type=int)


class NewsResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = create_session()
        news = session.get(News, news_id)
        return jsonify({'news': news.to_dict()})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = create_session()
        news = session.get(News, news_id)
        session.delete(news)
        session.commit()
        return jsonify({"success": "Ok"})

    def put(self, news_id):
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
    def get(self):
        session = create_session()
        news = session.query(News).all()
        return jsonify({'news': [item.to_dict(only=("id", "title", "content", "date", "user")) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = create_session()
        news = News(
            title=args["title"],
            content=args["content"],
            date=args["date"],
            user_id=args["user_id"]
        )
        session.add(news)
        session.commit()
        return jsonify({'id': news.id})

