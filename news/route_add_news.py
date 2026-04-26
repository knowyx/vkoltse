# route for adding news
import os
from secrets import token_urlsafe

from auth.handler import auth_user_view
from data import db_session
from data.news import News
from data.sessions import Sessions
from data.users import Users
from flask import abort, redirect, render_template
from werkzeug.utils import secure_filename

from .blueprint import news_blueprint
from .forms import NewsSubmitForm
from .handler import check_admin_status, save_news

BASE_DIR = "/home/knowyx/proj/py/vkoltse3/vkoltse"


@news_blueprint.route("/news/add", methods=["GET", "POST"])
def add_news():
    user = auth_user_view(db_session, Users, Sessions)
    if user == "Remove_cookie":
        return redirect("/auth/logout")
    if not check_admin_status(db_session, Users, Sessions):
        abort(403, "Недостаточно прав для просмотра данного контента.")
    form = NewsSubmitForm()
    if form.validate_on_submit():
        try:
            file = form.cover.data
            ext = file.filename.split(".")[-1]
            filename = secure_filename(token_urlsafe(32) + "." + ext)
            file.save(os.path.join(BASE_DIR, "media/user_upload", filename))
        except AttributeError:
            filename = None
        save_news(
            db_session, News, form.title.data, form.content.data, filename, Sessions
        )
        return redirect("/cabinet/admin?news-success=1")
    return render_template(
        "add_news.html", pagename="Отправка новости", user=user, form=form
    )
