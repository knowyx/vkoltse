"""This module contains forms for news"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileSize
from wtforms import StringField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import Length


def empty_field_rus(_, field):
    """Validator function for WTForm. Reqire field to be filled (like DataRequired,
    but on Russian)"""
    if len(str(field.data)) == 0:
        raise ValidationError("Поле обязательно к заполнению.")


# pylint: disable=too-few-public-methods
class NewsSubmitForm(FlaskForm):
    """This class contains form for sending news (with file loading)"""

    title = StringField("Заголовок", validators=[empty_field_rus, Length(max=200)])
    content = TextAreaField("Текст", validators=[empty_field_rus])
    cover = FileField(
        "Обложка",
        validators=[
            FileAllowed(
                ["jpg", "png", "bmp", "svg", "jpeg", "webp"],
                "Файл должен быть картинкой. (jpg, png, bmp, svg, jpeg, webp).",
            ),
            FileSize(
                max_size=2 * 1024 * 1024,
                message="Размер файла не должен привышать 2 Мб.",
            ),
        ],
    )
    submit = SubmitField("Отправить")
