"""This module contains route for submitting stories"""

from datetime import datetime

from flask import abort, redirect, render_template, request

from auth.handler import auth_user_view
from data import db_session
from data.sessions import Sessions
from data.stories import Stories
from data.users import Users

from .blueprint import story_blueprint
from .forms import StorySubmitForm


@story_blueprint.route("/story/submit", methods=["GET", "POST"])
def story_submit():
    """This func contains route for submitting stories, supports GET and POST methods"""
    if not check_cookie_exist():  # if session cookie does not exist, return 403 error
        return abort(403, "Для совершения этого действия необходимо авторизоваться.")
    user = auth_user_view(db_session, Users, Sessions)
    if user == "Remove_cookie":
        return redirect("/auth/logout")

    form = StorySubmitForm()
    print(form.errors)
    if form.validate_on_submit():
        # if form is submitted and valid, create new story and add it to database,
        # then redirect to stories list with success message
        connection_db = db_session.create_session()
        try:
            story = Stories(
                title=form.title.data,
                content=form.content.data,
                author_id=get_user_id(db_session),
                date=datetime.now(),
            )
            connection_db.add(story)
            connection_db.commit()
        finally:
            connection_db.close()

        return redirect("/story?success=1")

    return render_template("story_submit.html", form=form, user=user)


def check_cookie_exist():
    """This function used for checking if session cookie exists, returns True if exists,
    False otherwise"""
    session_key = request.cookies.get("session_key (DO NOT SHARE WITH ANYONE!)")
    return bool(session_key)


def get_user_id(
    db_sess,
):
    """This function for getting user id from session cookie, returns user id if session exists,
    None otherwise"""
    session_key = request.cookies.get("session_key (DO NOT SHARE WITH ANYONE!)")
    with db_sess.create_session() as active_sess:
        session = (
            active_sess.query(Sessions)
            .filter(Sessions.session_key == session_key)
            .first()
        )
    return session.user_id
