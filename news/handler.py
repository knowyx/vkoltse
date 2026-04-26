from datetime import datetime

from flask import request


def check_admin_status(db_session, Users, Sessions):
    cookie_data = request.cookies.get("session_key (DO NOT SHARE WITH ANYONE!)")
    if cookie_data == None:
        return False
    with db_session.create_session() as db_session:
        session = db_session.query(Sessions).filter(Sessions.session_key == cookie_data).first()
        if session == None:
            return False
        user = db_session.query(Users).filter(Users.id == session.user_id).first()
        print(user.permissions)
        return user.permissions


def save_news(db_session, News, title, content, filename, Sessions):
    with db_session.create_session() as db_session:
        cookie_data = request.cookies.get("session_key (DO NOT SHARE WITH ANYONE!)")
        session = db_session.query(Sessions).filter(Sessions.session_key == cookie_data).first()
        content = content.strip()
        paragraphs = content.split("\n")
        news = News(
            user_id=session.user_id,
            title=title,
            content=paragraphs,
            cover_filename=filename,
            date=datetime.now(),
        )
        db_session.add(news)
        db_session.commit()
