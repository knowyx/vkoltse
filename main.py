from flask import Flask, render_template, request, redirect
from sqlalchemy.testing.pickleable import User

from auth import __init__auth
from data.users import Users
from data.sessions import Sessions
from data import db_session
from api.__init__api import init_api
from auth.handler import auth_user_view
import stories_handlers

app = Flask(__name__, template_folder='html', static_folder="static")
app.config['SECRET_KEY'] = 'vkoltse_dev'


@app.route("/")
@app.route("/index")
def index():
    user = auth_user_view(db_session, Users, Sessions)
    if user == 'Remove_cookie':
        return redirect("/auth/logout")
    return render_template("index.html", pagename="Главная", user=user)


@app.route("/about")
def about():
    user = auth_user_view(db_session, Users, Sessions)
    if user == 'Remove_cookie':
        return redirect("/auth/logout")
    return render_template("about.html", pagename='О проекте', user=user)


@app.errorhandler(404)
def err404(junk):
    user = auth_user_view(db_session, Users, Sessions)
    if user == 'Remove_cookie':
        return redirect("/auth/logout")
    return render_template("404.html", pagename='404', addr=request.url, user=user)


def main():
    db_session.global_init("db/data.db")
    app.register_blueprint(__init__auth.blueprint)
    init_api(app)
    app.register_blueprint(stories_handlers.story_blueprint)
    app.run(port=8080, host="127.0.0.1")
    

if __name__ == "__main__":
    main()
