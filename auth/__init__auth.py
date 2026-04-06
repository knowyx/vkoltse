from flask import Blueprint, redirect, render_template, make_response, request
from auth.auth_forms import RegisterForm, LoginForm, ForgotForm, SetupPasswordForm
from auth.handler import register_user, login_user, create_auth_session
from data import db_session
from data.users import Users
from data.sessions import Sessions
from secrets import randbelow
from auth.email_sender import sent_mail

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
        return redirect(f'/auth/forgot-password/setup?email={form.email.data}')
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


#@blueprint.route('/auth/forgot-password/setup', methods=['GET', 'POST'])
#def setup_password():
#    form = SetupPasswordForm()
#    if form.validate_on_submit():
#        if form.code.data == code:
#            print("111111")
#        print("0000")
#        return redirect('/login')
#    else:
#        code = randbelow(1000000)
#        sent_mail(request.args.get('email', None), code)
#    return render_template('auth/setup-password.html', pagename='Установка пароля', form=form)
