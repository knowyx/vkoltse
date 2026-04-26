from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import Length


def empty_field_rus(form, field): # validator for checking if field is empty, with error message in Russian
    if len(str(field.data)) == 0:
        raise ValidationError("Поле обязательно к заполнению.")


class StorySubmitForm(FlaskForm): # form for submitting stories, contains title and content fields, with validators for checking if fields are empty and if title is not too long
    title = StringField(
        'Заголовок',
        validators=[empty_field_rus, Length(max=200)]
    )
    content = TextAreaField(
        'Текст',
        validators=[empty_field_rus]
    )
    submit = SubmitField('Отправить')