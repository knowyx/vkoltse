"""This module contains functions for handling authentication logic, it includes
functions for registering users, checking if a username or email already exists,
creating and removing authentication sessions, logging in users, getting user
information by session key, creating and checking email tokens for password reset
and email confirmation, and confirming users by email token"""

import os
import threading
from datetime import datetime, timedelta
from secrets import SystemRandom, token_urlsafe

from flask import request

from auth.email_sender import build_mail, sent_mail

BASE_DIR = "base_dir of project deploy"
MAILBOXES = {
    "reset_password": ("mailbox@mail.com", "password"),
    "confirm_account": ("mailbox@mail.com", "password"),
}


def register_user(login, email, password, db_session, user_class):
    """Function to add user in database (open connection here), set up user creditionals"""
    with db_session.create_session() as active_sess:
        user = user_class()
        user.login = login
        user.email = email
        user.set_password(password)
        user.permissions = 0
        active_sess.add(user)
        active_sess.commit()


def email_exist(email, db_session, user_class):
    """Fuction to check email existing in database (open connection here). Returns false if
    len of query list more then 0"""
    with db_session.create_session() as active_sess:
        users = active_sess.query(user_class).filter(user_class.email == email)
    if len(list(users)) > 0:
        return True
    return False


def username_exist(username, db_session, user_class):
    """Fuction to check username existing in database (open connection here). Returns false if
    len of query list more then 0"""
    with db_session.create_session() as active_sess:
        users = active_sess.query(user_class).filter(user_class.login == username)
    if len(list(users)) > 0:
        return True
    return False


def remove_auth_sessions_email(email, db_session, session_class, user_class):
    """Fuction to remove old session keys of this user (by email) in database
    (open connection here)"""
    with db_session.create_session() as active_sess:
        user = active_sess.query(user_class).filter(user_class.email == email).first()
        active_sess.query(session_class).filter(
            session_class.user_id == user.id
        ).delete()
        active_sess.commit()


def create_auth_session(email, db_session, session_class, user_class):
    """Fuction to create session for this user (by email) in database
    (open connection here)"""
    remove_auth_sessions_email(email, db_session, session_class, user_class)
    with db_session.create_session() as active_sess:
        user = active_sess.query(user_class).filter(user_class.email == email).first()
        session = session_class()
        session.user_id = user.id
        session.session_key = token_urlsafe(32)
        session.auth_date = datetime.now()
        session.user_agent = request.headers.get("User-Agent")
        active_sess.add(session)
        active_sess.commit()
        return session.session_key


def login_user(email, password, db_session, user_class):
    """Function to authentificate user (compare password from database
    with given) (open connection here)"""
    with db_session.create_session() as active_sess:
        user = active_sess.query(user_class).filter(user_class.email == email).first()
    check_pass = False
    try:
        check_pass = user.check_password(password)
    except AttributeError:
        pass
    if check_pass:
        return True
    return False


def auth_user_view(db_session, user_class, session_class):
    """Fuction to read session data from cookie, get user info or remove old session
    from db and return signal for deleting cookie. Returns signal, login button or
    dropout (if user logged in successfully) (open connection here)"""
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

    with db_session.create_session() as active_sess:
        try:
            session_data = (
                active_sess.query(session_class)
                .filter(session_class.session_key == cookie_data)
                .first()
            )
            user = (
                active_sess.query(user_class)
                .filter(user_class.id == session_data.user_id)
                .first()
            )
        except AttributeError:
            return base_button

        if datetime.now() > session_data.auth_date + timedelta(days=10):
            active_sess.query(session_class).filter(
                session_class.session_key == cookie_data
            ).delete()
            active_sess.commit()
            return "Remove_cookie"

    if request.headers.get("User-Agent") != session_data.user_agent:
        return base_button

    if user.permissions:
        admin_link = """<li><a class="dropdown-item" href="/cabinet/admin">
        Кабинет Администратора</a></li>"""
    else:
        admin_link = ""
    if not user.is_confirmed:
        confirm_link = """<li><a class="dropdown-item" href="/auth/confirm-mail">
        Подтвердить аккаунт</a></li>"""
    else:
        confirm_link = ""
    return dropout.format(
        user_login=user.login, admin_link=admin_link, confirm_link=confirm_link
    )


def have_tokens_in_interval_email(
    db_session, email, user_class, email_tokens_class, typ
):
    """Function to check existing a tokens in interval (10 mins) by email
    (open connection here)"""
    with db_session.create_session() as active_sess:
        user = active_sess.query(user_class).filter(user_class.email == email).first()
        token = (
            active_sess.query(email_tokens_class)
            .filter(
                email_tokens_class.user_id == user.id, email_tokens_class.type == typ
            )
            .first()
        )
        try:
            if token.sent_date + timedelta(minutes=10) < datetime.now():
                return False
            return True
        except AttributeError:
            return False


