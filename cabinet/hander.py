from flask import request
from sqlalchemy.orm import joinedload


def check_admin_status(db_session, Users, Sessions):
    cookie_data = request.cookies.get("session_key (DO NOT SHARE WITH ANYONE!)")
    if cookie_data == None:
        return False
    with db_session.create_session() as db_session:
        session = db_session.query(Sessions).filter(Sessions.session_key == cookie_data).first()
        if session == None:
            return False
        user = db_session.query(Users).filter(Users.id == session.user_id).first()
        print(user.permissions)
        return user.permissions


def get_stories(db_session, Stories):
    with db_session.create_session() as db_session:
        stories = db_session.query(Stories).options(
            joinedload(Stories.author),
            joinedload(Stories.review_authors)
        ).filter(Stories.checked == 0).all()
    return stories


def confirm_story(db_session, id, Stories, Sessions):
    with db_session.create_session() as db_session:
        story = db_session.query(Stories).filter(Stories.id == id, Stories.checked == 0).first()
        if story == None:
            return False
        cookie_data = request.cookies.get("session_key (DO NOT SHARE WITH ANYONE!)")
        if cookie_data == None:
            return False
        session = db_session.query(Sessions).filter(Sessions.session_key == cookie_data).first()
        if session == None:
            return False
        story.checked = 1
        story.review_authors_id = session.user_id
        db_session.commit()
    return True


def remove_story(db_session, id, Stories):
    with db_session.create_session() as db_session:
        story = db_session.query(Stories).filter(Stories.id == id, Stories.checked == 0).first()
        if story == None:
            return False
        db_session.query(Stories).filter(Stories.id == id, Stories.checked == 0).delete()
        db_session.commit()
    return True

