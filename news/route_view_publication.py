"""This module contains route for viewing news publication"""

from flask import redirect, render_template

from auth.handler import auth_user_view
from data import db_session as db_sess
from data.news import News
from data.sessions import Sessions
from data.users import Users

from .blueprint import news_blueprint


@news_blueprint.route("/news/<news_num>")
def view_publication(news_num):
    """This function get all publications and render it"""
    user = auth_user_view(db_sess, Users, Sessions)
    if user == "Remove_cookie":
        return redirect("/auth/logout")
    try:
        db_session = db_sess.create_session()
        news = db_session.query(News).filter(News.id == news_num).first()
        if news:
            return render_template(
                "publication.html", news=news, pagename=news.title, user=user
            )
        return redirect("/news")
    finally:
        db_session.close()
