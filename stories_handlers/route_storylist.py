from flask import render_template, redirect, request
from data import db_session
from .blueprint import story_blueprint
from data.stories import Stories
from sqlalchemy.orm import joinedload
from auth.handler import auth_user_view
from data.users import Users
from data.sessions import Sessions

@story_blueprint.route("/story")
def show_stories():
    user = auth_user_view(db_session, Users, Sessions)
    if user == 'Remove_cookie':
        return redirect("/auth/logout")
    session = db_session.create_session()
    try:
        stories = session.query(Stories).options(
            joinedload(Stories.author),
            joinedload(Stories.review_authors)
        ).filter(Stories.checked == 1).all()
        return render_template(
            "stories_list.html",
            stories=stories,
            pagename="Истории",
            user=user,
            success=request.args.get('success', None)
        )   
    finally:
        session.close()