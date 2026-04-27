# pylint: disable=R0801
# route for news list
from flask import redirect, render_template

from auth.handler import auth_user_view
from data import db_session as db_sess
from data.news import News
from data.sessions import Sessions
from data.users import Users

from .blueprint import news_blueprint


@news_blueprint.route("/news")
def news_list():
    user = auth_user_view(db_sess, Users, Sessions)
    if user == "Remove_cookie":
        return redirect("/auth/logout")
    try:
        db_session = db_sess.create_session()
        news = db_session.query(News).all()
        return render_template(
            "news_list.html", user=user, pagename="Новости", news=news
        )
    finally:
        db_session.close()
