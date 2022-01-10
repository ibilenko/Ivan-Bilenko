import smtplib
from email.mime.text import MIMEText
from email.header import Header

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SMTP_LOGIN = "notify@vmarket.ru"
SMTP_PASS = "jwelkjrwofs"

MAIL_FROM = "notify@vmarket.ru"


# TODO Возможность обработать русские буквы
class ServiceEmail:
    def __init__(self, server, login, password, mail_from, server_port=587):
        self.server = server
        self.server_port = server_port

        self.login = login
        self.password = password

        self.mail_from = mail_from

    def send(self, target, msg, subject="Notify Service"):
        # msg = MIMEText(msg, 'plain', 'utf-8').as_string()
        server = smtplib.SMTP_SSL('smtp.yandex.com')
        # server.set_debuglevel(1)
        server.ehlo(self.login)
        server.login(self.login, SMTP_PASS)
        server.auth_plain()

        message = f"From: {self.login}\nTo: {target}\nSubject: {subject}\n\n{str(msg)}"
        server.sendmail(self.login, target, message)
        server.quit()


# GOOGLE
# server = smtplib.SMTP("smtp.gmail.com", 587)
# server.ehlo()
# server.starttls()
# server.login("login", "pass")
# message = "\r\n".join([
#     "From: от кого",
#     "To: кому",
#     "Subject: тема",
#     "",
#     str(text)
# ])
# server.sendmail("от кого", "кому", message)
# server.quit()

# YANDEX
# server = smtp.SMTP_SSL('smtp.yandex.com')
# server.set_debuglevel(1)
# server.ehlo(email)
# server.login(email, password)
# server.auth_plain()
# server.sendmail(email, dest_email, message)
# server.quit()

if __name__ == "__main__":
    notify = ServiceEmail()
    notify.send("aalakhn4@mts.ru", "MESSAGE")
