from flask import abort, redirect, render_template, request

from auth.handler import auth_user_view
from data import db_session
from data.sessions import Sessions
from data.stories import Stories
from data.users import Users

from .blueprint import cabinet_blueprint
from .hander import check_admin_status, get_stories


@cabinet_blueprint.route("/cabinet/admin", methods=["GET"])
def admin_cabinet():
    user = auth_user_view(db_session, Users, Sessions)
    if user == "Remove_cookie":
        return redirect("/auth/logout")
    if not check_admin_status(db_session, Users, Sessions):
        abort(403, "Недостаточно прав для просмотра данного контента.")
    stories = get_stories(db_session, Stories)
    return render_template(
        "admin_cabinet.html",
        pagename="Кабинет Администратора",
        user=user,
        stories=stories,
        err=request.args.get("err", None),
        id=request.args.get("id", None),
        success=request.args.get("success", None),
        news_success=request.args.get("news-success", None),
    )
