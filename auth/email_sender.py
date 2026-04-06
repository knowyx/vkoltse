import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def sent_mail(reciver, code):
    # Параметры SMTP-сервера
    smtp_server = "smtp.timeweb.ru"
    port = 465
    sender_email = ""
    password = ""
    receiver_email = ""

    # Создаем объект сообщения
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Образование в кольце"

    # Добавляем текст письма
    with open("html/email/reset-password.html", mode='rt', encoding='UTF-8') as f:
        text = f.read()
    text = text.format(code=code)
    message.attach(MIMEText(text, "html"))

    # Подключаемся к серверу и отправляем письмо
    try:
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(sender_email, password)
            server.send_message(message)
            print("Письмо успешно отправлено!")
    except Exception as e:
        print(f"Возникла ошибка: {e}")