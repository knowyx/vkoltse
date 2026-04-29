"""This is the main file which initializes the app, sets up routes and error handlers,
and runs the app (without using a gunicorn (for develop purposes))"""

from flask import Flask, redirect, render_template, request

from api.__init__api import init_api
from auth import __init__auth
from auth.handler import auth_user_view
from data import db_session
from data.sessions import Sessions
from data.users import Users
from stories_handlers.blueprint import story_blueprint

app = Flask(__name__, template_folder="html", static_folder="static")
app.config["SECRET_KEY"] = "vkoltse_dev"


BASE_DIR = "base_dir of project deploy"


@app.route("/")
@app.route("/index")
def index():
    """route for index page, supports GET method, returns index page with user
    information if session exists, otherwise redirects to logout"""
    user = auth_user_view(db_session, Users, Sessions)
    if user == "Remove_cookie":
        return redirect("/auth/logout")
    return render_template("index.html", pagename="Главная", user=user)


@app.route("/about")
def about():
    """route for about page, supports GET method"""
    user = auth_user_view(db_session, Users, Sessions)
    if user == "Remove_cookie":
        return redirect("/auth/logout")
    return render_template("about.html", pagename="О проекте", user=user)


@app.errorhandler(403)
def err403(msg):
    """handler for 403 error, returns 403 page with error message and user
    information if session exists, otherwise redirects to logout"""
    user = auth_user_view(db_session, Users, Sessions)
    if user == "Remove_cookie":
        return redirect("/auth/logout")
    return render_template(
        "403.html", pagename="403. Forbidden", user=user, msg=msg.description
    )


@app.errorhandler(404)
def err404(_):
    """handler for 404 error, returns 404 page with error message and user
    information if session exists, otherwise redirects to logout"""
    user = auth_user_view(db_session, Users, Sessions)
    if user == "Remove_cookie":
        return redirect("/auth/logout")
    return render_template(
        "404.html", pagename="404. Not Found", addr=request.url, user=user
    )


def main():
    """main function, initializes database, registers blueprints and runs the app
    (develop, not using now)"""
    db_session.global_init("db/data.db")
    app.register_blueprint(__init__auth.blueprint)
    init_api(app)
    app.register_blueprint(story_blueprint)
    app.run(port=8080, host="127.0.0.1")


if __name__ == "__main__":
    main()
