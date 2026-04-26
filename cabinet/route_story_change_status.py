from auth.handler import auth_user_view
from data import db_session
from data.sessions import Sessions
from data.stories import Stories
from data.users import Users
from flask import abort, redirect, request

from .blueprint import cabinet_blueprint
from .hander import check_admin_status, confirm_story, remove_story


@cabinet_blueprint.route("/cabinet/admin/story-change-status", methods=["GET"])
def story_confirm():
    user = auth_user_view(db_session, Users, Sessions)
    if user == "Remove_cookie":
        return redirect("/auth/logout")
    if not check_admin_status(db_session, Users, Sessions):
        abort(403, "Недостаточно прав для просмотра данного контента.")
    story_id = request.args.get("id", None)
    try:
        story_id = int(story_id)
    except ValueError:
        return redirect(f"/cabinet/admin?err=invalid-id-type&id={story_id}")
    if story_id < 0:
        return redirect(f"/cabinet/admin?err=invalid-id-type&id={story_id}")
    typ = request.args.get("type", None)
    if typ == "1":
        status = confirm_story(db_session, story_id, Stories, Sessions)
    elif typ == "-1":
        status = remove_story(db_session, story_id, Stories)
    else:
        return redirect(f"/cabinet/admin?err=nothing")
    print(status)
    if status:
        return redirect(f"/cabinet/admin?success={typ}&id={story_id}")
    else:
        return redirect(f"/cabinet/admin?err=invalid-id&id={story_id}")
