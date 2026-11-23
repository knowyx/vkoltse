"""This module contains  route for showing stories list"""

from flask import redirect, render_template, request
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from auth.handler import auth_user_view
from data import db_session
from data.sessions import Sessions
from data.stories import Stories, StoryPublication
from data.users import Users

from .blueprint import story_blueprint


@story_blueprint.route("/story")
def show_stories():
    """This function contains route for showing stories list,
    supports GET method"""
    user = auth_user_view(db_session, Users, Sessions)
    if user == "Remove_cookie":
        return redirect("/auth/logout")
    session = db_session.create_session()
    try:
        stories = (
            session.query(Stories)
            .options(joinedload(Stories.author), joinedload(Stories.review_authors))
            .filter(Stories.checked == 1)
            .outerjoin(Stories.publication)
            .order_by(func.coalesce(StoryPublication.published_at, Stories.date).desc(), Stories.id.desc())
            .all()
        )
        return render_template(
            "stories_list.html",
            stories=stories,
            pagename="Истории",
            user=user,
            success=request.args.get("success", None),
        )
    finally:
        session.close()
