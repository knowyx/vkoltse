from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms.validators import Length


def empty_field_rus(form, field):
    if len(str(field.data)) == 0:
        raise ValidationError("Поле обязательно к заполнению.")


class NewsSubmitForm(FlaskForm):
    title = StringField(
        'Заголовок',
        validators=[empty_field_rus, Length(max=200)]
    )
    content = TextAreaField(
        'Текст',
        validators=[empty_field_rus]
    )
    cover = FileField(
        'Обложка',
        validators=[FileAllowed(['jpg', 'png', 'bmp', 'svg', 'jpeg', 'webp'], 
                                'Файл должен быть картинкой. (jpg, png, bmp, svg, jpeg, webp).'),
                                FileSize(max_size=2 * 1024 * 1024, message='Размер файла не должен привышать 2 Мб.')]
    )
    submit = SubmitField('Отправить')