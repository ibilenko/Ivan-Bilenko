from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import telebot
from telebot import types
import pandas as pd
from telebot.types import LabeledPrice
import requests
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import telegram
from datetime import datetime

bot = telebot.TeleBot('2076202639:AAEJpWaBdbykAvs2l051at--aUXyGRB7nWk')

class main:
    db_string = "postgresql://postgres:sjvnfi_LFMR740@internal.cfnsbden5utu.us-east-2.rds.amazonaws.com:5432/"
    engine = create_engine(db_string, pool_size=10, max_overflow=20)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Обновить"))


    kb_ask = telebot.types.InlineKeyboardMarkup()
    kb_ask.add(telebot.types.InlineKeyboardButton('Да!', callback_data='yes'),
                   telebot.types.InlineKeyboardButton('Нет', callback_data='no'))
    kb_category = telebot.types.InlineKeyboardMarkup()
    kb_category.add(telebot.types.InlineKeyboardButton('Kalinka', callback_data='Kalinka'),
                       telebot.types.InlineKeyboardButton('Ayboost', callback_data='Ayboost'),
                       telebot.types.InlineKeyboardButton('Фриланс', callback_data='Фриланс'))
    link = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']  # задаем ссылку на Гугл таблици
    my_creds = ServiceAccountCredentials.from_json_keyfile_name('gogol.json',link)  # формируем данные для входа из нашего json файла
    client = gspread.authorize(my_creds)  # запускаем клиент для связи с таблицами
    sheet1 = client.open('Бабки малышки').worksheet("Kalinka")
    sheet2 = client.open('Бабки малышки').worksheet("Ayboost")
    sheet3 = client.open('Бабки малышки').worksheet("Фриланс")
    sheet4 = client.open('Бабки малышки').worksheet("История")
    mode = True
    client = False
    project = False
    count = 0
    task = ''
    client_name = ''
    _dict = {"Kalinka":sheet1,
             "Ayboost":sheet2,
             "Фриланс":sheet3}
    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, f'Жду таск', reply_markup=main.markup)
        main.mode = True

    @bot.message_handler(content_types=['text'])
    def send_screen(message):
        if message.text == 'Обновить':
            bot.send_message(message.chat.id, f'Уверена?', reply_markup=main.kb_ask)
        else:
            if main.mode:
                main.task = message.text
                bot.send_message(message.chat.id, f'Какой проект?', reply_markup=main.kb_category)
                main.mode = False
            if main.client:
                main.client_name = message.text
                main.engine.connect().execute(f"""insert into malysh.tasks values ('{main.task}','{main.project}','{main.client_name}','{datetime.now().replace(microsecond=0)}')""")
                df1 = pd.read_sql(f"select * from malysh.tasks where project = '{main.project}'",main.engine)
                main._dict[main.project].update([df1.columns.values.tolist()] + df1.values.tolist())
                bot.send_message(message.chat.id, f'Запихнул в шиты')
                main.client = False
                main.mode = True


    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        user_id = call.message.chat.id
        if call.data == "Kalinka":
            main.project = "Kalinka"
            bot.send_message(call.message.chat.id, f'Напиши имя заказчика')
            main.client = True
        if call.data == "Ayboost":
            main.project = "Ayboost"
            bot.send_message(call.message.chat.id, f'Напиши имя заказчика')
            main.client = True
        if call.data == "Фриланс":
            main.project = "Фриланс"
            bot.send_message(call.message.chat.id, f'Напиши имя заказчика')
            main.client = True
        if call.data == 'yes':
            main.engine.connect().execute(f"""insert into malysh.history (select * from malysh.tasks)""")
            main.engine.connect().execute(f"""truncate malysh.tasks""")
            main.sheet1.clear()
            print(1)
            main.sheet2.clear()
            print(2)
            main.sheet3.clear()
            print(3)
            main.sheet4.clear()
            print(4)
            df = pd.read_sql("""select * from malysh.history""",main.engine)
            print(df)
            main.sheet4.update([df.columns.values.tolist()] + df.values.tolist())
            print('update')
            bot.send_message(user_id, 'Очистил листы.')

            bot.send_message(user_id, 'Продолжаем работать, жду название задачи!')
        if call.data == 'no':
            bot.send_message(user_id, 'Продолжаем работать, жду название задачи')



bot.polling()