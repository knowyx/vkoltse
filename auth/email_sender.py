"""This module contains functions for sending emails, it includes functions for
sending password reset emails and email confirmation emails, it uses the smtplib
library to send emails through an SMTP server, it also uses the email.mime
library to create email messages with HTML content"""

import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ssl import SSLError

SERVER = "put here your mail server"
PORT = 465

BASE_URL = "base_dir of project deploy"


def sent_mail(sender_email, sender_pass, message):
    """Function send email to an email address of recipient or print error"""
    try:
        with smtplib.SMTP_SSL(SERVER, PORT) as server:
            server.login(sender_email, sender_pass)
            server.send_message(message)
            print("Письмо успешно отправлено!")
            return True
    except (smtplib.SMTPException, OSError, SSLError):
        return False


def build_mail(sender_email, subject, mail_content, reciver):
    """Function to build mail structure with content"""
    try:
        message = MIMEMultipart("related")
        message["From"] = sender_email
        message["To"] = reciver
        message["Subject"] = subject + " | Образование в кольце"

        alt = MIMEMultipart("alternative")
        message.attach(alt)

        with open(
            os.path.join(os.path.join(BASE_URL, "html/email"), "mail.html"),
            mode="rt",
            encoding="UTF-8",
        ) as f:
            text = f.read()
        text = text.format(
            custom_content=mail_content,
        )

        alt.attach(MIMEText("Текст письма", "plain"))
        alt.attach(MIMEText(text, "html"))

        with open(os.path.join(BASE_URL, "static/img/logo1000.png"), mode="rb") as f:
            img = MIMEImage(f.read(), _subtype="png")

        img.add_header("Content-ID", "<image1>")
        img.add_header("Content-Disposition", "inline", filename="logo.png")

        message.attach(img)
        return message
    except (OSError, TypeError, ValueError):
        return None
