"""This module contains functions needed to work for the logic of cabinet blueprint.
Confirm/decline (remove) story, check if user have admin rights and get all unchecked
stories to display"""

from flask import request
from sqlalchemy.orm import joinedload


def check_admin_status(db_session, user_class, session_class):
    """This function check if user have admin rights by getting a session key and
    request to the database (open connection here)"""
    cookie_data = request.cookies.get("session_key (DO NOT SHARE WITH ANYONE!)")
    if cookie_data is None:
        return False
    with db_session.create_session() as active_sess:
        session = (
            active_sess.query(session_class)
            .filter(session_class.session_key == cookie_data)
            .first()
        )
        if session is None:
            return False
        user = (
            active_sess.query(user_class)
            .filter(user_class.id == session.user_id)
            .first()
        )
        print(user.permissions)
        return user.permissions


def get_unchecked_stories(db_session, story_class):
    """This function get all unchecked stories to display in admin cabinet
    (open connection here)"""
    with db_session.create_session() as active_sess:
        stories = (
            active_sess.query(story_class)
            .options(
                joinedload(story_class.author),
                joinedload(story_class.review_authors),
            )
            .filter(story_class.checked == 0)
            .all()
        )
    return stories


def confirm_story(db_session, story_id, story_class, session_class):
    """This function need to confirm story (then, it will display to others)
    (open connection here)"""
    with db_session.create_session() as active_sess:
        story = (
            active_sess.query(story_class)
            .filter(story_class.id == story_id, story_class.checked == 0)
            .first()
        )
        if story is None:
            return False
        cookie_data = request.cookies.get("session_key (DO NOT SHARE WITH ANYONE!)")
        if cookie_data is None:
            return False
        session = (
            active_sess.query(session_class)
            .filter(session_class.session_key == cookie_data)
            .first()
        )
        if session is None:
            return False
        story.checked = 1
        story.review_authors_id = session.user_id
        active_sess.commit()
    return True


def decline_story(db_session, story_id, story_class):
    """This function need to decline story (then, they it will be removed)
    (open connection here)"""
    with db_session.create_session() as active_sess:
        story = (
            active_sess.query(story_class)
            .filter(story_class.id == story_id, story_class.checked == 0)
            .first()
        )
        if story is None:
            return False
        active_sess.query(story_class).filter(
            story_class.id == story_id, story_class.checked == 0
        ).delete()
        active_sess.commit()
    return True
