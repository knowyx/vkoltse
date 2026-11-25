"""This module contains functions for sending emails, it includes functions for
sending password reset emails and email confirmation emails, it uses the smtplib
library to send emails through an SMTP server, it also uses the email.mime
library to create email messages with HTML content"""

import logging
import os
import smtplib
import ssl
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.cfg_handler import get_config_data

SERVER = get_config_data("email-sending-server")
PORT = get_config_data("email-sending-port")

BASE_DIR = get_config_data("base-dir")


def sent_mail(message, address, password):
    """Function send email to an email address of recipient or print error"""
    stage = "connection"
    try:
        with smtplib.SMTP_SSL(
            SERVER, PORT, timeout=8, context=ssl.create_default_context()
        ) as server:
            stage = "authentication"
            server.login(address, password)
            stage = "submission"
            server.send_message(message)
            return True
    except (smtplib.SMTPException, OSError) as error:
        logging.getLogger(__name__).warning(
            "SMTP %s:%s failed during %s (%s, SMTP code %s)",
            SERVER, PORT, stage, type(error).__name__, getattr(error, "smtp_code", None),
        )
        return False


def build_mail(sender_email, subject, mail_content, reciver, plain_text):
    """Function to build mail structure with content"""
    try:
        message = MIMEMultipart("related")
        message["From"] = sender_email
        message["To"] = reciver
        message["Subject"] = subject + " | Образование в кольце"

        alt = MIMEMultipart("alternative")
        message.attach(alt)

        with open(
            os.path.join(os.path.join(BASE_DIR, "html/email"), "mail.html"),
            mode="rt",
            encoding="UTF-8",
        ) as f:
            text = f.read()
        text = text.format(
            custom_content=mail_content,
        )

        alt.attach(MIMEText(plain_text, "plain", "utf-8"))
        alt.attach(MIMEText(text, "html"))

        with open(os.path.join(BASE_DIR, "static/img/logo1000.png"), mode="rb") as f:
            img = MIMEImage(f.read(), _subtype="png")

        img.add_header("Content-ID", "<image1>")
        img.add_header("Content-Disposition", "inline", filename="logo.png")

        message.attach(img)
        return message
    except (OSError, TypeError, ValueError):
        return None