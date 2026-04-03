from flask import Flask, render_template, request
from sqlalchemy.testing.pickleable import User
from werkzeug.utils import redirect

from py.auth_forms import LoginForm, RegisterForm, ForgotForm
from py.user_bd_handler import register_user
from data.users import Users
from data import db_session
from api.__init__api import init_api

app = Flask(__name__, template_folder='html', static_folder="static")
app.config['SECRET_KEY'] = 'vkoltse_dev'


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", pagename="Главная", usr=request.args.get('user', 'user'))


@app.route("/about")
def about():
    return render_template("about.html", pagename='О проекте')


@app.errorhandler(404)
def err404(junk):
    return render_template("404.html", pagename='404', addr=request.url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/index')
    return render_template('login.html', pagename='Авторизация', form=form)


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotForm()
    if form.validate_on_submit():
        return redirect('/login')
    return render_template('forgot-password.html', pagename='Сброс пароля', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        register_user(form.username.data, form.email.data, form.password.data, db_session, Users)
        return redirect('/index')
    return render_template('register.html', pagename='Регистрация', form=form)

def main():
    db_session.global_init("db/data.db")
    init_api(app)
    app.run(port=8080, host="127.0.0.1")

if __name__ == "__main__":
    main()
