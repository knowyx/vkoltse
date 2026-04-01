import smtplib

smtpObj = smtplib.SMTP('smtp.yandex.ru', 587)
smtpObj.starttls()
smtpObj.login('','')
smtpObj.sendmail("","","hello world")
smtpObj.quit()