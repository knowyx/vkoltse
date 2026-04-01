from flask_restful import Resource, abort, reqparse
from flask import jsonify
from data.db_session import create_session
from data.news import News
from data import db_session

parser = reqparse.RequestParser()
parser.add_argument('', required= ,type=)

def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.get(News, news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")

class NewsResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = create_session()
        news = session.query(News).get(news_id)
        return jsonify({'news': news.to_dict()})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = create_session()
        news = session.get(News, news_id)
        session.delete(news)
        session.commit()
        return jsonify({"success": "Ok"})

class