from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length

class StorySubmitForm(FlaskForm):
    title = StringField(
        'Заголовок',
        validators=[DataRequired(), Length(max=200)]
    )
    content = TextAreaField(
        'Текст',
        validators=[DataRequired()]
    )
    date = DateTimeField(
        'Дата',
        format='%Y-%m-%d %H:%M',
        validators=[DataRequired()]
    )
    submit = SubmitField('Отправить')