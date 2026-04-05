from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, ValidationError
from wtforms.validators import DataRequired
from auth.handler import email_exist, username_exist
from data.users import Users


def validate_password_match(form, field):
    if field.data != form.password.data:
        raise ValidationError('Введенные пароли не совпадают!')
        

def empty_field_rus(form, field):
    if len(field.data) == 0:
        raise ValidationError("Поле обязательно к заполнению.")


class RegisterForm(FlaskForm):
    def __init__(self, *args, session=None, **kwargs):
        super().__init__(*args, **kwargs) 
        self.session = session

    username = StringField('Имя пользователя', validators=[empty_field_rus])
    email = EmailField('Электронная почта', validators=[empty_field_rus])
    password = PasswordField('Пароль', validators=[empty_field_rus])
    repeat_password = PasswordField('Пароль (еще раз)', validators=[empty_field_rus, validate_password_match])
    submit = SubmitField('Зарегестрироваться')

    def validate_email(self, field):
        if email_exist(field.data, self.session, Users):
            raise ValidationError(f'Пользователь с почтой "{field.data}" уже зарегестрирован!')
    
    def validate_username(self, field):
        if username_exist(field.data, self.session, Users):
            raise ValidationError(f'Пользователь с именем "{field.data}" уже зарегестрирован!')


class LoginForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')        


class ForgotForm(FlaskForm):
    def __init__(self, *args, session=None, **kwargs):
        super().__init__(*args, **kwargs) 
        self.session = session
        
    email = EmailField('Электронная почта', validators=[empty_field_rus])
    submit = SubmitField('Отправить')

    def validate_email(self, field):
        if not email_exist(field.data, self.session, Users):
            raise ValidationError(f'Пользователь с почтой "{field.data}" не зарегестрирован.')
