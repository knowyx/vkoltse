from datetime import datetime, timedelta
from flask import request
from secrets import token_urlsafe


def register_user(login, email, password, db_session, User):
    with db_session.create_session() as db_session:
        user = User()
        user.login = login
        user.email = email
        user.set_password(password)
        user.permissions = '0'
        db_session.add(user)
        db_session.commit()


def email_exist(email, db_session, User):
    with db_session.create_session() as db_session:
        users = db_session.query(User).filter(User.email == email)
    if len(list(users)) > 0:
        return True
    else:
        return False


def username_exist(username, db_session, User):
    with db_session.create_session() as db_session:
        users = db_session.query(User).filter(User.login == username)
    if len(list(users)) > 0:
        return True
    else:
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
        session.user_agent = request.headers.get('User-Agent')
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
    else:
        return False
    

def check_data_and_ua(session_data, db_session, Sessions, User):
    if datetime.now() < session_data.auth_date + timedelta(days=10):
        if request.headers.get('User-Agent') == session_data.user_agent:
            return True
        else:
            return False
    else:
        with db_session.create_session() as db_session:
            db_session.query(Sessions).filter(Sessions.session_key == session_data.session_key).delete()
            db_session.commit()
        return False
        

def auth_user_view(db_session, User, Sessions):
    cookie_data = request.cookies.get("session_key (DO NOT SHARE WITH ANYONE!)")
    base_button = '''
                    <div class="d-flex ms-auto">
                        <a href="/auth"><button type="button" class="btn btn-dark">Войти</button></a>
                    </div>
                    '''
    
    if cookie_data == None:
        return base_button
    
    with db_session.create_session() as db_session:
        try:
            session_data = db_session.query(Sessions).filter(Sessions.session_key == cookie_data).first()
            user = db_session.query(User).filter(User.id == session_data.user_id).first()
        except AttributeError:
            return base_button

        if datetime.now() > session_data.auth_date + timedelta(days=10):
            db_session.query(Sessions).filter(Sessions.session_key == cookie_data).delete()
            db_session.commit()
            return base_button
    
    if request.headers.get('User-Agent') != session_data.user_agent:
        return base_button
    
    if user.permissions == 'Admin':
        admin_link = '''<li><a class="dropdown-item" href="/admin-cabinet">Кабинет Администратора</a></li>'''
    else:
        admin_link = ''
    return f'''
        <div class="d-flex ms-auto">
            <div class="btn-group">
                <button type="button" class="btn btn-dark dropdown-toggle" data-bs-toggle="dropdown" data-bs-display="static" aria-expanded="false">
                    {user.login}
                </button>
                <ul class="dropdown-menu dropdown-menu-lg-end">
                    <li><a class="dropdown-item" href="/dashboard">Личный кабинет</a></li>
                    {admin_link}
                    <li><a class="dropdown-item" href="/auth/logout">Выйти</a></li>
                </ul>
            </div>
        </div>
        '''
        