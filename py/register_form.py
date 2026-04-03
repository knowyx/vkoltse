from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    email = EmailField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
