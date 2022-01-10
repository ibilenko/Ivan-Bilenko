from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import telebot
from telebot import types
import pandas as pd
from telebot.types import LabeledPrice
import requests

import telegram

bot = telebot.TeleBot('2015622992:AAHYO27kxQ4uYOlwYMsRWBU55_12mFSPfS0')


class main:
    unread_df = False
    db_string = "postgresql://postgres:sjvnfi_LFMR740@internal.cfnsbden5utu.us-east-2.rds.amazonaws.com:5432/"
    engine = create_engine(db_string, pool_size=10, max_overflow=20)
    client_name = ''
    kb_dialog = telebot.types.InlineKeyboardMarkup()
    kb_main = telebot.types.InlineKeyboardMarkup()
    kb_main.add(telebot.types.InlineKeyboardButton('Отобрать лидов', callback_data='lead'))
    kb_main.add(telebot.types.InlineKeyboardButton('Отправка писем', callback_data='messanger'))
    kb_message = telebot.types.InlineKeyboardMarkup()
    kb_message.add(telebot.types.InlineKeyboardButton('Выбрать из шаблона', callback_data='template'))
    kb_message.add(telebot.types.InlineKeyboardButton('Написать новое', callback_data='send'))
    kb_unread_mode = telebot.types.InlineKeyboardMarkup()
    kb_unread_mode.add(telebot.types.InlineKeyboardButton('answer', callback_data='answer'),
                       telebot.types.InlineKeyboardButton('wait', callback_data='wait'),
                       telebot.types.InlineKeyboardButton('skip', callback_data='skip'))

    mode = 0  # 1 - лиды, 2 - непрочитанные, 3 - отправка
    client_name = False
    acc_name = False
    markup = types.ReplyKeyboardMarkup()
    markup.add('next')

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, f'Привет! что хочешь сделать?', reply_markup=main.kb_main)
        #bot.send_photo(message.chat.id, 'https://genlead.s3.us-east-2.amazonaws.com/first.png')
        bot.send_photo(message.chat.id,'https://w-dog.ru/wallpapers/11/5/499834462083843/gora-ozero-voda-vetki-kamni.jpg')

    @bot.message_handler(content_types=['text'])
    def send_screen(message):
        if message.text == 'next' and main.mode == 1:
            df = pd.read_sql("""select po.name, screenshots from link.potential_clients po
                        join link.connections c on c.name = po.name
                        where po.screenshots is not null
                        and target is null 
                        limit 1""", main.engine)
            if df.empty:
                bot.send_message(message.chat.id, f'Лиды закончились', reply_markup=main.kb_main)
            main.client_name = df['name'][0]
            screenshots = df['screenshots'][0]
            screenshot_2 = screenshots.split(';')[0]
            screenshot_1 = screenshots.split(';')[1]
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('yes', callback_data='yes'),
                telebot.types.InlineKeyboardButton('no', callback_data='no')
            )
            keyboard.add(telebot.types.InlineKeyboardButton('skip', callback_data='skip'))
            keyboard.add(telebot.types.InlineKeyboardButton('message', callback_data='message'))
            bot.send_photo(message.chat.id, photo=open(screenshot_1, 'rb'))
            bot.send_photo(message.chat.id, photo=open(screenshot_2, 'rb'), reply_markup=keyboard)


    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        user_id = call.message.chat.id
        if call.data == "lead":
            main.mode = 1
            bot.send_message(call.message.chat.id, f'Нажмите next', reply_markup=main.markup)
        if call.data == "messanger":
            main.mode = 2
            df = pd.read_sql("""select * from link.un_messages""", main.engine)
            main.unread_df = df
            print(main.unread_df)
            for i in range(len(main.unread_df)):
                main.kb_dialog.add(
                    telebot.types.InlineKeyboardButton(f"{df['name'][i]}(account {df['acc_name'][i]})",
                                                       callback_data=f"{df['name'][i]}"))
            bot.send_message(call.message.chat.id, text='Names of diaolgs', reply_markup=main.kb_dialog)
        if call.data == "yes":
            main.engine.connect().execute(
                f"""update link.potential_clients set target = 'yes' where name = '{main.client_name}'""", main.engine)
            msg = bot.send_message(call.message.chat.id, text=f"Зафиксировал 'yes' в базе")
        if call.data == "no":
            main.engine.connect().execute(
                f"""update link.potential_clients set target = 'no' where name = '{main.client_name}'""", main.engine)
            msg = bot.send_message(call.message.chat.id, text=f"Зафиксировал 'no' в базе")
        if call.data == "skip":
            main.engine.connect().execute(
                f"""update link.potential_clients set target = 'split' where name = '{main.client_name}'""",
                main.engine)
            msg = bot.send_message(call.message.chat.id, text=f"Зафиксировал 'skip' в базе")
        if call.data == "send":
            main.mode = 3
            msg = bot.send_message(call.message.chat.id, text=f"Напиши текст")
        if main.unread_df:
            print(main.unread_df)
            for i in range(len(main.unread_df)):
                if call.data == main.unread_df['name'][i]:
                    main.client_name = main.unread_df['name'][i]
                    main.acc_name = main.unread_df['acc_name'][i]
                    bot.send_message(call.message.chat.id, text={main.unread_df['dialog'][i]},
                                     reply_markup=main.kb_unread_mode, parse_mode=telegram.ParseMode.MARKDOWN)
        if call.data == "wait":
            bot.send_message(call.message.chat.id, text='*Dialogs*', reply_markup=main.kb_dialog)
        if call.data == "answer":
            bot.send_message(call.message.chat.id, text='Write your message:')
            main.mode = 3
        # if call.data == "skip":
        #     main.engine.connect().execute(
        #         f"""update link.potential_clients set target = 'yes' where name = '{main.client_name}'""", main.engine)


bot.polling()