import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import url_for

SERVER = "smtp.timeweb.ru"
PORT = 465


def sent_mail(sender_email, password, message):
    try:
        with smtplib.SMTP_SSL(SERVER, PORT) as server:
            server.login(sender_email, password)
            server.send_message(message)
            print("Письмо успешно отправлено!")
    except Exception as e:
        print(f"Возникла ошибка: {e}")


def sent_resetpass_mail(reciver, code):
    sender_email = ""
    password = ""

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = reciver
    message["Subject"] = "Восстановление пароля | Образование в кольце"
    
    with open("html/email/reset-password.html", mode='rt', encoding='UTF-8') as f:
        text = f.read()
    text = text.format(code=code, img_path=url_for('static', filename='img/logo.svg'))
    message.attach(MIMEText(text, "html"))

    sent_mail(sender_email, password, message)


def sent_confirm_mail(reciver, url_key, host):
    sender_email = ""
    password = ""

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = reciver
    message["Subject"] = "Подтверждение аккаунта | Образование в кольце"
    
    url = f"{host}auth/confirm-mail/confirm?key={url_key}"
    with open("html/email/confirm_mail.html", mode='rt', encoding='UTF-8') as f:
        text = f.read()
    text = text.format(link=url, img_path=url_for('static', filename='img/logo.svg'))
    message.attach(MIMEText(text, "html"))

    sent_mail(sender_email, password, message)