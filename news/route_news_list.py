from .blueprint import news_blueprint
from flask import render_template, redirect
from auth.handler import auth_user_view
from data import db_session as db_sess
from data.users import Users
from data.sessions import Sessions
from data.news import News

@news_blueprint.route("/news")
def news_list():
    user = auth_user_view(db_sess, Users, Sessions)
    if user == 'Remove_cookie':
        return redirect("/auth/logout")
    try:
        db_session = db_sess.create_session()
        news = db_session.query(News).all()
        return render_template("news_list.html", user=user, pagename="Новости", news=news)
    finally:
        db_session.close()