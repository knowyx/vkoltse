import sys
import os
import traceback

BASE_DIR = "/home/knowyx/proj/py/vkoltse3/vkoltse"

sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "venv1/lib/python3.10/site-packages"))

print("WSGI START", file=sys.stderr)

try:
    from main import app

    from data import db_session
    from api.__init__api import init_api

    from auth import __init__auth
    from stories_handlers import blueprint as story_bp
    from cabinet import blueprint as cab_bp
    from news import blueprint as news_bp

    db_path = os.path.join(BASE_DIR, "db/data.db")
    print(f"DB PATH: {db_path}", file=sys.stderr)

    db_session.global_init(db_path)

    app.register_blueprint(__init__auth.blueprint)
    app.register_blueprint(story_bp.story_blueprint)
    app.register_blueprint(cab_bp.cabinet_blueprint)
    app.register_blueprint(news_bp.news_blueprint)

    init_api(app)

    #from werkzeug.debug import DebuggedApplication #debug
    #application = DebuggedApplication(app, evalex=True) #debug
    application = app

    print("WSGI READY", file=sys.stderr)

except Exception:
    print("WSGI FAILED", file=sys.stderr)
    #traceback.print_exc(file=sys.stderr) #debug
    raise