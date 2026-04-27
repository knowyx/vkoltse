# This module contains forms for authentication, it includes forms for registration, login, password reset and email confirmation, it also includes custom validators for these forms
from re import escape, fullmatch

from flask_wtf import FlaskForm
from wtforms import (EmailField, IntegerField, PasswordField, StringField,
                     SubmitField, ValidationError)
from wtforms.validators import DataRequired

from auth.handler import (check_email_code, email_exist,
                          have_tokens_in_interval_email, username_exist)
from data.email_tokens import EmailTokens
from data.users import Users


def validate_password_match(form, field):
    if field.data != form.password.data:
        raise ValidationError("Введенные пароли не совпадают!")


def empty_field_rus(form, field):
    if len(str(field.data)) == 0:
        raise ValidationError("Поле обязательно к заполнению.")


def easy_password(form, field):
    syms = "!@#$%^&*()_+-?="
    pattern = (
        "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*["
        + escape(syms)
        + "])[A-Za-z\\d"
        + escape(syms)
        + "]{8,}$"
    )
    if not fullmatch(pattern, field.data):
        raise ValidationError("Пароль слишком простой.")


class RegisterForm(FlaskForm):
    def __init__(self, *args, session=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = session

    username = StringField("Имя пользователя", validators=[empty_field_rus])
    email = EmailField("Электронная почта", validators=[empty_field_rus])
    password = PasswordField("Пароль", validators=[empty_field_rus, easy_password])
    repeat_password = PasswordField(
        "Пароль (еще раз)", validators=[empty_field_rus, validate_password_match]
    )
    submit = SubmitField("Зарегестрироваться")

    def validate_email(self, field):
        if email_exist(field.data, self.session, Users):
            raise ValidationError(
                f'Пользователь с почтой "{field.data}" уже зарегестрирован!'
            )

    def validate_username(self, field):
        if username_exist(field.data, self.session, Users):
            raise ValidationError(
                f'Пользователь с именем "{field.data}" уже зарегестрирован!'
            )


class LoginForm(FlaskForm):
    email = EmailField("Электронная почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class ForgotForm(FlaskForm):
    def __init__(self, *args, session=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = session

    email = EmailField("Электронная почта", validators=[empty_field_rus])
    submit = SubmitField("Отправить")

    def validate_email(self, field):
        if not email_exist(field.data, self.session, Users):
            raise ValidationError(
                f'Пользователь с почтой "{field.data}" не зарегестрирован.'
            )

        if have_tokens_in_interval_email(
            self.session, field.data, Users, EmailTokens, typ=0
        ):
            raise ValidationError(
                "Предыдущий запрос на сброс пароля был отправлен менее, чем 10 минут назад. "
                + "Проверьте электронную почту."
            )


class SetupPasswordForm(FlaskForm):
    def __init__(self, *args, session=None, url_key, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = session
        self.url_key = url_key

    code = IntegerField("Одноразовый код", validators=[empty_field_rus])
    password = PasswordField("Пароль", validators=[empty_field_rus, easy_password])
    repeat_password = PasswordField(
        "Пароль (еще раз)", validators=[empty_field_rus, validate_password_match]
    )
    submit = SubmitField("Установить новый пароль")

    def validate_code(self, field):
        if not check_email_code(self.session, field.data, self.url_key, EmailTokens):
            raise ValidationError(f"Неверный код. Попробуйте ввести заново.")


class ConfirmMailForm(FlaskForm):
    def __init__(self, *args, session=None, email, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = session
        self.email = email

    submit = SubmitField("Продолжить")

    def validate_submit(self, field):
        if have_tokens_in_interval_email(
            self.session, self.email, Users, EmailTokens, typ=1
        ):
            raise ValidationError(
                "Предыдущий запрос на подтверждение аккаунта был отправлен менее, чем 10 минут назад. "
                + "Проверьте электронную почту."
            )
