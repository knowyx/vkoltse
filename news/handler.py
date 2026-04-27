"""This module contains handlers for news"""

from datetime import datetime

from flask import request


def check_admin_status(db_session, user_class, session_class):
    """This func check user for admin status (open connection here)"""
    cookie_data = request.cookies.get("session_key (DO NOT SHARE WITH ANYONE!)")
    if cookie_data is None:
        return False
    with db_session.create_session() as active_sess:
        session = (
            active_sess.query(session_class)
            .filter(session_class.session_key == cookie_data)
            .first()
        )
        if session is None:
            return False
        user = (
            active_sess.query(user_class)
            .filter(user_class.id == session.user_id)
            .first()
        )
        print(user.permissions)
        return user.permissions


def save_news(db_session, news_class, news_data, session_class):
    """This func save news to the database (open connection here)"""
    with db_session.create_session() as active_sess:
        cookie_data = request.cookies.get("session_key (DO NOT SHARE WITH ANYONE!)")
        session = (
            active_sess.query(session_class)
            .filter(session_class.session_key == cookie_data)
            .first()
        )
        content = news_data[1].strip()
        paragraphs = content.split("\n")
        news = news_class(
            user_id=session.user_id,
            title=news_data[0],
            content=paragraphs,
            cover_filename=news_data[2],
            date=datetime.now(),
        )
        active_sess.add(news)
        active_sess.commit()
