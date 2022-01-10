import time
from datetime import datetime
import requests

BOT_NAME = "tbpy_bot"
BOT_TOKEN = "1928659548:AAEMc3Q-f-k459cWSc0oWzGGNGfazBPKuOI"
BASE_URL = "https://api.telegram.org/bot"


class ServiceTelegram:
    def __init__(self, token):
        self.token = token

    def send(self, target, msg):
        method = "sendMessage"
        url = f"{BASE_URL}{self.token}/{method}"
        data = {
            "chat_id": target,
            "text": msg
        }
        requests.post(url, data=data)

    def delete_webhook(self):
        method = "deleteWebhook"
        response = requests.get(f"{BASE_URL}{self.token}/{method}", timeout=60)
        if response.status_code != 200:
            print(response.json())
        return response

    # Функция для поиска канала для отправки сообщений
    def long_pooling(self):
        method = "getUpdates"
        while True:
            response = requests.get(f"{BASE_URL}{self.token}/{method}", timeout=60)
            print(response.json())
            time.sleep(5)


if __name__ == "__main__":
    user_chat_id = 2194759
    channel_chat_id = -433592576

    tg = ServiceTelegram(BOT_TOKEN)
    # tg.delete_webhook()
    # tg.long_pooling()

    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    tg.send(user_chat_id, f"Chat Test: date and time {date_time}")
    tg.send(channel_chat_id, f"Group Test: date and time {date_time}")
