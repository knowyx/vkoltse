def register_user(login, email, password, session, User):
    user = User()
    user.login = login
    user.email = email
    user.set_password(password)
    user.permissions = '0'
    session = session.create_session()
    session.add(user)
    session.commit()
