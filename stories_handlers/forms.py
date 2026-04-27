"This module contains forms for stories_handlers " ""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import Length


def empty_field_rus(_, field):
    """Validator function for WTForm. Reqire field to be filled (like DataRequired,
    but on Russian)"""
    if len(str(field.data)) == 0:
        raise ValidationError("Поле обязательно к заполнению.")


# pylint: disable=too-few-public-methods
class StorySubmitForm(FlaskForm):
    """Form for submitting stories, contains title and content fields, with validators
    for checking if fields are empty and if title is not too long"""

    title = StringField("Заголовок", validators=[empty_field_rus, Length(max=200)])
    content = TextAreaField("Текст", validators=[empty_field_rus])
    submit = SubmitField("Отправить")
