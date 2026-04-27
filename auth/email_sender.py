"""This module contains functions for sending emails, it includes functions for
sending password reset emails and email confirmation emails, it uses the smtplib
library to send emails through an SMTP server, it also uses the email.mime
library to create email messages with HTML content"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import url_for

SERVER = "smtp.timeweb.ru"
PORT = 465

BASE_URL = "/home/knowyx/proj/py/vkoltse3/vkoltse/html/email"  # <- put abs path here


def sent_mail(sender_email, password, message, endpoint):
    """Function send email to an email address of recipient or print error"""
    try:
        with smtplib.SMTP_SSL(SERVER, PORT) as server:
            server.login(sender_email, password)
            server.send_message(message)
            print("Письмо успешно отправлено!")
    except smtplib.SMTPException as e:
        print(f"{endpoint} error! {e}")


def sent_resetpass_mail(reciver, code):
    """Function create email for reset password page with html code"""
    sender_email = ""
    password = ""

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = reciver
    message["Subject"] = "Восстановление пароля | Образование в кольце"

    with open(
        os.path.join(BASE_URL, "reset-password.html"), mode="rt", encoding="UTF-8"
    ) as f:
        text = f.read()
    text = text.format(
        code=code,
        img_path=url_for("static", filename="img/logo1000.png", _external=True),
    )
    message.attach(MIMEText(text, "html"))

    endpoint = "/auth/forgot-password"
    sent_mail(sender_email, password, message, endpoint)


def sent_confirm_mail(reciver, url_key, host):
    """Function create email for account confirm page with html code"""
    sender_email = ""
    password = ""

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = reciver
    message["Subject"] = "Подтверждение аккаунта | Образование в кольце"

    url = f"{host}auth/confirm-mail/confirm?key={url_key}"
    with open(
        os.path.join(BASE_URL, "confirm_mail.html"), mode="rt", encoding="UTF-8"
    ) as f:
        text = f.read()
    text = text.format(
        link=url,
        img_path=url_for("static", filename="img/logo1000.png", _external=True),
    )
    message.attach(MIMEText(text, "html"))

    endpoint = "/auth/confirm-mail"
    sent_mail(sender_email, password, message, endpoint)
