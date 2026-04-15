from flask import render_template
from data import db_session
from .blueprint import story_blueprint
from data.stories import Stories
from sqlalchemy.orm import joinedload

@story_blueprint.route("/stories_list")
def show_stories():
    session = db_session.create_session()
    try:
        stories = session.query(Stories).options(
            joinedload(Stories.author),
            joinedload(Stories.review_authors)
        ).all()
        return render_template(
            "stories_list.html",
            stories=stories,
            pagename="Истории"
        )
    finally:
        session.close()