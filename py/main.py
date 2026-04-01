from flask import Flask, render_template, request
# from data import db_session

WEBDIRPATH = 'html/'

app = Flask(__name__, template_folder='../html', static_folder="../static")


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

if __name__ == "__main__":
    # db_session.global_init("../db/data.db")
    app.run(port=8080, host="127.0.0.1")