from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField
from wtforms.validators import DataRequired


class ForgotForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired()])
    submit = SubmitField('Отправить')
