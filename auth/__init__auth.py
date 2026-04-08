from flask import Blueprint, redirect, render_template, make_response, request
from auth.auth_forms import RegisterForm, LoginForm, ForgotForm, SetupPasswordForm
from auth.handler import register_user, login_user, create_auth_session, create_resetpass_key, get_token_data, update_password
from data import db_session
from data.users import Users
from data.sessions import Sessions
from data.email_tokens import EmailTokens

blueprint = Blueprint(
    'auth',
    __name__,
    template_folder="html/auth"
)


@blueprint.route('/auth')
def auth():
    return redirect('/auth/login')


@blueprint.route('/auth/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(request.form.get("smart-token"))
        if login_user(form.email.data, form.password.data, db_session, Users):
            session_key = create_auth_session(form.email.data, db_session, Sessions, Users)
            res = make_response('', 302)
            res.headers["Location"] = '/index'
            res.set_cookie("session_key (DO NOT SHARE WITH ANYONE!)", session_key, 10 * 24 * 60 * 60, httponly=True)
            return res
        else:
            return redirect('/auth/login?err')
    return render_template('auth/login.html', pagename='Авторизация', form=form,  err=request.args.get('err', None))


@blueprint.route('/auth/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotForm(session=db_session)
    if form.validate_on_submit():
        url_key = create_resetpass_key(form.email.data, db_session, Users, EmailTokens)
        return redirect(f'/auth/forgot-password/setup?key={url_key}')
    return render_template('auth/forgot-password.html', pagename='Сброс пароля', form=form)


@blueprint.route('/auth/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(session=db_session)
    if form.validate_on_submit():
        register_user(form.username.data, form.email.data, form.password.data, db_session, Users)
        session_key = create_auth_session(form.email.data, db_session, Sessions, Users)
        res = make_response('', 302)
        res.headers["Location"] = '/index'
        res.set_cookie("session_key (DO NOT SHARE WITH ANYONE!)", session_key, 10 * 24 * 60 * 60, httponly=True)
        return res
    return render_template('auth/register.html', pagename='Регистрация', form=form)


@blueprint.route('/auth/logout')
def logout():
    res = make_response('', 302)
    res.headers["Location"] = '/index'
    res.set_cookie("session_key (DO NOT SHARE WITH ANYONE!)", '', 0)
    return res



@blueprint.route('/auth/forgot-password/setup', methods=['GET', 'POST'])
def setup_password():
    url_key = request.args.get('key', None)
    token = get_token_data(db_session, url_key, Users, EmailTokens)
    if not token:    #если полученная в результате get_token_data структура пуста (т.е. выборка из базы пуста)
        return redirect("/")
    form = SetupPasswordForm(session=db_session, url_key=url_key)
    if form.validate_on_submit():
        update_password(db_session, url_key, form.password.data, EmailTokens, Users)
        return redirect("/auth/login")
    return render_template('auth/setup-password.html', pagename='Установка пароля', form=form)