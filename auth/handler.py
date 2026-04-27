# This module contains functions for handling authentication logic, it includes functions for registering users, checking if a username or email already exists, creating and removing authentication sessions, logging in users, getting user information by session key, creating and checking email tokens for password reset and email confirmation, and confirming users by email token
import os
from datetime import datetime, timedelta
from secrets import SystemRandom, token_urlsafe

from flask import request

from auth.email_sender import sent_confirm_mail, sent_resetpass_mail

BASE_DIR = "/home/knowyx/proj/py/vkoltse3/vkoltse"


def register_user(login, email, password, db_session, User):
    with db_session.create_session() as db_session:
        user = User()
        user.login = login
        user.email = email
        user.set_password(password)
        user.permissions = 0
        db_session.add(user)
        db_session.commit()


def email_exist(email, db_session, User):
    with db_session.create_session() as db_session:
        users = db_session.query(User).filter(User.email == email)
    if len(list(users)) > 0:
        return True
    return False


def username_exist(username, db_session, User):
    with db_session.create_session() as db_session:
        users = db_session.query(User).filter(User.login == username)
    if len(list(users)) > 0:
        return True
    return False


def remove_auth_sessions_email(email, db_session, Sessions, User):
    with db_session.create_session() as db_session:
        user = db_session.query(User).filter(User.email == email).first()
        db_session.query(Sessions).filter(Sessions.user_id == user.id).delete()
        db_session.commit()


def create_auth_session(email, db_session, Sessions, User):
    remove_auth_sessions_email(email, db_session, Sessions, User)
    with db_session.create_session() as db_session:
        user = db_session.query(User).filter(User.email == email).first()
        session = Sessions()
        session.user_id = user.id
        session.session_key = token_urlsafe(32)
        session.auth_date = datetime.now()
        session.user_agent = request.headers.get("User-Agent")
        db_session.add(session)
        db_session.commit()
        return session.session_key


def login_user(email, password, db_session, User):
    with db_session.create_session() as db_session:
        user = db_session.query(User).filter(User.email == email).first()
    check_pass = False
    try:
        check_pass = user.check_password(password)
    except AttributeError:
        pass
    if check_pass:
        return True
    return False


def auth_user_view(db_session, User, Sessions):
    cookie_data = request.cookies.get("session_key (DO NOT SHARE WITH ANYONE!)")
    try:
        with open(
            os.path.join(BASE_DIR, "html/auth/base_button.html"),
            mode="rt",
            encoding="UTF-8",
        ) as file:
            base_button = file.read()

        with open(
            os.path.join(BASE_DIR, "html/auth/dropout-authed.html"),
            mode="rt",
            encoding="UTF-8",
        ) as file:
            dropout = file.read()
    except FileNotFoundError:
        return "Files not found! Please, contact with admin."

    if cookie_data is None:
        return base_button

    with db_session.create_session() as db_session:
        try:
            session_data = (
                db_session.query(Sessions)
                .filter(Sessions.session_key == cookie_data)
                .first()
            )
            user = (
                db_session.query(User).filter(User.id == session_data.user_id).first()
            )
        except AttributeError:
            return base_button

        if datetime.now() > session_data.auth_date + timedelta(days=10):
            db_session.query(Sessions).filter(
                Sessions.session_key == cookie_data
            ).delete()
            db_session.commit()
            return "Remove_cookie"

    if request.headers.get("User-Agent") != session_data.user_agent:
        return base_button

    if user.permissions:
        admin_link = """<li><a class="dropdown-item" href="/cabinet/admin">Кабинет Администратора</a></li>"""
    else:
        admin_link = ""
    if not user.is_confirmed:
        confirm_link = """<li><a class="dropdown-item" href="/auth/confirm-mail">Подтвердить аккаунт</a></li>"""
    else:
        confirm_link = ""
    return dropout.format(
        user_login=user.login, admin_link=admin_link, confirm_link=confirm_link
    )


def have_tokens_in_interval_email(db_session, email, User, Tokens, typ):
    with db_session.create_session() as db_session:
        user = (
            db_session.query(User)
            .filter(User.email == email and Tokens.type == typ)
            .first()
        )
        token = db_session.query(Tokens).filter(Tokens.user_id == user.id).first()
        try:
            if token.sent_date + timedelta(minutes=10) < datetime.now():
                return False
            else:
                return True
        except AttributeError:
            return False


def get_token_data(db_session, url_key, User, Tokens):
    with db_session.create_session() as db_session:
        token = db_session.query(Tokens).filter(Tokens.url_key == url_key).first()
        return token


def create_resetpass_key(email, db_session, User, Tokens):
    with db_session.create_session() as db_session:
        user = (
            db_session.query(User)
            .filter(User.email == email and Tokens.type == 0)
            .first()
        )
        db_session.query(Tokens).filter(Tokens.user_id == user.id).delete()
        email_token = Tokens()
        email_token.url_key = token_urlsafe(32)
        email_token.email_key = SystemRandom().randint(100000, 999999)
        email_token.user_id = user.id
        email_token.type = 0
        email_token.sent_date = datetime.now()
        db_session.add(email_token)
        db_session.commit()
        sent_resetpass_mail(email, email_token.email_key)
        return email_token.url_key


def get_user_info_by_session(db_session, session_key, Users, Sessions):
    with db_session.create_session() as db_session:
        session = (
            db_session.query(Sessions)
            .filter(Sessions.session_key == session_key)
            .first()
        )
        user = db_session.query(Users).filter(Users.id == session.user_id).first()
    return user


def create_confirm_key(user, db_session, Tokens):
    with db_session.create_session() as db_session:
        db_session.query(Tokens).filter(
            Tokens.user_id == user.id and Tokens.type == 1
        ).delete()
        email_token = Tokens()
        email_token.url_key = token_urlsafe(32)
        email_token.user_id = user.id
        email_token.type = 1
        email_token.sent_date = datetime.now()
        db_session.add(email_token)
        db_session.commit()
        sent_confirm_mail(user.email, email_token.url_key, request.host_url)


def check_email_code(db_session, code, url_key, Tokens):
    with db_session.create_session() as db_session:
        token = db_session.query(Tokens).filter(Tokens.url_key == url_key).first()
        if token.email_key == code:
            return True
        return False


def update_password(db_session, url_key, password, Tokens, User):
    with db_session.create_session() as db_session:
        token = db_session.query(Tokens).filter(Tokens.url_key == url_key).first()
        user = db_session.query(User).filter(User.id == token.user_id).first()
        user.set_password(password)
        db_session.query(Tokens).filter(Tokens.user_id == user.id).delete()
        db_session.commit()


def check_cookie_exist():
    cookie_data = request.cookies.get("session_key (DO NOT SHARE WITH ANYONE!)")
    if cookie_data != None:
        return True
    return False


def confirm_user(db_session, key, EmailTokens, Users):
    with db_session.create_session() as db_session:
        token = db_session.query(EmailTokens).filter(EmailTokens.url_key == key).first()
        if token is None:
            return False
        user = db_session.query(Users).filter(Users.id == token.user_id).first()
        user.is_confirmed = True
        db_session.query(EmailTokens).filter(EmailTokens.url_key == key).delete()
        db_session.commit()
        return True
