import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import url_for


def sent_mail(reciver, code):
    smtp_server = "smtp.timeweb.ru"
    port = 465
    sender_email = ""
    password = ""

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = reciver
    message["Subject"] = "Образование в кольце"
    
    with open("html/email/reset-password.html", mode='rt', encoding='UTF-8') as f:
        text = f.read()
    text = text.format(code=code, img_path=url_for('static', filename='img/logo.svg'))
    message.attach(MIMEText(text, "html"))

    try:
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(sender_email, password)
            server.send_message(message)
            print("Письмо успешно отправлено!")
    except Exception as e:
        print(f"Возникла ошибка: {e}")
