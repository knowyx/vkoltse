from flask import Blueprint, redirect, render_template, make_response, request
from auth.auth_forms import RegisterForm, LoginForm, ForgotForm, SetupPasswordForm, ConfirmMailForm
from auth.handler import register_user, login_user, create_auth_session, create_resetpass_key, get_token_data
from auth.handler import update_password, check_cookie_exist, get_user_info_by_session, create_confirm_key, confirm_user, auth_user_view
from data import db_session
from data.users import Users
from data.sessions import Sessions
from data.email_tokens import EmailTokens
from auth.captcha_check import check_captcha



blueprint = Blueprint(
    'auth',
    __name__,
    template_folder="html/auth"
)


@blueprint.route('/auth')
def authREDIR():
    if check_cookie_exist():
        return redirect("/")
    return redirect('/auth/login')


@blueprint.route('/auth/login', methods=['GET', 'POST'])
def login():
    if check_cookie_exist():
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        if check_captcha(request.form.get("smart-token"), request.remote_addr):
            if login_user(form.email.data, form.password.data, db_session, Users):
                session_key = create_auth_session(form.email.data, db_session, Sessions, Users)
                res = make_response('', 302)
                res.headers["Location"] = '/index'
                res.set_cookie("session_key (DO NOT SHARE WITH ANYONE!)", session_key, 10 * 24 * 60 * 60, httponly=True)
                return res
            else:
                return redirect('/auth/login?err=invcreds')
        else:
            return redirect('/auth/login?err=captcha')
    return render_template('auth/login.html', pagename='Авторизация', form=form,  err=request.args.get('err', None))


@blueprint.route('/auth/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if check_cookie_exist():
        return redirect("/")
    form = ForgotForm(session=db_session)
    if form.validate_on_submit():
        if check_captcha(request.form.get("smart-token"), request.remote_addr):
            url_key = create_resetpass_key(form.email.data, db_session, Users, EmailTokens)
            return redirect(f'/auth/forgot-password/setup?key={url_key}')
        else:
            return redirect("/auth/forgot-password?err=captcha")
    return render_template('auth/forgot-password.html', pagename='Сброс пароля', form=form, err=request.args.get('err', None))


@blueprint.route('/auth/register', methods=['GET', 'POST'])
def register():
    if check_cookie_exist():
        return redirect("/")
    form = RegisterForm(session=db_session)
    if form.validate_on_submit():
        if check_captcha(request.form.get("smart-token"), request.remote_addr):
            register_user(form.username.data, form.email.data, form.password.data, db_session, Users)
            session_key = create_auth_session(form.email.data, db_session, Sessions, Users)
            res = make_response('', 302)
            res.headers["Location"] = '/index'
            res.set_cookie("session_key (DO NOT SHARE WITH ANYONE!)", session_key, 10 * 24 * 60 * 60, httponly=True)
            return res
        else:
            return redirect("/auth/register?err=captcha")
    return render_template('auth/register.html', pagename='Регистрация', form=form, err=request.args.get('err', None))


@blueprint.route('/auth/logout')
def logout():
    res = make_response('', 302)
    res.headers["Location"] = '/index'
    res.set_cookie("session_key (DO NOT SHARE WITH ANYONE!)", '', 0)
    return res


@blueprint.route('/auth/forgot-password/setup', methods=['GET', 'POST'])
def setup_password():
    if check_cookie_exist():
        return redirect("/")
    url_key = request.args.get('key', None)
    token = get_token_data(db_session, url_key, Users, EmailTokens)
    if not token:    #если полученная в результате get_token_data структура пуста (т.е. выборка из базы пуста)
        return redirect("/")
    form = SetupPasswordForm(session=db_session, url_key=url_key)
    if form.validate_on_submit():
        if check_captcha(request.form.get("smart-token"), request.remote_addr):
            update_password(db_session, url_key, form.password.data, EmailTokens, Users)
            return redirect("/auth/login")
        else:
            return redirect(f"/auth/forgot-password/setup?err=captcha&key={url_key}")
    return render_template('auth/setup-password.html', pagename='Установка пароля', form=form, err=request.args.get('err', None))


@blueprint.route('/auth/confirm-mail', methods=['GET', 'POST'])
def confirm_mail_sent():
    if not check_cookie_exist():
        return redirect("/")
    try:
        session_key = request.cookies.get("session_key (DO NOT SHARE WITH ANYONE!)")
        user = get_user_info_by_session(db_session, session_key, Users, Sessions)
    except AttributeError:
        return redirect("/")
    if user.is_confirmed:
        return redirect("/")
    user_button = auth_user_view(db_session, Users, Sessions)
    if user == 'Remove_cookie':
        return redirect("/auth/logout")
    form = ConfirmMailForm(session=db_session, email=user.email)
    if form.validate_on_submit():
        if check_captcha(request.form.get("smart-token"), request.remote_addr):
            create_confirm_key(user, db_session, EmailTokens)
            return render_template("auth/confirm_mail_success_sent.html", pagename="Подтверждение аккаунта")
        else:
            return redirect("/auth/confirm-mail?err=captcha")
    return render_template("auth/confirm_mail_sent.html", pagename="Подтверждение аккаунта", form=form, 
                           err=request.args.get('err', None), 
                           username=get_user_info_by_session(db_session, session_key, Users, Sessions).login, user=user_button)


@blueprint.route('/auth/confirm-mail/confirm')
def confirm_mail_final():
    if not check_cookie_exist():
        return redirect("/")
    try:
        session_key = request.cookies.get("session_key (DO NOT SHARE WITH ANYONE!)")
        user = get_user_info_by_session(db_session, session_key, Users, Sessions)
    except AttributeError:
        return redirect("/")
    if user.is_confirmed:
        return redirect("/")
    user_button = auth_user_view(db_session, Users, Sessions)
    if user == 'Remove_cookie':
        return redirect("/auth/logout")
    res = confirm_user(db_session, request.args.get('key', None), EmailTokens, Users)
    if res:
        return render_template("auth/confirm_mail_final_success.html", pagename="Подтверждение аккаунта", user=user_button)
    else:
        return render_template("auth/confirm_mail_final_fail.html", pagename="Подтверждение аккаунта", user=user_button)
