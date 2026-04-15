from .blueprint import story_blueprint
from flask import render_template
from data import db_session
from data.stories import Stories
from .forms import StorySubmitForm

@story_blueprint.route("/story/submit", methods=["GET", "POST"])
def story_submit():
    form = StorySubmitForm()
    if form.validate_on_submit():
        connection_db = db_session.create_session()
    
    return render_template("story_submit.html", form=form)