def get_token_data(db_session, url_key, email_tokens_class):
    """Function to get info about session tokens by url_key (from mail) (open connection here)"""
    with db_session.create_session() as active_sess:
        token = (
            active_sess.query(email_tokens_class)
            .filter(email_tokens_class.url_key == url_key)
            .first()
        )
        return token


def create_resetpass_key(reciver_email, db_session, user_class, email_tokens_class):
    """Function to create key for reset password, add it to database and sent mail with code
    (open connection here)"""
    with db_session.create_session() as active_sess:
        user = (
            active_sess.query(user_class)
            .filter(user_class.email == reciver_email and email_tokens_class.type == 0)
            .first()
        )
        active_sess.query(email_tokens_class).filter(
            email_tokens_class.user_id == user.id
        ).delete()
        email_token = email_tokens_class()
        email_token.url_key = token_urlsafe(32)
        email_token.email_key = SystemRandom().randint(100000, 999999)
        email_token.user_id = user.id
        email_token.type = 0
        email_token.sent_date = datetime.now()

        mail_content = (
            f"<p>Уважаемый пользователь, используйте код<br>{email_token.email_key}"
            + '<br>для восстановления пароля на сайте проекта "Образование в кольце"</p><br>'
        )
        subject = "Восстановление пароля"
        message = build_mail(
            MAILBOXES["reset_password"][0], subject, mail_content, reciver_email
        )
        if message is None:
            return -1
        threading.Thread(
            target=sent_mail, args=(*MAILBOXES["reset_password"], message), daemon=True
        ).start()

        active_sess.add(email_token)
        active_sess.commit()
        return email_token.url_key


def get_user_info_by_session(db_session, session_key, user_class, session_class):
    """Fuction to get user info by his session (grant what user and session exist)
    (open connection here)"""
    with db_session.create_session() as active_sess:
        session = (
            active_sess.query(session_class)
            .filter(session_class.session_key == session_key)
            .first()
        )
        user = (
            active_sess.query(user_class)
            .filter(user_class.id == session.user_id)
            .first()
        )
    return user


def create_confirm_key(user, db_session, email_tokens_class):
    """Fuction to create mail confirm key (link at email) (open connection here)"""
    with db_session.create_session() as active_sess:
        active_sess.query(email_tokens_class).filter(
            email_tokens_class.user_id == user.id and email_tokens_class.type == 1
        ).delete()
        email_token = email_tokens_class()
        email_token.url_key = token_urlsafe(32)
        email_token.user_id = user.id
        email_token.type = 1
        email_token.sent_date = datetime.now()

        mail_content = (
            "<p>Уважаемый пользователь, для подтверждения аккаунта перейтите по ссылке:"
            + f"<br>{request.host_url}auth/confirm-mail/confirm?key={email_token.url_key}<br>"
        )
        subject = "Подтверждение аккаунта"
        message = build_mail(
            MAILBOXES["confirm_account"][0], subject, mail_content, user.email
        )
        if message is None:
            return -1
        threading.Thread(
            target=sent_mail, args=(*MAILBOXES["confirm_account"], message), daemon=True
        ).start()

        active_sess.add(email_token)
        active_sess.commit()
        return 0


def check_email_code(db_session, code, url_key, email_tokens_class):
    """Fuction to validate code gived by user and code in databse (open connection here)"""
    with db_session.create_session() as active_sess:
        token = (
            active_sess.query(email_tokens_class)
            .filter(email_tokens_class.url_key == url_key)
            .first()
        )
        if token.email_key == code:
            return True
        return False


def update_password(db_session, url_key, password, email_tokens_class, user_class):
    """Fuction to set up a new password for user by url key (open connection here)"""
    with db_session.create_session() as active_sess:
        token = (
            active_sess.query(email_tokens_class)
            .filter(email_tokens_class.url_key == url_key)
            .first()
        )
        user = (
            active_sess.query(user_class).filter(user_class.id == token.user_id).first()
        )
        user.set_password(password)
        active_sess.query(email_tokens_class).filter(
            email_tokens_class.user_id == user.id
        ).delete()
        active_sess.commit()


def check_cookie_exist():
    """Fuction to validate cookie existing"""
    cookie_data = request.cookies.get("session_key (DO NOT SHARE WITH ANYONE!)")
    if cookie_data is not None:
        return True
    return False


def confirm_user(db_session, key, email_tokens_class, user_class):
    """Fuction to change user status to "Confirmed by email" after getting confirmition code"""
    with db_session.create_session() as active_sess:
        token = (
            active_sess.query(email_tokens_class)
            .filter(email_tokens_class.url_key == key)
            .first()
        )
        if token is None:
            return False
        user = (
            active_sess.query(user_class).filter(user_class.id == token.user_id).first()
        )
        user.is_confirmed = True
        active_sess.query(email_tokens_class).filter(
            email_tokens_class.url_key == key
        ).delete()
        active_sess.commit()
        return True
