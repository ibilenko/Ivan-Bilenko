from service_email import ServiceEmail, SMTP_LOGIN, SMTP_PASS, SMTP_SERVER, SMTP_PORT, MAIL_FROM
from service_telegram import ServiceTelegram, BOT_TOKEN
from service_base import BaseNotifService


def get_notification_service(name):
    print(name)
    if name == 'email':
        return ServiceEmail(SMTP_SERVER, SMTP_LOGIN, SMTP_PASS, MAIL_FROM, server_port=SMTP_PORT)
    elif name == 'telegram':
        return ServiceTelegram(BOT_TOKEN)
    else:
        return BaseNotifService()
