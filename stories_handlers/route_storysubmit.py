from .blueprint import story_blueprint
from flask import render_template, session, redirect
from data import db_session
from data.stories import Stories
from .forms import StorySubmitForm
from data.sessions import Sessions
from datetime import datetime

@story_blueprint.route("/story/submit", methods=["GET", "POST"])
def story_submit():
    user = get_current_user()
    if not user:
        return redirect("/auth/login")
    
    form = StorySubmitForm()
    print(form.errors)
    if form.validate_on_submit():
        connection_db = db_session.create_session()
        try:
            story = Stories(
                title=form.title.data,
                content=form.content.data,
                author_id=1,
                date=datetime.utcnow(),
                review_authors=0
            )
            connection_db.add(story)
            connection_db.commit()
        finally:
            connection_db.close()
            
        return render_template("story_submit.html", form=form, success=True)
    
    return render_template("story_submit.html", form=form)


def get_current_user():
    session_key = session.get("session_key")
    if not session_key:
        return None

    db_sess = db_session.create_session()
    sess = db_sess.query(Sessions).filter(
        Sessions.session_key == session_key
    ).first()

    if not sess:
        return None

    return sess.user