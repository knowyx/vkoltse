from data import db_session
from data.stories import Stories
from .__init__ import story_blueprint
from flask import render_template, redirect, url_for
from .forms import StorySubmitForm


@story_blueprint.route('/story_submit')
def story_submit():
    form = StorySubmitForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        story = Stories(
            title=form.title.data,
            content=form.content.data,
            date=form.date.data
        )
        session.add(story)
        session.commit()
        
        return redirect(url_for('stories_list'))

    return render_template('story_submit.html', form=form)
