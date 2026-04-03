from datetime import datetime
from flask import request
from data.sessions import Sessions


def register_user(login, email, password, session, User):
    user = User()
    user.login = login
    user.email = email
    user.set_password(password)
    user.permissions = '0'
    session = session.create_session()
    session.add(user)
    session.commit()


def email_exist(email, session, User):
    session = session.create_session()
    users = session.query(User).filter(User.email == email)
    if len(list(users)) > 0:
        return True
    else:
        return False


def username_exist(username, session, User):
    session = session.create_session()
    users = session.query(User).filter(User.login == username)
    if len(list(users)) > 0:
        return True
    else:
        return False


def create_auth_session(email, db_session, Sessions, User):
    db_session = db_session.create_session()
    user = session.query(User).filter(User.email == email).first()
    session = Sessions()
    session.user_id = user.id
    session.auth_date = datetime.now().timestamp()
    session.user_agent = request.headers.get('User-Agent')
    db_session.add(session)
    db_session.coommit()



def login_user(email, password, session, User):
    session = session.create_session()
    user = session.query(User).filter(User.email == email).first()
    if user.check_password(password):
        return True
    else:
        return False
