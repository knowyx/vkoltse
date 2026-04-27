"""This module contains a function, what change status of story (accept/decline).
This route don't have a gui. This route is only accessible only from admin cabinet"""

from flask import abort, redirect, request

from auth.handler import auth_user_view
from data import db_session
from data.sessions import Sessions
from data.stories import Stories
from data.users import Users

from .blueprint import cabinet_blueprint
from .hander import check_admin_status, confirm_story, decline_story


@cabinet_blueprint.route("/cabinet/admin/story-change-status", methods=["GET"])
def story_change_status():
    """This function change status of story (accept/decline)"""
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
        status = decline_story(db_session, story_id, Stories)
    else:
        return redirect("/cabinet/admin?err=nothing")
    print(status)
    if status:
        return redirect(f"/cabinet/admin?success={typ}&id={story_id}")
    return redirect(f"/cabinet/admin?err=invalid-id&id={story_id}")
