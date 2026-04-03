from flask import Flask, render_template, request
from sqlalchemy.testing.pickleable import User

from auth import __init__auth
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


def main():
    db_session.global_init("db/data.db")
    app.register_blueprint(__init__auth.blueprint)
    init_api(app)
    app.run(port=8080, host="127.0.0.1")
    

if __name__ == "__main__":
    main()
